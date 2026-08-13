# EXP005 Method

## Fixed model

Reuse EXP004 without changing the associative dynamics, three matched path frames, 120-step budget, controller logic, or frame-distance manipulation.

## Held-out grid

- blocks: 1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 40, 60;
- thresholds: 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.04;
- held-out seeds: 1,000–1,199.

The factorial grid contains 16,800 runs. Threshold-specific controller orders are deterministically seeded and not shared with EXP004.

## Analysis

Compute each block × threshold mean peak activation. Select each threshold’s maximizing block with the frozen shorter-tie rule. Rank the seven threshold positions and the seven optimal blocks using average ranks for ties, then compute Pearson correlation of those rank vectors (Spearman correlation). Count adjacent decreases in the optimal-block sequence.

Store cell summaries, selected optima, and the final criteria in separate generated tables. No curve family is fitted confirmatorily.
