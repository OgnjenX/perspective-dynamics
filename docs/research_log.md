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
