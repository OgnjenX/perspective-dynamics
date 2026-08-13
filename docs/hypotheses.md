# Hypotheses and Falsification Criteria

Each hypothesis is provisional. Tests must report effect sizes and uncertainty, not only thresholded significance.

## H1 — Perspective advantage

**Claim:** For problems whose solution is inaccessible or remote under the initial frame, an adaptive perspective system will outperform a matched fixed-frame system.

**Primary prediction:** solution rate and/or constrained utility will be higher for adaptive switching while knowledge, compute budget, and exposure are held constant.

**Critical controls:** fixed best frame, fixed initial frame, matched additional cue, matched compute, and oracle frame as an upper bound.

**Disconfirmation:** no reliable advantage across preregistered perspective-dependent tasks, or the advantage disappears when compute and information are matched.

## H2 — Structured switching

**Claim:** Useful perspective changes are guided by task state, mismatch, or expected progress rather than being equivalent to random exploration.

**Primary prediction:** adaptive switching outperforms random switching with identical switch counts, dwell-time distributions, state noise, and compute.

**Disconfirmation:** random switching matches adaptive switching across held-out problems, or performance is fully explained by the number of visited states.

## H3 — Metastability

**Claim:** Performance peaks between rigid persistence and uncontrolled switching.

**Primary prediction:** over a preregistered switching-pressure or adaptation parameter, perspective-dependent task performance shows an inverted-U, alongside intermediate dwell times and coherent within-frame trajectories.

**Disconfirmation:** performance is monotonic, flat, or the apparent peak fails held-out replication and model comparison against simpler trends.

## H4 — Geometry/accessibility

**Claim:** A successful perspective transition changes representational geometry or dynamics so that a valid solution becomes more accessible.

**Primary predictions:** before the solution is emitted, the useful frame should produce at least one preregistered change: reduced state-to-solution distance, improved linear decodability, neighborhood reorganization, altered transition probability, or a basin/stability change.

**Causal test:** selectively block or scramble the perspective-specific transformation while preserving general switching and test whether the advantage falls.

**Disconfirmation:** success occurs without the predicted change, the change follows rather than precedes solution, or arbitrary transformations yield the same result.

## H5 — Mechanistic robustness and biological constraint

**Claim:** If perspective-dependent dynamics express a genuine computational principle, the qualitative advantage should survive reasonable changes in implementation, though magnitudes and signatures may differ.

**Primary prediction:** after establishing the effect in a minimal rate model, its direction and key regime reproduce in at least one more biologically constrained family, such as shunting, LIF, or AdEx dynamics, under matched tasks.

**Disconfirmation:** the effect requires a narrow artifact of one activation function, update rule, metric, or hand-tuned parameterization.

## Shared measurement plan

- **Task outcomes:** valid solution rate, utility, originality relative to a specified reference distribution, time/steps to solution.
- **Search controls:** visited states, compute, energy/activity, switch count, dwell time, entropy.
- **Geometry:** representational dissimilarity, local neighborhoods, subspace angles, dimensionality, cross-validated decodability.
- **Dynamics:** fixed points or recurrent states, stability/eigenvalues where defined, transition matrices, basin estimates, metastability indices.
- **Robustness:** seeds, task families, hyperparameter regions, ablations, and held-out generalization.

## Claim ladder

1. Switching improves a constrained task.
2. Structured switching beats matched random exploration.
3. A perspective-specific geometric/dynamical change predicts and mediates improvement.
4. The mechanism generalizes across tasks and implementations.
5. Biological data show an analogous signature and intervention sensitivity.

Conclusions must stop at the highest rung actually supported.
