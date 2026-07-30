---
created: 2026-07-30
title: "Three mistakes when introducing embeddings and vector search"
aliases:
  - "Four mistakes when introducing embeddings and vector search"
source: "https://bergum.medium.com/four-mistakes-when-introducing-embeddings-and-vector-search-d39478a568c5"
author: "[[Jo Kristian Bergum]]"
published: 2023-04-14
type: article
access: paywalled
concepts:
  - "[[Zero-Shot Retrieval]]"
  - "[[Embedding Fine-tuning]]"
  - "[[Brute-Force Vector Search]]"
  - "[[Approximate Nearest Neighbor Search]]"
topics:
  - "[[Vector Search Tradeoffs]]"
  - "[[Search Platforms]]"
tags: [article, embeddings, vector-search, ann, zero-shot, embedding-fine-tuning, paywalled]
---

# Three mistakes when introducing embeddings and vector search

**Author:** [[Jo Kristian Bergum]] · written while working on [[Vespa]]

## Summary

Three failure modes teams hit when adopting embedding-based retrieval (EBR): shipping a
pre-trained model with no task fine-tuning, trusting a single-vector model fine-tuned on
[[MS MARCO]] once the domain shifts, and reaching for approximate search without pricing the
tradeoffs. The third section is the origin of the line later quoted by [[Doug Turnbull]] —
*"an exhaustive search might be all you need."*

> The article's own closing summary section is not captured here.

## What an Embedding Actually Is

The post opens with [[Roy Keyes]]' definition — *"Embeddings are learned transformations to
make data more useful"* ([The shortest definition of embeddings?](https://roycoding.com/blog/2022/embeddings.html)) —
and places the practice in representation learning, a research field for decades. The surge in
interest is attributed to better architectures (Transformers) plus self-supervised
representation learning, with LLM hype layered on top.

Self-supervised pre-training on unlabeled piles of data, then fine-tuning on a smaller labeled
set for a specific task, is **transfer learning**. Bergum's running analogy: learning to
snowboard transfers to skateboarding, windsurfing and surfing — a device he reuses to make each
mistake land.

### The BERT mechanics the mistakes depend on

- Weights come from pre-training with a **masked language model** objective.
- Vocabulary is ~30K wordpieces for vanilla English BERT. Out-of-vocabulary words all collapse
  to a single `UNK` identifier — the model *cannot distinguish "foo" from "bar"* if neither is
  in the vocabulary.
- Input is capped at **512 wordpieces**, a consequence of attention's quadratic cost.
- Output is one vector per input token — 512 × 768 floats for vanilla [[BERT]]. Unlike
  [[Word2Vec]], each token vector is contextualised by attention over the whole input.
- Getting *one* vector per passage means either picking a single output vector or **pooling**
  (e.g. average pooling across the 512 outputs) — see [[Token Pooling]].

That pooled single vector is what the first two mistakes are about.

## Mistake #1: Using pre-trained models without task-specific fine-tuning

