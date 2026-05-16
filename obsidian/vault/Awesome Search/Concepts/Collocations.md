---
title: "Collocations"
aliases: ["collocations", "common phrases", "phrase detection", "multi-word expressions", "MWE", "bigrams", "n-grams", "shingles", "phrase queries"]
tags:
  - concept
  - search
  - nlp
  - query-understanding
created: 2026-05-16
---

# Collocations

## Definition

Collocations are word combinations that appear together more frequently than chance and function as a semantic unit: "machine learning", "credit card", "New York", "hot dog". Treating them as single tokens rather than independent words improves both indexing and retrieval accuracy.

## Why They Matter for Search

Without phrase awareness:
- "New York" is tokenized as ["New", "York"] — "New" matches unrelated documents
- "hot dog" could match pages about warm canines
- Query "machine learning jobs" could match documents mentioning machines and learning separately

Collocations are especially important for:
- **Named entities**: "San Francisco", "Apple Inc."
- **Technical terms**: "support vector machine", "random forest"
- **Product names**: compound product names that lose meaning when split

## Detection Methods

### Statistical Measures
Identify word pairs (bigrams) that co-occur significantly more than expected:
- **PMI (Pointwise Mutual Information)**: `log P(w1,w2) / (P(w1) × P(w2))` — high PMI = strong collocation
- **Chi-squared test**: statistical significance of co-occurrence
- **Log-likelihood ratio**: robust to low-frequency pairs

### Frequency Thresholds
Simple but effective: bigrams appearing > N times in corpus are candidates. Often combined with stop-word filtering to exclude function word pairs.

### Dependency Parsing
NLP approach — extract noun phrases and named entities from a corpus using a parser. Higher quality, higher compute.

## Collocations in Search Systems

### Indexing
- Detect phrases in documents at index time and add phrase tokens alongside word tokens
- Shingling: index overlapping n-grams for approximate phrase matching

### Query Processing
- Detect phrases in user queries and treat them as units in [[Query Understanding]]
- Phrase queries in Elasticsearch: `{"match_phrase": {"text": "machine learning"}}` requires words adjacent and in order

### Synonym Integration
Collocations must be handled carefully in [[Synonyms]] expansion — "hot dog" → "frankfurter" is valid, but splitting and expanding "hot" and "dog" separately produces garbage.

### Relation to Stopwords
[[Stopwords]] inside collocations should *not* be removed — "right to repair", "to be or not to be" lose meaning without function words.

## Related Concepts

- [[Query Understanding]] — phrase detection is a preprocessing step
- [[BM25]] — phrase handling in lexical retrieval
- [[Synonyms]] — collocations need special handling in synonym expansion
- [[Stopwords]] — stopwords inside phrases must be preserved
- [[Query Segmentation]] — related task of segmenting queries into meaningful units
- [[Keywords Extraction]] — related task of identifying important phrases in documents
