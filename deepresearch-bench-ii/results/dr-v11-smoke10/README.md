# dr-v11 — 10-task smoke (L1 + official judge, full row, 2026-09-16)

Same 10 tasks as dr-v1/dr-v7. Changes since dr-v7 (api 0.1.31): table-cell hunt after both report paths (rows re-researched with topic-word queries, up to two pages per row), fact-hunt cap 20 with exhaustive `list` items, executive summary as an untitled lead paragraph in structure mode, per-requirement paragraph minimum, analysis rule with causal sentences, blocked-source DOI/truncated-title matching, section-revision guard in the repair pass (the rewrite prompt no longer truncates sections at 8k characters and keeps tables/sub-items verbatim), Semantic Scholar gate 2 s. The **internal judge now requires a verbatim evidence quote** (numbers below are not comparable with the dr-v7 internal column). dr-v8/v9/v10 were stopped early after 1–5 tasks when a defect showed (summary re-added by the repair pass; filled cells lost in the section rewrite) — not stored.

| task | lang | rubrics | internal overall | official overall (recall · analysis · presentation) | dr-v7 official | s | $ |
|---|---|---|---|---|---|---|---|
| task7 | zh | 58 | 0.29 | **0.36** (10/26 · 7/26 · 4/6) | 0.29 | 2186 | 0.16 |
| task1+ | en | 109 | 0.09 | **0.11** (7/87 · 1/17 · 4/5) | 0.11 | 2633 | 0.15 |
| task51 | zh | 83 | 0.10 | **0.12** (5/69 · 0/8 · 5/6) | 0.16 | 1834 | 0.76 |
| task2+ | en | 72 | 0.07 | **0.06** (1/53 · 0/11 · 3/8) | 0.07 | 2943 | 0.30 |
| task52 | zh | 48 | 0.15 | **0.21** (0/23 · 6/20 · 4/5) | 0.23 | 3507 | 0.27 |
| task3+ | en | 86 | 0.09 | **0.17** (9/64 · 2/13 · 4/9) | 0.24 | 2227 | 0.14 |
| task53 | zh | 75 | 0.17 | **0.27** (18/60 · 0/10 · 2/5) | 0.25 | 2361 | 0.18 |
| task4 | en | 72 | 0.06 | **0.10** (3/55 · 0/11 · 4/6) | 0.12 | 2646 | 0.07 |
| task4+ | zh | 63 | 0.17 | **0.19** (4/13 · 2/41 · 6/9) | 0.37 | 1790 | 0.24 |
| task54 | en | 67 | 0.37 | **0.54** (24/44 · 7/17 · 5/6) | 0.37 | 2506 | 1.01 |
| **mean** | | | **0.157** | **0.212** (recall 0.190 · analysis 0.124 · presentation 0.649) | 0.222 | 2463 | 0.33 |

Official judge vs dr-v7: **0.212 vs 0.222 — flat within task variance** (task54 +0.16, task7 +0.07, task53 +0.01; task4+ −0.18, task3+ −0.07, task51 −0.04). Recall 0.190 (v7 0.235), analysis 0.124 (0.161), presentation 0.649 (0.654). Per-task Pearson r with the internal judge = **0.97** (the evidence-quote rule fixed the over-crediting seen in dr-v7). Blocked-source −1 items: **9** (dr-v7: 2) — all on task54, where the report cited the research-brief pseudo-source [61] 121 times; that number never appears in References, and the official judge read it as the blocked article. Fixed for the next run (brief citations are stripped from the final body).

What moved: the cell hunt filled 6–14 cells per table-heavy task but the rubric values (accrual rates, minimum years, per-study parameters) mostly stayed unmatched — search reach, not pipeline plumbing, is now the limit; task4's 105 empty d-value cells exist only in the blocked paper. task4+ lost the VIX/GVZ/OVX definition rubrics that dr-v7 had (fact hunt 0/5 found this run vs 5/5 in dr-v7 — DuckDuckGo result variance). The repair-pass regression guard kept a 31k-character report on task1+ that the section rewrite had cut to 15.6k.

Files: `full.summary.json`, `official-gpt55.jsonl`, `official-gpt55-vs-internal.json`.
