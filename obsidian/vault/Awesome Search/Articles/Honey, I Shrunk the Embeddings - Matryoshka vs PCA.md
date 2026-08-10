---
type: article
title: "Honey, I Shrunk the Embeddings: Matryoshka vs. PCA"
source: "https://dylancastillo.co/posts/matryoshka-vs-pca"
author: "[[Dylan Castillo]]"
published: 2026-08-01
created: 2026-08-10
tags: [article, PCA, matryoshka, dimensionality-reduction, embeddings, vector-search, quantization, BEIR, benchmark]
concepts: ["[[PCA]]", "[[Matryoshka Embeddings]]", "[[Dimensionality Reduction]]", "[[Binary Quantization]]", "[[Scalar Quantization]]", "[[NDCG]]", "[[Dense Vector Retrieval]]"]
topics: ["[[Dimensionality Reduction vs Quantization]]", "[[Embedding Models Compared]]"]
---

# Honey, I Shrunk the Embeddings: Matryoshka vs. PCA

**Author:** [[Dylan Castillo]]

A head-to-head benchmark of the two ways to shrink an embedding: truncating an
[[Matryoshka Embeddings|MRL]]-trained vector, versus fitting a [[PCA]] projection
after the fact. Eight [[BEIR]] datasets, three models, five target dimensions,
about $30 of compute.

The author's own summary of the result:

> "PCA not only held its own against MRL truncation, it won on most dimensions."

This is a single practitioner benchmark rather than a settled finding — see
*Standing in the vault* below for how it sits against the existing guidance.

## Setup

**Quality retained** is nDCG@10 at the reduced dimension divided by nDCG@10 at
full dimensions, averaged across the eight datasets — so 100% means the shrunk
index ranks as well as the original, not that it returns identical results.

- **Datasets** — SciFact, NFCorpus, ArguAna, FiQA-2018, SciDocs, Quora,
  TREC-COVID, Touché-2020 (all [[BEIR]] subsets)
- **Models** — OpenAI `text-embedding-3-small` (1,536d, MRL),
  `qwen3-embedding-8b` (4,096d, MRL), `text-embedding-ada-002` (1,536d, no MRL)
- **Dimensions** — 512, 256, 128, 64, 32
- **Truncation** — keep the first *d* dimensions and re-normalize
- **PCA** — projection fit on full-dimension *document* embeddings from the
  target dataset

## Truncation vs PCA

`text-embedding-3-small` (1,536d):

| Dims | Truncation | PCA |
|---|---|---|
| 512 | 98% | 97% |
| 256 | 94% | 95% |
| 128 | 86% | 90% |
| 64 | 71% | 82% |
| 32 | 46% | 65% |

`qwen3-embedding-8b` (4,096d):

| Dims | Truncation | PCA |
|---|---|---|
| 512 | 99% | 98% |
| 256 | 96% | 96% |
| 128 | 91% | 91% |
| 64 | 83% | 84% |
| 32 | 68% | 71% |

The shape reported is consistent across the two MRL models: the methods are
close down to 256, and PCA pulls ahead as compression gets aggressive. On
`3-small` at 32 dims the gap is 19 percentage points. On `qwen3-embedding-8b`
the gap barely opens at all — a 4,096-dim model has enough headroom that both
methods survive comfortably to 512.

## Does PCA only work because the model was MRL-trained?

The control is `text-embedding-ada-002`, which predates MRL:

| Dims | Truncation | PCA |
|---|---|---|
| 512 | 96% | 99% |
| 256 | 89% | 96% |
| 128 | 83% | 89% |
| 64 | 66% | 78% |
| 32 | 41% | 59% |

PCA on ada-002 retains 78% at 64 dims and 59% at 32, against 82% and 65% for
`3-small`. On these numbers PCA is not riding on MRL training — it works on a
model that was never trained to be truncatable, and the MRL model's advantage
over the non-MRL one is a few points rather than a category difference.

Truncating ada-002 is also not catastrophic here (96% at 512), which is a softer
result than the usual "a standard model truncated loses most performance" framing.

## How much data does the projection need?

