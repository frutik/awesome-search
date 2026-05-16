---
type: topic
aliases: ["synonyms in search", "vocabulary management", "search vocabulary"]
tags: [topic, synonyms, query-understanding, vocabulary]
related_concepts: ["[[Synonyms]]", "[[Spelling Correction]]", "[[Query Understanding]]", "[[Zero Results]]", "[[BM25]]", "[[Dense Vector Retrieval]]"]
related_topics: ["[[E-commerce Search]]", "[[Query Understanding in Practice]]", "[[Search Quality Assurance]]"]
articles: [
  "[[Real Talk About Synonyms and Search]]",
  "[[Three Pillars of Search Quality - Findability]]",
  "[[Semantic Search Without Embeddings]]"
]
people: ["[[Daniel Tunkelang]]", "[[Andreas Wagner]]", "[[Doug Turnbull]]"]
created: 2026-05-16
---

# Synonyms and Vocabulary Management

How to bridge the vocabulary gap between how users describe things and how documents/products are indexed. Synonyms, spelling correction, and dense retrieval are complementary tools — not alternatives.

---

## The Vocabulary Gap Problem

Users search in their vocabulary. Documents are indexed in the author's vocabulary. These rarely match perfectly.

Common gap types:
- **Lexical**: "sofa" vs "couch", "laptop" vs "notebook"
- **Domain**: "cottagecore" (platform-specific) vs what a standard dictionary expects
- **Abbreviation**: "HDMI" vs "High-Definition Multimedia Interface"
- **Multilingual**: "kitty" (English) vs "chat" (French) in a multilingual catalog
- **Typo**: "runninh shoes" vs "running shoes"

The zero-results rate is your primary signal that vocabulary gaps exist.

---

## The Synonym Toolbox

### 1. Explicit Synonyms (Synonym Dictionaries)
Handcrafted pairs managed in your search engine's synonym config (Elasticsearch/Solr `synonyms.txt`).

**Two directionality types**:
- **Bidirectional**: `sofa <=> couch` — searches for either term find both
- **One-way (expansion)**: `laptop => laptop, notebook` — "laptop" finds notebook listings, but "notebook" doesn't find laptop listings

**Getting directionality wrong is the most common synonym mistake**. "Laptop" → "MacBook Pro" should be one-way (laptop is broader than MacBook Pro). Making it bidirectional means searching for "MacBook Pro" returns generic laptops.

### 2. Spelling Correction
Handle user typos before retrieval fails. Two stages:
- **Error detection**: is this query a likely typo?
- **Correction generation**: what was the user trying to type?

Domain-specific spell correction matters: "cottagecore" should NOT be corrected even though it's absent from general dictionaries. Train on your query logs, not generic corpora.

See [[Spelling Correction]].

### 3. Query Expansion
Expand the query with related terms at query time, either:
- From a synonym dictionary (explicit, controlled)
- From a learned model (Query2Vec, query embeddings)
- From the document corpus (significant_terms co-occurrence)

### 4. Dense/Semantic Retrieval
Embeddings handle many synonym problems implicitly — semantically similar terms cluster in vector space. However:
- Rare domain terms may not be in training data
- Abbreviations and brand names often need explicit handling
- Dense vectors don't replace synonyms; they cover different failure cases

---

## When to Use What

| Problem | Best tool |
|---|---|
| Known synonym pairs ("sofa"/"couch") | Explicit synonyms — fast, interpretable, controllable |
| Domain jargon the model doesn't know | Explicit synonyms + synonym dictionary from query logs |
| Typos and misspellings | Spelling correction |
| Vocabulary mismatch for common concepts | Dense retrieval |
| Rare/novel queries | Query expansion from corpus |
| Mixed language queries | Multilingual embeddings |

---

## Maintaining Synonym Dictionaries

Synonym dictionaries rot. Common sources of decay:
- Product discontinuation ("iPhone 5" synonyms no longer useful)
- Seasonal trends
- Brand name changes
- New platform-specific vocabulary

**Maintenance process**:
1. Monitor zero-results rate — rising rate signals new vocabulary gaps
2. Audit using click data: if a synonym expansion leads to zero clicks on expanded results, the synonym is wrong
3. Use query logs to discover new term pairs (terms that appear in the same query session frequently)
4. Re-review synonym list quarterly

---

## Common Mistakes

**Adding too many synonyms too fast.** Each synonym reduces precision. "Add all synonyms" is a precision disaster. Add sparingly, monitor click data for each addition.

**Symmetric synonyms for asymmetric relationships.** "TV" ↔ "television" is symmetric. "TV" ↔ "Samsung QLED 65 4K" is not — one is specific, one is broad.

**Correcting valid platform-specific terms.** Spell correction must be trained on your domain, not generic text.

**Expecting dense retrieval to replace all synonyms.** Dense models fail on abbreviations, brand names, product codes, and terms not in their training data.

---

## Related

- [[Zero Results]] — the main signal that vocabulary management is needed
- [[Spelling Correction]] — handles the typo case
- [[Dense Vector Retrieval]] — handles the semantic gap case
- [[E-commerce Search]] — vocabulary management is especially critical in product search
- [[Query Understanding in Practice]] — synonyms are one component of the QU pipeline
