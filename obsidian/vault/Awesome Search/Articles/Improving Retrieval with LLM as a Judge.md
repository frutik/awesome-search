---
title: "Improving Retrieval with LLM-as-a-Judge"
source: "https://blog.vespa.ai/improving-retrieval-with-llm-as-a-judge/"
author: ["Vespa"]
tags:
  - clippings
  - search-evaluation
  - llm-judge
  - retrieval
  - vespa
concepts:
  - LLM as Judge
  - Search Evaluation
  - Dense Vector Retrieval
  - NDCG
created: 2026-05-15
---

# Improving Retrieval with LLM-as-a-Judge

**Source**: https://blog.vespa.ai/improving-retrieval-with-llm-as-a-judge/  
**Publisher**: Vespa

## Summary

Vespa demonstrates using an LLM as an automated relevance judge to evaluate first-stage retrieval quality, showing that LLM judgments correlate strongly with human judgments and enable rapid iteration without expensive annotation rounds.

## The Problem: Manual Evaluation is a Bottleneck

Improving retrieval systems requires evaluation. But:
- Human annotation: $1–5 per (query, document) pair
- For 500 queries × 10 candidates: $5,000–$25,000
- Turnaround: 1–2 weeks per evaluation cycle
- Iteration speed: blocks rapid experimentation

LLM judges enable evaluation in minutes at cents per query.

## Vespa's LLM Evaluation Approach

### Step 1: Generate Ideal Answer
For each query, use an LLM to generate what an ideal answer would contain:
```python
ideal_answer = llm.generate(
    f"For the query '{query}', describe what an ideal answer would contain."
)
```

### Step 2: Judge Document Relevance
For each retrieved document, ask the LLM to assess relevance:
```python
grade = llm.generate(
    f"""Query: {query}
    Ideal answer characteristics: {ideal_answer}
    Document: {document}
    
    Rate relevance 0-3:
    0: Not relevant
    1: Marginally relevant
    2: Relevant  
    3: Highly relevant
    
    Return only the integer."""
)
```

### Step 3: Compute NDCG from LLM Grades
Standard [[NDCG]] computation with LLM grades as relevance labels.

## Correlation with Human Judgments

Vespa validates LLM judges against human annotations:
- **Spearman's ρ ≈ 0.87** (system-level ranking correlation)
- LLM judges agree with humans on system ranking in 85%+ of comparisons
- Diverge most on ambiguous/subjective queries

## Using LLM Judges for Rapid Experimentation

With LLM judges, the retrieval experimentation loop becomes:
```
1. Change retrieval parameter (chunk size, model, index)
2. Run queries (< 1 minute)
3. LLM judges candidates (< 5 minutes, $2–10)
4. Compute NDCG (< 1 minute)
5. Compare to baseline
```

Iteration time: 10 minutes vs. 2 weeks for human annotation.

## Limitations Observed

1. **Verbose documents preferred**: LLM judges often favor longer, more comprehensive documents even when a short precise answer is better
2. **Factually hallucinated judgments**: LLM "remembers" facts not in the document, rates it highly anyway
3. **Domain-specific failure**: LLM may lack domain knowledge to judge specialized content (legal, medical, financial)

## Recommendation

Use LLM judges for:
- **Rapid prototyping**: direction of improvement before investing in human annotation
- **Continuous evaluation**: automated quality gates in CI/CD
- **Regression testing**: catch quality regressions between releases

Don't use LLM judges alone for:
- Final pre-launch decisions (supplement with human annotation)
- Highly specialized domains where LLM knowledge is limited

## Related Articles

- [[Evaluating Search - Using Human Judgments]] — human annotation counterpart
- [[What Is a Judgment List]] — judgment list fundamentals
- [[Announcing the Vespa ColBERT Embedder]] — same publisher, retrieval quality

## Related Concepts

- [[LLM as Judge]] — primary concept
- [[Search Evaluation]] — context
- [[NDCG]] — metric computed from LLM grades
- [[Judgment Lists]] — LLM judgments as alternative
- [[Dense Vector Retrieval]] — retrieval being evaluated

## People

- [[Jo Kristian Bergum]] — Vespa Chief Scientist (likely involved)
