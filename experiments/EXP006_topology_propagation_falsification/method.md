# EXP006 Method

## Frozen factorial design

Cross two graph topologies with two propagation rules:

| Factor | Levels |
|---|---|
| Topology | `path`, `branched_path` |
| Propagation | `source_normalized`, `symmetric_normalized` |

The path condition reuses the matched frames from EXP005. The branched condition attaches one leaf to every shared core node in every frame. It therefore adds local competition without changing core content, core frame distance, branch count per core item, or total branch-weight distribution across frames.

Source normalization divides each outgoing contribution by the source’s total outgoing weight. Symmetric normalization scales an edge by the geometric mean of source and target weighted degree:

```text
message(i → j) = xᵢ wᵢⱼ / sqrt(sᵢ sⱼ)
```

where `sᵢ` and `sⱼ` are weighted degrees. All other dynamics remain unchanged.

## Frozen grid

- blocks: 1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 40, 60;
- thresholds: 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.04;
- unseen seeds: 2,000–2,149;
- topology × propagation environments: 4;
- total scheduled runs: 50,400.

Controller randomization remains threshold-specific and deterministic. Each environment receives the same seed set. The controller logic, frame distances, primary outcome, shorter-block tie rule, and 120-step budget remain fixed from EXP005.

## Analysis

Within each environment, calculate mean peak goal activation for every threshold × block cell. Select the maximizing block at each threshold, choosing the shorter block on exact ties. Compute average-rank Spearman correlation, adjacent reversals, the number of distinct optima, and the number of interior optima.

Report each criterion separately for each environment and the conjunction across the three novel environments. Also report success rate, peak activation, useful-frame dwell, and switch count for ceiling/floor diagnosis; these do not replace the frozen outcome or criteria.

## Integrity checks

- identical core nodes and frame-distance targets across environments;
- one branch per core node only in `branched_path`;
- matched frame node sets, edge counts, and total weights within each topology/seed;
- deterministic results for repeated seed/configuration;
- the existing source-normalized rule remains numerically unchanged.
