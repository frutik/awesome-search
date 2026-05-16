---
type: person
name: Isabella Tromba
affiliation: Slack
role: Software Engineer, Search & Learning Infrastructure (SLI)
tags: [person, learning-to-rank, enterprise-search, slack]
created: 2026-05-16
---

# Isabella Tromba

Software Engineer on Slack's **Search & Learning Infrastructure (SLI)** team. Co-authored the Search at Slack engineering post describing Slack's two-stage LTR system for enterprise message search.

## Articles

- [[Search at Slack]] — two-stage LTR, work graph signals, position bias oversampling, +27% P@1

## Key Contributions

- Position bias fix: oversample clicks from lower positions to equalize positional distribution in training data
- Work graph as personalization signal: user affinity to message author, channel priority
- Two-stage architecture: Solr first-pass + application-layer re-ranking with SparkML SVM

## Related

- [[Slack]] · [[Learning to Rank]] · [[Position Bias]] · [[Personalization]]
