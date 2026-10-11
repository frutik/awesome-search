---
title: "rerank-3 and rerank-3-lite - the next generation of Voyage rerankers"
type: article
tags: [article, reranking, vendor-blog, benchmark, model-release]
source: "https://blog.voyageai.com/2026/09/30/rerank-3/"
author:
  - "[[Voyage AI]]"
published: 2026-09-30
created: 2026-10-11
concepts:
  - "[[Reranking]]"
  - "[[Cross-Encoder]]"
  - "[[Retrieval Pipeline]]"
  - "[[NDCG]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[BM25]]"
topics:
  - "[[Reasoning Reranking]]"
companies:
  - "[[Voyage AI]]"
  - "[[Cohere]]"
  - "[[MongoDB]]"
  - "[[Jina AI]]"
  - "[[Mixedbread]]"
tools:
  - "[[Voyage rerank-3]]"
  - "[[Jev]]"
datasets:
  - "[[LongEmbed]]"
  - "[[MAIR]]"
---

# rerank-3 and rerank-3-lite - the next generation of Voyage rerankers

**Source:** https://blog.voyageai.com/2026/09/30/rerank-3/
**Publisher:** [[Voyage AI]] (contributors: Tengyu Ma, project advisor; Minghan Li, project lead; with the Voyage team at [[MongoDB]]) · 2026-09-30
**Detailed results:** [spreadsheet](https://docs.google.com/spreadsheets/d/1rGzFkGERw6WDAWRuLrtG6AWlejn0T9Bb_vHPJA9_4cA/edit?gid=1684416114#gid=1684416114)

## Summary

Launch post for **[[Voyage rerank-3|rerank-3 and rerank-3-lite]]**, successors to rerank-2.5 and rerank-2.5-lite (released August 2025). They use an updated backbone and a revised training-data mix. Price, API, 32K-token context and instruction-following are unchanged. The stated motivation is a shift in traffic: **coding agents now issue many of the queries**, and the documents being reranked are getting longer. Those are the two areas with the largest gains.

All figures are Voyage's own, measured on Voyage's own evaluation suite.

## Setup

- **95 datasets across 9 domains:** technical docs, code, law, finance, web reviews, multilingual (51 datasets, 31 languages), long documents, medical, conversations. Instruction-following is evaluated on [[MAIR]] (123 tasks).
- **Four first stages,** each retrieving up to 100 candidates: [[BM25]], OpenAI text-embedding-3-large, voyage-3-large, voyage-4-large. The reranker reorders them, and NDCG@10 is reported.
- **Baselines:** rerank-2.5 / -lite, [[Cohere]] Rerank v4.0 Pro and Fast, Qwen3-Reranker-8B, [[Jina AI|Jina]] Reranker v3.5, [[Mixedbread|mxbai]]-rerank-large-v2, NVIDIA Llama-Nemotron Rerank 1B v2.

## Results (averaged over the four first stages)

| Comparison | rerank-3 | rerank-3-lite |
|---|---|---|
| vs Cohere Rerank v4.0 Pro | +2.72% | +2.23% |
| vs Cohere Rerank v4.0 Fast | +5.74% | +5.25% |
| vs Qwen3-Reranker-8B | +3.02% | +2.53% |
| vs own predecessor (2.5 / 2.5-lite) | +0.96% | +1.10% |

- **Lift over the first stage:** +7.65% NDCG@10 over voyage-3-large, +6.38% over voyage-4-large, +16.67% over OpenAI v3 large, +20.33% over BM25. The weaker the first stage, the more a reranker adds.
- **Long documents ([[LongEmbed]]):** rerank-3 beats rerank-2.5 by 3.35% and Cohere v4.0 Pro by 13.84%. The gains come from NarrativeQA (+3.77%) and QMSum (+6.20%). Every Voyage reranker scores above 99% on SummScreenFD, so that subset no longer separates models.
- **Code** (DS-1000, APPS, CodeChef C++, RepoBench Java, WikiSQL): rerank-3 beats rerank-2.5 by about 2.1–2.2%, and rerank-3-lite beats rerank-2.5-lite by about 3.6–3.7%.
- **Multilingual:** small gains (+0.52% over rerank-2.5, +1.19% over Cohere Pro).
- **Instruction-following:** on par with rerank-2.5 on MAIR, and +3.58% over Cohere Pro.
- **rerank-3-lite** roughly matches rerank-2.5 at 40% of the price. It also beats Qwen3-Reranker-8B, which the post calls the leading open-weights reranker and says is over ten times larger.

## Against Jev

Across 26 datasets, rerank-3 led [[Jev]] 1.13 by 1.77, 5.69 and 5.87 NDCG@10 *points* in code, law and finance. Jev ran in score mode with no prompt tuning. It was not a full evaluation, because of Jev's rate limits. The comparison is vendor-run on expertise-heavy domains, untuned and partial. Published work has shown Jev's default prompt to be a lower bound ([[Adapting Jev to Your Domain with GEPA]]).

## Reading It

- **Score calibration is held across versions.** Relevance scores are calibrated to match the score distributions of the corresponding 2.5 models, so thresholds tuned on rerank-2.5 still work. This is a less common promise than accuracy. It treats the score as an operational contract, which is the property at issue in [[Calibrated Relevance Probability]].
- **The headline gains are relative percentages on a vendor suite.** The post reports them only as domain averages; per-dataset numbers are in the linked spreadsheet. Two of the four first stages are Voyage's own embedding models. The post's closing claim that Voyage embeddings plus Voyage rerankers give "the highest possible retrieval accuracy" is marketing, not a finding.
- **The model name predates the launch.** [[Hev meets Jev]] (published 2026-09-16) already benchmarked a "Voyage rerank-3" two weeks before this announcement. The post does not explain this.

## Pricing and Availability

$0.05 (rerank-3) and $0.02 (rerank-3-lite) per million tokens, the same as the 2.5 series, which stays available. The first 200M tokens are free. Both are also served inside [[MongoDB]] Atlas, through the Embedding and Reranking API and native reranking in Atlas Vector Search.

## Related Concepts

- [[Reranking]] · [[Cross-Encoder]] · [[Retrieval Pipeline]] — the second stage being upgraded
- [[NDCG]] — the reported metric
- [[Calibrated Relevance Probability]] — score distributions kept stable across model versions
- [[BM25]] — the first stage that gains most from reranking

## Related Notes

- [[Voyage rerank-3]] · [[Voyage AI]] · [[MongoDB]]
- [[Cohere]] · [[Jina AI]] · [[Mixedbread]] — competing rerankers in the comparison
- [[Jev]] · [[Hev meets Jev]] — the other published rerank-3 vs Jev comparison, on [[BEIR]]
- [[LongEmbed]] · [[MAIR]]
- [[Reasoning Reranking]]
