---
title: "Tokenization"
source: "https://queryunderstanding.com/tokenization-c8cdd6aef7ff"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems split queries into tokens (words, subwords, characters) as a foundation for all subsequent NLP processing — part of the Query Understanding series."
tags:
  - clippings
---

# Tokenization

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Tokenization splits raw query text into discrete units (tokens) for further processing. It appears simple but has significant impact on search quality, especially for technical terms, brand names, and non-English languages.

## Key Concepts

**Word tokenization**
- Whitespace splitting as a baseline
- Language-specific rules for compound words (German: "Donaudampfschifffahrtsgesellschaft")
- Hyphenation handling ("e-commerce" → ["e", "commerce"] or keep as one?)

**Subword tokenization**
- BPE (Byte Pair Encoding) — used by GPT, many NLP models
- WordPiece — used by BERT
- Handles rare/OOV words by splitting into known subwords

**Character-level tokenization**
- Character n-grams for fuzzy matching

**Domain-specific considerations**
- Product codes, SKUs (need to keep intact)
- Measurements ("5kg", "32GB")
- URLs and email addresses

**Search-specific issues**
- Query segmentation relates to tokenization (multiword tokens)
- Mismatch between query tokenization and index tokenization causes recall failures

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Query Segmentation]]
- [[Spelling Correction]]

## People

- [[Daniel Tunkelang]]
