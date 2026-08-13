"""Interpretable Level 1 relational-schema composition prototype.

This module deliberately contains no neural dynamics.  It tests whether
perspective-indexed relational schemas can be composed into a plan when no
single schema contains the complete trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

Fact = tuple[str, ...]


def _matches(pattern: Fact, fact: Fact, bindings: dict[str, str]) -> dict[str, str] | None:
    if len(pattern) != len(fact) or pattern[0] != fact[0]:
        return None
    result = dict(bindings)
    for expected, actual in zip(pattern[1:], fact[1:]):
        if expected.startswith("?"):
            if expected in result and result[expected] != actual:
                return None
            result[expected] = actual
        elif expected != actual:
            return None
    return result


def _ground(pattern: Fact, bindings: dict[str, str]) -> Fact:
    return tuple(bindings.get(token, token) for token in pattern)


@dataclass(frozen=True)
class RelationalWorld:
    """A finite world represented as a deterministic set of relational facts."""

    facts: frozenset[Fact]

    @classmethod
    def from_facts(cls, facts: Iterable[Fact]) -> "RelationalWorld":
        normalized = frozenset(tuple(fact) for fact in facts)
        if any(not fact for fact in normalized):
            raise ValueError("facts must be non-empty tuples")
        return cls(normalized)


@dataclass(frozen=True)
class RelationalSchema:
    """A reusable affordance schema indexed by a perspective."""

    name: str
    perspective: str
    prerequisites: tuple[Fact, ...]
    effects: tuple[Fact, ...]
    action: str

    def __post_init__(self) -> None:
        if not self.name or not self.perspective or not self.action:
            raise ValueError("schema name, perspective, and action are required")
        if not self.prerequisites or not self.effects:
            raise ValueError("schemas need prerequisites and effects")


@dataclass(frozen=True)
class PlanStep:
    schema: str
    perspective: str
    action: str
    produced: tuple[Fact, ...]
    enabled_by: tuple[Fact, ...]


@dataclass(frozen=True)
class CompositionResult:
    success: bool
    goal: Fact
    facts: frozenset[Fact]
    steps: tuple[PlanStep, ...]
    explored_states: int
    reason: str
    schema_checks: int = 0


class SchemaCompositionEngine:
    """Breadth-first forward planner with explicit schema provenance.

    ``mode='compose'`` matches schema effects to later prerequisites.  The
    baseline modes intentionally restrict that operation for comparison:
    ``single`` accesses one perspective, while ``pool`` exposes all schemas
    but cannot use newly produced facts.  A genuine randomized-composition
    control is intentionally deferred to EXP009, where its sampling policy and
    compute budget can be specified prospectively.
    """

    def __init__(self, schemas: Iterable[RelationalSchema]) -> None:
        self.schemas = tuple(schemas)
        if len({schema.name for schema in self.schemas}) != len(self.schemas):
            raise ValueError("schema names must be unique")

    def solve(
        self,
        world: RelationalWorld,
        goal: Fact,
        *,
        perspectives: tuple[str, ...] | None = None,
        mode: str = "compose",
        max_schema_checks: int | None = None,
    ) -> CompositionResult:
        if mode not in {"compose", "single", "pool"}:
            raise ValueError("mode must be compose, single, or pool")
        allowed = set(perspectives) if perspectives is not None else None
        schemas = tuple(
            schema for schema in self.schemas
            if allowed is None or schema.perspective in allowed
        )
        if mode == "single" and len({s.perspective for s in schemas}) > 1:
            raise ValueError("single mode requires one perspective")
        if goal in world.facts:
            return CompositionResult(True, goal, world.facts, (), 0, "goal already present")
        if max_schema_checks is not None and max_schema_checks < 1:
            raise ValueError("max_schema_checks must be positive")

        # States are (facts, provenance).  The search is finite because each
        # schema application only adds facts and duplicate states are pruned.
        frontier: list[tuple[frozenset[Fact], tuple[PlanStep, ...]]] = [(world.facts, ())]
        seen = {world.facts}
        explored = 0
        schema_checks = 0
        while frontier:
            facts, steps = frontier.pop(0)
            explored += 1
            for schema in schemas:
                schema_checks += 1
                if max_schema_checks is not None and schema_checks > max_schema_checks:
                    return CompositionResult(
                        False, goal, facts, steps, explored,
                        "schema-check budget exhausted", max_schema_checks,
                    )
                for bindings, enabled in self._bindings(schema, facts):
                    produced = tuple(_ground(effect, bindings) for effect in schema.effects)
                    new_facts = facts | set(produced)
                    if new_facts == facts or new_facts in seen:
                        continue
                    seen.add(new_facts)
                    step = PlanStep(
                        schema.name, schema.perspective,
                        schema.action.format(**{key.lstrip("?"): value for key, value in bindings.items()}),
                        produced, tuple(enabled),
                    )
                    new_steps = steps + (step,)
                    if goal in new_facts:
                        return CompositionResult(
                            True, goal, new_facts, new_steps, explored,
                            "goal reached", schema_checks,
                        )
                    # The baselines expose stored facts but do not compose
                    # effects into later prerequisites.
                    if mode == "pool":
                        continue
                    frontier.append((new_facts, new_steps))
        return CompositionResult(
            False, goal, world.facts, (), explored,
            "no compositional plan", schema_checks,
        )

    @staticmethod
    def _bindings(schema: RelationalSchema, facts: frozenset[Fact]) -> list[tuple[dict[str, str], list[Fact]]]:
        candidates: list[tuple[dict[str, str], list[Fact]]] = [({}, [])]
        for prerequisite in schema.prerequisites:
            next_candidates: list[tuple[dict[str, str], list[Fact]]] = []
            for bindings, enabled in candidates:
                for fact in sorted(facts):
                    updated = _matches(prerequisite, fact, bindings)
                    if updated is not None and len(set(updated.values())) == len(updated):
                        next_candidates.append((updated, enabled + [fact]))
            candidates = next_candidates
        return candidates


def demo_world() -> tuple[RelationalWorld, tuple[RelationalSchema, ...], Fact]:
    """Return the prospective Phase 1 task used by EXP008."""
    world = RelationalWorld.from_facts(
        [("box", "box_a"), ("box", "box_b"),
         ("available", "board"), ("available", "rope"),
         ("target_high", "target")]
    )
    schemas = (
        RelationalSchema(
            "assemble_platform", "support",
            (("box", "?left"), ("box", "?right"), ("available", "board")),
            (("elevated", "platform"), ("supports", "platform", "agent")),
            "place board on {left} and {right}",
        ),
        RelationalSchema(
            "secure_platform", "stability",
            (("available", "rope"), ("elevated", "platform")),
            (("stable", "platform"),),
            "tie rope around platform",
        ),
        RelationalSchema(
            "reach_target", "goal",
            (("stable", "platform"), ("target_high", "target")),
            (("reached", "target"),),
            "climb stable platform to target",
        ),
    )
    return world, schemas, ("reached", "target")
