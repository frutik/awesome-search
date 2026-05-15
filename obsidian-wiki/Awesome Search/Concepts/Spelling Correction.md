---
title: "Spelling Correction"
aliases: ["spell check", "spell correction", "did you mean", "typo correction", "fuzzy matching"]
tags:
  - concept
  - query-understanding
  - nlp
  - search
---

# Spelling Correction

## Definition

Spelling correction in search identifies and corrects typographic errors and misspellings in user queries before retrieval — replacing "iphne" with "iphone", or "maneger" with "manager". It is a foundational component of [[Query Understanding]].

## Why Spelling Matters in Search

Up to 15% of all search queries contain spelling errors. Without correction:
- "iphne" → zero results (exact BM25 match fails)
- User abandons → session failure
- Revenue impact in e-commerce

## Error Types

| Type | Example | Correction Strategy |
|------|---------|-------------------|
| Typographic | "iphne" (dropped letter) | Edit distance |
| Phonetic | "fone" for "phone" | Soundex/Metaphone |
| Cognitive | "definately" for "definitely" | Statistical LM |
| Context error | "I ate desert" (should be "dessert") | Context-aware LM |

## Classic Algorithm: Norvig's Spell Corrector

Peter Norvig's classic algorithm (2007):
1. Generate all edits within distance 1 and 2 of the input word
2. Filter edits that appear in the language model vocabulary
3. Rank by n-gram language model probability

```python
def candidates(word):
    return (known([word]) or known(edits1(word)) or 
            known(edits2(word)) or [word])

def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
    deletes = [L + R[1:] for L,R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L,R in splits if len(R)>1]
    replaces = [L + c + R[1:] for L,R in splits if R for c in letters]
    inserts = [L + c + R for L,R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
```

## SymSpell

Wolf Garbe's SymSpell: 1000x faster spelling correction:
- Pre-computes a dictionary of all words within edit distance 1 and 2
- At query time: lookup (not generate) → O(1) per edit distance level
- Works for both single-word and phrase corrections

## Context-Aware Correction

Standard spell correction is word-by-word. Context-aware correction considers surrounding words:
- "I went to the beech" → "beech" could be "beach" or tree
- Context ("went to the") disambiguates toward "beach"

Implemented with n-gram language models or transformer-based models (BERT).

## Deep Learning Approaches

Modern approaches use neural models:
- **Chars2vec**: character-level embeddings robust to spelling errors
- **BERT-based**: pre-trained LM scores candidate corrections in context
- **JamSpell**: context-aware correction using 3-gram LM + SymSpell

## Search-Specific Considerations

Search spelling correction differs from general spell correction:
1. **Query log augmentation**: "iphne" → "iphone" can be learned from query logs without a dictionary
2. **Brand names**: proper nouns, product names, model numbers require product catalog
3. **Don't always correct**: "python" vs "phyton" — user may mean the snake on a reptile site
4. **"Did you mean" vs. automatic**: show suggestion vs. silently correct (UX tradeoff)

## Etsy Case Study

Etsy's spelling correction uses:
- Multiple candidate generators (edit distance, phonetic, query log)
- Language model ranker (domain-specific, trained on Etsy query logs)
- Real-time A/B testing to validate correction quality

## Related Concepts

- [[Query Understanding]] — spelling correction is Part 1 (formulation analysis)
- [[Query Segmentation]] — co-occurs with spelling correction in the preprocessing pipeline
- [[Autocomplete]] — suggests correct queries before user finishes typing
- [[Zero Results]] — spelling errors are the #1 cause of zero results
- [[BM25]] — fails completely on misspelled queries

## People

- [[Daniel Tunkelang]] — "Spelling Correction" at queryunderstanding.com
