---
title: Apache Solr
type: tool
aliases: ["Solr", "Apache Solr"]
tags:
  - tool
  - search-engine
  - open-source
  - lucene
website: https://solr.apache.org
repo: https://github.com/apache/solr
created: 2026-07-01
---

# Apache Solr

Mature open-source enterprise search platform built on [[Elasticsearch|Apache Lucene]]. Solr predates Elasticsearch and remains widely deployed; alongside Elasticsearch, [[OpenSearch]], and [[Vespa]] it is one of the reference engines for engine-selection discussions in this vault.

- Website: https://solr.apache.org
- GitHub: https://github.com/apache/solr

---

## Core Model

- **Core** — a single physical index with its own configuration (analogous to a [[Vespa]] *application*, though a Vespa app can hold multiple indexes).
- **`managed-schema`** — field and field-type definitions (`indexed`, `stored`, `docValues`, analyzers).
- **`solrconfig.xml`** — request handlers, caching, update processors.
- **Update endpoint** — document ingestion; **query endpoint** — Lucene/eDisMax queries.

## Notable Features

- **BM25 relevance** via Lucene (see [[BM25]]).
- **More Like This (MLT)** — similarity search from a seed document; the classic lexical analog of dense-vector "more like this" (`nearestNeighbor` in Vespa; kNN in OpenSearch).
- **Function queries** — score manipulation via functions/UDF-like expressions.
- **Faceting** — mature faceted-search support (see [[Faceted Search]]).
- **Late-interaction reranking** — recent ColBERT-on-Solr work; see [[ColBERT Comes to Apache Solr]].

## Position in the Ecosystem

Solr and Elasticsearch share the Lucene foundation and overlap heavily in capability; Solr is often favored for its configurability and community governance (Apache). It is a common **source** system in platform migrations to OpenSearch or Vespa — see [[Migration between Search Engines]].

## Related Tools

- [[Elasticsearch]] — the other major Lucene-based engine
- [[OpenSearch]] — Elasticsearch fork; a common Solr migration target (AWS Migration Assistant supports Solr live-traffic capture/replay)
- [[Vespa]] — ML-native alternative; see the Solr→Vespa mapping in [[How I learned Vespa by thinking in Solr]]

## Related Concepts

[[BM25]] · [[Full-Text Search]] · [[Faceted Search]] · [[Late Interaction]] · [[ColBERT]] · [[Search Platforms]]

## Articles

- [[ColBERT Comes to Apache Solr]] — late-interaction reranking on Solr
- [[How I learned Vespa by thinking in Solr]] — Solr operations mapped onto Vespa
- [[Amazon OpenSearch Service now offers AI-assisted migrations]] — Solr as a migration source with live-traffic capture/replay
