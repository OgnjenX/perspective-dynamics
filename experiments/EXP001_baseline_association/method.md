# EXP001 Method

## Task construction

Each task contains one valid cue-to-goal path. Path edges have weight 1.0. Every non-goal path node receives 0, 1, or 3 dead-end distractor branches whose weights are independently sampled from a uniform distribution between 0.4 and 0.8 using a recorded seed. The model is not told which edges form the valid route.

Path length and distractor load are crossed factorially. Twenty seeds yield 240 runs.

## Model

The state `xᵢ` is a non-negative activation for node `i`. At each Euler step, a node leaks activation, receives weighted propagation from its neighbors, receives constant cue input if applicable, and experiences weak global inhibition:

```text
dxᵢ/dt = −λxᵢ + g Σⱼ Pᵢⱼxⱼ + Iᵢ − β mean(x)
```

`Pᵢⱼ` is the outgoing-weight-normalized graph matrix. Negative updated values are rectified to zero. Parameters and the 120-step budget are fixed in `parameters.json`.

## Outcomes

- `success`: whether goal activation ever reaches 0.01;
- `first_passage_step`: first threshold-crossing step;
- `peak_goal_activation`;
- `final_goal_rank`: rank among non-cue nodes at the final step.

The threshold is an operational detector setting, not a fitted biological constant.

## Analysis

Aggregate each path-length × distractor condition across 20 seeds. Report success rate, median first-passage step among successful runs, mean peak activation, and mean final rank. EXP001 is descriptive; no null-hypothesis significance test is planned.

## Reproducibility

Python’s standard-library pseudorandom generator is initialized separately for every task seed. Raw results retain the full factor settings and seed. No third-party runtime packages are used.
