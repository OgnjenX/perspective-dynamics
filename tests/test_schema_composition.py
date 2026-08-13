import unittest

from perspective_dynamics.schema_composition import (
    RelationalSchema,
    RelationalWorld,
    SchemaCompositionEngine,
    demo_world,
)


class SchemaCompositionTests(unittest.TestCase):
    def test_composition_reaches_goal_with_cross_perspective_provenance(self) -> None:
        world, schemas, goal = demo_world()
        result = SchemaCompositionEngine(schemas).solve(world, goal)
        self.assertTrue(result.success)
        self.assertEqual([step.perspective for step in result.steps], ["support", "stability", "goal"])
        self.assertEqual(result.steps[0].enabled_by[:2], (("box", "box_a"), ("box", "box_b")))
        self.assertEqual(result.steps[-1].enabled_by[0], ("stable", "platform"))

    def test_single_perspective_fails_when_trajectory_is_split(self) -> None:
        world, schemas, goal = demo_world()
        engine = SchemaCompositionEngine(schemas)
        result = engine.solve(world, goal, perspectives=("support",), mode="single")
        self.assertFalse(result.success)

    def test_pooling_without_composition_does_not_create_intermediates(self) -> None:
        world, schemas, goal = demo_world()
        result = SchemaCompositionEngine(schemas).solve(world, goal, mode="pool")
        self.assertFalse(result.success)
        self.assertNotIn(("stable", "platform"), result.facts)

    def test_rejects_malformed_schema(self) -> None:
        with self.assertRaises(ValueError):
            RelationalSchema("", "support", (("a",),), (("b",),), "act")

    def test_rejects_unimplemented_random_control(self) -> None:
        world, schemas, goal = demo_world()
        with self.assertRaisesRegex(ValueError, "compose, single, or pool"):
            SchemaCompositionEngine(schemas).solve(world, goal, mode="random")

    def test_world_is_immutable_and_normalized(self) -> None:
        world = RelationalWorld.from_facts([["a", "b"], ["a", "b"]])
        self.assertEqual(world.facts, frozenset({("a", "b")}))


if __name__ == "__main__":
    unittest.main()
