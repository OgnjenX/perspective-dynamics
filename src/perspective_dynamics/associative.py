"""A transparent fixed-representation spreading-activation baseline.

The model is intentionally small. It is not presented as a biologically
complete neural model; it establishes what ordinary propagation over one fixed
relational graph can achieve before perspective-dependent mechanisms are added.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Mapping


@dataclass(frozen=True)
class AssociativeGraph:
    """Directed weighted graph with deterministic node ordering."""

    adjacency: Mapping[str, Mapping[str, float]]

    def __post_init__(self) -> None:
        nodes = set(self.adjacency)
        if not nodes:
            raise ValueError("graph must contain at least one node")
        for source, neighbors in self.adjacency.items():
            for target, weight in neighbors.items():
                if target not in nodes:
                    raise ValueError(f"edge target {target!r} is not a graph node")
                if not isfinite(weight) or weight <= 0:
                    raise ValueError(
                        f"edge {source!r}->{target!r} must have positive finite weight"
                    )

    @property
    def nodes(self) -> tuple[str, ...]:
        return tuple(sorted(self.adjacency))

    @classmethod
    def undirected(
        cls, nodes: Iterable[str], edges: Iterable[tuple[str, str, float]]
    ) -> "AssociativeGraph":
        adjacency: dict[str, dict[str, float]] = {node: {} for node in nodes}
        for left, right, weight in edges:
            if left == right:
                raise ValueError("self-edges are not supported in the baseline")
            if left not in adjacency or right not in adjacency:
                raise ValueError("all edge endpoints must be declared as nodes")
            adjacency[left][right] = weight
            adjacency[right][left] = weight
        return cls(adjacency=adjacency)


@dataclass(frozen=True)
class DynamicsConfig:
    """Parameters for a leaky spreading-activation process."""

    time_step: float = 0.1
    decay_rate: float = 1.0
    propagation_gain: float = 0.9
    input_gain: float = 1.0
    global_inhibition: float = 0.05
    steps: int = 120

    def __post_init__(self) -> None:
        numeric = (
            self.time_step,
            self.decay_rate,
            self.propagation_gain,
            self.input_gain,
            self.global_inhibition,
        )
        if not all(isfinite(value) and value >= 0 for value in numeric):
            raise ValueError("dynamics parameters must be finite and non-negative")
        if self.time_step == 0:
            raise ValueError("time_step must be positive")
        if self.steps < 1:
            raise ValueError("steps must be at least one")


@dataclass(frozen=True)
class SimulationResult:
    """Immutable trajectory and task-level metrics."""

    trajectory: tuple[Mapping[str, float], ...]
    goal: str
    threshold: float
    cue_nodes: tuple[str, ...]

    @property
    def goal_activations(self) -> tuple[float, ...]:
        return tuple(state[self.goal] for state in self.trajectory)

    @property
    def peak_goal_activation(self) -> float:
        return max(self.goal_activations)

    @property
    def first_passage_step(self) -> int | None:
        for step, activation in enumerate(self.goal_activations):
            if activation >= self.threshold:
                return step
        return None

    @property
    def success(self) -> bool:
        return self.first_passage_step is not None

    @property
    def final_goal_rank(self) -> int:
        final_state = self.trajectory[-1]
        candidates = [node for node in final_state if node not in self.cue_nodes]
        ordered = sorted(candidates, key=lambda node: (-final_state[node], node))
        return ordered.index(self.goal) + 1


class SpreadingActivationModel:
    """Euler-integrated leaky activation over one fixed weighted graph.

    Each source distributes its activation among outgoing edges in proportion
    to their weights. Constant cue input is clamped throughout a run. A weak
    global inhibitory term prevents undifferentiated activation growth.
    """

    def __init__(self, graph: AssociativeGraph, config: DynamicsConfig) -> None:
        self.graph = graph
        self.config = config

    def run(
        self,
        cue: Mapping[str, float],
        goal: str,
        threshold: float,
    ) -> SimulationResult:
        nodes = self.graph.nodes
        if goal not in self.graph.adjacency:
            raise ValueError(f"goal {goal!r} is not a graph node")
        if not isfinite(threshold) or threshold <= 0:
            raise ValueError("threshold must be positive and finite")
        unknown_cues = set(cue) - set(nodes)
        if unknown_cues:
            raise ValueError(f"unknown cue nodes: {sorted(unknown_cues)}")
        if any(not isfinite(value) or value < 0 for value in cue.values()):
            raise ValueError("cue values must be finite and non-negative")

        state = {node: 0.0 for node in nodes}
        trajectory: list[Mapping[str, float]] = [dict(state)]
        for _ in range(self.config.steps):
            state = self.step(state, cue)
            trajectory.append(dict(state))

        return SimulationResult(
            trajectory=tuple(trajectory),
            goal=goal,
            threshold=threshold,
            cue_nodes=tuple(sorted(cue)),
        )

    def step(
        self, state: Mapping[str, float], cue: Mapping[str, float]
    ) -> dict[str, float]:
        """Advance one Euler step, allowing controlled frame schedules."""
        if set(state) != set(self.graph.nodes):
            raise ValueError("state nodes must exactly match graph nodes")
        propagated = {node: 0.0 for node in self.graph.nodes}
        for source in self.graph.nodes:
            neighbors = self.graph.adjacency[source]
            total_weight = sum(neighbors.values())
            if total_weight == 0:
                continue
            for target, weight in neighbors.items():
                propagated[target] += state[source] * weight / total_weight

        mean_activity = sum(state.values()) / len(state)
        updated: dict[str, float] = {}
        for node in self.graph.nodes:
            derivative = (
                -self.config.decay_rate * state[node]
                + self.config.propagation_gain * propagated[node]
                + self.config.input_gain * cue.get(node, 0.0)
                - self.config.global_inhibition * mean_activity
            )
            updated[node] = max(
                0.0, state[node] + self.config.time_step * derivative
            )
        return updated
