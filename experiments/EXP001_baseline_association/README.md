# EXP001 — Fixed-Frame Associative Baseline

## Question

How does ordinary spreading activation over one fixed relational graph degrade as the valid association becomes more distant and competes with more distractors?

This experiment establishes a reference point for later perspective-switching experiments. It does not test creativity or H1 directly.

## Factors

- shortest cue-to-goal path length: 2, 4, 6, or 8 edges;
- distractors attached to every non-goal path node: 0, 1, or 3;
- 20 fixed seeds controlling distractor weights.

The model receives constant input only at `cue`. The valid `goal` is used for scoring but is never given to the dynamics.

## Reproduce

From the repository root:

```text
make reproduce
```

This runs the tests, all 240 conditions, and the summary analysis using Python 3.11 or later. The experiment has no third-party runtime dependency.

## Files

- `hypothesis.md`: prospective prediction and interpretation boundaries;
- `method.md`: task, model, outcomes, and analysis;
- `parameters.json`: complete condition grid and fixed dynamics parameters;
- `run.py`: raw-data generation;
- `analysis.py`: condition aggregation;
- `results/`: generated raw and summary tables;
- `conclusion.md`: filled only after the run.
