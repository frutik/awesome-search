---
type: topic
title: Vector Search Tradeoffs
aliases:
  - vector search trade-offs
  - ANN tradeoffs
  - choosing a vector index
  - do you need a vector database
tags:
  - topic
  - vector-search
  - ann
  - performance
  - architecture
related_concepts:
  - "[[Brute-Force Vector Search]]"
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[HNSW]]"
  - "[[IVF]]"
  - "[[LSH]]"
  - "[[Vector Filtering]]"
  - "[[Vector Quantization]]"
  - "[[Vector Search Evaluation]]"
  - "[[Late Interaction]]"
  - "[[MUVERA]]"
related_topics:
  - "[[Dimensionality Reduction vs Quantization]]"
  - "[[Search Platforms]]"
  - "[[Search Quality Assurance]]"
articles:
  - "[[Just brute force your embeddings]]"
  - "[[Three mistakes when introducing embeddings and vector search]]"
  - "[[Choosing a Vector Database for ANN Search at Reddit]]"
  - "[[Choosing Indexes for Similarity Search (Faiss in Python)]]"
created: 2026-07-30
---

# Vector Search Tradeoffs

There is no best vector index. Every choice is a position on a handful of axes, and the axes
interact — compressing vectors changes which index is affordable, adding a metadata filter changes
which index still returns correct results, and needing live updates disqualifies some options
outright. This note is the map; each axis delegates to the note that owns it.

The single most useful framing, from [[Jo Kristian Bergum]] in
[[Three mistakes when introducing embeddings and vector search]]: the decision is **not** which ANN
algorithm to use. It is whether to introduce approximation at all, and that question is answered by
three numbers you should be able to state before choosing anything.

| Axis | The question to answer first |
|---|---|
| **Latency SLA** | 0.001ms, 1ms, 10ms, 100ms, a second — maybe 3 seconds is fine? |
| **Throughput** | 1 QPS, 1M QPS, billions? What is the anticipated peak, not the average? |
| **Tolerable accuracy loss** | Approximation costs recall. How much can *this* use case absorb? |

All three collapse into deployment cost: how many servers — **or whether you need servers at all**.

## Axis 0 — Do You Need an Index?

The cheapest position on every other axis is not being on it. [[Brute-Force Vector Search]] scans
every vector, returns the true nearest neighbours by construction, has no parameters, no build step,
no recall curve, and no operational surface.

Two independent measurements three years apart — [[Jo Kristian Bergum]] in 2023 and
[[Doug Turnbull]] in 2026, on different hardware and dimensionality — agree on the conclusion even
though their numbers aren't comparable: **a million vectors is comfortably scannable**, in the tens
of milliseconds single-threaded. The measurements themselves, and why they can't be turned into a
speedup figure, live in [[Brute-Force Vector Search]].

Turnbull's profile for skipping the vector database entirely: around 1m documents, low query
traffic, and embeddings written up front.

Where this breaks is cost rather than correctness. The scan parallelises until memory bandwidth
saturates and can be distributed across nodes (as [[Vespa]] does), but at 10B vectors with no way to
restrict the search to a subset, server rental becomes the binding constraint — and high query
throughput makes it worse.

## Axis 1 — Recall vs Latency vs Memory

Once you do need an index, every family sits somewhere on a three-way surface. Exact search is 100%
recall and slowest; each approximation prunes the search space in exchange for recall.

| Family | Mechanism | Recall | Memory | Update story |
|---|---|---|---|---|
| [[Brute-Force Vector Search\|Flat]] | Exhaustive scan | 100% by construction | Raw vectors only | Trivial — append |
| [[LSH]] | Hash similar vectors into buckets | Weakest; best at low dimensionality | Tunable via `nbits` | — |
| [[HNSW]] | Multi-layer proximity graph | 95–99%+ with reasonable `ef_search` | Highest — edge storage on top of vectors | Incremental inserts, no rebuild |
| [[IVF]] | Cluster into cells, probe nearest | Lower than HNSW at equivalent settings | Lower than HNSW | Centroids fixed after training; partial rebuild for large changes |

The knobs that actually matter at runtime: `ef_search` for [[HNSW]] (beam width — the main recall/
latency dial), `nprobe` for [[IVF]] (clusters probed per query). Build-time choices — `M`,
`ef_construct`, `nlist` — are harder to change later.

