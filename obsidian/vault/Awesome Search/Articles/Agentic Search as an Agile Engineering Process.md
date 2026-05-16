---
title: "Agentic Search as an Agile Engineering Process"
source: "https://dtunkelang.medium.com/agentic-search-as-an-agile-engineering-process-5514b0790e8e"
author: ["Daniel Tunkelang", "Asif Makhani"]
tags:
  - clippings
  - agentic-search
  - search
  - ai-agents
concepts:
  - Agentic Search
  - Bag-of-Documents Model
  - Retrieval Pipeline
created: 2026-05-15
---

# Agentic Search as an Agile Engineering Process

**Source**: https://dtunkelang.medium.com/agentic-search-as-an-agile-engineering-process-5514b0790e8e  
**Authors**: [[Daniel Tunkelang]], [[Asif Makhani]]

## Summary

Tunkelang and Makhani argue that [[Agentic Search]] is best understood through the lens of agile software engineering: rather than committing upfront to a fixed retrieval plan (waterfall), an agent iteratively plans, executes, verifies, and adapts its retrieval strategy based on what it finds.

## Key Concepts

### The Agile Analogy
Traditional search: waterfall — one query → one retrieval → one answer.  
Agentic search: agile — sprint planning (query decomposition) → execution (retrieval) → review (verification) → retrospective (reformulation).

### Scope-Cost-Quality Triangle
The article introduces a fundamental tradeoff:
- **Scope**: what the agent retrieves (breadth of search)
- **Cost**: computational budget (number of retrieval calls, LLM tokens)
- **Quality**: accuracy/completeness of final answer

You can optimize for at most two of the three. The agent's job is to navigate this triangle intelligently given a budget.

### Three Agentic Strategies

1. **Iterative refinement**: start broad → narrow based on retrieved evidence
2. **Parallel decomposition**: split complex query into sub-queries → retrieve in parallel → synthesize
3. **Verification loop**: retrieve → LLM judges sufficiency → re-retrieve if inadequate

### Agent as Search Manager
The agent acts like a senior engineer managing a team:
- Assigns retrieval sub-tasks
- Monitors quality of intermediate results
- Decides when "good enough" is sufficient
- Adapts strategy when initial approach fails

## Insights

- Agentic search transforms search from a single-shot problem to a multi-turn conversation between the agent and the retrieval system
- The cost of failed retrieval calls is real — agents must balance exploration vs. exploitation
- Traditional IR metrics (precision, recall) are insufficient; need outcome-oriented evaluation
- [[Bag-of-Documents Model]] provides theoretical grounding: the agent iteratively refines the distribution P(d|q)

## Key Quotes

> "Search is not a single-shot problem. It's an iterative process of hypothesis formation and testing."

> "The agent's value is not in making a single perfect query, but in knowing when to stop — and when to keep going."

## Related Articles

- [[Awesome Search/Articles/Distilling Retrieval Pipelines to a Single Embedding Model]] — same author, retrieval efficiency
- [[Symmetric vs. Asymmetric Semantic Search]] — retrieval mechanics agents use
- [[Nearest Neighbor Indexes for Similarity Search]] — infrastructure for agentic retrieval

## Related Concepts

- [[Agentic Search]] — primary topic
- [[Bag-of-Documents Model]] — theoretical framing
- [[Retrieval Pipeline]] — what the agent orchestrates
- [[RAG]] — downstream use of agentic retrieval
- [[Hybrid Search]] — common retrieval strategy within agents
