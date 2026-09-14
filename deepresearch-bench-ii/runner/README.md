# DeepResearch Bench II runner

Adapter: `neutropic2-api/app/benchmarks/deepresearch.py`. Loads the official
`tasks_and_rubrics.jsonl` (field names read leniently), runs one deep-research
turn per task, and grades the report against each binary rubric
(PASS / FAIL) with a fixed judge. Metrics: `overall_pass_rate` and
`recall / analysis / presentation_pass_rate`; cited-statement accuracy reuses
the ReportBench evaluator.

## Files

| File | Purpose |
|------|---------|
| `matrix_deepresearch.yaml` | ladder for `dr-v1` (basic-search / full / full-no-review) |
| `chart.json` · `chart.py` · `logos/` | data + sources behind `../chart.png`; `python chart.py` re-renders it (matplotlib). `logos/` holds 96 px brand marks (trademarks of their owners, used for identification only) |

## Data

```bash
git clone https://github.com/imlrz/DeepResearch-Bench-II ~/.neutropic-bench/data/DRB2
# tasks_and_rubrics.jsonl — 132 tasks, per-task licence (129 CC BY 4.0, 2 CC BY-NC 4.0, 1 CC0)
```

## Run

```bash
python -m app.benchmarks.matrix --config evals/matrix_deepresearch.yaml        # smoke (limit 10)
python -m app.benchmarks.run --bench deepresearch --data bench_data/DRB2/tasks_and_rubrics.jsonl \
  --policy full --provider gemini --grader-provider gemini --tag dr-v1
```

Per task: one research turn plus (number of rubrics ≤ 60) + (≤ 20 citation
judgements) grader calls. Reports are also written as
`results/<tag>/report/<row>/idx-<task>.md` — the layout the official
submission expects.

## Official protocol (L2) and submission (L3)

```bash
python run_evaluation.py --reports results/<tag>/report/full --judge gpt-5.5   # official repo
python aggregate_scores.py
```

Report internal-vs-official per-task agreement before quoting an L2 number.
Submission: e-mail the maintainers with the `report/` folder, a temporary
GPT-5.5 key and reproducibility details.

## Contamination guard

Rubrics are public. `tests/test_bench_contamination.py` (planned) asserts that
no rubric string appears in prompts, skill guidance or the retrieval corpus;
blocked-source exclusions are logged per task in the results.
