"""Aggregate EXP002 and compute the prospective paired comparison."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, median


EXPERIMENT_DIR = Path(__file__).resolve().parent


def main() -> None:
    raw_path = EXPERIMENT_DIR / "results" / "raw.csv"
    with raw_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_seed: dict[int, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        grouped[row["condition"]].append(row)
        by_seed[int(row["seed"])][row["condition"]] = row

    summary_rows: list[dict[str, object]] = []
    for condition in sorted(grouped):
        condition_rows = grouped[condition]
        passage = [
            int(row["first_passage_step"])
            for row in condition_rows
            if row["first_passage_step"]
        ]
        summary_rows.append(
            {
                "condition": condition,
                "n": len(condition_rows),
                "success_rate": f"{mean(int(row['success']) for row in condition_rows):.3f}",
                "median_first_passage_step": "" if not passage else f"{median(passage):.1f}",
                "mean_peak_goal_activation": f"{mean(float(row['peak_goal_activation']) for row in condition_rows):.8f}",
                "mean_final_goal_rank": f"{mean(int(row['final_goal_rank']) for row in condition_rows):.3f}",
                "mean_realized_distance": f"{mean(int(row['realized_distance']) for row in condition_rows):.3f}",
                "mean_edge_count": f"{mean(int(row['edge_count']) for row in condition_rows):.3f}",
                "mean_total_weight": f"{mean(float(row['total_undirected_weight']) for row in condition_rows):.8f}",
            }
        )

    differences = [
        float(conditions["fixed_useful"]["peak_goal_activation"])
        - float(conditions["fixed_initial"]["peak_goal_activation"])
        for conditions in by_seed.values()
    ]
    paired_row = {
        "comparison": "fixed_useful_minus_fixed_initial_peak_goal_activation",
        "n": len(differences),
        "positive_count": sum(difference > 0 for difference in differences),
        "mean_difference": f"{mean(differences):.8f}",
        "median_difference": f"{median(differences):.8f}",
        "min_difference": f"{min(differences):.8f}",
        "max_difference": f"{max(differences):.8f}",
    }

    # Added after inspecting the primary result. This comparison is explicitly
    # exploratory and is written separately from the prospective paired test.
    useful_minus_mixed = [
        float(conditions["fixed_useful"]["peak_goal_activation"])
        - float(conditions["mixed"]["peak_goal_activation"])
        for conditions in by_seed.values()
    ]
    exploratory_row = {
        "comparison": "fixed_useful_minus_mixed_peak_goal_activation",
        "status": "post_result_exploratory",
        "n": len(useful_minus_mixed),
        "positive_count": sum(difference > 0 for difference in useful_minus_mixed),
        "mean_difference": f"{mean(useful_minus_mixed):.8f}",
        "median_difference": f"{median(useful_minus_mixed):.8f}",
        "min_difference": f"{min(useful_minus_mixed):.8f}",
        "max_difference": f"{max(useful_minus_mixed):.8f}",
    }

    _write(EXPERIMENT_DIR / "results" / "summary.csv", summary_rows)
    _write(EXPERIMENT_DIR / "results" / "paired.csv", [paired_row])
    _write(EXPERIMENT_DIR / "results" / "exploratory.csv", [exploratory_row])
    print(
        f"Wrote {len(summary_rows)} summaries, one prospective paired comparison, "
        "and one exploratory comparison"
    )


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
