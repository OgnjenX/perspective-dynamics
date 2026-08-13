"""Perspective-dependent relational frames over shared content."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from random import Random
from typing import Mapping

from .associative import AssociativeGraph


@dataclass(frozen=True)
class PerspectiveFamily:
    """Named graph frames that share an identical node set."""

    frames: Mapping[str, AssociativeGraph]
    cue: dict[str, float]
    goal: str
    seed: int

    def __post_init__(self) -> None:
        if not self.frames:
            raise ValueError("a perspective family must contain at least one frame")
        node_sets = {frame.nodes for frame in self.frames.values()}
        if len(node_sets) != 1:
            raise ValueError("all perspectives must contain identical nodes")
        nodes = next(iter(node_sets))
        if self.goal not in nodes:
            raise ValueError("goal must occur in every perspective")
        if not set(self.cue).issubset(nodes):
            raise ValueError("cue nodes must occur in every perspective")


def undirected_edge_count(graph: AssociativeGraph) -> int:
    return sum(len(neighbors) for neighbors in graph.adjacency.values()) // 2


def total_undirected_weight(graph: AssociativeGraph) -> float:
    return sum(sum(neighbors.values()) for neighbors in graph.adjacency.values()) / 2


def shortest_path_length(graph: AssociativeGraph, start: str, goal: str) -> int:
    if start not in graph.adjacency or goal not in graph.adjacency:
        raise ValueError("start and goal must be graph nodes")
    queue: deque[tuple[str, int]] = deque([(start, 0)])
    visited = {start}
    while queue:
        node, distance = queue.popleft()
        if node == goal:
            return distance
        for neighbor in graph.adjacency[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    raise ValueError(f"goal {goal!r} is unreachable from {start!r}")


def blend_graphs(
    graphs: Mapping[str, AssociativeGraph], coefficients: Mapping[str, float]
) -> AssociativeGraph:
    """Return a non-negative weighted sum of matched graph adjacencies."""

    if set(graphs) != set(coefficients):
        raise ValueError("graphs and coefficients must have the same names")
    if any(coefficient < 0 for coefficient in coefficients.values()):
        raise ValueError("blend coefficients cannot be negative")
    if not graphs:
        raise ValueError("at least one graph is required")
    node_sets = {graph.nodes for graph in graphs.values()}
    if len(node_sets) != 1:
        raise ValueError("all blended graphs must contain identical nodes")

    nodes = next(iter(node_sets))
    adjacency: dict[str, dict[str, float]] = {node: {} for node in nodes}
    for name, graph in graphs.items():
        coefficient = coefficients[name]
        for source, neighbors in graph.adjacency.items():
            for target, weight in neighbors.items():
                adjacency[source][target] = (
                    adjacency[source].get(target, 0.0) + coefficient * weight
                )
    adjacency = {
        source: {target: weight for target, weight in neighbors.items() if weight > 0}
        for source, neighbors in adjacency.items()
    }
    return AssociativeGraph(adjacency=adjacency)


def build_matched_path_perspectives(
    *,
    seed: int,
    node_count: int,
    distances: Mapping[str, int],
    edge_weight_min: float,
    edge_weight_max: float,
) -> PerspectiveFamily:
    """Construct path frames matched in content, size, and edge weights.

    Every frame uses the same weight at each path position. Perspective names
    receive independent, reproducible bridge permutations, and the goal is
    inserted at the requested distance from the cue.
    """

    if node_count < 4:
        raise ValueError("node_count must be at least four")
    if edge_weight_min <= 0 or edge_weight_max < edge_weight_min:
        raise ValueError("edge-weight bounds must be positive and ordered")
    if not distances:
        raise ValueError("at least one named distance is required")
    if any(distance < 1 or distance >= node_count - 1 for distance in distances.values()):
        raise ValueError(
            "distances must keep goal internal: 1 <= distance < node_count - 1"
        )

    rng = Random(seed)
    weights = [
        rng.uniform(edge_weight_min, edge_weight_max)
        for _ in range(node_count - 1)
    ]
    bridges = [f"bridge_{index}" for index in range(node_count - 2)]
    frames: dict[str, AssociativeGraph] = {}
    for name, distance in distances.items():
        ordered_bridges = list(bridges)
        rng.shuffle(ordered_bridges)
        ordering = ["cue", *ordered_bridges]
        ordering.insert(distance, "goal")
        edges = [
            (left, right, weight)
            for left, right, weight in zip(ordering, ordering[1:], weights)
        ]
        frames[name] = AssociativeGraph.undirected(ordering, edges)

    return PerspectiveFamily(frames=frames, cue={"cue": 1.0}, goal="goal", seed=seed)
