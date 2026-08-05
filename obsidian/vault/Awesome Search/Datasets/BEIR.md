---
title: "BEIR"
aliases: ["BEIR benchmark", "Benchmarking-IR", "BEIR suite"]
tags:
  - dataset
  - benchmark
  - information-retrieval
  - zero-shot
  - search-evaluation
type: dataset
source: UKP Lab / TU Darmstadt (Thakur et al., 2021)
domain: heterogeneous — 9 retrieval tasks, 18 zero-shot datasets (+ MS MARCO as training corpus)
website: https://github.com/beir-cellar/beir
created: 2026-07-29
---

# BEIR

## Overview

**BEIR** (Benchmarking-IR) is a heterogeneous **zero-shot** retrieval benchmark spanning 9 task types — fact checking, question answering, bio-medical IR, argument retrieval, duplicate question detection, citation prediction, entity retrieval, news retrieval, and tweet retrieval. Models are trained elsewhere (usually on [[MS MARCO]]) and evaluated on the suite without further tuning.

**On "18 datasets":** that is the figure the paper and repository headline, but the repository's own table enumerates 19 corpus names. [[MS MARCO]] is the discrepancy — it is distributed with the suite yet normally serves as the *training* corpus rather than a zero-shot target, so it is usually excluded from the count and from reported averages. Worth knowing before reconciling two papers' dataset tallies.

Where MS MARCO answers *"how good is this model on web-search passages"*, BEIR answers *"how much of that survives contact with a different domain"* — which is why it became the default proof of generality for a retrieval model, and why it appears in nearly every model announcement in this vault.

**nDCG@10** is the canonical reported metric (see [[NDCG Variants]] — BEIR's convention is one of the per-library variants that make cross-paper NDCG comparison hazardous).

## Constituent Datasets

The full list: [[MS MARCO]], TREC-COVID, NFCorpus, BioASQ, Natural Questions, HotpotQA, FiQA-2018, Signal-1M, TREC-NEWS, Robust04, ArguAna, Touché-2020, CQADupStack, Quora, DBPedia-entity, SCIDOCS, FEVER, Climate-FEVER, SciFact.

Four — **BioASQ, Signal-1M, TREC-NEWS, Robust04** — are licence-restricted and not publicly downloadable; the repo ships reproduction instructions instead. Published "BEIR average" figures therefore often cover 12–15 datasets rather than the full suite, which is the first thing to check before comparing two papers' averages.

Scale varies by three orders of magnitude, from NFCorpus (~3.6K documents) to MS MARCO (~8.8M), which is what makes the suite useful for efficiency claims as well as quality ones.

## Why It Recurs

- **Zero-shot by construction.** The headline finding of the original paper was that BM25 is a formidable out-of-domain baseline, and that dense retrievers trained on MS MARCO frequently lose to it on unfamiliar domains. Much subsequent work — [[Learned Sparse Retrieval]], [[Late Interaction]], hybrid schemes — is a response to that result.
- **Domain diversity as a stress test.** A model can only score well across BEIR by generalising, not by fitting one query distribution.
- **Comparability.** Ubiquitous enough that a BEIR number is instantly legible, subject to the subset caveat above.

## Known Limitations

- **Shallow judgments.** Most subsets carry sparse, largely binary qrels; unjudged-but-relevant documents are common, so recall-oriented conclusions understate real quality — the same problem as [[MS MARCO]], inherited across the suite.
- **Small query sets.** Several subsets have only a few hundred test queries, so per-dataset differences of a point or two are not obviously meaningful.
- **Averaging hides variance.** A model can win on average while losing badly on specific domains — the per-dataset table is where the information is.
- **Not a substitute for your data.** Strong BEIR generalisation says nothing about a product catalog; see [[E-commerce Search]] and the domain-transfer failures in [[Fine-Tuning Sparse Embeddings for E-Commerce Search]].

## Comparison with Other Datasets

| Dataset | Domain | Scale | Purpose |
|---|---|---|---|
| BEIR | 9 tasks, 18 zero-shot corpora | 3.6K–8.8M docs | Zero-shot generalisation |
| [[MS MARCO]] | Web search (Bing) | ~8.8M passages | In-domain training + eval |
| [[TREC-COVID]] | Biomedical (COVID-19 papers) | ~171K docs, 50 queries | Deeply judged BEIR subset |
| [[Natural Questions]] | Wikipedia QA | ~2.68M docs, 4,352 queries | Shallowly judged BEIR subset |
| [[Amazon ESCI Dataset]] | General e-commerce | Very large | Graded product relevance |
| [[WANDS Dataset]] | Home goods | ~42K pairs | E-commerce relevance judgments |

## In This Vault

BEIR is the shared yardstick across the retrieval-model notes:

- [[Elastic Learned Sparse Encoder (ELSER) Retrieval Performance]] — **+17% average NDCG@10 over BM25**; 10 wins, 1 draw, 1 loss across 12 BEIR datasets
- [[ColBERT-Zero - To Pre-train Or Not To Pre-train ColBERT Models]] — SOTA under 150M params, **55.43 vs 54.67 nDCG@10**
- [[miniCOIL]] — wins 4 of the 5 BEIR datasets it was *not* trained on
- [[Relevance Feedback in Qdrant]] — five subsets (NFCorpus, SCIDOCS, FiQA-2018, Quora, MS MARCO), evaluated with a custom `abovethreshold@10` metric rather than nDCG
- [[Superintelligent Retrieval Agent SIRA]] — LLM-enriched BM25 beating agentic RAG on Recall@10 and NDCG@10
- [[psql_bm25s]] — the 15-dataset suite used for **throughput** rather than quality: median ~3.97× QPS
- [[Announcing the Vespa ColBERT Embedder]] — compressed vs uncompressed [[ColBERT]] on BEIR
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]] uses BEIR's headline finding as the argument against trusting single-vector models out-of-domain
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — [[Jo Kristian Bergum]]; what BEIR contains and why its per-dataset judgment depth varies by three orders of magnitude ([[TREC-COVID]] ~493.5 judgments/query vs [[Natural Questions]] ~1.2)
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — a **tuned BM25 baseline beating the BM25 numbers published with BEIR** (0.453 vs 0.440 avg), and hybrid BM25 + distilled [[ColBERT]] at **0.481**, winning 12 of 13 datasets
- [[PROMPTAGATOR]] — the few-shot comparison point on the BEIR subset it reports

