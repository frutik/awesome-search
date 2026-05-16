---
type: company
industry: enterprise SaaS / communication
products:
  - Slack (team messaging)
search_domain: enterprise message and file search
use_cases:
  - "[[Slack - Enterprise Message Search with LTR]]"
---

# Slack

## Search Context

Slack's search problem is a classic enterprise retrieval challenge: users searching their own private communication history. The product must surface the right message, file, or channel across potentially years of workspace history.

It sits at the intersection of personal information retrieval and enterprise knowledge management — more similar to email search than web search or e-commerce.

## Search Challenges

- **Query non-repeatability**: searches are personal and contextual; no stable query distribution
- **Document privacy**: each user accesses a unique document set — aggregate signals don't generalize
- **Recency vs. relevance tension**: the most recent message for a query is often not the right one
- **Position bias in training data**: enterprise users still click top results disproportionately, poisoning LTR training if uncorrected
- **Work graph as signal**: user interaction history (who they talk to, which channels they prioritize) is the key relevance signal

## Tech Stack

- **Apache Solr** for first-stage retrieval (fast, configurable sorting)
- **Application-layer re-ranking** for second stage with richer features
- **SVM via SparkML** as LTR model (pairwise training on click data)
- Work graph: internal interaction history per user (author affinity, channel priority)

## Use Cases

- [[Slack - Enterprise Message Search with LTR]]

## Published Articles

- [[Search at Slack]]
