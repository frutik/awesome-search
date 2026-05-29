---
title: "Context Engineering"
aliases: ["context curation", "context window curation"]
tags:
  - concept
  - agentic-search
  - llm
  - retrieval
---

# Context Engineering

**Context engineering** is the process of deciding which information from all available context sources actually enters the LLM's context window so the model can generate the best response. Also called **context curation**.

> *Context engineering is about 80% agentic search.* — [[Leonie Monigatti]]

The "context curation arrow" — the selection and routing step between all possible sources and the context window — is almost entirely implemented by a set of search tools the agent decides to invoke.

## Context Sources

| Source | Native tool |
|---|---|
| Local files | file search, `grep`, `find` |
| Agent Skills | skill loading tool |
| Databases | semantic search, SQL/ES\|QL query execution |
| Web | web search API |
| Long-term memory | memory retrieval tool |

The **shell tool** (bash) is a cross-cutting tool: it can hit files (`ls`, `grep`), databases (CLIs, scripts, `curl`), and the web (`curl`). Current debate: "bash + filesystem is all you need." The practical answer is that **good search is hard**, so you curate a stack matching your latency and quality requirements rather than defaulting to one escape hatch.

## Design Principle: Low Floor, High Ceiling

- **Specialized tools** (e.g., semantic search with a topic string, lookup-by-ID) — simple parameters, fewer failures, lower token cost
- **General-purpose tools** (shell, raw query) — handle long-tail edge cases, need more iterations and a stronger model

Ideal stack has both: specialized tools for common patterns, a general-purpose escape hatch for the long tail.

## Failure Modes

1. Agent calls no tool (answers from parametric knowledge)
2. Agent calls the wrong tool
3. Agent calls the right tool with wrong parameters

Fix: write strong tool descriptions (core purpose, trigger conditions, actions, relationships, limitations, examples). Reinforce in system prompt. Inject **Agent Skills** for domain-specific syntax (e.g., ES|QL before a database query tool).

## Evolution from RAG

```
RAG (fixed pipeline)
  → single retrieval, no correction possible

Agentic RAG
  → agent decides when/what/how to retrieve, can retry

Context Engineering
  → many source types, many tools, curated stack
```

## Related Concepts

- [[Agentic Search]] — the execution mechanism behind context engineering
- [[RAG]] — the foundational architecture context engineering extends
- [[Retrieval Pipeline]] — the underlying pipeline tools orchestrate
- [[Query Understanding]] — understanding intent drives tool selection
- [[Semantic Search]]
- [[Hybrid Search]]

## Articles

- [[Agentic Search for Context Engineering]] — [[Leonie Monigatti]]; central treatment; workshop at AI Engineer Europe 2026
