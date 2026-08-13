# Experimental Roadmap

## General workflow

Every implemented experiment will receive a self-contained folder with: question, preregistered hypotheses, method, parameters, environment lockfile, seeds, run instructions, raw outputs, analysis, figures, conclusion, deviations, and links to the exact commit. Negative and failed results remain part of the record.

No experiment is implemented in Week 1.

## Phase 0 — Framing review (current gate)

**Goal:** decide whether the operational definitions, hypotheses, controls, and claim ladder are precise enough to justify implementation.

**Exit criteria:** reviewer can identify what is manipulated, what is measured, what would falsify each hypothesis, and which alternative explanations are controlled.

## Phase 1 — Baseline associative system

**Goal:** establish a transparent task and a fixed-representation baseline without perspectives.

**Design requirements:** a small, inspectable relational world; predefined valid solutions; tasks stratified by solution distance; fixed compute budget; reproducible seeds.

**Question answered:** what can ordinary search, noise, and association solve before perspective machinery is added?

## Phase 2 — Same knowledge, different geometry

Add manually specified frames over identical items—for example functional, shape, and material relations. Construct problems where the solution is far in the initial frame, near in one useful frame, and far in an irrelevant frame.

Compare:

1. fixed initial frame;
2. fixed useful frame (oracle upper bound);
3. simultaneous/mixed frames;
4. random frame switching;
5. adaptive frame switching;
6. matched noise or generic task-switch control.

**Primary test:** H1, H2, and the initial form of H4.

## Phase 3 — Adaptive switching and metastability

Introduce explicit progress, mismatch, adaptation, and competition signals. Sweep switching pressure using held-out tasks and compare monotonic, quadratic/inverted-U, and nonparametric models.

**Measures:** solution quality, switch count, dwell time, entropy, within-frame coherence, state coverage, and compute.

**Primary test:** H3 and the causal component of H4.

## Phase 4 — Dynamical and geometric analysis

Analyze rather than merely visualize:

- recurrent states or attractors and their stability;
- transition paths and probabilities;
- basin accessibility under each perspective;
- representational distances and neighborhood changes;
- subspace angles, dimensionality, and decodability;
- temporal order: frame signal → geometry change → candidate → evaluation.

All primary metrics must be selected before inspecting test-condition outcomes.

## Phase 5 — Robustness and biological grounding

Reproduce the qualitative phenomenon across alternative dynamics only after it exists in the minimal model. Candidate implementations include shunting rate units, LIF, AdEx, inhibitory competition, adaptation, synaptic modulation, and mismatch/reset circuits (potentially in Brian2).

**Primary test:** H5. Exact numerical equivalence is not expected; qualitative mechanisms, boundaries, and failure modes are.

## Phase 6 — Empirical bridge (conditional)

If earlier phases support the theory, design a human task with identical information but experimentally cued useful, irrelevant, or unchanged frames. Candidate measurements include behavioral trajectories, eye tracking, EEG/MEG, or fMRI representational analyses. This phase requires ethics review, power analysis, preregistration, and domain collaboration.

## Week 2 candidate experiment (not yet implemented)

A small relational graph with the same nodes under three predefined edge sets. The task is designed so one target is unreachable within a step budget under the initial edge set but reachable under another. Compare fixed, random, and adaptive switching under identical step and switching budgets.

Before coding, freeze:

- the definition of a perspective;
- graph-generation and task-sampling rules;
- valid-solution and novelty metrics;
- the adaptive signal;
- matched-control budgets;
- the H1–H4 analysis plan.

## Stop conditions

Pause or revise the theory if perspective benefits vanish under matched compute/information controls, geometry metrics do not generalize out of sample, or results depend on post-hoc task construction. Such outcomes are informative and must be documented.
