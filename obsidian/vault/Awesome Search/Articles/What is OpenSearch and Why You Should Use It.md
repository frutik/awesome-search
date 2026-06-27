---
type: article
title: "What is OpenSearch and Why You Should Use It"
source: "https://bonsai.io/blog/what-is-opensearch-and-why-you-should-use-it/"
author: "[[Leo Schuster]]"
company: "[[Bonsai]]"
published: 2023-04-11
tags: [article, company-blog, opensearch, elasticsearch, licensing, introduction]
concepts: ["[[Full-Text Search]]", "[[Search Architecture]]"]
topics: ["[[Search Platforms]]", "[[Elasticsearch vs OpenSearch]]"]
created: 2026-06-27
---

# What is OpenSearch and Why You Should Use It

An introductory [[Bonsai]] explainer by [[Leo Schuster]] on [[OpenSearch]] — what it is, why it exists, and when to choose it. Companion to [[What is Elasticsearch and Why You Should Use It]].

---

## What It Is

"A community-driven, open-source search and analytics suite derived from Apache 2.0-licensed **Elasticsearch 7.10.2 & Kibana 7.10.2**." Comprises the search engine daemon plus **OpenSearch Dashboards** (a Kibana fork) to ingest, secure, search, aggregate, and analyze data.

## Why It Exists — The Fork

OpenSearch was created in response to Elastic's 2021 license change, moving Elasticsearch/Kibana off **Apache 2.0** to the "highly-restrictive and anti-competition **SSPL**." The last open-source versions (7.10.2) were forked into **OpenSearch 1.0**, led by AWS. The framing is explicitly about **freedom and avoiding vendor lock-in**.

## Differentiating Features (plugins)

Anomaly detection · Performance Analyzer · SQL · Security · Alerting · ML Commons · **k-NN search** · cross-cluster replication — many bundled open-source where Elastic gated them behind commercial tiers.

## Compatibility

Backward-compatible with Elasticsearch 7.10.2 APIs — AWS stated the APIs would be "backwards compatible... to eliminate any need for customers to update their current client code."

## When / Why to Use It

Real-time analytics, e-commerce/media search, social networks, log analytics — anywhere you want Elasticsearch-class capability under a permissive Apache 2.0 license. Adopters cited: AWS, Bonsai, SAP, CapitalOne, RedHat, Aiven, Logz.

## Related Concepts
- [[Full-Text Search]]
- [[Search Architecture]]

## Related Notes
- [[OpenSearch]] — the tool note
- [[Elasticsearch vs OpenSearch]] — the full comparison and licensing history
- [[What is Elasticsearch and Why You Should Use It]] — the sibling explainer

## People
- [[Leo Schuster]]

## Source
- https://bonsai.io/blog/what-is-opensearch-and-why-you-should-use-it/
