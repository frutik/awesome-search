---
type: article
title: "What is Elasticsearch and Why You Should Use It"
source: "https://bonsai.io/blog/what-is-elasticsearch-and-why-you-should-use-it/"
author: "[[Leo Schuster]]"
company: "[[Bonsai]]"
published: 2023-03-19
tags: [article, company-blog, elasticsearch, lucene, introduction, search-architecture]
concepts: ["[[Full-Text Search]]", "[[Inverted Index]]", "[[Search Architecture]]"]
topics: ["[[Search Platforms]]"]
created: 2026-06-27
---

# What is Elasticsearch and Why You Should Use It

An introductory [[Bonsai]] explainer by [[Leo Schuster]]: what [[Elasticsearch]] is, its architecture, and when it earns a place in a developer's toolkit. Aimed at newcomers evaluating a dedicated search engine.

---

## What It Is

"A distributed, RESTful search and analytics engine used to query, index, and store JSON data." Built on **Apache Lucene** (a 20+ year-old Java text-search library), it provides scalability, fault tolerance, and broad client compatibility without custom integration code.

## Architecture (the relational analogy)

| Elasticsearch | Rough RDBMS analogy |
|---|---|
| **Lucene** | underlying indexing library |
| **Node** | one Elasticsearch instance (best practice: one per server) |
| **Cluster** | nodes sharing a cluster name; auto primary election + failover |
| **Index** | "table" — logical namespace over shards |
| **Document** | "row" — a JSON record |
| **Primary shard** | data division enabling parallel query execution |
| **Replica shard** | redundancy for failover + serving read/search traffic |

## Key Features

- RESTful API; rich search + aggregation APIs
- Fault tolerance via replica shards (dynamically configurable)
- Rich-document ingestion via plugins (`mapper-attachment` / `ingest-attachment`, using **Apache Tika**)
- Kibana for visualization

## A Key Caveat

> "Elasticsearch is a search engine, not a content crawler."

Indexing is the **application's** responsibility — Elasticsearch does not autonomously extract content. To scan a website you need a separate crawler (e.g. Apache Nutch).

## When / Why to Use It

Fast time-to-value, real-time analytics, mature client ecosystem (Java, JS, Ruby, Python, Go, PHP, .NET, Perl; framework integrations like `searchkick`, `django-haystack`, `ElasticPress`). Hosting via self-managed or SaaS (Bonsai, Elastic Cloud, Amazon OpenSearch Service, Aiven, Instaclustr). Notable users cited: Netflix, Walmart, eBay.

## Related Concepts
- [[Full-Text Search]]
- [[Inverted Index]]
- [[Search Architecture]]

## Related Notes
- [[Elasticsearch]] — the tool note
- [[Elasticsearch vs OpenSearch]] — licensing/performance comparison
- [[What is OpenSearch and Why You Should Use It]] — the sibling explainer

## People
- [[Leo Schuster]]

## Source
- https://bonsai.io/blog/what-is-elasticsearch-and-why-you-should-use-it/
