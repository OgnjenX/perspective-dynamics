import csv
import tempfile
import unittest
from pathlib import Path

from perspective_dynamics.experiment import run_conditions, summarize, write_rows


class ExperimentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parameters = {
            "path_lengths": [1, 2],
            "distractor_levels": [0],
            "seeds": [0, 1],
            "threshold": 0.01,
            "dynamics": {"steps": 40},
        }

    def test_condition_count_is_factorial(self) -> None:
        rows = run_conditions(self.parameters)
        self.assertEqual(len(rows), 4)

    def test_written_rows_round_trip_to_summary(self) -> None:
        rows = run_conditions(self.parameters)
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "raw.csv"
            write_rows(path, rows)
            with path.open(encoding="utf-8", newline="") as handle:
                loaded = list(csv.DictReader(handle))
        summary = summarize(loaded)
        self.assertEqual(len(summary), 2)
        self.assertTrue(all(row["n"] == 2 for row in summary))


if __name__ == "__main__":
    unittest.main()
