# Hypotheses and Falsification Criteria

Each hypothesis is provisional. Tests must report effect sizes and uncertainty, not only thresholded significance.

## H1 — Effective perspective repertoire advantage

**Claim:** For problems whose solution is inaccessible or remote under the initial frame, a system with a larger effective perspective repertoire will outperform a matched fixed-frame system.

**Primary prediction:** solution rate and/or constrained utility will initially increase with the number and relational diversity of usable frames while knowledge, parameter capacity, compute budget, evaluation opportunity, and exposure are held constant.

**Critical controls:** fixed best frame, fixed initial frame, duplicated/redundant frames, matched additional cue, matched capacity and compute, and oracle frame as an upper bound.

**Disconfirmation:** no reliable advantage across preregistered perspective-dependent tasks, the advantage disappears when capacity and information are matched, or redundant and relationally distinct frame sets perform equivalently.

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

## H6 — Individual versus collective distribution

**Claim:** Some creative benefits of collaboration arise because different task-relevant perspectives can be distributed across people and integrated, implementing a collective analogue of within-person perspective switching.

**Primary prediction:** under matched frame coverage, information, generation time, and evaluation opportunity, both a multi-perspective individual/system and a communicating group of narrower individuals/systems will outperform corresponding single-frame controls. The group advantage should depend on cross-perspective elaboration or integration, not merely pooling or voting.

**Critical controls:** homogeneous groups, noncommunicating diverse groups, independent generation followed by voting, matched total information, and matched total compute.

**Disconfirmation:** measured perspective diversity does not predict performance, communication/integration provides no advantage over pooled independent output, or any apparent team benefit is fully explained by additional information or compute.

## H7 — Perspective distance and integrability

**Claim:** Creativity depends on a balance between nonredundant perspective distance and the ability to translate and integrate across frames.

**Primary prediction:** performance follows an inverted-U or saturating interaction: low distance yields redundancy, intermediate interpretable distance yields the largest benefit, and extreme distance reduces benefit when shared structure or communication is insufficient.

**Critical controls:** preregister the distance metric independently of creative outcomes; vary integration support separately from distance; match frame count, information, and compute.

**Disconfirmation:** performance is unrelated to preregistered frame distance and integration, or raw frame count explains outcomes equally well.

## Shared measurement plan

- **Task outcomes:** valid solution rate, utility, originality relative to a specified reference distribution, time/steps to solution.
- **Search controls:** visited states, compute, energy/activity, switch count, dwell time, entropy.
- **Geometry:** representational dissimilarity, local neighborhoods, subspace angles, dimensionality, cross-validated decodability.
- **Dynamics:** fixed points or recurrent states, stability/eigenvalues where defined, transition matrices, basin estimates, metastability indices.
- **Robustness:** seeds, task families, hyperparameter regions, ablations, and held-out generalization.
- **Repertoire:** frame count, pairwise frame distance, coverage, retrieval success, redundancy, and integration success.
- **Collective organization:** information distribution, communication content, cross-frame elaboration, coordination cost, and performance beyond pooled independent output.

## Claim ladder

1. Switching improves a constrained task.
2. Structured switching beats matched random exploration.
3. A perspective-specific geometric/dynamical change predicts and mediates improvement.
4. The mechanism generalizes across tasks and implementations.
5. Biological data show an analogous signature and intervention sensitivity.
6. Matched individual and collective systems show that perspective diversity plus integration—not headcount or capacity—accounts for an advantage.

Conclusions must stop at the highest rung actually supported.
