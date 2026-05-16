---
title: "Conversational Search"
aliases: ["conversational search", "dialogue-based search", "multi-turn search", "conversational IR", "conversational information retrieval", "chat search"]
tags:
  - concept
  - search
  - query-understanding
  - agentic
created: 2026-05-16
---

# Conversational Search

## Definition

Conversational search is an interaction model where users find information through a multi-turn dialogue rather than a single query. The system maintains context across turns, asks clarifying questions, and refines results based on ongoing conversation.

Distinct from single-query search in that **the query is not a single string** — it's a conversation history.

## Core Challenges

### Coreference and Context Carryover
"Show me laptops under $1000" → "What about ones with 16GB RAM?" — the second query implicitly refers to the first filter set. The system must resolve "ones" to "laptops under $1000."

### Query Rewriting
Each user turn must be rewritten into a standalone query before retrieval. LLMs have made this tractable:
```
Conversation history + new turn → LLM → self-contained query → retrieval
```

### Mixed Initiative
Both user and system can take initiative:
- **User-driven**: user narrows down step by step
- **System-driven**: system asks clarifying questions ([[Query Understanding]] → clarification dialogues)

## Architecture Patterns

### RAG-Based Conversational Search
[[RAG]] with conversation history in the LLM context. User's question + prior turns → query rewriting → retrieval → LLM answer generation. The dominant pattern for LLM-powered search.

### Faceted Dialogue
System presents [[Faceted Search]] options as conversation turns: "Did you mean laptops for gaming or for work?" — structured clarification.

### [[Agentic Search]]
Search agents that decompose complex questions into sub-queries, run multiple searches, and synthesize answers across turns.

## Conversational Search vs. Chatbots

| | Conversational Search | Chatbot |
|---|---|---|
| Primary goal | Information retrieval | Task completion / conversation |
| Truth grounding | Retrieved documents | Model weights |
| Hallucination risk | Lower (grounded) | Higher |
| Failure mode | Poor retrieval | Confabulation |

## Evaluation

Standard single-query metrics ([[NDCG]], [[MRR]]) don't capture multi-turn quality. Additional considerations:
- **Turn-level relevance**: was each response relevant to that turn?
- **Session-level coherence**: did the conversation converge on the user's need?
- **Clarification quality**: did clarifying questions actually help?

[[Session-Based Evaluation]] is most appropriate.

## Related Concepts

- [[Agentic Search]] — overlapping paradigm for complex multi-step retrieval
- [[Query Understanding]] — each turn requires understanding
- [[RAG]] — primary retrieval architecture for conversational search
- [[Faceted Search]] — structured clarification as dialogue
- [[Session-Based Evaluation]] — evaluation must span the full conversation
- [[Search Intent]] — intent can evolve across turns
