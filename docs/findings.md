# Findings Registry

This registry records results that passed a prospective or held-out criterion. It distinguishes model findings from biological or psychological claims. Exploratory observations remain in experiment conclusions and the research log until confirmed.

## F001 — Evidence demand calibrates productive perspective dwell

**Status:** confirmed and robust across the four tested synthetic topology × propagation environments; controller-specific; not biologically validated.

**Discovery:** EXP004, post-result observation on seeds 0–99.

**Confirmation:** EXP005, prospectively frozen criteria on held-out seeds 1,000–1,199.

**Structural falsification:** EXP006, prospectively frozen conjunction across unseen seeds 2,000–2,149.

**Self-timed challenge:** EXP007, prospectively frozen conjunction across unseen seeds 3,000–3,149; overall failed because the variable completed-dwell criterion failed, although calibration and both performance controls passed.

**Finding:** As the evaluation evidence threshold increased, the block length maximizing mean peak goal activation increased monotonically from 2 to 10 steps across the held-out grid.

**Confirmatory evidence:** selected optima `2, 3, 3, 4, 5, 7, 10`; Spearman ρ = 0.99103121 against ordered thresholds; zero adjacent reversals. Required criteria were ρ ≥ 0.8 and at most one reversal.

**EXP006 evidence:** the positive control and all three novel environments passed. Environment-level Spearman correlations ranged from 0.98198051 to 0.99103121, with zero adjacent reversals, five or six distinct optima, and all seven optima inside the frozen grid boundaries. This rules out specificity to an unbranched path or source-only normalization within the tested family.

**EXP007 qualification:** without periodic decision blocks, selected intrinsic patience still increased with evidence demand (ρ = 0.95431352 and 0.99103121), and progress coupling beat both optimized adaptation-only control and exact-timing random replay at every threshold. However, selected runs commonly escaped the initial frame and remained in the useful frame until censoring. The preregistered repeated-variable-dwell criterion failed in both environments, so EXP007 does not confirm emergent metastable timing.

**Mechanistic interpretation:** A frame must remain active long enough for task-valid evidence to accumulate. Low thresholds permit rapid evaluation and short dwell; high thresholds require longer integration. Excessive dwell remains harmful when the active frame is unproductive, yielding a threshold-dependent stability–flexibility balance.

**What this does not establish:** that human creativity uses this rule; that timing is recurrently metastable, emergent, or neural; that goal activation is a realistic evaluation signal; or that the relation survives learned frames, nonlinear dynamics, graph families without a path backbone, or nonabsorbing tasks.

**Closest literature themes:** cognitive stability versus flexibility, learned switch readiness, creative persistence versus shifting, metastable-state duration control, and dynamic cycles in creative cognition. The targeted Week 1/EXP005 search found no direct test of evidence threshold calibrating perspective-frame dwell, but only a systematic review can support a novelty claim.

**Required falsification attempts:**

1. graph families without a path backbone and varied solution geometries;
2. nonlinear propagation and activation rules;
3. noise and variable run budgets;
4. self-timed adaptation/mismatch dynamics in a nonabsorbing multi-stage task;
5. usefulness signals that do not directly read goal-node activation;
6. learned rather than hand-constructed perspectives.

**Paper relevance:** strengthened mechanistic prediction for a computational theory paper, but the external clock and supervised progress signal remain critical blockers.

## F002 — Abstract schemas transfer, but explicit integration is planning-equivalent

**Status:** prospectively supported structural result with a failed
distinctiveness criterion; not evidence for creativity or biology.

**Experiments:** EXP009 and EXP010.

**Finding:** Role-annotated schemas generalized across three held-out object
sets and their name-scrambled counterparts. Structured composition achieved a
1.0 success rate versus 0.633333 for random schema selection under matched
schema-check budgets. EXP010 produced a four-step trajectory only when a
task-valid bridge consumed relations from support and stability perspectives;
all individual, static-union, schema-removal, and matched-sham controls failed.
The result was invariant across 72 environment × schema-order runs.

**Critical qualification:** A perspective-erased ordinary forward planner with
the same operators reproduced every structured result and schema-check count.
The current implementation therefore demonstrates abstract compositional
planning and explicit bridge necessity, not a mechanism computationally
distinct from ordinary planning.

**What this does not establish:** autonomous schema extraction, discovery of
the bridge relation, a creative advantage, neural implementation, or biological
plausibility.

**Next falsification gate:** compare systems from the same separate experience
corpus without supplying the bridge operator. Any proposed integration
mechanism must show held-out transfer, efficiency, or representational
construction unavailable to a matched planner over the same stored evidence.

## F003 — Engineered episode features support learned categories and bridge conjunctions

**Status:** prospectively supported representation-learning result; predictive
uniqueness failed; not evidence for creativity or biology.

**Experiments:** EXP011–EXP014.

**Finding:** Unsupervised competitive/SOM learning recovered reusable episode
families across unseen identities. Predictive vigilance learning refined
categories after mismatches and different supplied targets induced different
organizations. In EXP014, a predictive category inferred the conjunction
`elevated + stable + structure` without receiving a bridge feature; both
component removals eliminated success.

**Critical qualification:** Similarity-only SOM also solved every EXP014 task.
The bridge was separable in supplied feature geometry, so prediction was not
necessary. EXP012 also used nine predictive categories versus three in its
frozen SOM; a post-hoc nine-category SOM reached 0.777778 versus 1.0 predictive
accuracy. Capacity-matched confirmation remains absent.

**Next falsification gate:** prospectively match category capacity and construct
episodes where similarity is uninformative but outcome contingencies support a
transferable abstraction. Biological interpretation remains closed.
