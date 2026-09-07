---
type: article
title: "Uncovering the Bigger Picture: Comprehensive Event Understanding via Diverse News Retrieval"
source: "https://aclanthology.org/2025.emnlp-main.1722/"
pdf: "https://aclanthology.org/2025.emnlp-main.1722.pdf"
repo: "https://github.com/tangyixuan/NEWSCOPE"
author:
  - "[[Yixuan Tang]]"
  - "[[Yuanyuan Shi]]"
  - "[[Yiqun Sun]]"
  - "[[Anthony K.H. Tung]]"
published: 2025-11-04
created: 2026-09-07
venue: "EMNLP 2025 (main conference), pp. 33939–33957"
datasets:
  - "[[LocalNews]]"
  - "[[DSGlobal]]"
concepts:
  - "[[APD]]"
  - "[[Diversity Metrics]]"
  - "[[MMR]]"
  - "[[Reranking]]"
  - "[[Dense Embeddings]]"
  - "[[BM25]]"
  - "[[Precision and Recall]]"
topics:
  - "[[Search Result Diversity]]"
tags:
  - article
  - diversity
  - ranking
  - reranking
  - news
  - information-retrieval
---

# Uncovering the Bigger Picture: Comprehensive Event Understanding via Diverse News Retrieval

**Authors:** [[Yixuan Tang]], [[Yuanyuan Shi]], [[Yiqun Sun]], [[Anthony K.H. Tung]] · EMNLP 2025 main conference, Suzhou, pp. 33939–33957 · code and data at [tangyixuan/NEWSCOPE](https://github.com/tangyixuan/NEWSCOPE)

## Summary

NEWSCOPE — "NEWs Understanding via Sentence Clustering and cOmPrehensive rEtrieval" — is a two-stage retrieval framework for news events. Its argument against the existing diversification literature is one of *granularity*: [[MMR]] and its descendants operate on whole-document or whole-article embeddings, which the authors say "fail to capture fine-grained differences in perspectives, framing, and coverage." NEWSCOPE retrieves at the paragraph level but models diversity at the **sentence** level, treating sentences as the atomic units of meaning.

The task it formalizes is **event-centric diverse news retrieval**: given an event and a corpus, return *k* paragraphs that are each relevant and that *collectively* cover semantically distinct aspects of the event. It is deliberately stance-agnostic — unlike claim-centric stance discovery, it does not look for supporting versus opposing views, only for distinct factual aspects and framings.

## The Two Stages

### Stage I — relevance-based retrieval

The event headline and candidate paragraphs are encoded with `bilingual-embedding-large` and ranked by cosine similarity. This is a filter: only the top candidates (e.g. 100) reach Stage II.

### Stage II — diversity-aware reranking

Paragraphs are split into sentences, each sentence is embedded, and **OPTICS** (Ankerst et al., 1999) clusters them by density — chosen because it does not require the number of clusters in advance. Each cluster stands in for a distinct informational aspect of the event. Two selection strategies run on top:

**GreedySCS** — greedy cluster selection. With `U` the uncovered clusters, score each paragraph by how many new ones it brings:

```
Score(p) = |U ∩ Clusters(p)|
```

Pick the maximum, mark its clusters covered, repeat until *k* paragraphs are selected or a coverage threshold is met.

**GreedyPlus** — adds soft weighting so relevance is not thrown away. Each cluster gets a relevance weight, the mean similarity between the headline and the paragraphs containing that cluster's sentences, scored with `bge-reranker-large`:

```
ClusterScore(c) = (1/|c|) · Σ_{sᵢ ∈ c} Sim(h, p_sᵢ)
Score⁺(p)      = Σ_{c ∈ Clusters(p) ∩ U} ClusterScore(c)  +  λ · Sim(h, p)
                 └──────── diversity term ────────┘         └─ relevance ─┘
```

λ = 0.5 in all reported results. The cluster weight doubles as a soft noise filter, downweighting incidental or promotional clusters that survived Stage I.

Because Stage II only ever touches the top-ranked candidates, the reported cost is about **1.2 seconds per event**.

## The Three Diversity Metrics

The paper's second contribution, and the part that matters most outside news:

- **Average Pairwise Distance (D)** — mean pairwise cosine *distance* among the retrieved paragraph embeddings. See [[APD]]; this is the passive, document-level measure the vault already carries.
- **Positive Cluster Coverage (C)** — covered sentence clusters ÷ total clusters present in the relevant paragraphs. Fine-grained semantic recall: it asks how much of the available perspective space was actually surfaced, and by construction gives no credit for redundancy.
- **Information Density Ratio (I)** — covered clusters ÷ total sentences in the retrieved paragraphs. Rewards concision, penalizing padding and repetition inside the results.

C and I are the interesting pair. Both are *coverage-denominated* rather than distance-denominated, which sidesteps the standard complaint about APD — that a set can be spread out in embedding space without covering the aspects a reader needs.

## Results

Baselines: [[BM25]], dense retrieval alone, [[MMR]], and DkMIPS (diversity-aware maximum inner product search). On LocalNews at top-10:

| Method | F1 | D | I | C |
|---|---|---|---|---|
| BM25 | 46.7 | 26.5 | 36.9 | 51.2 |
| Dense retrieval | **48.9** | 23.0 | 36.5 | 52.8 |
| [[MMR]] | 48.1 | 29.0 | 38.8 | 55.8 |
| DkMIPS | 43.0 | **34.6** | 39.1 | 50.2 |
| NEWSCOPE (GreedySCS) | 48.3 | 26.3 | 44.6 | 62.0 |
| NEWSCOPE (GreedyPlus) | 46.8 | 30.2 | **54.4** | **74.5** |

The shape of the win is worth reading carefully, because it is not uniform. On **C** and **I** GreedyPlus is far ahead — cluster coverage 74.5 against dense retrieval's 52.8. On **D**, the distance-based metric, it does not dominate at all: DkMIPS scores higher here and at several other depths, while GreedyPlus lands roughly level with MMR. The relevance cost is about two F1 points against the dense retriever. The same pattern holds on DSGlobal.

That divergence is itself a finding: **a system can lead on aspect coverage while trailing on average pairwise distance**, and vice versa. Spreading results out in embedding space and covering the distinct things a reader needs are not the same objective.

An ablation confirms both halves of GreedyPlus are load-bearing. Dropping the diversity term recovers a little F1 (48.8) and collapses coverage (C 52.8). Dropping the relevance term pushes coverage to 80.5 and destroys relevance (F1 32.0) by pulling in loosely-related content.

## Why It Matters

Two things carry beyond news search.

The first is granularity. Diversification is almost always implemented over whole-document vectors, which is where the redundancy hides: two articles can be far apart as documents while repeating the same three facts. Clustering at the sentence level makes the unit of diversity the *claim* rather than the *document*, and it makes the result interpretable — each cluster is inspectable, so a diversity score can be explained rather than merely reported.

The second is the metric gap. Tracking [[APD]] alongside [[NDCG]] catches gross redundancy, but APD cannot distinguish a result set that is spread out from one that is comprehensive. Positive Cluster Coverage needs a notion of the aspects that *ought* to be covered — expensive, and here supplied by clustering the relevant paragraphs — but it measures the thing practitioners actually mean by diversity.

## Limitations

- Coverage and density are defined against the paper's own clustering step, so the metrics and the method share machinery: C is measured in the same cluster space that GreedySCS optimizes over. The authors present the clusters as good proxies for event aspects with a qualitative appendix, not an independent validation.
- Both benchmarks use an LLM-generated one-sentence summary as the query, which simulates rather than observes user intent.
- All reported comparisons are the authors' own; no independent replication is known.

## Related Concepts

- [[APD]] — the D metric, and the one the other two are designed to improve on
- [[Diversity Metrics]] — where Positive Cluster Coverage and Information Density Ratio belong
- [[MMR]] — the coarse-grained baseline the framework argues against
- [[Reranking]] — Stage II is a reranker
- [[Dense Embeddings]] — Stage I retrieval and the sentence encoding
- [[BM25]] — sparse baseline
- [[Precision and Recall]] — the relevance side of the evaluation

## Related Topics

- [[Search Result Diversity]] — the vault's treatment of the relevance/diversity trade-off

## Related Datasets

- [[LocalNews]] — the paper's new benchmark, from Google News "Full Coverage"
- [[DSGlobal]] — its global-news counterpart, adapted from DiverseSumm

## People

- [[Yixuan Tang]] — author
- [[Yuanyuan Shi]] — author
- [[Yiqun Sun]] — author
- [[Anthony K.H. Tung]] — author
