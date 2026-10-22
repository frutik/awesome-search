---
title: "BlitzRank - Principled Zero-shot Ranking Agents with Tournament Graphs"
type: article
tags: [article, reranking, llm, paper, benchmark]
source: "https://arxiv.org/abs/2602.05448"
author:
  - "[[Sheshansh Agrawal]]"
  - "[[Thien Hang Nguyen]]"
  - "[[Douwe Kiela]]"
published: 2026-02-05
created: 2026-10-22
concepts:
  - "[[BlitzRank]]"
  - "[[Reranking]]"
  - "[[RankGPT]]"
  - "[[Listwise Relevance Evaluation]]"
  - "[[Pairwise Relevance Evaluation]]"
  - "[[LLM as Judge]]"
  - "[[NDCG]]"
  - "[[BM25]]"
topics:
  - "[[Reasoning Reranking]]"
companies:
  - "[[Contextual AI]]"
datasets:
  - "[[TREC Deep Learning Track]]"
  - "[[BEIR]]"
  - "[[TREC-COVID]]"
---

# BlitzRank - Principled Zero-shot Ranking Agents with Tournament Graphs

**Source:** https://arxiv.org/abs/2602.05448 (v1 2026-02-05, v4 2026-05-25; arXiv comment: "ICML 2026 spotlight")
**Authors:** [[Sheshansh Agrawal]], [[Thien Hang Nguyen]], [[Douwe Kiela]] ([[Contextual AI]])
**Code:** https://github.com/ContextualAI/BlitzRank (MIT) · `pip install blitzrank`

## Summary

The paper introduces [[BlitzRank]], an LLM [[Reranking|reranker]] built on one observation: when an LLM ranks a window of *k* documents, that single answer settles every one of the k(k−1)/2 pairs inside the window. BlitzRank keeps all those preferences in one graph and uses transitive closure to infer orderings it never asked about. It then picks the next comparisons until the top-*m* results are provably settled. The headline is cost. Across 14 benchmarks it matches the most expensive baseline's quality at a fraction of the tokens.

## Method

- **Problem framing.** Select the top *m* of *n* items with an oracle that compares up to *k* at a time. Each call returns a small tournament.
- **Revealed graph.** Every returned preference is an edge. If A reaches C through any path, A ≻ C counts as known even though that pair was never shown together.
- **Resolved items and stopping.** An item is resolved once its relation to all other items is implied. The algorithm stops when the current top *m* are all resolved, and the output is then certified correct for the oracle's tournament.
- **Scheduling.** Each round queries one representative from each of the *k* earliest unresolved groups. A tie-breaking heuristic (used in all experiments) prefers the items with the fewest known relationships.
- **Cycles.** Non-transitive judgments (A ≻ B ≻ C ≻ A) are collapsed into tied tiers, so the result is a tiered ranking rather than a forced total order.
- **The oracle in practice.** The LLM gets a [[RankGPT]]-style listwise prompt, and its permutation is read as the full tournament on that window.
- **Theory.** Correctness and termination are proved. Top-1 needs at most ⌈(n−1)/(k−1)⌉ queries. The bound for general *m* is a conjecture, not a proof. As a sanity check it solves the classic 25-horses puzzle (n=25, k=5, m=3) in the optimal 7 queries.

## Experiments

[[BM25]] retrieves the top 100 per query. The 14 datasets are six [[TREC Deep Learning Track|TREC DL]] sets (DL19–DL23, DL-Hard) and eight [[BEIR]] sets ([[TREC-COVID]], NFCorpus, Signal-1M, News, Robust04, Touché, DBPedia, SciFact). Five LLMs act as the oracle: GPT-4.1, Gemini-3-Flash, GLM-4.7, DeepSeek-V3.2 and Qwen3-235B-A22B-Instruct. Results are reported as [[NDCG|nDCG@10]] and input tokens per query, with m=10.

Macro-average over the 14 datasets, GPT-4.1 and Gemini-3-Flash:

| Method | nDCG@10 | Tokens / query |
|---|---|---|
| BM25 (no rerank) | 41.1 | 0 |
| Pairwise | 57.0 | 324k |
| Setwise | 56.6 | 115k |
| Sliding window ([[RankGPT]]-style) | 56.7 | 54k |
| TourRank | 56.0 | 57k |
| AcuRank-H | 56.6 | 127k |
| **BlitzRank, k=10** | **56.9** | **42k** |
| BlitzRank, k=20 | 56.4 | 40k |

- **The win is tokens, not quality.** BlitzRank is within 0.1 nDCG of the Pairwise baseline (which aggregates LLM pair comparisons by sorting) at about one-eighth of the tokens. The quality gaps between methods are fractions of a point, and no significance tests are reported.
- **Smaller windows were better.** k=10 beat k=20 for every oracle. The authors connect this to larger windows producing more cyclic judgments, which suggests a single long listwise answer is a less reliable source of pairwise preferences.
- **Fewer calls.** About 6.5 LLM calls per query, against 9 for the sliding window and 13 for TourRank and AcuRank. At k=10 it converged in 12–15 rounds.
- **Cycles group look-alikes.** Documents tied in a cycle had more similar BM25 scores than neighbouring groups did, which suggests the LLM struggles to separate near-duplicates.

## Limitations

- **Deterministic oracle.** The framework assumes each comparison has one fixed outcome. Real LLMs are noisy. The authors note that a single wrong edge can collapse a long chain into one tie, and they call principled noise handling an open problem. Nothing in the method repeats or votes on comparisons.
- **Top-m only.** It certifies the top 10, not a full ordering of the 100 candidates.
- **Reranking only.** Every experiment is reranking against TREC/BEIR judgments. The paper does not test BlitzRank output as relevance labels for [[Search Evaluation]], and it does not compare against pointwise rubric [[LLM as Judge|judges]].
- **No product-search data.** The benchmarks are web, news and scientific collections.

## Reception

[[Doug Turnbull]] promoted the paper on LinkedIn on 2026-10-22 as "the sweet spot of LLM Judge quality / cost in search". He framed it as a cheaper road to [[Pairwise Relevance Evaluation|pairwise judging]], which takes 45 comparisons for 10 results, or 90 when checking both orders. The post announced a Nov 11 guest lecture, "Evals with Blitzrank", by William Barber of [[turbopuffer]] in the *AI-Powered Search* course ([[Courses]]). The evaluation use the post describes goes beyond what the paper tests. And where the post talks about extra comparisons "to gain confidence", the scheduler actually targets pairs whose order is still unknown; it does not measure uncertainty.

## Related Concepts

- [[BlitzRank]] — the method
- [[RankGPT]] — the listwise prompt used as BlitzRank's oracle, and the sliding-window baseline it beats on cost
- [[Listwise Relevance Evaluation]] · [[Pairwise Relevance Evaluation]] — BlitzRank reads one listwise answer as many pairwise ones
- [[Reranking]] · [[LLM as Judge]] · [[NDCG]] · [[BM25]]

## Related Notes

- [[Reasoning Reranking]]
- [[Contextual AI]]
- [[TREC Deep Learning Track]] · [[BEIR]]

## People

- [[Sheshansh Agrawal]] · [[Thien Hang Nguyen]] · [[Douwe Kiela]]
- [[Doug Turnbull]]
