# Method

The world contains two boxes, a board, a rope, and a high target. The support perspective assembles an elevated platform. The stability perspective secures that platform. The goal perspective reaches the target only after stability is present.

The engine uses immutable facts, explicit variable binding, breadth-first forward chaining, and deterministic ordering. Controls use the same world and schemas. `single` restricts access to support; `pool` exposes all schemas but does not feed newly produced effects into later prerequisites.

Primary outcome is success/failure. Audit fields are explored-state count, schema order, perspective sequence, produced facts, and enabling facts.
