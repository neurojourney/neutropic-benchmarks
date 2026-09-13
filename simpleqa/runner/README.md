# SimpleQA runner

Adapter: `neutropic2-api/app/benchmarks/simpleqa.py` (attaches the
`research-web` skill and a "verify with search first, then answer in one
line" suffix to every question; output normalized to a short answer, report
synthesis and review disabled). Grader: 3-way `correct` / `incorrect` /
`not_attempted` with a fixed cloud model.

## Files

| File | Purpose |
|------|---------|
| `matrix.yaml` | ablation ladder used for `matrix-v2` / `matrix-v3` (copy of `neutropic2-api/evals/matrix.yaml`) |
| `chart.json` · `chart.py` · `logos/` | data + sources behind `../chart.png`; `python chart.py` re-renders it (matplotlib). `logos/` holds 96 px brand marks (trademarks of their owners, used for identification only) |

## Run

```bash
# from neutropic2-api, inside the bench Docker image
python -m app.benchmarks.matrix --config evals/matrix.yaml            # 4 rows, subset 100
python -m app.benchmarks.matrix --config evals/matrix.yaml --rows full # one row
python -m app.benchmarks.run --bench simpleqa --data evals/simpleqa_test.csv \
  --policy full --provider gemini --grader-provider gemini --tag official-v1   # full 4,326 (L2)
```

- Never regenerate `simpleqa_subset100.csv` — it is the baseline for every row and machine.
- Change `tag:` for a new run; keeping it resumes an interrupted one.
- `NEUTROPIC_SEARCH_CACHE=replay` re-runs a row against recorded search results (model nondeterminism only).

## Output → `results/<tag>/`

Copy `simpleqa_<row>_<tag>-<row>.summary.json` as `<row>.summary.json` and
`<tag>_comparison.{md,json}`; per-item `.jsonl` after review.
