"""Controlled schedules for switching relational frames while state persists."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Mapping, Sequence

from .associative import DynamicsConfig, SimulationResult, SpreadingActivationModel
from .perspectives import PerspectiveFamily


@dataclass(frozen=True)
class ScheduledResult:
    simulation: SimulationResult
    schedule: tuple[str, ...]

    @property
    def switch_times(self) -> tuple[int, ...]:
        return tuple(
            step for step in range(1, len(self.schedule))
            if self.schedule[step] != self.schedule[step - 1]
        )

    @property
    def switch_count(self) -> int:
        return len(self.switch_times)

    def dwell(self, frame: str) -> int:
        return self.schedule.count(frame)

    @property
    def segments(self) -> tuple[tuple[str, int], ...]:
        segments: list[tuple[str, int]] = []
        for frame in self.schedule:
            if segments and segments[-1][0] == frame:
                name, length = segments[-1]
                segments[-1] = (name, length + 1)
            else:
                segments.append((frame, 1))
        return tuple(segments)


def run_schedule(
    family: PerspectiveFamily,
    config: DynamicsConfig,
    schedule: Sequence[str],
    threshold: float,
) -> ScheduledResult:
    if len(schedule) != config.steps:
        raise ValueError("schedule length must equal configured steps")
    if not set(schedule).issubset(family.frames):
        raise ValueError("schedule contains an unknown perspective")
    models = {
        name: SpreadingActivationModel(graph, config)
        for name, graph in family.frames.items()
    }
    state = {node: 0.0 for node in next(iter(family.frames.values())).nodes}
    trajectory: list[Mapping[str, float]] = [dict(state)]
    for frame in schedule:
        state = models[frame].step(state, family.cue)
        trajectory.append(dict(state))
    return ScheduledResult(
        simulation=SimulationResult(
            trajectory=tuple(trajectory), goal=family.goal, threshold=threshold,
            cue_nodes=tuple(sorted(family.cue))
        ),
        schedule=tuple(schedule),
    )


def run_adaptive_mismatch(
    family: PerspectiveFamily,
    config: DynamicsConfig,
    *,
    block_steps: int,
    evaluation_threshold: float,
    solution_threshold: float,
    rng: Random,
) -> ScheduledResult:
    remaining = [name for name in family.frames if name != "initial"]
    rng.shuffle(remaining)
    exploration_order = ["initial", *remaining]
    models = {
        name: SpreadingActivationModel(graph, config)
        for name, graph in family.frames.items()
    }
    frame_index = 0
    schedule: list[str] = []
    state = {node: 0.0 for node in next(iter(family.frames.values())).nodes}
    trajectory: list[Mapping[str, float]] = [dict(state)]
    block_values: list[float] = []
    for step in range(config.steps):
        frame = exploration_order[frame_index]
        state = models[frame].step(state, family.cue)
        schedule.append(frame)
        trajectory.append(dict(state))
        block_values.append(state[family.goal])
        if (step + 1) % block_steps == 0:
            if max(block_values) < evaluation_threshold:
                frame_index = (frame_index + 1) % len(exploration_order)
            block_values = []
    return ScheduledResult(
        simulation=SimulationResult(
            trajectory=tuple(trajectory), goal=family.goal,
            threshold=solution_threshold, cue_nodes=tuple(sorted(family.cue))
        ),
        schedule=tuple(schedule),
    )


def replay_schedule(
    adaptive: ScheduledResult, frame_names: Sequence[str], rng: Random
) -> tuple[str, ...]:
    lengths = [length for _, length in adaptive.segments]
    chosen = ["initial"]
    for _ in lengths[1:]:
        options = [frame for frame in frame_names if frame != chosen[-1]]
        chosen.append(rng.choice(options))
    return tuple(
        frame for frame, length in zip(chosen, lengths) for _ in range(length)
    )


def run_self_timed_mismatch(
    family: PerspectiveFamily,
    config: DynamicsConfig,
    *,
    patience_steps: int,
    evaluation_threshold: float,
    solution_threshold: float,
    progress_credit: float,
    normalization_epsilon: float,
    rng: Random,
) -> ScheduledResult:
    """Switch when continuously accumulated mismatch reaches one.

    Adaptation adds ``1 / patience_steps`` every model step. Positive change
    in goal evidence subtracts normalized progress credit, allowing useful
    trajectories to prolong their realized dwell without periodic decisions.
    """

    if patience_steps < 1:
        raise ValueError("patience_steps must be at least one")
    if evaluation_threshold <= 0 or solution_threshold <= 0:
        raise ValueError("evaluation and solution thresholds must be positive")
    if progress_credit < 0:
        raise ValueError("progress_credit cannot be negative")
    if normalization_epsilon <= 0:
        raise ValueError("normalization_epsilon must be positive")

    remaining = [name for name in family.frames if name != "initial"]
    rng.shuffle(remaining)
    exploration_order = ["initial", *remaining]
    models = {
        name: SpreadingActivationModel(graph, config)
        for name, graph in family.frames.items()
    }
    frame_index = 0
    mismatch = 0.0
    previous_evidence = 0.0
    schedule: list[str] = []
    state = {node: 0.0 for node in next(iter(family.frames.values())).nodes}
    trajectory: list[Mapping[str, float]] = [dict(state)]
    for _ in range(config.steps):
        frame = exploration_order[frame_index]
        state = models[frame].step(state, family.cue)
        evidence = state[family.goal]
        positive_progress = max(0.0, evidence - previous_evidence) / (
            evaluation_threshold + normalization_epsilon
        )
        mismatch = max(
            0.0,
            mismatch + 1.0 / patience_steps - progress_credit * positive_progress,
        )
        schedule.append(frame)
        trajectory.append(dict(state))
        if mismatch >= 1.0:
            frame_index = (frame_index + 1) % len(exploration_order)
            mismatch = 0.0
        previous_evidence = evidence
    return ScheduledResult(
        simulation=SimulationResult(
            trajectory=tuple(trajectory), goal=family.goal,
            threshold=solution_threshold, cue_nodes=tuple(sorted(family.cue))
        ),
        schedule=tuple(schedule),
    )


def blocked_schedule(
    *, frame_names: Sequence[str], steps: int, block_steps: int,
    rng: Random, periodic: bool
) -> tuple[str, ...]:
    remaining = [name for name in frame_names if name != "initial"]
    rng.shuffle(remaining)
    order = ["initial", *remaining]
    schedule: list[str] = []
    previous = ""
    for block_start in range(0, steps, block_steps):
        if periodic:
            frame = order[(block_start // block_steps) % len(order)]
        else:
            options = [name for name in frame_names if name != previous]
            frame = "initial" if block_start == 0 else rng.choice(options)
        schedule.extend([frame] * min(block_steps, steps - block_start))
        previous = frame
    return tuple(schedule)
