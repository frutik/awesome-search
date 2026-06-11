---
type: company
tags: [company, e-commerce, germany, ltr, marketplace, solr]
category: end-user
industry: e-commerce / marketplace
products: [otto.de marketplace]
search_domain: [product search, learning to rank, marketplace ranking]
use_cases: []
people: [Andrea Schütt]
---

# Otto

Otto (otto.de) is one of Germany's largest e-commerce companies, transitioning from a catalogue retailer to a marketplace with millions of products from multiple sellers.

## Search & Ranking Work

**LTR implementation** — motivated by marketplace expansion making manual ranking rules unscalable:
- Model: **[[LambdaMART]]** (pairwise + NDCG-weighted listwise)
- Training framework: **[[RankLib|RankyMcRankFace]]** (fork of RankLib)
- Infrastructure: **Solr** with LTR plugin + feature store
- Labels: derived from customer interaction data (clicks, add-to-basket, orders, dwell time)
- Evaluation: custom Offline Metrics Analyzer computing NDCG at multiple configurations

Challenge: crowd-sourced labels don't work for purchase-intent relevance — labels must come from behavioral signals.

## Related

- [[Part 1 - Learning to Rank for E-Commerce Search at Otto]]
- [[Andrea Schütt]]
