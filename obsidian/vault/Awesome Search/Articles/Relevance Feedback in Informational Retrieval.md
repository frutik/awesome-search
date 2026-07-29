---
type: article
title: "Relevance Feedback in Informational Retrieval"
author: "[[Evgeniya Sukhodolskaya]]"
company: "[[Qdrant]]"
published: 2025-03-27
source: "https://qdrant.tech/articles/search-feedback-loop/"
tags:
  - article
  - relevance-feedback
  - query-expansion
  - ir-foundations
  - literature-survey
topics:
  - "[[Query Understanding in Practice]]"
concepts:
  - "[[Relevance Feedback]]"
  - "[[Query Expansion]]"
  - "[[Reranking]]"
  - "[[Cross-Encoder]]"
  - "[[Dense Vector Retrieval]]"
  - "[[ColBERT]]"
created: 2026-07-29
---

# Relevance Feedback in Informational Retrieval

📄 **Source:** https://qdrant.tech/articles/search-feedback-loop/

## Summary

A survey of the [[Relevance Feedback]] literature, organised as a two-axis taxonomy, written to answer one question: the methods have existed for sixty years, so why is there no production-grade relevance feedback in neural search? The answer it lands on — that researchers can't reach inside the retrieval system, so the whole field is pushed toward query rewriting — is the premise for the mechanism built a year later in [[Relevance Feedback in Qdrant]].

## Axis 1 — Who Gives Feedback, and How Granular

| Type | Definition | The catch |
|---|---|---|
| **Pseudo-relevance feedback** | Assume the top-ranked results are relevant | *"Provides a noticeable performance boost in lexical retrieval while being relatively cheap to compute"* — but drifts when the first pass is poor |
| **Binary relevance feedback** | A user or classifier marks yes/no | Users won't do it (Google removed its upvote/downvote feature through disuse), and relevant documents may be absent from the initial results entirely |
| **Re-scored relevance feedback** | An ML model assigns graded relevance scores | *"How accurately can the automated judge determine relevance"*, and can you afford to run it |

The third is where the modern work sits, and it's what [[Qdrant]]'s later mechanism assumes.

## Axis 2 — What the Feedback Changes

Retrieval has three ingredients: query, documents, and similarity scoring. Rewriting documents per request is impractical at scale, which leaves two paths.

### Query refinement

**As text** — expand the query with terms:

- **RM3 (relevance models)** — picks expansion terms by probability in pseudo-relevant documents weighted by query likelihood. *"Still appearing in papers of the last few years as a (noticeably decent) baseline."*
- **BERT-QE** — a fine-tuned BERT reranker scores query–chunk relevance in pseudo-relevant documents; top chunks expand the query. **+11% NDCG@20 for 11.01× the computation** of just using BERT to rerank — the cost/benefit problem in one line.
- **ANCE-PRF, ColBERT-PRF** — fine-tuned query encoders that ingest feedback documents and emit an adjusted query embedding. They *"struggle with generalization, performing poorly on out-of-domain tasks."*

**As vector** — move the query point directly:

- **Rocchio (1965)** — *"update the query vector by adding a difference between the centroids of relevant and non-relevant documents."* The parametrized version for dense retrieval consistently improves Recall@1000 by 1–5%.
- **TOUR** — test-time optimization of query representations: repeated *retrieve → rerank → gradient descent* cycles guided by a reranker.
- **ReFit (2024)** — one iteration instead of many; matches retriever and [[Cross-Encoder]] similarity distributions via KL divergence. Stably improves Recall@100 by 2–3%.

See [[Query Expansion]] and [[Query Understanding - Query Rewriting Overview]] for the vault's coverage of this path.

### Similarity scoring adjustment

- **kNN-based scoring** — add the summed similarity between a candidate and all known relevant examples to its query score. Worth ~5.6 pp NDCG@20, but needs explicit user-labeled feedback.
- **Reranker fine-tuning** — either train rerankers offline to take feedback as extra inference input, or fine-tune a cross-encoder's bias parameters per query on 2–8 feedback documents.

The structural limit: these *"cannot retrieve relevant documents beyond those returned in the initial search."* See [[Reranking]].

## The Argument: Why Neural Search Has No Answer

Lexical retrieval adopted PRF decades ago. Vector search has nothing industry-adopted — *"neural search-compatible methods remain stuck in research papers."* The article's diagnosis is not that the methods are unknown:

> *"Researchers have no direct access to retrieval systems, forcing them to design wrappers around the black-box-like retrieval oracles. This is sufficient for query-adjusting methods but not for similarity scoring function adjustment."*

That access asymmetry explains the shape of the literature. Query rewriting is over-represented because it's the only thing you can do from outside; scoring-function work is rare because almost nobody owns an index. The remaining barriers are practical — query drift, hyperparameter sensitivity, feedback volume, and cost.

Its stated requirement for a real solution:

> *"A real-world solution should be simple… It shouldn't require fine-tuning thousands of parameters or feeding paragraphs of text into transformers. And for it to be effective, it needs to be integrated directly into the retrieval system itself."*

Read as a research agenda, the last clause is the whole point — and [[Relevance Feedback in Qdrant]] is the follow-through.

## Related

- Concept: [[Relevance Feedback]] — this article is the taxonomy behind that note's structure
- Sequel: [[Relevance Feedback in Qdrant]] — same author; the index-native mechanism this argues for
- Talk: [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] — where she cites this survey from stage
- [[Query Expansion]] · [[Query Understanding - Query Rewriting Overview]] — the query-refinement path
- [[Reranking]] · [[Cross-Encoder]] — the scoring path's usual ceiling
- [[Query Understanding - Relevance Feedback]] — [[Daniel Tunkelang]]'s shorter treatment of the same taxonomy
- [[Dense Vector Retrieval]] · [[HNSW]] — where the gap is
