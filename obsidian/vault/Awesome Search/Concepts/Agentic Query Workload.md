---
title: "Agentic Query Workload"
type: concept
aliases: ["Agent Query Workload", "Agentic Retrieval Workload", "The New User of Search"]
tags: [concept, agentic-search, retrieval-efficiency, query-understanding]
---

# Agentic Query Workload

## Definition

The **agentic query workload** is the distinct shape of demand that autonomous agents place on retrieval systems — qualitatively different from the human search workload that current infrastructure was tuned for. "Agents are the new user of search."

## How Agents Query Differently

Measured against the [AOL search log](https://en.wikipedia.org/wiki/AOL_search_log_release) (human median 2 terms, 99th percentile 8 terms):

- **Long queries** — agent queries routinely run 8–15 terms; GPT-5's median (~10) sits past the human 99th percentile. First-turn queries can average ~19 terms.
- **Structured queries with operators** — phrase quotes, `site:`, `filetype:`, year ranges, `OR`, negation. GPT-5 used phrase quotes in 98% of BrowseComp-Plus sessions. Operators that web engines deprecated because humans stopped using them "need to make a comeback for agents" (Davis Treybig: dumb client / smart server → smart client).
- **High volume, multi-turn** — dozens of queries per human session vs potentially thousands for an agent testing hypotheses; each call conditions the next, so a miss compounds across the session (median ~24 search calls per BrowseComp-Plus question).
- **Out-of-distribution for neural retrievers** — agent queries don't look like the short fluent MS MARCO / Natural Questions training data, hurting trained dense retrievers.

## Why Infrastructure Must Adapt

The serving side built for short human queries strains under this load:

- [[Block-Max WAND]] dynamic pruning degrades — and can fall below exhaustive scoring — past ~7 terms when term weights are uniform.
- One-string search APIs (a holdover from the human search box) can't express the constraints agents intend.
- Latency is a proxy for cost; longer queries at higher volume are a direct infrastructure cost multiplier.

The response: query execution and scoring strategies that **adapt to query structure**, not a fixed pipeline.

## Related Concepts

- [[Agentic Search]] — the systems that generate this workload
- [[Block-Max WAND]] — the pruning optimization that breaks on long uniform-weight queries
- [[BM25]] · [[WAND]] — the keyword-search machinery under stress
- [[Query Understanding]] — agent queries are pre-structured, shifting where understanding happens

## Articles

- [[This Is What Agentic Retrieval Looks Like]] — [[Jo Kristian Bergum]]; the query-side analysis
- [[The Scaling Dimensions of Keyword Search]] — [[Skip Everling]]; the serving-side cost analysis

## Topics

- [[Frontier of Search 2026]]
- [[Conversational and Agentic Search]]
