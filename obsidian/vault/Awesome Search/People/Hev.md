---
type: person
title: "Hev"
aliases: ["hev", "hev mind", "hevmind"]
tags:
  - person
  - reranking
  - benchmarks
  - independent
website: https://hevmind.com
blog: https://hevmind.com/writing/
github: https://github.com/hev
created: 2026-09-19
---

# Hev

**Hev** writes at *hev mind* (https://hevmind.com), a personal site mixing technical writing on
search and AI tooling with interactive data essays, and publishes code at
https://github.com/hev. The name is a handle rather than a stated full name, and no
affiliation is given on the site; the writing is first-person and independent, and it
advertises a small line of self-hosted AI tools under the same `hev` name.

---

## Contribution to This Vault

- [[Hev meets Jev]] (2026-09-16) — benchmarks [[TypeSafe]]'s structured-output model [[Jev]]
  as a search [[Reranking|reranker]] against [[Voyage AI|Voyage]], [[Cohere]], and
  [[Mixedbread]] on three [[BEIR]] subsets, and releases the implementation as
  [[hev-rerank]].

Two things make the piece worth keeping. First, the result: an untuned general decision model
lands within 0.003 mean nDCG@10 of the best purpose-built reranker in the comparison, which is
evidence about the *category* rather than about one vendor. Second, the method — the write-up
reports a determinism re-run, a [[Position Bias|position-bias]] check by order reversal, a
random-permutation floor, and an ablation of the question shape, then states the cases where
its own approach loses. That set of checks is a reusable template for evaluating any reranker.

The author is explicit about the limits: public benchmarks mean possible contamination for
every model in the table, rerank depth was 30, and latency was measured from a laptop with
network included.

## Related Concepts

- [[Reranking]] · [[Calibrated Relevance Probability]] · [[NDCG]]
- [[Statistical Significance in Search Evaluation]] · [[Position Bias]]

## Related Notes

- [[Jev]] · [[TypeSafe]] · [[hev-rerank]]
- [[BEIR]] — the benchmark suite used

## Related Topics

- [[Reasoning Reranking]] · [[Retrieval Benchmarks and Leaderboards]]
- [[Reception of Jev]] — where this benchmark sits in the wider reaction
