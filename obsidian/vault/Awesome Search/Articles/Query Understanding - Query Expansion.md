---
title: "Query Expansion"
source: "https://queryunderstanding.com/query-expansion-2d68d47cf9c8"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems add related terms to queries to improve recall by matching documents that use different vocabulary than the user — part of the Query Understanding series."
tags:
  - clippings
---

# Query Expansion

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Query expansion adds terms to the user's original query to increase the chance of matching relevant documents that use different vocabulary. The core problem it addresses is the vocabulary mismatch between how users phrase queries and how documents are written — a user searching for one word should be able to find content that only uses a synonym. Expansion sources include structured synonym resources, behavioral data showing which queries lead users to the same results, and semantic models that surface conceptually related terms. The key tension is between recall and precision: adding too many terms dilutes the query's original meaning and surfaces irrelevant results, so expanded terms are typically given lower weight than the original query terms. Context matters too — the right expansions for an ambiguous word depend on which sense the user intended.

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Synonyms]]
- [[Zero Results]]
- [[Hybrid Search]]

## People

- [[Daniel Tunkelang]]
