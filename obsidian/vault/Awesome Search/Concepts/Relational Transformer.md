---
type: concept
title: "Relational Transformer"
aliases: ["RT", "Relational Transformer reranker"]
tags:
  - concept
  - reranking
  - relational-deep-learning
  - learning-to-rank
created: 2026-08-28
---

# Relational Transformer

## Definition

The Relational Transformer (RT) is a transformer architecture — implemented by [[RelativeDB]] at 85M parameters for search reranking — that conditions directly on structured relational data (typed fields and their schema relationships) rather than converting candidates to text first. It's positioned as a reranking-stage model: it operates on a candidate set already produced by retrieval, and rescores that set using structured facts a text-only reranker would otherwise discard (price/stock conditions, personalization, recent purchase signals).

## Cells: The Input Representation

RT's unit of input is a **Cell** — a `(name, type, value)` triple, e.g. `products.price: float = 38.00`. The field name carries semantic meaning and the declared type shapes how the value is read. Database rows act as graph nodes linked by typed schema relationships (e.g. an `also_buy` Cell pointing from one product row to another); a scoring context for a given query gathers candidate Cells plus query-derived facts pulled from selected linked rows — a bounded, schema-aware context rather than an unbounded free-text one.

## Why Structure Helps: RelBench Precedent

The case for conditioning on relational structure rather than text predates RT: on [[RelBench]], relational deep learning systems that learn across primary/foreign-key links matched or beat tuned tabular-model baselines on 11 of 15 tasks, because the models gain access to fields outside the target table. RT's Cell-based attention brings that same cross-table structure into the reranking setting.

## Sensitivity to Context (Ablations)

Removing structure degrades RT's accuracy in a graded way: full-context zero-shot regression reached 22.8 mean R²; dropping schema names (keeping values but losing field semantics) fell to 20.5; dropping the target entity's own history fell to -5.5. The reranking analogue of this test removes a single product field or an entire linked-row group and measures the resulting drop in held-out [[NDCG]].

## Query Parsing Is Load-Bearing

Feeding RT a long free-text query degrades it toward the quality of the underlying embedding retriever, because the surrounding context loses structure. [[RelativeDB]] addresses this with an LLM query-parsing step that converts free text into candidate database Cells and resolves vague semantic terms ("cheap", "popular") into concrete values. This reportedly doubled model accuracy over unparsed text, and parsing into a known schema made RT competitive with an LLM reranker roughly 7x its parameter count.

## Benchmark Results

- **MTEB DeepPlanning** (product-search slice): a MiniLM embedding retriever alone scored 0.286 NDCG@10; RT, trained on 87 queries, reached 0.633 NDCG@10 across 24 held-out queries over all 4,047 candidates.
- **[[STaRK]]**: on an Amazon co-purchase graph, adding the `also_buy` relational edge into a candidate's context moved the correct product from rank #2 (under title similarity alone) to rank #1.
- On a FLOPs-per-query vs. NDCG@10 comparison, RT is positioned ahead of MiniLM retrieval/cross-encoders and BERT cross-encoders, and comparable in quality — at substantially lower inference cost — to [[RankLLaMA]]-7B and a GPT-4 listwise reranker.

## Related Concepts

- [[Reranking]] — the pipeline stage RT operates at
- [[Learning to Rank]] — the broader family RT sits within, distinguished by conditioning on relational structure instead of engineered scalar features
- [[NDCG]] — the metric used to evaluate RT
- [[RankLLaMA]] — LLM reranker RT is benchmarked against for quality-per-FLOP
- [[ColBERT]] — ColBERTv2 is used as a comparison point on RT's FLOPs/quality chart

## Datasets

- [[RelBench]] — precedent benchmark motivating relational conditioning over tabular features
- [[STaRK]] — benchmark used to demonstrate relational-edge reranking

## Companies

- [[RelativeDB]]

## Articles

- [[Relational Reranking - Scoring Search Results with Structured Facts]] — source article introducing RT

## People

- [[Daniel Henneberger]]
