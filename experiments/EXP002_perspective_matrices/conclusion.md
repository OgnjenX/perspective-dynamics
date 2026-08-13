# EXP002 Conclusion

## Status

First validated run completed on 2026-08-13: 200 runs across four conditions and 50 matched seeds. Twelve unit tests passed, including frame-integrity checks.

## Integrity checks

Every individual frame contained the same ten nodes, nine edges, and seed-specific total weight. The realized cue-to-goal distances were exactly 2, 6, and 8 for useful, initial, and irrelevant frames. The equal blend preserved the total weight mass of one frame, although its union contained an average of 21.24 nonzero undirected edges.

## Prospective result

The primary hypothesis was supported in this synthetic system.

- `fixed_useful` succeeded in all 50 seeds, crossed threshold at a median of 8 steps, and reached mean peak goal activation 1.15170451.
- `fixed_initial` and `fixed_irrelevant` never reached threshold. Their mean peak activations were 0.00007021 and effectively zero.
- Useful-minus-initial peak activation was positive for all 50 seeds: mean difference 1.15163429, range 0.95402222–1.29331524.

Changing only relational ordering therefore changed solution accessibility while content, frame size, weight distribution, dynamics, cue input, and compute remained controlled. This validates the perspective-matrix manipulation; it is also an expected consequence of diffusion distance rather than a novel theory by itself.

## Exploratory observation: selective framing versus simultaneous relations

The equal blend succeeded in all seeds and had the same two-edge shortest distance as the useful frame, but mean peak goal activation was only 0.40483027. After observing this pattern, a separate exploratory comparison found useful-minus-mixed activation positive in all 50 seeds, with mean difference 0.74687423 (range 0.58610985–0.97304188).

Within this normalized propagation model, making all relations simultaneously available introduced competing routes that diluted the task-relevant relation. Selective framing therefore did more than expose a short path: it protected that path from cross-frame interference. This is interesting but post-result and model-dependent. It requires a prospectively designed replication that matches local cue/goal strength and examines alternative normalization rules.

## Limitations

- The useful-frame advantage is engineered through path distance; EXP002 validates a mechanism but does not demonstrate autonomous reframing.
- Initial and irrelevant frames inherit the EXP001 floor effect, making thresholded success categorical. Continuous activation preserves some resolution.
- The mixed graph has more nonzero edges despite matched total weight mass. Its reduced activation may reflect degree normalization, not a general cognitive principle.
- Frames are synthetic paths, not learned semantic representations.
- No switching, novelty, usefulness evaluation, metastability, or biological mechanism is present.

## Decision

Proceed to EXP003, but separate two questions prospectively:

1. Can a non-oracle controller discover and dwell in a useful frame better than random or periodic switching under matched budgets?
2. Does selective gating retain an advantage over simultaneous blending after controlling local degree, cue outflow, goal inflow, and propagation normalization?
