---
title: "Maximal Marginal Relevance to Re-rank results in Unsupervised KeyPhrase Extraction"
source: "https://medium.com/tech-that-works/maximal-marginal-relevance-to-rerank-results-in-unsupervised-keyphrase-extraction-22d95015c7c5"
author:
  - "[[Aditya Kumar]]"
published: 2019-10-24
created: 2026-05-15
description: "How MMR solves the keyphrase redundancy problem — selecting keyphrases that are both query-relevant and novel relative to already-selected phrases."
tags:
  - clippings
---
# Maximal Marginal Relevance for Keyphrase Extraction

## The problem

Keyphrase extractors (TextRank, RAKE, POS tagging) produce redundant results. "Good Product," "Great Product," "Nice Product," "Excellent Product" all rank highly but convey the same information — wasting limited display space.

## Solution 1: Cosine similarity filtering

Remove phrases with cosine similarity above threshold (e.g., 0.9). Requires manual threshold adjustment, may miss similar phrases below cutoff.

## Solution 2: MMR re-ranking

MMR score = λ × Sim(phrase, document) − (1−λ) × max Sim(phrase, previously_selected_phrases)

- λ = 0.5: optimal balance between diversity and accuracy
- λ → 1: prioritize relevance
- λ → 0: prioritize diversity

The algorithm selects keyphrases based on both query relevance and novelty — "the degree of dissimilarity between the document being considered and previously selected ones."

## Result

Top N keyphrases provide meaningful variety. Similar phrases are ranked far apart, eliminating the clustering problem where redundant terms dominate results.


## Related Concepts

- [[Diversity Metrics]]
- [[Query Understanding]]
- [[Search Evaluation]]

## People

- [[Aditya Kumar]]
