---
type: article
title: "Qdrant 1.19 - Turbo4 Datatype and Memory Tiers"
aliases: ["Qdrant 1.19"]
source: "https://mohamedarbi.xyz/posts/qdrant-119"
author:
  - "[[Mohamed Arbi Nsibi]]"
published: 2026-08-07
created: 2026-08-10
company: [Qdrant]
tags:
  - article
  - qdrant
  - vector-quantization
  - turboquant
  - multitenancy
  - bm25
  - vector-database
concepts:
  - TurboQuant
  - Vector Quantization
  - BM25
  - HNSW
topics:
  - Multi-Tenancy in Search
---

# Qdrant 1.19 - Turbo4 Datatype and Memory Tiers

**[[Mohamed Arbi Nsibi]]** walks through four changes in [[Qdrant]] 1.19, with runnable client examples and a companion repo. The through-line is storage: 1.18 added [[TurboQuant]] as a *quantization mode*; 1.19 adds it as a *storage datatype*, and reorganizes how everything else decides between RAM and disk.

---

## Turbo4 as a Datatype, Not a Quantization Mode

The distinction is the substance of the release. Quantization in the 1.18 model is an *accelerator*: the compressed copy is a fast filter, the float32 original stays on disk, and top candidates are rescored against the originals to recover the recall the compression lost. Both copies exist — 32 bits plus 4 bits, 36 bits per coordinate.

`Datatype.TURBO4` stores only the 4-bit form, applied at write time:

```python
vectors_config=models.VectorParams(
    size=1024,
    distance=models.Distance.COSINE,
    datatype=models.Datatype.TURBO4,
)
```

36 bits to 4 is the nine-fold disk reduction the article reports. The cost is structural rather than incremental: with no originals retained, there is nothing to rescore against, so the rescoring stage that normally repairs quantization error is simply unavailable.

The reported gap is recall@10 of 0.866 for turbo4 against 0.998 for float32. The measurement is on random gaussian vectors, which the author flags as "the worst possible case for any quantizer" — real embedding models produce structured, correlated vectors, and rotation-based quantizers exploit exactly that structure. Read the 13-point gap as a bound, not an estimate.

## Memory Tiers

One `memory` parameter replaces the `on_disk`, `always_ram`, and `on_disk_payload` flags, with three tiers:

| Tier | Semantics |
|---|---|
| `pinned` | Loaded onto the heap, never evicted |
| `cached` | On disk; Qdrant pre-warms the OS page cache at startup |
| `cold` | On disk; loaded lazily on first access |

`cached` is the notable one — it names something the old flags could not express: relying on the OS page cache while removing the first-query penalty that normally comes with it. The setting applies per component, so vectors, the [[HNSW]] graph, and the quantized copy can sit in different tiers. `pinned` is rejected for dense vectors and payloads.

## Per-Tenant IDF

Multi-tenant [[BM25]] scoring can now scope inverse document frequency to a tenant rather than the whole shard. The article's example: one tenant stores legal documents where "invoice" is rare and highly discriminating; another stores accounting documents where it appears in nearly every file. Blended statistics give both tenants a term weight that is wrong for their own corpus.

What matters architecturally is not the problem — it is that the fix no longer requires physical separation. Tenant-local statistics were previously a consequence of index-per-tenant; making them a scoring option removes one of the standard reasons to climb the isolation ladder. See [[Multi-Tenancy in Search]].

## Filtering: Prefix and Slice

Keyword indexes accept `prefix=True`, enabling `MatchPrefix` queries — useful for URL and path-shaped keyword fields.

`SliceCondition` partitions a collection deterministically: a point belongs to slice `index` of `total` when `hash(id) % total == index`, hashed with SipHash-2-4. The slices are disjoint, need no coordination between workers, and are stable across versions — which is what makes it usable for parallel scrolls and reproducible sampling rather than just sharding.

## Related Concepts
- [[TurboQuant]] — the algorithm turbo4 stores
- [[Vector Quantization]] — the family; turbo4 is the storage-format end of it
- [[BM25]] — per-tenant IDF scopes its corpus statistic
- [[HNSW]] — one of the components with its own memory tier

## Related Topics
- [[Multi-Tenancy in Search]]

## Related Articles
- [[TurboQuant in Qdrant]] — the 1.18 release this builds on

## People
- [[Mohamed Arbi Nsibi]]

## Sources
- https://mohamedarbi.xyz/posts/qdrant-119
- https://github.com/Goodnight77/qdrant-resources/tree/main/Qdrant-1.19-hands-on
