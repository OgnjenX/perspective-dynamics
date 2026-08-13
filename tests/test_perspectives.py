import unittest

from perspective_dynamics.associative import DynamicsConfig, SpreadingActivationModel
from perspective_dynamics.perspectives import (
    blend_graphs,
    build_matched_path_perspectives,
    shortest_path_length,
    total_undirected_weight,
    undirected_edge_count,
)


class PerspectiveConstructionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.family = build_matched_path_perspectives(
            seed=11,
            node_count=10,
            distances={"initial": 6, "useful": 2, "irrelevant": 8},
            edge_weight_min=0.8,
            edge_weight_max=1.2,
        )

    def test_frames_have_requested_distances(self) -> None:
        observed = {
            name: shortest_path_length(graph, "cue", "goal")
            for name, graph in self.family.frames.items()
        }
        self.assertEqual(observed, {"initial": 6, "useful": 2, "irrelevant": 8})

    def test_frames_match_nodes_edges_and_total_weight(self) -> None:
        node_sets = {graph.nodes for graph in self.family.frames.values()}
        edge_counts = {undirected_edge_count(graph) for graph in self.family.frames.values()}
        total_weights = {
            round(total_undirected_weight(graph), 12)
            for graph in self.family.frames.values()
        }
        self.assertEqual(len(node_sets), 1)
        self.assertEqual(edge_counts, {9})
        self.assertEqual(len(total_weights), 1)

    def test_equal_blend_preserves_total_weight_mass(self) -> None:
        coefficients = {name: 1 / 3 for name in self.family.frames}
        mixed = blend_graphs(self.family.frames, coefficients)
        reference = next(iter(self.family.frames.values()))
        self.assertAlmostEqual(
            total_undirected_weight(mixed), total_undirected_weight(reference)
        )

    def test_useful_frame_increases_goal_activation(self) -> None:
        config = DynamicsConfig(steps=120)
        useful = SpreadingActivationModel(self.family.frames["useful"], config).run(
            self.family.cue, self.family.goal, threshold=0.01
        )
        initial = SpreadingActivationModel(self.family.frames["initial"], config).run(
            self.family.cue, self.family.goal, threshold=0.01
        )
        self.assertGreater(useful.peak_goal_activation, initial.peak_goal_activation)


if __name__ == "__main__":
    unittest.main()
