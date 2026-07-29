---
type: article
title: "Relevance Feedback in Qdrant"
author: "[[Evgeniya Sukhodolskaya]]"
company: "[[Qdrant]]"
published: 2026-02-20
source: "https://qdrant.tech/articles/relevance-feedback/"
tags:
  - article
  - relevance-feedback
  - vector-search
  - hnsw
  - reranking
  - benchmarks
topics:
  - "[[Reasoning Reranking]]"
  - "[[Conversational and Agentic Search]]"
concepts:
  - "[[Relevance Feedback]]"
  - "[[HNSW]]"
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Dense Vector Retrieval]]"
  - "[[Reranking]]"
  - "[[Cross-Encoder]]"
  - "[[ColBERT]]"
  - "[[Late Interaction]]"
  - "[[Knowledge Distillation]]"
datasets:
  - "[[BEIR]]"
  - "[[MS MARCO]]"
tools:
  - "[[qdrant-relevance-feedback]]"
  - "[[Qdrant Vector DB]]"
created: 2026-07-29
---

# Relevance Feedback in Qdrant

📄 **Source:** https://qdrant.tech/articles/relevance-feedback/

## Summary

The mechanism behind [[Qdrant]] 1.17's `RelevanceFeedbackQuery`, and the evidence for it. Where the companion survey [[Relevance Feedback in Informational Retrieval]] argues that [[Relevance Feedback]] can only be solved *inside* the retrieval system, this article builds that solution: a scoring formula that replaces plain query similarity during [[HNSW]] traversal, so a feedback model's judgement reaches the whole collection instead of a retrieved top-k.

The talk [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] gives the argument without the maths; this note carries the formula, the training procedure, and the [[BEIR]] numbers.

## The Framing: Relevance Direction

A feedback model cannot map the entire vector space — running a [[Cross-Encoder]] or LLM over millions of documents is exactly what nobody can afford. But it *can* say which direction is better from where you stand. The article's analogy is a hiker in a forest with a guide who knows the terrain locally: move toward the positive examples, away from the negative ones.

> *"That implies warping the notion of 'closer' and 'further', the distance (or similarity) **scoring metric** used during the retrieval."*

Three stated production requirements shape the design:

| Requirement | Meaning |
|---|---|
| **Cheap** | Feedback on very few documents; automated; no human labeling |
| **Universal** | Any data type, tolerant of noisy signals |
| **Scalable** | Traverses the entire vector space, not a result subset |

The third is the differentiator. Conventional [[Reranking]] can only reorder what the first pass returned; this rescores during traversal.

## The Method

Four steps: initial retrieval → collect a little feedback on the top results → extract the signal into a new similarity formula → run a second retrieval over the whole dataset with that formula.

### Context pairs

From the top-K initial results, form **(positive, negative)** pairs — two documents the feedback model scored differently. The pair encodes a direction, not an absolute judgement, which is what makes weak or noisy feedback usable.

### The formula

```
F = a · score + Σ_pairs confidence_p^b · c · delta_p
```

| Term | Definition | When computed |
|---|---|---|
| `score` | Retriever's own similarity (e.g. cosine) between query and candidate | Second retrieval |
| `confidence` | Gap in the feedback model's scores between the pair's positive and negative — e.g. `0.99 − 0.70 = 0.29` | After initial retrieval |
| `delta` | `cos(positive, candidate) − cos(negative, candidate)` — is this candidate more like the good example or the bad one? | Second retrieval |
| `a`, `b`, `c` | Trained parameters: weight on the original retriever, sharpness of confidence, strength of the directional pull | Fitted once, offline |

The edge cases justify the shape. If `delta = 0` the candidate is equidistant from both poles and the formula defers to the retriever; if `confidence = 0` the pair carries no signal and again the retriever dominates. Exponentiating confidence by `b` keeps it from collapsing into a single joint term with `delta`.

Sukhodolskaya is explicit this is provisional: *"Is this formula set in stone? Absolutely not! We tried three others in experiments, and this one was the simplest that worked."* Custom formulas are planned.

### Training

Parameters are fitted by **pairwise ranking loss** on domain queries — once per *(feedback model, collection, retriever)*, never per query. Setup: feedback scored on the top 100 documents per query, context limit K=5, top-1 pair by confidence during training, lr 0.005, up to 2000 epochs with early stopping (patience 200), 50/50 train/validation.

At inference, K=3 and *all* pairs are used by confidence rank — using multiple pairs at test time beats the single pair used in training.

