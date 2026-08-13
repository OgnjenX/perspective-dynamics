# Integration: Level 1 definition

Integration is successful when representations selected from at least two perspectives jointly enable a goal-directed trajectory that no selected single perspective can produce under the same search limits and initial facts.

The minimal signature is:

1. perspective A produces an intermediate relation;
2. perspective B consumes that relation;
3. the final plan reaches the goal;
4. the corresponding single-perspective and no-composition controls fail.

This is stronger than switching, voting, or concatenating facts. The implementation records `perspective`, `enabled_by`, and `produced` for every plan step.
