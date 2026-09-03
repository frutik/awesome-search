---
title: "LLMJudge"
aliases: ["LLMJudge challenge", "LLM4Eval LLMJudge"]
tags:
  - dataset
  - benchmark
  - search-evaluation
  - llm-judge
  - information-retrieval
type: dataset
source: "LLMJudge challenge, LLM4Eval workshop at SIGIR 2024 — arXiv:2408.08896"
domain: relevance-judgment agreement (web passages)
related_concepts:
  - "[[LLM as Judge]]"
  - "[[Judgment Lists]]"
  - "[[Search Evaluation]]"
  - "[[Pointwise Relevance Evaluation]]"
website: https://arxiv.org/abs/2408.08896
created: 2026-09-03
---

# LLMJudge

## Overview

**LLMJudge** is not a retrieval benchmark — it is a benchmark for *judges*. Organized as part of the **LLM4Eval workshop at SIGIR 2024**, it asks participants to generate relevance labels with an LLM and scores how closely those labels match human ones. Its stated motivation is that collecting relevance judgments at scale "is costly and resource-intensive," so experiments lean on third-party labelers "who may not always produce accurate annotations."

The open questions it was set up to probe: which LLMs match human labelers, which prompts work, how fine-tuned open-source models compare to closed-source ones like GPT-4, whether synthetic labels carry biases, and whether data leakage inflates apparent quality.

Organizers include Hossein A. Rahmani, Emine Yilmaz, Nick Craswell, Bhaskar Mitra, Paul Thomas, [[Charles L. A. Clarke]], Mohammad Aliannejadi, Clemencia Siro and Guglielmo Faggioli (arXiv:2408.08896, 2024).

## Data

Built on the **passage retrieval task dataset of the TREC 2023 Deep Learning track** — see [[TREC Deep Learning Track]].

| Split | Queries | Passages | Query-document pairs |
|---|---|---|---|
| Development | 25 | 7,224 | 7,263 |
| Test | 25 | 4,414 | 4,423 |

Few queries, deeply judged — the collection is sized for measuring judge agreement, not for training rankers.

## Grade Scale

Four points:

- **3** — Perfectly relevant
- **2** — Highly relevant
- **1** — Related
- **0** — Irrelevant

## Task and Evaluation

Participants submit an LLM-generated score of 0–3 for each query-document pair. Submissions are scored on two axes:

1. **Cohen's kappa** — inter-rater agreement with human labels at the query-document level.
2. **Kendall's tau** — agreement on the *system ordering* obtained by re-scoring the TREC DL 2023 submissions with the participant's labels.

The reported pattern across submissions: consistent system rankings, but considerably more variation in inter-rater reliability. That gap — leaderboards agree while individual labels do not — is the same phenomenon [[Benchmarking LLM-based Relevance Judgment Methods]] traces to the choice of judgment paradigm, and it is why an [[LLM as Judge|LLM judge]] validated only on system ranking should not be assumed accurate per document.

## Related Datasets

- [[TREC Deep Learning Track]] — the source collection
- [[MS MARCO]] — underlying corpus, one level further back

## Related Concepts

- [[LLM as Judge]] — the thing being benchmarked
- [[Judgment Lists]] — what participants generate
- [[Search Evaluation]]
- [[Pointwise Relevance Evaluation]] — the 0–3 pointwise format the challenge fixes

## Related Articles

- [[Criteria-Based LLM Relevance Judgments]] — its Multi-Criteria framework placed first on Spearman correlation in this challenge
- [[Benchmarking LLM-based Relevance Judgment Methods]] — same two-axis evaluation logic

## People

- [[Charles L. A. Clarke]] — co-organizer
