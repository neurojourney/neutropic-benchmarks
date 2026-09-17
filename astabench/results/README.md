Two 10-question LitQA2 smokes so far (`litqa2-smoke10`, `litqa2-v2`) (custom-tools track, public split). Planned per category: `asta-lit-v1` → `asta-data-v1` → `asta-code-v1` → `asta-e2e-v1`, each as agent-eval logs plus a `scores.json`. Validation split during development; test split only for leaderboard submission. See [../../README.md](../../README.md) for projected targets.

| Run | Date | Task | Notes |
|-----|------|------|-------|
| `litqa2-smoke10` | 2026-09-13 | `litqa2` (public split, no Asta tools) | 10 questions via the Neutropic solve service — accuracy 0.30, precision 1.00, coverage 0.30, $2.18 · 20 min. Custom-tools track; not a leaderboard result. |
| `litqa2-v2` | 2026-09-17 | `litqa2` (public split, no Asta tools) | same 10 questions with the exact-term probe (phrase search + Europe PMC full text) and a 14-step cap — accuracy 0.40, precision 1.00, coverage 0.40, $2.49 · 49 min. Four of six 'insufficient' answers had the right paper but could not see the figure (4k-character tool-output spill); fixed next. |
