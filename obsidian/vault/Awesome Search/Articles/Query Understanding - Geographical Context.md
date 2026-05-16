---
title: "Location as Context"
source: "https://queryunderstanding.com/geographical-context-77ce4c773dc7"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems use the user's geographic location to interpret queries and return locally relevant results — part of the Query Understanding series."
tags:
  - clippings
---

# Location as Context

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

User location is one of the most powerful contextual signals for search. Many queries have strong geographic intent — even when location isn't explicitly mentioned.

## Types of Geographic Queries

**Implicitly local queries**
- "pizza" → nearby restaurants
- "weather" → local forecast
- "gas stations" → nearby stations
- "best dentist" → local providers

**Explicitly geographic queries**
- "Paris hotels"
- "California wine"
- "NYC apartments"

**Location-insensitive queries**
- "how to tie a tie" — location irrelevant
- "history of Rome" — no local intent

## Location Signals

- IP address geolocation (coarse, city-level)
- GPS/device location (precise, requires permission)
- User profile settings (home, work locations)
- Query-embedded location terms

## Implementation

**Geosearch indexes**
- Elasticsearch geo_point queries
- Filtering by distance or bounding box
- Boosting proximity in scoring

**Query understanding**
- Detect implicit local intent (query classification)
- Extract explicit locations (NER)
- Resolve to canonical geo-entities (city, region, country)

## Challenges

- Privacy concerns with precise location tracking
- International queries need timezone awareness
- "Paris" might mean Paris, TX vs. Paris, France
- Roaming users (searching local to destination, not current location)

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Personalization]]
- [[Search Intent]]

## People

- [[Daniel Tunkelang]]
