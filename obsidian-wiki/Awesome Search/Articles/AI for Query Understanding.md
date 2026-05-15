---
title: "AI for Query Understanding"
source: "https://www.linkedin.com/pulse/ai-query-understanding-daniel-tunkelang"
author: ["Daniel Tunkelang"]
tags:
  - clippings
  - query-understanding
  - ai
  - llm
  - search
concepts:
  - Query Understanding
  - Search Intent
  - Agentic Search
created: 2026-05-15
---

# AI for Query Understanding

**Source**: https://www.linkedin.com/pulse/ai-query-understanding-daniel-tunkelang  
**Author**: [[Daniel Tunkelang]]

## Summary

[[Daniel Tunkelang]] argues that LLMs fundamentally change [[Query Understanding]] — not by replacing existing NLP pipelines entirely, but by enabling new capabilities in intent classification, entity understanding, and contextual interpretation that were previously impractical.

## LLMs vs. Traditional Query Understanding

Traditional QU pipeline:
```
Spell correction → tokenizer → NER → intent classifier → entity linker
```
Each component: separate model, separate training data, separate failure modes.

LLM-based QU:
```
prompt(query + context) → LLM → structured interpretation
```
One model handles all three of Tunkelang's parts ([[Query Understanding - Divided into Three Parts]]).

## What LLMs Enable

### Zero-Shot Intent Classification
```python
response = llm.generate(f"""
Classify this search query's intent:
Query: "best running shoes for wide feet under $100"

Options: navigational, informational, transactional, comparative

Return the label and confidence.""")
# → "transactional, 0.92"
```

No training data required for new domains.

### Entity Understanding with Context
LLMs understand "Python" means programming in a developer context, reptile in a zoo search context — without domain-specific disambiguation training.

### Conversational Query Interpretation
Multi-turn session:
- Q1: "mountain bikes"
- Q2: "under 1000"
- Q3: "full suspension"

LLM correctly interprets Q3 as "full suspension mountain bikes under $1000" (coreference resolution across turns).

Traditional systems require explicit session state tracking; LLMs handle it natively.

### Query Rewriting
```python
rewritten = llm.generate(f"""
Rewrite this search query to be more retrievable:
Original: "phone case that doesnt break when dropped"
Improved: ?
""")
# → "shockproof protective phone case drop resistant"
```

## Limitations and Cautions

1. **Latency**: LLM inference (50–200ms) adds to query time — acceptable for voice/complex queries, problematic for instant search
2. **Cost**: LLM API calls per query add up at scale
3. **Consistency**: LLMs can produce different interpretations for the same query — use structured output (JSON) to enforce consistency
4. **Hallucination in entities**: LLM may link "Cortana" to both the AI assistant and Halo character without domain grounding

## Hybrid Approach (Recommended)

Don't replace all QU with LLMs:

| Task | Recommended Approach |
|------|---------------------|
| Spell correction | Traditional (fast, reliable) |
| Common intent classes | Fine-tuned classifier (fastest) |
| Ambiguous/complex intent | LLM |
| Conversational queries | LLM (mandatory) |
| Entity linking | LLM + knowledge base |

## Connection to [[Agentic Search]]

AI-powered query understanding is a prerequisite for [[Agentic Search]]:
- Agent needs to understand multi-turn intent evolution
- Agent reformulates queries — LLM-powered reformulation is natural
- Agent verifies sufficiency — requires understanding what "sufficient" means for the query

## Related Articles

- [[Query Understanding - Introduction]] — foundational framework
- [[Agentic Search as an Agile Engineering Process]] — downstream application
- [[Mapping Search Queries To Search Intents]] — intent classification deep-dive

## Related Concepts

- [[Query Understanding]] — primary topic
- [[Search Intent]] — key component
- [[Agentic Search]] — where LLM-based QU leads
- [[RAG]] — LLM-powered query understanding improves RAG retrieval
- [[Bag-of-Documents Model]] — LLM interprets query as document distribution

## People

- [[Daniel Tunkelang]] — author
