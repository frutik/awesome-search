---
title: "Pointwise Relevance Evaluation"
aliases: ["pointwise evaluation", "pointwise scoring", "absolute relevance scoring"]
tags:
  - concept
  - search-evaluation
  - llm-judge
---

# Pointwise Relevance Evaluation

## Definition

A relevance judgment method where each (query, document) pair is scored **independently**, without reference to other candidates. An evaluator — human or LLM — assigns an absolute grade (e.g. 0–3, or Not Relevant / Partially Relevant / Highly Relevant) to each item in isolation.

## How It Works

```
Query: "entrance table"
Document: "aleah coffee table — great for living rooms"
→ Grade: 1 (Partially Relevant)

Query: "entrance table"
Document: "slim console table for entryways"
→ Grade: 3 (Highly Relevant)
```

Each judgment is independent. The resulting grades feed directly into metrics like [[NDCG]] or [[MAP]].

## LLM Pointwise Prompt Pattern

```
Rate the relevance of this document to the query on a scale of 0–3:
  0 = Not relevant
  1 = Marginally relevant
  2 = Relevant
  3 = Highly relevant

Query: {query}
Document: {document}

Return only the integer grade.
```

## Strengths

- Simple and scalable — one LLM call per (query, doc) pair
- Output feeds directly into standard IR metrics
- No need to retrieve multiple candidates simultaneously
- Easy to cache and parallelize

## Weaknesses

- **Calibration variance**: different annotators (human or LLM) interpret grade boundaries differently
- **No relative signal**: harder to detect subtle preference between two similar documents
- **Position/length bias** in LLM judges is harder to detect without a reference point
- Absolute scores are less reliable than relative preferences — see [[Pairwise Relevance Evaluation]]

## Comparison to Other Paradigms

| Paradigm | Input | Output | Scalability | Signal strength |
|---|---|---|---|---|
| **Pointwise** | (query, doc) | absolute grade | O(n) | weakest |
| [[Pairwise Relevance Evaluation\|Pairwise]] | (query, doc_A, doc_B) | preference | O(n²) | strong |
| [[Listwise Relevance Evaluation\|Listwise]] | (query, [doc_1…doc_k]) | ranked order | O(k per query) | strongest |

## Related Concepts

- [[Pairwise Relevance Evaluation]] — compares two items; stronger signal, higher cost
- [[Listwise Relevance Evaluation]] — ranks full list; most holistic
- [[LLM as Judge]] — LLM as the scoring agent
- [[Judgment Lists]] — output product of pointwise evaluation
- [[NDCG]] — primary metric consuming pointwise grades
- [[Learning to Rank]] — uses pointwise labels as one training signal type

## Articles

- [[What AI Engineers Should Know about Search]] — [[Doug Turnbull]]; points 3–11 cover judgment methodology; points 42–43 contrast pointwise grading vs. pairwise/listwise LTR
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; contrasts forced pointwise scoring vs. pairwise comparison; pairwise wins on precision
