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
