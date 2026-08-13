import unittest

from perspective_dynamics.associative import (
    AssociativeGraph,
    DynamicsConfig,
    SpreadingActivationModel,
)
from perspective_dynamics.tasks import TaskSpec, build_fixed_frame_task


class AssociativeGraphTests(unittest.TestCase):
    def test_rejects_non_positive_edge_weight(self) -> None:
        with self.assertRaises(ValueError):
            AssociativeGraph.undirected(["a", "b"], [("a", "b", 0.0)])

    def test_task_generation_is_reproducible(self) -> None:
        spec = TaskSpec(path_length=4, distractors_per_path_node=2, seed=17)
        first = build_fixed_frame_task(spec)
        second = build_fixed_frame_task(spec)
        self.assertEqual(first.graph.adjacency, second.graph.adjacency)


class SpreadingActivationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = DynamicsConfig(steps=120)

    def _result(self, path_length: int, distractors: int = 0):
        task = build_fixed_frame_task(
            TaskSpec(
                path_length=path_length,
                distractors_per_path_node=distractors,
                seed=0,
            )
        )
        return SpreadingActivationModel(task.graph, self.config).run(
            cue=task.cue,
            goal=task.goal,
            threshold=0.01,
        )

    def test_activation_reaches_direct_neighbor(self) -> None:
        result = self._result(path_length=1)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.first_passage_step)

    def test_longer_path_has_lower_peak_activation(self) -> None:
        short = self._result(path_length=2)
        long = self._result(path_length=6)
        self.assertGreater(short.peak_goal_activation, long.peak_goal_activation)

    def test_distractors_reduce_goal_activation(self) -> None:
        clear = self._result(path_length=4, distractors=0)
        distracted = self._result(path_length=4, distractors=3)
        self.assertGreater(clear.peak_goal_activation, distracted.peak_goal_activation)

    def test_goal_is_never_cued_directly(self) -> None:
        task = build_fixed_frame_task(
            TaskSpec(path_length=3, distractors_per_path_node=1, seed=0)
        )
        self.assertNotIn(task.goal, task.cue)


if __name__ == "__main__":
    unittest.main()
