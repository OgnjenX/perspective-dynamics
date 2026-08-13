# Research Question

## Main question

Does access to a diverse, usable repertoire of representational perspectives provide a computational advantage for creative problem solving compared with searching within a fixed representation?

The same question applies at two organizational scales:

1. **Within-person:** can one system represent the same topic through several distinct frames and selectively switch among them?
2. **Between-person:** can collaboration distribute those frames across people and then recover the advantage through communication and integration?

## Why this matters

People often escape an impasse by changing viewpoint, abstraction level, interpretation, assumed constraint, goal, or reference frame. Existing accounts of creativity emphasize associative search, recombination, stochastic exploration, memory retrieval, and interaction between spontaneous and controlled cognition. These mechanisms may be necessary, but they do not by themselves explain why a reframing makes a previously obscure relation actionable.

This project tests a more specific proposal:

> Creativity can sometimes arise because a system transforms the representational space in which its existing knowledge is processed.

Under this proposal, a perspective changes which relations are emphasized, which states are nearby, which trajectories are reachable, and which candidate solutions are stable. The proposed causal chain is:

> **Perspective change → effective geometry/dynamics change → new solution accessibility.**

## Operational definitions

**Context** is any task-relevant surrounding state, including goals, instructions, recent history, location, affect, or social situation.

**Reference frame** specifies coordinates or relations in which content is represented.

**Perspective** is an active, structured representational frame applied to otherwise shared subject matter. It changes at least one of: feature weighting, relational structure, causal or affordance interpretation, transition dynamics, or readout. Every perspective is contextual, but not every contextual change is a perspective.

A proposed context counts as a perspective only if, while factual content and task goal are controlled, it produces a reproducible and reusable change in at least one of:

1. similarities or neighborhoods among items;
2. feature relevance or attention;
3. causal, functional, or affordance predictions;
4. search trajectories and candidate solutions.

Merely adding information, noise, an arbitrary label, or a transient cue without changing one of those computations does not count.

**Perspective change** is a measurable transition from one such contextual state to another while the underlying knowledge items and task goal remain controlled.

**Creative advantage** is improved production of solutions that are both novel relative to a defined comparison set and valid/useful under explicit task constraints. Novelty alone is insufficient.

**Representational geometry** is the pattern of relations among population or model states, quantified using preregistered measures such as distances, angles, neighborhood structure, dimensionality, or cross-condition generalization.

**Perspective repertoire** is the set of distinct perspectives a person, team, or model can access for a topic. Raw count is not the proposed explanatory variable. An **effective repertoire** additionally requires that frames are meaningfully distinct, retrievable, selectively activated, and capable of being integrated into a task-valid solution.

**Perspective distance** is a preregistered difference between frames, measured through their relational geometry, predictions, or induced search behavior. Demographic difference, separate identity, or the mere presence of another person is not by itself evidence of task-relevant perspective distance.

## Subquestions

1. Can a system solve selected problems by changing perspective without acquiring new factual information?
2. Does structured, goal-sensitive switching outperform random switching and matched noise?
3. Does success require a metastable regime between fixation and incoherent switching?
4. Do successful switches measurably reduce solution distance or reshape accessibility in state space?
5. Which effects survive changes in model class and biologically plausible implementation?
6. Does creativity vary with effective perspective repertoire after knowledge, capacity, compute, and time are matched?
7. Can a multi-perspective individual and a collaborating set of narrower agents obtain the same advantage when frame coverage and integration opportunity are matched?
8. Is perspective distance beneficial only up to the point at which translation and integration fail?

## Scope boundaries

The project does not assume that all creativity requires perspective change, that every subjective “Aha!” reflects restructuring, or that one large-scale brain network is a creativity center. It begins with constrained problem settings where representations can be specified and manipulated. Claims about open-ended human creativity will require separate evidence.

## Principal alternatives

- **More search:** switching helps only because it increases the number of sampled states.
- **Noise/arousal:** any perturbation of comparable magnitude would help equally.
- **Extra information:** the new cue supplies the answer instead of changing a representation.
- **Generic executive control:** benefits reflect task switching rather than perspective-specific geometry.
- **Readout-only change:** the internal representation stays fixed and only the decoder changes.
- **More agents or capacity:** a team or multi-frame model helps only because it contains more knowledge, parameters, samples, or compute.
- **Ensemble voting:** independent solution generation plus selection explains performance without cross-perspective transformation or integration.
- **Communication benefit:** collaboration helps through error correction or motivation rather than perspective diversity.

Experiments must distinguish the central proposal from these alternatives.

## Evidence threshold

The strongest initial evidence would combine: (1) a controlled behavioral or computational advantage over the alternatives above; (2) a perspective-specific geometric change preceding solution; and (3) mediation or intervention evidence linking that change to success. For the repertoire claim, total information, model capacity, compute, and evaluation opportunity must be held constant. For the collaboration claim, frame diversity must be measured rather than inferred from headcount or demographic categories. A performance gain without a geometric or dynamical signature would support a weaker switching or ensemble account, not the full theory.
