---
title: "Spelling Correction"
source: "https://queryunderstanding.com/spelling-correction-471f71b19880"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems detect and correct spelling errors in queries to improve recall — part of the Query Understanding series."
tags:
  - clippings
---

# Spelling Correction

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Spelling correction is one of the highest-impact query understanding tasks. Misspelled queries return poor or zero results; effective correction dramatically improves recall and user satisfaction.

## Key Concepts

**Types of spelling errors**
- Typographic errors (transpositions, substitutions, insertions, deletions)
- Phonetic errors (sounds right but spelled wrong: "nife" → "knife")
- Cognitive errors (confusion between similar words)
- Domain-specific errors (brand misspellings, technical terms)

**Correction approaches**
- Edit distance (Levenshtein, Damerau-Levenshtein)
- Noisy channel model (Peter Norvig's classic approach)
- N-gram language model re-ranking
- Neural models (sequence-to-sequence)
- SymSpell for fast candidate generation

**Context-aware correction**
- Single-word vs. context-aware (surrounding words matter)
- "I saw the dessert" vs. "I crossed the desert" — same sound, different spelling needed

**Search-specific considerations**
- Query frequency as prior (popular queries are probably correct)
- Index-based correction (suggest based on what's indexed)
- "Did you mean?" vs. silent auto-correction
- Correction of product names and brand terms

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Spelling Correction]]
- [[Query Understanding]]
- [[Zero Results]]

## People

- [[Daniel Tunkelang]]
