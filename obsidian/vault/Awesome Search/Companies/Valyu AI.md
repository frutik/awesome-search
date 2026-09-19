---
type: company
title: "Valyu AI"
aliases: ["Valyu", "valyu.ai", "valyu.network"]
tags:
  - company
  - search-api
  - retrieval
  - rag
  - specialist-search
website: https://www.valyu.ai
created: 2026-09-19
---

# Valyu AI

**Valyu** sells a retrieval API positioned as the data layer for research agents: one interface
to search specialist, proprietary, and web sources and run multi-step research that returns
cited, structured output. Its stated focus sectors are **finance** and **life sciences / R&D**,
covering specialist scientific sources such as preprint archives alongside general web results.

The pitch is evidence control — retrieval over curated primary sources with citations attached,
rather than whatever a general crawl surfaces.

Website: https://www.valyu.ai

---

## The API, as Used in Practice

From the worked example in [[How to Use Jev - A Practical Guide]], the search call takes an
`included_sources` allowlist (e.g. PubMed and arXiv collections), a `start_date`, a
`max_num_results`, and a `relevance_threshold` — so filtering happens at retrieval time rather
than downstream. Results carry title, URL, and content.

That threshold parameter is the interesting part for this vault: it presumes a comparable
relevance score at the retrieval stage, which is the same property [[Calibrated Relevance
Probability|calibrated scoring]] provides at the rerank stage.

## Relevance to Search

Valyu is a [[Federated Search|federated]] retrieval product over curated source collections —
the "fetch precisely" half of the retrieve-then-judge pattern its own guide describes, where a
cheap per-passage judgment ([[Reranking]]) filters the retrieved set before anything expensive
consumes it. The argument it makes for itself is a grounding argument rather than a ranking
one: a downstream model's judgment can only be as good as the corpus it was handed.

## In This Vault

- [[How to Use Jev - A Practical Guide]] — published on Valyu's dev.to account by
  [[Prosper Otemuyiwa]]; a guide to [[Jev]] whose Pattern 5 pairs Valyu retrieval with
  per-passage Noul filtering. Vendor-adjacent, and the product placement should be read as
  such, though the underlying observation about grounding stands on its own.

## Related Concepts

- [[Reranking]] — the judging half of the pattern
- [[Federated Search]] · [[Search Scopes]] — searching across curated source collections
- [[Calibrated Relevance Probability]] — comparable scores as a precondition for thresholding
- [[RAG]] · [[Clean Context]] · [[Context Engineering]] — what precise retrieval is in service of
- [[Semantic Relevance]] — relevance thresholding at retrieval time

## Related Notes

- [[TypeSafe]] · [[Jev]] — the judging model in the pattern
- [[How to Use Jev - A Practical Guide]] — the source
