# Predictive categories

A similarity category groups nearby input vectors. A predictive category is
also constrained by consequence: episodes that look similar but reliably
produce different outcomes should be separated.

The EXP012 learner is **ARTMAP-style**, not a full canonical ARTMAP
implementation. It uses competitive category choice, a vigilance threshold,
and prediction-error reset/refinement. This isolates the computational motif:

```text
input match → category prediction → mismatch → category refinement
```

Calling it ARTMAP-style identifies the tested algorithmic motif. It makes no
claim about biological circuitry or fidelity to every ART equation.

Prediction-driven refinement is supported only if it improves held-out outcome
prediction over matched similarity-only and random-category controls.
