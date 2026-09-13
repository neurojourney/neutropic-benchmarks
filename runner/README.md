# Reproducing a Neutropic benchmark run

The adapters and evaluators live in the Neutropic API repository
(`neutropic2-api/app/benchmarks/`); this folder documents the commands and
the result file layout so that a `results/<run-tag>/` folder here can be
regenerated.

## Runner

```bash
# one benchmark, one row
python -m app.benchmarks.run --bench <simpleqa|reportbench|deepresearch> \
  --data <dataset file> --policy <model-only|basic-search|generic-rag|full> \
  --provider gemini --grader-provider gemini --limit 10 --tag <run-tag>

# full ablation ladder from a matrix file
python -m app.benchmarks.matrix --config evals/matrix.yaml
```

Runs execute inside the API Docker image with `NEUTROPIC_SEARCH_CACHE=on`
(first run, records search results) or `=replay` (deterministic re-run),
`NEUTROPIC_EMBED_PROVIDER=off`, and `NEUTROPIC_WORKDIR_SCOPE=session`
(per-question working directory). Sessions are isolated in a dedicated
`__benchmarks__` project with project memory disabled.

## Datasets

| Benchmark | Source | Notes |
|-----------|--------|-------|
| SimpleQA | `simpleqa_test.csv` (OpenAI simple-evals) | fixed 100-question subset `simpleqa_subset100.csv` is topic-stratified and deterministic — never regenerated |
| ReportBench | `git clone https://github.com/ByteDance-BandAI/ReportBench` | `ReportBench_v1.1.jsonl` + `ReportBench_v1.1_GT/` |
| DeepResearch Bench II | `git clone https://github.com/imlrz/DeepResearch-Bench-II` | `tasks_and_rubrics.jsonl`; per-task CC BY / CC BY-NC / CC0 licences |
| AstaBench | `pip install agent-eval` + Ai2 datasets | validation split for development, test split for submission only |

Dataset files are not committed here.

## Result files

| File | Content |
|------|---------|
| `<row>.summary.json` | n, grade distribution, accuracy metrics, `agent_performance` (tool success / selection / recovery, latency, tokens, cost), grader, policy overrides |
| `<tag>_comparison.md` / `.json` | all rows of one run side by side (the ablation ladder) |
| `<bench>_<policy>_<tag>-<row>.jsonl` | per-item: question, gold, answer, grade, usage, trajectory (added after review) |

## Rows

| Row | Tools | Research policy | Meaning |
|-----|-------|-----------------|---------|
| `model-only` | none | off | frontier model baseline |
| `basic-search` | web search | off | model + search |
| `generic-rag` | search + corpus | off | model + generic RAG |
| `full` | all | on | Neutropic (planner, iterative retrieval, reranker, evidence store, citation chain, reviewer, repair) |
| `full-no-<component>` | all | on, one component removed via `overrides:` | component ablation |
