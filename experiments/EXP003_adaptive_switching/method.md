# EXP003 Method

## Task family

Reuse EXP002’s matched ten-node frames and unchanged activation parameters. Useful, initial, and irrelevant frames place the goal two, six, and eight edges from the cue while matching individual-frame size and total weight.

## Blocked switching

Runs contain 120 Euler steps divided into 15-step decision blocks. State persists across frame changes; switching changes the active adjacency matrix but does not reset activation.

The adaptive controller starts in the initial frame. At each block boundary it examines the maximum goal activation during the completed block as a scalar task-validity signal:

- below 0.005: declare mismatch and try the next frame in a seed-shuffled exploration order;
- at or above 0.005: retain the current frame for the next block.

The signal is available only to the controller. It is never added to node activation. This operationalizes a system that can evaluate partial candidate validity but does not know in advance which named frame is useful.

## Matched random replay

After generating the adaptive schedule, record its contiguous segment lengths. Random replay uses those exact lengths and therefore the same switch times and count. It begins in the initial frame, while later segment identities are assigned by a separate seeded random process with no immediate repetition and no access to the evaluation signal.

## Other schedules

- `periodic`: cycle through a seed-shuffled frame order every 15 steps;
- `random_block`: choose a different random frame every 15 steps;
- static fixed-initial, fixed-useful, and equal-blend controls.

## Outcomes

- success, first passage, peak goal activation, and final goal rank;
- steps spent in each frame;
- switch count and ordered schedule segments;
- paired adaptive-minus-replay activation and useful-dwell differences;
- integrity equality of adaptive and replay switch count and switch times.

## Analysis

Aggregate 100 paired task seeds. The primary descriptive evidence is mean and median paired peak-activation difference plus positive/zero/negative counts. Report useful-dwell differences and whether switch schedules are exactly matched. Synthetic seeds are controlled replications, not a sampled biological population; inferential population claims are out of scope.