One calibration point on how large the spread is: on [[SIFT1M]], [[LSH]] at `nbits = d*4` ran ~10×
faster than exact Flat search with good recall — while [[ann-benchmarks]] shows **some algorithms
struggling to get past 50% recall at any speed.** "We use ANN" describes a range, not a quality.

## Axis 2 — Bytes per Vector

```
bytes per vector  =  dimensions  ×  bits per dimension
```

Two independent multipliers, not competing choices. Cutting bytes helps everywhere, but not
identically: a full scan is sequential and bandwidth-bound, so compression buys close to
proportional speedup there, while a graph index pays random access and cache misses, where fewer
bytes per vector mainly improves cache residency. Either way this is usually the axis with the best
return per unit of effort, because it costs no recall structure — only precision per coordinate.

This axis is owned by **[[Dimensionality Reduction vs Quantization]]**, which covers the stacked
pipeline ([[PCA]] → random rotation → [[Scalar Quantization]]), why the rotation stage is not
optional, and where the fit cost is paid for each technique. The short version: **SQ8 for a
near-lossless 4×** as the default when you can't change the model, [[Binary Quantization]] / [[BBQ]]
for 32× if you can absorb rescoring, [[TurboQuant]] / [[RaBitQ]] to recover 9–24pp of recall over
plain BQ at the same compression, and [[Matryoshka Embeddings]] when the model supports it because
truncation is free at query time.

The trap on this axis is assuming a compression budget rather than measuring it. From
[[Principal Component Analysis - an embedding shrink-ray]], MiniLM on MS MARCO: 384→200 dims holds
0.879 recall, 384→100 drops to 0.5714, 384→50 collapses to 0.2029. Degradation is steeply
non-linear and model-specific.

## Axis 3 — Filtering

Metadata predicates are where ANN's guarantees quietly stop holding, and the cost depends on
**selectivity** rather than on the filter's existence:

| Filter selectivity | Pre-filter risk | Post-filter risk |
|---|---|---|
| 50% of corpus | Low | Low |
| 10% | Medium | Medium |
| 1% | High — ANN degrades on a subset too small to traverse | High — recall collapse |
| 0.1% | Critical | Critical |

Post-filtering forces you to over-retrieve by 10–100× to compensate, which spends the latency the
index was bought to save. [[ACORN-1]] keeps recall under aggressive filtering by walking multi-hop
neighbourhoods, at a real price: in the referenced benchmark it evaluates roughly **23× more nodes**
than standard HNSW (~600 → ~14,000).

Worth noting how this interacts with Axis 0: under a full scan a metadata predicate is just a mask
over the score array, so the whole problem dissolves. Filtering difficulty is a cost of
approximation, not an inherent property of vector search. See [[Vector Filtering]].

## Axis 4 — Build Cost, Updates, and CRUD

Query-time curves hide this entirely. Three questions the recall-vs-QPS plot cannot answer:

- **What does indexing cost?** [[HNSW]] builds in roughly O(n log n); [[IVF]] needs k-means training
  first (rule of thumb `nlist ≈ sqrt(n)`, and ≥ 39 × `nlist` training vectors) but is fast after.
- **Can it accept writes?** HNSW takes incremental inserts. IVF's centroids are fixed once trained,
  so significant corpus drift means retraining. Some algorithms are batch-oriented and cannot build
  an index until a large sample of vectors exists.
- **Does the deployment isolate ingest from queries?** See Axis 6 — this decided Reddit's choice.

[[ann-benchmarks]] is explicit that indexing cost and update support are outside what it measures,
which is exactly why a strong published curve does not mean a system fits your write pattern.

## Axis 5 — One Vector per Document, or Many

[[Bi-Encoder]] pooling gives one vector per document: cheapest to store, cheapest to index, and the
weakest at surviving a change of domain (see [[Zero-Shot Retrieval]]). [[Late Interaction]] models
like [[ColBERT]] keep per-token vectors and defer matching to query time — better quality and better
transfer, at multiplied storage and a MaxSim comparison too expensive for first-stage retrieval.

[[MUVERA]] is the compromise worth knowing: collapse the multi-vector representation into a single
fixed-dimensional vector that approximates MaxSim under an ordinary inner product, retrieve with
standard single-vector [[HNSW]], then rerank the candidates with full [[ColBERT]]. The multi-vector
cost moves to stage two, where the candidate set is small.

## Axis 6 — Cost, Topology, and Choosing a System

