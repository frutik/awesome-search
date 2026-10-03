---
title: "NewsSpectrum"
aliases: ["NewsSpectrum dataset", "DiversiNews NewsSpectrum"]
type: dataset
tags:
  - dataset
  - diversity
  - news
  - information-retrieval
source: "Introduced with DiversiNews (PVLDB 17(12), 2024)"
domain: political-perspective diversity in news retrieval
related_concepts:
  - "[[Diversity Metrics]]"
  - "[[Maximum Inner Product Search]]"
  - "[[MMR]]"
repo: https://github.com/dukesun99/DiversiNews/tree/main/NewsSpectrum
created: 2026-10-03
---

# NewsSpectrum

## Overview

**NewsSpectrum** is a news corpus balanced across political media-bias categories. It was built for **DiversiNews**, the news-retrieval demo of diversity-aware inner-product search covered in [[Diversity-Aware k-Maximum Inner Product Search Revisited]]. Every article carries its outlet's bias rating, so a retrieved set can be scored on how far it spreads across the political spectrum, as well as on relevance.

## Construction

| Property | Value |
|---|---|
| Source | URLs from Reddit submissions in the Pushshift dump, up to July 2022, with at least 10 upvotes |
| Articles | 250,000 |
| News sources | 961 |
| Bias categories | Left, Lean Left, Center, Lean Right, Right — 50,000 articles each |
| Label source | AllSides media-bias ratings, matched by outlet domain, scored −2 to +2 |

## What the labels are — and are not

The bias labels describe **outlets**, not individual articles. The dataset's own documentation says they are not independently annotated article-level ideology or factual-accuracy labels. A diversity score computed on them, such as the mean pairwise bias difference used in DiversiNews, measures a **spread of sources**, which is only a proxy for a spread of viewpoints. The corpus is also concentrated on US politics. The DiversiNews authors note this but argue the method does not depend on it, because the labels are used only for evaluation and never for encoding or retrieval.

## Use

- **DiversiNews** — the evaluation corpus, encoded with Sentence-BERT, AnglE and LLaMA 2 embeddings and searched with DkMIPS at k = 10.
- **DkMIPS journal version** — the accompanying repository lists NewsSpectrum (249,000 vectors, encoded with AnglE `UAE-Large-V1`) as one of its two text-retrieval evaluation sets.

## Availability

Published in the [DiversiNews repository](https://github.com/dukesun99/DiversiNews/tree/main/NewsSpectrum) via Git LFS. The MIT license covers the code and the curated metadata and labels; the article texts remain the property of their publishers and are provided for research use.

## Related Concepts

- [[Diversity Metrics]] — the bias-difference diversity measure is a label-based, set-level metric
- [[Maximum Inner Product Search]] — the retrieval setting it was built to evaluate
- [[MMR]] — the relevance/diversity trade-off being measured

## Related Topics

- [[Search Result Diversity]]

## Related Datasets

- [[LocalNews]] — another diverse-news benchmark from the same research group, aimed at aspect coverage rather than political spread

## Related Articles

- [[Diversity-Aware k-Maximum Inner Product Search Revisited]] — DkMIPS and the DiversiNews demo that released this corpus
