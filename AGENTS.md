# Repository Guidelines

## Project Structure & Module Organization

This repository is currently a documentation-first research project. `docs/` contains the scientific question, working theory, falsifiable hypotheses, experimental roadmap, literature map, decision record, and chronological research log. `papers/` holds the bibliography and future source notes. `models/`, `experiments/`, `analysis/`, and `results/` are intentionally empty except for scope READMEs; do not add implementation until the Week 1 framing has been reviewed.

Keep claims at the correct evidence level. Distinguish cited findings, project interpretations, modeling assumptions, and speculation. A conceptual equation is not a result.

## Documentation Conventions

Use Markdown with descriptive headings, short paragraphs, and LaTeX equations. Define new technical terms on first use. Cite factual scientific claims inline and add complete source metadata to `papers/bibliography.bib`. Verify bibliographic metadata against publisher records before manuscript use.

Record each consequential change in `docs/decisions.md`; append rather than silently rewriting history. Add dated entries to `docs/research_log.md` for completed work, failed approaches, deviations, and next steps.

## Experimental Record

Once implementation is approved, give every experiment its own folder under `experiments/`. It must identify the hypothesis, controls, method, environment, parameters, seeds, exact run instructions, raw outputs, analysis, conclusion, and commit. Preserve negative results. Separate preregistered/confirmatory analyses from exploratory work.

## Commit & Review Guidelines

The repository begins with `Initialize perspective dynamics research project`; no broader history exists yet from which to infer a convention. Use concise, imperative commit subjects and keep each commit limited to one scientific or structural change. Pull requests should state which hypothesis or decision they affect, list evidence and assumptions, identify changed claims, and include reproducibility information when code or results are eventually introduced.
