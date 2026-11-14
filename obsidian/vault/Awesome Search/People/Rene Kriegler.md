---
type: person
title: "Rene Kriegler"
aliases: ["René Kriegler", "Kriegler"]
tags:
  - person
  - search-practitioner
  - e-commerce
  - query-rewriting
affiliation: independent consultant (frequently with OpenSource Connections)
role: Search & relevance consultant
created: 2026-07-05
---

# Rene Kriegler

Search and NLP relevance consultant with a long focus on **e-commerce** search, working mainly with Solr/Lucene. Maintainer of [[Querqy]], the open-source query rewriting library, and organizer of the [[MICES]] (Mix-Camp E-Commerce Search) conference in Berlin, held alongside [[Berlin Buzzwords]]. Has contracted with [[OpenSource Connections]] and previously worked with [[Charlie Hull]] at Flax (later merged into OSC).

## Known For

- **[[Querqy]]** — query rewriting library for Solr/Lucene/Elasticsearch/OpenSearch
- [[MICES]] e-commerce search conference (Berlin)
- Framing **[[Query Relaxation]] as a query recommendation** problem rather than query repair (see the talk below), and applying [[Word2Vec]] + a multi-layer neural network with word-shape features to predict which query term to drop.

## Videos

- [[Rene Kriegler - Query Relaxation]] — "Query relaxation - a rewriting technique between search and recommendations" (2019)

- [[Rene Kriegler & Jean Silva - Alternative Queries for Zero Results]] — [[Haystack EU]] 2023, with [[Jean Silva]] of [[Wallapop]]; revisits the 2019 models and finds that fixing a token-order bug lifts the MLP to 0.98, matched by a fine-tuned RoBERTa classifier

## Related Concepts

- [[Query Relaxation]]
- [[Zero Results]]
- [[Word2Vec]]

## Related Tools

- [[Querqy]]

## Related People

- [[Charlie Hull]] — colleague at Flax / OpenSource Connections
- [[Daniel Tunkelang]] — whose blog post on word embeddings for relaxation informed the approach
- [[Mihajlo Grbovic]] — query embeddings (query-as-word) referenced in the talk
