---
title: "TREC Deep Learning Track"
aliases: ["TREC DL", "TREC Deep Learning", "Deep Learning Track", "DL-19", "DL-20", "DL-21"]
tags:
  - dataset
  - benchmark
  - information-retrieval
  - search-evaluation
  - ranking
type: dataset
source: TREC / NIST, built on the [[MS MARCO]] corpora
domain: open-domain web passage and document ranking
related_concepts:
  - "[[Search Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[NDCG]]"
  - "[[LLM as Judge]]"
  - "[[Reranking]]"
website: https://microsoft.github.io/msmarco/TREC-Deep-Learning
created: 2026-09-03
---

# TREC Deep Learning Track

## Overview

The **TREC Deep Learning Track** is the evaluation campaign that asked what ranking models can do when training labels are abundant rather than scarce. It ran from **2019 through 2023**, with the 2023 edition billed as the fifth anniversary and the final one, and it is built on [[MS MARCO]] — the track exists because MS MARCO supplies "a large human-generated set of training labels," on the order of hundreds of thousands of labelled queries, which earlier TREC collections never had.

Within this vault it is the collection most retrieval-evaluation work is measured on, and the one both [[Benchmarking LLM-based Relevance Judgment Methods]] and [[Criteria-Based LLM Relevance Judgments]] use to test whether an [[LLM as Judge|LLM judge]] can stand in for NIST assessors.

## Tasks

Two tasks, each with a full-ranking and a reranking subtask:

- **Passage ranking** — rank passages from the full collection, or rerank the top 100. The primary focus by 2023.
- **Document ranking** — rank documents "based on their likelihood of containing a passage relevant to the question."

Runs submit up to 100 results per query per task.

## Scale

The 2019 edition used a corpus of **3.2 million documents** and **8.8 million passages**, with 367,000 training queries for the document task and 503,000 for the passage task. The later (v2) corpora are considerably larger: **138,364,198 passages** (20.3 GB) and **11,959,635 documents** (32.3 GB).

Test queries are few and deeply judged rather than many and shallowly judged — **43 reusable test queries per task in 2019**, against which 15 groups submitted 75 runs. The 2023 edition released a 700-query test set.

## Judgments

NIST assessors apply **multi-graded judgments** to passages using **depth pooling**. Document-ranking labels are not assessed independently — they are inferred from the passage judgments.

This is the property that makes the track useful for studying automatic judges: the human labels are graded, pooled, and produced under a documented process, so a proposed [[LLM as Judge|LLM judge]] can be scored both on whether it reproduces individual assessor grades and on whether a leaderboard built from its labels orders the submitted runs the way the human one does. Those two questions have different answers — see [[Benchmarking LLM-based Relevance Judgment Methods]].

## Related Datasets

- [[MS MARCO]] — the corpora and training labels the track is built on
- [[LLMJudge]] — a relevance-judgment challenge collection derived from the track's TREC 2023 passage task
- [[TREC-COVID]] — a different TREC collection, biomedical rather than open-domain web
- [[BEIR]] — zero-shot suite that includes MS MARCO and other TREC collections

## Related Concepts

- [[Search Evaluation]] — the practice this track institutionalizes
- [[Judgment Lists]] — what the NIST assessors produce
- [[NDCG]] — the metric the track's system rankings are built from
- [[LLM as Judge]] — evaluated against these judgments
- [[Reranking]] — the track's reranking subtask

## Related Articles

- [[Benchmarking LLM-based Relevance Judgment Methods]] — uses DL-19/20/21 to separate label agreement from system-ranking agreement
- [[Criteria-Based LLM Relevance Judgments]] — uses DL-19/20 plus LLMJudge
