"""Run EXP014 bridge discovery and matched controls."""

from __future__ import annotations

from collections import Counter
from dataclasses import replace
import json
from pathlib import Path
from random import Random

from perspective_dynamics.schema_learning import (
    Episode, FeatureSpace, PredictiveVigilanceLearner, SelfOrganizingMap1D,
    bridge_episodes, category_labels, majority_label,
)

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
SUCCESS = "reach_success"


def select(predictions: list[str]) -> int:
    return next((index for index, label in enumerate(predictions) if label == SUCCESS), 0)


def success_rate(environments, selections) -> float:
    return sum(environment[index].outcome == SUCCESS
               for environment, index in zip(environments, selections)) / len(environments)


def main() -> None:
    p = json.loads((ROOT / "parameters.json").read_text())
    train, environments = bridge_episodes()
    space = FeatureSpace(train)
    train_vectors = [space.transform(item) for item in train]
    train_labels = [item.outcome for item in train]

    predictive = PredictiveVigilanceLearner(p["vigilance"]).fit(train_vectors, train_labels)
    predictive_selections = []
    predictive_events = []
    for environment in environments:
        predictions = [predictive.predict(space.transform(item)) for item in environment]
        chosen = select(predictions)
        predictive_selections.append(chosen)
        predictive_events.append({
            "environment": environment[0].identity.split("_candidate_")[0],
            "predictions": predictions, "selected": chosen,
            "selected_identity": environment[chosen].identity,
            "success": environment[chosen].outcome == SUCCESS,
        })
    predictive_rate = success_rate(environments, predictive_selections)

    som = SelfOrganizingMap1D(
        p["som_category_count"], p["som_epochs"], p["learning_rate"], p["som_seed"]
    ).fit(train_vectors)
    som_assignments = [som.category(vector) for vector in train_vectors]
    som_mapping = category_labels(som_assignments, train_labels)
    fallback = majority_label(train_labels)
    som_selections = []
    for environment in environments:
        predictions = [som_mapping.get(som.category(space.transform(item)), fallback)
                       for item in environment]
        som_selections.append(select(predictions))
    som_rate = success_rate(environments, som_selections)

    random_rates = []
    for seed in range(p["random_seed_start"], p["random_seed_stop"] + 1):
        rng = Random(seed)
        assignments = [rng.randrange(p["som_category_count"]) for _ in train]
        mapping = category_labels(assignments, train_labels)
        selections = []
        for environment in environments:
            predictions = [mapping.get(rng.randrange(p["som_category_count"]), fallback)
                           for _ in environment]
            selections.append(select(predictions))
        random_rates.append(success_rate(environments, selections))
    random_mean = sum(random_rates) / len(random_rates)

    # Exact-memory planner has no transition for held-out identities and chooses
    # the first candidate under the frozen deterministic fallback.
    memory = {item.identity: item.outcome for item in train}
    ordinary_selections = [
        select([memory.get(item.identity, "unknown") for item in environment])
        for environment in environments
    ]
    ordinary_rate = success_rate(environments, ordinary_selections)
    oracle_selections = [
        next(index for index, item in enumerate(environment)
             if {"elevated", "stable"}.issubset(item.features))
        for environment in environments
    ]
    oracle_rate = success_rate(environments, oracle_selections)

    selected_positive = environments[0][predictive_selections[0]]
    positive_category = predictive.category(space.transform(selected_positive))
    member_indices = predictive.categories[positive_category].members
    explanation = set(train[member_indices[0]].features)
    for index in member_indices[1:]:
        explanation &= set(train[index].features)

    removal_rates = {}
    for removed in ("elevated", "stable"):
        modified_environments = tuple(
            tuple(replace(item, features=frozenset(set(item.features) - {removed}))
                  for item in environment)
            for environment in environments
        )
        selections = []
        for environment in modified_environments:
            predictions = [predictive.predict(space.transform(item)) for item in environment]
            selections.append(select(predictions))
        removal_rates[removed] = success_rate(environments, selections)

    scrambled = tuple(
        tuple(replace(item, identity=f"scrambled_{env_index}_{item_index}")
              for item_index, item in enumerate(environment))
        for env_index, environment in enumerate(environments)
    )
    scrambled_selections = [
        select([predictive.predict(space.transform(item)) for item in environment])
        for environment in scrambled
    ]
    min_advantage = p["minimum_advantage"]
    criteria = {
        "h14_1_predictive_transfer": predictive_rate >= p["minimum_predictive_success"],
        "h14_2_over_controls": predictive_rate - ordinary_rate >= min_advantage
            and predictive_rate - random_mean >= min_advantage
            and predictive_rate - som_rate >= min_advantage,
        "h14_3_bridge_explanation": {"elevated", "stable"}.issubset(explanation)
            and all("candidate" not in token and "training" not in token for token in explanation)
            and "stable_elevation" not in space.names,
        "h14_4_component_removal": all(
            predictive_rate - rate >= p["minimum_removal_drop"]
            for rate in removal_rates.values()
        ),
        "h14_5_identity_invariance": predictive_selections == scrambled_selections,
        "predictive_success_rate": predictive_rate,
        "som_success_rate": som_rate,
        "random_mean_success_rate": random_mean,
        "ordinary_memory_planner_success_rate": ordinary_rate,
        "handwritten_oracle_success_rate": oracle_rate,
        "learned_positive_explanation": sorted(explanation),
        "removal_success_rates": removal_rates,
        "predictive_category_count": len(predictive.categories),
        "predictive_reset_count": predictive.reset_count,
    }
    criteria["overall_pass"] = all(criteria[key] for key in criteria if key.startswith("h14_"))
    summary = {"experiment": "EXP014", "criteria": criteria,
               "predictive_events": predictive_events,
               "claim_boundary": "Bridge is a learned predictive conjunction in a synthetic candidate-selection task, not creativity or biology."}
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "random_scores.json").write_text(json.dumps(random_rates) + "\n")
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
