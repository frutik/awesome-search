---
title: "CLERC"
aliases: ["Case Law Evaluation and Retrieval Corpus", "CLERC dataset"]
tags:
  - dataset
  - benchmark
  - legal-search
  - information-retrieval
  - rag
type: dataset
source: "Johns Hopkins CLSP — Hou et al., NAACL 2025 Findings (arXiv:2406.17186)"
domain: "US federal case law — legal case retrieval and retrieval-augmented analysis generation"
website: https://huggingface.co/datasets/jhu-clsp/CLERC
related_concepts: ["Reranking", "BM25", "RAG", "Zero-Shot Retrieval", "Precision and Recall", "Hallucination Detection"]
created: 2026-09-19
---

# CLERC

## Overview

**CLERC** (Case Law Evaluation and Retrieval Corpus) is a legal information-retrieval benchmark
built from US federal case law, designed around two linked tasks: finding the citations that
support a given piece of legal analysis, and compiling those cited texts into a coherent
analysis. It was constructed with legal professionals from the Caselaw Access Project corpus of
Harvard Law School, which holds more than 1.8 million federal case documents.

The dataset ships as `CLERC/doc`, `CLERC/passage`, and `CLERC/queries` for retrieval, plus
`CLERC/generation` for the [[RAG]] half.

## The Retrieval Task

A query is an excerpt from a court opinion with a citation **removed**; the gold document is
the passage that removed citation pointed to. This construction is what makes CLERC hard and
interesting — the match is not topical similarity but whether a candidate *establishes the
specific legal proposition* the excerpt invokes at its citation point. A passage on the same
doctrine that does not supply that proposition is a negative, and a well-chosen one.

That distinction defeats lexical and embedding similarity alike, which is why it is a natural
[[Reranking]] benchmark: the signal that separates gold from a near-miss is a judgment, not a
distance.

## Difficulty

CLERC is hard by the standards of retrieval benchmarks. The paper reports zero-shot IR models
reaching only **48.3% recall@1000**, and notes that GPT-4o produced the highest ROUGE F-scores
on the generation task while hallucinating the most — a pairing that makes the dataset useful
for [[Hallucination Detection]] work as well as ranking.

For contrast, most [[BEIR]] subsets are shallow-judgment topical-relevance tasks where a tuned
BM25 is already a strong baseline. CLERC is closer to a reasoning-retrieval benchmark like
[[BRIGHT]], where relevance requires an inference step rather than a similarity measurement.

## In This Vault

- [[TypeSafe Cookbook - Re-ranking]] — a 3,565-passage slice with 40 queries, where a [[BM25]]
  top-30 shortlist contained the correct passage for **100%** of queries but ranked it first
  only 5% of the time; [[Jev]] reranking raised that to 18% top-1 and 62% top-10. The clearest
  illustration in this vault of retrieval and ranking failing independently — perfect candidate
  recall with ranking as the sole bottleneck.

## Related Concepts

- [[Reranking]] — the stage CLERC most directly stresses
- [[Precision and Recall]] — recall@K and top-K accuracy coming apart
- [[Zero-Shot Retrieval]] — how CLERC is usually evaluated
- [[Semantic Relevance]] — relevance here is propositional, not topical
- [[RAG]] · [[Hallucination Detection]] — the generation half of the benchmark
- [[Judgment Lists]] — gold labels derived from real citations rather than annotator ratings

## Related Benchmarks

- [[BRIGHT]] — reasoning-intensive retrieval, the closest sibling in difficulty
- [[BEIR]] — the general heterogeneous suite, topical rather than propositional
- [[TREC-COVID]] — another specialist-domain corpus with deep judgments
- [[Retrieval Benchmarks and Leaderboards]] — how these fit together

## Source

- Dataset: https://huggingface.co/datasets/jhu-clsp/CLERC
- Paper: *CLERC: A Dataset for U.S. Legal Case Retrieval and Retrieval-Augmented Analysis
  Generation* — Johns Hopkins CLSP, Findings of NAACL 2025, arXiv:2406.17186
- Built from the Caselaw Access Project (Harvard Law School)
