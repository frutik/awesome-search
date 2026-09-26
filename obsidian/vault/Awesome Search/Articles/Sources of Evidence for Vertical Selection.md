---
type: article
title: Sources of Evidence for Vertical Selection
source: http://www.cs.cmu.edu/~callan/Papers/sigir09-jarguello.pdf
author:
  - "[[Jaime Arguello]]"
  - "[[Fernando Diaz]]"
  - "[[Jamie Callan]]"
  - Jean-François Crespo
published: 2009
tags:
  - article
  - paper
  - query-routing
  - federated-search
  - aggregated-search
  - sigir
concepts:
  - "[[Vertical Selection]]"
  - "[[Federated Search]]"
  - "[[Query Routing]]"
  - "[[Query Classification]]"
topics:
  - "[[Query Classification]]"
  - "[[Federated vs Unified Search]]"
created: 2026-09-26
---

# Sources of Evidence for Vertical Selection

**Authors:** [[Jaime Arguello]], [[Fernando Diaz]], [[Jamie Callan]], Jean-François Crespo (Carnegie Mellon University; Yahoo! Labs Montréal)
**Venue:** SIGIR 2009 · [PDF](http://www.cs.cmu.edu/~callan/Papers/sigir09-jarguello.pdf)

## Summary

Web search engines run specialised search services — **verticals** such as news, images, video, local, shopping, travel, job postings — and show a block of vertical results inside the main results page when a query calls for it (*aggregated search*). **[[Vertical Selection]]** is deciding which vertical, if any, a query issued to the main search box should trigger. It is [[Query Routing]] as a web-scale production problem, long before RAG gave the idea its current name — and a cooperative form of [[Federated Search]] resource selection, since the engine owns every vertical.

## Three Sources of Evidence

The paper's point is that vertical selection has evidence ordinary query classification and resource selection lack:

1. **The query string** — rule-based vertical triggers (words like "news" or "pictures") and geographic features.
2. **Vertical query logs** — queries users previously typed *directly* into each vertical; the likelihood of the query under each vertical's query-log language model.
3. **Vertical-representative corpora** — sampled vertical content, plus Wikipedia articles associated with verticals for text-poor ones like video, scored with resource-selection methods such as ReDDE and Clarity.

A supervised classifier combines all three and is compared against single-evidence baselines drawn from federated search (ReDDE, Soft.ReDDE, Clarity) and from query-log likelihood.

## Setup

- 18 verticals differing in genre, media type, size and traffic.
- 25,195 unique queries from a commercial engine's log; editors assigned zero to six relevant verticals each. About 26% — mostly navigational queries like "myspace" — had **no relevant vertical**, and 44% had exactly one.
- The task is single-vertical prediction, including an explicit **"no relevant vertical"** class; precision counts a query as correct when it predicts a relevant vertical or correctly predicts none. Always predicting "none" already scores 0.263.

## Findings

- **Query logs were the best single source**: ranking verticals by the query's likelihood under each vertical's query-log language model beat corpus-based resource-selection methods. Using collection-specific query logs for resource selection had not been studied before, partly because in uncooperative federated search those logs are inaccessible.
- The supervised combination beat every single-evidence baseline; features not derived from any vertical resource (categorical, geographic) contributed significantly.
- Clarity scores did worse than always predicting "no vertical" — per-collection scores are not comparable across collections.
- Among misclassified queries with a true vertical, 57% of errors predicted "no vertical" and 43% the wrong vertical. The authors note the costs are asymmetric: showing an irrelevant vertical may annoy users more than missing a relevant one.

## Why It Still Matters

Most modern router write-ups rediscover the same pieces: a "none / default" route, keyword triggers as the cheap first stage, and using past traffic as evidence. The abstain class and the asymmetric cost of a wrong route are exactly the points [[Query Classification]] makes about routing classifiers.

## Related Concepts

- [[Vertical Selection]] · [[Federated Search]] · [[Query Routing]] · [[Query Classification]]

## Related Notes

- [[Efficient Federated Search for RAG using Lightweight Routing]] — resource selection for RAG federations
- [[LTRR - Learning To Rank Retrievers for LLMs]] — Diaz again, ranking retrievers instead of verticals
- [[Query Routing - Direct Queries to the Right Source]] — keyword → embedding → LLM cascade with a default route
