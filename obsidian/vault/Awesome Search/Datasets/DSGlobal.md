---
title: "DSGlobal"
aliases: ["DSGlobal benchmark", "DiverseSumm Global"]
type: dataset
tags:
  - dataset
  - benchmark
  - diversity
  - news
  - information-retrieval
source: "Introduced in Uncovering the Bigger Picture: Comprehensive Event Understanding via Diverse News Retrieval (EMNLP 2025); adapted from DiverseSumm"
domain: paragraph-level diverse news retrieval (global events)
related_concepts:
  - "[[APD]]"
  - "[[Diversity Metrics]]"
  - "[[Search Evaluation]]"
website: https://github.com/tangyixuan/NEWSCOPE
created: 2026-09-07
---

# DSGlobal

## Overview

**DSGlobal** is the global-news counterpart to [[LocalNews]], released with [[Uncovering the Bigger Picture - Comprehensive Event Understanding via Diverse News Retrieval|NEWSCOPE]] to test whether diverse-retrieval results generalize beyond regional reporting.

It is an **adaptation, not a new collection**: the underlying corpus is **DiverseSumm** (Huang et al., 2024), a dataset originally built for multi-source news *summarization*, re-segmented into paragraphs and repurposed as a retrieval benchmark. That lineage is the point — DiverseSumm was already assembled around the premise that one event is reported many ways, which is exactly the property a diversity benchmark needs.

## Statistics

| Property | Value |
|---|---|
| Events | 147 |
| Paragraphs | 7,532 |
| Avg. sentences per paragraph | 7.5 |
| Avg. words per paragraph | 123 |

Larger than [[LocalNews]] on both axes, with near-identical paragraph shape — the two were built to be compared directly.

## What It Measures

The same six measures as [[LocalNews]]: [[Precision and Recall|precision, recall]] and F1 for relevance, plus [[APD|Average Pairwise Distance]], Positive Cluster Coverage and Information Density Ratio for diversity, at depths of 5, 10, 20 and 50.

Results on DSGlobal track LocalNews closely, which is what the dataset exists to establish. The one visible difference is that recall is much lower at shallow depths across every method — global events carry more relevant paragraphs, so the top 5 covers proportionally less of them.

## Availability

Distributed as `DSGlobal.zip` in the [NEWSCOPE repository](https://github.com/tangyixuan/NEWSCOPE). The repository carries **no license file**; the original DiverseSumm terms also apply upstream.

## Related Datasets

- [[LocalNews]] — the companion local-news benchmark, built from scratch rather than adapted

## Related Concepts

- [[APD]] — one of the three diversity metrics reported on it
- [[Diversity Metrics]] — the broader family
- [[Search Evaluation]]

## Related Topics

- [[Search Result Diversity]]

## Related Articles

- [[Uncovering the Bigger Picture - Comprehensive Event Understanding via Diverse News Retrieval]] — the paper that adapted it
