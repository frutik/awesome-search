---
title: "Using Jev as a Search Reranker - Benchmarks and How to Implement"
type: article
tags: [article, reranking, e-commerce, hybrid-search, benchmark, vendor-blog]
source: "https://www.elastic.co/search-labs/blog/ecommerce-search-reranking-llm-alternative-jev"
author:
  - "[[Dustin Coates]]"
published: 2026-09-30
created: 2026-10-11
concepts:
  - "[[Reranking]]"
  - "[[Hybrid Search]]"
  - "[[Reciprocal Rank Fusion]]"
  - "[[ESCI Label Scheme]]"
  - "[[NDCG]]"
  - "[[MRR]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[Pointwise Relevance Evaluation]]"
topics:
  - "[[Reasoning Reranking]]"
  - "[[E-commerce Search]]"
companies:
  - "[[Elastic]]"
  - "[[TypeSafe]]"
tools:
  - "[[Jev]]"
  - "[[Elasticsearch]]"
datasets:
  - "[[Amazon ESCI Dataset]]"
---

# Using Jev as a Search Reranker - Benchmarks and How to Implement

**Source:** https://www.elastic.co/search-labs/blog/ecommerce-search-reranking-llm-alternative-jev
**Author:** [[Dustin Coates]] ([[Elastic]] Search Labs) · 2026-09-30
**Code:** [companion notebook](https://github.com/elastic/elastic-labs/blob/main/supporting-blog-content/ecommerce-search-reranking-llm-alternative-jev/ecommerce-search-reranking-llm-alternative-jev.ipynb)
**Model:** `jev-1.13.0`

## Summary

[[Elasticsearch]] retrieves, [[Jev]] judges each query/product pair, and a **small deterministic Python policy** turns those judgments into the final order. On 250 US-English queries from the [[Amazon ESCI Dataset|Shopping Queries Dataset]], the best policy raised nDCG@10 from **0.9351** (hybrid search) to **0.9565**, and Exact [[MRR]] from 0.9201 to as high as 0.9616.

The author argues the architecture matters more than the lift. Jev returns typed decisions and probabilities, so **the application decides what "relevant" means** and weights the probabilities to fit its goals, rather than accepting one opaque score.

## Setup

- **Retrieval:** a product index with separate display fields plus a combined `product_text` field duplicated into a `semantic_text` field (`.jina-embeddings-v5-text-small` via Elastic Inference Service). Lexical `multi_match` (title^4, brand^2, bullet_points^2, description^0.5) and semantic retrievers are fused with the RRF retriever (`rank_window_size` 100, `rank_constant` 60).
- **Benchmark design:** reranking is evaluated **separately from retrieval**. Every strategy receives the same complete, human-judged candidate group from the dataset (about 19 products per query), so differences measure ordering, not recall.
- **Split:** 50 training-split queries for development. Questions, model, endpoints and policy were then frozen before a 250-query test run over 4,754 judged pairs.
- **What Jev sees:** the query plus title, brand, colour, bullet points and description. It does not see the product ID, Elasticsearch score, label or original position.

## The Questions

- A **Choice** over the four [[ESCI Label Scheme|ESCI]] relationships (exact / substitute / complement / irrelevant), returning a probability for each.
- Four **Noul** signals in the same call: `requested_item` (the main item, not an accessory), `explicit_constraints` (every stated constraint supported), `same_core_purpose`, and `compatibility_supported`.
- Separately, a single **Score** with an ordered four-level rubric.

## Four Policies

| Policy | Score |
|---|---|
| Exact probability | P(exact) alone |
| Relationship expected utility | 1.00·P(exact) + 0.55·P(substitute) + 0.15·P(complement) |
| Composite | expected utility × (0.60 + 0.40·requested_item) × (0.70 + 0.30·explicit_constraints), × (0.60 + 0.40·compatibility) when code detects compatibility language ("fits", "works with", "replacement") |
| Direct Score | expected value of the single ordered Score question |

The composite caps each discount (at most 40% for an accessory) so that incomplete product metadata cannot sink a result. `same_core_purpose` was collected but left out because it overlaps the relationship Choice. The utility weights are the author's own and were barely tuned.

## Results

| Strategy | nDCG@10 | Δ vs hybrid (95% CI) | Random-to-perfect gap captured | Exact MRR |
|---|---|---|---|---|
| Jev relationship expected utility | **0.9565** | +0.0214 [+0.0125, +0.0307] | 69.1% | 0.9550 |
| Jev direct Score | 0.9557 | +0.0206 [+0.0106, +0.0308] | 68.5% | 0.9457 |
| Jev composite | 0.9555 | +0.0204 [+0.0114, +0.0295] | 68.3% | 0.9559 |
| Jev exact probability | 0.9533 | +0.0182 [+0.0102, +0.0263] | 66.8% | **0.9616** |
| Hybrid (BM25 + semantic, RRF) | 0.9351 | baseline | 53.8% | 0.9201 |
| BM25 | 0.9234 | −0.0117 | 45.5% | 0.9015 |
| Random order | 0.8595 | −0.0756 | 0.0% | 0.7426 |

## Reading the Numbers

- **The random baseline is 0.86.** Of the judged pairs, 2,960 were Exact and only 439 Irrelevant. With that label mix, a random ordering is expected to score 0.8634 nDCG@10. That is why every absolute figure is high. The author proposes a follow-up on a judgment list with more irrelevant results.
- **All four policies land within 0.0032 of each other**, with overlapping confidence intervals. The one-question Score is nearly as good as the hand-built policies, so the extra signals bought little *on this metric*. Exact probability predictably wins Exact MRR.
- **The prose and the table disagree in two places.** The takeaways credit the composite policy with the best result, but the table puts relationship expected utility first. The pair count is given as both 4,754 and 4,716. The table is used here.
- **Calibrated uncertainty is visible in the output.** For *bts map of the soul 7* against a branded T-shirt, the Choice came back spread almost evenly (exact 0.25, complement 0.29, irrelevant 0.30, confidence 0.06), yet the held-out label was Exact. The author's point is that the distribution exposes ambiguity but Jev is not infallible ([[Calibrated Relevance Probability]]).
- **Prompt tuning was left on the table.** The criteria were not optimized, and the post points to GEPA's `optimize_anything` as a next step (cf. [[Adapting Jev to Your Domain with GEPA]]).

The conclusion is that ranking, like text relevance, benefits from **blending several scores** rather than using one directly. It comes with stated caveats: one test, one dataset, 250 queries, and labels skewed toward Exact.

## Related Concepts

- [[Reranking]] · [[Hybrid Search]] · [[Reciprocal Rank Fusion]]
- [[ESCI Label Scheme]] — the four relationships the Choice asks about, turned into an expected-utility score
- [[NDCG]] · [[MRR]] — the two metrics reported
- [[Pointwise Relevance Evaluation]] — one judgment per pair
- [[Calibrated Relevance Probability]] — what makes probability-weighted policies possible

## Related Notes

- [[Jev]] · [[TypeSafe]] · [[Elasticsearch]] · [[Elastic]]
- [[Amazon ESCI Dataset]]
- [[Bag of Decisions Reranker]] — several Jev questions per pair, but generated per query and summed
- [[Jevjitsu - How We Tried Generalized Classifiers on Everything]] — Qdrant's Jev reranking and beyond
- [[Hev meets Jev]] · [[TypeSafe Cookbook - Re-ranking]] — earlier Jev reranking benchmarks
- [[Reasoning Reranking]] · [[Reception of Jev]]

## People

- [[Dustin Coates]]
