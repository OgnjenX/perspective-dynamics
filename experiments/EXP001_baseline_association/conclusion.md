# EXP001 Conclusion

## Status

First validated run completed on 2026-08-13: 240 runs across 12 conditions. All eight unit tests passed before generation and analysis.

## Observed outcomes

The prospective qualitative prediction was supported within the tested parameter grid.

- At path length 2, every run succeeded. Median threshold-crossing time increased from 8 steps without distractors to 15 steps with three distractors per path node. Mean peak goal activation fell from 1.014456 to 0.263569.
- At path length 4, the zero- and one-distractor conditions both succeeded in every run, with median crossing times of 45 and 77 steps. With three distractors, no run reached threshold and mean peak activation was only 0.000023.
- At path lengths 6 and 8, no condition produced nonzero goal activation within the 120-step budget under the recorded precision. Final goal rank also worsened with distance and distraction.

Thus, longer propagation depth delayed and attenuated the valid signal, while distractor branches diluted it. The behavior matches the implemented local propagation rule and shows that the valid goal is not reached trivially.

## Limitations

- The grid contains a strong floor effect for path lengths 6 and 8. It characterizes this parameterization but cannot distinguish degrees of failure there.
- The threshold is an operational detector setting; different thresholds or run durations would shift categorical success rates.
- Distractor seeds change branch weights but not topology, and the descriptive grid is not a population sample.
- This is a fixed graph with hand-designed structure. It does not measure novelty, usefulness, reframing, or human creativity.
- The model is a transparent computational baseline, not a biologically calibrated neural circuit.

## Decision

Proceed to the controlled perspective phase. EXP001 supplies suitable task regimes: a useful perspective can shorten an otherwise inaccessible path, while irrelevant frames and matched controls can preserve long or distracted routes. Phase 2 must compare continuous activation measures as well as thresholded success and must avoid claiming that escaping this engineered floor alone demonstrates creativity.
