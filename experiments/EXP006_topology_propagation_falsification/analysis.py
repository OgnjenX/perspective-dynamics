"""Apply the frozen EXP006 environment-level falsification criteria."""

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
    grouped: dict[tuple[str, str, float, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (
            row["topology"], row["propagation_rule"],
            float(row["evaluation_threshold"]), int(row["decision_block_steps"]),
        )
        grouped[key].append(row)

    summaries: list[dict[str, object]] = []
    activation: dict[tuple[str, str, float], dict[int, float]] = defaultdict(dict)
    for (topology, rule, threshold, block), values in sorted(grouped.items()):
        peak = mean(float(row["peak_goal_activation"]) for row in values)
        activation[(topology, rule, threshold)][block] = peak
        summaries.append({
            "topology": topology,
            "propagation_rule": rule,
            "evaluation_threshold": threshold,
            "decision_block_steps": block,
            "n": len(values),
            "success_rate": f"{mean(int(row['success']) for row in values):.4f}",
            "mean_peak_goal_activation": f"{peak:.8f}",
            "mean_useful_dwell_steps": (
                f"{mean(int(row['useful_dwell_steps']) for row in values):.3f}"
            ),
            "mean_switch_count": (
                f"{mean(int(row['switch_count']) for row in values):.3f}"
            ),
        })

    optima: list[dict[str, object]] = []
    by_environment: dict[tuple[str, str], list[tuple[float, int]]] = defaultdict(list)
    for (topology, rule, threshold), by_block in sorted(activation.items()):
        optimal = min(by_block, key=lambda block: (-by_block[block], block))
        by_environment[(topology, rule)].append((threshold, optimal))
        optima.append({
            "topology": topology,
            "propagation_rule": rule,
            "evaluation_threshold": threshold,
            "optimal_block_steps": optimal,
            "optimal_mean_peak_activation": f"{by_block[optimal]:.8f}",
        })

    criteria: list[dict[str, object]] = []
    novel_passes: list[bool] = []
    for (topology, rule), values in sorted(by_environment.items()):
        values.sort()
        blocks = [block for _, block in values]
        rho = _spearman_ordered(blocks)
        reversals = sum(right < left for left, right in zip(blocks, blocks[1:]))
        distinct = len(set(blocks))
        interior = sum(1 < block < 60 for block in blocks)
        positive_control = topology == "path" and rule == "source_normalized"
        if positive_control:
            environment_pass = (
                rho >= parameters["positive_control_minimum_spearman_rho"]
                and reversals <= parameters["positive_control_maximum_adjacent_reversals"]
            )
        else:
            environment_pass = (
                rho >= parameters["novel_minimum_spearman_rho"]
                and reversals <= parameters["novel_maximum_adjacent_reversals"]
                and distinct >= parameters["novel_minimum_distinct_optima"]
                and interior >= parameters["novel_minimum_interior_optima"]
            )
            novel_passes.append(environment_pass)
        criteria.append({
            "scope": "environment",
            "topology": topology,
            "propagation_rule": rule,
            "positive_control": int(positive_control),
            "spearman_rho": f"{rho:.8f}",
            "adjacent_reversals": reversals,
            "distinct_optima": distinct,
            "interior_optima": interior,
            "environment_pass": int(environment_pass),
        })
    criteria.append({
        "scope": "overall_novel",
        "topology": "all",
        "propagation_rule": "all",
        "positive_control": 0,
        "spearman_rho": "",
        "adjacent_reversals": "",
        "distinct_optima": "",
        "interior_optima": "",
        "environment_pass": int(all(novel_passes) and len(novel_passes) == 3),
    })
    _write(HERE / "results" / "summary.csv", summaries)
    _write(HERE / "results" / "optima.csv", optima)
    _write(HERE / "results" / "criteria.csv", criteria)
    print(f"Wrote {len(summaries)} cells, {len(optima)} optima, and {len(criteria)} criteria")


def _spearman_ordered(values: list[int]) -> float:
    ranks = _average_ranks(values)
    if len(set(ranks)) == 1:
        return 0.0
    order = [float(index) for index in range(1, len(values) + 1)]
    return _pearson(order, ranks)


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
    return numerator / denominator


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
