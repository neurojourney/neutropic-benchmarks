# litqa2-smoke10 — AstaBench LitQA2 (custom-tools track), first 10 tasks (L1, 2026-09-13)

Harness: [asta-bench v0.3.1](https://github.com/allenai/asta-bench) (Inspect) → Neutropic headless solve service
(`serve.py`, production core in the bench container) via `solver/solver.py`. Task: `litqa2` from LAB-bench, public
`split=all` (the official validation split needs the gated `allenai/asta-bench` HF dataset), no Asta Scientific Corpus tool
(`ASTA_TOOL_KEY` not set) — retrieval is Neutropic's own academic fan-out. **Smoke, not a leaderboard result**: 10 of the
task's questions, one of AstaBench's 11 benchmarks.

Metrics (official `score_litqa2` scorer): accuracy **0.3**, precision 1.0
(correct among sure answers), coverage 0.3 (share of sure answers). Total $2.18, 20 min.
The agent chose "Insufficient information" whenever its searches did not surface the key paper (6 of 10); one reply had no
final letter and scored as wrong.

| sample | target | answer | correct | sure | tools | s | $ |
|---|---|---|---|---|---|---|---|
| 27234279 | F | C | no | no | 11 | 110 | 0.22 |
| 2c05315d | E | E | yes | yes | 7 | 58 | 0.14 |
| 39129e1c | B | B | yes | yes | 11 | 84 | 0.16 |
| 517e7cf8 | A | E | no | no | 12 | 109 | 0.19 |
| 5c4c602c | D | D | yes | yes | 12 | 108 | 0.22 |
| 76184ccf | A | D | no | no | 12 | 195 | 0.19 |
| c9bdb9b5 | A | D | no | no | 6 | 59 | 0.10 |
| cb710074 | G | F | no | no | 12 | 318 | 0.57 |
| e3b5a4af | C | D | no | no | 3 | 73 | 0.17 |
| e6b0f9e5 | E | (no letter) | no | no | 12 | 109 | 0.21 |
