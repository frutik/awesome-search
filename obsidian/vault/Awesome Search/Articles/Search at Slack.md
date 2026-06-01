---
title: "Search at Slack"
tags:
  - clippings
  - search
  - case-study
  - ranking
  - company-blog
source: "https://slack.engineering/search-at-slack-431f8c80619e"
author: "[[Isabella Tromba]], John Gallagher, Jason Liszka"
created: 2026-05-15
concepts:
  - Learning to Rank
  - Personalization
  - Position Bias
---

# Search at Slack

**Source:** https://slack.engineering/search-at-slack-431f8c80619e
**Authors:** [[Isabella Tromba]] (Software Engineer, SLI), John Gallagher, Jason Liszka (Senior Staff Engineer)

## Summary

How Slack built a two-stage [[Learning to Rank]] system for message search, addressing unique challenges of enterprise communication search where queries rarely repeat and each user accesses unique documents.

## Architecture

**Two-Stage System:**
1. **First stage** — Solr custom sorting on features easy for Solr to compute (fast)
2. **Second stage** — Application-layer re-ranking using additional features (accurate)

LTR model: SVM via SparkML trained on pairwise-transformed click data.

## Unique Data Challenges

- Slack queries rarely repeat (unlike web search)
- Each user accesses unique private documents
- Solution: leverage the "work graph" — internal interaction history — instead of aggregate click data

## Position Bias Handling

Users clicked top results 30% more often purely due to position. Fix: **oversample clicks on results lower in the list** to equalize positional distribution in training data.

## Top Ranking Signals

1. Message age (recency)
2. Lucene match score
3. User affinity to message author
4. Priority scores for channels and DMs
5. Message metadata (pins, stars, reactions)
6. Content characteristics (word count, formatting)

## Results

- **+9%** increase in clicked searches
- **+27%** increase in clicks at position 1
- Top Results feature combining relevant + recent results

## Related Concepts

- [[Learning to Rank]]
- [[Personalization]]
- [[Position Bias]]
- [[BM25]]
- [[Click Signals]]

## Related Articles

- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]]
- [[How LambdaMART Works]]
