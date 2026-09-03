---
title: "MS MARCO"
aliases: ["MSMarco", "MSMARCO", "MS MARCO passage", "MS MARCO passage ranking", "Microsoft MAchine Reading COmprehension"]
tags:
  - dataset
  - benchmark
  - information-retrieval
  - passage-ranking
  - search-evaluation
type: dataset
source: Microsoft
domain: web search / open-domain passage retrieval
website: https://microsoft.github.io/msmarco/
---

# MS MARCO

## Overview

MS MARCO (Microsoft MAchine Reading COmprehension) is a large-scale information retrieval
benchmark built from real anonymized Bing search queries. Its **passage ranking** subset has
become the default training and evaluation corpus for neural retrieval research — most
published [[Dense Embeddings|dense retrieval]] and [[Learned Sparse Retrieval|sparse]] models
report MS MARCO numbers, and many are trained on it directly.

Its scale is what makes it the standard stress test: the passage corpus contains roughly
8.8 million passages, large enough that memory footprint and index efficiency become real
engineering constraints rather than afterthoughts.

## Why It Recurs in Retrieval Work

- **Real queries.** Drawn from Bing traffic, not synthesized — query distribution reflects
  actual user behavior, including the short, underspecified queries that dominate web search
- **Training scale.** Hundreds of thousands of labeled query–passage pairs, enough to train
  neural rankers from scratch
- **Comparability.** So widely used that a MS MARCO number is instantly comparable across papers
- **Benchmark for efficiency work.** Corpus size makes it the natural testbed for
  [[Dimensionality Reduction]], [[Vector Quantization]], and [[Approximate Nearest Neighbor Search]]
  experiments — compression wins are measurable at this scale

## Known Limitations

- **Sparse labels.** Typically ~1 relevant passage marked per query; many genuinely relevant
  passages are unlabeled, so recall-oriented metrics understate true system quality
- **Binary relevance.** The standard qrels are binary rather than graded, limiting [[NDCG]]'s
  usefulness compared to graded datasets like [[Amazon ESCI Dataset]]
- **Web-search domain.** Models tuned on MS MARCO don't automatically transfer to
  [[E-commerce Search]], enterprise, or other verticals, motivating out-of-domain evaluation
  on separate benchmark suites

## Comparison with Other Datasets

| Dataset | Domain | Scale | Label type |
|---|---|---|---|
| MS MARCO | Web search (Bing) | ~8.8M passages | Binary, sparse |
| [[Amazon ESCI Dataset]] | General e-commerce | Very large | 4-class (ESCI) |
| [[WANDS Dataset]] | Home goods | ~42K pairs | 3-class |
| [[Home Depot Product Search Relevance]] | Home improvement | ~74K pairs | Continuous 1–3 |
| [[Natural Questions]] | Wikipedia QA | ~2.68M passages | Binary, sparse (~1.2/query) |
| [[TREC-COVID]] | Biomedical | ~171K docs | Graded, deep (~493.5/query) |

## In This Vault

MS MARCO appears as the evaluation corpus across a broad slice of the retrieval notes —
embedding compression, reranking, sparse retrieval, and metric definitions. Notably:

- [[Principal Component Analysis - an embedding shrink-ray]] — 9M records × 384 dims × 4 bytes
  ≈ 14GB, the memory problem that motivates [[PCA]]; recall measured at 50/100/200 dimensions
- [[Flavors of NDCG]] — MS MARCO's NDCG conventions as one of the per-library variants
- [[Three mistakes when introducing embeddings and vector search]] — MS MARCO fine-tuning beats
  [[BM25]] *"by a very large margin"* on MS MARCO itself, and frequently loses to it elsewhere;
  the canonical warning against adopting a model on its MS MARCO number alone
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — the MS MARCO / [[Natural Questions]] corpus
  comparison (5.9 vs 9.2-word queries, 56.6 vs 76.0-word documents, 8.84M vs 2.68M documents) and
  the [[Dense Passage Retriever]] result: NQ-trained dense retrieval losing to [[BM25]] here
  zero-shot. BM25 is reported to trail neural approaches by 7–18 points on MS MARCO itself

## Related Concepts

- [[Precision and Recall]] — the metric most often reported against MS MARCO
- [[MRR]] — MRR@10 is the canonical MS MARCO passage ranking metric
- [[Judgment Lists]] — MS MARCO qrels are a public judgment list
- [[Dense Vector Retrieval]] — the paradigm MS MARCO largely trained
- [[Cross-Encoder]] · [[Bi-Encoder]] — both architectures benchmark here
- [[BEIR]] — the zero-shot suite MS MARCO-trained models are judged against; MS MARCO is also one of its 18 subsets
- [[Zero-Shot Retrieval]] — why a strong MS MARCO score predicts less than it appears to
- [[Dense Passage Retriever]] — the model whose MS MARCO transfer failure is the standard illustration
- [[Search Evaluation]] — broader evaluation context

## Related Benchmarks

- [[TREC Deep Learning Track]] — the NIST evaluation campaign built directly on these corpora and training labels, supplying the deeply-judged graded test queries MS MARCO's own shallow judgments lack
- [[BEIR]] · [[MTEB]] — where MS MARCO-trained models get judged
- [[LoTTE]] — built explicitly against MS MARCO's head-heavy query distribution
- [[BRIGHT]] · [[MIRACL]] · [[RTEB]] — the stress-test, multilingual, and anti-contamination benchmarks
- [[Retrieval Benchmarks and Leaderboards]] — the landscape, and why MS MARCO's ubiquity is now a contamination risk

## Source

- Official site: https://microsoft.github.io/msmarco/
- Passage corpus via ir-datasets: https://ir-datasets.com/msmarco-passage.html
