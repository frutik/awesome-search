---
title: "SID-1"
type: tool
aliases: ["SID-1 model"]
website: https://www.sid.ai/research/sid-1
repo:
maintainer: "SID.ai"
tags: [tool, model, agentic-search, reranking, llm]
created: 2026-06-18
---

# SID-1

SID-1 is [[SID.ai]]'s first **purpose-built agentic retrieval model** — a small LLM trained specifically on the rewrite / retrieve / rerank loop rather than general-purpose tool use. It is a concrete instance of the [[Purpose-Built Agentic Search Models]] category.

## Characteristics

- **Interface:** OpenAI-compatible API (`api.sid-1.com/v1`). Tool definitions go in the system prompt as structured text, not the OpenAI `tools` field.
- **Loop:** typically 2–3 retrieval turns plus a dedicated reranking turn (`report_helpful_ids`); up to 6–7 turns for long/paragraph queries.
- **Claimed quality:** ~1.9x more likely to surface the right result than embedding-only search; more accurate than agentic retrieval on Gemini 3 Pro, Sonnet 4.5, and GPT-5.1 at highest compute, while ~24x faster.
- **Cost:** priced similar to gpt-5.4-mini (~$0.00093/query in one Gutenberg-corpus test), cheaper and faster than the larger frontier models it beats.

## Why a Small Model Wins

Specialization plus focused training on a single task (search rewrite/retrieve/rerank) lets SID-1 outperform much larger general models that must support every conceivable tool and task.

## Articles
- [[Agentic Search Models with OpenSearch and Elasticsearch]] — Bonsai's hands-on integration against OpenSearch
- [[Agentic search models]] — [[Doug Turnbull]]; positions SID-1 as the first mover

## Concepts
- [[Purpose-Built Agentic Search Models]]
- [[Agentic Search]]
- [[Reranking]]

## Topics
- [[Current Frontier of Search]]
