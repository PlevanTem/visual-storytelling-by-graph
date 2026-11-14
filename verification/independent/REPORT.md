# Independent specialist forward test

Completed C15, C17, C19 and C23 from raw fixtures. Seven SVG states and an interactive HTML artifact were produced independently. Data and SVG encoding checks pass (114 assertions); Chromium checks pass (11 checks). This is evidence of executing these four supplied synthetic tasks, not evidence of reader understanding, aesthetic effectiveness, arbitrary-data generality or production readiness.

## Source files actually read

All below are relative to `outputs/visual-storytelling-by-graph/`:

- `SKILL.md`
- `references/specialized-methods.md`
- `references/implementation-and-validation.md`
- `evals/requests/C15.md`
- `evals/requests/C17.md`
- `evals/requests/C19.md`
- `evals/requests/C23.md`
- `evals/fixtures/survival.json`
- `evals/fixtures/intersections.json`
- `evals/fixtures/recurrence.json`
- `evals/fixtures/swarm.json`

No answer key, `examples/`, `docs/`, `verification/`, parent rendering/validation implementation, bootstrap code, GitHub or other agents were accessed. Package files were not modified. No expected numerical answers were supplied.

## Independently computed outcomes and design choices

| Case | Selected expression and reason | Results |
|---|---|---|
| C15 | Kaplan-Meier step curves, censor marks and common-time at-risk table preserve event/censor semantics. | Dry: 12 samples, 4 events, 8 censored, last observation 100 cycles, median not reached. Humid: 12 samples, 7 events, 5 censored, last observation 88 cycles, median 56. Dry final estimate 0.5775; Humid final estimate 0.3. |
| C17 | Exact-intersection bars and membership matrix permit exact counts without four-set Venn geometry. Toggle filters full objects by number of labels. | All tagged: 64 objects, 15 patterns. At least two tags: 42 objects, 11 patterns. Each observed exact pattern is retained in its selected state. |
| C19 | Time-index by time-index recurrence matrix with three fixed thresholds, same axes and units. | n=64. At epsilon 0.1: 422/4032=10.4663%; 0.25: 986/4032=24.4544%; 0.45: 1744/4032=43.2540%. Diagonal remains visible but is excluded from rate. |
| C23 | Exact-x swarm preserves every raw sample and duplicate; only y is displaced. | All means=15 min, n=12 each. Medians Compact/Split/Tail=15/15/8. Ranges=13–17, 0–30, 8–92. Split: six zeros and six thirties. Tail: eleven eights and one 92. |

KM risk sets include all rows with `time >= t`; tied Humid event/censor at 24 uses the same pre-removal risk set. Exact rational products are retained in `results.json`. An independent life-table decrement cross-check matches those risk sets. No confidence interval or significance test was computed. Non-informative, independent censoring is assumed, as stated by the synthetic fixture; it is not established by these data.

Recurrence uses exact decimal arithmetic on the supplied scalar amplitudes. Sampling interval is absent, so axes are sample indices, not physical time. Embedding dimension is 1. Recurrence does not identify chaos or a hidden mechanism.

The observed waiting-time distributions describe a plausible distinction in experience; these data do not identify the cause of complaints. Vertical offsets in the swarm encode no variable.

## Exact executed checks

From the workspace root:

```powershell
python -c "import importlib.util; print('playwright',bool(importlib.util.find_spec('playwright')))"
python work/specialist-forward-test/run_forward_test.py
python work/specialist-forward-test/browser_check.py
```

The first browser execution in the sandbox failed with `PermissionError: [WinError 5]` while creating Playwright's subprocess pipe. A scoped approved escalation reran the same local browser script successfully; no package or dependency installation was required. After self-generated SVG styling/layering corrections, data checks and browser checks were rerun on the final files.

Data/SVG assertions in `results.json` check: unique object IDs; defined universe; membership conservation; each bar height and baseline; included/excluded dot fill; KM event-only step drops, group endpoints, survival y coordinates, censor multiplicity and risk-set bookkeeping; recurrence rule equivalence for every cell, actual coordinates, symmetry, diagonal, monotonic thresholds and unordered-pair count cross-check; every swarm observation's exact x and pairwise non-collision. Assertions parse actual SVG marks, not just labels or the presence of result numbers.

Chromium browser checks in `browser-results.json` cover: C17 default, filtered and reset summaries; all C19 threshold summaries; Enter-key reset; all seven state SVG text bounding boxes inside native viewBoxes; 390px document overflow and filter operation; absence of JS errors. Rendering sizes: desktop 1200×900, narrow 390×844, device scale factor 1. Screenshots were saved, and the four desktop chart screenshots were visually inspected by the agent. The first render exposed weak censor marks and grid lines over swarm dots in this independent implementation; these were corrected and visually rechecked. No such defect is attributed to the Skill instructions.

## Material defects and limits

No material instruction defect was found in the read Skill sections for these four supplied requests. This is a narrow positive result. No human reader study was run. Aesthetic effectiveness was not tested. Narrow viewport checks establish operation and absence of horizontal page overflow, not readable small text or touch-device usability; the graphics retain their desktop proportions. Missing-data, empty-data, large-volume, accessibility audit and arbitrary new-fixture behavior were not tested. No actual survival inference or service policy recommendation should be inferred from the synthetic outputs.

## Artifacts

- `index.html` — self-contained interactive four-case page; native buttons and reset; all states available in no-JS fallback.
- `C15-kaplan-meier.svg`
- `C17-exact-1.svg`, `C17-exact-2.svg`
- `C19-recurrence-0.1.svg`, `C19-recurrence-0.25.svg`, `C19-recurrence-0.45.svg`
- `C23-exact-x-swarm.svg`
- `results.json`, `browser-results.json`
- `run_forward_test.py`, `browser_check.py`
- `desktop.png`, `narrow.png`, `C15-desktop.png`, `C17-desktop.png`, `C19-desktop.png`, `C23-desktop.png`

Progression: read permitted instructions and inputs → compute independent results → create marks → parse/check actual encodings → render and exercise controls → fix independent implementation issues → rerun affected checks → preserve scoped evidence.
