# Prospective hypotheses and criteria

## H10.1 — Trajectory exclusion

For every task, the successful trajectory `τ*` must be absent from the
trajectory set of each individual perspective. Each single perspective must
fail to reach the goal.

## H10.2 — Static-union exclusion

The union of all perspective schemas without the explicit integration rule
must fail. Merely exposing more schemas or facts is insufficient.

## H10.3 — Integration sufficiency and provenance

Adding one cross-perspective rule that consumes a support-sourced relation and
a stability-sourced relation must solve every task. Every step must record its
action, perspective, schema, produced relations, and consumed relations.

## H10.4 — Counterfactual necessity

Removing either the support schema or the stability schema must eliminate the
solution in every task.

## H10.5 — Ordering and budget controls

Success and minimal plan length must be invariant across every schema ordering.
An ordinary forward planner given the same integration rule and budget must be
reported. If it is behaviorally equivalent, the experiment demonstrates an
explicit bridging operator but not a computational primitive beyond planning.

The structural emergence conjunction is H10.1–H10.4 plus ordering invariance.
The broader distinctiveness claim additionally requires non-equivalence to the
ordinary planner.
