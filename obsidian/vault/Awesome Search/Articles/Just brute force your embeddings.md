---
created: 2026-07-30
title: "Just brute force your embeddings"
source: "https://softwaredoug.com/blog/2026/07/29/just-brute-force-embeddings"
author: "[[Doug Turnbull]]"
published: 2026-07-29
type: article
concepts:
  - "[[Brute-Force Vector Search]]"
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Dense Vector Retrieval]]"
topics:
  - "[[Vector Search Tradeoffs]]"
  - "[[Search Platforms]]"
tags: [article, vector-search, brute-force, numpy, vector-database, capacity-planning]
---

# Just brute force your embeddings

**Author:** [[Doug Turnbull]]

## Summary

Most teams reaching for a vector database don't have the corpus size to justify one. On
384-dimensional float32 embeddings on an M4 MacBook Pro, a single NumPy dot product against
the whole matrix serves ~1M documents at 79.7 QPS single-threaded with 12ms average latency.
For low enough n, [[Brute-Force Vector Search|brute force]] the embeddings "until you can't
bear to."

The framing borrows from Raymond Chen, quoted in the post: *"My O(n) algorithm can run
circles around your O(log n) algorithm; why much of what you learned in school simply doesn't
matter."* Doug's addition: true of sorting, true of vector search.

## The Measurement

| Index Size | Client Threads | QPS | Avg Latency |
|---|---|---|---|
| 1,000,000 | 1 | 79.7 | 0.012s |
| 1,000,000 | 10 | 170.5 | 0.058s |
| 8,841,823 | 1 | 9.34 | 0.106s |
| 8,841,823 | 10 | 18.34 | 0.106s |

384-dim embeddings, float32, M4 MacBook Pro. One oddity, reproduced here as published: at
8,841,823 vectors the table reports the same 0.106s average latency for one and ten client
threads, although QPS roughly doubles between them. The other three rows are consistent with
QPS ≈ threads ÷ latency; this one is not.

The entire search is one line:

```python
# Dot product against all
scores = self.doc_vectors @ query_vector.astype(np.float32, copy=False)
```

## When Brute Force Is Enough

The profile of teams Doug describes as not needing vector database complexity:

- **~1m documents** to search
- **Low query traffic**
- **Embeddings written up front** — no live index updates

The cost avoided is not just licensing but operations: *"They don't need to buy a
multi-million dollar vector database, or spend 6 months learning to operate it."*

Past that point: consider a database, or load everything into memory with [[FAISS]] and call
it done. The post cites [[Jo Kristian Bergum]] — *"an exhaustive search may be all you need"* —
from [[Three mistakes when introducing embeddings and vector search]].

## Headroom Left on the Table

The numbers are naive NumPy and could go faster. Two openings noted:

- Give each thread **more than one query per scan** (credited in the post to Andreas Erickson,
  [post](https://x.com/andreer/status/2082531919233761580)) — amortising the memory pass over
  a batch of queries instead of re-scanning per query.
- Collecting into a **top-n heap** during the scan rather than having NumPy score everything
  first.

Both are throughput optimisations, not asymptotic ones — the scan stays O(n × d).

## Related Concepts

- [[Brute-Force Vector Search]] — the exact-scan baseline this post argues for
- [[Approximate Nearest Neighbor Search]] — what you buy an index to avoid the scan
- [[Dense Vector Retrieval]] — the retrieval setting
- [[Vector Similarity Metrics]] — the dot product being computed here

## Related Articles

- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]];
  the source of the exhaustive-search argument quoted here, with its own measurement of the
  same scan on 2023 hardware
- [[Principal Component Analysis - an embedding shrink-ray]] — same author; shrink the vectors
  instead of indexing them
- [[Why Are Embeddings So Cheap]] — the other half of the cost argument
- [[The Scaling Dimensions of Keyword Search]] — the lexical counterpart to "how big before it
  hurts"

## People

- [[Doug Turnbull]] — author
- [[Jo Kristian Bergum]] — cited

## External References

- Raymond Chen, *My O(n) algorithm can run circles around your O(log n) algorithm* — https://devblogs.microsoft.com/oldnewthing/20050622-49/?p=35223
- Jo Kristian Bergum, *Three mistakes when introducing embeddings and vector search* — https://bergum.medium.com/four-mistakes-when-introducing-embeddings-and-vector-search-d39478a568c5
- Andreas Erickson on batching queries per scan — https://x.com/andreer/status/2082531919233761580
- *Build your own vector database* (the author's course) — https://maven.com/softwaredoug/vectordb (see [[Courses]])
