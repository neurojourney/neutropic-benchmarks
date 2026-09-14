# AstaBench runner (planned)

AstaBench is run through Ai2's `agent-eval` harness (Inspect-based), not
through the Neutropic matrix runner. The plan is a thin solver that calls the
Neutropic headless core per sample and returns the answer / artifact the
task expects; `agent-eval` handles scoring, logs and cost accounting.

## Files

| File | Purpose |
|------|---------|
| `chart.json` · `chart.py` · `logos/` | data + sources behind `../chart.png`; `python chart.py` re-renders it (matplotlib). `logos/` holds 96 px brand marks (trademarks of their owners, used for identification only) |
| `solver/solver.py` | Inspect `@solver` that POSTs each sample to the Neutropic solve service and returns the chat answer; multiple-choice prompts are rewritten to a `Final answer: <letter>` instruction and converted back to `{"answer": "<letter>"}` for the scorer |
| `solver/tasks.py` | task wrappers pinning `with_search_tools=False` (custom-tools track) — the stock `litqa2` wrapper drops that `-T` argument |
| `solver/serve.py` | the solve service (`python -m app.benchmarks.serve`, runs inside the Neutropic bench container; copy of `neutropic2-api/app/benchmarks/serve.py`) |

## Setup

```bash
git clone --recursive --branch v0.3.1 https://github.com/allenai/asta-bench.git ~/.neutropic-bench/asta-bench
cd ~/.neutropic-bench/asta-bench && uv sync
cp -r <this repo>/astabench/runner/solver solvers/neutropic
# Neutropic side: bench image + solve service on :8765 (session-independent container)
python scripts/bench-detached.py --serve 8765 --policy full --provider gemini
```

```bash
export GOOGLE_API_KEY=...          # Inspect requires a --model even though the solver never calls it
uv run inspect eval solvers/neutropic/tasks.py@litqa2_notools -T split=all \
  --solver solvers/neutropic/solver.py@neutropic --model google/gemini-3.8-flash \
  --limit 10 --max-connections 1 --log-dir logs/neutropic-litqa2 --display plain
```

Official splits need `HF_TOKEN` with access to the gated `allenai/asta-bench` dataset; the standard-tools track needs
`ASTA_TOOL_KEY` (Asta Scientific Corpus). Cost is reported by the service (`metadata.neutropic.cost_usd` per sample),
not by Inspect's model usage.

Order: Literature Understanding → Data Analysis (DiscoveryBench) →
Code & Execution (needs containerized repos for CORE-Bench / SUPER) →
End-to-End Discovery. Validation split for development; test split only for
the leaderboard submission. Both standard-tools and custom-tools tracks are
reported.
