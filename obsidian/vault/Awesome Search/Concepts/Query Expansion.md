---
title: "Query Expansion"
aliases: ["query expansion", "query augmentation", "query broadening", "automatic query expansion", "AQE", "pseudo-relevance feedback", "PRF"]
tags:
  - concept
  - search
  - query-understanding
  - nlp
created: 2026-05-16
---

# Query Expansion

## Definition

Query expansion adds terms to the original query to improve recall — bridging vocabulary mismatches between what users type and how documents are written. A user searching "car" should also match documents about "automobile" and "vehicle."

## Why It's Needed

Search systems suffer from the **vocabulary mismatch problem**: users and authors use different words for the same concept. Without expansion:
- "MI" doesn't match "myocardial infarction"
- "sneakers" doesn't match "trainers" (UK English)
- "broke" doesn't match "no money"

Semantic search ([[Dense Embeddings]]) partially solves this, but [[BM25]] and exact-match scenarios still depend on expansion.

## Types of Query Expansion

### Synonym-Based
Map query terms to synonyms using a curated [[Synonyms]] dictionary or ontology. High precision, requires maintenance.

### Thesaurus / Ontology-Based
Use [[Knowledge Graph Search]] or domain ontologies to find related terms, parent/child concepts, and associated entities.

### Pseudo-Relevance Feedback (PRF)
1. Run the original query
2. Assume top-k results are relevant
3. Extract key terms from those results
4. Add those terms back to the query and re-run

Fast and unsupervised, but risky — if top-k results are wrong, expansion degrades quality ("query drift").

### LLM-Based Expansion
Use an LLM to generate related terms, rephrasings, or hypothetical relevant passages ([[HyDE]]). Examples:
- "Generate 5 synonyms for: {query}"
- "What terms would appear in a document answering: {query}?"

### Embedding-Based Expansion
Find nearest neighbor terms/queries in embedding space and add them to the lexical query — bridges semantic and lexical retrieval.

## Query Expansion vs. Query Relaxation

| | Query Expansion | [[Query Relaxation]] |
|---|---|---|
| Goal | Improve recall | Rescue zero-result queries |
| Timing | Always applied (proactive) | Applied when results are too few (reactive) |
| Direction | Broader vocabulary | Fewer/looser constraints |

## Risks

- **Over-expansion**: adding irrelevant terms hurts precision
- **Topic drift**: PRF-based expansion can pull queries off-topic
- **Latency**: re-running expanded queries adds processing time

## Related Concepts

- [[Synonyms]] — curated synonym dictionaries are the most common expansion source
- [[Query Understanding]] — expansion is one step in the QU pipeline
- [[Query Relaxation]] — reactive broadening when results are too few
- [[BM25]] — primary beneficiary of expansion (semantic search handles vocab mismatch differently)
- [[Zero Results]] — expansion is a key mitigation for zero-result queries
- [[Hypothetical Document Embeddings]] — LLM-based expansion via HyDE
- [[Spelling Correction]] — related query normalization step
