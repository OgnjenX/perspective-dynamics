"""Run the frozen EXP006 topology × propagation falsification grid."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from random import Random
from typing import Any

from perspective_dynamics.associative import DynamicsConfig
from perspective_dynamics.perspectives import (
    PerspectiveFamily,
    add_uniform_branches,
    build_matched_path_perspectives,
    shortest_path_length,
    total_undirected_weight,
    undirected_edge_count,
)
from perspective_dynamics.switching import run_adaptive_mismatch


HERE = Path(__file__).resolve().parent
FIELDS = (
    "topology", "propagation_rule", "decision_block_steps",
    "evaluation_threshold", "seed", "success", "peak_goal_activation",
    "useful_dwell_steps", "switch_count",
)


def build_family(parameters: dict[str, Any], seed: int, topology: str) -> PerspectiveFamily:
    family = build_matched_path_perspectives(
        seed=seed,
        node_count=parameters["node_count"],
        distances=parameters["distances"],
        edge_weight_min=parameters["edge_weight_min"],
        edge_weight_max=parameters["edge_weight_max"],
    )
    if topology == "branched_path":
        family = add_uniform_branches(
            family,
            branches_per_core_node=parameters["branches_per_core_node"],
            edge_weight_min=parameters["branch_weight_min"],
            edge_weight_max=parameters["branch_weight_max"],
        )
    elif topology != "path":
        raise ValueError(f"unknown topology: {topology}")
    return family


def main() -> None:
    parameters = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    integrity: list[dict[str, object]] = []
    seeds = range(parameters["seed_start"], parameters["seed_stop_exclusive"])
    for topology in parameters["topologies"]:
        integrity_by_seed = []
        for seed in seeds:
            family = build_family(parameters, seed, topology)
            frames = list(family.frames.values())
            integrity_by_seed.append((
                len({frame.nodes for frame in frames}) == 1,
                len({undirected_edge_count(frame) for frame in frames}) == 1,
                len({round(total_undirected_weight(frame), 12) for frame in frames}) == 1,
                all(
                    shortest_path_length(frame, "cue", "goal")
                    == parameters["distances"][name]
                    for name, frame in family.frames.items()
                ),
            ))
        for propagation_rule in parameters["propagation_rules"]:
            integrity.append({
                "topology": topology,
                "propagation_rule": propagation_rule,
                "seeds_checked": len(integrity_by_seed),
                "node_sets_match": int(all(item[0] for item in integrity_by_seed)),
                "edge_counts_match": int(all(item[1] for item in integrity_by_seed)),
                "total_weights_match": int(all(item[2] for item in integrity_by_seed)),
                "distances_match": int(all(item[3] for item in integrity_by_seed)),
            })
            config = DynamicsConfig(
                **parameters["dynamics"], propagation_rule=propagation_rule
            )
            for threshold_index, threshold in enumerate(
                parameters["evaluation_thresholds"]
            ):
                for block_steps in parameters["decision_block_steps"]:
                    for seed in seeds:
                        family = build_family(parameters, seed, topology)
                        result = run_adaptive_mismatch(
                            family,
                            config,
                            block_steps=block_steps,
                            evaluation_threshold=threshold,
                            solution_threshold=parameters["solution_threshold"],
                            rng=Random(
                                seed + parameters["controller_seed_offset"]
                                + threshold_index * 10_000
                            ),
                        )
                        rows.append({
                            "topology": topology,
                            "propagation_rule": propagation_rule,
                            "decision_block_steps": block_steps,
                            "evaluation_threshold": threshold,
                            "seed": seed,
                            "success": int(result.simulation.success),
                            "peak_goal_activation": (
                                f"{result.simulation.peak_goal_activation:.10f}"
                            ),
                            "useful_dwell_steps": result.dwell("useful"),
                            "switch_count": result.switch_count,
                        })
    _write(HERE / "results" / "raw.csv", rows, FIELDS)
    _write(HERE / "results" / "integrity.csv", integrity, tuple(integrity[0]))
    print(f"Wrote {len(rows)} runs and {len(integrity)} integrity rows")


def _write(
    path: Path, rows: list[dict[str, object]], fields: tuple[str, ...]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
