# EXP007 Method

## Controller state

Let `q(t)` be current goal activation, `θ` the evaluation threshold, `P` intrinsic patience, and `m(t)` accumulated mismatch/adaptation. At every integration step:

```text
positive_progress(t) = max(0, q(t) − q(t−1)) / (θ + ε)
m(t+1) = max(0, m(t) + 1/P − β positive_progress(t))
```

The active frame switches when `m ≥ 1`, after which `m` resets to zero and exploration advances through a seeded frame order. `β = 1` is frozen for the progress-coupled policy. This rule has no periodic decision boundary: realized segment duration depends on the continuous trajectory.

## Controls

1. **Adaptation-only:** identical per-step accumulator with `β = 0`; it isolates the value of progress coupling.
2. **Exact-timing random replay:** inherits every segment boundary from a progress-coupled run but randomizes subsequent frame identities; it isolates task-coupled frame selection from realized timing and switch count.

All policies share graph, initial frame, inputs, dynamics, total steps, seeds, and candidate patience values.

## Frozen environments

Use two environments from EXP006:

- path with source-normalized propagation as the positive-control environment;
- uniformly branched path with symmetric-normalized propagation as the joint structural challenge.

## Frozen grid

- patience values: 1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 40, 60;
- evaluation thresholds: 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.04;
- unseen seeds: 3,000–3,149;
- 120 steps per run;
- `ε = 10⁻¹²`;
- progress credit `β = 1`.

The primary progress-coupled and adaptation-only grid contains 50,400 runs. Exact-timing replay adds one matched run per progress-coupled run, for 75,600 total runs.

## Frozen analysis

Peak goal activation remains primary. For each environment, policy, and evidence threshold, select the patience value with maximal mean peak activation, resolving exact ties toward shorter patience. Apply H7.1 to progress-coupled optima.

For H7.2, compare independently optimized progress-coupled and adaptation-only mean peaks at each threshold. For H7.3, compare progress-coupled runs and their exact-timing replays at the selected progress-coupled patience. For H7.4, calculate per-seed segment-length diversity at those selected conditions.

Report success, switch count, useful-frame dwell, segment statistics, and boundary optima as diagnostics. They cannot replace the frozen primary outcome or criteria.

## Stop rule

Any failed frozen hypothesis is recorded as failure. Parameter retuning, alternate progress normalization, threshold removal, or a different patience grid belongs to a later prospective diagnostic experiment.
