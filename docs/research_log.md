# Research Log

## 2026-08-13 — Week 1 initialization

### Objective

Create the research foundation for testing whether perspective change can provide a computational advantage in creative problem solving and, if supported, how that advantage relates to neural dynamics and biological mechanisms.

### Work completed

- Defined the main question, operational terms, scope, and alternative explanations.
- Converted the central idea into five falsifiable hypotheses with explicit disconfirmation criteria.
- Drafted a staged experimental roadmap with review gates and stop conditions.
- Created an initial, non-systematic literature map using fetched peer-reviewed paper records.
- Recorded foundational project decisions and documentation rules.
- Initialized empty areas for papers, models, experiments, analysis, and results.
- Initialized Git on `main` and prepared the intended `OgnjenX/perspective-dynamics` remote.

### Current scientific hypothesis

Creative cognition may sometimes benefit from dynamic changes in representational geometry or effective dynamics that make previously inaccessible valid solutions reachable.

### Current status

No implementation, simulation, dataset, analysis output, or empirical finding exists. All equations are schematic working proposals.

### Known uncertainties

- Whether “perspective” can be formalized without becoming a catch-all for context.
- Whether any benefit survives matched compute, information, noise, and task-switch controls.
- Whether geometric change is causal, predictive only, or a consequence of solution.
- Which level of biological description is appropriate for the first empirical bridge.

### Review checklist

- Is the definition of perspective sufficiently restrictive?
- Are H1–H5 genuinely falsifiable?
- Are the controls capable of separating the main alternatives?
- Does the proposed Week 2 graph task test creativity or only contextual routing?
- Which geometry measures should be primary rather than exploratory?
- What result would justify moving toward biological detail?

### Next step after review

Revise and freeze the Week 1 framing. Only then specify the minimal mathematical model and baseline experiment. Any changes to hypotheses or primary measures after observing results must be logged as exploratory.

## 2026-08-13 — Phase 1 baseline specification

### Decision

The Week 1 framing was judged a reasonable starting point. Phase 1 begins with a fixed-representation spreading-activation model and EXP001; perspective switching remains deliberately excluded.

### Prospective experiment

EXP001 crosses cue-to-goal path length with distractor load over fixed seeds. It tests whether the model exhibits the expected attenuation, delay, and competition effects. The goal is implementation validation and baseline characterization, not evidence of creativity.

### Publication status

Public GitHub publication was authorized, but the local GitHub CLI credential for `OgnjenX` was found to be expired before any external write. Local research work can continue; publication requires re-authentication.

## 2026-08-13 — EXP001 first validated run

### Validation

Eight unit tests passed. The fixed parameter grid produced 240 raw runs and 12 aggregated conditions using only Python 3.11 standard-library runtime dependencies.

### Result

The expected baseline limitation appeared. All path-length-2 conditions succeeded, but threshold crossing slowed and peak goal activation fell with distractor load. At path length 4, zero and one distractor per path node succeeded; three distractors produced complete threshold failure. Path lengths 6 and 8 remained at the activation floor within 120 steps.

### Interpretation

The result validates that the fixed-frame model expresses propagation depth and competitive dilution. It does not test creativity or perspective advantage. The complete floor for longer paths is a design constraint for Phase 2: report continuous activation and rank alongside success, and ensure useful versus irrelevant frames produce controlled differences rather than an uninformative ceiling/floor comparison.

### Next step

Specify a perspective manipulation over shared nodes in which relational edges—not factual content or compute budget—change. Predefine fixed-useful, fixed-initial, random-switching, and adaptive-switching controls before implementation.

## 2026-08-13 — EXP002 prospective design

### Question

Does relational geometry alone change solution accessibility when nodes, edge count, edge weights, degree profile, dynamics, cue input, and compute are matched?

### Frozen design

Use three weighted-path frames over the same ten nodes. Their only intended difference is node ordering, which places the goal two, six, or eight edges from the cue. Compare each fixed frame and an equal matrix blend across 50 seeds. Reuse the validated EXP001 dynamics unchanged.

### Claim boundary

EXP002 can validate the perspective-matrix manipulation and the minimal geometry effect. It cannot show that the system discovers or adaptively selects a useful frame. Those are reserved for EXP003.

## 2026-08-13 — EXP002 first validated run

### Validation

Twelve unit tests passed. Frame integrity checks confirmed matched nodes, nine edges per individual frame, identical seed-level total weights, requested distances, and preserved total weight mass in the equal blend. The experiment generated 200 raw runs.

