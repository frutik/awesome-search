---
title: "Observability for AI Workloads: A New Paradigm for a New Era"
author: "[[Dotan Horovits]]"
published: 2026-01-04
source: "https://horovits.medium.com/observability-for-ai-workloads-a-new-paradigm-for-a-new-era-b8972ba1b6ba"
tags:
  - article
  - observability
  - search-quality
  - retrieval
  - agentic-search
  - medium
created: 2026-06-01
---

# Observability for AI Workloads: A New Paradigm for a New Era

## Summary

A 2026 retrospective on how AI workloads changed observability requirements. Broadly covers LLM/AI observability, but contains a significant section on **RAG and vector database layer observability** directly relevant to search systems. The article also argues that AI workloads invert the scale assumptions baked into traditional observability tooling.

## Search-Relevant Content

### RAG and Vector Database Layer

The article calls out RAG and vector search as a distinct observability layer requiring its own signals:

- **Retrieval performance and query latency** — same P50/P99 approach as traditional search, but queries are semantic; latency is measured differently when LLM calls chain into retrieval
- **Retrieval accuracy and relevance scoring** — are retrieved chunks actually relevant to the query? Requires quality evaluation beyond infrastructure metrics
- **Semantic similarity quality** — measuring whether the vector retrieval is returning semantically appropriate results
- **Index health and freshness** — same concern as classic search: is the index current? Staleness degrades RAG answer quality
- **Context assembly effectiveness** — are the retrieved chunks sufficient to answer the query, and are they assembled in a useful order?

### Agentic Search Observability

The article describes **agentic layer observability** — monitoring agent-to-agent communication, tool invocations, and external API calls. For search systems using agentic retrieval (query planning, tool-calling to search, result synthesis), this is directly applicable:

- Trace the full reasoning path: what queries were issued, what was retrieved, how results were synthesized
- Capture prompt templates and retrieved context alongside the final answer
- Monitor tool usage patterns across multi-step retrieval workflows

### Inverted Scale Assumptions

Traditional search observability is tuned for high-throughput, low-latency, small-payload workloads. AI-augmented search flips this:
- **Lower throughput** — hundreds to thousands of requests/minute, not millions/second
- **Higher latency tolerance** — LLM calls take 2–30 seconds; P99 thresholds shift accordingly
- **Larger payloads** — prompts and retrieved chunks reach tens of kilobytes

This matters when instrumenting hybrid search + RAG pipelines: existing alerting thresholds and sampling rates need recalibration.

### OpenTelemetry for GenAI

The OpenTelemetry Generative AI SIG is standardizing semantic conventions for AI telemetry. For RAG search systems, this means traces that capture: query text, retrieved document IDs and scores, context passed to the LLM, model parameters, and token counts — the same structured event logging search teams already apply, extended to cover the generation step.

## Related Entities

- [[Search Observability]] — the search-specific elaboration of these principles
- [[Agentic Search]] — the retrieval pattern this article's agentic observability section addresses
- [[RAG]] — the retrieval-augmented generation pattern with its own observability layer
- [[Context Engineering]] — managing context quality is the observability target in RAG

## Related Notes

- [[This Is What Agentic Retrieval Looks Like]] — concrete agentic retrieval patterns to observe
- [[Agentic Search for Context Engineering]] — context engineering as the goal of agentic retrieval
- [[Search Quality Assurance with AI as a Judge]] — quality evaluation as a complement to production observability
