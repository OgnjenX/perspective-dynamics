# Perspective Dynamics

**Working title:** *Perspective Dynamics: A Neurocomputational Theory of Creativity Through Adaptive Representational Frames*

## Research question

Can creativity emerge from neural systems that dynamically change the representational frame in which knowledge is processed?

## Core hypothesis

A creative solution may not require finding a new path through a fixed representation. It may instead become reachable when a system changes the geometry and dynamics of its internal representation. The refined hypothesis concerns an **effective perspective repertoire**: creativity should benefit from access to several distinct frames only when the system can retrieve, select, dwell within, and integrate them.

A fixed-frame system can be written schematically as:

```text
dx/dt = F(x)
```

A perspective-dependent system is:

```text
dx/dt = F(x, p)
```

Here, `x` is the system state and `p` is the active perspective or context. The claim to test is that changing `p` can alter effective distances, transition paths, and attractor accessibility—not merely add noise or more information.

The project treats collaboration as a second organizational form of this proposal: different task-relevant frames may be distributed across people rather than held within one person. This is a hypothesis to test under matched information and compute, not an assumption that more people or greater demographic diversity automatically improves creativity.

## Long-term goal

Develop and evaluate a biologically grounded computational theory connecting:

- creative cognition and insight;
- neural population dynamics and metastability;
- representational geometry and reference frames;
- contextual modulation and adaptive switching;
- candidate Grossberg-inspired mechanisms such as competition, adaptation, and mismatch/reset.

## Project status

Week 1 framing and eight computational experiments are complete. `EXP001`–`EXP006` established and structurally challenged a model-specific evidence-demand/dwell relation. `EXP007` removed periodic decision blocks: calibration and matched controls passed, but the full experiment failed because productive frames became horizon-censored absorbing states rather than demonstrating repeated variable completed dwell. `EXP008` establishes only that explicit cross-perspective schema composition is implementable in one hand-designed synthetic world. It is a Level 1 prototype, not evidence for creativity, generalization, learning, or biology.

Run the fully reproducible baseline with:

```text
make reproduce
```

## Documentation map

- [Research question](docs/research_question.md)
- [Theory](docs/theory.md)
- [Falsifiable hypotheses](docs/hypotheses.md)
- [Experimental plan](docs/experimental_plan.md)
- [Literature map](docs/literature_review.md)
- [Decision record](docs/decisions.md)
- [Research log](docs/research_log.md)
- [Findings registry](docs/findings.md)
- [Research milestones](docs/milestones.md)

## Research principles

1. Separate established evidence, working interpretation, and speculation.
2. Define outcomes and falsification criteria before running experiments.
3. Compare adaptive perspective change with fixed-frame, random-switching, and matched-control systems.
4. Preserve exact configurations, seeds, environments, outputs, and negative results once implementation begins.
5. Treat biological grounding as a constraint on an established computational effect, not as decoration.

## Planned public repository

Repository: `OgnjenX/perspective-dynamics`

The local Git repository is initialized on `main` with the intended GitHub remote configured. Publication is a separate step and has not been performed during Week 1 initialization.
