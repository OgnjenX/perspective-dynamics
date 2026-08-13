"""Generalization and explicit-integration tasks for EXP009 and EXP010."""

from __future__ import annotations

from dataclasses import dataclass, replace
from random import Random
from typing import Iterable

from .schema_composition import (
    CompositionResult,
    Fact,
    PlanStep,
    RelationalSchema,
    RelationalWorld,
    SchemaCompositionEngine,
    _ground,
)


@dataclass(frozen=True)
class ConcreteExperience:
    """One observed transition with supervised entity-to-role annotations."""

    name: str
    perspective: str
    prerequisites: tuple[Fact, ...]
    effects: tuple[Fact, ...]
    action: str
    entity_variables: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class GeneralizationTask:
    name: str
    world: RelationalWorld
    goal: Fact


def abstract_experience(experience: ConcreteExperience) -> RelationalSchema:
    """Replace supervised concrete entities with variables.

    The mapping is deliberately supplied rather than learned.  EXP009 tests
    transfer of the resulting relational schema, not discovery of object roles.
    """

    mapping = dict(experience.entity_variables)

    def abstract_fact(fact: Fact) -> Fact:
        return tuple(mapping.get(token, token) for token in fact)

    action = experience.action
    for entity, variable in experience.entity_variables:
        action = action.replace(entity, "{" + variable.lstrip("?") + "}")
    return RelationalSchema(
        name=experience.name,
        perspective=experience.perspective,
        prerequisites=tuple(abstract_fact(fact) for fact in experience.prerequisites),
        effects=tuple(abstract_fact(fact) for fact in experience.effects),
        action=action,
    )


def training_experiences() -> tuple[ConcreteExperience, ...]:
    """Concrete component transitions; no complete solution is demonstrated."""

    return (
        ConcreteExperience(
            "construct_elevation", "support",
            (("support_role", "chair_left"), ("support_role", "chair_right"),
             ("surface_role", "shelf")),
            (("elevated_surface", "shelf"),),
            "place shelf on chair_left and chair_right",
            (("chair_left", "?left"), ("chair_right", "?right"),
             ("shelf", "?surface")),
        ),
        ConcreteExperience(
            "stabilize_elevation", "stability",
            (("stabilizer_role", "training_rope"),
             ("elevated_surface", "training_podium")),
            (("stable_surface", "training_podium"),),
            "secure training_podium with training_rope",
            (("training_rope", "?stabilizer"),
             ("training_podium", "?surface")),
        ),
        ConcreteExperience(
            "reach_high_target", "goal",
            (("stable_surface", "training_pedestal"),
             ("high_target", "training_bell")),
            (("reached", "training_bell"),),
            "climb training_pedestal to training_bell",
            (("training_pedestal", "?surface"),
             ("training_bell", "?target")),
        ),
    )


def generalized_schemas() -> tuple[RelationalSchema, ...]:
    return tuple(abstract_experience(item) for item in training_experiences())


_ENVIRONMENTS = {
    "construction": ("crate_a", "crate_b", "plank", "cable", "wall_marker"),
    "garden": ("planter_a", "planter_b", "trellis", "twine", "fruit"),
    "warehouse": ("pallet_a", "pallet_b", "ramp", "strap", "high_shelf"),
}


def generalized_tasks() -> tuple[GeneralizationTask, ...]:
    tasks = []
    for name, (left, right, surface, stabilizer, target) in _ENVIRONMENTS.items():
        tasks.append(GeneralizationTask(
            name,
            RelationalWorld.from_facts((
                ("support_role", left), ("support_role", right),
                ("surface_role", surface), ("stabilizer_role", stabilizer),
                ("high_target", target),
            )),
            ("reached", target),
        ))
    return tuple(tasks)


def scramble_task(task: GeneralizationTask, seed: int) -> GeneralizationTask:
    """Apply a seeded bijection to entities while preserving predicates."""

    entities = sorted({token for fact in task.world.facts for token in fact[1:]})
    rng = Random(f"{seed}:{task.name}")
    labels = [f"entity_{index}" for index in range(len(entities))]
    rng.shuffle(labels)
    mapping = dict(zip(entities, labels))
    facts = [tuple([fact[0], *(mapping[token] for token in fact[1:])])
             for fact in task.world.facts]
    goal = tuple([task.goal[0], *(mapping[token] for token in task.goal[1:])])
    return GeneralizationTask(
        task.name + "_scrambled", RelationalWorld.from_facts(facts), goal
    )


def perspective_erased(schemas: Iterable[RelationalSchema]) -> tuple[RelationalSchema, ...]:
    """Construct the matched ordinary-planning operator set."""

    return tuple(replace(schema, perspective="ordinary_planner") for schema in schemas)


def run_random_schema_selection(
    world: RelationalWorld,
    schemas: tuple[RelationalSchema, ...],
    goal: Fact,
    *,
    seed: int,
    schema_check_budget: int,
) -> CompositionResult:
    """Sample schemas without alignment under a matched check budget."""

    rng = Random(seed)
    facts = world.facts
    steps: tuple[PlanStep, ...] = ()
    for check in range(1, schema_check_budget + 1):
        schema = rng.choice(schemas)
        applications = SchemaCompositionEngine._bindings(schema, facts)
        if not applications:
            continue
        bindings, enabled = rng.choice(applications)
        produced = tuple(_ground(effect, bindings) for effect in schema.effects)
        new_facts = facts | set(produced)
        if new_facts == facts:
            continue
        step = PlanStep(
            schema.name,
            schema.perspective,
            schema.action.format(**{
                key.lstrip("?"): value for key, value in bindings.items()
            }),
            produced,
            tuple(enabled),
        )
        steps += (step,)
        facts = new_facts
        if goal in facts:
            return CompositionResult(
                True, goal, facts, steps, check, "goal reached", check
            )
    return CompositionResult(
        False, goal, facts, steps, schema_check_budget,
        "schema-check budget exhausted", schema_check_budget,
    )


def integration_schemas() -> tuple[RelationalSchema, ...]:
    """Schemas for EXP010, including one explicit cross-perspective bridge."""

    return (
        RelationalSchema(
            "produce_support_relation", "support",
            (("support_role", "?left"), ("support_role", "?right"),
             ("surface_role", "?surface")),
            (("support:elevated", "?surface"),),
            "elevate {surface} on {left} and {right}",
        ),
        RelationalSchema(
            "produce_stability_relation", "stability",
            (("stabilizer_role", "?stabilizer"),
             ("surface_role", "?surface")),
            (("stability:secured", "?surface"),),
            "secure {surface} with {stabilizer}",
        ),
        RelationalSchema(
            "integrate_stable_elevation", "integration",
            (("support:elevated", "?surface"),
             ("stability:secured", "?surface")),
            (("integrated:stable_elevation", "?surface"),),
            "recognize {surface} as stable elevation",
        ),
        RelationalSchema(
            "use_integrated_relation", "goal",
            (("integrated:stable_elevation", "?surface"),
             ("high_target", "?target")),
            (("reached", "?target"),),
            "use {surface} to reach {target}",
        ),
    )


def sham_integration_schemas() -> tuple[RelationalSchema, ...]:
    """Replace the valid bridge with an equally sized goal-irrelevant bridge."""

    schemas = list(integration_schemas())
    schemas[2] = RelationalSchema(
        "sham_integration", "integration_control",
        (("support:elevated", "?surface"),
         ("stability:secured", "?surface")),
        (("integrated:decorative_combination", "?surface"),),
        "recognize {surface} as a decorative combination",
    )
    return tuple(schemas)
