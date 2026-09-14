# dr-v1 — 10-task smoke (L1, full row, Gemini judge, 2026-09-13)

First 10 tasks of the official `tasks_and_rubrics.jsonl`, production core, Gemini 3.1 Pro generation, Gemini 3.8 Flash rubric judge (PASS/FAIL, exact-number rule). **Smoke, not a result** — 10 of 132 tasks, internal judge; two tasks cited a blocked source via the Crossref path (fixed after this run).

| task | lang | rubrics | passed | overall | recall | analysis | presentation | blocked | cite-match | s | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| task7 | zh | 58 | 11 | 0.19 | 0.3077 | 0.0769 | 0.1667 | 0 | 0.6 | 606 | 0.40 |
| task1+ | en | 109 | 4 | 0.04 | 0.023 | 0.0 | 0.4 | 0 | 1.0 | 531 | 0.27 |
| task51 | zh | 83 | 2 | 0.02 | 0.0 | 0.0 | 0.3333 | 0 | 0.55 | 1047 | 0.33 |
| task2+ | en | 72 | 2 | 0.03 | 0.0 | 0.0 | 0.25 | 0 | — | 524 | 0.35 |
| task52 | zh | 48 | 10 | 0.21 | 0.0 | 0.35 | 0.6 | 1 | — | 568 | 0.27 |
| task3+ | en | 86 | 4 | 0.05 | 0.0469 | 0.0 | 0.1111 | 0 | — | 503 | 0.38 |
| task53 | zh | 75 | 18 | 0.24 | 0.2833 | 0.0 | 0.2 | 0 | 1.0 | 921 | 0.53 |
| task4 | en | 72 | 1 | 0.01 | 0.0 | 0.0 | 0.1667 | 0 | 0.6667 | 1263 | 0.98 |
| task4+ | zh | 63 | 15 | 0.24 | 0.1538 | 0.2195 | 0.4444 | 2 | — | 561 | 0.42 |
| task54 | en | 67 | 3 | 0.04 | 0.0 | 0.0588 | 0.3333 | 0 | — | 590 | 0.21 |
| **mean** | | | | **0.107** | 0.081 | 0.071 | 0.301 | 2task | 0.763 | 711 | 0.41 |

## Official judge (GPT-5.5, `run_evaluation.py`) on the same 10 reports — 2026-09-14

| idx | task | official total (recall · analysis · presentation) | internal Gemini total |
|---|---|---|---|
| 1 | task7 | 0.21 (8/26 · 3/26 · 1/6) | 0.19 |
| 2 | task1+ | 0.06 (4/87 · 0/17 · 2/5) | 0.04 |
| 3 | task51 | 0.05 (1/69 · 0/8 · 3/6) | 0.02 |
| 4 | task2+ | 0.03 (0/53 · 0/11 · 2/8) | 0.03 |
| 5 | task52 | 0.21 (0/23 · 6/20 · 4/5) | 0.21 |
| 6 | task3+ | 0.06 (5/64 · 0/13 · 0/9) | 0.05 |
| 7 | task53 | 0.33 (23/60 · 0/10 · 2/5) | 0.24 |
| 8 | task4 | 0.00 (0/55 · 0/11 · 0/6) | 0.01 |
| 9 | task4+ | 0.35 (2/13 · 13/41 · 7/9) | 0.24 |
| 10 | task54 | 0.07 (2/44 · 2/17 · 1/6) | 0.04 |
| **mean** | | **0.136** (recall 0.103 · analysis 0.085 · presentation 0.346) | **0.107** |

Per-task Pearson r = **0.97**; the internal judge is a conservative proxy (−3 pp on average). The official judge flagged 4 rubric items
as −1 (blocked-source citation) in the two tasks where the Crossref path leaked the expert article. Files:
`official-gpt55.jsonl` (raw), `official-gpt55-vs-internal.json`.
