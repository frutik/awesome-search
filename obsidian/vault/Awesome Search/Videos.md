---
type: index
title: "Videos"
aliases: ["search videos", "talks", "Videos Index"]
tags: [index, moc, videos]
created: 2026-07-05
---

# Videos

Conference talks and recorded presentations on search & information retrieval — the practitioner knowledge that lives in slides and hallway war stories rather than papers.

- [[Max Irwin - The Search Engine Migration Circus]] — [[Max Irwin]] ([[OpenSource Connections]]), Haystack Live; a migration playbook ("Hello Search", feature parity, the "damage" metric) plus real war stories. Companion to [[Migration between Search Engines]].
- [[Choosing Indexes for Similarity Search (Faiss in Python)]] — [[James Briggs]] ([[Pinecone]]); hands-on [[FAISS]] tutorial comparing Flat, [[LSH]], [[HNSW]], and [[IVF]] on Sift1M, with benchmarks and index-selection guidance. Companion to [[Nearest Neighbor Indexes for Similarity Search]].
- [[Rene Kriegler - Query Relaxation]] — [[Rene Kriegler]] ([[OpenSource Connections]]); reframes [[Query Relaxation]] as a query *recommendation* problem and compares word-shape heuristics, term frequency, [[Word2Vec]] and a neural network for predicting which query term to drop. Companion to [[Query Relaxation]].
- [[Roman Grebennikov - Personalizing Search Results in Real-Time]] — [[Roman Grebennikov]] (Findify); [[MICES]] 2019 war stories on real-time LTR personalization: [[Position Bias]] feedback loops, the ~1% shuffled exploration segment, one generic cross-merchant model, and purchase-weighted "perfect rankings" (the Stanley bong story). Companion to [[Exploration vs Exploitation]] and [[Position Bias]].

- [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — [[Evgeniya Sukhodolskaya]] ([[Qdrant]]); [[MICES]] 2026 on making [[SPLADE]] fine-tuning approachable: why off-the-shelf sparse models trained on [[MS MARCO]] misfire on catalogs, the ANCE loop that puts a search engine inside training, and the specialize-vs-generalize trade. Companion to [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] and [[Hard Negative Mining]].
- [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] — [[Evgeniya Sukhodolskaya]] ([[Qdrant]]); [[Berlin Buzzwords]] 2026 on the one search component nobody adapts — the scoring function. Model-generated [[Relevance Feedback]] steers [[HNSW]] hop selection instead of reranking a top-k, distilling a reranker into the index. Companion to [[Relevance Feedback]] and [[HNSW]].

## Related
- [[Case Studies]] · [[Topics]] · [[Concepts]] · [[Tools]] · [[People]]
