"""Run the prospectively specified EXP010 emergence and control grid."""

from __future__ import annotations

from itertools import permutations
import json
from pathlib import Path

from perspective_dynamics.compositional_emergence import (
    generalized_tasks,
    integration_schemas,
    perspective_erased,
    sham_integration_schemas,
)
from perspective_dynamics.schema_composition import CompositionResult, SchemaCompositionEngine

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"


def _event(task: str, condition: str, result: CompositionResult, **extra) -> dict[str, object]:
    return {
        "experiment": "EXP010", "task": task, "condition": condition,
        "success": result.success, "reason": result.reason,
        "explored_states": result.explored_states,
        "schema_checks": result.schema_checks,
        "trajectory": [{
            "step": index,
            "action": step.action,
            "perspective_source": step.perspective,
            "schema_source": step.schema,
            "produced_relation": step.produced,
            "consumed_relation": step.enabled_by,
        } for index, step in enumerate(result.steps, start=1)],
        **extra,
    }


def main() -> None:
    parameters = json.loads((ROOT / "parameters.json").read_text(encoding="utf-8"))
    schemas = integration_schemas()
    tasks = generalized_tasks()
    events: list[dict[str, object]] = []
    integrated_pairs: list[tuple[CompositionResult, CompositionResult]] = []

    for task in tasks:
        for order_index, ordered in enumerate(permutations(schemas)):
            order = tuple(schema.name for schema in ordered)
            integrated = SchemaCompositionEngine(ordered).solve(task.world, task.goal)
            ordinary = SchemaCompositionEngine(perspective_erased(ordered)).solve(
                task.world, task.goal
            )
            integrated_pairs.append((integrated, ordinary))
            events.append(_event(
                task.name, "integration", integrated,
                schema_order_index=order_index, schema_order=order,
            ))
            events.append(_event(
                task.name, "ordinary_forward_planner", ordinary,
                schema_order_index=order_index, schema_order=order,
            ))

        for perspective in sorted({schema.perspective for schema in schemas}):
            selected = tuple(schema for schema in schemas if schema.perspective == perspective)
            result = SchemaCompositionEngine(selected).solve(task.world, task.goal)
            events.append(_event(
                task.name, "single_perspective", result,
                selected_perspective=perspective,
            ))

        static_union = tuple(
            schema for schema in schemas if schema.perspective != "integration"
        )
        events.append(_event(
            task.name, "static_union_without_integration",
            SchemaCompositionEngine(static_union).solve(task.world, task.goal),
        ))

        for removed in ("support", "stability"):
            remaining = tuple(
                schema for schema in schemas if schema.perspective != removed
            )
            events.append(_event(
                task.name, "schema_removal_counterfactual",
                SchemaCompositionEngine(remaining).solve(task.world, task.goal),
                removed_perspective=removed,
            ))

        events.append(_event(
            task.name, "matched_capacity_sham",
            SchemaCompositionEngine(sham_integration_schemas()).solve(
                task.world, task.goal
            ),
        ))

    integration_events = [event for event in events if event["condition"] == "integration"]
    single_events = [event for event in events if event["condition"] == "single_perspective"]
    static_events = [
        event for event in events if event["condition"] == "static_union_without_integration"
    ]
    counterfactual_events = [
        event for event in events if event["condition"] == "schema_removal_counterfactual"
    ]
    sham_events = [event for event in events if event["condition"] == "matched_capacity_sham"]

    h101 = all(not bool(event["success"]) for event in single_events)
    h102 = all(not bool(event["success"]) for event in static_events)
    h103 = all(
        bool(event["success"])
        and len(event["trajectory"]) == parameters["required_plan_length"]
        and all(
            step["schema_source"] and step["perspective_source"]
            and step["produced_relation"] and step["consumed_relation"]
            for step in event["trajectory"]
        )
        for event in integration_events
    )
    h104 = all(not bool(event["success"]) for event in counterfactual_events)
    ordering_invariant = all(
        bool(event["success"])
        and len(event["trajectory"]) == parameters["required_plan_length"]
        for event in integration_events
    )
    h106 = all(not bool(event["success"]) for event in sham_events)
    ordinary_equivalent = all(
        integrated.success == ordinary.success
        and [step.schema for step in integrated.steps]
        == [step.schema for step in ordinary.steps]
        and integrated.schema_checks == ordinary.schema_checks
        for integrated, ordinary in integrated_pairs
    )
    structural_pass = h101 and h102 and h103 and h104 and ordering_invariant and h106
    criteria = {
        "h10_1_individual_trajectory_exclusion": h101,
        "h10_2_static_union_exclusion": h102,
        "h10_3_integration_sufficiency_and_provenance": h103,
        "h10_4_counterfactual_necessity": h104,
        "h10_5_ordering_invariance": ordering_invariant,
        "h10_6_matched_capacity_sham_failure": h106,
        "structural_emergence_pass": structural_pass,
        "ordinary_planner_equivalent": ordinary_equivalent,
        "beyond_ordinary_planning_pass": structural_pass and not ordinary_equivalent,
    }
    summary = {
        "experiment": "EXP010", "criteria": criteria,
        "environment_count": len(tasks),
        "schema_orderings_per_environment": 24,
        "integration_runs": len(integration_events),
        "claim_boundary": (
            "The integration rule is explicit and hand-designed. Structural emergence "
            "does not imply a primitive beyond ordinary planning."
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
