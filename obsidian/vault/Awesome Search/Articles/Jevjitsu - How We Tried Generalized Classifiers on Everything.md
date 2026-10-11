---
title: "Jevjitsu - How We Tried Generalized Classifiers on Everything"
type: article
tags: [article, reranking, diversity, query-understanding, chunking, rag, vendor-blog]
source: "https://qdrant.tech/blog/jevjitsu/"
author:
  - "[[Andrei Cristea]]"
  - "[[Chadha Sridi]]"
published: 2026-10-08
created: 2026-10-11
concepts:
  - "[[Reranking]]"
  - "[[MMR]]"
  - "[[Query Understanding]]"
  - "[[Text Chunking]]"
  - "[[Cross-Encoder]]"
  - "[[Hybrid Search]]"
  - "[[System One Model]]"
  - "[[RAG]]"
topics:
  - "[[Reasoning Reranking]]"
  - "[[Search Result Diversity]]"
  - "[[Query Classification]]"
companies:
  - "[[Qdrant]]"
  - "[[TypeSafe]]"
tools:
  - "[[Jev]]"
  - "[[Qdrant Vector DB]]"
datasets:
  - "[[BEIR]]"
  - "[[WANDS Dataset]]"
  - "[[QASPER]]"
---

# Jevjitsu - How We Tried Generalized Classifiers on Everything

**Source:** https://qdrant.tech/blog/jevjitsu/
**Authors:** [[Andrei Cristea]] & [[Chadha Sridi]] ([[Qdrant]]) · 2026-10-08
**Code:** the `many-jev-recipies` repository and per-experiment notebooks linked from the post

## Summary

Qdrant treats [[Jev]] as a **general-purpose classifier** and runs it against four search decisions, not just reranking. The post places it in a taxonomy of classifiers. A trained task classifier is fast but needs labels. A zero-shot NLI or label-embedding classifier is fast and accepts new labels. A prompted LLM is slow and not constrained to the labels by default. Jev needs no training, accepts new labels at runtime, is constrained to them by design, and is fast. The authors call this "describe it, don't train it". They also present it as part of a move away from "LLM is all you need" toward concrete methods.

Their own summary is that Jev's most interesting uses came **after** reranking.

## 1. Reranking

The authors note that benchmarking Jev as a reranker on a few hundred queries has become "a rite of passage" for search vendors. They tested 100 NFCorpus ([[BEIR]]) queries, reranking the top 30 and top 50 candidates from Qdrant with BGE-small, using three call shapes. **Score** judges each document on its own in one request. **Choice** asks "which doc is most relevant?" once over all documents. **Iterative** asks that question once per rank position, removing each winner (10 requests for a top 10).

| Method | Requests/query | nDCG@10 lift, top 30 | lift, top 50 |
|---|---|---|---|
| Jev Score | 1 | +0.0665 | +0.0741 |
| Jev Choice | 1 | +0.0583 | +0.0673 |
| Jev Iterative | 10 | +0.0746 | +0.0789 |
| ms-marco-MiniLM-L-6-v2 ([[Cross-Encoder]]) | local | +0.0313 | +0.0258 |
| bge-reranker-base | local | −0.0015 | −0.0127 |

All three Jev shapes beat both local cross-encoders, and they sit within 0.02 of each other. Iterative wins by too little to justify ten requests, so **Score is their default**.

## 2. Reducing Repetitive Results

On 240 held-out [[WANDS Dataset|WANDS]] queries, they measured relevance (nDCG@10), near-duplicate pairs per page (embedding similarity ≥ 0.95) and distinct product classes in the top 10:

| Pipeline | nDCG@10 | Near-dup pairs/page | Product classes |
|---|---|---|---|
| Hybrid search | 0.683 | 1.27 | 3.17 |
| Qdrant [[MMR]], diversity 0.5 | 0.561 | 0.00 | 4.74 |
| Jev rerank | **0.769** | 1.25 | 2.41 |
| Jev score inside MMR, diversity 0.7 | 0.719 | 0.22 | 3.40 |
| MMR (0.5), then Jev rerank of top 20 | 0.723 | 0.04 | 3.12 |

