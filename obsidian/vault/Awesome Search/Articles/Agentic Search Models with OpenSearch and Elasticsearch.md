---
title: "Agentic Search Models with OpenSearch and Elasticsearch"
type: article
source: "https://bonsai.io/blog/agent-search-with-sid/"
author: "Bonsai"
published: 2026-06-05
created: 2026-06-18
concepts: [Purpose-Built Agentic Search Models, Agentic Search, Reranking, Query Understanding, RAG]
topics: [Frontier of Search 2026, Conversational and Agentic Search, Elasticsearch vs OpenSearch]
companies: [Bonsai, SID.ai]
tags: [article, agentic-search, reranking, opensearch, llm]
---

# Agentic Search Models with OpenSearch and Elasticsearch

A hands-on Bonsai blog post introducing **purpose-built agentic LLMs for searching and reranking** as a drop-in relevance improvement, demonstrated with preview access to the [[SID-1]] model wired into an [[OpenSearch]] cluster running the Gutenberg corpus.

> SID-1 is described as 1.9x more likely to surface the right results than embedding-only search across general knowledge, finance, science, legal, and email — and more accurate than agentic retrieval built on Gemini 3 Pro, Sonnet 4.5, and GPT-5.1 at its highest compute setting, while being 24x faster (144 vs 5.7 seconds).

---

## The Problems It Targets

Gaps that exist in nearly every hybrid search solution:

- The best results might not be at the top
- Noisy / irrelevant results pollute the page
- The user's query language might not match the corpus/domain language
- Vector search has no cutoff — everything is a "match"

Prior attempts to throw LLMs at these problems hit walls: [[LLM as Judge|LLM-as-judge]] reranking at query time is slow and expensive (especially [[Pairwise Relevance Evaluation|pairwise]] judgements, which were the most effective), and [[RAG]] summarization deprioritizes the actual results and gets in the way of discovery.

## Agentic Retrievers as the Solution

The emerging pattern is **tool-based / multi-turn retrieval**, the same loop running behind a coding agent or chat:

1. Write several query variants to improve recall
2. Execute them and gather results
3. Pick the best results across responses, ignoring noise
4. Iterate based on what was found ("turns")

General agents (ChatGPT, Claude) may take 7–8 turns. [[SID-1]] typically takes 2–3 turns plus a specialized reranking turn (`report_helpful_ids`), and at most 6–7 retrieval turns for paragraph-length queries.

## Implementation Notes

- Built on top of an existing two-tier OpenSearch search app; ~800 lines of new code, only new dependency is the `openai` package (SID exposes an OpenAI-compatible API at `api.sid-1.com/v1`).
- Four tools defined for the model: `search` (multi_match), `text_search` (query_string for advanced syntax), `read` (fetch a doc by ID), `report_helpful_ids` (termination/rerank).
- Quirk: SID does **not** use the OpenAI `tools` field — you pass a dummy stub and put the real tool definitions in the system prompt as structured text.
- Queries within a turn are batched into a single `_msearch` request (~3 requests over 3 turns instead of ~12).

## Cost and Latency

A typical query uses ~10k input + 400 output tokens. SID-1 is priced similar to gpt-5.4-mini (~$0.00093/query, ~1075 queries/dollar) but tests more accurate than the larger, pricier gpt-5.1 (~$0.0019/query). Full "took" time scaled with query length: 2–7 seconds. General models also incur more turns, raising their effective cost further.

## Why a Small Specialized Model Beats GPT

GPT is general — it can call any tool and was trained on every task. SID is specialized: trained on just the rewrite / retrieve / rerank toolset and outcome. Specialization plus focused training lets a smaller model outperform the general one on this narrow task. This is the same thesis [[Doug Turnbull]] argues in [[Agentic search models]] — domain- and task-tuned agentic search models replacing the bespoke retrieval monolith.

---

## Related Concepts
- [[Purpose-Built Agentic Search Models]] — the category SID-1 belongs to
- [[Agentic Search]] — the multi-turn tool-based retrieval paradigm
- [[Reranking]] — SID's terminal reranking turn
- [[RAG]] — contrasted as the alternative the author critiques

## Related Articles
- [[Agentic search models]] — [[Doug Turnbull]]; the conceptual case for agentic search models for "the last 20%"
- [[The Scaling Dimensions of Keyword Search]] — why agent-driven multi-turn querying stresses keyword backends
- [[This Is What Agentic Retrieval Looks Like]] — how agents actually query

## Tools
- [[SID-1]]
- [[OpenSearch]]
- [[Elasticsearch]]

## Companies
- [[Bonsai]]
- [[SID.ai]]

## Topics
- [[Frontier of Search 2026]]
- [[Conversational and Agentic Search]]
