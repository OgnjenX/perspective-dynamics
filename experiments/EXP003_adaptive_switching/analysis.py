"""Aggregate EXP003 and verify schedule matching before interpretation."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, median


HERE = Path(__file__).resolve().parent


def main() -> None:
    with (HERE / "results" / "raw.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    paired: dict[int, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        grouped[row["condition"]].append(row)
        paired[int(row["seed"])][row["condition"]] = row

    summaries = []
    for condition in sorted(grouped):
        values = grouped[condition]
        passage = [int(row["first_passage_step"]) for row in values if row["first_passage_step"]]
        summaries.append({
            "condition": condition, "n": len(values),
            "success_rate": f"{mean(int(row['success']) for row in values):.3f}",
            "median_first_passage_step": "" if not passage else f"{median(passage):.1f}",
            "mean_peak_goal_activation": f"{mean(float(row['peak_goal_activation']) for row in values):.8f}",
            "mean_useful_dwell_steps": f"{mean(int(row['useful_dwell_steps']) for row in values):.3f}",
            "mean_switch_count": f"{mean(int(row['switch_count']) for row in values):.3f}",
        })

    activation_differences = []
    dwell_differences = []
    exact_matches = []
    for conditions in paired.values():
        adaptive, replay = conditions["adaptive_mismatch"], conditions["random_replay"]
        activation_differences.append(
            float(adaptive["peak_goal_activation"]) - float(replay["peak_goal_activation"])
        )
        dwell_differences.append(
            int(adaptive["useful_dwell_steps"]) - int(replay["useful_dwell_steps"])
        )
        exact_matches.append(
            adaptive["switch_count"] == replay["switch_count"]
            and adaptive["switch_times"] == replay["switch_times"]
        )

    primary = [{
        "comparison": "adaptive_minus_random_replay_peak_goal_activation",
        "n": len(activation_differences),
        "positive_count": sum(value > 0 for value in activation_differences),
        "zero_count": sum(value == 0 for value in activation_differences),
        "negative_count": sum(value < 0 for value in activation_differences),
        "mean_difference": f"{mean(activation_differences):.8f}",
        "median_difference": f"{median(activation_differences):.8f}",
        "mean_useful_dwell_difference": f"{mean(dwell_differences):.3f}",
        "same_sign_nonzero_count": sum(
            activation * dwell > 0
            for activation, dwell in zip(activation_differences, dwell_differences)
        ),
    }]
    integrity = [{
        "comparison": "adaptive_vs_random_replay_schedule",
        "n": len(exact_matches),
        "exact_switch_time_and_count_matches": sum(exact_matches),
        "all_exact": int(all(exact_matches)),
    }]
    _write(HERE / "results" / "summary.csv", summaries)
    _write(HERE / "results" / "paired.csv", primary)
    _write(HERE / "results" / "integrity.csv", integrity)
    print(f"Wrote {len(summaries)} summaries, paired result, and integrity check")


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0])); writer.writeheader(); writer.writerows(rows)


if __name__ == "__main__":
    main()