Fitting PCA on FiQA with 1,000 / 5,000 / 20,000 / 57,000 documents produced
almost no spread — "the projection fit on 1,000 documents performs almost the
same as the one fit on the full corpus."

Fitting **out of domain** — one projection fit on [[MS MARCO]] passages, applied
to every dataset — also held up better than the author expected: through 512–64
dims for `3-small`, and through 128 dims for `qwen3-embedding-8b`, which then
drops to 56% at 32 against 71% for the in-domain fit.

This is the operationally interesting part. The standard objection to PCA is the
calibration burden — you need representative data, you must store the matrix,
and you must apply it identically at index and query time. On this evidence two
of those three are cheaper than assumed: a thousand documents was enough, and
the documents did not have to come from the target corpus.

## Stacking with quantization

`text-embedding-3-small` at full 1,536 dims:

| Config | Bytes/vector | Size vs float32 | Quality |
|---|---|---|---|
| float32 | 6,144 | 100% | 100% |
| int8 ([[Scalar Quantization]]) | 1,536 | 25% | 100% |
| binary ([[Binary Quantization]]) | 192 | 3.1% | 95% |
| binary + PCA to 512 | 64 | ~1% | 82% |

Quantization is the cheaper first move by a wide margin: int8 is 4× smaller at
no measured quality cost, where PCA to 512 already costs 2–3 points, and binary
alone gives 32× for five points. Dimensionality reduction reads here as the
second multiplier on `bytes = dimensions × bits per dimension`, worth spending
after the bit-level compression rather than instead of it.

## Limitations the author states

- Three models, two of them from the same vendor
- The largest [[BEIR]] datasets were excluded on budget grounds
- Exact search over raw vectors, not approximate indexing in a real vector
  database — so these numbers isolate representation loss and say nothing about
  how the two compressed spaces behave under [[HNSW]]
- BEIR's presence in embedding-model training data is a contamination risk

The ANN caveat is the one that matters most for a production reading. PCA output
is anisotropic by construction, which interacts badly with quantizers and graph
indexes alike — an effect this methodology cannot observe. See
[[Dimensionality Reduction vs Quantization]] for the rotation step that addresses it.

## Standing in the vault

This is one practitioner's benchmark, and it points the opposite way from the
working recommendation in [[Dimensionality Reduction vs Quantization]], which
treats MRL truncation as the cleanest option where the model supports it. The
guidance there has not been rewritten on the strength of a single study; the
disagreement is recorded and attributed instead.

Worth noting that [[Doug Turnbull]]'s [[Principal Component Analysis - an embedding shrink-ray]]
reaches much harsher conclusions about PCA on a different model, corpus and
metric — MiniLM on [[MS MARCO]], 384→50, recall collapsing to 0.2029. The two
sets of numbers are not directly comparable, and the spread between them is
itself the argument for measuring compression on your own model and corpus.

## Related Articles

- [[Principal Component Analysis - an embedding shrink-ray]] — [[Doug Turnbull]];
  same technique, harsher numbers, measured as recall against brute-force ground
  truth rather than nDCG retention
- [[Introduction to Matryoshka Embedding Models]] — the MRL training technique
- [[Matryoshka Embeddings - Faster OpenAI Vector Search]] — the adaptive-retrieval
  pattern these truncation numbers apply to
- [[Qwen3 Embedding Series]] — one of the three models benchmarked

## Related Concepts

- [[PCA]] · [[Matryoshka Embeddings]] — the two methods compared
- [[Dimensionality Reduction]] — parent concept
- [[Scalar Quantization]] · [[Binary Quantization]] — the cheaper axis
- [[NDCG]] — the retention metric's basis
- [[Dense Vector Retrieval]] · [[Brute-Force Vector Search]] — the evaluation setting

## Related Topics

- [[Dimensionality Reduction vs Quantization]] — where this evidence lands
- [[Embedding Models Compared]] — dimensionality as a selection axis
- [[Vector Search Tradeoffs]]

## Datasets

- [[BEIR]] — the eight subsets used
- [[MS MARCO]] — the out-of-domain PCA fitting corpus

## Sources

- Article: https://dylancastillo.co/posts/matryoshka-vs-pca
- Code and data: published on GitHub per the article
