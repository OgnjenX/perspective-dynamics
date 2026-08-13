import importlib.util
from pathlib import Path
import unittest


PATH = (
    Path(__file__).parents[1]
    / "experiments/EXP006_topology_propagation_falsification/analysis.py"
)
SPEC = importlib.util.spec_from_file_location("exp006_analysis", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class TrendAnalysisTests(unittest.TestCase):
    def test_increasing_optima_have_unit_rank_correlation(self) -> None:
        self.assertAlmostEqual(MODULE._spearman_ordered([1, 2, 3, 4]), 1.0)

    def test_constant_optima_are_scored_as_no_trend(self) -> None:
        self.assertEqual(MODULE._spearman_ordered([3, 3, 3, 3]), 0.0)

    def test_ties_receive_average_ranks(self) -> None:
        self.assertEqual(MODULE._average_ranks([2, 2, 5]), [1.5, 1.5, 3.0])


if __name__ == "__main__":
    unittest.main()
