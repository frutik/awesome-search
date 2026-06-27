---
type: article
title: "How to Really Do Autocomplete"
source: "https://bonsai.io/blog/how-to-really-do-autocomplete/"
author: "[[Max Irwin]]"
company: "[[Bonsai]]"
published: 2025-06-06
tags: [article, company-blog, autocomplete, elasticsearch, opensearch, edge-ngram, aggregations]
concepts: ["[[Autocomplete]]", "[[Full-Text Search]]"]
topics: ["[[Autocomplete and Autosuggest]]"]
created: 2026-06-27
---

# How to Really Do Autocomplete

Part 1 of [[Max Irwin]]'s [[Bonsai]] autocomplete series. Its thesis targets a gap every other tutorial skips: **how to generate the suggestion vocabulary from your actual document content** — not assume you already have a curated list of terms. Official docs (including OpenSearch's) start from a predefined suggestion dictionary; real sites rarely have one. Worked end-to-end on Bonsai's own ~260-page site. Continued in [[How to Really Scale Autocomplete]].

---

## The Two Things Users Expect

When typing, users want both:
1. **Pages / results** — actual content matching the prefix.
2. **Search terms** — guidance on *what* to search, because "they might not know what content your site has, or they might not know how to express themselves."

## Three-Field Architecture

| Step | Field | Technique | Produces |
|---|---|---|---|
| 1. Page suggestions | `completion` | **Edge-ngram** tokenizer (`min_gram:1`, `max_gram:25`); title + description copied in | Fast prefix-matched document hits — trades memory to avoid slow prefix queries |
| 2. Word suggestions | `suggest_word` (`fielddata: true`) | **`significant_terms`** aggregation with an `include` prefix pattern; light stemming (possessive only); stopwords filtered | Single-word suggestions that are *statistically interesting* in the prefix-filtered subset vs. the whole corpus |
| 3. Phrase suggestions | `suggest_phrase` (`fielddata: true`) | **Shingles** (bigrams + trigrams) | Multi-word suggestions like "opensearch platform" |

A single request returns ranked document hits **+** word suggestions **+** phrase suggestions together.

## Why `significant_terms` (not plain `terms`)

`significant_terms` surfaces terms that are unusually frequent in the matched subset relative to the background corpus — so suggestions are *relevant to the prefix*, not just globally common words. (Part 2 shows this aggregation must be swapped for a pre-filtered plain `terms` agg once you hit millions of docs.)

## Post-Processing

- Shingle phrases contain stopword placeholders (`_`) that must be cleaned.
- Suggested terms are re-run through the `analyze_english` analyzer to **collapse variants/duplicates**.
- A JS example uses `@opensearch-project/opensearch` + `p-limit` for parallel normalization, emitting `{label, value}` objects (🔍 for search terms, 🔖 for documents).

## Performance Target

Sub-50ms ideal, ≤70ms acceptable; above ~250ms the lag is user-perceptible.

## Related Topics
- [[Autocomplete and Autosuggest]]

## Related Concepts
- [[Autocomplete]]
- [[Full-Text Search]]

## Related Articles
- [[How to Really Scale Autocomplete]] — Part 2; what breaks at 6M docs and how to fix it
- [[LLM-Powered Query Extraction for Autocomplete]] — an LLM alternative for generating the suggestion vocabulary

## People
- [[Max Irwin]]

## Source
- https://bonsai.io/blog/how-to-really-do-autocomplete/
