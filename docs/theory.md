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

## Perspective as a constrained transformation

Let `K` denote controlled knowledge about a topic. A perspective is represented as a transformation `Tₚ`:

```text
Rₚ = Tₚ(K)
```

`Tₚ` does not need to add facts. It may instead reorganize which features, relations, predictions, or actions are accessible. This makes perspective narrower than generic context and more general than a literal spatial reference frame.

Two candidate perspectives are meaningfully distinct only if they induce a reproducible difference in representation or computation over the same content. This criterion prevents post-hoc relabeling of arbitrary contextual changes as perspectives.

## Effective perspective repertoire

The stronger project hypothesis concerns not raw frame count but an effective repertoire. Its components are:

- **coverage:** the task-relevant relational structures represented;
- **distinctness:** nonredundancy among those structures;
- **accessibility:** the ability to retrieve a potentially useful frame;
- **control:** appropriate switching and dwell;
- **integration:** preservation and combination of useful relations across frames.

These components are not assumed to combine multiplicatively, but all are candidate limiting factors. More frames can be useless or harmful when they are redundant, inaccessible, selected indiscriminately, or mutually unintelligible.

## Individual and collective organization

A person can hold multiple frames internally. A team can distribute frames across people. The proposed computational analogy is:

```text
one system with several selectable frames
                 versus
several narrower systems plus communication and integration
```

The two arrangements are not assumed to be equivalent. Collaboration introduces memory, communication, coordination, trust, and translation processes. People also do not necessarily possess task-relevant different perspectives merely because they are different individuals. The collective claim therefore requires measured frame diversity and matched information, compute, and evaluation controls.

The predicted benefit of frame distance is likely bounded. Nearby frames may be redundant; very distant frames may lack the shared structure required for translation and integration. An intermediate optimum is a prospective hypothesis.

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
- Hippocampal-entorhinal systems may support context-indexed relational maps, relational recombination, and episodic construction. Parallel maps for different relations among the same items are a particularly relevant candidate mechanism.
- Prefrontal and orbitofrontal population states may select task-relevant rules, goals, and mappings through distributed mixed selectivity and context-dependent recurrent dynamics.
- Frontostriatal competition, adaptation, neuromodulation, and mismatch signals are candidate control mechanisms.

These are mappings to investigate, not one-to-one identifications. Large-scale fMRI networks, local circuit dynamics, and psychological operations live at different explanatory levels.

The neural proposal does not require a fixed subset of neurons to encode “context” in every firing event. A perspective may be a distributed population state in which neurons show mixed selectivity for combinations of content, goal, task state, and memory. Such a state could alter gain, effective connectivity, trajectory, or downstream readout. Hippocampal-prefrontal interaction is therefore a specific candidate prediction, not the definition of perspective and not yet a project result.

## Boundary conditions and risks

- A useful solution may already be accessible within one frame.
- A switch may help by resetting search, not by changing geometry.
- “Distance to solution” can become circular if the metric is chosen after observing success.
- Neural manifolds inferred from finite data may reflect measurement or analysis choices.
- Grossberg/ART-inspired reset is one candidate mechanism, not a presupposed answer.

The experimental program must predefine representations and metrics whenever possible and use held-out tests to avoid post-hoc geometry stories.
