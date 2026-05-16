---
type: article
tags: [article, vespa, e-commerce, ltr, facets, vocabulary-mismatch, recommendations]
source: "https://blog.vespa.ai/e-commerce-search-and-recommendation-with-vespaai/"
author: [Jo Kristian Bergum]
company: [Vespa]
concepts: [BM25, Learning to Rank, Faceted Search, Embeddings, Query Understanding]
topics: [E-commerce Search, Personalization in Search]
---

# E-commerce Search and Recommendation with Vespa

**[[Jo Kristian Bergum]]** (Vespa) surveys how Vespa addresses core e-commerce search challenges. Used at Yahoo e-commerce sites in Asia.

## Key Capabilities Covered

### Text Ranking Beyond BM25/TF-IDF
Vespa's native ranking features consider query term proximity (not just frequency) — important for e-commerce where "black mini iPad cover compatible with iPad 2" shouldn't outrank "iPad 2."

### Custom Business Ranking Logic
Ranking profiles allow hand-crafted + ML ranking expressions. Sponsored/promoted items can be tiered above organic results via a simple rank profile, combined with LTR models (TensorFlow, XGBoost via ONNX).

### Facets and Grouping
Vespa Grouping Language supports deep nested facet aggregation and pagination within groups.

### Vocabulary Mismatch
"Ladies pregnancy dress" ≠ "Women maternity gown" — solved via semantic retrieval (dense tensor embeddings from Universal Sentence Encoder). Enables multilingual retrieval from a single index.

### Query Classification
ML models (BERT, deployed via ONNX) classify query intent (navigational vs. informational vs. category browse), selecting different ranking profiles or triggering query rewrites.

### Scaling for Holiday Traffic
Vespa's C++ core avoids JVM GC pauses; no shard concept (elastic resizing without re-indexing); graceful degradation under overload; 40-50K partial attribute updates/sec for real-time inventory/price signals.

## Key Takeaway

Vespa's design philosophy — "ranking is just math" — gives relevance engineers full control over scoring functions without needing to rewrite queries. First-class LTR + real-time partial updates + prefiltered ANN makes it a strong all-in-one e-commerce search platform.
