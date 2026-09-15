One 10-task smoke so far (`dr-v1-smoke10`, internal Gemini judge, re-scored with the official GPT-5.5 judge). Next: `dr-v2` (WS2 fact ledger + request-structure composer, same 10 tasks then 132), `dr-v3` (GPT-5.5 judge on the same reports), `dr-official` (official `run_evaluation.py`; reports stored as `report/<row>/idx-*.md` for submission). See [../../README.md](../../README.md) for projected targets.

| Run | Date | Rows | Notes |
|-----|------|------|-------|
| `dr-v1-smoke10` | 2026-09-13/14 | full | 10 of 132 tasks, Gemini judge — overall 0.107 (recall 0.08 / analysis 0.07 / presentation 0.30), $0.41 · 712 s per task. Same reports under the official GPT-5.5 judge (2026-09-14): **0.136** (recall 0.10 / analysis 0.09 / presentation 0.35), per-task r = 0.97 with the internal judge. Smoke only. |
