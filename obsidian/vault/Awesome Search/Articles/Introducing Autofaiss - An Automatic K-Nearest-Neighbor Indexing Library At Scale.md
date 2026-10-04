---
type: article
title: "Introducing Autofaiss: An Automatic K-Nearest-Neighbor Indexing Library
  At Scale"
aliases:
  - Introducing Autofaiss
source: https://medium.com/criteo-engineering/introducing-autofaiss-an-automatic-k-nearest-neighbor-indexing-library-at-scale-c90842005a11
author:
  - "[[Victor Paltz]]"
  - "[[Romain Beaumont]]"
company: "[[Criteo]]"
published: 2021-08-12
created: 2026-10-04
tools:
  - "[[autofaiss]]"
  - "[[FAISS]]"
concepts:
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Vector Quantization]]"
  - "[[Brute-Force Vector Search]]"
  - "[[Dense Vector Retrieval]]"
  - "[[Multimodal Embeddings]]"
topics:
  - "[[Vector Search Tradeoffs]]"
tags:
  - article
  - vector-search
  - ann
  - faiss
  - quantization
  - company-blog
---

# Introducing Autofaiss: An Automatic K-Nearest-Neighbor Indexing Library At Scale

**Authors:** [[Victor Paltz]], [[Romain Beaumont]] · [[Criteo]] R&D Blog (Medium), 12 August 2021 · code at [criteo/autofaiss](https://github.com/criteo/autofaiss)

The launch post for [[autofaiss]], Criteo's open-source wrapper around [[FAISS]] that picks a k-nearest-neighbour index and its hyperparameters for you. You give it a RAM budget and a query-time budget; it returns the index that maximises recall inside them.

---

## Summary

The post opens with a short primer. A KNN search finds the vectors most similar to a query vector, and a KNN index is a data structure holding a transformed version of those vectors so the search runs efficiently. The running example is image search over a flower database. An encoder turns each image into a vector, so that two pictures of roses land close together and a rose and a sunflower land far apart. The index then returns the images whose vectors sit nearest the query image's vector.

**Why an index rather than a scan.** The authors argue that an exhaustive [[Brute-Force Vector Search|brute-force]] search is usually too expensive in both runtime and memory. Approximate algorithms fix the speed, but they can still hold too much in RAM to scale. FAISS's quantization-based indexes cut memory while keeping a reasonable recall and query-time trade-off.

**Product quantization, briefly.** The post's explanation of [[Vector Quantization|product quantization]]: split the vector space into many smaller sub-spaces, learn 256 cluster centres in each, and store each sub-vector as the integer ID of its nearest centre instead of as floats. Its worked figure shows a 16× reduction. The authors note that compressing further lowers both recall and how faithfully the compressed vectors reconstruct the originals.

**The problem autofaiss solves.** FAISS offers hundreds of algorithm combinations, each with up to six build hyperparameters, plus separate search-time parameters that set the recall/speed trade-off. The authors say most users don't understand the differences between them and end up spending a lot of time building sub-optimal indexes. At Criteo the team spent weeks calibrating index choices across query speed, index size, recall and build time. autofaiss packages the result.

## Headline result (authors' own)

- **Corpus:** 200 million image embeddings, about 1 TB.
- **Result:** an index of about 10 GB, built in 3 hours, answering queries in about 10 ms with what the authors call good recall. The TLDR puts the memory used at 15 GB.
- **Method:** FAISS's efficient indexes plus binary search and heuristics to choose the parameters.
- A benchmark figure compares index size against recall at a fixed 10 ms latency for different index types on the same dataset.

The authors credit the compression ratio and query speed to product quantization. No recall number or independent benchmark is given.

## Usage

One command builds an index from a folder of embeddings, under a memory cap and a latency cap:

```
autofaiss quantize --embeddings_path="embeddings_folder" \
                   --output_path="my_index_folder" \
                   --metric_type="ip" \
                   --max_index_memory_usage="10GB" \
                   --max_index_query_time_ms=10
```

Users who already know which index they want can pass a FAISS `index_key` and have autofaiss tune only its parameters. The post also links a Colab notebook for building an index and an interactive demo of how the index choice changes with the constraints.

## Why It Matters

- **The index-choice decision, automated.** Picking a FAISS index by hand means working through hundreds of algorithm combinations and their build and search hyperparameters. autofaiss turns that into a constrained search: state the budgets, get the best recall the library can find within them. It is a concrete tool for the recall/latency/memory surface described in [[Vector Search Tradeoffs]].
- **Memory as the binding constraint.** The post frames scale as a RAM problem first and a speed problem second, and its answer leans on quantization.

## Limitations

- All figures are the authors' own, from one 200M-vector image dataset, with no recall value stated.
- It only builds FAISS indexes, so the inherited limits apply: a library rather than a service, with no filtering or live updates of its own (see [[FAISS]]).

## Related Concepts

- [[Approximate Nearest Neighbor Search]] — the problem the index serves
- [[Vector Quantization]] — product quantization, the source of the compression
- [[Brute-Force Vector Search]] — the exhaustive scan the post argues against at this scale
- [[Dense Vector Retrieval]] — the retrieval setting
- [[Multimodal Embeddings]] — the image-search example

## Related Topics

- [[Vector Search Tradeoffs]]

## Related Articles

- [[Nearest Neighbor Indexes for Similarity Search]] — choosing a FAISS index by hand
- [[Choosing Indexes for Similarity Search (Faiss in Python)]] — the same decision, benchmarked in a video

## Tools

- [[autofaiss]] — the library introduced
- [[FAISS]] — the library it wraps

## People

- [[Victor Paltz]] — author
- [[Romain Beaumont]] — co-author

## Company

- [[Criteo]]
