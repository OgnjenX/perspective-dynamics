# Method

Three concrete training experiences separately demonstrate elevation,
stabilization, and reaching. A deterministic abstraction procedure replaces
role-annotated entity identities with variables. Role annotations are supplied;
the model does not learn them.

Testing uses three environments with new identities and surface descriptions:
construction (`crate`, `plank`, `cable`), garden (`planter`, `trellis`,
`twine`), and warehouse (`pallet`, `ramp`, `strap`). Each is paired with a
seeded bijective renaming of every entity.

Conditions use identical initial facts and goals:

- structured effect-to-prerequisite composition;
- each single perspective;
- all schemas visible without chaining produced effects;
- random schema selection with replacement;
- ordinary forward planning after erasing perspective labels.

Random selection receives exactly the number of schema checks used by the
structured condition for that task. All conditions log schema checks, actions,
produced relations, consumed relations, and schema/perspective provenance.
