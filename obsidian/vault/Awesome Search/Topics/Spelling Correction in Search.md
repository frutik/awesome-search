---
type: topic
related_concepts:
  - "[[Edit Distance]]"
  - "[[Noisy Channel Model]]"
  - "[[Language Models]]"
related_topics:
  - "[[Query Understanding in Practice]]"
  - "[[Autocomplete and Autosuggest]]"
  - "[[Synonyms and Vocabulary Management]]"
articles:
  - "[[1000x Faster Spelling Correction Algorithm - SymSpell]]"
  - "[[How to Write a Spelling Corrector]]"
  - "[[Modeling Spelling Correction for Search at Etsy]]"
  - "[[Query Understanding - Spelling Correction]]"
  - "[[Mirror Mirror - All About Search Suggestions]]"
companies:
  - "[[Etsy]]"
people:
  - "[[Wolf Garbe]]"
---

# Spelling Correction in Search

Spelling correction transforms a mistyped query into the user's intended query before retrieval. In search, it is one of the highest-ROI query understanding steps: fixing a single common typo can recover thousands of zero-result sessions.

## Why It Matters

- Typos are common: mobile keyboards, fast typing, and domain-specific terminology all produce errors.
- Zero results from a misspelling feel like a broken product, even when the inventory exists.
- Correction must be fast (sub-millisecond at scale) and precise (wrong corrections are worse than no correction).

## Core Algorithms

### Edit Distance

The foundation of most spelling correctors. Measures how many single-character operations separate two strings:

- **Levenshtein distance**: insertions, deletions, substitutions.
- **Damerau-Levenshtein distance**: adds transpositions (the most common human typo: "teh" → "the").
- Naïve computation is O(n·m); becomes expensive when scanning a large dictionary.

### Noisy Channel Model (Peter Norvig)

Treats spelling correction as a Bayesian problem:

```
P(intended | typed) ∝ P(typed | intended) × P(intended)
```

- **P(typed | intended)**: error model — how likely is this typo given the correct word? Derived from confusion matrices of common mistakes.
- **P(intended)**: language model — how common is this word in the corpus?
- Norvig's classic Python implementation generates all words within edit distance 1 or 2, then ranks by corpus frequency. Simple, surprisingly effective.

### SymSpell (Wolf Garbe)

Achieves ~1000× speedup over naïve edit distance search by pre-generating **delete-only variants** of every dictionary word at index time.

- At query time, generate deletes of the input and look them up in the pre-built index.
- Symmetric: a match means one word needs inserts and the other needs deletes to reach a common form.
- Supports edit distance 1 and 2 efficiently.
- Works well for real-time autocorrect and autosuggest; open-source and widely adopted.

### Levenshtein Automata

Construct a finite automaton that accepts all strings within distance k of a query term. Used in:

- **Lucene/Elasticsearch FuzzyQuery**: builds automata at query time to scan the term dictionary.
- More efficient than generating all candidate strings explicitly when the dictionary is large.

## Domain-Specific Spelling Correction

Generic dictionaries fail for e-commerce and vertical search:

- Product names, brand names, and model numbers are not in standard dictionaries ("Levi's", "Patagonia", "iPhone 15 Pro").
- Correct spelling in one domain may be wrong in another ("Mac" vs "mac").

**Etsy's approach** (Modeling Spelling Correction for Search at Etsy):
- Train a correction model on query logs: if users reformulate a query with different spelling and click the same items, the two spellings are likely variants of the same intent.
- Use session signals: if a user types "vintige" and immediately retypes "vintage", that's a training pair.
- Candidate generation from domain vocabulary + edit distance; ranking with a learned model.

## Phonetic Matching

Catch errors that sound the same but are spelled differently:
- **Soundex**, **Metaphone**, **Double Metaphone**: encode words into phonetic keys; match on key equality.
- Useful for names and brand terms where users write phonetically ("nike" → "niké" is trivial; "frazier" → "Frasier" is phonetic).
- Typically used as a fallback or a feature in candidate ranking, not as the primary corrector.

## Neural and Contextual Approaches

- **Character-level sequence-to-sequence models**: learn to transduce mistyped strings to correct strings.
- **BERT-based correctors**: exploit surrounding query context — "redd shooes" is more likely "red shoes" than "reed shoes" because of "shooes".
- Context is especially valuable for **real-word errors** (valid words that are the wrong word: "from" vs "form").
- Trade-off: neural models are slower and harder to control; rule-based and dictionary methods are more predictable.

## When to Apply Correction

| Signal | Action |
|---|---|
| Query returns zero results | Trigger correction, show "Did you mean…?" |
| Query returns very few results | Optionally offer correction |
| High edit-distance candidate, low confidence | Show original results + suggestion, don't auto-correct |
| Short queries (1-2 chars) | Avoid correction — too much ambiguity |
| Brand/product name from catalog | Suppress correction if exact match exists in index |

**Auto-correct vs. suggest**: auto-correcting silently can frustrate users who typed correctly (e.g., a niche brand). "Did you mean?" lets the user decide.

## Integration with Query Understanding

Spelling correction sits early in the query understanding pipeline:

```
Raw query
  → Spelling correction
  → Tokenization / normalization
  → Intent classification
  → Query expansion / synonyms
  → Retrieval
```

Correct before expanding: applying synonyms to a misspelled query compounds the problem.

## Evaluation

- **Precision**: fraction of corrected queries that were correctly corrected (wrong correction = harmful).
- **Recall**: fraction of misspelled queries that were corrected.
- **Zero-result rate**: before/after correction, measures business impact directly.
- **Click-through rate on corrected queries**: proxy for user acceptance of suggestions.
- Test on a held-out set of (misspelling, intended) pairs derived from query reformulation logs.

## Key Takeaways

1. Damerau-Levenshtein is the right edit distance baseline (transpositions are the most common error type).
2. SymSpell is the fastest practical algorithm for dictionary lookup within edit distance 1–2.
3. Domain vocabulary (catalog terms, brand names) must augment the correction dictionary.
4. Use query logs as training signal — they encode real user correction behavior.
5. When confidence is low, suggest rather than silently auto-correct.
