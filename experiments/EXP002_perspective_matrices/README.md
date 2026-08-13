# EXP002 — Matched Perspective Matrices

## Position in the research program

EXP001 established how a single fixed relational graph attenuates activation with distance and distraction. EXP002 introduces multiple perspectives over the **same nodes** and asks whether changing only their relational organization changes solution accessibility.

This is the minimal geometry test. It does not yet implement switching, adaptation, metastability, or biological mechanisms.

## Question

When graph size, edge count, edge-weight distribution, node identities, dynamics, cue input, and compute are controlled, does a perspective that places the goal nearer to the cue increase goal accessibility?

## Conditions

- `fixed_initial`: goal is six edges from the cue;
- `fixed_useful`: goal is two edges from the cue;
- `fixed_irrelevant`: goal is eight edges from the cue;
- `mixed`: equal blend of all three frame matrices.

Every individual frame is a weighted path over the same ten nodes. Frame construction changes node ordering only. Fifty fixed seeds generate weight lists and bridge permutations.

## Reproduce

From the repository root:

```text
make exp002
make analyze-exp002
```

The prospective hypothesis and method were written before implementing or running the experiment.
