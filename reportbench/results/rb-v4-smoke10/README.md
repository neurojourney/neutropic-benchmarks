# rb-v4 — 10-task smoke, WS4 execution budget (per-host request gate · 10-min task budget · no figures; L1, 2026-09-15)

Same first 10 tasks as `rb-v3-smoke10`, same `full` = product Deep preset, production core, Gemini. What changed
(`docs/benchmark-improvement-plan.md` WS4): every external-DB request now passes a per-host **request gate**
(pacing, concurrency, `Retry-After`, circuit breaker); each task has a **600 s research budget** after which search /
page / delegation tools are removed, the gap controller stops and the deep pass is skipped (report synthesis, review
and repair still run); report figures are off. **Smoke, not a result** — 10 of 100 tasks, internal (L1) judge.

**Environment caveat.** OpenAlex now bills per request and the key-less daily allowance was exhausted for the whole run
(every OpenAlex call → 429 `Insufficient budget`, `Retry-After` ≈ 9 h); arXiv answered `Rate exceeded` to single paced
requests from this IP. The gate turned both into ~0 s circuit skips instead of minutes of retries, so **these scores were
produced without OpenAlex and (mostly) without arXiv** — Semantic Scholar, Crossref, PubMed and Europe PMC only. Task 1
ran with the first gate build (OpenAlex still waited 285 s); tasks 2–10 with the final one.

Result: **time −52 % and cost −22 % at the same reference scores.** Mean P 0.169 / R 0.031 / F1 0.051 (rb-v3 on the
same tasks: 0.182 / 0.033 / 0.055 — within task-to-task noise); 24 min per task (rb-v3 49 min), longest 34 min (rb-v3 100 min);
$2.10 total (rb-v3 $2.69). Citation faithfulness dropped (cite-match 0.78 → 0.61, cited-statement accuracy 0.89 → 0.81):
the budget cuts the deep pass (full-text reading + claim extraction) on the longer tasks, which is where rb-v3 got it.

| task | refs | matched/gold | P | R | F1 | cite-match | cited acc | s | $ | OpenAlex · arXiv · S2 (req/429/skips) | rb-v3 P / R · s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2312.04861 | 35 | 10/277 | 0.286 | 0.036 | 0.064 | 0.55 | 0.775 | 1979 | 0.13 | 12/12/11 · 12/10/10 · 9/2 | 0.467 / 0.054 · 1636 |
| 2308.06419 | 27 | 6/106 | 0.222 | 0.057 | 0.090 | 0.50 | 0.750 | 830 | 0.28 | 1/1/4 · 6/3/9 · 0/0 | 0.300 / 0.057 · 1623 |
| 2308.15985 | 22 | 6/155 | 0.273 | 0.039 | 0.068 | 0.65 | 0.825 | 1084 | 0.22 | 0/0/13 · 3/2/10 · 12/3 | 0.200 / 0.013 · 2536 |
| 2402.10079 | 15 | 4/148 | 0.267 | 0.027 | 0.049 | 0.65 | 0.825 | 1729 | 0.18 | 1/1/17 · 6/6/17 · 15/2 | 0.115 / 0.020 · 1206 |
| 2108.09522 | 26 | 10/47 | 0.385 | 0.085 | 0.139 | 0.43 | 0.714 | 2059 | 0.22 | 1/1/36 · 3/3/29 · 34/9 | 0.667 / 0.170 · 3482 |
| 2108.09091 | 10 | 0/83 | 0.000 | 0.000 | 0.000 | 0.55 | 0.775 | 1513 | 0.26 | 1/1/38 · 3/2/30 · 26/10 | 0.000 / 0.000 · 3871 |
| 2006.00648 | 10 | 1/60 | 0.100 | 0.017 | 0.029 | 0.55 | 0.775 | 492 | 0.21 | 0/0/15 · 0/0/11 · 16/5 | 0.000 / 0.000 · 1969 |
| 2204.07974 | 6 | 0/104 | 0.000 | 0.000 | 0.000 | 0.90 | 0.950 | 1848 | 0.29 | 1/1/55 · 3/3/44 · 42/8 | 0.074 / 0.019 · 5997 |
| 2302.10588 | 19 | 3/65 | 0.158 | 0.046 | 0.071 | 0.70 | 0.850 | 1124 | 0.16 | 1/1/13 · 3/3/9 · 15/6 | 0.000 / 0.000 · 3192 |
| 2408.14199 | 2 | 0/64 | 0.000 | 0.000 | 0.000 | 0.62 | 0.812 | 1584 | 0.15 | 1/1/33 · 30/2/1 · 35/7 | 0.000 / 0.000 · 3982 |
| **mean (10)** | 17.2 | | **0.169** | **0.031** | 0.051 | 0.61 | 0.805 | 1424 | 0.21 | | 0.182 / 0.033 · 2949 |
## Reading the run

- The gate did its job: OpenAlex 1 request → 429 → circuit for the rest of the task (13–55 skips, 0 s waiting); arXiv
  2–6 requests → skips. Before WS4 the same tasks spent up to 285 s per task waiting on OpenAlex retries alone.
- The time budget fired on the long tasks (2312.04861, 2408.14199: `effort.time_capped` / `deep_pass.skipped`); the rest
  finished research inside 10 min on their own. What remains above 10 min is synthesis → citation chain → review →
  repair back-edge → re-synthesis (5 of 10 tasks took the repair loop, ≈ +10 min each).
- Reference scores are unchanged on average but flip per task (2108.09522 0.67/0.17 → 0.38/0.085; 2302.10588 and
  2006.00648 0 → 0.046 / 0.017); with 2–35 citations per report the metric is dominated by a handful of matches.
- 2408.14199 cited only 2 sources: the prompt's `before November 2024` cutoff plus venue constraints left almost nothing
  after the reviewer pruned unsupported statements — the date-window work (WS1-6) is the fix, not more time.
- Next: OpenAlex API key (prepaid credits; ~$0.08 per task) so the full 100-task run has all sources, then WS1
  (date window, reference budget 120, 1-hop snowballing).

Files: `full.summary.json` (runner summary incl. per-host `db_stats`). Per-task rows with trajectories and `db_stats`
stay in the API repo's `benchmark_runs/` (not published).
