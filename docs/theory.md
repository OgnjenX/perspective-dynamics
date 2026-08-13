# Initial Theory

## Status

This document is a working conceptual model, not an established biological theory. Its purpose is to make assumptions explicit enough to test and revise.

## Core claim

A perspective is a control state that changes the effective computation performed over otherwise shared knowledge. Reframing therefore means changing the dynamics through which the current knowledge state evolves.

Let `x` denote a neural or model population state, `u` the problem input, and `p` the active perspective:

```text
τ dx/dt = −x + φ(W(p)x + Uu + b) + ξ(t)
```

A minimal parameterization is

```text
W(p) = W₀ + Σₖ pₖWₖ
```

where `W₀` contains shared relations and each `Wₖ` contributes perspective-specific relations. For example, separate components might emphasize function, shape, material, causal role, or another agent’s goal. This equation is a modeling proposal, not a claim that cortical connectivity is literally rebuilt whenever perspective changes; fast modulation, gating, gain control, or readout changes could alter effective connectivity.

## Functional architecture

```text
Problem and goal
       |
       v
Progress / mismatch evaluation
       |
       v
Perspective selection and gating
       |
       v
Perspective-dependent population dynamics
       |
       v
Associative knowledge and candidate generation
       |
       v
Validity, usefulness, and novelty evaluation
```

Feedback is essential: failure to make progress can destabilize the current perspective; promising candidates can prolong it; evaluation can reject novel but invalid states.

## Three mechanistic strengths

1. **Readout switching:** `yₚ = Dₚx`. A different decoder interprets a largely unchanged internal state.
2. **Subspace gating or rotation:** context amplifies relevant axes and suppresses others, changing effective distances and generalization.
3. **Attractor-landscape restructuring:** contextual modulation changes the vector field, stability, basins, and transition probabilities.

These mechanisms should be compared rather than conflated. The strongest version of the theory predicts more than a readout change.

## Why geometry could help

Suppose knowledge item `zᵢ` has a perspective-dependent representation:

```text
rᵖᵢ = Eₚ(zᵢ)
dₚ(zᵢ, zⱼ) = ‖Eₚ(zᵢ) − Eₚ(zⱼ)‖
```

Locally biased associative processes can fail when the solution is remote under the current metric. A useful frame can bring a task-relevant relation closer without adding the solution to memory. The computational sequence is:

> **Frame selection → search/elaboration within frame → cross-frame integration → evaluation.**

The integration and evaluation steps prevent “more perspectives” from being equated with creativity.

## Proposed dynamical regimes

| Regime | Candidate dynamics | Expected consequence |
|---|---|---|
| Strong persistence, weak adaptation | Deep or long-lived state | Fixation |
| Moderate persistence and adaptation | Metastable frame sequence | Productive exploration |
| Excessive switching or noise | Short, weakly coherent states | Fragmentation |
| Stable frame plus no integration | Local elaboration only | Conventional solutions |

The predicted inverted-U concerns a defined switching-control parameter, not an unrestricted claim that all neural variability improves creativity.

## Candidate biological correspondences

- Default-mode systems may contribute internally generated associations and simulations.
- Executive-control systems may maintain goals, constrain search, and evaluate candidates.
- Salience/midcingulo-insular systems may contribute switching or prioritization signals.
- Hippocampal systems may support relational recombination and episodic construction.
- Frontostriatal competition, adaptation, neuromodulation, and mismatch signals are candidate control mechanisms.

These are mappings to investigate, not one-to-one identifications. Large-scale fMRI networks, local circuit dynamics, and psychological operations live at different explanatory levels.

## Boundary conditions and risks

- A useful solution may already be accessible within one frame.
- A switch may help by resetting search, not by changing geometry.
- “Distance to solution” can become circular if the metric is chosen after observing success.
- Neural manifolds inferred from finite data may reflect measurement or analysis choices.
- Grossberg/ART-inspired reset is one candidate mechanism, not a presupposed answer.

The experimental program must predefine representations and metrics whenever possible and use held-out tests to avoid post-hoc geometry stories.
