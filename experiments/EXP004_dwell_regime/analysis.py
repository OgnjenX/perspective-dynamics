"""Evaluate EXP004 using only the frozen intermediate-versus-extreme contrasts."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, median


HERE = Path(__file__).resolve().parent


def main() -> None:
    parameters = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    with (HERE / "results" / "raw.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[tuple[float, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(float(row["evaluation_threshold"]), int(row["decision_block_steps"]))].append(row)

    summaries = []
    for (threshold, block), values in sorted(grouped.items()):
        passage = [int(row["first_passage_step"]) for row in values if row["first_passage_step"]]
        first_useful = [int(row["first_useful_entry_step"]) for row in values if row["first_useful_entry_step"]]
        summaries.append({
            "evaluation_threshold": threshold, "decision_block_steps": block,
            "n": len(values),
            "success_rate": f"{mean(int(row['success']) for row in values):.3f}",
            "mean_peak_goal_activation": f"{mean(float(row['peak_goal_activation']) for row in values):.8f}",
            "median_first_passage_step": "" if not passage else f"{median(passage):.1f}",
            "mean_useful_dwell_steps": f"{mean(int(row['useful_dwell_steps']) for row in values):.3f}",
            "mean_switch_count": f"{mean(int(row['switch_count']) for row in values):.3f}",
            "median_first_useful_entry_step": "" if not first_useful else f"{median(first_useful):.1f}",
        })

    intermediate = set(parameters["intermediate_block_steps"])
    rapid, persistent = parameters["rapid_extreme"], parameters["persistent_extreme"]
    contrast_rows = []
    for threshold in [*parameters["evaluation_thresholds"], "pooled"]:
        selected = rows if threshold == "pooled" else [
            row for row in rows if float(row["evaluation_threshold"]) == float(threshold)
        ]
        intermediate_mean = mean(
            float(row["peak_goal_activation"])
            for row in selected if int(row["decision_block_steps"]) in intermediate
        )
        rapid_mean = mean(
            float(row["peak_goal_activation"])
            for row in selected if int(row["decision_block_steps"]) == rapid
        )
        persistent_mean = mean(
            float(row["peak_goal_activation"])
            for row in selected if int(row["decision_block_steps"]) == persistent
        )
        contrast_rows.append({
            "evaluation_threshold": threshold,
            "intermediate_mean_activation": f"{intermediate_mean:.8f}",
            "rapid_mean_activation": f"{rapid_mean:.8f}",
            "persistent_mean_activation": f"{persistent_mean:.8f}",
            "intermediate_minus_rapid": f"{intermediate_mean - rapid_mean:.8f}",
            "intermediate_minus_persistent": f"{intermediate_mean - persistent_mean:.8f}",
            "both_primary_inequalities_pass": int(
                intermediate_mean > rapid_mean and intermediate_mean > persistent_mean
            ),
        })
    _write(HERE / "results" / "summary.csv", summaries)
    _write(HERE / "results" / "contrasts.csv", contrast_rows)
    print(f"Wrote {len(summaries)} cell summaries and {len(contrast_rows)} frozen contrasts")


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0])); writer.writeheader(); writer.writerows(rows)


if __name__ == "__main__":
    main()
