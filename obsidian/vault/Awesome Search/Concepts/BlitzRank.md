---
type: concept
title: "BlitzRank"
aliases: ["Blitz Rank", "Blitzrank", "tournament-graph reranking"]
tags:
  - concept
  - reranking
  - llm
  - ranking
repo: "https://github.com/ContextualAI/BlitzRank"
created: 2026-10-22
---

# BlitzRank

A zero-shot LLM [[Reranking|reranking]] algorithm from [[Contextual AI]]. It treats every listwise LLM call as a small tournament, keeps all the revealed preferences in one graph, and infers further orderings by transitivity. It stops as soon as the top *m* results are provably settled. The name comes from blitz chess, where fast tournament play settles rankings efficiently.

- Paper: [[BlitzRank - Principled Zero-shot Ranking Agents with Tournament Graphs]] (arXiv:2602.05448)
- Code: https://github.com/ContextualAI/BlitzRank (MIT; also on PyPI as `blitzrank`)

---

## How It Works

1. Ask an LLM to order a window of *k* candidates, using a [[RankGPT]]-style listwise prompt.
2. Read the answer as all k(k−1)/2 pairwise preferences inside the window and add them to a global preference graph.
3. Use the transitive closure: if A ≻ B and B ≻ C are both known, A ≻ C is known without asking.
4. Pick the next window from the items whose position is still unresolved, favouring those with the fewest known relationships.
5. Stop when every item in the current top *m* has a known relation to every other candidate.

Contradictory judgments (A ≻ B ≻ C ≻ A) become tied tiers instead of being forced into an order.

## Where It Sits

| Approach | One LLM call gives |
|---|---|
| [[Pointwise Relevance Evaluation\|Pointwise]] | one grade |
| [[Pairwise Relevance Evaluation\|Pairwise]] | one preference |
| Sliding window ([[RankGPT]]) | a window ordering, with survivors carried forward |
| **BlitzRank** | k(k−1)/2 preferences, kept in one graph and extended by transitivity |

Averaged over 14 [[TREC Deep Learning Track|TREC DL]] and [[BEIR]] datasets and two LLMs (GPT-4.1, Gemini-3-Flash), it scored 56.9 nDCG@10 using 42k tokens per query. The paper's Pairwise baseline scored 57.0 using 324k, and the sliding window 56.7 using 54k.

## Caveats

- It assumes a **deterministic oracle**: each comparison is read once and trusted. One wrong LLM judgment can collapse a long chain of inferences into a tie. Handling noisy judges is left open.
- It was published and benchmarked as a **reranker**. Using it to produce preference labels for offline [[Search Evaluation]] has been proposed by practitioners, but the paper does not test it.
- Larger windows gave worse results (k=10 beat k=20), consistent with long listwise answers being less internally consistent.

## Related Concepts

- [[RankGPT]] — the listwise prompt it uses, and the sliding-window baseline
- [[Pairwise Relevance Evaluation]] — what each window is decomposed into
- [[Listwise Relevance Evaluation]] — what each call actually asks
- [[LLM as Judge]] — the oracle role the LLM plays
- [[Reranking]] · [[NDCG]]

## Related Articles

- [[BlitzRank - Principled Zero-shot Ranking Agents with Tournament Graphs]]

## Topics

- [[Reasoning Reranking]]

## People

- [[Sheshansh Agrawal]] · [[Thien Hang Nguyen]] · [[Douwe Kiela]]
- [[Doug Turnbull]] — promoted it as an LLM-judge approach for search evaluation