Jev reranking improved relevance but **narrowed variety**. Even ordering by the human labels gave only 2.66 product classes: relevant results can still be repetitive. MMR removes duplicates but costs 0.12 nDCG@10, because it measures relevance as vector similarity to the query. The fix is to **use the reranker's score as MMR's relevance term**, or run MMR first and let Jev rerank its output. Both beat hybrid search on relevance *and* repetition.

## 3. Query Understanding

Following [[Doug Turnbull]]'s rule to filter only when very sure and otherwise boost, they classify queries into product categories. Category names taken directly from products gave almost no gain. What worked was **clustering products, having a cheap LLM name each cluster, and using Jev to check the names**. After that nothing is generated, only categorized:

- **Index time:** Jev tags each product with categories, stored as Qdrant payload.
- **Query time:** Jev scores each category against the query. At **≥ 0.9** search filters to that category. At **0.5–0.9** it boosts matching products. Below 0.5 it does nothing. Filtering is a payload filter and boosting is a score formula over hybrid search.

On 300 Amazon-C4 searches, this tiered setup worked best, and every setup beat plain hybrid search on average. Filtering on every guess was within noise. Jev adds 0.5–2 s per query depending on how many categories it reads. Small classifiers trained on Jev's product tags handled 37% of queries with boosts only, skipping Jev, at slightly higher average nDCG@10.

The caveat is the useful part. Amazon-C4 queries are long and LLM-generated, while real queries are short. In unlabelled spot checks, *apple* filtered to Food & Beverage at 0.91, just past the threshold, which wiped out the MacBook, the apple tree and the laptop decal. *kitchen faucet replacement* → Plumbing Parts (0.98) helped. *running shoes that aren't nike* got the right category, but a category cannot express "not Nike". **A confident category prediction can still miss intent, and a filter cannot be undone downstream.** Two fixes are proposed but untested: boost rather than filter on one- or two-word queries, and pass extra context such as the shop the query came from.

## 4. Semantic Chunking

Instead of cutting where neighbouring-sentence embeddings drift apart, Jev is shown a window of numbered sentences and asked, for each gap, whether the next sentence starts a new topic ("a new section, story, question or theme begins"). In their example, a section heading scored 0.97 and the two sentences after it 0.13 and 0.03. Cuts happen where the answer passes a threshold, within minimum and maximum chunk sizes. Because cuts are a pure function of the answers, **changing chunk size needs no new requests**.

On [[QASPER]] (407 papers, 1,297 questions with researcher-marked evidence), Qdrant retrieved five chunks per question. At matched mean chunk sizes, Jev beat fixed-size, recursive and embedding-based chunkers on character-level IoU (+13.0% average relative), precision (+11.2%) and recall (+9.1%), with every 95% CI excluding zero, on the first try and without tuning the question. The smallest gain was over a blank-line-first recursive splitter, because QASPER's answers are whole paragraphs. The cost is that the text goes to an API (about $0.27 per million document tokens), while the alternatives run locally for free.

## What They Would Try First

For [[RAG]], start with the chunker: it is easy to set up and adds nothing at query time. For product search, combine Jev's relevance scores with MMR. Query understanding has the most potential but needs testing on ambiguous queries before you trust a filter. Skip Iterative reranking. They point to OpenAI's Decisions API and to open-source OpenJev, JevLite and CLM as the industry exploring the same idea.

## Related Concepts

- [[Reranking]] · [[Cross-Encoder]] · [[Hybrid Search]]
- [[MMR]] — Jev's score swapped in as the relevance term
- [[Query Understanding]] · [[Results Boosting]] — tiered filter/boost by classifier confidence
- [[Text Chunking]] — boundary detection as a yes/no decision per sentence gap
- [[System One Model]] — the model class, framed as a generalized classifier
- [[Knowledge Distillation]] — small classifiers trained on Jev's product tags to skip it

## Related Notes

- [[Jev]] · [[TypeSafe]] · [[Qdrant]] · [[Qdrant Vector DB]]
- [[BEIR]] · [[WANDS Dataset]] · [[QASPER]]
- [[Bag of Decisions Reranker]] · [[Using Jev as a Search Reranker - Benchmarks and How to Implement]] — the same fortnight's other Jev reranking experiments
- [[Search Result Diversity]] · [[Query Classification]] · [[Reasoning Reranking]] · [[Reception of Jev]]

## People

- [[Andrei Cristea]] · [[Chadha Sridi]] · [[Doug Turnbull]] (cited for the filter-only-when-sure rule)
