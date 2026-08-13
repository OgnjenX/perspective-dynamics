# EXP005 — Held-Out Evidence–Timescale Replication

## Position

EXP004 prospectively confirmed an intermediate dwell regime and then revealed an exploratory shift in the cell maximum: higher evaluation thresholds favored longer decision intervals. EXP005 is a held-out confirmatory replication of that scaling pattern.

## Separation from discovery data

- EXP004 discovery seeds: 0–99;
- EXP005 confirmation seeds: 1,000–1,199;
- denser, frozen block and threshold grids;
- frozen rank-trend criterion committed before any EXP005 run.

## Confirmatory criterion

For the seven ordered evaluation thresholds, compute the block length with greatest mean peak activation, choosing the shorter block if values tie. Confirmation requires:

1. Spearman rank correlation between threshold order and optimal block ≥ 0.8;
2. no more than one adjacent downward reversal in the optimal-block sequence.

## Reproduce

```text
make exp005
make analyze-exp005
```
