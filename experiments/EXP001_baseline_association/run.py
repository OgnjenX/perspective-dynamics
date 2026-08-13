"""Run the preregistered EXP001 condition grid."""

from pathlib import Path

from perspective_dynamics.experiment import load_parameters, run_conditions, write_rows


EXPERIMENT_DIR = Path(__file__).resolve().parent


def main() -> None:
    parameters = load_parameters(EXPERIMENT_DIR / "parameters.json")
    rows = run_conditions(parameters)
    output = EXPERIMENT_DIR / "results" / "raw.csv"
    write_rows(output, rows)
    print(f"Wrote {len(rows)} runs to {output}")


if __name__ == "__main__":
    main()
