# ReportBench runner

Adapter: `neutropic2-api/app/benchmarks/reportbench.py`. Each task is a
survey-writing prompt derived from an arXiv survey; the evaluator matches the
report's reference list against the expert references (`reference_precision /
recall / f1`, deterministic on title / arXiv id / DOI), judges each cited
statement against its source (`citation_match_rate`,
`cited_statement_accuracy`) and approximates non-cited factuality with a
parametric grader (`noncited_accuracy`, row-to-row comparison only).

## Files

| File | Purpose |
|------|---------|
| `matrix_reportbench.yaml` | ablation ladder for `rb-v1` (basic-search / full / full-no-review / full-no-citechain) |
| `chart.json` · `chart.py` · `logos/` | data + sources behind `../chart.png`; `python chart.py` re-renders it (matplotlib). `logos/` holds 96 px brand marks (trademarks of their owners, used for identification only) |

## Data

```bash
git clone https://github.com/ByteDance-BandAI/ReportBench ~/.neutropic-bench/data/ReportBench
# ReportBench_v1.1.jsonl + ReportBench_v1.1_GT/<arxiv_id>.jsonl — not committed here
```

## Run

```bash
python -m app.benchmarks.matrix --config evals/matrix_reportbench.yaml          # smoke (limit 10)
python -m app.benchmarks.run --bench reportbench --data /bench/ReportBench/ReportBench_v1.1.jsonl \
  --policy full --provider gemini --grader-provider gemini --pause 10 --tag rb-v1
```

Per task: one research turn (search fan-out → report → review → repair) plus
≤ 40 grader calls. Budget roughly $0.5–1.5 and 5–15 min per task.

## Official protocol (L2)

Feed the same reports to the official pipeline —
`statement_evaluator.py` → `related_work_evaluator.py` →
`metrics_calculator.py` — and store its output next to ours as
`results/<tag>/official/`.
