---
title: "Personalization"
source: "https://queryunderstanding.com/personalization-3ed715e05ef"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems use individual user profiles and history to tailor query interpretation and result ranking to each user's preferences — part of the Query Understanding series."
tags:
  - clippings
---

# Personalization

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Personalization adapts search results to individual users based on their history, preferences, and behavior. The same query from different users may warrant different results.

## Personalization Signals

**Explicit signals**
- User profile settings (preferred brands, size, gender)
- Saved preferences, wish lists
- Purchase history

**Implicit behavioral signals**
- Click history (what did they click before?)
- Purchase history (what have they bought?)
- Browse history (what categories have they explored?)
- Dwell time (what content did they engage with?)
- Search history (what have they searched for?)

## Personalization Approaches

**Collaborative filtering**
- "Users like you also liked..."
- Find similar users and rank what they prefer

**Content-based filtering**
- Match query results to user's historical preference patterns
- Feature-based similarity (brand, category, price range, style)

**Hybrid approaches**
- Combine collaborative and content-based
- Neural personalization models

**Query rewriting**
- Add user-specific terms to the query
- Boost user-preferred categories/brands

## Challenges

- **Cold start**: New users have no history
- **Privacy**: Personalization requires tracking; GDPR implications
- **Filter bubble**: Over-personalization limits discovery
- **Intent shift**: Past preferences may not reflect current needs
- **Multi-user devices**: Shared devices conflate different users

## E-commerce Personalization

- Show size variants matching user's historical size
- Prioritize preferred brands
- De-rank previously purchased items
- Surface recently viewed items

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Personalization]]
- [[Click Signals]]

## People

- [[Daniel Tunkelang]]
