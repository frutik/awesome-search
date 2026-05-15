---
title: "Stemming and Lemmatization"
source: "https://queryunderstanding.com/stemming-and-lemmatization-6c086742fe45"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How stemming and lemmatization normalize query and document terms to improve recall by matching morphological variants — part of the Query Understanding series."
tags:
  - clippings
---

# Stemming and Lemmatization

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Stemming and lemmatization reduce word variants to a common base form, enabling queries to match documents that use different morphological forms of the same word.

## Stemming

**What it does**: Removes word endings using heuristic rules, without regard to meaning.

- "running" → "run", "dogs" → "dog", "happily" → "happili"
- Fast and language-agnostic
- Can produce non-words ("happili")

**Common algorithms**
- Porter Stemmer (English, widely used)
- Snowball/Porter2 (improved)
- Lancaster (aggressive)

**Tradeoff**: High recall improvement, but risks over-stemming (conflating unrelated words: "universe" and "university" → "univers").

## Lemmatization

**What it does**: Reduces words to their dictionary base form (lemma) using morphological analysis.

- "running" → "run", "better" → "good", "mice" → "mouse"
- Produces real words
- Requires part-of-speech information for accuracy

**Tradeoffs**
- More accurate than stemming
- Slower (requires NLP pipeline)
- Requires language-specific models

## Search Implications

- Applied symmetrically to queries AND index (both stemmed/lemmatized)
- E-commerce: stemming helps ("shoes" matches "shoe") but risks ("dress" matching "dresses" AND "dressed")
- Domain-specific lemmatizers outperform general ones

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Spelling Correction]]
- [[BM25]]

## People

- [[Daniel Tunkelang]]
