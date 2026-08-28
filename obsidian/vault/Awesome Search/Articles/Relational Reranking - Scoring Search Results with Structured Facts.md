---
type: article
title: "Relational Reranking: Scoring Search Results with Structured Facts"
source: "https://relativedb.com/research/relational-reranking"
author:
  - "[[Daniel Henneberger]]"
published: 2026-08-11
created: 2026-08-28
concepts:
  - "[[Relational Transformer]]"
  - "[[Reranking]]"
topics: []
companies:
  - "[[RelativeDB]]"
datasets:
  - "[[RelBench]]"
  - "[[STaRK]]"
tags:
  - article
  - reranking
  - relational-deep-learning
  - e-commerce
  - company-blog
---

# Relational Reranking: Scoring Search Results with Structured Facts

[[Daniel Henneberger]] of [[RelativeDB]] presents **RT**, an 85-million-parameter [[Relational Transformer]] that reranks e-commerce search candidates directly from structured product data instead of treating candidates as text. The pitch: enterprise search queries often carry structured conditions ("goggles under $50"), personalization needs, and recent purchase signals that a text-only reranker discards; RT instead selects typed data from a "context graph," parses the query into structured facts, and conditions the transformer on that structured context.

## Cells: The Structured Input Unit

RT represents each structured fact as a **Cell** — a `(name, type, value)` triple, e.g. `products.price: float = 38.00`. The field name supplies semantic meaning; the declared type shapes how the model reads the value. Rows act as graph nodes connected by typed schema relationships — an `also_buy` Cell can point from one product row to a linked product row — so a scoring context gathers candidate Cells plus query-derived facts from selected linked rows.

## Ablations

The article reports RT achieving 22.8 mean R² across zero-shot regression tasks with full context; removing schema names dropped this to 20.5, and removing the target entity's own history dropped it to -5.5. Applied to reranking, the analogous test measures held-out [[NDCG]] after removing a product field or an entire linked-row group.

## Query Parsing Matters as Much as the Model

Long free-text queries degrade RT toward the accuracy of the underlying embedding retriever and whatever context happens to be present. RelativeDB adds an LLM query-parsing step that converts a query into candidate database Cells and adds semantic context (e.g. what "cheap" or "popular" should resolve to numerically). Converting free text into arbitrary Cells reportedly doubled model accuracy; parsing into a known schema made RT competitive with an LLM reranker roughly 7x its parameter count.

## Benchmarks

- **[[RelBench]]**: relational deep learning systems matched or beat tuned [[LightGBM]]-style models on 11 of 15 tasks by learning across primary/foreign-key links, giving access to fields outside the target table — the architectural premise RT's Cell attention builds on.
- **MTEB DeepPlanning** (product-search portion): a MiniLM embedding retriever scored 0.286 NDCG@10; training RT on 87 queries brought it to 0.633 NDCG@10 across 24 held-out queries over all 4,047 candidates.
- **[[STaRK]]**: using an Amazon product graph recording frequent co-purchases, RT resolves a named product to its row, adds the `also_buy` edge into the candidate context, and uses it to move a matching product from rank #2 (under title-similarity alone) to rank #1.
- On a chart plotting inference FLOPs per query against NDCG@10, the article positions RT's quality/cost tradeoff ahead of MiniLM retrieval, [[ColBERT|ColBERTv2]], MiniLM/BERT cross-encoders, and Qwen3-Reranker-0.6B, and comparable in quality (at far lower FLOPs) to [[RankLLaMA]]-7B and a GPT-4 listwise reranker.

## Sourcing

Cites prior work including [[XGBoost]] (Chen & Guestrin, 2016), passage reranking with BERT (Nogueira & Cho, 2019), [[ColBERT|ColBERTv2]] (Santhanam et al., NAACL 2022), RelBench (Robinson et al., 2024), STaRK (Wu et al., NeurIPS 2024), and the Relational Transformer architecture paper (Ranjan et al., ICLR 2026) that RT builds on. Code released as `stanford-star/rt-j`, described as the pretrained checkpoint used in this work.

## Related Concepts

- [[Relational Transformer]] — the model architecture this article introduces applying to reranking
- [[Reranking]] — the pipeline stage RT occupies
- [[NDCG]] — evaluation metric used throughout

## Datasets

- [[RelBench]] · [[STaRK]]

## Companies

- [[RelativeDB]]

## People

- [[Daniel Henneberger]]
