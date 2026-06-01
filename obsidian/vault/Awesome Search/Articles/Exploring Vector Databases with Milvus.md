---
type: article
title: "Exploring Vector Databases with Milvus"
source: "https://medium.com/@hsinhungw/exploring-vector-databases-with-milvus-dbf917d9ab00"
author: "Henry"
published: 2024-02-06
tags:
  - article
  - vector-database
  - milvus
  - architecture
concepts:
  - HNSW
  - IVF
  - Vector Quantization
  - Dense Vector Retrieval
topics:
  - Search Platforms
---

# Exploring Vector Databases with Milvus

A deep technical dive into the Milvus vector database system architecture, closely following the 2021 SIGMOD paper "Milvus: A Purpose-Built Vector Data Management System." Covers the Query Engine, GPU Engine, Storage Engine, and distributed architecture.

---

## Background

Growth in unstructured data (images, text, video) and machine learning produced vector embeddings that capture semantic relationships. Traditional databases struggle with high-dimensional vector data, driving development of purpose-built vector databases. Milvus is built on top of Facebook FAISS with added scalability, dynamic data management, and a distributed architecture.

## System Architecture Overview

Three major components:

- **Query Engine** — CPU/GPU-optimized query processing over vector data
- **GPU Engine** — co-processing engine leveraging GPU parallelism; supports multi-GPU
- **Storage Engine** — data durability via LSM-based structure; LRU buffer pool; multi-storage backends (local, S3, HDFS)

## Query Engine

### Query Types
1. **Vector Query** — similarity search returning top-k most similar vectors
2. **Attribute Filtering** — vector similarity search with metadata constraints
3. **Multi-Vector Query** — similarity over composite multi-vector objects via an aggregation function

Supports similarity metrics: Euclidean distance, inner product, cosine similarity, Hamming distance, Jaccard distance.

### Indexing
Milvus supports **quantization-based indexes** and **graph-based indexes** (like HNSW). The core of quantization-based indexes:
- **Coarse quantizer**: K-means clustering to create K clusters
- **Fine quantizer**: encodes vectors within each cluster
- `n_probe` parameter controls the accuracy/speed tradeoff: higher n_probe → higher recall, slower queries

### Query Processing Optimizations
- **Cache-aware**: assigns threads to data vectors (not queries) to minimize CPU cache misses; leverages multi-core parallelism
- **SIMD-aware**: automatic runtime selection of SIMD instructions for distance computation
- **GPU**: co-processing with CPU for large workloads; copies multiple clusters in parallel to maximize I/O utilization; hybrid mode executes cluster-finding on GPU and in-cluster search on CPU when data transfer overhead is high

## Attribute Filtering Strategies

Milvus implements five strategies (A–E) for filtered ANN search:

| Strategy | Description | Best For |
|---|---|---|
| A | Filter first → full scan of matching vectors | Highly selective attribute filter |
| B | Filter first → ANN on matching vectors | Moderate selectivity |
| C | ANN first → filter hits | Low selectivity filter |
| D | Cost-based: pick A, B, or C by estimated cost | General case |
| E | **Partition-based** (Milvus's approach): partition by frequent attribute, apply D per partition | Production; outperforms D |

## Multi-Vector Queries

Two approaches for finding top-k multi-vector results:

**Vector Fusion** — for decomposable similarity functions (e.g., inner product on normalized data): concatenate all component vectors into one, aggregate query vectors similarly, then run standard ANN.

**Iterative Merging** — based on Fagin's NRA (No Random Access) algorithm: iteratively issue top-k' queries per component vector, merge results with NRA, double k' until k results can be determined.

## Storage Engine

- **LSM structure**: inserts buffered in memory → flushed to immutable disk segments when threshold reached → smaller segments merged for sequential access; deletes removed during merge
- **Buffer pool**: LRU-based cache for frequently accessed segments
- **Multi-storage**: local filesystem, Amazon S3, HDFS

## Distributed System

Three-layer architecture (Milvus 2.x):
1. **Coordinator layer** — metadata (sharding, load-balancing info)
2. **Computing layer** (Kubernetes-managed): single writer (WAL) + multiple auto-scaling readers; consistent hashing for data sharding; local caching to reduce storage I/O
3. **Storage layer** — Amazon S3 for high availability

Key features: asynchronous processing for throughput, **snapshot isolation** for consistent reads during dynamic updates.

---

## Related Concepts
- [[HNSW]] — graph-based ANN index supported
- [[IVF]] — quantization-based index (coarse + fine quantizer)
- [[Vector Quantization]] — foundational technique for Milvus indexes
- [[Dense Vector Retrieval]] — primary use case
- [[Vector Filtering]] — attribute filtering strategies A–E

## Related Articles
- [[Choosing a Vector Database for ANN Search at Reddit]] — Reddit's real-world Milvus vs. Qdrant benchmarking
- [[Milvus - Unlocking Your Data's Hidden Relationships]] — introductory Milvus overview

## Tools
- [[Milvus Vector DB]]
