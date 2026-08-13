"""Run EXP011 similarity-based schema discovery baselines."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from perspective_dynamics.schema_learning import (
    CompetitiveLearner, FeatureSpace, SelfOrganizingMap1D, accuracy,
    category_labels, cluster_purity, majority_label, predict_from_categories,
    random_category_accuracy, schema_discovery_episodes,
)

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"


def evaluate(name, model, train_vectors, test_vectors, train_labels, test_labels):
    model.fit(train_vectors)
    assignments = [model.category(vector) for vector in train_vectors]
    mapping = category_labels(assignments, train_labels)
    predictions = predict_from_categories(
        model, test_vectors, mapping, majority_label(train_labels)
    )
    return {
        "method": name,
        "purity": cluster_purity(assignments, train_labels),
        "transfer_accuracy": accuracy(test_labels, predictions),
        "train_assignments": assignments,
        "test_predictions": predictions,
        "prototypes": model.prototypes,
    }


def main() -> None:
    parameters = json.loads((ROOT / "parameters.json").read_text())
    train, test = schema_discovery_episodes()
    space = FeatureSpace(train)
    train_vectors = [space.transform(item) for item in train]
    test_vectors = [space.transform(item) for item in test]
    train_labels = [item.outcome for item in train]
    test_labels = [item.outcome for item in test]
    args = (parameters["category_count"], parameters["epochs"],
            parameters["learning_rate"], parameters["seed"])
    competitive = evaluate("competitive", CompetitiveLearner(*args), train_vectors,
                           test_vectors, train_labels, test_labels)
    som = evaluate("som", SelfOrganizingMap1D(*args), train_vectors,
                   test_vectors, train_labels, test_labels)
    random_scores = [random_category_accuracy(
        train_labels, test_labels, parameters["category_count"], seed
    ) for seed in range(parameters["random_seed_start"], parameters["random_seed_stop"] + 1)]
    random_mean = sum(random_scores) / len(random_scores)
    identity_scramble_invariant = all(
        space.transform(original) == space.transform(
            replace(original, identity=f"scrambled_{index}")
        )
        for index, original in enumerate((*train, *test))
    )
    criteria = {
        "h11_1_purity": competitive["purity"] >= parameters["minimum_purity"]
            and som["purity"] >= parameters["minimum_purity"],
        "h11_2_transfer": competitive["transfer_accuracy"] >= parameters["minimum_transfer_accuracy"]
            and som["transfer_accuracy"] >= parameters["minimum_transfer_accuracy"],
        "h11_3_identity_invariance": identity_scramble_invariant,
        "h11_4_som_over_random": som["transfer_accuracy"] - random_mean
            >= parameters["minimum_som_minus_random"],
        "random_mean_accuracy": random_mean,
        "handwritten_reference_accuracy": 1.0,
    }
    criteria["overall_pass"] = all(
        criteria[key] for key in criteria if key.startswith("h11_")
    )
    summary = {"experiment": "EXP011", "feature_names": space.names,
               "methods": [competitive, som], "criteria": criteria,
               "claim_boundary": "Identity excluded by vectorizer; schemas are similarity categories, not learned rules."}
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "random_scores.json").write_text(json.dumps(random_scores) + "\n")
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
