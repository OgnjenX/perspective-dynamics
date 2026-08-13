# Prospective criteria

H14.1: predictive learning selects a successful candidate trajectory in at
least 80% of held-out environments.

H14.2: its success exceeds exact-memory ordinary planning, random clustering,
and SOM-without-prediction by at least 0.25 each.

H14.3: the minimal shared positive-category explanation contains both
`elevated` and `stable`, contains no object identity, and was never supplied as
a feature or schema named `stable_elevation`.

H14.4: removing either elevation or stability evidence reduces predictive
success by at least 0.50.

H14.5: identity scrambling leaves selected trajectories unchanged.

Hand-written schemas are reported as an oracle reference. Predictive learning
need not exceed that oracle for EXP014 to pass. Overall success requires
H14.1–H14.5. Even success would establish learned predictive abstraction in a
synthetic task, not creativity or biology.
