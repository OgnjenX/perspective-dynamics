# Decision Record

This file records consequential scientific and repository decisions. Decisions may be superseded, but not silently rewritten; add a new entry and link it to the earlier one.

| ID | Date | Status | Decision | Rationale | Revisit when |
|---|---|---|---|---|---|
| D001 | 2026-08-13 | Accepted | Use `perspective-dynamics` as the project and repository name. | Describes the central manipulation and dynamical focus without asserting a result. | The scientific scope materially changes. |
| D002 | 2026-08-13 | Accepted | Treat Week 1 as documentation-only initialization. | Precise hypotheses and controls are needed before choosing an implementation. | The Week 1 review is complete. |
| D003 | 2026-08-13 | Accepted | Define perspective as a contextual state that changes feature weighting, relations, dynamics, or readout. | Makes the term operational and distinguishes it from generic new information. | A formal model exposes ambiguity. |
| D004 | 2026-08-13 | Accepted | Keep fixed, random-switching, matched-noise/task-switch, and oracle-frame controls in the initial roadmap. | Separates geometry change from more search, perturbation, switching, or information. | A control proves infeasible; document replacement. |
| D005 | 2026-08-13 | Accepted | Establish the computational effect before Brian2 or detailed neuron models. | Avoids biological complexity obscuring whether the proposed effect exists. | H1–H4 have a robust minimal-model result. |
| D006 | 2026-08-13 | Accepted | Use a claim ladder and explicit disconfirmation criteria. | Prevents a narrow simulation result from being described as a general theory of creativity. | Never; individual criteria may be refined prospectively. |
| D007 | 2026-08-13 | Provisional | Consider Grossberg/ART-style competition, adaptation, vigilance, and mismatch/reset as candidate mechanisms. | They offer plausible control motifs but are not yet uniquely supported. | After minimal adaptive switching is characterized. |
| D008 | 2026-08-13 | Accepted | Configure the intended GitHub remote but do not publish in this phase. | “Prepare for publishing” is distinct from making an external repository public. | Owner approves the documentation and requests publication. |
| D009 | 2026-08-13 | Accepted | Begin implementation with a dependency-free fixed-frame spreading-activation baseline. | Establishes the behavior and limits of ordinary association before adding perspectives. | EXP001 fails validation or cannot express the intended baseline. |
| D010 | 2026-08-13 | Accepted | Manipulate path length and distractor load in EXP001. | These factors provide transparent tests of propagation depth and competitive dilution without perspective switching. | Results reveal a confound or ceiling/floor effect. |
| D011 | 2026-08-13 | Accepted | Treat EXP001 as model validation, not a creativity test. | The task measures fixed-graph accessibility and cannot establish novelty, usefulness, or reframing. | Never; later experiments receive separate claims. |
| D012 | 2026-08-13 | Accepted | Isolate perspective geometry in EXP002 using matched weighted paths over identical nodes. | Equal nodes, edges, weight distributions, degree profiles, inputs, and compute rule out simple capacity explanations. | Integrity checks fail or the manipulation proves too artificial for its stated validation role. |
| D013 | 2026-08-13 | Accepted | Keep switching out of EXP002. | First verify that the perspective representation itself has the predicted computational consequence; test selection and switching separately in EXP003. | After EXP002 passes its prospective integrity and behavior checks. |
| D014 | 2026-08-13 | Accepted | Include an equal-matrix blend as an exploratory simultaneous-frames control. | Tests whether making all relations concurrently available substitutes for selective framing, while preserving total weight mass. | The blend cannot be interpreted due to topology or normalization artifacts. |
| D015 | 2026-08-13 | Accepted | Treat the selective-frame advantage over the mixed graph as exploratory and require prospective interference controls. | The comparison was inspected after results and may be explained by greater mixed-graph degree under outgoing normalization. | A preregistered replication controls local degree/flow and alternative propagation rules. |
| D016 | 2026-08-13 | Accepted | Define EXP003 adaptation as mismatch-triggered switching plus progress-triggered dwell. | Tests the proposed balance between escaping an unproductive frame and maintaining a productive one. | The evaluation signal trivially reveals frame identity or fails to separate policies. |
| D017 | 2026-08-13 | Accepted | Use random schedule replay matched to adaptive segment lengths as the primary control. | Equal switch times and counts isolate the association between task feedback and frame dwell. | Replay generation fails exact integrity checks. |
| D018 | 2026-08-13 | Accepted | Expose goal activation only as a scalar controller evaluation signal, never as content input. | Models usefulness feedback while preserving search dynamics, but explicitly bounds the claim to supervised evaluation-gated switching. | A less supervised progress signal is validated. |
| D019 | 2026-08-13 | Accepted | Test the dwell-time tradeoff in EXP004 before calling the dynamics metastable. | The switching interval is externally controlled; an intermediate optimum is necessary but not sufficient evidence for emergent metastability. | A self-organized controller reproduces the regime. |
| D020 | 2026-08-13 | Accepted | Freeze contrasts on blocks 10/15/20 versus blocks 1 and 60 across three evaluation thresholds. | Prevents selecting a favorable interval or threshold after observing the sweep. | Integrity failure or numerical instability invalidates the grid. |
| D021 | 2026-08-13 | Accepted | Treat the apparent 3→5→10 optimum shift as exploratory and replicate it on held-out seeds. | The scaling pattern was noticed after inspecting EXP004 cell maxima. | A prospectively specified held-out experiment passes or falsifies it. |
| D022 | 2026-08-13 | Accepted | Confirm evidence–timescale scaling using seeds 1,000–1,199, a denser grid, Spearman ρ ≥ 0.8, and at most one adjacent reversal. | Separates confirmation from EXP004 discovery and prevents qualitative curve interpretation after inspection. | EXP005 reports both criteria without changing them. |
| D023 | 2026-08-13 | Accepted | Refine perspective as a structured, reusable transformation over controlled shared content rather than a synonym for context. | Provides empirical identity criteria and prevents the construct from becoming a catch-all. | A task requires a contextual manipulation that cannot be classified prospectively. |
| D024 | 2026-08-13 | Accepted | Treat effective perspective repertoire—not raw perspective count—as the primary individual-level hypothesis. | Distinctness, accessibility, appropriate switching, and integration can each limit the value of additional frames. | A validated model shows raw count is sufficient under matched controls. |
| D025 | 2026-08-13 | Accepted | Test collaboration as a potentially distributed implementation of perspective diversity, not as evidence for it by definition. | Separate people may have redundant task representations; communication and integration introduce additional mechanisms and costs. | Matched individual and collective experiments identify a different organizing principle. |
| D026 | 2026-08-13 | Accepted | Preserve EXP001–EXP005 as mechanistic groundwork and do not reinterpret them as tests of collaboration, repertoire size, or hippocampal involvement. | The new conceptual refinement was made after those results and requires prospective experiments. | Never; later experiments may extend but not retroactively change their claims. |
| D027 | 2026-08-13 | Accepted | Attempt to falsify F001 by crossing path/branched topology with source/symmetric propagation before repertoire or biological implementation. | Tests whether the registered relation survives structural and update-rule changes while keeping the controller and primary analysis fixed. | EXP006 reports all frozen environment-level criteria. |
| D028 | 2026-08-13 | Accepted | Require all three novel EXP006 environments to pass relaxed but nondegenerate trend criteria. | A conjunction makes the robustness claim difficult to obtain and treats boundary or constant optima as failures rather than favorable trends. | Never for EXP006; later diagnostic studies may use new prospective criteria. |
| D029 | 2026-08-13 | Accepted | Upgrade F001 from single-structure confirmation to tested topology/propagation robustness, while retaining controller-specific status. | EXP006 passed the positive control and the frozen conjunction across all three novel environments without boundary or constant optima. | A self-timed or broader structural test fails. |
| D030 | 2026-08-13 | Accepted | Test a self-timed mismatch/adaptation controller before biological neuron models. | The external decision clock is now the strongest obvious artifact explanation for F001. | A clock-free controller is specified and tested prospectively. |
| D031 | 2026-08-13 | Accepted | Define EXP007 switching through a per-step mismatch accumulator whose growth is opposed by normalized positive progress. | Produces trajectory-dependent segment boundaries without periodic evaluation blocks while keeping the mechanism transparent. | EXP007 integrity checks show fixed rather than variable realized dwell. |
| D032 | 2026-08-13 | Accepted | Compare progress coupling with adaptation-only and exact-timing random replay controls. | Separates continuous task feedback from an intrinsic timer and separates frame selection from realized switch timing. | A control cannot be matched without leaking task information. |

## Decision template

```text
ID and date:
Status: proposed | accepted | rejected | superseded
Context:
Decision:
Alternatives considered:
Evidence and assumptions:
Consequences:
Revisit trigger:
Links to experiments/commits:
```
