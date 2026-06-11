---
title: OpenSearch
type: tool
tags:
  - tool
  - search-engine
  - vector-search
  - open-source
  - lucene
  - aws
website: https://opensearch.org
repo: https://github.com/opensearch-project/OpenSearch
maintainer: "AWS / Linux Foundation"
created: 2026-06-01
---

# OpenSearch

Open-source distributed search and analytics engine forked from Elasticsearch 7.10.2 in 2021 by AWS, after Elastic changed its license from Apache 2.0 to SSPL/Elastic License. Licensed under Apache 2.0 and governed by a community that includes the Linux Foundation. Primary managed offering: Amazon OpenSearch Service.

- Website: https://opensearch.org
- GitHub: https://github.com/opensearch-project/OpenSearch

---

## What It Does

OpenSearch indexes documents as JSON and exposes a REST API for full-text search, aggregations, filtering, and vector ANN search. Architecture mirrors Elasticsearch at the shard/node level — same Lucene foundation, same distributed replication model. Horizontally scalable.

Key capabilities:
- **Full-text search** — [[BM25]]-based relevance scoring via Lucene
- **Dense vector search** — k-NN plugin with HNSW; supports Faiss, nmslib, and native Lucene backends; up to 16,000 dimensions
- **Hybrid search** — BM25 + kNN with normalization pipeline; native RRF support
- **Neural sparse retrieval** — learned sparse encoding (open-source counterpart to [[ELSER]])
- **Search pipelines** — composable request/response processors for ML inference and score normalization
- **Aggregations** — `significant_terms`, facets, histograms; foundational for [[Wormhole Vectors]] traversal
- **PPL (Piped Processing Language)** — SQL-like analytics query language

## Retrieval Options

| Mode | Query type | Notes |
|------|-----------|-------|
| BM25 | `match`, `multi_match` | Default; no ML dependency |
| Dense semantic | `knn` | k-NN plugin; choice of Faiss / nmslib / Lucene engine |
| Hybrid | `hybrid` + normalization pipeline | Built-in RRF and min-max normalization |
| Neural sparse | `neural_sparse` | Requires a sparse encoding model |

## Vector Search: k-NN Plugin Backends

| Engine | Notes |
|--------|-------|
| **Faiss** | Facebook's library; strong at scale; GPU support |
| **nmslib** | HNSW; good recall/speed balance; original plugin default |
| **Lucene** | Native HNSW; no plugin overhead; best for smaller indexes |

## AWS Integration

Deployed as **Amazon OpenSearch Service**, OpenSearch gains:
- Native IAM, VPC, CloudWatch, and Kinesis integration
- Direct connector to **Amazon Bedrock** for embedding inference and RAG generation
- Managed scaling, snapshots, and patching

See [[Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock]].

## Advanced Retrieval: Wormhole Vectors

[[Wormhole Vectors]] exploit OpenSearch's k-NN plugin and `significant_terms` aggregations together to traverse between dense, sparse, and behavioral vector spaces — beyond what standard RRF hybrid search achieves.

```python
# Dense query → aggregate statistically significant keywords from results
response = client.search(
    index="products",
    body={
        "size": 50,
        "query": {"knn": {"embedding_vector": query_vector, "k": 50}},
        "aggs": {
            "wormhole_keywords": {
                "significant_terms": {"field": "description_keywords", "size": 10}
            }
        }
    }
)
```

See [[Wormhole Vectors Beyond Hybrid Search in OpenSearch]] — [[Dima Kan]] (Aiven).

## Performance vs. Elasticsearch

2024–2025 benchmarks show Elasticsearch consistently faster:
- Text search / aggregations: **40–140% faster**
- Vector search: **2–12x faster**

The gap is largest on complex, high-throughput workloads. At smaller scales the difference narrows and OpenSearch is often sufficient. See [[Elasticsearch vs OpenSearch]] for the full comparison.

## Notable Implementations in This Vault

- [[Dima Kan]] (Aiven) — Wormhole Vectors in production; SKG traversal across sparse, dense, and behavioral spaces
- Canva — one of three parallel candidate generators alongside Solr and SageMaker (see [[Canva Search Pipeline Part II]])

## Related Tools

- **[[Elasticsearch]]** — upstream project; faster but proprietary-licensed above 7.10
- **[[Metarank]]** — external LambdaMART secondary re-ranker that integrates with OpenSearch (Remote Ranker Plugin RFC)
- **OpenSearch Dashboards** — visualization layer (Kibana fork)

## Related Concepts

- [[BM25]] — default scoring model
- [[Hybrid Search]] — BM25 + kNN combination
- [[Dense Vector Retrieval]] — k-NN plugin architecture
- [[HNSW]] — ANN index for dense vectors
- [[Reciprocal Rank Fusion]] — fusion strategy used in normalization pipeline
- [[Wormhole Vectors]] — advanced SKG traversal via OpenSearch primitives
- [[RAG]] — common AWS-native use case via Bedrock

## Articles

- [[Wormhole Vectors Beyond Hybrid Search in OpenSearch]] — [[Dima Kan]]; SKG traversal beyond RRF
- [[Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock]] — RAG pipeline on AWS with code
- [[How to Really Scale Autocomplete]] — `significant_terms`-based autocomplete patterns
- [[Learn-to-Rank with OpenSearch and Metarank]] — [[Roman Grebennikov]]; LambdaMART secondary re-ranking on top of OpenSearch via [[Metarank]]; Remote Ranker Plugin RFC

- [[Elasticsearch vs. OpenSearch (2025) The Definitive Showdown]] — [[Jagadeesh Chandra]]; 2025 performance comparison
- [[OpenSearch vs. Elasticsearch A Comprehensive Comparison in 2025]] — [[Frank Goortani]]; balanced licensing and performance comparison
- [[OpenSearch vs. Elasticsearch in 2025 - What's Changed and What Hasn't]] — Dattell; licensing (SSPL vs Apache 2.0), features, plugins, ecosystem

## Comparison

- [[Elasticsearch vs OpenSearch]] — licensing, performance, feature differences, and when to choose each
