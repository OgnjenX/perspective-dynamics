"""Run the frozen EXP003 switching-policy comparison."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from random import Random

from perspective_dynamics.associative import DynamicsConfig
from perspective_dynamics.perspectives import (
    PerspectiveFamily, blend_graphs, build_matched_path_perspectives,
)
from perspective_dynamics.switching import (
    blocked_schedule, replay_schedule, run_adaptive_mismatch, run_schedule,
)


HERE = Path(__file__).resolve().parent
FIELDS = (
    "condition", "seed", "success", "first_passage_step",
    "peak_goal_activation", "final_goal_rank", "useful_dwell_steps",
    "initial_dwell_steps", "irrelevant_dwell_steps", "switch_count",
    "switch_times", "segments",
)


def main() -> None:
    parameters = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    config = DynamicsConfig(**parameters["dynamics"])
    rows: list[dict[str, object]] = []
    for seed in parameters["seeds"]:
        base = build_matched_path_perspectives(
            seed=seed, node_count=parameters["node_count"],
            distances=parameters["distances"],
            edge_weight_min=parameters["edge_weight_min"],
            edge_weight_max=parameters["edge_weight_max"],
        )
        coefficients = {name: 1 / len(base.frames) for name in base.frames}
        frames = dict(base.frames)
        frames["mixed"] = blend_graphs(base.frames, coefficients)
        family = PerspectiveFamily(frames=frames, cue=base.cue, goal=base.goal, seed=seed)

        adaptive = run_adaptive_mismatch(
            base, config, block_steps=parameters["decision_block_steps"],
            evaluation_threshold=parameters["evaluation_threshold"],
            solution_threshold=parameters["solution_threshold"],
            rng=Random(seed + parameters["controller_seed_offset"]),
        )
        replay = replay_schedule(
            adaptive, tuple(base.frames),
            Random(seed + parameters["replay_seed_offset"]),
        )
        schedules = {
            "fixed_initial": ("initial",) * config.steps,
            "fixed_useful": ("useful",) * config.steps,
            "mixed": ("mixed",) * config.steps,
            "periodic": blocked_schedule(
                frame_names=tuple(base.frames), steps=config.steps,
                block_steps=parameters["decision_block_steps"],
                rng=Random(seed + parameters["controller_seed_offset"]), periodic=True,
            ),
            "random_block": blocked_schedule(
                frame_names=tuple(base.frames), steps=config.steps,
                block_steps=parameters["decision_block_steps"],
                rng=Random(seed + parameters["controller_seed_offset"] + 1), periodic=False,
            ),
            "random_replay": replay,
        }
        results = {
            condition: run_schedule(
                family, config, schedule, parameters["solution_threshold"]
            ) for condition, schedule in schedules.items()
        }
        results["adaptive_mismatch"] = adaptive
        for condition in parameters["conditions"]:
            result = results[condition]
            simulation = result.simulation
            rows.append({
                "condition": condition,
                "seed": seed,
                "success": int(simulation.success),
                "first_passage_step": "" if simulation.first_passage_step is None else simulation.first_passage_step,
                "peak_goal_activation": f"{simulation.peak_goal_activation:.10f}",
                "final_goal_rank": simulation.final_goal_rank,
                "useful_dwell_steps": result.dwell("useful"),
                "initial_dwell_steps": result.dwell("initial"),
                "irrelevant_dwell_steps": result.dwell("irrelevant"),
                "switch_count": result.switch_count,
                "switch_times": json.dumps(result.switch_times, separators=(",", ":")),
                "segments": json.dumps(result.segments, separators=(",", ":")),
            })

    output = HERE / "results" / "raw.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    print(f"Wrote {len(rows)} runs to {output}")


if __name__ == "__main__":
    main()
