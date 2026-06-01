---
title: "Agentic Search for Context Engineering"
source: "https://medium.com/@iamleonie/agentic-search-for-context-engineering-268b5a1bbc0b"
author: "[[Leonie Monigatti]]"
published: 2026-05-27
company: "[[Elastic]]"
tags:
  - article
  - agentic-search
  - context-engineering
  - retrieval
  - medium
---

# Agentic Search for Context Engineering

Long-form write-up of the workshop given at AI Engineer Europe 2026 (London, April 8, 2026). Argues that **context engineering is ~80% agentic search** and demonstrates three search tool patterns over a conference schedule dataset.

- Workshop repository: https://github.com/iamleonie/workshop-agentic-search
- Workshop recording: https://www.youtube.com/watch?v=ynJyIKwjonM

## Key Argument

> *Context engineering is about 80% agentic search.*

**[[Context Engineering]]** = the process of deciding which information from all available context sources goes into the LLM's context window (also called "context curation"). What hides behind the curation arrow is a set of search tools the agent can call.

## Evolution: RAG → Agentic RAG → Context Engineering

### RAG (fixed pipeline)
User message as query → single vector search → retrieved chunks + prompt → LLM.
Breaks when: retrieval isn't needed, query needs correction, or multi-hop retrieval is required.

### Agentic RAG
Fixed pipeline replaced with a search tool. Agent decides whether to call, retry, or rewrite.

### Context Engineering (current state)
Many context sources + a native tool per source:

| Source | Tool |
|---|---|
| Local files | file search, `grep`, `find` |
| Agent Skills | skill loading tool |
| Databases | semantic search, SQL/ES\|QL query tool |
| Web | web search API |
| Long-term memory | memory retrieval tool |

The **shell tool** (bash) is the cross-cutting wildcard — can hit files, databases via CLI, and web via `curl`. The article argues "bash is all you need" is a false dichotomy: **curate a stack for your latency and quality requirements**.

## Three Search Tool Patterns (Demonstrated)

### 1. Vanilla Semantic Search
- Tool: `semantic_search_conference_sessions(query: str)` — single string parameter
- Simple to call, low failure rate
- Fails on exact/acronym queries (e.g., "GEPA" returns unrelated sessions)

### 2. General-Purpose DB Query (ES|QL)
- Tool: `execute_esql_query(esql_query: str)` — full query as parameter
- Handles keyword, filter, and aggregation queries
- Requires stronger LLM; fails without domain syntax knowledge
- Fix: inject **Agent Skills** (a `load_skill` tool + middleware that injects ES|QL syntax docs before the agent writes a query)

### 3. Shell Tool (bash/grep over local files)
- Uses LangChain `ShellTool`; no safeguards by default — sandbox in production
- `grep` works well for exact/known terms; chaining synonym expansions is needed for semantic-style queries
- `jina-grep-cli` adds semantic search to filesystem: `jina-grep -r "regulatory constraints" /data/`
- Alternatives: LlamaIndex `semtools`, LightOn `colgrep`

## Failure Modes in Agentic Search

1. Agent calls no tool (answers from parametric knowledge)
2. Agent calls the wrong tool
3. Agent calls the right tool with wrong parameters

## Tool Description Best Practices

Tool description is the most critical component of any tool. Start with core purpose + trigger conditions. Add actions, relationships, limitations, and examples when agent struggles. Repeat key rules in the system prompt.

## Design Principle: Low Floor, High Ceiling

- **Specialized tools** — narrow scope, simple parameters, fewer failures, lower token cost
- **General-purpose tools** — shell, raw queries — handle edge cases, need more iterations and stronger models
- Recommendation: start general-purpose, log tool call traces, add specialized tools where repetition appears

## Related Notes

- [[Context Engineering]]
- [[Agentic Search]]
- [[RAG]]
- [[Semantic Search]]
- [[Hybrid Search]]

## People

- [[Leonie Monigatti]] (author)

## Companies / Tools

- [[Elastic]] — author's employer; Elasticsearch and ES|QL used in demos
- [[Jina AI]] — `jina-grep-cli` for semantic filesystem search

## Further Reading (from article)

- https://www.elastic.co/search-labs/blog/search-tools-context-engineering (shell tool is not a silver bullet)
- https://www.elastic.co/search-labs/blog/database-retrieval-tools-context-engineering (effective database retrieval tools)
- https://github.com/jina-ai/jina-grep-cli
