---
created: 2026-05-16
type: article
tags: [article, evaluation, metrics, progressive-scroll, precision, recall]
source: "https://softwaredoug.com/blog/2021/05/05/finding-the-cutoff-when-search-results-stop-being-relevant.html"
author: [Doug Turnbull]
company: [Shopify]
concepts: [Precision and Recall, Search Evaluation]
topics: [Search Quality Assurance]
---

# Finding the Relevance Cutoff: When to Stop Showing Search Results

**[[Doug Turnbull]]** (at Shopify) explores metrics for the progressive-scroll UX — when users review *all* returned results and you need to know where to cut off the result set.

Classic metrics (NDCG) assume users ignore results past top-N. Progressive scroll is different — every returned result is potentially seen.

## Three Candidate Metrics

### 1. Variable Precision
Proportion of relevant results in the full result set: `sum(grades) / n`

**Fatal flaw**: Returns 1.0 if you show only 1 result (if it's relevant), even when many relevant results exist.

### 2. F1 Score
Harmonic mean of precision and recall over the full result set. Requires knowing `total_positives` (total relevant results in the corpus).

Advantages over variable precision: penalizes cutting out relevant results AND diluting with irrelevant ones.

### 3. Time Well Spent (compounding)
Accumulates reward/frustration as a user scrolls. Relevant results = +0.5 reward; irrelevant = -0.5 frustration. Compounding variant amplifies consecutive same-quality runs.

Better at capturing the tail: a long string of irrelevant results is harder to "recover" from.

## Key Insight

"There is no replacement for combining qualitative + quantitative understanding of search quality. Targeted, simple metrics with well-known flaws beat complex metrics that try to 'capture everything'."

The right metric for progressive scroll is **not NDCG** — it's F1 or a time-based model that treats the entire returned set holistically.
