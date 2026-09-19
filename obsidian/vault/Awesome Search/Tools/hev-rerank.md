---
type: tool
title: "hev-rerank"
aliases: ["hev_rerank", "jev-rerank", "hev reranker"]
tags:
  - tool
  - reranking
  - python
  - open-source
website: https://pypi.org/project/hev-rerank/
repo: https://github.com/hev/reranker
license: Apache-2.0
created: 2026-09-19
---

# hev-rerank

**hev-rerank** is a small open-source Python wrapper that uses [[TypeSafe]]'s [[Jev]] model as a
search [[Reranking|reranker]]: one call carries the query and up to 30 candidate documents, and
a true-or-false question (Jev's *Noul* type) is answered per document as a
[[Calibrated Relevance Probability|calibrated probability]]. The ranking is the sort by that
probability.

It was released by [[Hev]] alongside the benchmark in [[Hev meets Jev]], deliberately as a
minimal reference implementation rather than a framework — the stated contents are the prompt,
the request schema, a 90-line wrapper handling chunking and a prune threshold, and the
evaluation results with confidence intervals.

Repository: https://github.com/hev/reranker · PyPI: https://pypi.org/project/hev-rerank/

---

## Usage

```python
# pip install hev-rerank
from hev_rerank import rerank

hits = rerank(query, shortlist, top_n=10, threshold=0.1)
```

The `threshold` argument is the part that distinguishes this from a conventional reranker
client: because the score is a probability rather than a [[Cross-Encoder]] logit, an absolute
cutoff is portable across corpora, and a single call performs a rerank and a prune in the same
round trip.

## Positioning

The author's own read, published with the code, is not a win claim. Voyage rerank-3 scored
marginally higher and cost marginally less in the same benchmark, and the batch call shape has
a worse latency tail (p95 near 1.4 s for thirty documents in one call). What the approach adds
is the calibrated probability and the fact that the same call shape also covers routing,
classification, and gating — and that it requires no reranker training at all.

## Related Notes

- [[Jev]] — the model this wraps
- [[TypeSafe]] — the model's vendor
- [[Hev meets Jev]] — the benchmark and the release announcement
- [[Hev]] — the author
- [[BEIR]] — the evaluation suite

## Related Concepts

- [[Reranking]] — the stage implemented
- [[Calibrated Relevance Probability]] — why the `threshold` argument works
- [[Pointwise Relevance Evaluation]] — the per-document question shape
- [[Text Chunking]] — the wrapper handles chunking against the request budget
- [[Retrieval Pipeline]] — where it sits

## Related Topics

- [[Reasoning Reranking]]
