---
title: Reddit - Vector Database Selection
type: case-study
tags:
  - case-study
  - vector-database
  - evaluation
  - ann
company: "[[Reddit]]"
year: 2025
created: 2026-06-01
---

# Reddit - Vector Database Selection

In 2025, Reddit's engineering team ran a systematic evaluation to replace fragmented ANN vector search solutions with a single company-wide vector database. After rigorous qualitative scoring and quantitative benchmarking, they selected **Milvus** over Qdrant.

---

## Problem

Reddit teams were using multiple incompatible ANN solutions:
- Google Vertex AI Vector Search
- Apache Solr ANN for larger datasets
- Facebook FAISS in vertically-scaled sidecars for smaller datasets

This fragmentation created inconsistent capabilities, high operational overhead, and gaps in feature support (e.g., FAISS has no filtering).

## Solution

Selected **Milvus** as the unified vector database for ANN search across Reddit teams.

## Evaluation Process

1. **Requirements collection** from all interested teams (functional + non-functional); requirement bias was actively challenged
2. **Qualitative scoring** of 11 candidates on ~60 weighted criteria
3. **Quantitative benchmarking**: Qdrant v1.12 vs Milvus v2.4 at 340M post vectors (384 dims, HNSW M=16, efConstruction=100)
4. Open-source as a hard constraint (eliminated Vertex AI, Pinecone)

## Key Results

- Milvus's heterogeneous node architecture (separate query/ingest/index) isolated ingest from query traffic better than Qdrant's homogeneous nodes
- At RF=2, Milvus sustained higher QPS with acceptable latency
- Qdrant had better raw latency in some single-replica tests
- Milvus won on organizational fit: Go codebase (matches Reddit's stack), automatic rebalancing, stronger project velocity

## Scale

- ~340M Reddit post vectors
- 384 dimensions
- Testing at 100–400 QPS with filtering and ingest load

---

## Company
- [[Reddit]]

## Tools
- [[Milvus Vector DB]] — selected solution
- [[Qdrant Vector DB]] — main alternative

## People
- [[Chris Fournie]] — evaluation lead

## Articles
- [[Choosing a Vector Database for ANN Search at Reddit]]
