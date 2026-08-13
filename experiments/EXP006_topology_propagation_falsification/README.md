# EXP006 — Topology and propagation falsification

## Question

Does F001—the positive relation between evidence demand and productive perspective dwell—survive a changed graph topology and a changed propagation rule?

This is an aggressive robustness test, not a new discovery search. It retains the controller, frame distances, thresholds, block grid, run budget, and primary outcome from EXP005 while crossing:

- simple path versus uniformly branched path topology;
- source-normalized versus symmetric-normalized propagation.

The original path × source-normalized condition is a positive-control replication on unseen seeds. The other three environments are falsification conditions.

## Status

Completed. The positive control and all three novel environments passed the frozen criteria. See `conclusion.md` for interpretation and boundaries.

## Reproduce

```text
make exp006
make analyze-exp006
```
