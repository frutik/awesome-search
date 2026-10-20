---
type: tool
title: "opensearch-muvera-plugin"
aliases: ["OpenSearch MUVERA plugin", "muvera ingest processor"]
website: "https://github.com/aws-samples/AI-search-with-amazon-opensearch-service/tree/muvera-late-interaction/muvera-late-interaction"
repo: "https://github.com/aws-samples/AI-search-with-amazon-opensearch-service/tree/muvera-late-interaction/muvera-late-interaction"
maintainer: "[[Amazon Web Services]]"
tags: [tool, opensearch, plugin, multi-vector, muvera, late-interaction]
created: 2026-10-20
---

# opensearch-muvera-plugin

An Apache-2.0 Java plugin for self-managed [[OpenSearch]], published in the `aws-samples/AI-search-with-amazon-opensearch-service` repo, that computes [[MUVERA]] fixed dimensional encodings server-side.

- Repo: https://github.com/aws-samples/AI-search-with-amazon-opensearch-service/tree/muvera-late-interaction/muvera-late-interaction

---

## What It Adds

- **`muvera` ingest processor** — encodes a document's multi-vectors into one FDE stored in a `knn_vector` field.
- **`muvera_query` search processor** — encodes the query the same way.

The FDE drives first-stage ANN; candidates are then reranked with exact MaxSim via k-NN's `lateInteractionScore`. The prebuilt zip targets OpenSearch **3.8.0** only (OpenSearch requires an exact version match); other versions need a source build with JDK 21. On managed Amazon OpenSearch Service, where custom plugins can't be installed, the same encodings come from [[FastEmbed]] on the client instead.

Benchmarks with ColBERTv2 and ColModernVBERT are in [[Scaling Late Interaction Retrieval in OpenSearch with MUVERA]].

## Related Concepts
- [[MUVERA]] · [[Late Interaction]] · [[ColBERT]] · [[ColPali]] · [[Reranking]]

## Related Topics
- [[Late Interaction in OpenSearch]]

## Related Articles
- [[Scaling Late Interaction Retrieval in OpenSearch with MUVERA]]
