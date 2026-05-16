---
type: company
industry: ride-sharing / food delivery / logistics
products:
  - Uber Eats
  - Uber (rides)
search_domain: geo-aware food and retail catalog search
use_cases:
  - "[[Uber Eats - Scaling Search for Food Delivery]]"
---

# Uber

## Search Context

Uber's search infrastructure primarily serves **Uber Eats** — a food, grocery, and retail delivery marketplace operating globally. The search problem is inherently geo-aware: results must be filtered and ranked by delivery radius, ETD (Estimated Time of Delivery), and store availability in real time.

The same infrastructure powers multiple surfaces: Home Feed, Search, Suggestions, Ads.

## Search Challenges

- **Geo-awareness at scale**: sharding a global index by location without hotspots
- **Multi-category catalog**: restaurants (hundreds of items) vs. grocery (100k SKUs/store) require different index layouts
- **Latency under expansion**: growing delivery radius from 10–15 min to 50+ miles multiplied candidate set size
- **Real-time constraints**: ETD changes constantly; indexing must reflect current delivery windows

## Tech Stack

- Custom search platform built on **Apache Lucene** with Lambda architecture (Spark batch + Kafka streaming)
- **H3 hexagonal geosharding** for geographic partitioning
- Four-layer architecture: Base Search → NER Query Builder → Catalog API → Search API + Algorithm Gateway

## People

- [[Janani Narayanan]] — ML Engineer
- [[Karthik Ramasamy]] — Senior Staff SWE

## Use Cases

- [[Uber Eats - Scaling Search for Food Delivery]]

## Published Articles

- [[Optimizing Search at Uber Eats]]
- [[Food Discovery with Uber Eats - Building a Query Understanding Engine]]
