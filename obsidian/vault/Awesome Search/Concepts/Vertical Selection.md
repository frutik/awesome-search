---
type: concept
title: "Vertical Selection"
aliases: ["vertical prediction", "aggregated search", "vertical intent", "vertical triggering"]
tags:
  - concept
  - query-routing
  - federated-search
  - web-search
related_concepts:
  - "[[Query Routing]]"
  - "[[Federated Search]]"
  - "[[Query Classification]]"
created: 2026-09-26
---

# Vertical Selection

## Definition

Predicting which specialised search services — **verticals** such as news, images, video, local, shopping or travel — are relevant to a query typed into a general search box, **including the answer "none"**, so their results can be blended into the main results page. The blended page is **aggregated search**; vertical selection is its first and decisive step.

It is the web-search ancestor of [[Query Routing]], and a *cooperative* case of [[Federated Search]] resource selection: the search engine owns every vertical, so it has access to evidence an uncooperative federation never sees — above all, each vertical's own query log.

## Evidence

From [[Sources of Evidence for Vertical Selection]] ([[Jaime Arguello]], [[Fernando Diaz]], [[Jamie Callan]], Crespo — SIGIR 2009):

| Evidence | Examples |
|---|---|
| **Query string** | Trigger words ("news", "pictures"), geographic terms |
| **Vertical query logs** | Likelihood of the query under a language model of queries users typed directly into that vertical |
| **Vertical corpora** | Resource-selection scores (ReDDE, Clarity) over sampled vertical content, or Wikipedia proxies for text-poor verticals |

Query-log evidence was the strongest single predictor; a supervised classifier combining all three was best.

## Properties Worth Keeping in Mind

- **"No vertical" is the biggest class.** About a quarter of queries — mostly navigational — should trigger nothing, so an explicit abstain class is part of the design, not a fallback.
- **Error costs are asymmetric.** An irrelevant vertical block may annoy users more than a missing one.
- **Verticals are unlike each other.** Some are genres (travel), some media types (images, video), some highly dynamic (news, where same-day demand matters).

## Related Concepts

- [[Query Routing]] — the general pattern; vertical selection is its web-search instance
- [[Federated Search]] — resource selection, of which this is the cooperative case
- [[Query Classification]] · [[Search Intent]]
- [[Search Scopes]] — the user-chosen counterpart to engine-chosen verticals

## Articles

- [[Sources of Evidence for Vertical Selection]] — the SIGIR 2009 paper defining the evidence sources
- [[Efficient Federated Search for RAG using Lightweight Routing]] — the same selection problem for RAG data sources
