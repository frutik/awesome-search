---
type: concept
title: "Query Rewriting"
aliases: ["query rewrite", "query reformulation", "query transformation", "query enrichment"]
tags:
  - concept
  - search
  - query-understanding
  - ranking
created: 2026-09-07
---

# Query Rewriting

## Definition

**Query rewriting** is the family of techniques that transform a user's original query into a different formulation better suited to what the search system can actually serve. It is the pivot point of [[Query Understanding]]: everything upstream works out what the user meant, and rewriting is where that interpretation is committed to an executable query.

The goal is always to close the gap between how the user expressed their intent and how the system can best satisfy it.

## Why Rewrite

Different rewriting strategies address different failure modes:

| Problem | Strategy | Related |
|---|---|---|
| Query too narrow — too few results | Add terms | [[Query Expansion]] |
| Query too specific — [[Zero Results]] | Drop or loosen terms | [[Query Relaxation]] |
| Equivalent expressions differ in surface form | Normalize | [[Synonyms]] |
| The query contains errors | Correct | [[Spelling Correction]] |
| Multi-word units are being tokenised wrongly | Group | [[Query Segmentation]] |

## How Rewrites Are Produced

Three broad sources, increasing in flexibility and decreasing in predictability:

- **Hand-crafted rules** — reliable for well-understood, high-traffic patterns.
- **Learned from logs** — historical query and click data mined for reformulations users make themselves.
- **Model-generated** — models trained on reformulation tasks. An agent holding user context can also produce the rewrite at query time; see the memory-driven case below.

## Measuring It

Impact has to be read across three quantities at once: **recall**, **precision**, and the **fraction of queries actually affected**. The governing constraint is that rewriting which helps the tail must not damage the head — a rewrite that rescues rare queries while degrading the most common ones is a net loss, and aggregate metrics can easily hide that.

## Personalized and Memory-Driven Rewriting

Rewriting is also the natural place to apply per-user context. In the [[Agentic Memory]] pattern, preferences held in memory are injected into the query itself — `backpack` becomes `backpack leather neutral professional` — so that personalization happens before retrieval rather than as a re-ordering afterwards. This shifts rewriting from a static, corpus-level transformation to a per-user one.

Two practical constraints surface in that setting:

- **Prefer soft signals to hard filters** when the rewrite is driven by inferred preference rather than explicit user input, since a preference is evidence rather than a constraint.
- **Express negative preferences affirmatively** where the rewritten query feeds an embedding model, because such models handle negation poorly.

Because a rewrite can lose information the ranker still needs, the same context is often supplied to the [[Reranking|rerank]] stage as well.

## Related Concepts

- [[Query Understanding]] — the broader stage rewriting belongs to
- [[Query Expansion]] · [[Query Relaxation]] · [[Synonyms]] · [[Spelling Correction]] · [[Query Segmentation]] — specific rewriting strategies
- [[Zero Results]] — the failure rewriting most often exists to prevent
- [[Agentic Memory]] — memory-driven, per-user rewriting
- [[Reranking]] — where context lost in the rewrite can be recovered
- [[Personalization]] — rewriting as a personalization mechanism

## Articles

- [[Query Understanding - Query Rewriting Overview]] — [[Daniel Tunkelang]]'s overview, part of the Query Understanding series

## Videos

- [[Hajer Bouafif - Personalize Search Results with OpenSearch Agentic Memory]] — memory-driven query enrichment in [[OpenSearch]]

## Topics

- [[Query Understanding in Practice]]