### Prospective result

The useful frame succeeded in every seed and produced greater peak goal activation than the initial frame in all 50 paired comparisons. Initial and irrelevant frames did not reach threshold. This validates the controlled geometry manipulation but is expected from their designed path lengths.

### Post-result exploratory observation

The equal blend and useful frame both had a two-edge shortest cue-to-goal path and identical total weight mass, yet the selective useful frame produced substantially stronger goal activation in every seed. This comparison was not a prospective primary prediction and is stored separately in `exploratory.csv`.

### Interpretation and next test

The pattern suggests selective framing may reduce cross-frame interference rather than merely add useful relations. Because the mixed graph has higher local degree and the model normalizes outgoing propagation, the effect may be a normalization artifact. A prospective control must match local degree/flow or vary normalization before treating selective gating as a broader result.

## 2026-08-13 — EXP003 prospective design

### Question

Can mismatch-responsive switching outperform random frame assignment when switch timing and count are identical?

### Frozen mechanism

The controller evaluates maximum goal activation only at 15-step block boundaries. Lack of task-valid signal triggers exploration of another frame; detectable progress triggers continued dwell. The signal controls frame selection but is not injected into associative activation.

### Primary control

For each seed, random replay inherits the adaptive schedule’s exact segment lengths, switch times, and switch count while randomizing later frame identities without evaluation. This directly tests whether task-coupled dwell—not merely reduced switching—produces an advantage.

### Claim boundary

Even a positive result would represent evaluation-gated search with synthetic frames. It would not establish unsupervised creativity, psychological perspective taking, metastable neural dynamics, or biological plausibility.

## 2026-08-13 — EXP003 first validated run

### Integrity

All 100 adaptive/replay pairs matched switch times and counts exactly. Fourteen unit tests passed, and 700 policy runs were generated.

### Result

Adaptive mismatch switching succeeded in every seed versus 76% for schedule-matched replay. Mean peak activation increased by 0.56774184. Adaptive policies allocated 50.85 more steps to the useful frame on average, despite identical segment timing.

### Interpretation

Task-valid feedback improved which frame occupied the available dwell segments. This supports H2’s structured-switching direction under supervised evaluation, but it is not evidence for unguided creativity or biology. The outcome is consistent with the controller design and is not claimed as novel.

### Next test

Prospectively sweep dwell/decision times to test the stronger metastability prediction: very short dwell should prevent evidence accumulation, while very long dwell should delay escape. An intermediate optimum must reproduce across seeds and evaluation thresholds before it is treated as interesting.

## 2026-08-13 — EXP004 prospective design

### Question

Does evaluation-gated switching show a robust intermediate dwell-time optimum rather than benefiting monotonically from faster or slower switching?

### Frozen contrasts

For each of three evaluation thresholds and in pooled data, mean peak activation across block lengths 10, 15, and 20 must exceed both block 1 and block 60. The complete 9 × 3 grid and 100 seeds are fixed before implementation.

### Claim boundary

Decision intervals are externally imposed. Even if the primary contrasts pass, the result is a controlled dwell-time tradeoff, not yet emergent neural metastability.

## 2026-08-13 — EXP004 first validated sweep

### Prospective result

All frozen intermediate-versus-extreme inequalities passed at each evaluation threshold and in pooled data. Intermediate blocks 10/15/20 exceeded both one-step switching and 60-step persistence on continuous peak activation.

### Mechanism visible in supporting measures

One-step conditions repeatedly revisited frames and accumulated enough state to succeed, but required 6.7–15.5 switches on average and remained below the intermediate activation mean. Sixty-step persistence delayed useful-frame entry to step 60 when reached and reduced success to 87–91%.

### Post-result exploratory pattern

The observed optimal block increased from 3 to 5 to 10 as evaluation threshold increased from 0.001 to 0.005 to 0.02. This threshold–timescale coupling was not a frozen primary test and must be replicated prospectively.

### Next step

Use held-out seeds and a denser threshold/block grid to test whether optimal dwell is monotonically related to evidence requirement. Only after replication should it inform a self-timed dynamical controller.

## 2026-08-13 — EXP005 confirmatory design

### Discovery claim being tested

EXP004 suggested that stricter evaluation thresholds move the performance-optimal dwell interval later.

### Held-out confirmation

