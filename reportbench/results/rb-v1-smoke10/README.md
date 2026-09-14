# rb-v1 — 10-task smoke (L1, full row, 2026-09-13)

First 10 tasks of `ReportBench_v1.1.jsonl`, production core, Gemini. **Smoke, not a result** — every task hit Semantic Scholar 429 / arXiv timeouts (no API key, two containers in parallel), so the CS-heavy tasks were answered from ERIC / Europe PMC results; the last five tasks are near zero for that reason. Reference P/R are deterministic (title / arXiv / DOI match); citation judgements are LLM-graded.

| task | refs | matched/gold | P | R | F1 | cite-match | cited acc | s | $ |
|---|---|---|---|---|---|---|---|---|---|
| 2312.04861 | 25 | 6/277 | 0.240 | 0.018 | 0.034 | 0.7 | 0.85 | 793 | 0.33 |
| 2308.06419 | 30 | 4/106 | 0.133 | 0.038 | 0.059 | 0.65 | 0.825 | 744 | 0.31 |
| 2308.15985 | 21 | 5/155 | 0.238 | 0.032 | 0.057 | 0.6 | 0.8 | 636 | 0.29 |
| 2402.10079 | 22 | 5/148 | 0.227 | 0.034 | 0.059 | 0.5 | 0.75 | 803 | 0.52 |
| 2108.09522 | 24 | 6/47 | 0.250 | 0.021 | 0.039 | 0.75 | 0.875 | 1182 | 0.37 |
| 2108.09091 | 28 | 0/83 | 0.000 | 0.000 | 0.000 | 0.6 | 0.8 | 687 | 0.27 |
| 2006.00648 | 7 | 0/60 | 0.000 | 0.000 | 0.000 | 0.95 | 0.975 | 660 | 0.21 |
| 2204.07974 | 31 | 1/104 | 0.032 | 0.010 | 0.015 | 0.5 | 0.75 | 1238 | 0.40 |
| 2302.10588 | 12 | 0/65 | 0.000 | 0.000 | 0.000 | 0.7 | 0.85 | 842 | 0.26 |
| 2408.14199 | 25 | 1/64 | 0.040 | 0.016 | 0.022 | 0.5 | 0.75 | 811 | 0.48 |
| **mean** | 22.5 | | **0.116** | **0.017** | 0.028 | 0.645 | 0.823 | 840 | 0.34 |
