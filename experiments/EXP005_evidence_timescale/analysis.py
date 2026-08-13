"""Apply the frozen EXP005 rank-trend confirmation criteria."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from math import sqrt
from pathlib import Path
from statistics import mean


HERE = Path(__file__).resolve().parent


def main() -> None:
    parameters = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    with (HERE / "results" / "raw.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[tuple[float, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(float(row["evaluation_threshold"]), int(row["decision_block_steps"]))].append(row)

    summaries = []
    activation_by_threshold: dict[float, dict[int, float]] = defaultdict(dict)
    for (threshold, block), values in sorted(grouped.items()):
        activation = mean(float(row["peak_goal_activation"]) for row in values)
        activation_by_threshold[threshold][block] = activation
        summaries.append({
            "evaluation_threshold": threshold, "decision_block_steps": block,
            "n": len(values),
            "success_rate": f"{mean(int(row['success']) for row in values):.3f}",
            "mean_peak_goal_activation": f"{activation:.8f}",
            "mean_useful_dwell_steps": f"{mean(int(row['useful_dwell_steps']) for row in values):.3f}",
            "mean_switch_count": f"{mean(int(row['switch_count']) for row in values):.3f}",
        })

    optima = []
    for threshold in sorted(activation_by_threshold):
        by_block = activation_by_threshold[threshold]
        optimal_block = min(
            by_block, key=lambda block: (-by_block[block], block)
        )
        optima.append({
            "evaluation_threshold": threshold,
            "optimal_block_steps": optimal_block,
            "optimal_mean_peak_activation": f"{by_block[optimal_block]:.8f}",
        })

    threshold_order = list(range(1, len(optima) + 1))
    optimal_blocks = [int(row["optimal_block_steps"]) for row in optima]
    rho = _pearson(threshold_order, _average_ranks(optimal_blocks))
    reversals = sum(
        right < left for left, right in zip(optimal_blocks, optimal_blocks[1:])
    )
    rho_pass = rho >= parameters["minimum_spearman_rho"]
    reversal_pass = reversals <= parameters["maximum_adjacent_reversals"]
    criteria = [{
        "n_thresholds": len(optima),
        "spearman_rho": f"{rho:.8f}",
        "minimum_required_rho": parameters["minimum_spearman_rho"],
        "rho_pass": int(rho_pass),
        "adjacent_reversals": reversals,
        "maximum_allowed_reversals": parameters["maximum_adjacent_reversals"],
        "reversal_pass": int(reversal_pass),
        "confirmation_pass": int(rho_pass and reversal_pass),
    }]
    _write(HERE / "results" / "summary.csv", summaries)
    _write(HERE / "results" / "optima.csv", optima)
    _write(HERE / "results" / "criteria.csv", criteria)
    print(f"Wrote {len(summaries)} cells, {len(optima)} optima, and confirmation criteria")


def _average_ranks(values: list[int]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(indexed):
        end = start + 1
        while end < len(indexed) and indexed[end][1] == indexed[start][1]:
            end += 1
        average_rank = ((start + 1) + end) / 2
        for position in range(start, end):
            ranks[indexed[position][0]] = average_rank
        start = end
    return ranks


def _pearson(left: list[float], right: list[float]) -> float:
    left_mean, right_mean = mean(left), mean(right)
    numerator = sum((x - left_mean) * (y - right_mean) for x, y in zip(left, right))
    denominator = sqrt(
        sum((x - left_mean) ** 2 for x in left)
        * sum((y - right_mean) ** 2 for y in right)
    )
    if denominator == 0:
        raise ValueError("correlation is undefined for a constant rank vector")
    return numerator / denominator


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0])); writer.writeheader(); writer.writerows(rows)


if __name__ == "__main__":
    main()
