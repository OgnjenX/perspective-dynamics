"""Run the prospectively specified EXP009 controls and criteria."""

from __future__ import annotations

import json
from pathlib import Path

from perspective_dynamics.compositional_emergence import (
    generalized_schemas,
    generalized_tasks,
    perspective_erased,
    run_random_schema_selection,
    scramble_task,
    training_experiences,
)
from perspective_dynamics.schema_composition import CompositionResult, SchemaCompositionEngine

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"


def _step(step) -> dict[str, object]:
    return {
        "action": step.action,
        "perspective": step.perspective,
        "schema": step.schema,
        "produced_relation": step.produced,
        "consumed_relation": step.enabled_by,
    }


def _event(task: str, condition: str, result: CompositionResult, **extra) -> dict[str, object]:
    return {
        "experiment": "EXP009", "task": task, "condition": condition,
        "success": result.success, "reason": result.reason,
        "explored_states": result.explored_states,
        "schema_checks": result.schema_checks,
        "trajectory": [_step(step) for step in result.steps],
        **extra,
    }


def main() -> None:
    parameters = json.loads((ROOT / "parameters.json").read_text(encoding="utf-8"))
    schemas = generalized_schemas()
    structured_engine = SchemaCompositionEngine(schemas)
    ordinary_engine = SchemaCompositionEngine(perspective_erased(schemas))
    originals = generalized_tasks()
    tasks = tuple(
        item
        for task in originals
        for item in (task, scramble_task(task, parameters["name_scramble_seed"]))
    )
    events: list[dict[str, object]] = []
    structured_by_task: dict[str, CompositionResult] = {}
    ordinary_by_task: dict[str, CompositionResult] = {}

    for task in tasks:
        structured = structured_engine.solve(task.world, task.goal)
        structured_by_task[task.name] = structured
        events.append(_event(task.name, "structured", structured))

        for perspective in sorted({schema.perspective for schema in schemas}):
            result = structured_engine.solve(
                task.world, task.goal,
                perspectives=(perspective,), mode="single",
            )
            events.append(_event(
                task.name, "single_perspective", result,
                selected_perspective=perspective,
            ))

        pooled = structured_engine.solve(task.world, task.goal, mode="pool")
        events.append(_event(task.name, "pooled_without_composition", pooled))

        ordinary = ordinary_engine.solve(task.world, task.goal)
        ordinary_by_task[task.name] = ordinary
        events.append(_event(task.name, "ordinary_forward_planner", ordinary))

        for seed in range(
            parameters["random_seeds"]["start"],
            parameters["random_seeds"]["stop"] + 1,
        ):
            random_result = run_random_schema_selection(
                task.world, schemas, task.goal, seed=seed,
                schema_check_budget=structured.schema_checks,
            )
            events.append(_event(
                task.name, "random_schema_selection", random_result,
                seed=seed, matched_schema_check_budget=structured.schema_checks,
            ))

    structured_events = [event for event in events if event["condition"] == "structured"]
    single_pool_events = [
        event for event in events
        if event["condition"] in {"single_perspective", "pooled_without_composition"}
    ]
    random_events = [
        event for event in events if event["condition"] == "random_schema_selection"
    ]
    structured_rate = sum(bool(event["success"]) for event in structured_events) / len(structured_events)
    random_rate = sum(bool(event["success"]) for event in random_events) / len(random_events)

    name_pairs_equivalent = True
    for task in originals:
        original = structured_by_task[task.name]
        scrambled = structured_by_task[task.name + "_scrambled"]
        name_pairs_equivalent &= (
            original.success == scrambled.success
            and [(step.schema, step.perspective) for step in original.steps]
            == [(step.schema, step.perspective) for step in scrambled.steps]
        )

    held_out_entities = {
        token for task in tasks for fact in task.world.facts for token in fact[1:]
    }
    schema_text = repr(schemas)
    schemas_exclude_held_out_names = all(name not in schema_text for name in held_out_entities)
    ordinary_equivalent = all(
        structured_by_task[name].success == ordinary_by_task[name].success
        and [step.schema for step in structured_by_task[name].steps]
        == [step.schema for step in ordinary_by_task[name].steps]
        and structured_by_task[name].schema_checks == ordinary_by_task[name].schema_checks
        for name in structured_by_task
    )

    h91 = all(bool(event["success"]) for event in structured_events) and all(
        len(experience.effects) == 1 for experience in training_experiences()
    )
    h92 = all(not bool(event["success"]) for event in single_pool_events)
    h93 = name_pairs_equivalent and schemas_exclude_held_out_names
    h94 = structured_rate - random_rate >= parameters[
        "minimum_structured_minus_random_success_rate"
    ]
    h95 = not ordinary_equivalent
    criteria = {
        "h9_1_relational_transfer": h91,
        "h9_2_single_and_pool_fail": h92,
        "h9_3_name_invariance": h93,
        "h9_4_structured_alignment": h94,
        "h9_5_distinct_from_ordinary_planning": h95,
        "structured_success_rate": structured_rate,
        "random_success_rate": random_rate,
        "structured_minus_random": structured_rate - random_rate,
        "ordinary_planner_equivalent": ordinary_equivalent,
        "robust_generalization_pass": h91 and h92 and h93 and h94,
        "beyond_ordinary_planning_pass": h95,
    }
    summary = {
        "experiment": "EXP009", "criteria": criteria,
        "task_count_including_scrambles": len(tasks),
        "random_run_count": len(random_events),
        "claim_boundary": (
            "Role annotations are supplied. Distinctiveness from ordinary planning "
            "is a separate gate from relational transfer."
        ),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "events.jsonl").write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
        encoding="utf-8",
    )
    (RESULTS / "criteria.json").write_text(
        json.dumps(criteria, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
