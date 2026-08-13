"""Minimal models for the Perspective Dynamics research program."""

from .associative import (
    AssociativeGraph,
    DynamicsConfig,
    SimulationResult,
    SpreadingActivationModel,
)
from .tasks import FixedFrameTask, TaskSpec, build_fixed_frame_task
from .perspectives import (
    PerspectiveFamily,
    blend_graphs,
    build_matched_path_perspectives,
    shortest_path_length,
    total_undirected_weight,
    undirected_edge_count,
)
from .switching import ScheduledResult, run_adaptive_mismatch, run_schedule

__all__ = [
    "AssociativeGraph",
    "DynamicsConfig",
    "FixedFrameTask",
    "PerspectiveFamily",
    "SimulationResult",
    "ScheduledResult",
    "SpreadingActivationModel",
    "TaskSpec",
    "build_fixed_frame_task",
    "blend_graphs",
    "build_matched_path_perspectives",
    "shortest_path_length",
    "run_adaptive_mismatch",
    "run_schedule",
    "total_undirected_weight",
    "undirected_edge_count",
]
