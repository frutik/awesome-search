---
title: Clean Context
aliases:
  - clean context
  - context hygiene
  - defensive retrieval
tags:
  - concept
  - agentic-search
  - retrieval
  - rag
---

# Clean Context

## Definition

**Clean context** is the principle that an LLM's context window should contain only genuinely useful, non-distracting content. In RAG and agentic retrieval systems, "clean context" means the retrieved documents are all relevant and none of them mislead the model toward incorrect reasoning.

The concept emerges from the recognition that **context injection is fundamentally different from search result presentation**: a human can skip a bad result, but an LLM processes all injected content in parallel and cannot selectively ignore it.

## The Problem: Context Contamination

When distractors — plausible but misleading passages — enter the context window:
- The model's attention anchors on wrong evidence
- Chain-of-thought reasoning **degrades**, not improves (inverse scaling under noise)
- In agentic loops, errors at step `t` propagate into context at step `t+1`, compounding with each iteration

A system with 90% per-step accuracy degrades to ~53% accuracy after 6 steps under context contamination.

Key finding: padding context with *random* noise can improve accuracy, because random noise increases attention entropy. **Distractors are worse than noise** — they are plausible enough for attention to sharpen around wrong evidence.

## Achieving Clean Context

### Retrieval Side
- Use **precision-first** strategies — fewer, higher-confidence documents over large recall
- **Dynamic-k**: stop retrieving when marginal utility drops below threshold
- **Abstention**: if no document meets confidence threshold, return nothing rather than inject uncertain content
- Evaluate retrieval with [[UDCG]] rather than [[NDCG]] to explicitly penalize distractor injection
- [[Reranking]] with context-aware models that distinguish relevant from plausible-but-wrong

### Generation Side
- **Context summarization**: compress retrieved passages before injection to reduce noise surface
- **Faithfulness checking**: verify generated output is grounded in injected context
- **[[LLM as Judge]]** to evaluate whether context was actually used correctly

## Clean Context vs. Recall

Standard retrieval optimization maximizes recall — find everything possibly relevant. Clean context optimization maximizes **precision** — inject only what is safely relevant.

The tradeoff:
- High recall, dirty context → high distractor risk, degraded agentic accuracy
- Lower recall, clean context → misses some relevant content, but preserves reasoning quality

For agentic tasks where a wrong answer is worse than no answer, clean context is the correct optimization target.

## Related Concepts

- [[UDCG]] — the evaluation metric that explicitly penalizes dirty context
- [[Agentic Search]] — the primary domain where clean context matters
- [[RAG]] — the retrieval-augmented generation pipeline that injects context
- [[Reranking]] — the stage where context can be cleaned before injection
- [[Precision and Recall]] — the fundamental tradeoff clean context navigates

## Related Articles

- [[Mutually Assured Distraction]] — primary source for this concept
