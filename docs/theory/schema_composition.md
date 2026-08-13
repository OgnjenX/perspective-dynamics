# Schema composition

Schema composition constructs a plan by matching effects of one relational schema to prerequisites of another. Given schemas `S₁` and `S₂`, composition is possible when:

```text
effects(S₁) unify with prerequisites(S₂)
```

The resulting plan contains the action sequence and intermediate relation linking the schemas. The prototype uses deterministic forward chaining with variable binding and breadth-first search.

Composition must be compared with a single perspective, all-schema access without effect-to-prerequisite chaining, and randomized controls. Otherwise success could be attributed to more stored facts, more actions, or more search rather than integration.

This tests sufficiency of an explicit symbolic operation; it does not test learning, neural implementation, or human-like generalization.
