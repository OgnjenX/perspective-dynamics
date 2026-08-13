import unittest
from random import Random

from perspective_dynamics.associative import DynamicsConfig
from perspective_dynamics.perspectives import build_matched_path_perspectives
from perspective_dynamics.switching import (
    replay_schedule,
    run_adaptive_mismatch,
    run_self_timed_mismatch,
)


class SwitchingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.family = build_matched_path_perspectives(
            seed=3, node_count=10,
            distances={"initial": 6, "useful": 2, "irrelevant": 8},
            edge_weight_min=0.8, edge_weight_max=1.2,
        )
        self.config = DynamicsConfig(steps=120)

    def test_adaptive_schedule_has_configured_length(self) -> None:
        result = run_adaptive_mismatch(
            self.family, self.config, block_steps=15,
            evaluation_threshold=0.005, solution_threshold=0.01, rng=Random(9)
        )
        self.assertEqual(len(result.schedule), 120)

    def test_replay_exactly_matches_switch_times_and_count(self) -> None:
        adaptive = run_adaptive_mismatch(
            self.family, self.config, block_steps=15,
            evaluation_threshold=0.005, solution_threshold=0.01, rng=Random(9)
        )
        schedule = replay_schedule(adaptive, tuple(self.family.frames), Random(19))
        replay_segments = []
        for frame in schedule:
            if replay_segments and replay_segments[-1][0] == frame:
                replay_segments[-1][1] += 1
            else:
                replay_segments.append([frame, 1])
        self.assertEqual(
            [length for _, length in adaptive.segments],
            [length for _, length in replay_segments],
        )

    def test_self_timed_schedule_has_configured_length(self) -> None:
        result = run_self_timed_mismatch(
            self.family,
            DynamicsConfig(steps=37),
            patience_steps=5,
            evaluation_threshold=0.01,
            solution_threshold=0.01,
            progress_credit=1.0,
            normalization_epsilon=1e-12,
            rng=Random(9),
        )
        self.assertEqual(len(result.schedule), 37)

    def test_adaptation_only_uses_intrinsic_patience(self) -> None:
        result = run_self_timed_mismatch(
            self.family,
            DynamicsConfig(steps=30),
            patience_steps=5,
            evaluation_threshold=0.01,
            solution_threshold=0.01,
            progress_credit=0.0,
            normalization_epsilon=1e-12,
            rng=Random(9),
        )
        self.assertTrue(all(length == 5 for _, length in result.segments))


if __name__ == "__main__":
    unittest.main()
