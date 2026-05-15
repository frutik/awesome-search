---
title: "Seasonality"
source: "https://queryunderstanding.com/seasonality-5eef79d8bf1c"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How temporal and seasonal signals influence query interpretation and result ranking in search systems — part of the Query Understanding series."
tags:
  - clippings
---

# Seasonality

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Time of year, day of week, and time of day all influence what users want from their searches. A seasonality-aware search system interprets the same query differently based on temporal context.

## Types of Seasonal Effects

**Calendar-driven seasonality**
- "costumes" → Halloween in October, costume parties rest of year
- "flowers" → Valentine's Day, Mother's Day, Christmas
- "swimsuit" → summer intent vs. vacation planning in winter

**Holiday-driven**
- "gifts for men" → Father's Day, Christmas, Valentine's
- "turkey recipes" → Thanksgiving
- Black Friday / Cyber Monday product searches

**Sports seasons**
- "jersey" → NFL season vs. MLB season
- "sneakers" → back-to-school August peak

**Time of day effects**
- "lunch" → different results at 11am vs. 3pm
- News queries → morning browsing patterns

## Implementation

**Time-based ranking boosts**
- Boost seasonally relevant products/content for the current date
- Decay functions for recency in news search

**Seasonal intent classifiers**
- Detect when a query has strong seasonal associations
- Adjust top-of-funnel content seasonally

**Trend detection**
- Real-time trending topics (Google Trends style)
- Spike detection in query logs

## E-commerce Applications

- Seasonal catalog surfacing (sunscreen in summer, jackets in fall)
- Marketing alignment: show promotional content for current season
- Inventory planning: anticipate seasonal demand spikes

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Personalization]]

## People

- [[Daniel Tunkelang]]
