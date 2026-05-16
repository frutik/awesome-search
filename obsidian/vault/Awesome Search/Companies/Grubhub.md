---
type: company
category: end-user
industry: [food delivery, marketplace]
products: [Grubhub food delivery search, restaurant discovery]
search_domain: food domain search, restaurant and dish retrieval
use_cases: ["[[Grubhub - Query2Vec Food Search]]"]
tags: [company, end-user, food-delivery, query-expansion, embeddings]
created: 2026-05-16
---

# Grubhub

Food delivery marketplace. Search must bridge the wide vocabulary gap in food queries — "tacos", "Mexican food", and "burritos" are semantically related but lexically disjoint.

## Search Context

Food search has extreme vocabulary diversity. Users describe dishes, cuisines, and attributes in highly varied ways. BM25 alone misses most cross-vocabulary matches.

## Key Engineering Work

### Query2Vec — Session-Context Query Embeddings
- Trained word2vec-style embeddings on query session logs
- Session = sequence of queries from same user session (queries in a session are context for each other)
- Skip-gram with negative sampling; predicts surrounding queries from current query
- Embeds entire queries (not individual words) → captures food-domain intent directly

### Query Expansion via KNN
- At query time: embed incoming query → find k-nearest-neighbor queries in embedding space
- Extract terms from neighbor queries as expansion candidates
- Expand original query with top-N candidate terms (weighted by similarity)
- Improved recall, reduced zero-result rate for rare food queries

### Key Design Choice
Domain-specific embeddings trained on Grubhub query logs outperformed general-purpose embeddings (GloVe) for food search.

## Articles

- [[Search Query Expansion with Query Embeddings]] — Query2Vec architecture and results

## Related Concepts

- [[Query Understanding]] · [[Embedding Fine-tuning]] · [[Synonyms]] · [[Zero Results]]
