# EXP004 — Dwell-Regime Sweep

## Position in the research program

EXP003 used one 15-step decision interval and showed that evaluation-gated switching can outperform matched random replay. EXP004 tests whether that result occupies a productive intermediate regime between rapid switching and excessive persistence.

This is a controlled-timescale precursor to metastability analysis. The switching interval is imposed externally, so a successful inverted-U must not yet be described as emergent neural metastability.

## Primary criterion

Across each prespecified evaluation threshold, the mean peak goal activation for the intermediate intervals (10, 15, and 20 steps) must exceed both:

- the one-step rapid-switching condition;
- the 60-step persistent condition.

The pattern must also appear when averaging across all three thresholds and must not depend solely on thresholded success.

## Reproduce

```text
make exp004
make analyze-exp004
```

The hypothesis, parameter grid, contrasts, and claim boundaries were committed before implementation and results.
