# Schema learning

## Computational target

A schema is no longer supplied as an operator. It is a reusable predictive
regularity inferred from episodes containing observable features, actions, and
outcomes. Object names are retained only for audit and held-out tests; they are
not privileged explanatory variables.

For episode `e = (x, a, y)`, schema discovery seeks a category `c` such that:

```text
c groups episodes by reusable structure in x and a
c predicts y on unseen objects
```

The immediate claim is narrow: learned categories may provide abstractions for
transfer. It does not imply semantic understanding, creativity, or neural
implementation.

## Evidence requirements

Training and test object identities must be disjoint. Identity scrambling must
not change predictions. Random clustering, similarity-only clustering,
hand-written schemas, and memory/planning controls must be reported. Category
definitions, assignments, prediction errors, and refinements remain auditable.
