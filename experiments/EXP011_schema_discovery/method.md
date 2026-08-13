# Method

Episodes contain an audit-only object identity, binary relational/property
features, an action, and an outcome. Train and test identities are disjoint.
The vectorizer excludes identity and includes property/action indicators.

Competitive learning and a 1-D SOM receive the same vectors, category count,
initialization seed, epochs, and learning-rate schedule. Category outcomes are
assigned only after unsupervised training by majority association on training
episodes. Random clustering uses the same category count over 200 frozen seeds.

Purity and held-out outcome accuracy are primary. Prototype vectors, category
assignments, and predictions are logged.
