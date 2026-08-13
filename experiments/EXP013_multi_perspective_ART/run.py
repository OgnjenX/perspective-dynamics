"""Run EXP013 multiple predictive organizations and cross-map evaluation."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path

from perspective_dynamics.schema_learning import (
    FeatureSpace, PredictiveVigilanceLearner, accuracy, majority_label,
    multi_target_episodes,
)

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"


def coclustering_distance(left: list[int], right: list[int]) -> float:
    disagreements = 0
    pairs = 0
    for i in range(len(left)):
        for j in range(i + 1, len(left)):
            disagreements += ((left[i] == left[j]) != (right[i] == right[j]))
            pairs += 1
    return disagreements / pairs


def main() -> None:
    p = json.loads((ROOT / "parameters.json").read_text())
    train, test = multi_target_episodes()
    space = FeatureSpace(train)
    train_vectors = [space.transform(item) for item in train]
    test_vectors = [space.transform(item) for item in test]
    fields = ("physical_target", "functional_target", "goal_target")
    models = {}
    assignments = {}
    metrics = {}
    for field in fields:
        train_labels = [getattr(item, field) for item in train]
        test_labels = [getattr(item, field) for item in test]
        model = PredictiveVigilanceLearner(p["vigilance"]).fit(train_vectors, train_labels)
        predicted = [model.predict(vector) for vector in test_vectors]
        models[field] = model
        assignments[field] = [model.category(vector) for vector in train_vectors]
        majority_accuracy = accuracy(test_labels, [majority_label(train_labels)] * len(test))
        metrics[field] = {
            "accuracy": accuracy(test_labels, predicted),
            "majority_accuracy": majority_accuracy,
            "over_majority": accuracy(test_labels, predicted) - majority_accuracy,
            "category_count": len(model.categories),
            "reset_count": model.reset_count,
        }

    distances = {}
    for index, left in enumerate(fields):
        for right in fields[index + 1:]:
            distances[f"{left}__{right}"] = coclustering_distance(
                assignments[left], assignments[right]
            )

    physical = models["physical_target"]
    functional = models["functional_target"]
    goal = models["goal_target"]
    cross_counts: dict[tuple[int, int], Counter[int]] = defaultdict(Counter)
    for vector in train_vectors:
        cross_counts[(physical.category(vector), functional.category(vector))][goal.category(vector)] += 1
    cross_map = {
        pair: sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
        for pair, counts in cross_counts.items()
    }
    expected_goal_categories = [goal.category(vector) for vector in test_vectors]
    predicted_goal_categories = [
        cross_map.get((physical.category(vector), functional.category(vector)), -1)
        for vector in test_vectors
    ]
    cross_accuracy = accuracy(
        [str(value) for value in expected_goal_categories],
        [str(value) for value in predicted_goal_categories],
    )
    criteria = {
        "h13_1_module_accuracy": all(
            item["accuracy"] >= p["minimum_module_accuracy"] for item in metrics.values()
        ),
        "h13_2_distinct_organizations": all(
            value >= p["minimum_coclustering_distance"] for value in distances.values()
        ),
        "h13_3_over_majority": all(
            item["over_majority"] >= p["minimum_over_majority"] for item in metrics.values()
        ),
        "h13_4_cross_map": cross_accuracy >= p["minimum_cross_map_accuracy"],
        "cross_map_accuracy": cross_accuracy,
    }
    criteria["overall_pass"] = all(criteria[key] for key in criteria if key.startswith("h13_"))
    summary = {"experiment": "EXP013", "criteria": criteria,
               "module_metrics": metrics, "coclustering_distances": distances,
               "claim_boundary": "Different predictive partitions are candidate computational perspectives only."}
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
