---
title: "Query Relaxation"
source: "https://queryunderstanding.com/query-relaxation-342bc37ad425"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems soften or loosen query constraints when initial queries return too few or zero results — part of the Query Understanding series."
tags:
  - clippings
---

# Query Relaxation

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Query relaxation addresses queries that return too few or zero results by progressively removing or softening constraints. It's a key strategy for handling "zero results" pages.

## Relaxation Strategies

**Term dropping**
Remove the least important or rarest terms from the query. Example: "blue vintage leather motorcycle jacket size XL" → "vintage leather motorcycle jacket" → "leather motorcycle jacket".

**AND-to-OR conversion**
Switch from requiring all terms to requiring any terms, with ranking to prioritize documents matching more terms.

**Attribute relaxation**
In structured e-commerce search, relax specific facet constraints:
- Size: "XL" → any size
- Color: "navy blue" → any blue → any color
- Brand: relax to category

**Semantic relaxation**
Move up the taxonomy hierarchy:
- "Nike Air Max 2024" → "Nike running shoes" → "running shoes"

## Implementation

- Waterfall approach: try progressively relaxed queries until results found
- Present "No exact results, but we found..." messaging
- Machine learning to predict best relaxation order

## Tradeoffs

- Too aggressive relaxation → irrelevant results and user frustration
- Too conservative → empty result pages (equally bad)
- Order of relaxation matters: preserve intent as long as possible

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Relaxation]]
- [[Zero Results]]
- [[Query Understanding]]
- [[Faceted Search]]

## People

- [[Daniel Tunkelang]]
