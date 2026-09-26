---
type: article
title: "Query Routing: Direct Queries to the Right Source"
source: https://app.ailog.fr/en/blog/guides/query-routing-rag
author:
  - "[[Ailog]]"
published: 2026-03-12
tags:
  - article
  - rag
  - query-routing
  - query-understanding
  - vendor-blog
concepts:
  - "[[Query Routing]]"
  - "[[RAG]]"
  - "[[Embeddings]]"
  - "[[Personalization]]"
topics:
  - "[[Query Classification]]"
created: 2026-09-26
---

# Query Routing: Direct Queries to the Right Source

**Author:** [[Ailog]] (Ailog Team)
**Source:** https://app.ailog.fr/en/blog/guides/query-routing-rag
**Published:** 2026-03-12 · Ailog RAG guides

## Summary

A code-first guide to [[Query Routing]] for enterprise [[RAG]]: rather than searching every data source for every question, a router picks the source first. The running example is a support assistant over four sources — FAQ, technical docs, product catalog, resolved tickets — with "How to return?" going to the FAQ, "API rate limits?" to the docs, "iPhone 15 price?" to the catalog and "WiFi connection bug?" to tickets. The claimed payoff of routing over searching everything: precise instead of diluted results, lower latency, and cost no longer proportional to the number of sources.

Its most reusable idea is the **cascade**: try the free router first, pay for the LLM only when the cheap ones are unsure.

## Three Routers, Cheapest First

| Router | Mechanism in the guide | Trade-off |
|---|---|---|
| **Keyword** | Regex patterns per route (`return\|refund\|cancel` → faq, `api\|endpoint\|webhook` → docs, `error\s+\d{3}` → docs); route with the most pattern hits wins, zero hits → `default` | Fast, predictable, no LLM cost; rigid, patterns need maintenance |
| **Embedding** | A handful of example questions per route, embedded with [[Sentence Transformers]] (`BAAI/bge-m3`); each route is the **centroid** of its examples; cosine to the query picks the route and doubles as confidence | No per-call cost; needs good examples |
| **LLM** | `gpt-4o-mini` at temperature 0 gets each route's one-line description and must answer in JSON: route, confidence, reasoning | Best decisions; slowest and paid |

The embedding router averages the examples into one centroid per route — the [[Query Routing|semantic router]] variant that compares against a prototype, not against the nearest individual example.

## Hierarchical Routing

The three are chained:

1. **Keywords** — if any pattern fires, take that route with a fixed confidence of 0.9.
2. **Embeddings** — if cosine confidence exceeds **0.85**, take the embedding route.
3. **LLM** — only for what is left; can be switched off, in which case the embedding route is used as a low-confidence fallback.

Every decision records which level made it (`keyword` / `embedding` / `llm`), which is what makes the monitoring step below possible.

## Beyond One Route

- **Multi-route.** An LLM scores *all* sources for relevance and every source above **0.5** is queried — e.g. "Why does the product API return error 500 on certain items?" → docs, tickets and products.
- **Contextual routing.** User metadata multiplies route scores after the embedding router has spoken: developers boost docs (×1.3), users with open tickets boost tickets (×1.2), being on a product page boosts products (×1.4). A light form of [[Personalization]] applied to the routing decision.

## Operating It

- **Log every decision** with query, route, method and confidence, and attach user feedback (correct / incorrect / unknown) so accuracy can be broken down **per routing method**.
- **Adaptive router.** User corrections are stored against a hash of the normalised query and override the model on repeat; the sketch suggests retraining every 100 corrections.

The complete pipeline routes, retrieves top-5 from the chosen source, and generates with `gpt-4o`, returning the route, method and confidence alongside the answer.

## Caveats

- **Vendor guide.** It closes by pitching Ailog's own automatic routing; nothing is benchmarked.
- **Thresholds are illustrative.** The 0.9 / 0.85 / 0.5 cut-offs and the ×1.2–1.4 boosts are values in example code, not tuned or evaluated settings; the printed confidences in the examples are sample outputs.
- **Snippets are sketches** — the retrievers (`FAQRetriever`, `DocsRetriever`, …) and analytics client are left undefined.

## Related Concepts

- [[Query Routing]] — primary topic; adds the cascade and multi-route patterns
- [[Query Classification]] — routing as classification over data sources
- [[RAG]] · [[Embeddings]] · [[Personalization]]

## Related Notes

- [[Build an Advanced RAG App - Query Routing]] — the router taxonomy with a LlamaIndex walkthrough
- [[Routing in RAG Driven Applications]] — [[Sami Maameri]]'s seven-router taxonomy
- [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]] — a trained classifier routing between retrievers rather than sources
- [[Ailog]] · [[Sentence Transformers]]
