---
type: use-case
company: "[[Slack]]"
domain: enterprise / B2B SaaS
problem: rank private message search results where queries rarely repeat and documents are user-specific
scale: enterprise-scale (millions of messages per workspace, unique document access per user)
concepts:
  - "[[Learning to Rank]]"
  - "[[Position Bias]]"
  - "[[Personalization]]"
  - "[[Click Signals]]"
sources:
  - "[[Search at Slack]]"
people: []
---

# Slack — Enterprise Message Search with LTR

## Problem

Message search in Slack has two fundamental differences from web or e-commerce search:

1. **Queries rarely repeat** — people search for specific messages in specific contexts; there's no stable query distribution to build signals from
2. **Documents are private and user-specific** — every user accesses a unique document set (their channels, DMs, files); aggregate click signals don't generalize across users

Standard LTR training on aggregate click data doesn't work. The team needed a signal source that is personal, rich, and available despite query uniqueness.

## Architecture

Two-stage ranking:
1. **First stage** — Solr custom sorting on features cheap for Solr to compute (fast retrieval)
2. **Second stage** — Application-layer re-ranking with richer features (accurate, slower)

LTR model: SVM via SparkML, trained on pairwise-transformed click data.

## Key Innovation: Work Graph as Signal Source

Instead of aggregate query-click logs, Slack used the **work graph** — internal interaction history per user:
- Messages from people you interact with frequently rank higher
- Channels and DMs you prioritize rank higher
- Pins, stars, and reactions surface important content

This personal interaction graph provides stable, high-quality relevance signal that doesn't depend on query repetition.

## Position Bias Fix

Discovery: users clicked top results 30% more often purely due to position.

Fix: **oversample clicks on lower-ranked results** during training data construction to equalize positional distribution. This prevents the model from learning "rank 1 is always clicked" as a spurious feature.

## Top Ranking Signals

1. Message recency (age)
2. Lucene BM25 match score
3. User affinity to message author (from work graph)
4. Priority scores for channels and DMs
5. Message metadata: pins, stars, reactions count
6. Content characteristics: word count, formatting richness

## Results

- **+27% clicks at position 1** — top result is more often the right result
- **+9% overall increase in clicked searches**

## Key Lessons

- When query repetition is low, the user's behavioral graph is a better training signal than aggregate click logs
- Position bias correction is mandatory before training pairwise LTR — uncorrected data teaches the model to rank popular positions, not relevant documents
- Two-stage ranking lets you put cheap features in Solr and expensive features in app layer — useful when the underlying search engine is a black box
- Work graph features (author affinity, channel priority) are more stable than document-level features for personal communication search

## What to Steal

- Work graph / interaction graph as LTR signal: applicable to any enterprise search where users have stable interaction patterns (email, docs, tickets)
- Position bias oversampling trick: simple to implement, high impact on pairwise LTR quality
- Two-stage architecture pattern with stage-appropriate feature sets
