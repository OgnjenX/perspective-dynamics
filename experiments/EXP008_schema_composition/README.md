# EXP008 — Level 1 schema composition

This experiment asks whether an interpretable agent can compose relational schemas from separate perspectives into a goal-directed trajectory unavailable to a single perspective or to pooled facts without composition.

The task is a hand-specified synthetic world. The result is an implementation check, not evidence for neural dynamics, biological plausibility, learning, or human creativity.

Run with:

```text
PYTHONPATH=src python3 experiments/EXP008_schema_composition/run.py
```

The runner writes `results/summary.json` and an audit JSON Lines log at `results/events.jsonl`.
