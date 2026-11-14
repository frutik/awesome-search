---
type: company
title: "Wallapop"
aliases: []
tags:
  - company
  - e-commerce
  - marketplace
  - classifieds
created: 2026-11-14
---

# Wallapop

Classified-ads marketplace in southern Europe (Spain, Italy, Portugal), with more than 70 million users. Almost anyone can sell almost anything, so its search runs over user-generated listings with frequent misspellings, and it also has a locality filter so buyers can find items near them. The search team includes search engineers, a principal search engineer, a product manager, front-end engineers, data scientists and analysts.

---

## Search work

- **[[Zero Results]] mitigation**: the team had already contributed a Spanish stemmer to Lucene and shipped synonyms and hyponyms, [[Spelling Correction]], a wider geographic radius for some queries, and looser Boolean matching (minimum-should-match on [[Solr]]). Its next step was alternative queries through [[Query Relaxation]]. The first version drops the least-frequent query term. It reached about 80% offline accuracy, and an A/B test was about to start as of October 2023.
- Vector search was planned as a medium-term investment. Embedding a large, fast-churning listing inventory was the main cost concern.

## Videos

- [[Rene Kriegler & Jean Silva - Alternative Queries for Zero Results]] — [[Haystack EU]] 2023

## People

- [[Jean Silva]] — search engineer

## Related

- [[E-commerce Search]] · [[Query Relaxation]] · [[Zero Results]]
