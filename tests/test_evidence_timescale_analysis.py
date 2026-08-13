import importlib.util
import unittest
from pathlib import Path


ANALYSIS_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments" / "EXP005_evidence_timescale" / "analysis.py"
)
SPEC = importlib.util.spec_from_file_location("exp005_analysis", ANALYSIS_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RankAnalysisTests(unittest.TestCase):
    def test_average_ranks_handles_ties(self) -> None:
        self.assertEqual(MODULE._average_ranks([3, 3, 7, 10]), [1.5, 1.5, 3.0, 4.0])

    def test_pearson_is_one_for_identical_order(self) -> None:
        self.assertAlmostEqual(MODULE._pearson([1, 2, 3], [1, 2, 3]), 1.0)


if __name__ == "__main__":
    unittest.main()
