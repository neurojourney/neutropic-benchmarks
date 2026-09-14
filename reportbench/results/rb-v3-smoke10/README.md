# rb-v3 — 10-task smoke, "true full" preset (WS0 measurement fix; L1, 2026-09-14)

Same first 10 tasks as `rb-v1-smoke10` / `rb-v2-smoke10`, production core, Gemini. Changes vs v2 (from
`docs/benchmark-improvement-plan.md` WS0): the `full` preset is now the product's **Deep** effort (deep second research
pass, reviewer forced, 48 steps) and the runner actually passes a review provider — v1/v2 rows never ran the reviewer.
Also: the eval token is refreshed in place by a background thread every 20 min (tasks now take 20–100 min), and the
runner appends each row as it finishes. **Smoke, not a result** — 10 of 100 tasks, internal (L1) judge.

All 10 tasks scored (v2: 8). Mean P 0.182 / R 0.033 / F1 0.055; cite-match 0.78, cited-statement accuracy 0.89.
v2 on its 8 scored tasks: P 0.155 / R 0.026 / F1 0.042, cite-match 0.60, accuracy 0.80. Total $2.69 (v2 $3.56),
mean 49 min per task (v2 21 min).

| task | prompt cutoff | refs | matched/gold | P | R | F1 | cite-match | cited acc | s | $ | v2 P / R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2312.04861 | April 2025 | 30 | 14/277 | 0.467 | 0.054 | 0.097 | 0.55 | 0.775 | 1636 | 0.47 | 0.231 / 0.022 |
| 2308.06419 | — | 20 | 6/106 | 0.300 | 0.057 | 0.095 | 0.65 | 0.825 | 1623 | 0.21 | 0.056 / 0.009 |
| 2308.15985 | August 2023 | 10 | 2/155 | 0.200 | 0.013 | 0.024 | 0.75 | 0.875 | 2536 | 0.20 | 0.333 / 0.045 |
| 2402.10079 | March 2025 | 26 | 3/148 | 0.115 | 0.020 | 0.035 | 0.70 | 0.850 | 1206 | 0.25 | 0.222 / 0.020 |
| 2108.09522 | August 2021 | 15 | 10/47 | 0.667 | 0.170 | 0.271 | 0.67 | 0.833 | 3482 | 0.24 | failed |
| 2108.09091 | August 2021 | 12 | 0/83 | 0.000 | 0.000 | 0.000 | 0.90 | 0.950 | 3871 | 0.26 | 0.059 / 0.036 |
| 2006.00648 | November 2020 | 8 | 0/60 | 0.000 | 0.000 | 0.000 | 0.75 | 0.875 | 1969 | 0.40 | 0.200 / 0.017 |
| 2204.07974 | April 2022 | 27 | 2/104 | 0.074 | 0.019 | 0.030 | 1.00 | 1.000 | 5997 | 0.24 | failed |
| 2302.10588 | — | 6 | 0/65 | 0.000 | 0.000 | 0.000 | 0.80 | 0.900 | 3192 | 0.17 | 0.100 / 0.046 |
| 2408.14199 | November 2024 | 5 | 0/64 | 0.000 | 0.000 | 0.000 | 1.00 | 1.000 | 3982 | 0.24 | 0.040 / 0.016 |
| **mean (10 scored)** | | 15.9 | | **0.182** | **0.033** | 0.055 | 0.78 | 0.888 | 2949 | 0.27 | 0.155 / 0.026 (8) |
## What moved

- **Precision and citation faithfulness rose across the board** (P 0.155 → 0.182, cite-match 0.60 → 0.78, cited-statement
  accuracy 0.80 → 0.89): the reviewer + deep pass prune weakly supported statements and unused sources. The reference list
  now contains only sources actually cited (15.9 per report vs 22.1), which is also why recall barely moved.
- **Best task ever**: 2108.09522 (spatio-temporal traffic, 47 gold refs) P 0.667 / R 0.170 — every one of its 15
  references predates the prompt's cutoff (August 2021).
- **Four tasks scored zero** (2108.09091, 2006.00648, 2302.10588, 2408.14199). Root causes, from the reports:
  1. **The prompt's date constraint is ignored.** 8 of 10 prompts say "all referenced papers must have been published
     before <month year>"; 41 of the 172 cited references (24 %) are newer than that — 9/12 on 2108.09091, 25/37 on
     2204.07974, 5/13 on 2308.15985. Those are exactly the worst-scoring tasks. The retrieval stack ranks by relevance /
     recency with no year filter, and nothing drops newer sources at citation time.
  2. **Off-topic and tooling references** survive into the bibliography (EEG emotion recognition and MOOC-dropout papers in a
     traffic-forecasting survey; NumPy and the PRISMA statement in a LiDAR-localization survey).
  3. **Too few citations** on some tasks (5–8 references against 60–65 gold) — the deep pass trims rather than widens.
- **Time doubled for a small gain**: the deep pass + reviewer take tasks from 21 to 49 min (one task 100 min). At 100 tasks
  that is ~80 h per run — the 10-minute task budget (WS4) and a wider reference budget with citation snowballing (WS1)
  are the next levers, together with enforcing the prompt's date window (new WS1 item).

Files: `full.summary.json` (runner summary). Per-task rows with trajectories stay in the API repo's `benchmark_runs/`
(not published).
