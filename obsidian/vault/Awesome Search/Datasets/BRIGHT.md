---
title: "BRIGHT"
aliases: ["BRIGHT benchmark", "reasoning-intensive retrieval benchmark"]
tags:
  - dataset
  - benchmark
  - retrieval
  - reasoning
  - search-evaluation
type: dataset
source: xlang-ai (Su et al., ICLR 2025)
domain: reasoning-intensive retrieval — StackExchange, LeetCode, math competitions
website: https://github.com/xlang-ai/BRIGHT
created: 2026-08-05
---

# BRIGHT

## Overview

**BRIGHT** is a retrieval benchmark of **1,385 real-world queries** where finding the relevant document requires *reasoning*, not surface similarity. Queries come from StackExchange, LeetCode, and math competitions; the relevant documents are connected to the query only by inference — a shared underlying theorem, an analogous algorithm, a transferable technique — rather than by shared vocabulary or obvious semantic proximity.

It was built specifically to expose the limits of both lexical and embedding-based retrieval on this class of query.

## The Result That Matters

BRIGHT is the most useful corrective in the field because of one comparison: **a model scoring 59.0 nDCG@10 on [[MTEB]] scores 18.3 on BRIGHT.**

That is not a modest degradation, it is a collapse. Whatever dense [[Embeddings|embedding]] models are doing well, it is not multi-step reasoning about relevance. Semantic similarity — which is all a [[Bi-Encoder]] can express — turns out to be a poor proxy for "this document helps answer this question" once the connection stops being lexical or topical.

A secondary finding: [[BM25]] with query augmentation remains competitive here, which is a familiar pattern from [[BEIR]] and one more reason to keep a lexical leg in the pipeline. See [[Hybrid Search]].

## Why It Matters for Practice

Most e-commerce and site search queries are *not* reasoning-intensive, so BRIGHT is not a direct proxy for typical product search quality. Its value is different:

- **As a ceiling check** — it marks where embedding-based retrieval structurally stops working, which matters as teams push search toward question answering, agentic workflows, and [[Conversational and Agentic Search]].
- **As a rhetorical tool** — cite BRIGHT whenever someone claims retrieval is a solved problem or that a leaderboard position implies general capability.
- **As motivation for reranking** — the gap is exactly the space that reasoning rerankers and LLM-based rerankers try to close. See [[Reasoning Reranking]] and [[Multi-Stage Ranking]].

## Related

- [[Retrieval Benchmarks and Leaderboards]] — the wider landscape
- [[MTEB]] — the board whose leaders BRIGHT humbles
- [[BEIR]] — zero-shot generalization, the previous generation of this critique
- [[Reasoning Reranking]] — the approaches attacking this gap
- [[BM25]] · [[Hybrid Search]] — why lexical retrieval keeps refusing to die
