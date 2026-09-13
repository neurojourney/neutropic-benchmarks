# AstaBench runner (planned)

AstaBench is run through Ai2's `agent-eval` harness (Inspect-based), not
through the Neutropic matrix runner. The plan is a thin solver that calls the
Neutropic headless core per sample and returns the answer / artifact the
task expects; `agent-eval` handles scoring, logs and cost accounting.

## Files

| File | Purpose |
|------|---------|
| `chart.json` · `chart.py` · `logos/` | data + sources behind `../chart.png`; `python chart.py` re-renders it (matplotlib). `logos/` holds 96 px brand marks (trademarks of their owners, used for identification only) |
| `solver/` (planned) | `neutropic_solver.py` — `agent-eval` solver wrapping `run_headless`; `tools.py` — Asta Scientific Corpus search registered as a Neutropic search connector for the standard-tools track |

## Setup (planned)

```bash
pip install agent-eval            # harness + datasets
export ASTA_TOOL_KEY=...           # Asta Scientific Corpus (standard-tools track)
```

## Run (planned)

```bash
# one category on the validation split
agent-eval run --suite astabench --split validation --tasks lit \
  --solver neutropic_solver.py --log-dir results/asta-lit-v1/
# scores + cost per problem
agent-eval score results/asta-lit-v1/ > results/asta-lit-v1/scores.json
```

Order: Literature Understanding → Data Analysis (DiscoveryBench) →
Code & Execution (needs containerized repos for CORE-Bench / SUPER) →
End-to-End Discovery. Validation split for development; test split only for
the leaderboard submission. Both standard-tools and custom-tools tracks are
reported.
