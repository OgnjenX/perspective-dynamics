"""Controlled fixed-frame graph tasks for the baseline experiment."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .associative import AssociativeGraph


@dataclass(frozen=True)
class TaskSpec:
    """Factors varied in EXP001."""

    path_length: int
    distractors_per_path_node: int
    seed: int

    def __post_init__(self) -> None:
        if self.path_length < 1:
            raise ValueError("path_length must be at least one")
        if self.distractors_per_path_node < 0:
            raise ValueError("distractors_per_path_node cannot be negative")


@dataclass(frozen=True)
class FixedFrameTask:
    """One cue-to-goal problem defined in a single relational graph."""

    spec: TaskSpec
    graph: AssociativeGraph
    cue: dict[str, float]
    goal: str


def build_fixed_frame_task(spec: TaskSpec) -> FixedFrameTask:
    """Construct a reproducible path with weighted distractor branches.

    The valid route is not marked for the model. Path edges have weight 1.0;
    distractor weights are sampled independently from [0.4, 0.8]. Increasing
    path length tests propagation depth, while increasing distractor load tests
    competition for activation under the same fixed representation.
    """

    rng = Random(spec.seed)
    path_nodes = ["cue"]
    path_nodes.extend(
        f"bridge_{index}" for index in range(1, spec.path_length)
    )
    path_nodes.append("goal")

    nodes = list(path_nodes)
    edges: list[tuple[str, str, float]] = []
    for left, right in zip(path_nodes, path_nodes[1:]):
        edges.append((left, right, 1.0))

    for path_index, path_node in enumerate(path_nodes[:-1]):
        for distractor_index in range(spec.distractors_per_path_node):
            distractor = f"d_{path_index}_{distractor_index}"
            nodes.append(distractor)
            edges.append((path_node, distractor, rng.uniform(0.4, 0.8)))

    return FixedFrameTask(
        spec=spec,
        graph=AssociativeGraph.undirected(nodes, edges),
        cue={"cue": 1.0},
        goal="goal",
    )
