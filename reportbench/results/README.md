No runs yet. Planned: `rb-v1` (2026-10, 10-task smoke then 100 tasks; rows basic-search / full / full-no-review / full-no-citechain), `rb-v2` (2026-12, citation snowballing + reference budget), `rb-official` (2027 H1, official scripts). See [../../README.md](../../README.md) for projected targets.

| Run | Date | Rows | Notes |
|-----|------|------|-------|
| `rb-v1-smoke10` | 2026-09-13 | full | 10 of 100 tasks — P 0.116 / R 0.017 (first five P 0.22 / R 0.029; academic-DB rate limits degraded the rest), citation match 0.65, $0.34 · 840 s per task. Smoke only. |
| `rb-v2-smoke10` | 2026-09-13/14 | full | same 10 tasks with a Semantic Scholar key, single container, larger HTTP budget — P 0.155 / R 0.026 over 8 scored tasks (2 lost their report to token expiry), $0.36 · 1,255 s per task. Smoke only. |
