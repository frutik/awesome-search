---
type: article
title: "Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity"
source: https://aclanthology.org/2024.naacl-long.389/
author:
  - Soyeong Jeong
  - Jinheon Baek
  - Sukmin Cho
  - Sung Ju Hwang
  - Jong C. Park
published: 2024-03-21
tags:
  - article
  - paper
  - rag
  - query-routing
  - adaptive-retrieval
  - naacl
concepts:
  - "[[Query Routing]]"
  - "[[Adaptive Retrieval]]"
  - "[[RAG]]"
  - "[[BM25]]"
  - "[[FLAN-T5]]"
topics:
  - "[[Query Classification]]"
created: 2026-09-26
---

# Adaptive-RAG: Learning to Adapt Retrieval-Augmented LLMs through Question Complexity

**Authors:** Soyeong Jeong, Jinheon Baek, Sukmin Cho, Sung Ju Hwang, Jong C. Park (KAIST)
**Venue:** NAACL 2024 · [arXiv 2403.14403](https://arxiv.org/abs/2403.14403) · [code](https://github.com/starsuzi/Adaptive-RAG)

## Summary

The route here is not *which source* but *how much retrieval*. Real traffic mixes trivial questions ("Paris is the capital of what?") with multi-hop ones, and a single strategy is wrong for one end or the other: multi-step retrieval wastes time on simple questions, single-step or no retrieval fails on complex ones. Adaptive-RAG puts a small classifier in front that predicts a question's **complexity** and routes it to one of three strategies:

| Label | Strategy |
|---|---|
| **A** | No retrieval — the LLM answers alone |
| **B** | Single-step retrieval, then answer |
| **C** | Multi-step: interleaved retrieval and reasoning over several rounds |

It is the canonical reference for [[Adaptive Retrieval]] as a routing problem, and the mapping later borrowed by [[Lightweight Query Routing for Adaptive RAG - A Baseline Study on RAGRouter-Bench|RAGRouter-Bench baselines]].

## Labels Without Annotators

No dataset labels question complexity, so labels are derived automatically in two passes:

1. **From outcomes** — run all three strategies; label a question with the *simplest* strategy that answers it correctly (if no-retrieval is right → A; if only the retrieval strategies are right → B; only multi-step → C).
2. **From dataset bias** — questions all three strategies fail on are labelled B if they come from a single-hop dataset and C if from a multi-hop one.

The classifier is **T5-Large (770M)** trained with cross-entropy on these pairs.

## Setup and Results

Single-hop: SQuAD v1.1, [[Natural Questions]], TriviaQA. Multi-hop: MuSiQue, HotpotQA, 2WikiMultiHopQA — mixed together to simulate varied traffic. Retriever: [[BM25]]. Generators: [[FLAN-T5]]-XL and -XXL, and GPT-3.5.

With GPT-3.5, averaged over all six datasets:

| Method | F1 | Time per query (relative to single-step) |
|---|---|---|
| No retrieval | 48.56 | 0.71 |
| Single-step | 46.99 | 1.00 |
| Multi-step | 50.87 | 3.33 |
| **Adaptive-RAG** | **50.91** | **1.46** |

Adaptive-RAG matches the always-multi-step system at well under half its time, and beats the prior adaptive methods (entity-frequency-based adaptive retrieval and Self-RAG) in the same table. An oracle classifier would do better still (F1 56.28 with FLAN-T5-XL), which is the headroom the authors point to.

## The Router Is Not Very Accurate

The classifier's overall accuracy is only **54.52%**. Its errors are telling: about 47% of no-retrieval questions are pushed to single-step, and multi-step and single-step questions are confused with each other in roughly a quarter to a third of cases. Most mistakes err toward *more* retrieval than necessary — costly but rarely fatal — which is why a weak router still pays. Larger classifiers help only modestly (60M → 770M: accuracy 53.48% → 54.52%).

## Caveats

- Open-domain QA benchmarks only; "complexity" is defined by which of three fixed strategies succeeded, not by any property of the question.
- Automatic labels are one instantiation and may mislabel; the authors flag both the labels and the classifier architecture as the main room for improvement.

## Related Concepts

- [[Adaptive Retrieval]] — the idea this paper makes a trained router
- [[Query Routing]] · [[Query Classification]] — routing by predicted complexity
- [[RAG]] · [[BM25]] · [[FLAN-T5]]

## Related Notes

- [[Lightweight Query Routing for Adaptive RAG - A Baseline Study on RAGRouter-Bench]] — reuses this complexity-to-strategy mapping
- [[LTRR - Learning To Rank Retrievers for LLMs]] — also treats "no retrieval" as a first-class route
- [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]] — another router where an imperfect classifier still beats a one-size-fits-all default
