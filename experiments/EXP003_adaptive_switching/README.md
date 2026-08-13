# EXP003 — Adaptive Perspective Switching

## Position in the research program

EXP002 showed that matched relational frames can make the same goal accessible or inaccessible. EXP003 asks the next, stronger question: can a controller that responds to task mismatch find and retain a useful frame better than non-adaptive switching?

This experiment tests switching policy. It still uses synthetic frames and a rate-like spreading-activation model; metastability and biological grounding remain later phases.

## Primary comparison

`adaptive_mismatch` is compared with `random_replay`. For every seed, random replay receives the adaptive run’s exact segment lengths, switch times, and switch count, but frame identities are reassigned without using evaluation. This prevents an adaptive advantage from being attributed merely to fewer switches or longer dwell.

## Additional controls

- fixed initial and fixed useful oracle bounds;
- equal static matrix blend;
- periodic switching at the same base block length;
- random block switching with no immediate frame repetition.

## Reproduce

```text
make exp003
make analyze-exp003
```

The hypothesis, method, parameters, and interpretation boundaries were frozen before implementation and results.
