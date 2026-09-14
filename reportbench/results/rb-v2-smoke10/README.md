# rb-v2 — 10-task smoke, rerun with a Semantic Scholar API key (L1, full row, 2026-09-13/14)

Same first 10 tasks as `rb-v1-smoke10`, production core, Gemini. Changes vs v1: `SEMANTIC_SCHOLAR_API_KEY` set, one
container at a time, 20 s pause, HTTP budget raised (4 status retries · 2 network retries · 30 s timeout · 120 s fan-out).
**Smoke, not a result.** Two tasks produced no report: the eval account's 1-hour token expired mid-task (tasks now take
20–26 min; the runner re-authenticated only every 40 min — lowered to 20 min afterwards). OpenAlex 429 / arXiv timeouts
still occurred on most tasks; Semantic Scholar now responds (28–33 hits per task).

Mean over the 8 scored tasks: P 0.155 / R 0.026 (v1 on the same 8 tasks: P 0.110 / R 0.017). Total $3.56.

| task | refs | matched/gold | P | R | F1 | cite-match | cited acc | s | $ | v1 P / R |
|---|---|---|---|---|---|---|---|---|---|---|
| 2312.04861 | 26 | 6/277 | 0.231 | 0.022 | 0.040 | 0.7 | 0.85 | 1256 | 0.46 | 0.240 / 0.018 |
| 2308.06419 | 18 | 1/106 | 0.056 | 0.009 | 0.016 | 0.7 | 0.85 | 1345 | 0.56 | 0.133 / 0.038 |
| 2308.15985 | 21 | 7/155 | 0.333 | 0.045 | 0.080 | 0.45 | 0.725 | 845 | 0.36 | 0.238 / 0.032 |
| 2402.10079 | 18 | 4/148 | 0.222 | 0.020 | 0.037 | 0.55 | 0.775 | 1191 | 0.34 | 0.227 / 0.034 |
| 2108.09522 | — | — | failed | failed | — | — | — | 1552 | 0.35 | 0.250 / 0.021 |
| 2108.09091 | 34 | 2/83 | 0.059 | 0.036 | 0.045 | 0.4 | 0.7 | 1113 | 0.32 | 0.000 / 0.000 |
| 2006.00648 | 5 | 1/60 | 0.200 | 0.017 | 0.031 | 0.75 | 0.875 | 1160 | 0.25 | 0.000 / 0.000 |
| 2204.07974 | — | — | failed | failed | — | — | — | 1396 | 0.16 | 0.032 / 0.010 |
| 2302.10588 | 30 | 3/65 | 0.100 | 0.046 | 0.063 | 0.6 | 0.8 | 1357 | 0.42 | 0.000 / 0.000 |
| 2408.14199 | 25 | 1/64 | 0.040 | 0.016 | 0.022 | 0.6667 | 0.8333 | 1335 | 0.34 | 0.040 / 0.016 |
| **mean (8 scored)** | 22.125 | | **0.155** | **0.026** | 0.042 | 0.602 | 0.801 | 1255 | 0.36 | 0.11 / 0.017 |
