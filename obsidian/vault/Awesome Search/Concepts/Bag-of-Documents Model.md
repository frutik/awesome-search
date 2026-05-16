---
title: "Bag-of-Documents Model"
aliases: ["bag of documents", "document distribution model", "query as document distribution"]
tags:
  - concept
  - search
  - information-retrieval
  - query-understanding
---

# Bag-of-Documents Model

## Definition

The Bag-of-Documents Model, proposed by [[Daniel Tunkelang]], models a search query as a **probability distribution over the set of relevant documents**, rather than as a string of terms or a single embedding vector.

This is a generalization of traditional probabilistic retrieval (like language modeling approaches) that treats the query's "meaning" as the entire set of documents that would satisfy it.

## Formal Framing

Instead of:
```
query → embedding → nearest neighbor documents
```

The Bag-of-Documents Model says:
```
query → probability distribution P(d | q) over all documents
```

The retrieval task is to find documents with high P(d | q).

## Why This Framing Matters

### 1. Captures Query Ambiguity
A query like "python" has mass over documents about:
- The programming language
- The snake
- Monty Python

The distribution captures this ambiguity naturally; a single embedding vector cannot.

### 2. Enables Non-obvious Connections
Documents that rarely match the query's literal terms but are frequently relevant (based on click patterns, co-occurrence, or semantic relatedness) get appropriate probability mass.

### 3. Integrates Multiple Signals
The distribution P(d | q) can be estimated from:
- BM25 / sparse retrieval scores
- Dense embedding similarity
- Behavioral signals (clicks, purchases)
- Structured metadata

## Relation to [[Wormhole Vectors]]

While [[Trey Grainger]]'s [[Wormhole Vectors]] take a geometric approach (bridging vector spaces), the Bag-of-Documents Model takes a probabilistic approach. Both address the same fundamental problem: a query has meaningful connections across multiple retrieval spaces, and a single-space model misses them.

## Empirical Results

Tunkelang reports +37.9% Recall@10 improvement over standard single-space retrieval in experiments using the Bag-of-Documents framing with multi-signal fusion.

## Connection to [[Agentic Search]]

In [[Agentic Search]], the agent's planning process can be viewed as iteratively refining the document distribution:
1. Initial query → broad distribution
2. Retrieved docs reveal what the "real" distribution should be
3. Agent reformulates → sharper distribution
4. Repeat until convergence

This makes the Bag-of-Documents Model a theoretical foundation for multi-turn agentic retrieval.

## Practical Implications

| Traditional Search | Bag-of-Documents |
|-------------------|------------------|
| Point estimate (top-k) | Distribution (all docs with non-zero mass) |
| Single retrieval space | Multi-space fusion |
| Static ranking | Iterative refinement |
| Fixed query interpretation | Ambiguity-aware |

## Related Concepts
- [[Embeddings]] — parent concept; query as a distribution over document embeddings
- [[Dense Embeddings]] — the centroid vector is a dense embedding
- [[Sparse Embeddings]] — sparse component feeds the document distribution

- [[Agentic Search]] — iterative refinement aligns with distribution narrowing
- [[Wormhole Vectors]] — geometric cousin
- [[Hybrid Search]] — multi-signal fusion feeds the distribution
- [[Semantic Search]] — dense component
- [[Sparse Vector Retrieval]] — sparse component
- [[Dense Vector Retrieval]] — dense component

## People

- [[Daniel Tunkelang]] — invented and advocates for Bag-of-Documents Model; QueryUnderstanding.com
