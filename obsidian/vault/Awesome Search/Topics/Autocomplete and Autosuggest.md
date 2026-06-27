---
type: topic
aliases:
  - autocomplete
  - autosuggest
  - search suggestions
  - typeahead
tags:
  - topic
  - autocomplete
  - ux
  - query-understanding
related_concepts:
  - "[[Autocomplete]]"
  - "[[Query Understanding]]"
  - "[[Personalization]]"
  - "[[Learning to Rank]]"
  - "[[Zero Results]]"
related_topics:
  - "[[Query Understanding in Practice]]"
  - "[[E-commerce Search]]"
  - "[[Search Quality Assurance]]"
articles:
  - "[[Autosuggest Retrieval Data Structures and Algorithms]]"
  - "[[Autosuggest Ranking]]"
  - "[[Bootstrapping Autosuggest]]"
  - "[[LLM-Powered Query Extraction for Autocomplete]]"
  - "[[How to Really Do Autocomplete]]"
  - "[[How to Really Scale Autocomplete]]"
people:
  - "[[Giovanni Fernandez-Kincade]]"
  - "[[David Albrecht]]"
  - "[[Max Irwin]]"
created: 2026-05-16
---

# Autocomplete and Autosuggest

How to build search suggestions that help users express intent faster. Autocomplete (prefix completion) and autosuggest (semantic fallback) are two distinct problems with different architectures.

---

## Autocomplete vs. Autosuggest

| | Autocomplete | Autosuggest |
|---|---|---|
| Trigger | User typing a prefix | Query typed but intent unclear |
| Mechanism | Prefix index / FST lookup | Semantic similarity / embedding KNN |
| Goal | Complete the query the user is typing | Suggest alternative framings |
| Response time | <10ms | <50ms |

Both are often displayed in the same suggestion dropdown, but use different backends.

---

## Retrieval: How to Get Candidates Fast

### Edge N-gram Index
Pre-index all suggestion strings with edge n-grams at index time. Fast prefix lookup at query time, but large index size.

### Finite State Transducer (FST)
Compact automaton for prefix matching. Lucene uses FSTs internally for its suggest component. Orders of magnitude more memory-efficient than edge n-grams.

### Trie
Simple prefix tree. Good for small vocabularies; doesn't scale to millions of suggestions.

### Practical Choice
Use your search engine's native suggest feature (Elasticsearch's `search_as_you_type`, `completion` suggester) for most cases. Only build custom FST if you need custom ranking or multi-field matching.

---

### Generating the Suggestion Vocabulary
The structures above assume you already *have* suggestion strings — most tutorials skip where the vocabulary actually comes from. [[How to Really Do Autocomplete]] ([[Max Irwin]], [[Bonsai]]) generates it straight from document content in a single request:

- **Page suggestions** — copy title/description into a `completion` field with an **edge-ngram** tokenizer for fast prefix hits.
- **Word suggestions** — a prefix-filtered `significant_terms` aggregation surfaces terms that are statistically interesting in the matched subset vs. the whole corpus.
- **Phrase suggestions** — a **shingles** field yields multi-word suggestions ("opensearch platform").

This is the document-driven counterpart to the query-log and LLM vocabularies in **Cold Start** below.

## Ranking: Once You Have Candidates

### Baseline: Frequency-Based
Sort by historical query frequency. Fast, interpretable, but ignores context.

### Probabilistic Model
`P(C | prefix) ∝ P(prefix | C) × P(C)` — noisy channel framing. P(C) = frequency prior; P(prefix|C) = edit model. Used in spell-correction-aware autocomplete.

### LTR Feature Categories
**Temporal**: recency of last usage, trending signal (24h spike), seasonality

**Behavioral**: CTR of the completion if clicked, conversion rate, session abandonment rate

**Contextual**: user location, language/locale, session history (what has the user already searched?)

**Query**: length of prefix typed, specificity of the candidate

### Two-Phase for Latency
1. **Fast retrieval** (<10ms): FST/edge n-grams → top-100 candidates
2. **Ranking** (<30ms): LTR model to re-score and reorder

---

## Personalization

User-specific ranking:
- Boost completions the user has typed before (with recency decay)
- Boost completions in categories the user frequently shops
- Cold start: fall back to location-based defaults, demographic cohort, or pure frequency

---

## Cold Start: No Query History

New search products have no query logs to build suggestions from. Options:

1. **Seed from catalog**: extract noun phrases from product descriptions as initial suggestions
2. **LLM generation**: prompt an LLM to generate realistic search queries for each product/category. David Albrecht's approach: GPT-4.1-nano generated 10 queries per product for 43k items at <$5 cost. Produces novel phrases traditional NLP can't extract.
3. **Competitor/open data**: use open query datasets as bootstrapping signal (MS MARCO, Amazon ESCI)

LLM-generated queries solve cold-start while producing user-like phrases. Validate over time with click/conversion data.

---

## Scaling Autocomplete

The naive approach (significant_terms aggregation on shingles) collapses at millions of documents — CPU saturation and multi-second queries.

**What works at scale**:
- Separate autocomplete index (different scaling profile from main search)
- `search_as_you_type` field type in Elasticsearch + `match_phrase_prefix`
- `terms` aggregation (frequency-ordered) instead of `significant_phrases`
- Debounce 25-50ms before firing (saves 40-50% of requests)
- Views/popularity as primary ranking signal via `field_value_factor` + `log1p`

At 6M+ docs: achieves 416 req/s at p99 ≤ 45ms.

---

> Source: [[How to Really Scale Autocomplete]] ([[Max Irwin]], [[Bonsai]]) — the 6M-doc benchmark and the `significant_phrases` → `terms` swap above are from this Part 2 writeup. [[How to Really Do Autocomplete]] is Part 1 (vocabulary generation).

## Common Failure Modes

**Showing irrelevant completions**: frequency ranking without context → "apple" suggests "apple pie" to a developer

**Stale suggestions**: popular-last-year completions that nobody searches now — need recency decay and trending signal

**Overly long completions**: users want to type less, not see their full query echoed back

**Zero-results for accepted suggestion**: suggestion exists but accepted query returns no results — catastrophic UX failure

---

## Related

- [[Query Understanding in Practice]] — suggestions feed into QU pipeline
- [[Personalization in Search]] — user-specific ranking of completions
- [[E-commerce Search]] — autocomplete is especially high-ROI in product search
