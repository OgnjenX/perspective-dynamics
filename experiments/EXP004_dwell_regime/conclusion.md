# EXP004 Conclusion

## Status

First validated sweep completed on 2026-08-13: 2,700 runs spanning nine decision intervals, three evaluation thresholds, and 100 seeds. Fourteen unit tests passed.

## Primary result

All eight frozen inequalities passed: intermediate mean activation (blocks 10, 15, and 20) exceeded both block 1 and block 60 at every threshold and in pooled data.

| Evaluation threshold | Intermediate mean | Block 1 | Block 60 | Intermediate − rapid | Intermediate − persistent |
|---:|---:|---:|---:|---:|---:|
| 0.001 | 1.02367781 | 0.95818476 | 0.53786744 | 0.06549305 | 0.48581037 |
| 0.005 | 1.04437789 | 0.96407709 | 0.53752291 | 0.08030080 | 0.50685498 |
| 0.020 | 1.06354795 | 0.90920775 | 0.59011211 | 0.15434020 | 0.47343584 |
| pooled | 1.04386788 | 0.94382320 | 0.55516749 | 0.10004469 | 0.48870040 |

Rapid switching still succeeded because state persisted and repeated visits accumulated signal, but it required many more switches and produced weaker peak activation. Excessive persistence delayed useful-frame entry and reduced success to 87–91% at block 60.

## Exploratory threshold–timescale pattern

The cell maxima were not part of the frozen contrast. After inspecting the complete table, the best block length increased with evidence threshold:

- threshold 0.001: block 3, mean peak 1.14200558;
- threshold 0.005: block 5, mean peak 1.13661399;
- threshold 0.020: block 10, mean peak 1.11361258.

This suggests the productive dwell interval may be set by the time required for a perspective to accumulate enough evidence to pass evaluation: stricter evidence criteria favor longer dwell. This pattern is mechanistically plausible but post-result and evaluated on the same grid that revealed it. It requires prospective replication on held-out seeds and a denser grid.

## Interpretation

EXP004 supports a non-monotonic dwell-time tradeoff in the controlled switching model. It is more informative than a single tuned block length, but it is not yet emergent metastability: block boundaries remain externally imposed, the evaluation signal is supervised, and the task frames are synthetic.

## Next decision

Run a held-out, prospectively specified evidence-timescale scaling experiment. If increasing evaluation thresholds reliably shift the optimal dwell later, use that relation to design a continuous self-timed controller whose dwell emerges from evidence, adaptation, and mismatch rather than from an external clock.
