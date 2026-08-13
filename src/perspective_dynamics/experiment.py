"""Reusable execution and aggregation helpers for EXP001."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any, Iterable, Mapping

from .associative import DynamicsConfig, SpreadingActivationModel
from .tasks import TaskSpec, build_fixed_frame_task


RAW_FIELDS = (
    "path_length",
    "distractors_per_path_node",
    "seed",
    "success",
    "first_passage_step",
    "peak_goal_activation",
    "final_goal_rank",
)


def load_parameters(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        parameters = json.load(handle)
    required = {"path_lengths", "distractor_levels", "seeds", "threshold", "dynamics"}
    missing = required - set(parameters)
    if missing:
        raise ValueError(f"missing experiment parameters: {sorted(missing)}")
    return parameters


def run_conditions(parameters: Mapping[str, Any]) -> list[dict[str, Any]]:
    config = DynamicsConfig(**parameters["dynamics"])
    threshold = float(parameters["threshold"])
    rows: list[dict[str, Any]] = []
    for path_length in parameters["path_lengths"]:
        for distractors in parameters["distractor_levels"]:
            for seed in parameters["seeds"]:
                spec = TaskSpec(
                    path_length=int(path_length),
                    distractors_per_path_node=int(distractors),
                    seed=int(seed),
                )
                task = build_fixed_frame_task(spec)
                result = SpreadingActivationModel(task.graph, config).run(
                    cue=task.cue,
                    goal=task.goal,
                    threshold=threshold,
                )
                rows.append(
                    {
                        "path_length": spec.path_length,
                        "distractors_per_path_node": spec.distractors_per_path_node,
                        "seed": spec.seed,
                        "success": int(result.success),
                        "first_passage_step": (
                            "" if result.first_passage_step is None else result.first_passage_step
                        ),
                        "peak_goal_activation": f"{result.peak_goal_activation:.10f}",
                        "final_goal_rank": result.final_goal_rank,
                    }
                )
    return rows


def write_rows(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RAW_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize(rows: Iterable[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int], list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        key = (int(row["path_length"]), int(row["distractors_per_path_node"]))
        grouped[key].append(row)

    summary: list[dict[str, Any]] = []
    for (path_length, distractors), condition_rows in sorted(grouped.items()):
        successes = [int(row["success"]) for row in condition_rows]
        passage_steps = [
            int(row["first_passage_step"])
            for row in condition_rows
            if row["first_passage_step"] != ""
        ]
        peaks = [float(row["peak_goal_activation"]) for row in condition_rows]
        ranks = [int(row["final_goal_rank"]) for row in condition_rows]
        summary.append(
            {
                "path_length": path_length,
                "distractors_per_path_node": distractors,
                "n": len(condition_rows),
                "success_rate": f"{mean(successes):.3f}",
                "median_first_passage_step": (
                    "" if not passage_steps else f"{median(passage_steps):.1f}"
                ),
                "mean_peak_goal_activation": f"{mean(peaks):.6f}",
                "mean_final_goal_rank": f"{mean(ranks):.3f}",
            }
        )
    return summary


def write_summary(path: Path, rows: list[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("cannot write an empty summary")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
