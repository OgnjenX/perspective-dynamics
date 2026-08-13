# Method

Each task has support, stability, goal, and integration schemas. Support and
stability produce perspective-namespaced relations independently. The
integration rule consumes both and produces a new `integrated` relation; the
goal schema consumes only that relation.

Controls remove one perspective, remove the integration rule while retaining
the static schema union, permute schema ordering exhaustively, and erase
perspective labels for an ordinary forward planner. Initial facts, operators,
goals, and search budgets are matched wherever the comparison permits.

A matched-capacity sham replaces the valid integration rule with a rule having
the same prerequisites and one effect, but its effect is irrelevant to the goal.
This control has the same schema count and an additional applicable transition.

The complete successful sequence is never stored as one schema or training
trajectory. The integration rule itself is explicit and hand-designed; EXP010
does not test discovery or learning of that rule.
