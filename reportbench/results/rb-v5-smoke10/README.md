# rb-v5 — 10-task smoke, WS1 recall work: date window · reference cap 120 · citation snowballing (L1, 2026-09-15)

Same first 10 tasks as rb-v3/rb-v4, same `full` = product Deep preset with the WS4 execution budget (10-min research
budget, request gate, no figures), production core, Gemini. What changed (`docs/benchmark-improvement-plan.md` WS1):

1. **The prompt's publication window is enforced.** 8 of 10 prompts say "all referenced papers must have been published
   before <month year>"; the turn extracts that window and sends it to every literature DB as a query filter (Semantic
   Scholar `year`, OpenAlex `to_publication_date`, arXiv `submittedDate`, Crossref, PubMed, Europe PMC) and drops
   out-of-window records at evidence collection. rb-v3 had 24 % of citations after the cutoff; rb-v5 has **0 of 290**.
2. **Reference cap 60 → 120** (`report_max_sources`), so the report can draw on a wider pool.
3. **1-hop citation snowballing**: the top 5 sources' references (OpenAlex batch) and citing papers (OpenAlex `cites:`),
   filtered by window/blocked/relevance, ranked by co-citation then citation count, top 30 added to the evidence
   (200–380 candidates per task → 30 added; 3 tasks ran their research past the budget and skipped it — fixed after
   the run so snowballing always runs).
4. OpenAlex API key active: 13–45 OpenAlex requests per task, **0 × 429** (rb-v4 had OpenAlex fully unavailable).

**Smoke, not a result** — 10 of 100 tasks, internal (L1) judge. Mean over 10 tasks: **P 0.287 / R 0.070 / F1 0.109**
(rb-v4 0.169 / 0.031 / 0.051; rb-v3 0.182 / 0.033 / 0.055), citation match 0.69, cited-statement accuracy 0.85,
22.3 cited references per report, **every task > 0** (rb-v3/v4 had four zeros). 20 min per task (max 38), $0.28,
$2.77 total.

| task | prompt cutoff | refs / after cutoff | cited | matched/gold | P | R | F1 | cite-match | cited acc | s | $ | OpenAlex req/429 | rb-v4 P / R | rb-v3 P / R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2312.04861 | April 2025 | 46 / 0 | 26 | 10/277 | 0.385 | 0.036 | 0.066 | 0.55 | 0.775 | 1136 | 0.42 | 13/0 | 0.286 / 0.036 | 0.467 / 0.054 |
| 2308.06419 | — | 24 / 0 | 15 | 4/106 | 0.267 | 0.038 | 0.066 | 0.80 | 0.900 | 1063 | 0.33 | 28/0 | 0.222 / 0.057 | 0.300 / 0.057 |
| 2308.15985 | August 2023 | 27 / 0 | 20 | 8/155 | 0.400 | 0.052 | 0.091 | 0.50 | 0.750 | 693 | 0.28 | 24/0 | 0.273 / 0.039 | 0.200 / 0.013 |
| 2402.10079 | March 2025 | 35 / 0 | 29 | 7/148 | 0.241 | 0.047 | 0.079 | 0.65 | 0.825 | 756 | 0.39 | 18/0 | 0.267 / 0.027 | 0.115 / 0.020 |
| 2108.09522 | August 2021 | 19 / 0 | 18 | 10/47 | 0.556 | 0.192 | 0.285 | 0.67 | 0.833 | 1547 | 0.20 | 43/0 | 0.385 / 0.085 | 0.667 / 0.170 |
| 2108.09091 | August 2021 | 18 / 0 | 15 | 5/83 | 0.333 | 0.133 | 0.190 | 0.60 | 0.800 | 1551 | 0.16 | 45/0 | 0.000 / 0.000 | 0.000 / 0.000 |
| 2006.00648 | November 2020 | 31 / 0 | 30 | 3/60 | 0.100 | 0.050 | 0.067 | 0.75 | 0.875 | 738 | 0.31 | 22/0 | 0.100 / 0.017 | 0.000 / 0.000 |
| 2204.07974 | April 2022 | 25 / 0 | 18 | 5/104 | 0.278 | 0.048 | 0.082 | 0.65 | 0.825 | 1302 | 0.18 | 35/0 | 0.000 / 0.000 | 0.074 / 0.019 |
| 2302.10588 | — | 32 / 0 | 19 | 3/65 | 0.158 | 0.046 | 0.071 | 0.80 | 0.900 | 676 | 0.29 | 22/0 | 0.158 / 0.046 | 0.000 / 0.000 |
| 2408.14199 | November 2024 | 33 / 0 | 33 | 5/64 | 0.151 | 0.062 | 0.088 | 0.94 | 0.972 | 2258 | 0.21 | 36/0 | 0.000 / 0.000 | 0.000 / 0.000 |
| **mean (10)** | | | 22.3 | | **0.287** | **0.070** | 0.109 | 0.69 | 0.846 | 1172 | 0.28 | | 0.169 / 0.031 | 0.182 / 0.033 |
## Reading the run

- Recall more than doubled on the same tasks (0.031 → 0.070) and precision rose (0.169 → 0.287) — the two zero-score tasks of
  rb-v4 (2108.09091, 2204.07974) now match 5 gold references each, 2408.14199 (2 citations in rb-v4) cites 33. The gains
  come from citing papers that exist in the survey's period rather than 2024–2026 follow-ups, and from the snowball pool.
- Recall is still capped by how many sources the report *cites* (15–33): the evidence pool now holds 120+ in-window papers,
  but each section cites a handful. The next lever is composer-side — a survey-style "related literature" coverage that
  cites the wider pool — plus reference ID normalisation (DOI/arXiv fill) so matches are not missed on title variants.
- For scale: the published ReportBench numbers (100 tasks) are recall 0.036 (Gemini Deep Research) and precision 0.385
  (OpenAI Deep Research). rb-v5 is 10 tasks under an internal judge, so no ranking claim is made here; the 100-task run is
  the next step (≈ 33 h, ≈ $28 + OpenAlex ≈ $8).

Files: `full.summary.json` (runner summary incl. per-host `db_stats`). Per-task rows with trajectories stay in the API
repo's `benchmark_runs/` (not published).
