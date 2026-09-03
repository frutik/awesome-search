---
title: "RTEB"
aliases: ["RTEB benchmark", "Retrieval Embedding Benchmark"]
tags:
  - dataset
  - benchmark
  - retrieval
  - leaderboard
  - search-evaluation
type: dataset
source: MTEB maintainers / Hugging Face (announced 1 October 2025, beta)
domain: retrieval — hybrid of open and private real-world datasets
website: https://huggingface.co/blog/rteb
created: 2026-08-05
---

# RTEB

## Overview

**RTEB** (Retrieval Embedding Benchmark) is a retrieval-focused benchmark announced in beta on **1 October 2025** by the [[MTEB]] maintainers, built to attack one specific problem: the **generalization gap** between leaderboard scores and real-world retrieval accuracy.

The diagnosis behind it is that public benchmarks reward memorization. When corpus, queries, and labels are all public, they leak into training data — and a model that has effectively seen the test posts a score that does not survive contact with new data.

## The Hybrid Design

RTEB's answer is to split its datasets in two:

- **Open datasets** — corpus, queries, and relevance labels fully public, for reproducibility and transparency
- **Private datasets** — held confidentially by the maintainers and evaluated on submitters' behalf, with only sample triplets published for transparency

The signal comes from the **gap between the two halves**. A model that scores well on the open datasets and drops sharply on the private ones has been trained on the test. That divergence is more informative than either number alone, and it is something no fully-public benchmark can produce.

## The Governance Problem

In 2026 the private column was **temporarily removed** from the leaderboard, following concerns that model vendors with access to the private evaluation data held a structural advantage — and observations that some models' gains were concentrated specifically in the private datasets rather than the public ones.

This is worth remembering as a general lesson rather than a piece of gossip: **"keep the test set secret" does not eliminate the incentive problem, it relocates it.** Someone has to hold the secret, and if that party also competes — or has commercial relationships with competitors — the benchmark inherits a new conflict of interest in place of the old contamination one. Held-out evaluation is a governance problem, not just a data problem.

## How to Use It

Where a private-set score is available, treat a large open-vs-private drop as the strongest available evidence of benchmark overfitting — more informative than absolute position on any board. It still does not substitute for evaluating on your own data; see [[Model Selection and Fine-Tuning Evaluation]].

## Related

- [[The Generalization Cliff]] — the wider argument this diagnostic feeds
- [[MTEB]] — the parent benchmark and the overfitting problem RTEB responds to
- [[Retrieval Benchmarks and Leaderboards]] — the wider landscape
- [[BEIR]] — the older zero-shot generalization test
- [[BRIGHT]] — a different attack on the same complacency
- [[Embedding Models Compared]] · [[Search Evaluation]]