Use 200 unseen seeds (1,000–1,199), 12 block lengths, and seven thresholds for 16,800 runs. Confirmation requires Spearman rank correlation at least 0.8 between threshold and selected optimal block, with at most one adjacent reversal. Both criteria are fixed before implementation.

### Claim boundary

Confirmation would establish a model-specific evidence–dwell calibration. Generality across task geometries, propagation rules, and self-timed biological dynamics remains untested.

## 2026-08-13 — EXP005 held-out confirmation

### Validation

Sixteen tests passed. EXP005 generated 16,800 runs over 200 seeds unused by EXP004. The analysis applied the committed rank and reversal criteria without changing the grid or outcome.

### Result

Selected optimal blocks were 2, 3, 3, 4, 5, 7, and 10 as thresholds increased. Spearman ρ was 0.99103121 and there were no downward reversals. Both confirmatory criteria passed.

### Finding registered

F001 records a model-specific evidence–dwell calibration: productive perspective stability increases with the evidence required to validate progress. This is the project’s first confirmed interesting result, not yet a biological or human-creativity claim.

### Literature orientation

Targeted searches found close work on stability/flexibility control, autonomous creative shift-versus-dwell choices, dynamic creative-state cycles, and flexible modulation of metastable state duration. No retrieved paper directly tested the evidence-threshold-to-perspective-dwell relation. This is an inference from a targeted search, not a systematic novelty determination.

### Next research gate

Attempt to falsify F001 across alternative graph structures and propagation rules, then replace the external block clock with self-timed adaptation and mismatch dynamics. Biological implementation remains premature until those tests pass.

## 2026-08-13 — Core-hypothesis refinement after conceptual review

### Motivation

The original motivation was clarified: collaboration may aid creativity because task-relevant perspectives are distributed across people, while an individual able to access several perspectives may implement a related process internally. This raised a sharper construct question than the initial switching experiments addressed.

### Definition change

Perspective is now distinguished from generic context and from a literal reference frame. A proposed perspective must produce a reproducible, reusable change in relational geometry, feature relevance, causal or affordance prediction, or search behavior over controlled shared content. Raw perspective count is replaced by effective perspective repertoire, which includes distinctness, accessibility, switching control, and integration.

### New prospective hypotheses

H6 compares multi-perspective individuals/systems with collaborating sets of narrower individuals/systems under matched frame coverage, information, compute, and evaluation. H7 predicts that perspective diversity is beneficial only while frames remain translatable and integrable. These hypotheses were formulated after EXP001–EXP005 and are not supported by those results.

### Neural interpretation

Perspective is provisionally treated as a distributed population state with mixed selectivity rather than a fixed set of context neurons. Hippocampal-entorhinal relational maps and prefrontal task-state control are candidate interacting mechanisms. This is a literature-grounded prediction for later empirical work, not a biological conclusion from the current simulations.

### Repository and merge implication

The existing experiment stack should be preserved because it provides documented mechanistic prerequisites and maintains appropriate claim boundaries. It should be merged in dependency order only after the conceptual-refinement changes are reviewed and the full stack remains reproducible. No old result should be relabeled as evidence for the new collaboration or repertoire hypotheses.

## 2026-08-13 — EXP006 prospective falsification design

### Target

Test whether F001 survives changed graph structure and propagation normalization. The original path × source-normalized environment is retained as a positive control; branched topology and symmetric normalization yield three novel environments.

### Frozen test

Use 150 unseen seeds and the unchanged EXP005 threshold/block grid for 50,400 scheduled runs. The positive control retains the original criteria. Every novel environment must independently show a positive rank trend, limited reversals, at least three distinct optimal dwell values, and at least four interior optima. The overall robustness claim requires all three novel environments to pass.

### Boundary

This is a synthetic model robustness test. It does not test the newly introduced effective-repertoire, collaboration, or hippocampal hypotheses. Result generation begins only after this design is committed.

## 2026-08-13 — EXP006 completed

### Validation

Twenty-two unit tests passed. The generalized implementation reproduced every committed EXP005 result file byte-for-byte under the default source-normalized rule. EXP006 generated 50,400 scheduled runs, 336 aggregated cells, 28 selected optima, and four integrity summaries.

### Frozen result

The path/source positive control replicated with ρ = 0.99103121 and no reversal. All three novel environments passed the preregistered conjunction: rank correlations were 0.98198051–0.99103121, none had an adjacent reversal, each selected five or six distinct optima, and every optimum was interior.

