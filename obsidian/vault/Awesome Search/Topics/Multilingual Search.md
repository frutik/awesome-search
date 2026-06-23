---
type: topic
tags: [topic, multilingual, cross-lingual, embeddings, nlp]
related_concepts: [Embeddings, BM25, Query Understanding]
related_topics: [Query Understanding in Practice, Synonyms and Vocabulary Management, E-commerce Search]
articles: []
companies: [Carousell, Elastic]
people: []
---

# Multilingual Search

Serving search across multiple languages — or mixed-language queries — requires solutions at every layer of the stack: tokenization, retrieval, ranking, and evaluation. A system that works well in English will degrade sharply when queries and documents don't share the same language.

---

## Why Multilingual Search Is Hard

| Challenge | Root Cause |
|-----------|-----------|
| Vocabulary mismatch | Query in Language A, document in Language B — BM25 scores zero |
| Script diversity | Latin, CJK, Arabic, Devanagari need different tokenizers |
| Mixed-language queries | "iPhone 13 price RM" mixes English brand + Malay currency |
| Low-resource languages | Sparse training data; embeddings may not generalize |
| Transliteration | Same word spelled multiple ways across scripts |
| Evaluation gap | Judgment collection is expensive in each language |

---

## Retrieval Approaches

### 1. Machine Translation (MT) Pipeline
Translate queries into a single canonical language (usually English), then search a monolingual index.

**Pros**: Reuses existing monolingual infrastructure.  
**Cons**: Translation latency; errors compound; loses rare-word precision.

### 2. Per-Language Indexes + [[Federated Search]]
Maintain separate indexes per language, fan out the query, merge results.

**Pros**: Each index is optimized for its language.  
**Cons**: Infrastructure cost; merging scores across heterogeneous indexes is non-trivial.

### 3. Multilingual Dense Retrieval
Encode queries and documents with a shared multilingual encoder (e.g., mBERT, XLM-R, E5-multilingual, Qwen3 multilingual). Queries and documents from any language land in the same vector space.

**Pros**: Single index; cross-lingual retrieval without translation; handles mixed-language queries naturally.  
**Cons**: Embedding quality varies by language; requires GPU infrastructure; ANN index size grows with document count.

**Key models (2024–2025)**:
- `intfloat/multilingual-e5-large` — strong general-purpose, 100+ languages
- `Alibaba-NLP/gte-Qwen2-1.5B-instruct` / Qwen3 multilingual — state-of-the-art on MTEB multilingual
- `cohere/multilingual-22-12` / `embed-multilingual-v3.0` — production-grade via API

### 4. Hybrid: BM25 + Multilingual Dense
Run BM25 per-language alongside a multilingual dense retriever; fuse with RRF or learned weights. Best of both worlds for high-recall + cross-lingual.

---

## Tokenization Matters

BM25 and sparse models depend heavily on tokenizers:
- **CJK (Chinese, Japanese, Korean)**: Character-level or n-gram tokenization; word boundaries are implicit.
- **Arabic/Hebrew**: Right-to-left; morphologically rich; stemming critical.
- **Agglutinative languages** (Finnish, Turkish, Hungarian): Compound splitting needed to avoid vocabulary explosion.

Elasticsearch / OpenSearch ship language-specific analyzers. For neural models, sentencepiece / BPE tokenizers handle scripts natively.

---

## Mixed-Language Queries

Common in multilingual markets (Southeast Asia, India, Switzerland, Belgium):

```
"iPhone 15 harga terbaik"        # English brand + Malay price query
"Nike running shoes 남성용"       # English brand + Korean "for men"
```

**Solutions**:
- Language detection per token (not just per query)
- Multilingual embeddings handle this naturally
- At ranking time, score documents in the query's dominant language higher

**Carousell** serves mixed-language queries across Southeast Asian markets (Bahasa Indonesia, Tagalog, Thai, English) with dense vector retrieval to bridge vocabulary gaps in sponsored search.

---

## Evaluation

Multilingual evaluation is expensive — you need annotators who speak each language.

**Practical strategies**:
- Use query logs + click data as a language-agnostic signal (CTR, reformulation rate)
- Stratified sampling by language in your query test set (see [[Query Sampling]])
- Automated MT + back-translation to generate cross-lingual test pairs cheaply
- MTEB multilingual benchmark for model selection offline

Watch for **language imbalance**: a model may score well on average while failing on low-resource languages that represent a real user population.

---

## Common Mistakes

- **English-first architecture**: Hard to retrofit multilingual later; build multilingual retrieval from day one if you serve non-English markets.
- **Ignoring transliteration**: "Москва" and "Moskva" are the same city — synonyms or normalization needed.
- **Single-language judgment pool**: Offline eval that only covers English hides quality gaps in other languages.
- **Token budget mismatch**: Cross-encoder rerankers have context limits that break down on long CJK documents if tokenized naively.

---

## Further Reading

- Elastic E5 multilingual embeddings documentation
- [[Carousell]] — multilingual dense retrieval for sponsored search
- [[Synonyms and Vocabulary Management]] — transliteration and cross-lingual synonym expansion
- [[Query Understanding in Practice]] — language detection as a preprocessing step
