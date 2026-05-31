---
title: "Listwise Relevance Evaluation"
aliases: ["listwise evaluation", "listwise ranking", "list-level evaluation"]
tags:
  - concept
  - search-evaluation
  - llm-judge
---

# Listwise Relevance Evaluation

## Definition

A relevance judgment method where an evaluator receives a **full list of candidates** for a query and produces a ranked ordering or set of grades over all items simultaneously. Unlike [[Pointwise Relevance Evaluation]] (one item at a time) or [[Pairwise Relevance Evaluation]] (two items at a time), listwise evaluation reasons about the entire result set in context.

## How It Works

```
Query: "entrance table"
Candidates:
  1. aleah coffee table
  2. slim console table for entryways
  3. marta side table

→ Ranked order: [2, 3, 1]
  or
→ Graded list: [Highly Relevant, Partially Relevant, Not Relevant]
```

## LLM Listwise Prompt Pattern

```
Rank these documents from most to least relevant to the query.

Query: {query}

Documents:
[A] {doc_1}
[B] {doc_2}
[C] {doc_3}

Return the document letters in ranked order, most relevant first.
```

## Strengths

- **Holistic**: LLM sees all candidates simultaneously — can make relative distinctions that pointwise misses
- **Efficient at inference**: one LLM call judges k documents (vs. k calls pointwise, or k² calls pairwise)
- **Natural for reranking**: matches how rerankers actually operate
- Avoids calibration issues of absolute grades

## Weaknesses

- **Context window pressure**: large candidate sets may exceed token limits or degrade quality
- **Position bias**: LLMs tend to favor items appearing early in the list
- **Inconsistency at scale**: hard to aggregate judgments across queries when list composition varies
- Less interpretable than pairwise — hard to know *why* item A beat item B

## Connection to Learning to Rank

In [[Learning to Rank]], listwise loss functions (e.g. LambdaMART) optimize ranking metrics (NDCG, MAP) directly over full lists, rather than training on individual scores or pairs. Listwise evaluation mirrors this training objective, making it natural for evaluating LTR models.

## Comparison to Other Paradigms

| Paradigm | Input | Output | Scalability | Signal strength |
|---|---|---|---|---|
| [[Pointwise Relevance Evaluation\|Pointwise]] | (query, doc) | absolute grade | O(n) | weakest |
| [[Pairwise Relevance Evaluation\|Pairwise]] | (query, doc_A, doc_B) | preference | O(n²) | strong |
| **Listwise** | (query, [doc_1…doc_k]) | ranked order | O(k per query) | strongest |

## Related Concepts

- [[Pointwise Relevance Evaluation]] — grades items independently; simpler but weaker signal
- [[Pairwise Relevance Evaluation]] — compares two items; LHS/RHS format
- [[LLM as Judge]] — LLM as the ranking agent
- [[Learning to Rank]] — listwise loss functions (LambdaMART) optimize the same objective
- [[NDCG]] — metric that listwise evaluation directly approximates
- [[Reranking]] — production stage where listwise evaluation is most applicable

## Articles

- [[What AI Engineers Should Know about Search]] — [[Doug Turnbull]]; LambdaMART as the canonical listwise LTR algorithm
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; ensemble of pairwise judges as an alternative to full listwise prompting
