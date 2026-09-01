---
type: company
industry: search infrastructure
products:
  - Vespa (open-source search and recommendation engine)
category: technology-provider
search_domain: open-source big data serving engine with native ML support
tags: [company]
created: 2026-05-16
---

# Vespa

## What They Build

Vespa is an open-source **big data serving engine** originally developed by Yahoo and now maintained as an independent open-source project (vespa.ai). Unlike Elasticsearch (document-centric) Vespa was built with ML-native ranking in mind from the start — it supports tensor computations, native embedding models, and multi-phase ranking as first-class features.

Vespa is particularly strong for use cases that mix retrieval, ranking, and ML inference in a single platform without an external reranking tier.

## Search Contributions

### Models and Embeddings
- **ColBERT embedder** — native integration of [[ColBERT]] late-interaction model into Vespa with asymmetric binarization (32x compression with minimal quality loss). Led by [[Jo Kristian Bergum]]. See [[Late Interaction in Vespa]] for the indexing/scoring/scaling mechanics
- Native HNSW approximate nearest neighbor for dense vector retrieval
- BM25 + dense vector [[Hybrid Search]] as a built-in feature

### Methodology
- **Zero-shot ranking without labels** — a three-post programme establishing that a tuned [[BM25]] baseline fused with a small distilled [[ColBERT]] reranker beats either component on [[BEIR]] (0.481 vs 0.453 avg nDCG@10), then that [[Synthetic Query Generation]] with a 3B open LLM closes the remaining gap on a specific domain. See [[Vespa - Ranking Without Labels on CORD-19]]
- **LLM-as-Judge for retrieval evaluation** — demonstrated how to use LLMs to generate relevance labels and compute NDCG; showed strong correlation with human judgments (Spearman ρ ≈ 0.85–0.90). Early and influential demonstration of the [[LLM as Judge]] pattern for retrieval

### Architecture
- Multi-phase ranking: cheap first-stage rankers → expensive ML models only on candidates. Native [[Learning to Rank|LTR]] via GBDT ([[XGBoost]]/[[LightGBM]]) and [[ONNX]] models in ranking expressions — see [[Vespa Learning to Rank]]
- Tensor computations at serving time without external ML serving infrastructure
- Native support for structured filtering alongside dense vector search
- Distributed **exact** nearest-neighbour search — an exhaustive scan can be spread across nodes
  in parallel to hold latency down, and restricted to a subset by query-engine filtering, so
  [[Brute-Force Vector Search|brute force]] stays viable further up the corpus-size curve than
  it would in a single process
- **[[Asymmetric Re-ranking]]** — scoring a full-precision query embedding against binary-quantized document vectors as a cheap second-phase recall-recovery step, with an algebraic rewrite that constant-folds the query-only term; documented by [[Dainius Jocas]]

## Position in the Ecosystem

Vespa is a direct alternative to Elasticsearch + separate ML serving tier. The value proposition: run BM25, dense vector ANN, and ML re-ranking in a single engine. The tradeoff: steeper learning curve, smaller community than Elasticsearch.

## People

- [[Jo Kristian Bergum]] — former Chief Scientist, Vespa AI (now co-founder of [[Hornet]]); author of the ColBERT embedder and LLM-as-judge work
- [[Marianne Haugvaldstad]] — Developer Intern; HNSW exploration and tooling
- [[Brage Vik]] — Developer Intern; HNSW exploration and tooling

## Articles

- [[Announcing the Vespa ColBERT Embedder]]
- [[Improving Retrieval with LLM as a Judge]]
- [[Exploring Hierarchical Navigable Small World]]
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]], written while at Vespa; distributed exhaustive search as the alternative to ANN, and how to price the choice
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] · [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — [[Jo Kristian Bergum]]; the zero-shot hybrid ranking series and its BEIR results
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]]; synthetic training data from three labeled examples

- [[From Elasticsearch to Vespa - Rebuilding the Kleinanzeigen Homepage Feed Part 1]] — [[Andre Charton]], [[Kleinanzeigen]]
- [[How I learned Vespa by thinking in Solr]] — [[Sujit Pal]] ([[Elsevier]]); onboarding to Vespa via Solr analogies
- [[How to Securely Hook Up Quepid to Vespa]] — [[Charlie Hull]]; interactive offline relevance testing for Vespa via [[Quepid]] (Vespa lacks built-in offline eval tooling)
- [[Updating a Vector Database Is No Simple Thing]] — [[Doug Turnbull]]; Vespa keeps a single graph updated concurrently in place, contrasted with tombstoning/segmentation elsewhere
- [[Optimize Asymmetric Re-ranking with Algebra]] — [[Dainius Jocas]]; algebraic rewrite of asymmetric BQ re-ranking, 28% latency cut at 1M documents

## Concepts

[[ColBERT]] · [[Late Interaction]] · [[Late Interaction in Vespa]] · [[Learning to Rank]] · [[Vespa Learning to Rank]] · [[LLM as Judge]] · [[Hybrid Search]] · [[Dense Vector Retrieval]] · [[Reranking]] · [[Asymmetric Re-ranking]] · [[Binary Quantization]] · [[Brute-Force Vector Search]] · [[Zero-Shot Retrieval]] · [[Score Normalization]] · [[Synthetic Query Generation]] · [[Consistency Filtering]] · [[Cross-Encoder]]

## Case Studies

- [[Vespa - Ranking Without Labels on CORD-19]] — ranking a 171K-document corpus with three labeled queries; live at cord19.vespa.ai

## Datasets

- [[BEIR]] · [[TREC-COVID]] — the benchmarks the zero-shot ranking work is measured on
