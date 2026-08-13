# Repository Guidelines

## Project Structure & Module Organization

This repository combines research documentation with small, controlled computational experiments. `docs/` contains the scientific question, working theory, falsifiable hypotheses, roadmap, literature map, decision record, and chronological log. `src/perspective_dynamics/` contains reusable model and task code. Every versioned experiment under `experiments/` owns its prospective hypothesis, method, parameters, entry points, generated outputs, and conclusion. `papers/` holds the bibliography and source notes.

Keep claims at the correct evidence level. Distinguish cited findings, project interpretations, modeling assumptions, and speculation. A conceptual equation is not a result.

## Documentation Conventions

Use Markdown with descriptive headings, short paragraphs, and renderer-compatible Unicode or fenced-text equations. Define new technical terms on first use. Cite factual scientific claims inline and add complete source metadata to `papers/bibliography.bib`. Verify bibliographic metadata against publisher records before manuscript use.

Record each consequential change in `docs/decisions.md`; append rather than silently rewriting history. Add dated entries to `docs/research_log.md` for completed work, failed approaches, deviations, and next steps.

## Build, Test, and Experiment Commands

- `make test`: run the standard-library unit tests.
- `make baseline`: generate EXP001 raw results.
- `make analyze`: aggregate EXP001 conditions.
- `make exp002`: generate EXP002 matched-perspective results.
- `make analyze-exp002`: aggregate EXP002 and its paired comparison.
- `make exp003`: generate EXP003 adaptive-switching results.
- `make analyze-exp003`: aggregate EXP003 and verify matched schedules.
- `make reproduce`: run tests, generation, and analysis in sequence.

Python 3.11 or later is required; the baseline has no third-party runtime dependency. Use four-space indentation, type hints, immutable dataclasses for configurations/results, and deterministic node ordering.

## Experimental Record

Every experiment must identify the hypothesis, controls, method, environment, parameters, seeds, exact run instructions, raw outputs, analysis, conclusion, and commit. Preserve negative results. Separate prospective/confirmatory analyses from exploratory work.

## Commit & Review Guidelines

The repository begins with `Initialize perspective dynamics research project`; no broader history exists yet from which to infer a convention. Use concise, imperative commit subjects and keep each commit limited to one scientific or structural change. Pull requests should state which hypothesis or decision they affect, list evidence and assumptions, identify changed claims, and include reproducibility information when code or results are eventually introduced.