Vector representations taken straight from a pre-trained-only model are not useful for any
task. Encoding queries and documents and expecting cosine similarity to rank by relevance is
naive and yields *"next to random ranking results"* — detailed in the author's
[How not to use BERT for search ranking](https://bergum.medium.com/how-not-to-use-bert-for-search-ranking-4586716428d9).
Snowboard skills don't transfer to golf or swimming.

See [[Embedding Fine-tuning]].

## Mistake #2: Using fine-tuned single vector embedding models out-of-domain

Fine-tuning on labeled relevant/irrelevant pairs — [[MS MARCO]] being the large web-search
collection for this — produces embeddings that beat [[BM25]] *"by a very large margin"* on MS
MARCO itself.

The trap is that the same single-vector model **does not beat BM25 in a different domain** with
slightly different documents and questions. [[BEIR]] exists to measure exactly this, and the
post quotes the benchmark's own finding:

> We studied the effectiveness of ten different retrieval models and demonstrate that in-domain
> performance cannot predict how well an approach will generalize in a zero-shot setup. Many
> approaches that outperform BM25 in an in-domain evaluation on MS MARCO, perform poorly on the
> BEIR datasets.

Bergum's stated remedy: multi-vector models such as [[ColBERT]] *"generalize much better than
single-vector representations."* See [[Zero-Shot Retrieval]].

## Mistake #3: Lack of understanding of vector search tradeoffs

The question to ask before adopting ANN is whether you need it at all. The axes, all on the
query-serving side:

| Axis | The question |
|---|---|
| **Latency SLA** | 0.001ms, 1ms, 10ms, 100ms, a second — maybe 3 seconds is fine? |
| **Throughput** | 1 QPS, 1M QPS, billions? What's the anticipated max? |
| **Accuracy loss tolerated** | Approximate search loses accuracy versus exhaustive; how much can this use case absorb? |

All three collapse into deployment cost: how many servers, *or servers at all*. Document-side
complexity — CRUD, real-time versus batch — is additional and not counted here.

Accuracy loss is measured by running the **exact** search, comparing against the approximate
output, and computing the overlap between the two: `overlap@10`, or `overlap@1`.

**Why tolerance is use-case dependent:** a billion-photo image search doesn't need perfect
recall — *"there are many equally great cat photos."* A retina-scan app deciding building
access needs excellent `overlap@1`. Academic ANN research separates these as **high-recall**
and **low-recall** settings.

## An exhaustive search might be all you need

Exact search brute-forces the distance between the query and all eligible documents, so the
returned k *are* the true nearest neighbours. It parallelises, is multi-threaded, and can use
optimised hardware instructions — *"vectors are the machine's language."* It can also be
efficiently restricted to a subset when the vectors live in an engine with query-engine
filtering.

Reported figure: brute-forcing **1M vectors at 128 dimensions takes about 100ms
single-threaded**, down to **about 25ms on four threads — until memory bandwidth hits**. Paging
vectors randomly from disk is slower but still parallelisable.

The ceiling is cost, not correctness. At 10B vectors with no way to select a subset, latency can
still be held down by distributing the search across nodes in parallel (as [[Vespa]] does), but
renting servers for billions of embeddings gets expensive — and adding high query throughput
makes it *"a real cost problem."*

## Introducing approximations

Going approximate means indexing the vectors so search costs less than a full scan, paid for in
resource usage and indexing work, with further tradeoffs in disk usage, memory usage, and how
well the algorithm handles real-time CRUD.

[[ann-benchmarks]] is offered as the source of understanding here. Reading its [[SIFT1M]] graph
(1M × 128-dim), recall@10 against QPS, single-threaded:

- 10² QPS ⇒ 10ms latency; 10³ QPS ⇒ 1ms. *"These algorithms are pretty damn fast."*
- 2 cores ≈ 2× QPS, absent contention or locking problems.
- Up and to the right is the better tradeoff; **some algorithms struggle to get past 50% recall.**

Two things the graph does not show: **indexing cost**, and whether the algorithm supports
updates — some are batch-oriented and need a large vector sample before an index can be built,
others build incrementally. And a caveat with teeth: ann-benchmarks can only cover open-source
algorithms reproducible on one runtime, so *"some commercial and proprietary vector search
vendors have unknown recall versus performance tradeoffs."*

## Related Concepts

- [[Zero-Shot Retrieval]] — Mistake #2 generalised
- [[Embedding Fine-tuning]] — the fix for Mistake #1
- [[Brute-Force Vector Search]] — the exhaustive baseline this post defends
- [[Approximate Nearest Neighbor Search]] — what Mistake #3 is about pricing
- [[ColBERT]] · [[Late Interaction]] — the multi-vector alternative recommended here
- [[Bi-Encoder]] — the single-vector architecture that fails out-of-domain
- [[BERT]] · [[Token Pooling]] — how one vector per passage gets produced
- [[Vector Search Evaluation]] — where `overlap@k` sits relative to relevance metrics

## Related Articles

- [[Just brute force your embeddings]] — [[Doug Turnbull]] quotes this post's exhaustive-search
  argument and measures it again on modern hardware
- [[Principal Component Analysis - an embedding shrink-ray]] — reducing scan cost rather than
  indexing

## Datasets

- [[MS MARCO]] — the fine-tuning collection behind Mistake #2
- [[BEIR]] — the benchmark that exposes it
- [[SIFT1M]] — the vector set in the ann-benchmarks graph discussed here

## People

- [[Jo Kristian Bergum]] — author
- [[Roy Keyes]] — quoted for the definition of embeddings

## External References

- Roy Keyes, *The shortest definition of embeddings?* — https://roycoding.com/blog/2022/embeddings.html
- *How not to use BERT for search ranking* — https://bergum.medium.com/how-not-to-use-bert-for-search-ranking-4586716428d9
- Vespa zero-shot ranking series — https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa/ ·
  https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa-part-two/ ·
  https://blog.vespa.ai/improving-text-ranking-with-few-shot-prompting/
- Multi-vector indexing — https://blog.vespa.ai/semantic-search-with-multi-vector-indexing/
- Pretrained Transformer language models for search, part 3 — https://blog.vespa.ai/pretrained-transformer-language-models-for-search-part-3/
- ann-benchmarks — https://github.com/erikbern/ann-benchmarks
- MS MARCO — https://microsoft.github.io/msmarco/ · BEIR — https://github.com/beir-cellar/beir
