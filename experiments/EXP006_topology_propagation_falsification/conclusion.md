# EXP006 Conclusion

## Status

Completed on 2026-08-13: 50,400 runs across 150 unseen seeds, four topology × propagation environments, 12 block lengths, and seven evaluation thresholds. Twenty-two unit tests passed. The EXP005 regression outputs remained byte-identical after the propagation implementation was generalized.

## Frozen result

The positive control and all three novel environments passed every preregistered criterion.

| Topology | Propagation | ρ | Reversals | Distinct optima | Interior optima | Pass |
|---|---|---:|---:|---:|---:|---:|
| Path | Source-normalized | 0.99103121 | 0 | 6 | 7 | Yes |
| Path | Symmetric-normalized | 0.98198051 | 0 | 5 | 7 | Yes |
| Branched path | Source-normalized | 0.98198051 | 0 | 5 | 7 | Yes |
| Branched path | Symmetric-normalized | 0.99103121 | 0 | 6 | 7 | Yes |

The conjunction across all three novel environments passed. Graph integrity checks passed for every seed: node sets, edge counts, total weights, and requested cue-to-goal distances matched across frames within each environment.

## Selected optima

- path, source-normalized: `2, 3, 3, 4, 5, 7, 10`;
- path, symmetric-normalized: `3, 3, 4, 5, 7, 7, 10`;
- branched path, source-normalized: `3, 4, 4, 7, 7, 10, 15`;
- branched path, symmetric-normalized: `3, 4, 5, 7, 10, 10, 15`.

The branched environments shifted productive dwell later, consistent with slower evidence propagation under added local competition. This comparison is mechanistically interpretable but was not a separately preregistered directional hypothesis.

## Ceiling and floor check

Mean success across the full grids ranged from 0.9779 to 0.9881. The primary outcome was continuous peak activation rather than success, and every environment selected multiple interior optima. The trend therefore did not arise from constant boundary choices, although the high aggregate success rate limits conclusions about binary task completion.

## Conclusion

F001 survived the first aggressive structural falsification attempt. Within this model family, evidence demand calibrated productive perspective dwell across both a simple and distractor-branched topology and across two normalization rules.

This narrows one artifact explanation: the registered relation is not specific to an unbranched path or to source-only normalization. It does not remove the more important concern that the controller uses an external block clock and directly evaluates goal activation.

## Remaining alternatives

- the relation may be intrinsic to any blockwise threshold controller rather than perspective dynamics;
- goal-node activation provides supervised, solution-proximal feedback;
- frames and their useful relation remain engineered;
- the dynamics remain deterministic and linear except for rectification and inhibition;
- all tested graphs share a path backbone;
- high binary success may conceal task difficulty limitations.

## Next test

Replace imposed decision blocks with a self-timed mismatch/adaptation controller. The next critical question is whether evidence-dependent dwell emerges from local state variables rather than being selected from an externally imposed clock grid.

## Provenance

- prospective design commit: `3752fa7`;
- implementation commit: `5dc2de4`;
- Python 3.11 standard-library runtime;
- exact parameters and raw outputs are stored in this experiment folder.
