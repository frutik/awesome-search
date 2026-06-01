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

Stemming and lemmatization both aim to reduce words to a common base form so that queries and documents using different morphological variants of the same word can still match each other. Stemming does this by mechanically stripping word endings using rules — it is fast but can produce errors in both directions, over-conflating unrelated words or under-conflating words that should match. Lemmatization is more careful, using linguistic knowledge to reduce words to their actual dictionary forms, but requires more processing and language-specific resources. Both techniques must be applied symmetrically to queries and documents at index time — the same base forms need to appear in both places for matching to work. The tradeoffs between speed, accuracy, and domain fit make the choice between them a meaningful one for any given system.

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Spelling Correction]]
- [[BM25]]

## People

- [[Daniel Tunkelang]]
