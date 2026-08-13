# Method

Training episodes describe candidate structures with primitive evidence such
as `elevated`, `stable`, `rigid`, and irrelevant surface features, plus whether
the candidate enabled a reach trajectory. Positive and negative examples vary
each primitive independently. No bridge feature or rule is present.

At test, each unseen environment offers candidate action sequences producing
different primitive evidence combinations. Methods select a candidate using:

- hand-written `elevated AND stable` oracle;
- exact-memory ordinary planner over object-specific observed transitions;
- random categories;
- SOM categories labeled after unsupervised training;
- predictive vigilance categories.

All methods receive the same episodes and candidates except that the oracle is
explicitly privileged as a reference. The learned explanation is the
intersection of active primitive features among training members of the
selected positive predictive category. Removal and identity-scrambling tests
are performed after model fitting.
