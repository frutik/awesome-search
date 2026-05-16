---
title: "Session Context"
source: "https://queryunderstanding.com/session-context-4af0a355c94a"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems use the history of queries within a session to better understand evolving user intent — part of the Query Understanding series."
tags:
  - clippings
---

# Session Context

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

A search session consists of multiple queries by the same user pursuing a goal. Later queries in a session provide context for understanding earlier and current queries. Session context enables more relevant results by tracking how user intent evolves.

## Why Sessions Matter

Single queries are often ambiguous. Sessions reveal:
- Refinements: "shoes" → "running shoes" → "Nike running shoes"
- Corrections: user reformulates after unsatisfying results
- Related facets: "red dress" → "red heels" (coordinating outfit)
- Progressive intent: "flights to Paris" → "hotels in Paris" → "Paris restaurants"

## Approaches

**Rule-based session modeling**
- Carry over key entities from previous queries
- Detect query reformulations vs. new search

**Statistical session models**
- Model query sequences as Markov chains
- Hidden Markov Models for session state

**Neural session models**
- RNN/LSTM to encode session history
- Transformer-based session encoders
- BERT fine-tuned on session sequences

## Implementation Challenges

- Session boundaries: when does a new search intent begin?
- Balance session context vs. new explicit intent
- Privacy: session data is sensitive
- Latency: session modeling adds overhead

## Applications

- Conversational search refinement
- Query auto-completion personalized to session
- "You searched for X earlier — do you want Y?"

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Session-Based Evaluation]]
- [[Click Signals]]

## People

- [[Daniel Tunkelang]]
