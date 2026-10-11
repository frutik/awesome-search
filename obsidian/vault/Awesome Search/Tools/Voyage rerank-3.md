---
type: tool
title: "Voyage rerank-3"
aliases: ["rerank-3", "rerank-3-lite", "Voyage Rerank 3", "Voyage reranker"]
tags: [tool, reranking, model, api]
website: "https://docs.voyageai.com/"
company: "[[Voyage AI]]"
created: 2026-10-11
---

# Voyage rerank-3

[[Voyage AI]]'s hosted reranker family, launched 2026-09-30 in two sizes, **rerank-3** and the latency-optimized **rerank-3-lite** ([[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers|launch post]]). It succeeds rerank-2.5 and rerank-2.5-lite (August 2025) as a drop-in upgrade with the same API and price.

---

## Properties

| | rerank-3 | rerank-3-lite |
|---|---|---|
| Price | $0.05 / M tokens | $0.02 / M tokens |
| Context | 32K tokens per document | 32K tokens per document |
| Instruction-following | yes | yes |

- **Score calibration is preserved across versions.** Scores match the distributions of the corresponding 2.5 models, so existing thresholds keep working ([[Calibrated Relevance Probability]]).
- **Positioning:** largest gains on long documents and code, attributed to coding agents issuing more queries and to longer candidates.
- **Availability:** Voyage API (first 200M tokens free), and natively in [[MongoDB]] Atlas Vector Search.

## Evidence

Vendor-reported, averaged across four first-stage retrievers on 95 datasets: +2.72% NDCG@10 over [[Cohere]] Rerank v4.0 Pro and +3.02% over Qwen3-Reranker-8B. On [[LongEmbed]] the lead over Cohere Pro is +13.84%.

Independent: [[Hev meets Jev]] measured "Voyage rerank-3" at **0.504 mean nDCG@10** on three [[BEIR]] subsets over a [[BM25]] top-30. That is second only to [[Mixedbread]]'s mxbai-rerank-v3.1-listwise (0.511), and the cheapest of the hosted rerankers at $0.50 per 1,000 queries, with p50/p95 latency of 185/287 ms. That post predates the official launch by two weeks.

## Versus Jev

Two published comparisons point in the same direction by different margins. In Hev's [[BEIR]] run, untuned [[Jev]] trailed rerank-3 by 0.003 nDCG@10, with a much wider latency tail. Voyage's own run on 26 expertise-heavy datasets had rerank-3 ahead by 1.77 (code), 5.69 (law) and 5.87 (finance) NDCG@10 points. That run used untuned Jev and was cut short by rate limits.

## Related Concepts

- [[Reranking]] · [[Cross-Encoder]] · [[Retrieval Pipeline]]
- [[Calibrated Relevance Probability]]

## Related Notes

- [[Voyage AI]] · [[MongoDB]]
- [[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]] · [[Hev meets Jev]]
- [[Jev]] · [[Cohere]] · [[Jina AI]] · [[Mixedbread]]
- [[Reasoning Reranking]]
