"""Run the frozen EXP002 matched-perspective condition grid."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from perspective_dynamics.associative import DynamicsConfig, SpreadingActivationModel
from perspective_dynamics.perspectives import (
    blend_graphs,
    build_matched_path_perspectives,
    shortest_path_length,
    total_undirected_weight,
    undirected_edge_count,
)


EXPERIMENT_DIR = Path(__file__).resolve().parent
FIELDS = (
    "condition",
    "seed",
    "realized_distance",
    "node_count",
    "edge_count",
    "total_undirected_weight",
    "success",
    "first_passage_step",
    "peak_goal_activation",
    "final_goal_rank",
)


def main() -> None:
    with (EXPERIMENT_DIR / "parameters.json").open(encoding="utf-8") as handle:
        parameters = json.load(handle)
    config = DynamicsConfig(**parameters["dynamics"])
    rows: list[dict[str, object]] = []

    for seed in parameters["seeds"]:
        family = build_matched_path_perspectives(
            seed=seed,
            node_count=parameters["node_count"],
            distances=parameters["distances"],
            edge_weight_min=parameters["edge_weight_min"],
            edge_weight_max=parameters["edge_weight_max"],
        )
        coefficients = {name: 1 / len(family.frames) for name in family.frames}
        condition_graphs = {
            "fixed_initial": family.frames["initial"],
            "fixed_useful": family.frames["useful"],
            "fixed_irrelevant": family.frames["irrelevant"],
            "mixed": blend_graphs(family.frames, coefficients),
        }
        for condition in parameters["conditions"]:
            graph = condition_graphs[condition]
            result = SpreadingActivationModel(graph, config).run(
                cue=family.cue,
                goal=family.goal,
                threshold=parameters["threshold"],
            )
            rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "realized_distance": shortest_path_length(graph, "cue", "goal"),
                    "node_count": len(graph.nodes),
                    "edge_count": undirected_edge_count(graph),
                    "total_undirected_weight": f"{total_undirected_weight(graph):.10f}",
                    "success": int(result.success),
                    "first_passage_step": (
                        "" if result.first_passage_step is None else result.first_passage_step
                    ),
                    "peak_goal_activation": f"{result.peak_goal_activation:.10f}",
                    "final_goal_rank": result.final_goal_rank,
                }
            )

    output = EXPERIMENT_DIR / "results" / "raw.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} runs to {output}")


if __name__ == "__main__":
    main()
