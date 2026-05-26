---
title: "WAND"
aliases: ["Weighted AND", "WAND retrieval", "weak AND", "wand algorithm"]
tags: [concept, retrieval, sparse-retrieval, efficiency]
---

# WAND (Weighted AND)

## Definition

WAND (Weak AND / Weighted AND) is a top-k retrieval algorithm for sparse vector inner-product scoring that avoids scoring every document in an inverted index. It uses per-term upper bound scores to safely skip documents that cannot make it into the top-k results, providing exact top-k guarantees while dramatically reducing the number of full document score evaluations.

## How It Works

WAND maintains a sorted posting list for each query term and uses a **pivot selection** strategy:

1. Assign each term an **upper bound** on the score contribution it can make to any document
2. Sum upper bounds across terms to determine the maximum possible score for a document
3. If this maximum is below the current k-th best score in the heap, the document can be **safely skipped** without computing its full score
4. Only documents that can potentially enter the top-k are fully evaluated

This gives exact top-k results (unlike ANN approximate search) while skipping the majority of candidates.

## WAND vs Full Scan

| | Full Scan | WAND |
|---|---|---|
| Documents evaluated | All (millions) | Small fraction |
| Result quality | Exact | Exact top-k |
| Latency | High | Low |
| Applicability | Any scoring | Inner-product / additive |

## Use in Practice

WAND is most useful for **sparse attribute matching** — queries over weighted feature vectors where documents have many possible attributes but only a few active at once. This is the regime of:
- Classifieds ads with structured attributes (brand, color, category)
- E-commerce product catalogs
- Sparse learned embeddings ([[SPLADE]])

### Kleinanzeigen Implementation

[[Kleinanzeigen]] uses WAND for click-profile retrieval in their Vespa homepage feed. User profiles are attribute weight vectors (L2-normalized, built from click history). Ads encode attributes as `field.value` tokens (e.g., `color.red`, `brand.bmw`). WAND retrieves the most profile-matching ads without scanning the full catalog.

A `relations` document extends the model: token similarity groups with propagation coefficients allow `color.red` to partially match `color.blue`, which is expanded at query time before firing the WAND query.

## WAND in Vespa

[[Vespa]] has a native WAND implementation (`wand()` query operator). It is well-suited to cases where:
- Documents are modeled as weighted sparse attribute vectors
- Queries are user profile vectors (inner product similarity)
- The corpus is large enough that full scan is prohibitive

## Related Concepts

- [[Sparse Vector Retrieval]] — broader category; WAND is a retrieval algorithm within it
- [[SPLADE]] — learned sparse vectors that also benefit from WAND-style retrieval
- [[Dense Vector Retrieval]] — complementary approach using ANN over dense embeddings
- [[Retrieval Pipeline]] — WAND typically serves as a first-stage retrieval method

## Related Notes

- [[From Elasticsearch to Vespa - Rebuilding the Kleinanzeigen Homepage Feed Part 1]]
- [[E-commerce Search and Recommendation with Vespa]]
