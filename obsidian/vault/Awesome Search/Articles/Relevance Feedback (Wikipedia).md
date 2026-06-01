---
title: "Relevance Feedback (Wikipedia)"
author: "[[Wikipedia]]"
published: 2006-07-04
source: "https://en.wikipedia.org/wiki/Relevance_feedback"
tags:
  - article
  - relevance-feedback
  - query-understanding
  - ir-foundations
created: 2026-05-31
---

# Relevance Feedback (Wikipedia)

## Summary

Wikipedia reference article on relevance feedback in information retrieval and recommender systems. Covers the three types (explicit, implicit, pseudo/blind) and the Rocchio algorithm. Foundational IR theory with well-cited references to TREC experiments and academic literature.

## Key Concepts Covered

### Explicit Feedback
User directly marks results as relevant or irrelevant using binary or graded scales. Requires active user participation — rare in practice. [[NDCG]] emerged around 2005 as the dominant metric for evaluating rankings built on explicit feedback.

### Implicit Feedback
Inferred from behavior: clicks, dwell time, browsing/scrolling. The user is not aware that their behavior is used as a relevance signal. Key types:
- **Dwell time** — time on page after clicking a result; high dwell = likely relevant
- **Click selection** — which results were opened

### Pseudo-Relevance Feedback (PRF)
Automates the manual part of relevance feedback. Assumes the top-k retrieved documents are relevant, extracts high-weight terms (via tf-idf), expands the query, and re-executes. Risk: **query drift** — if the top-k is poor, expansion terms can pull the query in the wrong direction.

PRF procedure:
1. Retrieve initial result set
2. Take top-k (typically 10–50) as assumed-relevant
3. Extract top 20–30 terms by tf-idf weight
4. Expand query with those terms and re-execute

Cornell SMART system results (Buckley et al., 1995) showed improvement on TREC 4. But web search is more susceptible to drift because web documents span multiple topics.

### Rocchio Algorithm
The classic vector-space implementation of explicit feedback:
```
new_query = α × original_query + β × avg(relevant_docs) − γ × avg(non_relevant_docs)
```
Moves the query vector toward relevant documents and away from non-relevant ones.

## Related Concepts

- [[Relevance Feedback]] — concept note with modern implementations
- [[Query Expansion]] — PRF is a specific form of query expansion
- [[Click Signals]] — the primary source of implicit feedback in production
- [[Position Bias]] — corrupts click-based implicit feedback
- [[Presentation Bias]] — limits which documents can generate feedback
- [[Learning to Rank]] — implicit feedback used as LTR training signal
