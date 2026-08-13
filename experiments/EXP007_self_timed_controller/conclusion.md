# EXP007 Conclusion

## Status

Completed on 2026-08-13: 75,600 runs across 150 unseen seeds, two environments, three policies, 12 patience values, and seven evidence thresholds. Twenty-four unit tests passed. Exact-timing replay matched all 25,200 source schedules.

## Overall result

EXP007 failed its full frozen conjunction because H7.4 failed in both environments. H7.1–H7.3 passed in both environments.

| Environment | H7.1 calibration | H7.2 adaptation control | H7.3 timing replay | H7.4 variable completed dwell | Overall |
|---|---:|---:|---:|---:|---:|
| Path / source-normalized | Pass | Pass | Pass | Fail | Fail |
| Branched / symmetric-normalized | Pass | Pass | Pass | Fail | Fail |

Under the preregistered rule, this is a failed experiment rather than a qualified confirmation.

## Passed components

### Clock-free calibration

Selected progress-coupled patience values increased with evidence threshold:

- path/source: `2, 2, 2, 3, 3, 4, 7`; ρ = 0.95431352; zero reversals;
- branched/symmetric: `2, 3, 3, 4, 5, 7, 10`; ρ = 0.99103121; zero reversals.

Thus the evidence-demand relation appeared without periodic decision blocks.

### Progress-coupling control

The optimized progress-coupled policy beat optimized adaptation-only timing at all seven thresholds in both environments. Mean advantages were 0.37634305 and 0.18954201 in peak activation.

### Exact-timing replay control

At selected progress-coupled patience values, the task-coupled policy beat its exact-timing random replay at all seven thresholds in both environments. Mean advantages were 0.70753761 and 0.30638087.

## Failed component: completed dwell variability

No selected threshold condition reached the frozen requirement that at least 80% of seeds exhibit two or more distinct completed segment lengths. The selected policies commonly switched away from the initial frame and then retained a productive frame until the 120-step horizon. Mean switch counts at selected conditions were typically about 1.4–1.6.

The long productive segment was therefore right-censored and excluded from the preregistered completed-segment statistic. Counting it after seeing the result would change the criterion and is not allowed.

## Interpretation

The result weakens the claim that an external periodic clock is necessary: calibration and both matched performance controls survived its removal. But the frozen experiment did not establish recurrent, dynamically variable metastable dwell. Instead, the controller often behaved like escape followed by absorption into a useful frame.

This exposes a task-design limitation. With one permanently useful frame and a finite horizon, good progress rationally suppresses further switching. A nonabsorbing task is required to test repeated adaptive dwell episodes without post-hoc recoding of censored segments.

## Next prospective test

Use a changing-goal or multi-stage relational task in which the currently useful perspective changes during a run. This forces multiple productive and unproductive episodes and permits uncensored tests of whether realized dwell tracks local evidence demand. The usefulness signal should also move away from direct goal-node activation.

## Provenance

- prospective design merged independently in PR #9, commit `639f4ac`;
- implementation commit: `17eebb1`;
- exact parameters and all generated outputs are stored in this folder.
