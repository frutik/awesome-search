---
type: article
title: "This Is What Agentic Retrieval Looks Like"
source: "https://hornet.dev/blog/this-is-what-agentic-retrieval-looks-like"
author:
  - "[[Jo Kristian Bergum]]"
published: 2026-05-20
created: 2026-05-31
concepts:
  - "[[Agentic Retrieval]]"
  - "[[BM25]]"
  - "[[Query Operators]]"
  - "[[Distribution Shift]]"
  - "[[BrowseComp-Plus]]"
topics:
  - "[[Agentic Search]]"
  - "[[Frontier of Search 2026]]"
companies:
  - "[[Hornet]]"
tags:
  - article
  - agentic-retrieval
  - bm25
  - query-understanding
  - hornet
  - company-blog
---

# This Is What Agentic Retrieval Looks Like

**[[Jo Kristian Bergum]]** ([[Hornet]]) analyzes 19,279 search calls made by GPT-5 during BrowseComp-Plus benchmark runs to characterize the agentic query workload. The core finding: agents search like power users, writing queries that are completely out of distribution for retrieval infrastructure built and tuned for humans.

*Part 2 of a series on agentic retrieval. Part 1: Deep research is a retrieval problem.*

---

## The BrowseComp-Plus Setup

- 830 riddle-like, multi-hop questions
- GPT-5 has only a BM25 search tool returning top-5 snippets (512 tokens each)
- Median session: **24 search calls** per question; p90: 35; max: 63
- Oracle accuracy (evidence pre-loaded): 93% correct; with weak BM25: 14%
- The **79-point gap** is where retrieval quality lives

Each search call is conditioned on all prior calls: a miss on turn 3 degrades every subsequent turn.

## Agent Query Length vs. Human Queries

| Distribution | Median | p90 | p99 |
|---|---|---|---|
| AOL human queries (2006) | 2 terms | 5 terms | 8 terms |
| GPT-5 BrowseComp-Plus | 10 terms | 17 terms | — |

**GPT-5's median query sits past the 99th percentile of human queries.** First queries average 19.1 terms; length drops to ~10 by turn 2 and plateaus there.

## GPT-5 Uses Web Search Syntax — Fluently

| Operator | % of individual queries | % of sessions |
|---|---|---|
| Phrase quotes `"..."` | 65.6% | 98.2% |
| Four-digit year | 45.6% | 95.4% |
| `site:` domain filter | 6.4% | 48.1% |

Agent also writes combinations humans almost never type:

- `OR` across a year range: `"born June" "video game composer" 1971 OR 1970 OR 1969`
- Wildcard subdomain: `site:*.org "January 28, 2019" "Blog" art`
- Stacked operators: `site:surrey.ac.uk filetype:pdf "student numbers" "2018/19"`
- Negation: `"Memphis 13" -football -soccer Wikipedia`

Phrase quotes appeared in 98% of sessions — the agent treats exact-string matching as a primary strategy.

## Why Current Retrieval Infrastructure Fails Agents

Retrieval was designed for the human workload:
- Inverted indexes and BM-WAND pruning degrade past ~7 terms (uniform term weights)
- Neural retrievers trained on MS MARCO / Natural Questions (short, fluent queries) → [[Distribution Shift]] on agent queries
- Search APIs expose one string input (optimized for human typers)
- Query operators deprecated because humans stopped using them

None of those choices were wrong for humans. They just don't match this workload.

## The Multi-Turn Compounding Problem

Poor retrieval compounds across a session. A missed document on turn 3 means turn 4 reasons over a different context, and the error propagates. **Miss rate × session length = accumulated degradation** — a problem that single-query NDCG benchmarks are blind to.

---

## Related Concepts

- [[Agentic Retrieval]] — the workload studied; multi-turn, long-query, operator-heavy
- [[BM25]] — the retrieval system used; reveals its limits under agent workload
- [[Query Operators]] — phrase quotes, `site:`, `filetype:`, `OR`, negation; GPT-5 uses them fluently
- [[Distribution Shift]] — neural retrievers trained on MS MARCO fail on long agent queries
- [[Agentic Search]] — broader context; retrieval is the bottleneck
- [[Agentic Query Workload]] — the canonical concept this article characterizes (query side)
- [[BrowseComp-Plus]] — benchmark used; 830 multi-hop questions, 100K-page corpus

## Related Articles

- [[The Scaling Dimensions of Keyword Search]] — [[Skip Everling]]; the serving-side companion (this is the query side)
- [[Beyond Semantic Similarity - Rethinking Retrieval for Agentic Search via Direct Corpus Interaction]] — complementary agentic retrieval research
- [[Agentic Search for Context Engineering]] — agentic search design patterns
- [[Agentic Search as an Agile Engineering Process]] — engineering framing of agentic search

## Companies

- [[Hornet]] — author's company; building retrieval infrastructure for agentic workloads

## People

- [[Jo Kristian Bergum]] — author; Hornet; former Vespa AI Chief Scientist
