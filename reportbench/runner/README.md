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
| `matrix_reportbench.yaml` | ablation ladder (basic-search / full / full-no-review / full-no-citechain); `full` = product Deep preset; the adapter adds `report_max_sources: 120`, `snowball_hops: 1` and the prompt date window (rb-v5 configuration), `full-no-snowball` turns snowballing off |
| `chart.json` · `chart.py` · `logos/` | data + sources behind `../chart.png`; `python chart.py` re-renders it (matplotlib). `logos/` holds 96 px brand marks (trademarks of their owners, used for identification only) |

## Data

```bash
git clone https://github.com/ByteDance-BandAI/ReportBench ~/.neutropic-bench/data/ReportBench
# ReportBench_v1.1.jsonl + ReportBench_v1.1_GT/<arxiv_id>.jsonl — not committed here
```

## Run

```bash
python -m app.benchmarks.matrix --config evals/matrix_reportbench.yaml          # smoke (limit 10)
python -m app.benchmarks.run --bench reportbench --data bench_data/ReportBench/ReportBench_v1.1.jsonl \
  --policy full --provider gemini --grader-provider gemini --pause 10 --tag rb-v1
```

Per task: one research turn (search fan-out → snowball → deep pass → report →
review → repair) plus ≤ 40 grader calls. Measured on rb-v5: $0.28 and 20 min
per task (max 38 min) with the WS4 request gate and 600 s research budget;
100 tasks ≈ 33 h, ≈ $28 + OpenAlex ≈ $8.

## Official protocol (L2)

Feed the same reports to the official pipeline —
`statement_evaluator.py` → `related_work_evaluator.py` →
`metrics_calculator.py` — and store its output next to ours as
`results/<tag>/official/`.
