"""Transparent category-learning baselines for EXP011--EXP014.

These are computational models, not neural or canonical biological ART models.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from math import exp, sqrt
from random import Random
from typing import Iterable, Sequence

Vector = tuple[float, ...]


@dataclass(frozen=True)
class Episode:
    identity: str
    features: frozenset[str]
    action: str
    outcome: str
    physical_target: str = ""
    functional_target: str = ""
    goal_target: str = ""


class FeatureSpace:
    """Deterministic binary vectorizer that excludes audit-only identity."""

    def __init__(self, episodes: Iterable[Episode]) -> None:
        self.names = tuple(sorted({
            token
            for episode in episodes
            for token in (*episode.features, f"action:{episode.action}")
        }))
        self._index = {name: index for index, name in enumerate(self.names)}

    def transform(self, episode: Episode) -> Vector:
        active = set(episode.features) | {f"action:{episode.action}"}
        return tuple(1.0 if name in active else 0.0 for name in self.names)

    def active_names(self, vector: Vector, threshold: float = 0.5) -> tuple[str, ...]:
        return tuple(name for name, value in zip(self.names, vector) if value >= threshold)


def _distance(left: Vector, right: Vector) -> float:
    return sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def _similarity(left: Vector, right: Vector) -> float:
    """Cosine similarity with a deterministic zero-vector convention."""
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def _updated(prototype: Vector, vector: Vector, rate: float) -> Vector:
    return tuple(old + rate * (new - old) for old, new in zip(prototype, vector))


def _farthest_first(vectors: Sequence[Vector], count: int, rng: Random) -> list[Vector]:
    """Seed distinct regions while retaining a reproducible random first node."""
    selected = [rng.randrange(len(vectors))]
    while len(selected) < count:
        candidates = [index for index in range(len(vectors)) if index not in selected]
        chosen = max(
            candidates,
            key=lambda index: (
                min(_distance(vectors[index], vectors[other]) for other in selected),
                -index,
            ),
        )
        selected.append(chosen)
    return [tuple(vectors[index]) for index in selected]


class CompetitiveLearner:
    def __init__(self, category_count: int, epochs: int, learning_rate: float, seed: int) -> None:
        self.category_count = category_count
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.seed = seed
        self.prototypes: tuple[Vector, ...] = ()

    def fit(self, vectors: Sequence[Vector]) -> "CompetitiveLearner":
        if self.category_count < 1 or self.category_count > len(vectors):
            raise ValueError("invalid category_count")
        rng = Random(self.seed)
        prototypes = _farthest_first(vectors, self.category_count, rng)
        for epoch in range(self.epochs):
            order = list(range(len(vectors)))
            rng.shuffle(order)
            rate = self.learning_rate * (1.0 - 0.8 * epoch / max(1, self.epochs - 1))
            for index in order:
                vector = vectors[index]
                winner = min(range(len(prototypes)), key=lambda i: (_distance(vector, prototypes[i]), i))
                prototypes[winner] = _updated(prototypes[winner], vector, rate)
        self.prototypes = tuple(prototypes)
        return self

    def category(self, vector: Vector) -> int:
        if not self.prototypes:
            raise RuntimeError("fit must be called first")
        return min(range(len(self.prototypes)), key=lambda i: (_distance(vector, self.prototypes[i]), i))


class SelfOrganizingMap1D(CompetitiveLearner):
    """A small 1-D SOM with Gaussian neighborhood cooperation."""

    def fit(self, vectors: Sequence[Vector]) -> "SelfOrganizingMap1D":
        if self.category_count < 1 or self.category_count > len(vectors):
            raise ValueError("invalid category_count")
        rng = Random(self.seed)
        prototypes = _farthest_first(vectors, self.category_count, rng)
        initial_radius = max(1.0, self.category_count / 2)
        for epoch in range(self.epochs):
            order = list(range(len(vectors)))
            rng.shuffle(order)
            progress = epoch / max(1, self.epochs - 1)
            rate = self.learning_rate * (1.0 - 0.8 * progress)
            radius = max(0.25, initial_radius * (1.0 - progress))
            for index in order:
                vector = vectors[index]
                winner = min(range(len(prototypes)), key=lambda i: (_distance(vector, prototypes[i]), i))
                for node in range(len(prototypes)):
                    influence = exp(-((node - winner) ** 2) / (2 * radius * radius))
                    prototypes[node] = _updated(prototypes[node], vector, rate * influence)
        self.prototypes = tuple(prototypes)
        return self


@dataclass
class PredictiveCategory:
    prototype: Vector
    label: str
    members: list[int]


class PredictiveVigilanceLearner:
    """ARTMAP-style predictive category refinement.

    Categories compete by cosine match. A sufficiently matching category with
    the wrong prediction is reset for that episode; another category is tried,
    or a new one is created. This is intentionally simpler than canonical ART.
    """

    def __init__(self, vigilance: float, learning_rate: float = 0.5) -> None:
        if not 0.0 <= vigilance <= 1.0:
            raise ValueError("vigilance must be in [0, 1]")
        self.vigilance = vigilance
        self.learning_rate = learning_rate
        self.categories: list[PredictiveCategory] = []
        self.reset_count = 0

    def fit(self, vectors: Sequence[Vector], labels: Sequence[str]) -> "PredictiveVigilanceLearner":
        if len(vectors) != len(labels):
            raise ValueError("vectors and labels must align")
        self.categories = []
        self.reset_count = 0
        for member_index, (vector, label) in enumerate(zip(vectors, labels)):
            ranked = sorted(
                range(len(self.categories)),
                key=lambda i: (-_similarity(vector, self.categories[i].prototype), i),
            )
            selected = None
            for index in ranked:
                category = self.categories[index]
                if _similarity(vector, category.prototype) < self.vigilance:
                    continue
                if category.label != label:
                    self.reset_count += 1
                    continue
                selected = index
                break
            if selected is None:
                self.categories.append(PredictiveCategory(tuple(vector), label, [member_index]))
            else:
                category = self.categories[selected]
                category.prototype = _updated(category.prototype, vector, self.learning_rate)
                category.members.append(member_index)
        return self

    def category(self, vector: Vector) -> int:
        if not self.categories:
            raise RuntimeError("fit must be called first")
        return max(
            range(len(self.categories)),
            key=lambda i: (_similarity(vector, self.categories[i].prototype), -i),
        )

    def predict(self, vector: Vector) -> str:
        return self.categories[self.category(vector)].label


def category_labels(assignments: Sequence[int], labels: Sequence[str]) -> dict[int, str]:
    grouped: dict[int, list[str]] = defaultdict(list)
    for category, label in zip(assignments, labels):
        grouped[category].append(label)
    return {
        category: sorted(Counter(values).items(), key=lambda item: (-item[1], item[0]))[0][0]
        for category, values in grouped.items()
    }


def predict_from_categories(
    model: CompetitiveLearner,
    vectors: Sequence[Vector],
    labels_by_category: dict[int, str],
    fallback: str,
) -> list[str]:
    return [labels_by_category.get(model.category(vector), fallback) for vector in vectors]


def accuracy(expected: Sequence[str], predicted: Sequence[str]) -> float:
    if not expected:
        raise ValueError("expected cannot be empty")
    return sum(a == b for a, b in zip(expected, predicted)) / len(expected)


def cluster_purity(assignments: Sequence[int], labels: Sequence[str]) -> float:
    grouped: dict[int, Counter[str]] = defaultdict(Counter)
    for category, label in zip(assignments, labels):
        grouped[category][label] += 1
    return sum(max(counts.values()) for counts in grouped.values()) / len(labels)


def majority_label(labels: Sequence[str]) -> str:
    return sorted(Counter(labels).items(), key=lambda item: (-item[1], item[0]))[0][0]


def random_category_accuracy(
    train_labels: Sequence[str], test_labels: Sequence[str],
    category_count: int, seed: int,
) -> float:
    rng = Random(seed)
    train_assignments = [rng.randrange(category_count) for _ in train_labels]
    mapping = category_labels(train_assignments, train_labels)
    fallback = majority_label(train_labels)
    predicted = [mapping.get(rng.randrange(category_count), fallback) for _ in test_labels]
    return accuracy(test_labels, predicted)


def schema_discovery_episodes() -> tuple[tuple[Episode, ...], tuple[Episode, ...]]:
    families = (
        ("support", frozenset({"rigid", "supports_weight", "elevated"}), "climb", "height_increase"),
        ("rolling", frozenset({"round", "rotates", "low_friction"}), "push", "translation"),
        ("container", frozenset({"hollow", "holds_contents", "open_top"}), "fill", "stored"),
    )
    train: list[Episode] = []
    test: list[Episode] = []
    for family, features, action, outcome in families:
        for index in range(4):
            train.append(Episode(f"train_{family}_{index}", features, action, outcome))
        for index in range(2):
            test.append(Episode(f"test_{family}_{index}", features, action, outcome))
    return tuple(train), tuple(test)


def predictive_conflict_episodes() -> tuple[tuple[Episode, ...], tuple[Episode, ...]]:
    shapes = {
        "round": {"round", "smooth", "symmetric"},
        "flat": {"flat", "thin", "symmetric"},
        "block": {"angular", "thick", "symmetric"},
    }
    functions = {
        "bounce": ("elastic", "bounce"),
        "roll": ("axle_ready", "roll"),
        "support": ("load_bearing", "support"),
    }
    train: list[Episode] = []
    test: list[Episode] = []
    for shape, appearance in shapes.items():
        for function, (diagnostic, outcome) in functions.items():
            features = frozenset(appearance | {diagnostic})
            train.append(Episode(f"train_{shape}_{function}", features, "interact", outcome))
            train.append(Episode(f"train2_{shape}_{function}", features, "interact", outcome))
            test.append(Episode(f"test_{shape}_{function}", features, "interact", outcome))
    return tuple(train), tuple(test)


def multi_target_episodes() -> tuple[tuple[Episode, ...], tuple[Episode, ...]]:
    train: list[Episode] = []
    test: list[Episode] = []
    for physical in ("rigid", "flexible"):
        for functional in ("support", "connect", "roll"):
            goal = "useful" if (physical, functional) in {
                ("rigid", "support"), ("flexible", "connect")
            } else "not_useful"
            features = frozenset({f"physical:{physical}", f"functional:{functional}"})
            for index in range(3):
                train.append(Episode(
                    f"train_{physical}_{functional}_{index}", features, "inspect", goal,
                    physical, functional, goal,
                ))
            test.append(Episode(
                f"test_{physical}_{functional}", features, "inspect", goal,
                physical, functional, goal,
            ))
    return tuple(train), tuple(test)


def bridge_episodes() -> tuple[tuple[Episode, ...], tuple[tuple[Episode, ...], ...]]:
    train: list[Episode] = []
    for elevated in (False, True):
        for stable in (False, True):
            for variant in range(4):
                features = {"structure"}
                if elevated:
                    features.add("elevated")
                if stable:
                    features.add("stable")
                if variant % 2:
                    features.add("painted")
                outcome = "reach_success" if elevated and stable else "reach_failure"
                train.append(Episode(
                    f"training_configuration_{elevated}_{stable}_{variant}",
                    frozenset(features), "attempt_reach", outcome,
                ))
    environments = []
    for environment in ("construction", "garden", "warehouse", "playground", "dock"):
        candidates = []
        # The successful candidate is deliberately not first.
        for index, (elevated, stable) in enumerate(((True, False), (False, True), (True, True), (False, False))):
            features = {"structure"}
            if elevated:
                features.add("elevated")
            if stable:
                features.add("stable")
            if index % 2:
                features.add("painted")
            outcome = "reach_success" if elevated and stable else "reach_failure"
            candidates.append(Episode(
                f"{environment}_candidate_{index}", frozenset(features),
                "attempt_reach", outcome,
            ))
        environments.append(tuple(candidates))
    return tuple(train), tuple(environments)
