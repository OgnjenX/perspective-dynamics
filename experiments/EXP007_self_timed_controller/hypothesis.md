# EXP007 Hypothesis

## H7.1 — Clock-free calibration

For each frozen environment, the performance-optimal intrinsic patience timescale will increase with evaluation evidence demand under the self-timed controller.

Each environment must independently satisfy:

- Spearman rank correlation ≥ 0.8;
- at most one adjacent downward reversal;
- at least three distinct selected patience values;
- at least four selected values inside the grid boundaries.

Both environments must pass. Failure in either retains F001 as dependent on externally imposed timing or on a narrower environment.

## H7.2 — Progress coupling contributes beyond adaptation alone

For at least five of seven evidence thresholds in each environment, the best self-timed progress-coupled condition must exceed the best adaptation-only condition in mean peak goal activation. The overall mean difference across thresholds must be positive in both environments.

## H7.3 — Frame identity matters beyond realized timing

At the self-timed controller’s selected patience value, exact-timing random replay must have lower mean peak goal activation for at least five of seven thresholds in each environment. The overall paired mean difference must be positive in both environments.

## H7.4 — Dwell is dynamically modulated

At least four of seven selected self-timed conditions per environment must show two or more realized segment lengths in at least 80% of seeds. Otherwise the mechanism is functionally equivalent to a fixed interval despite per-step updates.

## Interpretation boundary

Passing would reject the narrow claim that F001 requires periodic decision blocks. It would not make timing biologically realistic: intrinsic patience remains a parameter, progress still uses supervised goal activation, and frames remain engineered.
