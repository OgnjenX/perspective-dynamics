# Method

Episodes deliberately include objects sharing salient physical features but
having different action outcomes. The SOM is trained without outcome labels and
then receives majority outcome labels. The predictive learner chooses categories
by feature match; outcome mismatch triggers reset and search for or creation of
a more specific category.

Both receive the same training vectors and held-out identities. Random
categories use 200 frozen seeds. Report accuracy, category count, reset count,
and prototype/category audit logs.
