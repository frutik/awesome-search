---
title: "Query Rewriting: An Overview"
source: "https://queryunderstanding.com/query-rewriting-an-overview-d7916eb94b83"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "Overview of query rewriting techniques that transform a user's original query into one more likely to retrieve relevant results — part of the Query Understanding series."
tags:
  - clippings
---

# Query Rewriting: An Overview

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Query rewriting transforms the user's original query into an alternative formulation that better matches the search system's index and ranking capabilities. It's a catch-all term for many specific techniques.

## Types of Query Rewriting

**Query Expansion**
Adding terms to broaden the query scope and improve recall.
- Synonym expansion ("sofa" → "sofa OR couch OR settee")
- Related term expansion
- Ontology-based expansion

**Query Relaxation**
Removing or softening constraints to handle queries with few or zero results.
- Drop rare or overly specific terms
- Convert AND to OR
- Broaden category constraints

**Query Segmentation**
Rewriting by identifying phrase boundaries in multi-word queries.
- "red dress shoes" → ["red dress", "shoes"] vs. ["red", "dress shoes"]

**Query Substitution**
Replacing the entire query or key terms.
- Spelling correction
- Synonym substitution
- Acronym expansion

**Query Canonicalization**
Normalizing equivalent queries to a standard form.
- "shoes for men" → "men's shoes"

## Implementation Approaches

- Rule-based: Hand-crafted rewrite rules
- Statistical: Mining from query logs (click-through data)
- Neural: Seq2seq models, retrieval-augmented rewriting

## Key Metrics

- Effect on result count (recall)
- Effect on relevance (precision)
- Coverage (fraction of queries rewritten)

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Query Relaxation]]
- [[Synonyms]]
- [[Query Segmentation]]
- [[Spelling Correction]]
- [[Zero Results]]

## People

- [[Daniel Tunkelang]]
