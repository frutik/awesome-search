---
type: concept
aliases: ["Maximal Marginal Relevance", "maximal marginal relevance"]
tags: [concept, diversity, metrics, reranking]
related: ["[[Diversity Metrics]]", "[[APD]]", "[[Reranking]]", "[[Search Quality Assurance]]"]
created: 2026-05-16
---

# MMR — Maximal Marginal Relevance

> Note: MMR (Maximal Marginal Relevance) is a **diversity metric and reranking strategy**. Do not confuse with [[MRR]] (Mean Reciprocal Rank), a ranking quality metric.

A reranking method that balances relevance and novelty. Instead of ranking purely by relevance, MMR penalizes results that are similar to already-selected results — reducing redundancy while preserving quality.

## Formula

$$\text{MMR} = \arg\max_{d_i \in R \setminus S} \left[ \lambda \cdot \text{Sim}_1(d_i, q) - (1 - \lambda) \cdot \max_{d_j \in S} \text{Sim}_2(d_i, d_j) \right]$$

Where:
- $R$ = candidate result set
- $S$ = already-selected results
- $q$ = query
- $\text{Sim}_1$ = query-document relevance (e.g., cosine similarity)
- $\text{Sim}_2$ = document-document similarity
- $\lambda$ = tradeoff parameter (0 = pure diversity, 1 = pure relevance)

## Algorithm

Greedy iterative selection:
1. Select the most relevant document as the first result
2. For each subsequent position, pick the document that maximizes the MMR score — highest relevance minus penalty for similarity to already-chosen documents
3. Repeat until the result list is full

## Properties

- **Tunable**: λ controls the relevance/diversity tradeoff
- **Greedy**: not globally optimal, but O(n) per step — practical for reranking
- **Similarity-agnostic**: works with any similarity function (BM25 score, embedding cosine, etc.)

## Use Cases

- **Search result diversification**: reduce ten near-duplicate product results in favor of different categories
- **Keyphrase extraction**: select diverse keyphrases from a document rather than all from the same topic cluster
- **RAG context selection**: choose diverse passages for LLM context to avoid redundant information
- **Facet result pages**: ensure different facet values are represented in top results

## Tradeoffs

| Relevance-focused (λ→1) | Diversity-focused (λ→0) |
|---|---|
| Top results are most relevant | Top results cover more aspects |
| May show redundant content | May surface lower-relevance items |
| Better for known-item search | Better for exploratory / ambiguous queries |

## Related

- [[APD]] — Average Pairwise Distance, a passive diversity measurement (vs MMR's active reranking)
- [[Diversity Metrics]] — overview of diversity approaches
- [[Reranking]] — MMR is applied as a post-retrieval reranking step
