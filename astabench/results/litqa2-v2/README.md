# litqa2-v2 — 10-question smoke (custom-tools track, 2026-09-17)

Same 10 public-split LitQA2 questions as `litqa2-smoke10`, production core with the **exact-term probe** (improvement-plan A2: the question's distinctive terms — strain, gene, mutation, technique — are searched as exact phrases through the paper fan-out and Europe PMC directly; the top open-access PMC full texts are read and the passages around the question/option terms are injected before the model acts) and `fetch_page` serving Europe PMC full text for PMC/DOI links. Solver capped at 14 steps per question (the first attempt without a cap ran 48 steps / 25 min / $1.28 on Q1 and was stopped).

| id | question | answer | result |
|---|---|---|---|
| 27234279 | Approximately how many unique transposable element insertion loci are there in the mandari | C | insufficient |
| 2c05315d | Are enhancer and promoter sequences broadly compatible in human cells, and is this the sam | E | correct (sure) |
| 39129e1c | Among Cas9-disrupted loci in human neural stem cells, what fraction of disruption phenotyp | B | correct (sure) |
| 517e7cf8 | Approximately what percentage of Drosophila with a H3.3K36R mutation finish developing and | E | insufficient |
| 5c4c602c | At which amino acid position is a large oligosaccharide density observed in the cryo-EM ma | D | correct (sure) |
| 76184ccf | Active olfactory receptor genes increase their contacts with greek island regions by what  | D | insufficient |
| c9bdb9b5 | Based on experiments done in cohorts of mice injected with B16-F10 melanoma cells expressi | D | insufficient |
| cb710074 | Approximately what percentage of adr-1(-), adr-2(-), and adr-1(-);adr-2(-) mutant C. elega | F | insufficient |
| e3b5a4af | Acinetobacter lwoffii has been evolved in the lab to be resistant to which of these antibi | D | insufficient |
| e6b0f9e5 | Based on single-nuclei RNA sequencing data, myotendinous junction myonuclei are enriched f | E | correct (sure) |

**accuracy 0.40 · precision 1.00 · coverage 0.40** (litqa2-smoke10: 0.30 / 1.00 / 0.30). $2.49 · 49 min for 10 questions (27 s – 10.5 min each).

Where the six 'insufficient' answers came from (model justifications in the eval log): four found the right paper (Salzler 2023 / Brown 2024 for H3.3K36R, Monahan 2019 for Greek islands, Wang 2024 for B16-F10, Dhakal 2024 for adr-1/adr-2) but said the exact figure was 'in the full-text figures, not the accessible text' — tool observations over 4,000 characters are spilled to a file, so `fetch_page` on a 60k-character paper showed only the introduction; one (Acinetobacter lwoffii) answered from prior knowledge in 27 s without searching, before the probe (which runs at plan time, after the first search) could fire; one (Citrus reticulata TE loci) found the pangenome papers but not the count. Fixes for the next run: probe runs on the first step before any search; `fetch_page(url, query=…)` returns the passages around the query terms; excerpts include neighbouring sentences and favour numeric sentences for numeric questions.

Files: `litqa2-notools.eval` (Inspect log, samples with justifications), `scores.json`.
