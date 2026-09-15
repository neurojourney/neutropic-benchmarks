# dr-v7 — 10-task smoke (L1 + official judge, full row, 2026-09-16)

Same first 10 tasks as `dr-v1`, production core (`full` = product Deep) with everything landed since dr-v1: WS0 measurement fixes, WS4 request gates + 900 s research budget, WS1 date window / snowballing, WS2 fact ledger (planner `required_facts` → deterministic ledger matching → **fact hunt** after the ReAct loop), request-structure composer (parts / numbered items / tables as `###` sub-headings, brief as a citable source, empty sub-items filled), and — new in v7 — **fact hunt routed by fact kind through open/official data APIs** (Wikipedia in the request language then English, World Bank indicators for numeric facts with an identifiable country, DuckDuckGo only as the last fallback; no commercial search API). Internal Gemini judge on the run, then the same 10 reports re-scored by the **official GPT-5.5 judge** (`run_evaluation.py`). **Smoke, not a result** — 10 of 132 tasks.

| task | lang | rubrics | passed | internal overall | recall | analysis | presentation | official overall (recall · analysis · presentation) | cite-match | s | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| task7 | zh | 58 | 13 | 0.22 | 0.115 | 0.192 | 0.833 | **0.29** (7/26 · 5/26 · 5/6) | 0.86 | 2035 | 0.16 |
| task1+ | en | 109 | 10 | 0.09 | 0.069 | 0.059 | 0.600 | **0.11** (7/87 · 2/17 · 3/5) | 0.83 | 2046 | 0.22 |
| task51 | zh | 83 | 10 | 0.12 | 0.058 | 0.125 | 0.833 | **0.16** (6/69 · 1/8 · 6/6) | 0.65 | 1829 | 0.85 |
| task2+ | en | 72 | 4 | 0.06 | 0.038 | 0.000 | 0.250 | **0.07** (3/53 · 1/11 · 1/8) | 1.00 | 2206 | 0.16 |
| task52 | zh | 48 | 11 | 0.23 | 0.000 | 0.300 | 1.000 | **0.23** (0/23 · 7/20 · 4/5) | 0.55 | 1245 | 0.88 |
| task3+ | en | 86 | 12 | 0.14 | 0.109 | 0.154 | 0.333 | **0.24** (14/64 · 2/13 · 5/9) | 0.90 | 2259 | 0.21 |
| task53 | zh | 75 | 15 | 0.20 | 0.217 | 0.000 | 0.400 | **0.25** (17/60 · 0/10 · 2/5) | 0.85 | 1343 | 0.15 |
| task4 | en | 72 | 20 | 0.28 | 0.182 | 0.364 | 1.000 | **0.12** (1/55 · 3/11 · 5/6) | 0.75 | 1586 | 0.11 |
| task4+ | zh | 63 | 19 | 0.30 | 0.923 | 0.049 | 0.556 | **0.37** (12/13 · 3/41 · 8/9) | 0.85 | 1915 | 0.19 |
| task54 | en | 67 | 19 | 0.28 | 0.341 | 0.000 | 0.667 | **0.37** (18/44 · 4/17 · 3/6) | 0.93 | 1803 | 0.19 |
| **mean** | | | | **0.192** | 0.205 | 0.124 | 0.647 | **0.222** (recall 0.235 · analysis 0.161 · presentation 0.654) | 0.82 | 1827 | 0.31 |

## Versus dr-v1 (same 10 tasks)

| judge | run | total | recall | analysis | presentation |
|---|---|---|---|---|---|
| internal Gemini | dr-v1 | 0.107 | 0.081 | 0.071 | 0.301 |
| internal Gemini | dr-v7 | **0.192** | 0.205 | 0.124 | 0.647 |
| official GPT-5.5 | dr-v1 | 0.136 | 0.103 | 0.085 | 0.346 |
| official GPT-5.5 | dr-v7 | **0.222** | 0.235 | 0.161 | 0.654 |

Official judge per-task Pearson r with the internal judge = **0.73** (dr-v1: 0.97); the internal judge stays conservative (−3 pp) except task4, where it over-credits (0.28 vs 0.13). Blocked-source −1 items: 2 (task4, a same-title safe-haven paper reached through a different DOI — the title filter did not catch it). Every task improved under the official judge except task52 (flat). Presentation is now 0.65; recall 0.24 and analysis 0.16 remain the gap to the leaderboard (0.60 / 0.71).

Intermediate runs (dr-v2 … dr-v6, internal judge only, 3–5 tasks each, not stored here) tracked each WS2 change: v2 0.104 (structure only) → v4 0.117 (brief as source) → v6 0.124 on the first 3 tasks → v7 0.145 on the same 3. Fact hunt in v7: 61 of 100 ledger items found (Wikipedia zh 54 / en 127 requests, World Bank 10, no 429s); the gold-specific figures that only appear in ministry press releases are still missed by the DuckDuckGo fallback. Semantic Scholar tripped its circuit breaker (69 × 429, 32 skipped requests) despite the 1.2 s gate.

Files: `full.summary.json` (internal run summary incl. per-host request stats), `official-gpt55.jsonl` (raw official verdicts with reasons), `official-gpt55-vs-internal.json`.
