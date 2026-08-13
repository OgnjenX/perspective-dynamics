# SOM and ART-style hypothesis

## Hypothesis ladder

1. Similarity-based self-organization can recover coarse relational families.
2. Prediction-error refinement can form categories better aligned with action
   consequences than similarity alone.
3. Different predictive targets over the same episodes can induce different,
   reusable organizations: candidate computational perspectives.
4. Cross-category prediction can expose a useful conjunction absent as an
   explicit training label: a candidate bridge relation.

## Distinguishing tests

The learned system must be compared with hand-written schemas, exact-memory
ordinary planning, random clustering, SOM without prediction, and predictive
vigilance learning. A learned bridge is not distinct from planning if the
ordinary planner receives the same inferred rule. The relevant comparison
withholds that rule from both systems and asks whether learning from the same
episode corpus constructs a transferable representation.

## Boundary

These experiments test algorithmic motifs inspired by SOM and ART/ARTMAP. They
are not neural dynamics, Grossberg interpretation, or biological grounding.
