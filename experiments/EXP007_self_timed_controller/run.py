"""Run the frozen EXP007 self-timed controller and matched controls."""

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
)
from perspective_dynamics.switching import (
    ScheduledResult,
    replay_schedule,
    run_schedule,
    run_self_timed_mismatch,
)


HERE = Path(__file__).resolve().parent
FIELDS = (
    "topology", "propagation_rule", "policy", "patience_steps",
    "evaluation_threshold", "seed", "success", "peak_goal_activation",
    "useful_dwell_steps", "switch_count", "complete_segment_length_count",
    "mean_complete_segment_length",
)


def build_family(parameters: dict[str, Any], seed: int, topology: str) -> PerspectiveFamily:
    family = build_matched_path_perspectives(
        seed=seed, node_count=parameters["node_count"],
        distances=parameters["distances"],
        edge_weight_min=parameters["edge_weight_min"],
        edge_weight_max=parameters["edge_weight_max"],
    )
    if topology == "branched_path":
        return add_uniform_branches(
            family, branches_per_core_node=parameters["branches_per_core_node"],
            edge_weight_min=parameters["branch_weight_min"],
            edge_weight_max=parameters["branch_weight_max"],
        )
    if topology != "path":
        raise ValueError(f"unknown topology: {topology}")
    return family


def result_row(
    *, environment: dict[str, str], policy: str, patience: int,
    threshold: float, seed: int, result: ScheduledResult,
) -> dict[str, object]:
    complete_lengths = [length for _, length in result.segments[:-1]]
    return {
        "topology": environment["topology"],
        "propagation_rule": environment["propagation_rule"],
        "policy": policy,
        "patience_steps": patience,
        "evaluation_threshold": threshold,
        "seed": seed,
        "success": int(result.simulation.success),
        "peak_goal_activation": f"{result.simulation.peak_goal_activation:.10f}",
        "useful_dwell_steps": result.dwell("useful"),
        "switch_count": result.switch_count,
        "complete_segment_length_count": len(set(complete_lengths)),
        "mean_complete_segment_length": (
            f"{sum(complete_lengths) / len(complete_lengths):.6f}"
            if complete_lengths else ""
        ),
    }


def main() -> None:
    parameters = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    integrity: list[dict[str, object]] = []
    seeds = range(parameters["seed_start"], parameters["seed_stop_exclusive"])
    for environment_index, environment in enumerate(parameters["environments"]):
        config = DynamicsConfig(
            **parameters["dynamics"],
            propagation_rule=environment["propagation_rule"],
        )
        replay_matches = 0
        replay_pairs = 0
        for threshold_index, threshold in enumerate(parameters["evaluation_thresholds"]):
            for patience in parameters["patience_steps"]:
                for seed in seeds:
                    family = build_family(parameters, seed, environment["topology"])
                    controller_seed = (
                        seed + parameters["controller_seed_offset"]
                        + environment_index * 100_000 + threshold_index * 10_000
                    )
                    progress = run_self_timed_mismatch(
                        family, config, patience_steps=patience,
                        evaluation_threshold=threshold,
                        solution_threshold=parameters["solution_threshold"],
                        progress_credit=parameters["progress_credit"],
                        normalization_epsilon=parameters["normalization_epsilon"],
                        rng=Random(controller_seed),
                    )
                    adaptation = run_self_timed_mismatch(
                        family, config, patience_steps=patience,
                        evaluation_threshold=threshold,
                        solution_threshold=parameters["solution_threshold"],
                        progress_credit=0.0,
                        normalization_epsilon=parameters["normalization_epsilon"],
                        rng=Random(controller_seed),
                    )
                    replayed_schedule = replay_schedule(
                        progress, tuple(family.frames),
                        Random(
                            seed + parameters["replay_seed_offset"]
                            + environment_index * 100_000
                            + threshold_index * 10_000
                        ),
                    )
                    replayed = run_schedule(
                        family, config, replayed_schedule,
                        threshold=parameters["solution_threshold"],
                    )
                    replay_pairs += 1
                    replay_matches += int(
                        [length for _, length in progress.segments]
                        == [length for _, length in replayed.segments]
                    )
                    rows.extend((
                        result_row(
                            environment=environment, policy="progress_coupled",
                            patience=patience, threshold=threshold, seed=seed,
                            result=progress,
                        ),
                        result_row(
                            environment=environment, policy="adaptation_only",
                            patience=patience, threshold=threshold, seed=seed,
                            result=adaptation,
                        ),
                        result_row(
                            environment=environment, policy="timing_replay",
                            patience=patience, threshold=threshold, seed=seed,
                            result=replayed,
                        ),
                    ))
        integrity.append({
            "topology": environment["topology"],
            "propagation_rule": environment["propagation_rule"],
            "replay_pairs": replay_pairs,
            "exact_segment_length_matches": replay_matches,
            "all_replay_timings_match": int(replay_matches == replay_pairs),
        })
    _write(HERE / "results" / "raw.csv", rows, FIELDS)
    _write(HERE / "results" / "integrity.csv", integrity, tuple(integrity[0]))
    print(f"Wrote {len(rows)} runs and {len(integrity)} integrity rows")


def _write(path: Path, rows: list[dict[str, object]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