At scale the decision stops being about algorithms. [[Reddit - Vector Database Selection]] is the
vault's worked example of doing this properly: 11 candidate systems scored qualitatively on ~60
weighted criteria, open source as a hard constraint, then quantitative benchmarking of Qdrant v1.12
against Milvus v2.4 at **340M post vectors, 384 dims, HNSW `M=16` / `efConstruction=100`, under
100–400 QPS with filtering and ingest load.**

What decided it was not recall. [[Milvus Vector DB|Milvus]]'s heterogeneous node architecture
(separate query, ingest and index nodes) isolated ingest from query traffic better than Qdrant's
homogeneous nodes, and it won on organisational fit — Go codebase matching Reddit's stack, automatic
rebalancing, project velocity. [[Qdrant Vector DB|Qdrant]] had better raw latency in some
single-replica tests. In that evaluation, once both candidates cleared the quality bar the decision
turned on **deployment architecture and organisational fit rather than retrieval numbers** — one
well-documented selection, not a general law, but a useful prompt for what to benchmark beyond
recall and QPS.

## What to Measure

Two different things get called evaluation here, and conflating them makes this whole space
undebuggable:

| | Approximation fidelity | Relevance quality |
|---|---|---|
| Question | Did the index return what an exact scan would? | Are the results any good? |
| Ground truth | A [[Brute-Force Vector Search\|brute-force]] scan | Human or LLM judgments |
| Metric | `recall@k`, equivalently `overlap@k` | NDCG, MRR |

A model with poor relevance can post perfect `overlap@10`; an index at 90% recall can be
indistinguishable from exact in a user-facing metric. Measure both, or "quality dropped" has no
diagnosis. See [[Vector Search Evaluation]].

**How much fidelity you need is a property of the use case, not the index.** Bergum's framing: a
billion-photo image search does not need perfect recall — *"there are many equally great cat
photos"* — while a retina scan deciding building access needs excellent `overlap@1`. Academic ANN
work separates these as high-recall and low-recall settings.

## Recurring Pitfalls

- **Buying complexity you don't need.** The default assumption that a corpus requires a vector
  database usually goes unmeasured. Measure the scan first.
- **Treating "we use ANN" as a spec.** Recall varies enormously between implementations at the same
  throughput.
- **Assuming benchmark results transfer.** [[SIFT1M]] is 128-dimensional image descriptors; modern
  text embeddings run 384–1536+ dims with different distributional structure. Good SIFT1M numbers
  don't automatically carry over.
- **Averaging over query classes.** A regression confined to one class — exact-term lookups,
  parameter names, error codes — is invisible in an aggregate and total for the users issuing it.
  See [[Search Quality Assurance]].
- **Debugging downstream of the damage.** If a document never entered the candidate set, no reranker
  or generator recovers it. [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]] is the
  case study; the same logic applies to recall lost at the ANN stage.
- **Accepting "we use hybrid search" from a vendor.** Ask how the scores are combined, and for
  quality broken out by query type.

## Related Notes

- [[Approximate Nearest Neighbor Search]] — the parent concept and index-family reference
- [[Brute-Force Vector Search]] — Axis 0, and the baseline every other axis is measured against
- [[Dimensionality Reduction vs Quantization]] — Axis 2 in full
- [[Vector Filtering]] · [[ACORN-1]] — Axis 3 in full
- [[Vector Search Evaluation]] — fidelity versus relevance quality
- [[Vector Similarity Metrics]] — the distance function underneath all of it
- [[Search Platforms]] — the engine-level view of the same decisions
- [[Hybrid Search]] — where the lexical branch enters, with its own fusion tradeoffs

## Sources

- [[Just brute force your embeddings]] — [[Doug Turnbull]]; measured NumPy scan throughput, and the argument against adopting a vector database at ~1m documents
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]]; the three axes above, `overlap@k`, high- vs low-recall settings, and reading the ann-benchmarks curves
- [[Choosing a Vector Database for ANN Search at Reddit]] — the selection process behind [[Reddit - Vector Database Selection]]
- [[Choosing Indexes for Similarity Search (Faiss in Python)]] — Flat / LSH / HNSW / IVF compared hands-on on [[SIFT1M]]
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — quantization tradeoffs measured
- [[Principal Component Analysis - an embedding shrink-ray]] — the measured recall-vs-dimensions curve
- [[Why Are Embeddings So Cheap]] — why producing vectors is cheap while serving them is not
- [[Dense Retrieval at Vinted]] — HNSW on [[Vespa]] at billion scale in production
- [[Exploring Hierarchical Navigable Small World]] — HNSW internals and PCA as preprocessing
