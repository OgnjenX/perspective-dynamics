"""Aggregate EXP001 without changing its preregistered condition definitions."""

from pathlib import Path

from perspective_dynamics.experiment import read_rows, summarize, write_summary


EXPERIMENT_DIR = Path(__file__).resolve().parent


def main() -> None:
    raw_path = EXPERIMENT_DIR / "results" / "raw.csv"
    summary_path = EXPERIMENT_DIR / "results" / "summary.csv"
    summary = summarize(read_rows(raw_path))
    write_summary(summary_path, summary)
    print(f"Wrote {len(summary)} condition summaries to {summary_path}")


if __name__ == "__main__":
    main()
