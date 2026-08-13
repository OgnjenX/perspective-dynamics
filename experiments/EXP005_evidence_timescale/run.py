"""Run the held-out EXP005 evidence-threshold × dwell grid."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from random import Random

from perspective_dynamics.associative import DynamicsConfig
from perspective_dynamics.perspectives import build_matched_path_perspectives
from perspective_dynamics.switching import run_adaptive_mismatch


HERE = Path(__file__).resolve().parent
FIELDS = (
    "decision_block_steps", "evaluation_threshold", "seed", "success",
    "peak_goal_activation", "useful_dwell_steps", "switch_count",
)


def main() -> None:
    parameters = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    config = DynamicsConfig(**parameters["dynamics"])
    rows: list[dict[str, object]] = []
    seeds = range(parameters["seed_start"], parameters["seed_stop_exclusive"])
    for threshold_index, threshold in enumerate(parameters["evaluation_thresholds"]):
        for block_steps in parameters["decision_block_steps"]:
            for seed in seeds:
                family = build_matched_path_perspectives(
                    seed=seed, node_count=parameters["node_count"],
                    distances=parameters["distances"],
                    edge_weight_min=parameters["edge_weight_min"],
                    edge_weight_max=parameters["edge_weight_max"],
                )
                result = run_adaptive_mismatch(
                    family, config, block_steps=block_steps,
                    evaluation_threshold=threshold,
                    solution_threshold=parameters["solution_threshold"],
                    rng=Random(
                        seed + parameters["controller_seed_offset"]
                        + threshold_index * 10000
                    ),
                )
                rows.append({
                    "decision_block_steps": block_steps,
                    "evaluation_threshold": threshold,
                    "seed": seed,
                    "success": int(result.simulation.success),
                    "peak_goal_activation": f"{result.simulation.peak_goal_activation:.10f}",
                    "useful_dwell_steps": result.dwell("useful"),
                    "switch_count": result.switch_count,
                })
    output = HERE / "results" / "raw.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)
    print(f"Wrote {len(rows)} held-out runs to {output}")


if __name__ == "__main__":
    main()
