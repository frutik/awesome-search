---
title: "Direct Corpus Interaction"
aliases: ["DCI", "grep-based retrieval", "terminal-tool retrieval"]
tags:
  - concept
  - agentic-search
  - retrieval
  - neural-ir
---

# Direct Corpus Interaction (DCI)

## Definition

**Direct Corpus Interaction (DCI)** is a retrieval paradigm where an agent searches a raw text corpus directly using general-purpose terminal tools (grep, find, bash, shell pipelines, lightweight scripts) — without any embedding model, vector index, or retrieval API.

Proposed in the paper "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction" (TIGER-Lab, 2026, arXiv:2605.05242).

## Motivation

Traditional retrieval systems expose corpora through a **fixed similarity interface**: query → top-k results in one step. For agentic tasks, this is a bottleneck:
- Exact lexical constraints are hard to express through similarity
- Sparse clue conjunctions require multiple steps
- Evidence filtered out early cannot be recovered
- Multi-step hypothesis refinement is impossible in one-shot retrieval

## How DCI Works

Like a coding agent navigating a codebase:
- `grep` for exact patterns
- `find` for file discovery
- Bash pipelines for complex filtering
- Lightweight scripts for processing

No preprocessing. No offline indexing. No embeddings. Adapts naturally to evolving corpora.

## Results vs Traditional Retrieval

| Benchmark | Gain vs Best Traditional Baselines |
|---|---|
| Agentic Search (BrowseComp-Plus) | +11.0% |
| Multi-hop QA | +30.7% |
| IR Ranking (BEIR/BRIGHT) | +21.5% |

## Key Insight

> "Retrieval quality depends not only on reasoning ability but also on the **resolution of the interface** through which the model interacts with the corpus."

A higher-resolution interface (direct corpus access) enables more precise and adaptive retrieval than any pre-indexed similarity interface.

## Trade-offs

**Advantages:**
- No offline indexing required
- Exact lexical matching possible
- Multi-step hypothesis refinement
- Adapts to corpus changes

**Limitations:**
- Requires strong coding-capable agent
- Best suited for file-system-accessible corpora
- Latency depends on corpus size and search complexity

## Relationship to Agentic Search

DCI is a natural extension of [[Agentic Search]] — rather than calling a fixed retrieval API, the agent becomes a corpus explorer. This is why coding agents often perform well on information retrieval tasks.

## Related Concepts

- [[Agentic Search]] — the broader paradigm DCI extends
- [[Retrieval Pipeline]] — DCI replaces the traditional pre-indexed pipeline
- [[RAG]] — DCI provides an alternative retrieval mechanism for RAG
- [[Purpose-Built Agentic Search Models]] — the competing frontier bet: train a retrieval model rather than remove the retriever
- [[Agentic Query Workload]] — why the fixed similarity interface is a bottleneck for agents

See the topic [[Frontier of Search 2026]] for how DCI fits the broader agentic-retrieval landscape.

## Articles

- [[Beyond Semantic Similarity - Rethinking Retrieval for Agentic Search via Direct Corpus Interaction]]
