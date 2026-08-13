# EXP002 Method

## Shared content and matched frames

Each task uses ten named nodes: one cue, one goal, and eight bridge nodes. Every perspective is a weighted path containing all ten nodes exactly once. Therefore each frame has:

- identical node identities;
- nine undirected edges;
- the same nine edge weights for a given seed;
- one degree-one cue, one degree-one terminal bridge, and eight degree-two nodes;
- no additional facts, nodes, or compute.

Only the order of nodes along the path changes. The useful frame places the goal two edges from the cue, the initial frame places it six edges away, and the irrelevant frame places it eight edges away. The goal remains a degree-two internal node in every frame.

The mixed control averages corresponding adjacency matrices with equal coefficients. It has the same total edge-weight mass as one frame but can contain more nonzero edges.

## Dynamics

All conditions reuse the EXP001 leaky spreading-activation model without changing its parameters. Constant input is applied only to `cue`. The goal is used for scoring and never supplied to the dynamics.

## Design

Four conditions are crossed with 50 predetermined seeds, yielding 200 runs. A seed controls the shared edge-weight list and bridge permutations. All conditions for a seed reuse exactly the same generated task family.

## Outcomes

- success at the prespecified 0.01 threshold;
- first-passage step;
- peak goal activation;
- final goal rank;
- realized unweighted cue-to-goal distance;
- graph node count, edge count, and total undirected weight for integrity checks.

## Analysis

Report condition-level means or medians and paired useful-minus-initial differences by seed. The primary result requires the useful advantage to have the predicted sign for peak activation across seeds, not only a threshold-dependent success difference. No inferential population claim is made because seeds instantiate controlled synthetic tasks rather than sampled people or natural environments.
