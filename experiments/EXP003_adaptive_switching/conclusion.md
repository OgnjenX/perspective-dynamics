# EXP003 Conclusion

## Status

First validated run completed on 2026-08-13: 700 policy runs across 100 matched task seeds. Fourteen unit tests passed.

## Control integrity

Adaptive and random-replay schedules had exactly identical switch times and switch counts in all 100 pairs. Mean switch count was 1.47 in both conditions. The primary comparison therefore does not reduce to adaptive switching less often or receiving more total compute.

## Primary result

The prospective hypothesis was supported in this synthetic task.

- Adaptive switching succeeded in 100% of seeds; schedule-matched random replay succeeded in 76%.
- Mean peak goal activation was 1.06447822 for adaptive switching and 0.49673638 for replay.
- The paired adaptive-minus-replay difference had mean 0.56774184 and median 0.71042316: 64 positive, 32 exactly zero, and 4 negative pairs.
- Adaptive schedules spent 88.8 of 120 steps in the useful frame on average, versus 37.95 for replay, a mean difference of 50.85 steps.
- In all 64 nonzero pairs where adaptive activation was greater, adaptive useful-frame dwell was also greater.

The zero and negative cases are informative. Replay sometimes assigned the useful frame to the same long segment as adaptation, producing equality, and occasionally received a more favorable early assignment. Adaptation improved expected performance rather than dominating every realized schedule.

## Secondary controls

Fixed useful remained the oracle upper bound at mean peak activation 1.14837739. Periodic and random-block switching both succeeded in all seeds but reached only approximately half the oracle activation because continual switching prevented sustained useful-frame elaboration. The static equal blend reached 0.41641021, consistent with EXP002’s interference observation.

## Conclusion

Given a scalar task-validity signal, coupling mismatch to exploration and progress to dwell improved search over random frame identity under exactly matched switch timing and count. The advantage arose through selective allocation of dwell time to the useful relational frame.

This is stronger than showing that the useful frame works, but it remains an expected control result rather than a novel theory. The controller uses goal activation as supervised evaluation, frames are engineered, and the model has no learned semantic world or biologically grounded switching circuit.

## Next decision

Proceed to a prospectively specified regime sweep. The central dynamical prediction is that evaluation requires sufficient within-frame dwell, while excessive dwell delays escape from unproductive frames. Demonstrating a robust intermediate optimum—rather than tuning one 15-step block—would provide the first substantive metastability result.
