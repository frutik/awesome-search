---
type: article
title: "Milvus - Unlocking Your Data's Hidden Relationships"
source: "https://romellfudi.medium.com/milvus-unlocking-your-datas-hidden-relationships-92da9522d415"
author: "[[Freddy Domínguez]]"
published: 2023-10-05
tags:
  - article
  - vector-database
  - milvus
  - embeddings
  - medium
concepts:
  - Embeddings
  - Dense Vector Retrieval
  - HNSW
topics:
  - Search Platforms
---

# Milvus - Unlocking Your Data's Hidden Relationships

An introductory overview of Milvus as a vector database for scalable similarity search and AI applications. Covers what Milvus is, its core advantages, how to embed plain data, and how to perform similarity search using those embeddings.

---

## What Is Milvus?

Milvus is an open-source vector database designed to empower similarity searches and AI applications based on embeddings. Built on top of Facebook FAISS (C++ library for vector similarity search), it adds:
- Dynamic data support (insertions and deletions via LSM-based storage)
- Scalable distributed architecture
- Heterogeneous computing (CPUs and GPUs)
- Multiple storage backends (local, S3, HDFS)
- Accessible APIs (SDKs, RESTful)

## Advantages as a Vector Database

1. **Efficient Similarity Search** — retrieve similar vectors from massive collections (news, reports, books, media)
2. **Dynamic Data Management** — handles insertions and deletions at scale via LSM structure; real-time search with snapshot isolation
3. **Multiple Index Types** — quantization-based and graph-based (HNSW); extensible interface
4. **Heterogeneous Computing** — CPUs + GPUs; SIMD optimizations
5. **Distributed System** — multi-node for scalability and availability
6. **Versatile Query Types** — vector similarity, attribute filtering, multi-vector queries

## Key Use Cases

- Security video frame identification (image similarity)
- Virtual library document retrieval (text similarity)
- Recommendation systems
- Any AI application requiring "find things similar to this"

---

## Related Concepts
- [[Embeddings]] — the data representation Milvus stores and searches
- [[Dense Vector Retrieval]] — primary search mode
- [[HNSW]] — graph-based ANN index supported by Milvus
- [[Vector Quantization]] — quantization-based indexes supported by Milvus

## Related Articles
- [[Exploring Vector Databases with Milvus]] — deep technical architecture dive
- [[Choosing a Vector Database for ANN Search at Reddit]] — production evaluation

## Tools
- [[Milvus Vector DB]]

## People
- [[Freddy Domínguez]] — author
