One 10-question LitQA2 smoke so far (custom-tools track, public split). Planned per category: `asta-lit-v1` → `asta-data-v1` → `asta-code-v1` → `asta-e2e-v1`, each as agent-eval logs plus a `scores.json`. Validation split during development; test split only for leaderboard submission. See [../../README.md](../../README.md) for projected targets.

| Run | Date | Task | Notes |
|-----|------|------|-------|
| `litqa2-smoke10` | 2026-09-13 | `litqa2` (public split, no Asta tools) | 10 questions via the Neutropic solve service — accuracy 0.30, precision 1.00, coverage 0.30, $2.18 · 20 min. Custom-tools track; not a leaderboard result. |
