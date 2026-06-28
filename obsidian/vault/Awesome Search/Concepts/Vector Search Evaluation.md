---
title: "Vector Search Evaluation"
aliases: ["evaluating vector search", "semantic search evaluation", "evaluating semantic retrieval", "image search evaluation"]
tags:
  - concept
  - search-evaluation
  - vector-search
---

# Vector Search Evaluation

## Definition

Vector search evaluation is the practice of measuring the relevance quality of [[Dense Vector Retrieval]] (semantic, multimodal, hybrid) using the same IR machinery as lexical search — [[Judgment Lists]] and metrics like [[NDCG]], [[MRR]], and [[Precision and Recall]] — but adapted to queries that are *embeddings* rather than text.

The core practice is unchanged from lexical [[Search Evaluation]]: sample queries, retrieve candidates, collect relevance grades (human or [[LLM as Judge]]), compute a metric, and iterate. What changes is the plumbing.

## Why It's Harder Than Lexical Evaluation

Tools built for keyword search (notably [[Quepid]]) assume the query is human-readable text. Vector search breaks several of those assumptions:

| Challenge | Why it bites | Practical workaround |
|---|---|---|
| **Queries aren't human-readable** | A raw embedding (`[0.013, -0.21, ...]`) tells a human rater nothing about intent | Carry a human-readable label *alongside* the vector for the rating UI |
| **Query length limits** | A 3072-dim vector blows past input caps (e.g. Quepid's 2048-char query field) | Reduce dimensions ([[Matryoshka Embeddings]] truncation, e.g. 3072 → 94); or inject vectors via a case file / API instead of typing them |
| **JSON validity vs. valid query** | A raw array breaks the tool's JSON template validation, but quoting it produces a malformed engine query | Inject the vector via a query-option placeholder (e.g. `"vector": "#$qOption.clip##"`) |
| **Non-text results** | Rating image results means seeing the image, not a doc title | Render thumbnails in the scorer/UI; map engine payload → display fields |
| **Cross-modal queries** | Text-→-image or image-→-image search has no textual query at all | Use a [[Multimodal Embeddings]] model (e.g. CLIP) for both sides; evaluate image-to-image as a separate case |

## What Stays the Same

- Standard IR metrics (NDCG@10, etc.) still apply once relevance grades exist.
- [[Judgment Lists]] are still the foundation — built by humans or an [[LLM as Judge]].
- The workflow is still: baseline → hypothesis → experiment → re-measure.
- Public datasets like the [[Amazon ESCI Dataset]] / [[ESCI-S Dataset]] still seed query and product sets.

## Modes of Vector Evaluation

- **Text → text (semantic)**: query embedding vs. document embeddings.
- **Text → image (cross-modal)**: CLIP-style text encoder retrieves image vectors.
- **Image → image**: a product image is the query; useful for visual similarity.
- **Hybrid**: lexical + dense fused ([[Hybrid Search]]); vectors used for re-ranking.

## Related Concepts
- [[Search Evaluation]] — parent practice
- [[Judgment Lists]] — relevance grades the metrics consume
- [[NDCG]] — primary metric
- [[Dense Vector Retrieval]] — what's being evaluated
- [[Multimodal Embeddings]] — cross-modal and image search
- [[Matryoshka Embeddings]] — dimension reduction to fit tooling limits
- [[Hybrid Search]] — lexical + dense combination
- [[LLM as Judge]] — automated grading at scale

## Tools
- [[Quepid]] — judgment management and metric scoring; needs hacks for vector/image cases
- [[Qdrant Vector DB]] · [[Elasticsearch]] — backends evaluated in the linked articles

## Articles
- [[Why Setting Up Quepid for Vector Search Evaluation Went Wrong]]
- [[Oops, I Did It Again]]
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]]
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 2]]

## People
- [[Andrew Kornilov]] — hands-on series adapting Quepid to vector and image search
