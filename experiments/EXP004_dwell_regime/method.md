# EXP004 Method

## Fixed components

Reuse EXP003’s matched frames, spreading-activation parameters, 120-step budget, initial-frame start, seed-shuffled exploration order, and adaptive mismatch rule. Only the decision-block duration and evaluation threshold vary.

## Factorial grid

- decision-block steps: 1, 3, 5, 10, 15, 20, 30, 40, 60;
- evaluation threshold: 0.001, 0.005, 0.02;
- task seeds: 0–99.

This yields 2,700 runs. All intervals divide the 120-step run exactly, avoiding partial terminal blocks.

## Mechanism

At each block boundary, maximum goal activation within the block is evaluated. If it is below threshold, the controller advances to the next frame in its seed-shuffled exploration order. Otherwise it retains the active frame. State persists through every frame transition.

## Outcomes

- peak goal activation (primary);
- success and first passage;
- useful-frame dwell;
- switch count;
- time of first useful-frame entry;
- final goal rank.

## Analysis

Summarize every block × threshold cell over 100 seeds. Compute the two frozen primary contrasts for each threshold and for pooled data. Report whether all required inequalities pass. Also store the best observed block length as descriptive, not confirmatory, because the primary claim concerns the prespecified intermediate band.
