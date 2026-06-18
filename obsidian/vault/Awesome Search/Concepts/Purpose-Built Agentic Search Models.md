---
title: "Purpose-Built Agentic Search Models"
type: concept
aliases: ["Agentic Search Models", "Agentic Retrieval Models", "Purpose-Built Search LLMs", "Tool-Based Retrieval Models"]
tags: [concept, agentic-search, llm, reranking, neural-ir]
---

# Purpose-Built Agentic Search Models

## Definition

**Purpose-built agentic search models** are LLMs trained *specifically* on the search task — the rewrite / retrieve / rerank loop — rather than general-purpose models (GPT-5, Sonnet, Gemini) that happen to be able to call a search tool. Because they are specialized, they can be **smaller, faster, and cheaper** while matching or beating frontier models on domain retrieval.

## The Thesis

Frontier models handle the "80% case" of search well but miss the domain-specific last 20% (e.g. "bistro tables" means "small outdoor tables" in a furniture store, not restaurant equipment). They also conceive of "search" as near-flawless *web search*, whereas most teams run smaller, focused backends. A model trained on document search in a given domain orchestrates simple retrieval primitives (BM25, an embedding model, a few filters) and supplies that missing domain knowledge.

See [[Doug Turnbull]]'s framing in [[Agentic search models]]: agentic search **unbundles** the thick retrieval monolith — query classification, multiple backends, reranking — into thin tool wrappers orchestrated by one model that sees the whole problem.

## Mechanism

These models run a [[Agentic Search|multi-turn tool loop]]:

1. Write several query variants (query rewriting for recall)
2. Execute them against a search backend
3. Pick the best results, ignore noise
4. Iterate, then run a dedicated **[[Reranking|rerank]]** turn

A specialized model converges in 2–3 turns where a general agent may take 7–8.

## Examples

| Model | Maker | Notes |
|---|---|---|
| **[[SID-1]]** | [[SID.ai]] | First mover; OpenAI-compatible API; rewrite/retrieve/rerank |
| Waldo | Glean | Enterprise search model |
| (corpus-tailored) | Charcoal | Tailors a model to your corpus |

## Trade-offs

**Advantages:** smaller/faster/cheaper than frontier models; domain-aware; drop-in over an existing backend; reduces the context-engineering and bespoke-pipeline burden.

**Limitations:** today often too slow for high-QPS site search; quality depends on training data matching the deployment domain; an emerging, fast-moving category.

## Related Concepts

- [[Agentic Search]] — the multi-turn paradigm these models embody
- [[Reranking]] — the terminal step these models specialize in
- [[Direct Corpus Interaction]] — an alternative frontier direction: let the agent search raw text directly instead of training a retrieval model
- [[Query Understanding]] — query rewriting is a core competency
- [[RAG]] — these models can replace or sit alongside RAG pipelines

## Articles

- [[Agentic search models]] — [[Doug Turnbull]]; the conceptual case
- [[Agentic Search Models with OpenSearch and Elasticsearch]] — Bonsai; hands-on SID-1 integration

## Topics

- [[Current Frontier of Search]]
- [[Conversational and Agentic Search]]