## Experiments

**Datasets** — five [[BEIR]] subsets: NFCorpus (3.6K docs), SCIDOCS (25K), FiQA-2018 (57K), Quora (523K), [[MS MARCO]] (8.84M). Training queries range 223 (NFCorpus) to 6000 (Quora).

**Retrievers** — jina-embeddings-v2-base-en (768d), mxbai-embed-large-v1 (1024d), Qwen3-Embedding-0.6B (1024d).

**Feedback models** — mxbai-embed-large-v1, Qwen3-Embedding-0.6B, Qwen3-Embedding-4B (2560d), and colBERTv2.0 ([[ColBERT]], [[Late Interaction]]).

### The metric: `abovethreshold@N`

A custom relevance-recall metric, because the question isn't "is the ranking good" but:

> *"On the next retrieval iteration, can our feedback-based formula pull more relevant documents into the top N than the vanilla retriever did?"*

Take the highest feedback score among the top-K used for mining pairs as a threshold. Any document *outside* top-K scoring above it is "desired" — genuinely more relevant than the retriever realised. Count how many desired documents each method lands in the window, and report relative gain. A DCG win-rate against the feedback model's scores is reported alongside.

Note what this measures: agreement with the **feedback model**, not with human judgments. The feedback model is the ground truth by construction — consistent with the distillation framing, but it means these numbers bound how well the index imitates the judge, not how relevant users find the results.

### Results — relative gain in `abovethreshold@10`

| Retriever → Feedback model | NFCorpus | FiQA-2018 | SCIDOCS | MS MARCO | Quora |
|---|---|---|---|---|---|
| Qwen3-0.6B → colBERTv2.0 | +10.34% | +6.45% | **+38.72%** | +23.23% | +5.04% |
| Qwen3-0.6B → Qwen3-4B | +10.61% | +10.94% | +0.69% | +16.73% | +2.67% |
| mxbai-large-v1 → colBERTv2.0 | +21.57% | +12.24% | +9.55% | +2.40% | 0.00% |
| jina-v2-base → mxbai-large-v1 | +4.62% | −3.90% | +4.55% | +2.57% | 0.00% |
| jina-v2-base → Qwen3-0.6B | −3.85% | −1.59% | +1.62% | +2.23% | −1.37% |
| jina-v2-base → Qwen3-4B | +2.86% | +3.97% | +1.82% | +2.82% | 0.00% |

Full range across the reported pairings: **−3.90% to +38.72%**. This is not a free win — two of the three jina-v2-base rows contain regressions, and Quora is flat or negative for every pairing. But the weak retriever isn't uniformly bad either: paired with the largest feedback model it stays positive throughout, so "low-dimensional retriever ⇒ regression" would overstate it.

## What Governs Whether It Works

1. **The feedback model must disagree with the retriever.** If the judge agrees with the top-K ordering there is no direction to extract and nothing to gain — visible in the flat Quora column.
2. **Retriever expressiveness caps the benefit.** *"The retriever operates in a lower-dimensional space and can't capture all the distinctions the feedback model makes."* jina-v2-base (768d) gains a couple of percent at best where the stronger retrievers gain double digits — a better judge cannot rescue a retriever whose space can't represent the distinction.

## Limitations

- **The experiments simulate.** Feedback scoring ran on 100 documents per query rather than true full-dataset rescoring — *"rescoring humongous datasets like MSMARCO on the user side for every query would not have been fun."* The scalability claim rests on the mechanism, not on these measurements.
- **Training needs real queries.** *"If your use case doesn't involve document-to-document semantic similarity search, training on sampled documents alone may completely cancel the effect."*
- **Positioned as complementary** — *"here not to replace but to complement other search relevance tools"* like MMR, [[Reranking]], or [[Results Boosting]].

## Related

- Concept: [[Relevance Feedback]] — the index-native variant described here
- Survey: [[Relevance Feedback in Informational Retrieval]] — same author; the literature gap this fills
- Talk: [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] — [[Berlin Buzzwords]] 2026
- [[HNSW]] — the traversal being rescored · [[Approximate Nearest Neighbor Search]]
- [[Knowledge Distillation]] — the objective · [[Cross-Encoder]] · [[ColBERT]] · [[Late Interaction]]
- [[BEIR]] · [[MS MARCO]] — evaluation corpora
- Tool: [[qdrant-relevance-feedback]] · [[Qdrant Vector DB]]
