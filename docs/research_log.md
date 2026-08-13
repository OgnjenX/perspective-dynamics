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
