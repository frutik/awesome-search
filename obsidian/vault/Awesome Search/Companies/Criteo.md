---
type: company
blog: https://medium.com/criteo-engineering
tags:
  - company
created: 2026-10-04
---

# Criteo

Criteo uses k-nearest-neighbour search for targeted ads, to pick the most relevant products to display. Its R&D team publishes on the Criteo R&D Blog on Medium: https://medium.com/criteo-engineering

The team spent weeks calibrating [[FAISS]] index choices across query speed, index size, recall and build time. It released the result as the open-source library [[autofaiss]].

In retail media, Criteo places Sponsored Products ads beside organic results in retailers' own search. Its proprietary [[CLEPR]] model acts there as a relevance guardrail, checking that candidate ads match the query before performance optimization ranks them. Criteo frames this work around two targets: [[Semantic Relevance|accuracy]] (does the product match the query?) and [[Outcome-Based Relevance|outcome-based relevance]] (do clicks and purchases confirm it?). The same split underlies its agentic commerce recommendation service for AI shopping assistants.

## Tools

- [[autofaiss]] — automatic FAISS index selection under memory and latency budgets
- [[CLEPR]] — proprietary two-tower query–product relevance model

## People

- [[Victor Paltz]] — author of the autofaiss launch post
- [[Romain Beaumont]] — co-author
- [[Maxime Vono]] — author of the outcome-based relevancy post
- [[Paul Coursaux]] — author of the CLEPR post

## Published Articles

- [[Introducing Autofaiss - An Automatic K-Nearest-Neighbor Indexing Library At Scale]]
- [[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]]
- [[Introducing CLEPR, our model for semantic understanding]]

## Related Concepts

- [[Approximate Nearest Neighbor Search]] · [[Vector Quantization]] · [[Dense Vector Retrieval]]
- [[Outcome-Based Relevance]] · [[Semantic Relevance]] · [[Bi-Encoder]]
