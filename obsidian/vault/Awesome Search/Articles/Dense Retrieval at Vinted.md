---
created: 2026-06-29
type: article
tags: [article, vespa, dense-retrieval, two-tower, clip, hybrid-search, ann, e-commerce, company-blog]
source: "https://vinted.engineering/2025/11/18/dense-retrieval/"
author: ["Laurynas Jasiukėnas", "Dainius Jocas"]
published: 2025-11-18
company: [Vinted]
concepts: [Dense Vector Retrieval, Bi-Encoder, Multimodal Embeddings, Hybrid Search, HNSW]
topics: [E-commerce Search, Personalization in Search]
---

# Dense Retrieval at Vinted

**[[Laurynas Jasiukėnas]] & [[Dainius Jocas]]**, Vinted Engineering, 2025-11-18.

How [[Vinted]] added semantic [[Dense Vector Retrieval|dense retrieval]] to its [[Vespa]] search stack — as a **hybrid augmentation** of lexical search, not a replacement.

## Two-Tower Model

A [[Bi-Encoder|two-tower]] architecture, both towers emitting **256-dim** vectors:

- **Query tower** — frozen **multilingual [[Multimodal Embeddings|CLIP]] base** + a trainable projection head (GELU, LayerNorm) fine-tuning for search.
- **Item tower** — fuses categorical embeddings (brand, category, …), **visual features from the primary product image** (512D CLIP → projected to 256D), and metadata through a fusion layer.

## Hybrid, Not Replacement

Dense retrieval **supplements** keyword matching rather than replacing it: ANN candidates are merged into the lexical results, with the number of dense matches added to the top-K **capped** to protect result quality (avoid flooding users with approximate matches). See [[Hybrid Search]].

## Training

- Contrastive learning, **7,000–10,000 negatives per positive pair**
- Scaled to **>100 million positive pairs**
- Learnable temperature, mixed-precision (FP16), AdamW, cosine-annealing schedule

## Serving on Vespa

- [[HNSW]] indices across **30 content nodes per group**, split into **three indices by market bloc**
- **500 ms latency budget** with a retry strategy: **350 ms approximate + 150 ms exact fallback**
- Dynamic threshold tuning to balance approximate vs. exact NN
- **GraalVM + ZGC** garbage collection cut tail latencies by double-digit percentages
- **<0.02% error rate**

## Results

First experiments in 2022; full rollout after **~50 A/B tests**. Dense retrieval improved **recall in low-result sessions** and lifted overall search metrics (no specific conversion/revenue figures disclosed).

## Why It Matters

A production blueprint for **multimodal hybrid retrieval** at marketplace scale: a frozen-CLIP two-tower fused with visual + categorical features, ANN as a capped supplement to lexical, and the operational detail (latency budget with exact fallback, GraalVM/ZGC) that makes it viable. Completes the Vinted Vespa arc: platform migration → ranking (`match-features`) → semantic retrieval.

## Related Concepts

[[Dense Vector Retrieval]] · [[Bi-Encoder]] · [[Multimodal Embeddings]] · [[Hybrid Search]] · [[HNSW]] · [[Vespa]]

## Related Notes

- [[Adopting Vespa for Recommendation Retrieval at Vinted]] — Vinted's earlier two-tower ANN work (recommendations)
- [[Vinted - Migrating Search from Elasticsearch to Vespa]] — the platform this runs on
- [[Optimizing Vespa Latency with Match-Features at Vinted]] — the ranking layer

## People

- [[Laurynas Jasiukėnas]] · [[Dainius Jocas]] — [[Vinted]]
