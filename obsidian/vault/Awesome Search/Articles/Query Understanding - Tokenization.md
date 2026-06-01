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

Tokenization splits raw query text into discrete units for further processing. While splitting on whitespace works as a baseline, real-world queries require more nuanced decisions: whether to keep hyphenated terms together or apart, how to handle compound words in languages that form long concatenated strings, and what to do with product codes, measurements, or other domain-specific tokens that should be kept intact. A subtler but critical consideration is consistency — the way queries are tokenized must match the way documents were tokenized at index time, because a mismatch silently kills recall. Modern approaches can also break unknown words into smaller recognizable fragments, which helps when users search with rare or specialized terms.

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Query Segmentation]]
- [[Spelling Correction]]

## People

- [[Daniel Tunkelang]]
