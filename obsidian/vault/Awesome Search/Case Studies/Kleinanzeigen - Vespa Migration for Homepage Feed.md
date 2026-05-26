---
type: case-study
company: "[[Kleinanzeigen]]"
tags: [case-study, vespa, personalization, wand, homepage-feed, e-commerce]
source: "https://medium.com/berlin-tech-blog/from-elasticsearch-to-vespa-rebuilding-the-kleinanzeigen-homepage-feed-part-1-b6164e366ab8"
people:
  - "[[Andre Charton]]"
---

# Kleinanzeigen — Vespa Migration for Homepage Feed

## Context

[[Kleinanzeigen]] (Germany's largest classifieds marketplace) migrated their homepage personalized feed from [[Elasticsearch]] to [[Vespa]]. The homepage feed is the first screen millions of users see when they open the app.

## Problem

With Elasticsearch, profile learning, scoring, and retrieval were split across multiple services. Every new behavioral signal required a round-trip through an external orchestration layer. Scaling personalization meant scaling all dependencies.

## Solution: Everything Inside Vespa

### Infrastructure
- Vespa Cloud on AWS, European region
- Separate read/write containers sharing one content cluster
- Staging environment mirroring production

### Three Document Schemas

| Schema | Key / Keying | Contents |
|--------|-------------|----------|
| `ads` | ad ID | Attributes as `weighted_set<string>` in `field.value` format |
| `user_category_profile` | `{userId}:category:{categoryId}` | Click-derived weights (L2-normalized), recent keywords, clicked IDs, geo, explicit prefs |
| `relations` | category ID (global, replicated) | Field importance weights + token similarity groups with propagation coefficients |

### Click Profile Matching (Phase 1)

**Update path**: click → Vespa document update → document processor (in-process) → reads ad attributes + existing profile → merges with decay → writes updated profile back to Vespa.

**Query path**: read user profile → expand tokens via relations graph → fire WAND query → return personalized feed.

No external profile store. No service hop at query time. The full click-profile loop lives inside Vespa.

### Token Similarity Propagation

The `relations` document defines similarity groups: `color.red` and `color.blue` share a group with a similarity coefficient. At query time, weights are propagated to similar tokens before the WAND query fires. This allows partial attribute matching without secondary indices.

## Results / Insights

- Proved Vespa can own the full click-profile loop end-to-end
- System is faster, operationally simpler, and easier to evolve than the Elasticsearch setup
- Part 2 (by a colleague) covers explicit preferences, ranking strategies, and semantic retrieval

## Concepts

[[WAND]] · [[Personalization]] · [[Click Signals]] · [[Sparse Vector Retrieval]] · [[Vespa]]

## Related Notes

- [[From Elasticsearch to Vespa - Rebuilding the Kleinanzeigen Homepage Feed Part 1]]
- [[Adopting Vespa for Recommendation Retrieval at Vinted]]