### Interpretation

F001 is not specific to the original unbranched path or source-normalized propagation. Added uniform branches shifted optima later while preserving the monotonic evidence-demand relation. This supports structural robustness inside a still-narrow synthetic family.

### Boundary and next step

The controller still evaluates goal activation on an external block clock. EXP007 should remove that clock and test whether local mismatch/adaptation variables generate an evidence-dependent stability–flexibility relation. No collaboration, repertoire-size, or biological claim follows from EXP006.

## 2026-08-13 — EXP007 prospective self-timed design

### Artifact target

EXP004–EXP006 selected among externally imposed decision-block durations. EXP007 removes periodic boundaries and updates a mismatch/adaptation accumulator every integration step. Positive goal-evidence change can delay the next switch, making realized dwell trajectory-dependent.

### Frozen tests

Test clock-free evidence-demand calibration in the original path/source environment and the harder branched/symmetric environment. Compare against adaptation-only timing and exact-timing random replay. Require nondegenerate, variable realized dwell in addition to performance criteria.

### Boundary

This experiment still uses supervised goal activation and an intrinsic patience parameter. Passing removes one artifact explanation but does not establish biological timing, learned perspectives, creativity, or collaboration. Implementation and results begin only after this design is committed.

## 2026-08-13 — EXP007 completed with partial falsification

### Validation

Twenty-four tests passed. The experiment generated 75,600 runs and exact-timing replay matched all 25,200 source schedules.

### Passed criteria

Clock-free calibration passed in both environments (ρ = 0.95431352 and 0.99103121; zero reversals). Optimized progress coupling beat optimized adaptation-only timing at every threshold, and task-coupled frame identity beat exact-timing random replay at every threshold.

### Failed criterion

H7.4 failed in both environments. Selected controllers generally made roughly one to two switches, entered a useful frame, and retained it until the horizon. Because the final segment was right-censored and prospectively excluded, the required repeated variability among completed segments was absent. The overall conjunction therefore failed.

### Interpretation and next gate

Periodic decision blocks are not necessary for the calibration or performance-control results, but EXP007 does not establish recurrent metastable dwell. The next design must be nonabsorbing: a multi-stage task should change which perspective is useful so repeated uncensored adaptation episodes can be measured. The progress signal should simultaneously be made less solution-proximal than direct goal activation.

## 2026-08-13 — Level 1 schema-composition prototype

### Scope

The project was deliberately moved to a revised computational question: can relational schemas held from separate contexts be composed into a novel useful trajectory? Neural dynamics, ART/DFT, and biological grounding remain out of scope.

### Implementation

EXP008 adds immutable relational worlds, perspective-indexed schemas, variable binding, breadth-first effect-to-prerequisite composition, and per-step provenance. The synthetic task splits the route across support, stability, and goal perspectives.

### Controls and traceability

The same world and schemas are evaluated with structured composition, single-perspective access, and pooled facts without chaining. Results are written as JSONL events plus a JSON summary. Theory documents define perspective, composition, integration, emergence, and falsification criteria before later mechanism work.

### Interpretation boundary

Any positive result is an implementation demonstration on a toy world. It does not establish learning, biological plausibility, or creativity. Held-out object renaming, schema-order, and matched-capacity tests remain required before treating the principle as robust.

## 2026-08-13 — EXP009 and EXP010 prospective design freeze

### Milestone

Testing Genuine Compositional Emergence begins after merging the EXP008 Level 1
prototype. Biological interpretation remains closed.

### EXP009

Test role-annotated abstraction across three held-out environments and paired
object-name scrambling. Freeze single-perspective, no-chaining pool, random
selection, and perspective-erased ordinary-planning controls. Relational
generalization and distinctiveness from planning are separate criteria.

### EXP010

Require an explicit cross-perspective relation that is absent from each
perspective and from their static union. Freeze schema-removal counterfactuals,
exhaustive ordering checks, provenance, and a matched ordinary planner.

### Falsification commitment

If ordinary forward planning with the same operators reproduces the result,
the project will record that the current mechanism is not yet distinct from
ordinary planning. Structural success alone will not open the biological phase.

### Pre-execution EXP010 amendment

Before generating results, add a matched-capacity sham integration condition.
It replaces the valid bridge with an equally sized, applicable rule whose
effect is irrelevant to the goal. This prevents the static-union comparison
from attributing success merely to one additional operator or transition.
