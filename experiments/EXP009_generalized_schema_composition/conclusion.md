# Conclusion

EXP009 passed the frozen robust-generalization conjunction H9.1–H9.4. Structured
composition solved all six original/scrambled tasks. Every single-perspective
and no-chaining pool condition failed. Object-name scrambling preserved the
schema/perspective sequence. Structured success was 1.0 versus 0.633333 for
matched-budget random schema selection, a difference of 0.366667.

H9.5 failed. Erasing all perspective labels and running an ordinary forward
planner with the same operators produced identical success, schema sequence,
and schema-check count on every task. EXP009 therefore supports supervised
relational abstraction and transfer, but it provides no evidence that the
implemented computation differs from ordinary planning.

Role annotations were supplied, so the experiment does not demonstrate
unsupervised schema extraction or learning.
