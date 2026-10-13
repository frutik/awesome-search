---
type: concept
title: Benchmark Contamination
aliases:
  - train/test contamination
  - test set contamination
  - benchmark leakage
  - training-set contamination
  - benchmark memorization
  - benchmark overfitting
tags:
  - concept
  - evaluation
  - benchmark
  - retrieval
  - search-evaluation
created: 2026-10-13
---

# Benchmark Contamination

Benchmark contamination is when a public benchmark's test data (its corpus, queries, and relevance labels) ends up in a model's training data, deliberately or not. A model that has effectively seen the test posts a score that measures memorization rather than retrieval quality, and that score does not survive contact with new data. [[Retrieval Benchmarks and Leaderboards]] names it the dominant way leaderboards mislead.

---

## How it happens

Open corpus, queries, and labels are good for reproducibility, and the same openness lets the test set leak into training corpora, deliberately or not; the leaderboard rewards the leakage. The result is a **generalization gap**, where reported scores exceed real-world retrieval accuracy on unseen data ([[MTEB]]).

Two benchmarks show the problem from different sides:

- **[[MS MARCO]]** is the training corpus underneath nearly every retrieval model shipped in recent years. Because almost everything trains on it, MS MARCO appearing in an evaluation is a contamination risk in itself.
- **[[BEIR]]** was built to test zero-shot generalization, and it increasingly suffers from contamination: its corpora are public, so a contamination caveat applies to every model in a BEIR results table. [[RTEB]] is the private-data answer to that problem.

## Why it rewards memorization

A model trained on a benchmark's queries and relevance labels can learn which documents are relevant for those exact queries without learning how to judge relevance in general, like a student who has seen the answer key. The leaderboard scores both the same way, so it cannot tell memorization from retrieval skill, and it ranks the model that remembered the answers as if it had earned them. RTEB's diagnosis puts it in one line: public benchmarks reward memorization. The gap only shows when the model meets data it has not seen.

## Detecting it: the open-vs-private gap

[[RTEB]] splits its datasets into an **open** half (fully public) and a **private** half held by the maintainers, who evaluate submissions on the submitters' behalf. A model that scores well on the open datasets and drops sharply on the private ones has been trained on the test. Where both scores are available, a large open-vs-private drop is the strongest available evidence of benchmark overfitting, more informative than absolute position on any board.

## Hiding the test set moves the problem

In 2026 RTEB's private column was temporarily removed from the leaderboard after concerns that model vendors with access to the private evaluation data held a structural advantage. Keeping the test set secret does not eliminate the incentive problem; it relocates it. Someone has to hold the secret, and if that party also competes, or has commercial relationships with competitors, the benchmark trades contamination for a conflict of interest. Held-out evaluation is a governance problem as much as a data problem.

## Stating it as a caveat

Careful benchmark write-ups name the risk on their own numbers. [[Hev meets Jev]] lists training-set contamination as possible for every model in its [[BEIR]] reranking table, and [[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]] flags BEIR's presence in embedding training data as a contamination risk for its compression results.

## Practical response

- Use public boards to build a shortlist, then decide on your own judgments. See [[Model Selection and Fine-Tuning Evaluation]].
- Where a benchmark reports held-out results ([[RTEB]]), weigh the open-vs-private gap above the headline score.
- Treat vendor-reported public-benchmark numbers with extra care: they are often produced under favourable and unstated conditions, on top of the contamination risk.

## Related, but different

- **Train/test leakage in your own evaluation**: the same failure inside a team's fine-tuning harness. An enormous fine-tuning gain most often means query-level leakage between train and test splits. See [[Embedding Fine-tuning]] and [[Model Selection and Fine-Tuning Evaluation]].
- **Leakage between experiment arms**: in online ranking experiments, re-training and feature leakage couple control and treatment. That is an experimentation problem; see [[Isolated Feedback Loops]].
- **Context contamination**: distractor passages degrading an LLM's answer at inference time, unrelated to training data. See [[Clean Context]].

## Related Concepts

- [[Search Evaluation]] · [[Embedding Fine-tuning]] · [[Isolated Feedback Loops]] · [[Clean Context]]

## Datasets

- [[RTEB]] · [[MTEB]] · [[BEIR]] · [[MS MARCO]] · [[BRIGHT]]

## Topics

- [[Retrieval Benchmarks and Leaderboards]] · [[Model Selection and Fine-Tuning Evaluation]]

## Related Articles

- [[Hev meets Jev]] · [[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]]
