import unittest

from perspective_dynamics.schema_learning import (
    CompetitiveLearner,
    FeatureSpace,
    PredictiveVigilanceLearner,
    SelfOrganizingMap1D,
    accuracy,
    bridge_episodes,
    category_labels,
    cluster_purity,
    multi_target_episodes,
    predict_from_categories,
    predictive_conflict_episodes,
    schema_discovery_episodes,
)


class SchemaLearningTests(unittest.TestCase):
    def test_vectorizer_excludes_identity(self) -> None:
        train, test = schema_discovery_episodes()
        space = FeatureSpace(train)
        self.assertEqual(space.transform(train[0]), space.transform(test[0]))
        self.assertTrue(all("train_" not in name for name in space.names))

    def test_competitive_and_som_recover_schema_families(self) -> None:
        train, test = schema_discovery_episodes()
        space = FeatureSpace(train)
        vectors = [space.transform(item) for item in train]
        labels = [item.outcome for item in train]
        for model_type in (CompetitiveLearner, SelfOrganizingMap1D):
            model = model_type(3, 80, 0.35, 11011).fit(vectors)
            assignments = [model.category(vector) for vector in vectors]
            mapping = category_labels(assignments, labels)
            predicted = predict_from_categories(
                model, [space.transform(item) for item in test], mapping, labels[0]
            )
            self.assertEqual(cluster_purity(assignments, labels), 1.0)
            self.assertEqual(accuracy([item.outcome for item in test], predicted), 1.0)

    def test_predictive_refinement_responds_to_mismatch(self) -> None:
        train, test = predictive_conflict_episodes()
        space = FeatureSpace(train)
        model = PredictiveVigilanceLearner(0.65).fit(
            [space.transform(item) for item in train],
            [item.outcome for item in train],
        )
        predicted = [model.predict(space.transform(item)) for item in test]
        self.assertEqual(accuracy([item.outcome for item in test], predicted), 1.0)
        self.assertGreater(model.reset_count, 0)

    def test_different_targets_induce_different_assignments(self) -> None:
        train, _ = multi_target_episodes()
        space = FeatureSpace(train)
        vectors = [space.transform(item) for item in train]
        assignments = []
        for field in ("physical_target", "functional_target", "goal_target"):
            model = PredictiveVigilanceLearner(0.6).fit(
                vectors, [getattr(item, field) for item in train]
            )
            assignments.append([model.category(vector) for vector in vectors])
        self.assertNotEqual(assignments[0], assignments[1])
        self.assertNotEqual(assignments[1], assignments[2])

    def test_bridge_category_predicts_conjunction(self) -> None:
        train, environments = bridge_episodes()
        space = FeatureSpace(train)
        model = PredictiveVigilanceLearner(0.7).fit(
            [space.transform(item) for item in train],
            [item.outcome for item in train],
        )
        candidates = environments[0]
        predictions = [model.predict(space.transform(item)) for item in candidates]
        self.assertEqual(predictions[2], "reach_success")
        self.assertEqual(candidates[2].outcome, "reach_success")


if __name__ == "__main__":
    unittest.main()
