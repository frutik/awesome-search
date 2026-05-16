---
title: "Keywords Extraction"
aliases: ["keywords extraction", "keyword extraction", "keyphrase extraction", "RAKE", "YAKE", "KeyBERT", "key phrase extraction", "automatic keyword extraction"]
tags:
  - concept
  - search
  - nlp
  - query-understanding
created: 2026-05-16
---

# Keywords Extraction

## Definition

Keywords extraction (or keyphrase extraction) automatically identifies the most important words or phrases from a document that capture its main topics. In search, it's used for query suggestion, document summarization, tag generation, and building [[Synonyms]] / [[Collocations]] resources.

## Use Cases in Search

- **Query suggestion**: extract keyphrases from popular documents to suggest related searches
- **Facet generation**: extract candidate facet values from product descriptions
- **Index enrichment**: add extracted keyphrases as additional searchable fields
- **Diversity Metrics**: extracted keyphrases enable [[Diversity Metrics]] based on topic coverage
- **Query expansion**: keyphrases from top results used in pseudo-relevance feedback ([[Query Expansion]])

## Main Algorithms

### RAKE (Rapid Automatic Keyword Extraction)
Splits text on [[Stopwords]] and punctuation, scores remaining word sequences by word frequency and co-occurrence. Extremely fast, no training required.
- Score: `degree(word) / frequency(word)` — rewards words that appear in many different phrases
- Best for: short texts, real-time extraction

### YAKE (Yet Another Keyword Extractor)
Statistical approach using five features per candidate: casing, position in text, frequency, relatedness to context, sentence spread. Unsupervised, language-agnostic.
- Better than RAKE on longer documents and multiple languages

### KeyBERT
Uses [[BERT]] embeddings to find keyphrases most semantically similar to the document embedding. Embeds all candidate n-grams, ranks by cosine similarity to the full document vector.
- Higher quality than statistical methods
- Can use [[Diversity Metrics]] (MMR) to extract diverse keyphrases rather than redundant variants of the same topic

### Graph-Based (TextRank / PositionRank)
Builds a word co-occurrence graph, runs PageRank-style scoring. Captures structural importance.
- TextRank: word nodes, co-occurrence edges, PageRank scores
- PositionRank: weights by word position (early words score higher)

## Supervised / Fine-tuned Approaches
Models trained on labeled keyphrase datasets (KP20k, SemEval) achieve the highest quality. Often sequence-labeling models (BERT + CRF) or generative models (T5-based).

## Related Concepts

- [[Query Expansion]] — extracted keyphrases feed pseudo-relevance feedback
- [[Collocations]] — keyphrases are often multi-word collocations
- [[Stopwords]] — stopword removal is a preprocessing step for RAKE/YAKE
- [[BERT]] — foundation for KeyBERT and neural extraction
- [[Diversity Metrics]] — MMR applied to keyphrase selection for diversity
- [[Query Understanding]] — keyphrases aid query intent classification
