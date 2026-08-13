"""Apply the frozen EXP007 calibration and control criteria."""

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
    grouped: dict[tuple[str, str, str, float, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(
            row["topology"], row["propagation_rule"], row["policy"],
            float(row["evaluation_threshold"]), int(row["patience_steps"]),
        )].append(row)

    summaries: list[dict[str, object]] = []
    peaks: dict[tuple[str, str, str, float], dict[int, float]] = defaultdict(dict)
    for (topology, rule, policy, threshold, patience), values in sorted(grouped.items()):
        peak = mean(float(row["peak_goal_activation"]) for row in values)
        peaks[(topology, rule, policy, threshold)][patience] = peak
        summaries.append({
            "topology": topology, "propagation_rule": rule, "policy": policy,
            "evaluation_threshold": threshold, "patience_steps": patience,
            "n": len(values),
            "success_rate": f"{mean(int(row['success']) for row in values):.4f}",
            "mean_peak_goal_activation": f"{peak:.8f}",
            "mean_useful_dwell_steps": f"{mean(int(row['useful_dwell_steps']) for row in values):.3f}",
            "mean_switch_count": f"{mean(int(row['switch_count']) for row in values):.3f}",
            "variable_dwell_seed_fraction": f"{mean(int(row['complete_segment_length_count']) >= 2 for row in values):.4f}",
        })

    optima: list[dict[str, object]] = []
    selected: dict[tuple[str, str, str, float], tuple[int, float]] = {}
    for key, by_patience in sorted(peaks.items()):
        patience = min(by_patience, key=lambda value: (-by_patience[value], value))
        selected[key] = (patience, by_patience[patience])
        topology, rule, policy, threshold = key
        optima.append({
            "topology": topology, "propagation_rule": rule, "policy": policy,
            "evaluation_threshold": threshold, "optimal_patience_steps": patience,
            "optimal_mean_peak_activation": f"{by_patience[patience]:.8f}",
        })

    raw_index: dict[tuple[str, str, str, float, int], list[dict[str, str]]] = grouped
    criteria: list[dict[str, object]] = []
    environments = [
        (environment["topology"], environment["propagation_rule"])
        for environment in parameters["environments"]
    ]
    all_passes: list[bool] = []
    for topology, rule in environments:
        thresholds = sorted(parameters["evaluation_thresholds"])
        progress_optima = [
            selected[(topology, rule, "progress_coupled", threshold)][0]
            for threshold in thresholds
        ]
        rho = _spearman_ordered(progress_optima)
        reversals = sum(
            right < left for left, right in zip(progress_optima, progress_optima[1:])
        )
        distinct = len(set(progress_optima))
        interior = sum(1 < value < 60 for value in progress_optima)
        h71 = (
            rho >= parameters["minimum_spearman_rho"]
            and reversals <= parameters["maximum_adjacent_reversals"]
            and distinct >= parameters["minimum_distinct_optima"]
            and interior >= parameters["minimum_interior_optima"]
        )

        adaptation_differences = []
        replay_differences = []
        variable_fractions = []
        for threshold, patience in zip(thresholds, progress_optima):
            progress_peak = selected[(topology, rule, "progress_coupled", threshold)][1]
            adaptation_peak = selected[(topology, rule, "adaptation_only", threshold)][1]
            replay_peak = peaks[(topology, rule, "timing_replay", threshold)][patience]
            adaptation_differences.append(progress_peak - adaptation_peak)
            replay_differences.append(progress_peak - replay_peak)
            progress_rows = raw_index[
                (topology, rule, "progress_coupled", threshold, patience)
            ]
            variable_fractions.append(
                mean(int(row["complete_segment_length_count"]) >= 2 for row in progress_rows)
            )
        h72 = (
            sum(value > 0 for value in adaptation_differences)
            >= parameters["minimum_threshold_wins"]
            and mean(adaptation_differences) > 0
        )
        h73 = (
            sum(value > 0 for value in replay_differences)
            >= parameters["minimum_threshold_wins"]
            and mean(replay_differences) > 0
        )
        h74 = (
            sum(
                value >= parameters["minimum_variable_dwell_seed_fraction"]
                for value in variable_fractions
            )
            >= parameters["minimum_variable_dwell_thresholds"]
        )
        environment_pass = h71 and h72 and h73 and h74
        all_passes.append(environment_pass)
        criteria.append({
            "scope": "environment", "topology": topology,
            "propagation_rule": rule, "h71_calibration_pass": int(h71),
            "spearman_rho": f"{rho:.8f}", "adjacent_reversals": reversals,
            "distinct_optima": distinct, "interior_optima": interior,
            "h72_adaptation_control_pass": int(h72),
            "adaptation_threshold_wins": sum(value > 0 for value in adaptation_differences),
            "mean_progress_minus_adaptation": f"{mean(adaptation_differences):.8f}",
            "h73_replay_control_pass": int(h73),
            "replay_threshold_wins": sum(value > 0 for value in replay_differences),
            "mean_progress_minus_replay": f"{mean(replay_differences):.8f}",
            "h74_variable_dwell_pass": int(h74),
            "variable_dwell_thresholds": sum(
                value >= parameters["minimum_variable_dwell_seed_fraction"]
                for value in variable_fractions
            ),
            "environment_pass": int(environment_pass),
        })
    criteria.append({
        "scope": "overall", "topology": "all", "propagation_rule": "all",
        "h71_calibration_pass": "", "spearman_rho": "",
        "adjacent_reversals": "", "distinct_optima": "", "interior_optima": "",
        "h72_adaptation_control_pass": "", "adaptation_threshold_wins": "",
        "mean_progress_minus_adaptation": "", "h73_replay_control_pass": "",
        "replay_threshold_wins": "", "mean_progress_minus_replay": "",
        "h74_variable_dwell_pass": "", "variable_dwell_thresholds": "",
        "environment_pass": int(all(all_passes) and len(all_passes) == 2),
    })
    _write(HERE / "results" / "summary.csv", summaries)
    _write(HERE / "results" / "optima.csv", optima)
    _write(HERE / "results" / "criteria.csv", criteria)
    print(f"Wrote {len(summaries)} cells, {len(optima)} optima, and {len(criteria)} criteria")


def _spearman_ordered(values: list[int]) -> float:
    ranks = _average_ranks(values)
    if len(set(ranks)) == 1:
        return 0.0
    return _pearson([float(index) for index in range(1, len(values) + 1)], ranks)


def _average_ranks(values: list[int]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(indexed):
        end = start + 1
        while end < len(indexed) and indexed[end][1] == indexed[start][1]:
            end += 1
        rank = ((start + 1) + end) / 2
        for position in range(start, end):
            ranks[indexed[position][0]] = rank
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
