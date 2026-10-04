---
type: tool
title: autofaiss
aliases:
  - AutoFaiss
  - Autofaiss
website: https://criteo.github.io/autofaiss/
repo: https://github.com/criteo/autofaiss
license: Apache-2.0
company: "[[Criteo]]"
tags:
  - tool
  - vector-search
  - ann
  - faiss
  - library
  - open-source
related_concepts:
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Vector Quantization]]"
  - "[[Brute-Force Vector Search]]"
related_topics:
  - "[[Vector Search Tradeoffs]]"
created: 2026-10-04
---

# autofaiss

An open-source Python library from [[Criteo]] that builds [[FAISS]] k-nearest-neighbour indexes automatically. Instead of choosing an index type and its hyperparameters yourself, you set a maximum index size and a maximum query time, and autofaiss picks the index and parameters that give the highest recall within those limits.

- Repository: https://github.com/criteo/autofaiss (Apache-2.0)
- Docs: https://criteo.github.io/autofaiss/
- Launch post: [[Introducing Autofaiss - An Automatic K-Nearest-Neighbor Indexing Library At Scale]] (August 2021)
- Releases: 2.17.0 in January 2024, then 2.18.0 in November 2025, which mainly updated dependencies and CI

---

## What it does

FAISS offers hundreds of index combinations, each with up to six build hyperparameters and further search-time parameters. autofaiss searches that space for you using FAISS's efficient indexes, binary search and heuristics, maximising recall under two constraints:

| Constraint | CLI flag |
|---|---|
| Index memory | `--max_index_memory_usage` (e.g. `"10GB"`) |
| Query latency | `--max_index_query_time_ms` (e.g. `10`) |

A single `autofaiss quantize` command reads a folder of embeddings and writes the tuned index; the similarity metric is set with `--metric_type` (e.g. `"ip"`). Passing a FAISS `index_key` fixes the index type and has autofaiss tune only its parameters.

The launch post credits [[Vector Quantization|product quantization]] for its headline compression.

## The project's own numbers

On a 200-million-vector image-embedding dataset of about 1 TB, the authors report an index of about 10 GB built in 3 hours with about 15 GB of memory, answering queries in about 10 ms. These are Criteo's figures, without an independent benchmark or a stated recall value.

## Where it fits

- **Automates the index-choice step.** The trade-offs in [[Vector Search Tradeoffs]] — recall against latency against memory — are exactly what autofaiss searches over. The usual hand-made alternative is FAISS's own index-choice guide, or benchmarks like [[Choosing Indexes for Similarity Search (Faiss in Python)]].
- **FAISS-only.** It builds FAISS indexes and nothing else, so everything FAISS lacks on its own — filtering, persistence, live updates — autofaiss lacks too.
- **Release history.** The repository is not archived; the latest release is 2.18.0 (November 2025), and the one before it 2.17.0 (January 2024).

## Related Tools

- [[FAISS]] — the library it wraps

## Related Concepts

- [[Approximate Nearest Neighbor Search]]
- [[Vector Quantization]] — product quantization, the main compression lever
- [[Brute-Force Vector Search]] — the exact baseline

## Related Topics

- [[Vector Search Tradeoffs]]

## Articles

- [[Introducing Autofaiss - An Automatic K-Nearest-Neighbor Indexing Library At Scale]] — launch post

## People

- [[Victor Paltz]] · [[Romain Beaumont]] — authors of the launch post

## Company

- [[Criteo]]