## Related Concepts

- [[NDCG]] · [[NDCG Variants]] — the reported metric and its incompatible conventions
- [[Search Evaluation]] · [[Judgment Lists]] — what BEIR's qrels are and aren't
- [[Dense Vector Retrieval]] · [[Learned Sparse Retrieval]] · [[BM25]] — the three-way comparison BEIR usually adjudicates
- [[Precision and Recall]] — the recall-oriented caveats above
- [[MS MARCO]] — what BEIR models are typically trained on before zero-shot evaluation
- [[Zero-Shot Retrieval]] — the concept BEIR was built to measure
- [[Hybrid Search]] · [[Score Normalization]] — the fusion approach that lifted the BEIR average most in this vault
- [[Synthetic Query Generation]] — how the remaining gap gets closed on a single BEIR subset

## Related Benchmarks

- [[MTEB]] — absorbed BEIR as its retrieval component; BEIR scores are now reported inside MTEB
- [[RTEB]] — the private-data answer to the contamination BEIR increasingly suffers from
- [[BRIGHT]] — reasoning-intensive retrieval, where BEIR-strong models collapse
- [[MIRACL]] — the multilingual counterpart BEIR lacks
- [[LoTTE]] — long-tail topic stratification rather than heterogeneity
- [[Retrieval Benchmarks and Leaderboards]] — how these fit together, and how to use them without being misled

## Source

- Repository and leaderboard: https://github.com/beir-cellar/beir
- Paper: *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models* — Thakur, Reimers, Rücklé, Srivastava, Gurevych (NeurIPS 2021 Datasets & Benchmarks), arXiv:2104.08663
