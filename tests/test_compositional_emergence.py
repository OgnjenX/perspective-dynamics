import unittest

from perspective_dynamics.compositional_emergence import (
    generalized_schemas,
    generalized_tasks,
    integration_schemas,
    perspective_erased,
    run_random_schema_selection,
    scramble_task,
    sham_integration_schemas,
    training_experiences,
)
from perspective_dynamics.schema_composition import SchemaCompositionEngine


class GeneralizationTests(unittest.TestCase):
    def test_abstract_schemas_contain_no_training_entities(self) -> None:
        training_entities = {
            entity
            for experience in training_experiences()
            for entity, _ in experience.entity_variables
        }
        tokens = {
            token
            for schema in generalized_schemas()
            for fact in schema.prerequisites + schema.effects
            for token in fact[1:]
        }
        self.assertTrue(all(token.startswith("?") for token in tokens))
        self.assertTrue(training_entities.isdisjoint(tokens))

    def test_generalized_schemas_solve_all_held_out_tasks(self) -> None:
        engine = SchemaCompositionEngine(generalized_schemas())
        for task in generalized_tasks():
            with self.subTest(task=task.name):
                self.assertTrue(engine.solve(task.world, task.goal).success)

    def test_name_scrambling_preserves_schema_sequence(self) -> None:
        schemas = generalized_schemas()
        engine = SchemaCompositionEngine(schemas)
        for task in generalized_tasks():
            original = engine.solve(task.world, task.goal)
            scrambled_task = scramble_task(task, 9009)
            scrambled = engine.solve(scrambled_task.world, scrambled_task.goal)
            self.assertEqual(original.success, scrambled.success)
            self.assertEqual(
                [step.schema for step in original.steps],
                [step.schema for step in scrambled.steps],
            )

    def test_perspective_erased_planner_is_behaviorally_equivalent(self) -> None:
        task = generalized_tasks()[0]
        structured = SchemaCompositionEngine(generalized_schemas()).solve(
            task.world, task.goal
        )
        ordinary = SchemaCompositionEngine(
            perspective_erased(generalized_schemas())
        ).solve(task.world, task.goal)
        self.assertEqual(structured.success, ordinary.success)
        self.assertEqual(
            [step.schema for step in structured.steps],
            [step.schema for step in ordinary.steps],
        )
        self.assertEqual(structured.schema_checks, ordinary.schema_checks)

    def test_random_selection_respects_check_budget(self) -> None:
        task = generalized_tasks()[0]
        result = run_random_schema_selection(
            task.world, generalized_schemas(), task.goal,
            seed=9100, schema_check_budget=2,
        )
        self.assertFalse(result.success)
        self.assertEqual(result.schema_checks, 2)


class EmergentTrajectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = generalized_tasks()[0]
        self.schemas = integration_schemas()

    def test_integration_rule_creates_required_relation(self) -> None:
        result = SchemaCompositionEngine(self.schemas).solve(
            self.task.world, self.task.goal
        )
        self.assertTrue(result.success)
        self.assertEqual(len(result.steps), 4)
        self.assertIn(
            ("integrated:stable_elevation", "plank"),
            result.steps[-1].enabled_by,
        )

    def test_static_union_without_integration_fails(self) -> None:
        static_union = tuple(
            schema for schema in self.schemas if schema.perspective != "integration"
        )
        result = SchemaCompositionEngine(static_union).solve(
            self.task.world, self.task.goal
        )
        self.assertFalse(result.success)

    def test_each_component_is_counterfactually_necessary(self) -> None:
        for removed in ("support", "stability"):
            remaining = tuple(
                schema for schema in self.schemas if schema.perspective != removed
            )
            with self.subTest(removed=removed):
                self.assertFalse(
                    SchemaCompositionEngine(remaining).solve(
                        self.task.world, self.task.goal
                    ).success
                )

    def test_matched_capacity_sham_fails(self) -> None:
        result = SchemaCompositionEngine(sham_integration_schemas()).solve(
            self.task.world, self.task.goal
        )
        self.assertFalse(result.success)
        self.assertEqual(len(sham_integration_schemas()), len(self.schemas))


if __name__ == "__main__":
    unittest.main()
