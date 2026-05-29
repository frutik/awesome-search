---
title: "Agentic Search"
aliases: ["Agentic Retrieval", "AI Agent Search", "Agent-based Search"]
tags:
  - concept
  - search
  - agentic-ai
---

# Agentic Search

## Definition

Agentic search refers to search systems that go beyond simple retrieval to **plan, decompose, execute, verify, and refine** — functioning more like engineering teams pursuing goals under uncertainty than simple lookup functions.

The key distinction from traditional search: instead of a single-pass query → results interaction, agentic search operates through iterative, multi-step workflows managed by AI agents.

## Core Properties

- **Iterative uncertainty reduction** — each step should be evaluated by how much uncertainty it removes per unit of cost
- **Decomposition** — complex queries broken into subtasks, delegated to specialized tools
- **Verification** — intermediate results checked and refined
- **Evaluation-driven completion** — system stops when marginal gains no longer justify cost

## The Scope-Cost-Quality Triangle

Adapted from classic project management:

| Dimension | Meaning |
|---|---|
| **Scope** | Breadth of problem space explored |
| **Cost** | Token/computation spending |
| **Quality** | Correctness, completeness, confidence |

**Three operational strategies:**
1. **Reduce scope** (fixed cost & quality) — narrow focus, early stopping; default behavior
2. **Increase cost** (fixed scope & quality) — deep research mode; broader exploration
3. **Sacrifice quality** (fixed scope & cost) — quick overview mode; skimming + summarization

## Relationship to Agile Development

| Agile | Agentic Search |
|---|---|
| Product owners | Searchers |
| Engineers | Agents |
| Sprints (days) | Iterations (seconds/minutes) |
| Tests define done | Evaluation defines done |

## Normalization Note

"Agentic retrieval", "agentic search", "agent-based retrieval", and "AI agent search" all refer to the same paradigm. This note uses **Agentic Search** as the canonical term.

## Related Concepts

- [[Retrieval Pipeline]] — the multi-stage pipeline that agentic systems orchestrate
- [[RAG]] — foundational architecture that agentic search extends
- [[Query Understanding]] — understanding intent is especially critical in agentic workflows
- [[Context Engineering]] — agentic search is ~80% of context engineering; the curation arrow maps to search tools

## Articles

- [[Agentic Search as an Agile Engineering Process]] — [[Daniel Tunkelang]] & [[Asif Makhani]]
- [[Agentic Search for Context Engineering]] — [[Leonie Monigatti]]; evolution from RAG to context engineering; three search tool patterns; low-floor/high-ceiling design principle

- [[Superintelligent Retrieval Agent SIRA]] — LLM-enriched BM25; corpus enrichment + query expansion
- [[Mutually Assured Distraction]] — [[Lester Solbakken]]; better retrievers → better distractors; MAD dynamic; abstention as control signal
- [[You Say Search I Say Recs - Spotify Agentic Query Understanding]] — LLM router; +115% similar artists
- [[Incremental AI Adoption for E-commerce Search]] — 4 levels from traditional to conversational AI

## People

- [[Daniel Tunkelang]]
- [[Asif Makhani]]
- [[Leonie Monigatti]]

- [[Beyond Semantic Similarity - Rethinking Retrieval for Agentic Search via Direct Corpus Interaction]] — TIGER-Lab; DCI (grep/bash) outperforms all traditional retrievers on agentic tasks
- [[Metadata - The 3rd Kind of Retrieval]] — [[Doug Turnbull]]; attribute-based retrieval as alternative to embeddings in agentic context
