# Feature: presentation-builder

## What

Generates customized PowerPoint presentation decks (`.pptx`) for graduate school portfolio reviews and engineering presentations from project metrics and case summaries.

## Entry points

- `python3 renew_grad_ppt.py` — Generates renewed graduate portfolio PPTX
- `python3 generate_ppt.py` — Generates standard presentation deck
- `python3 inspect_ppt.py` — Inspects shape and layout geometry of PPTX slides

## Contract

- Inputs: Case study markdown data, layout configurations
- Outputs: PPTX files (`대학원_포트폴리오_황인혁_리뉴얼.pptx`, `대학원_포트폴리오_황인혁.pptx`)
- Gate: Valid python-pptx generation with zero runtime exceptions

## Data and state

- Repository data: `cases/`, `diagrams/`, `참조자료/`, root PPTX files
- External state: None (fully offline)
- Secrets: None

## Tests

- Execution smoke check via python-pptx

## Status

live; ad-hoc presentation generator.
