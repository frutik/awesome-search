---
title: "How to Write a Spelling Corrector"
tags:
  - clippings
  - search
  - spelling-correction
  - classic
source: "http://norvig.com/spell-correct.html"
author: "Peter Norvig"
created: 2026-05-15
concepts:
  - Spelling Correction
---

# How to Write a Spelling Corrector

**Source:** http://norvig.com/spell-correct.html
**Author:** Peter Norvig (Google)

## Summary

Classic ~21-line Python implementation of a probabilistic spelling corrector. The canonical reference for the noisy-channel model of spelling correction.

## Algorithm

Bayes' theorem to find the most probable correction:

```
argmax_c ∈ candidates P(c) * P(w|c)
```

Where:
- `P(c)` = language model (probability of the word in a corpus)
- `P(w|c)` = error model (probability of typing `w` when intending `c`)

## Key Components

### Candidate Generation
Generates candidates within edit distance 2 using four operations: deletion, transposition, replacement, insertion.

For a 9-character word: 442 candidates at edit distance 1, but after filtering to dictionary words → just a handful of valid corrections.

### Language Model
Word probabilities from ~1.1M word corpus (Project Gutenberg + frequency lists). Priority: known words at edit distance 1 > edit distance 2 > unknown words.

### Simplified Error Model
Prefers lower edit distance. Does not model keyboard proximity or phonetic similarity.

## Results

- Development set: **75% accuracy**
- Final test set: **68% accuracy**
- ~35-41 words/second

## Limitations

- No context awareness (surrounding words ignored)
- Unknown words (5-11% of test cases)
- Oversimplified error model (no keyboard layout, no phonetics)

## Historical Significance

This paper launched a thousand spelling corrector implementations. [[Wolf Garbe]] built [[Spelling Correction#SymSpell]] specifically to address its O(n) computational cost at scale.

## Related Concepts

- [[Spelling Correction]]
- [[Query Understanding]]

## Related Articles

- [[1000x Faster Spelling Correction Algorithm - SymSpell]]
- [[Modeling Spelling Correction for Search at Etsy]]
