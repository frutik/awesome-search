---
tags:
  - search
  - information-retrieval
---
 # Awesome Search — Information Retrieval & Search Knowledge Graph
 
 Hello, I am [Andrew](https://www.linkedin.com/in/andriy-kornilov).

I've been building e-commerce search applications for 15+ years. Over that time, I've collected and connected ideas from publications, conference talks, books, research papers, blog posts, and practitioners across the information retrieval ecosystem.

This knowledge graph maps many of the resources that have influenced my thinking, organized by topic and interconnected through shared concepts. Because search is inherently multidisciplinary, many resources are linked to multiple areas of the graph, reflecting how ideas from ranking, relevance, user behavior, machine learning, evaluation, and system design often overlap.

⭐ Star us on GitHub — it helps!

Semantic knowledge graph built from the [Awesome Search](https://github.com/frutik/awesome-search) curated list. Contains article notes (for paywalled articles, only summaries and key concepts are included), concept notes, topic notes, people notes, case study notes, and company notes, all interconnected through wikilinks.

## Maps of Content (Entry Points)

| Domain | MOC |
|---|---|
| Agentic Search & Embeddings | [[MOC - Agentic Search and Embeddings]] |
| Search Quality & Query Understanding | [[MOC - Search Quality Assurance and Query Understanding]] |
| Ranking & Retrieval | [[MOC - Ranking and Retrieval]] |
| Search UX & Discovery | [[MOC - Search UX and Discovery]] |
| Case Studies | [[MOC - Case Studies]] |
| Architecture & Search Team | [[MOC - Architecture and Search Team]] |

## Core Concepts by Domain

### Retrieval
[[BM25]] · [[Dense Vector Retrieval]] · [[Brute-Force Vector Search]] · [[Sparse Vector Retrieval]] · [[Learned Sparse Retrieval]] · [[SPLADE]] · [[miniCOIL]] · [[Hybrid Search]] · [[Reciprocal Rank Fusion]] · [[Relative Score Fusion]] · [[Semantic Boosting]] · [[Semantic Search]] · [[Zero-Shot Retrieval]] · [[SIRA]]

### Embeddings
[[Bi-Encoder]] · [[Cross-Encoder]] · [[ColBERT]] · [[Late Interaction]] · [[MUVERA]] · [[Matryoshka Embeddings]] · [[SPLADE]] · [[ELSER]] · [[Task-Aware Embeddings]] · [[Hypothetical Document Embeddings]] · [[Dimensionality Reduction]] · [[PCA]] · [[t-SNE]] · [[UMAP]] · [[Vector Quantization]] · [[Scalar Quantization]] · [[Binary Quantization]] · [[TurboQuant]]

### Ranking
[[Learning to Rank]] · [[Personalization]] · [[Position Bias]] · [[Diversity Metrics]] · [[Retrieval Pipeline]] · [[Results Boosting]] · [[Results Merchandising]] · [[Signal Downboosting]]

### Evaluation
[[NDCG]] · [[MRR]] · [[MAP]] · [[Precision and Recall]] · [[UDCG]] · [[Search Evaluation]] · [[Judgment Lists]] · [[Vector Search Evaluation]] · [[LLM as Judge]] · [[Session-Based Evaluation]] · [[Click Signals]] · [[Pointwise Relevance Evaluation]] · [[Pairwise Relevance Evaluation]] · [[Listwise Relevance Evaluation]]

### Query Understanding
[[Query Understanding]] · [[Query Types]] · [[Search Intent]] · [[Query Segmentation]] · [[Collocations]]

### Lexical Query Operations
[[Spelling Correction]] · [[Synonyms]] · [[Stopwords]] · [[Autocomplete]] · [[Query Expansion]] · [[Query Relaxation]]

### Search UX & Discovery
[[Search UX]] · [[Faceted Search]] · [[Search Scopes]] · [[Federated Search]] · [[Zero Results]] · [[Presentation Bias]] · [[Results Merchandising]] · [[Search Result Diversity]] · [[MMR]]

### Architecture & RAG
[[Search Architecture]] · [[Knowledge Graph Search]] · [[RAG]] · [[Agentic Search]] · [[Search-R1]] · [[Reinforcement Learning for Search]] · [[Vector Filtering]] · [[Text Chunking]] · [[Clean Context]]

## Topics
Practice-oriented guides — how to DO or deal with something in search.

[[Search Quality Assurance]] · [[A-B Testing for Search]] · [[Duality in Measuring Search]] · [[NDCG Variants]] · [[Managing a Search Team]] · [[Understaffed Search Team]] · [[Hiring for Search]] · [[Economics of Search]] · [[E-commerce Search]] · [[Autocomplete and Autosuggest]] · [[Search Result Diversity]] · [[Synonyms and Vocabulary Management]] · [[Query Understanding in Practice]] · [[Multilingual Search]] · [[Relevance Program Setup]] · [[Personalization in Search]] · [[Conversational and Agentic Search]] · [[Spelling Correction in Search]] · [[Vector Search Tradeoffs]] · [[Dimensionality Reduction vs Quantization]] · [[PCA vs t-SNE for Retrieval]] · [[Elasticsearch vs OpenSearch]] · [[Federated vs Unified Search]] · [[Late Interaction in Elasticsearch]] · [[Late Interaction in OpenSearch]] · [[Late Interaction in Qdrant]] · [[Late Interaction in Vespa]] · [[Migration between Search Engines]]

## Tools

[[Quepid]] · [[Search Relevance Workbench]] · [[Elasticsearch Relevance Studio]] · [[Querqy]] · [[Elasticsearch]] · [[OpenSearch]] · [[Solr]] · [[Qdrant Vector DB]] · [[Weaviate Vector DB]] · [[FAISS]] · [[ann-benchmarks]]

## Companies

**Technology Providers**
[[Elastic]] · [[Vespa]] · [[Meta]] · [[Cohere]] · [[OpenSource Connections]] · [[Algolia]] · [[Weaviate]] · [[searchHub]] · [[Empathy]] · [[Sease]] · [[MongoDB]] · [[Voyage AI]] · [[Qdrant]] · [[Hornet]] · [[Amazon Web Services]]

**End Users**
[[Uber]] · [[Airbnb]] · [[Zalando]] · [[Slack]] · [[Canva]] · [[Netflix]] · [[Twitter]] · [[Etsy]] · [[Skyscanner]] · [[Grubhub]] · [[Spotify]] · [[Carousell]] · [[Vinted]] · [[Shopify]] · [[Otto]] · [[Elsevier]]

## Case Studies

[[Uber Eats - Scaling Search for Food Delivery]] · [[Airbnb - ML-Powered Experiences Ranking]] · [[Zalando - Self-DoS via Facet Aggregation]] · [[Slack - Enterprise Message Search with LTR]] · [[Etsy - Search Quality and Query Understanding]] · [[Skyscanner - Learning to Rank for Flights]] · [[Netflix - Content Search Architecture]] · [[Canva - Search Pipeline Modernization]] · [[Vinted - Migrating Search from Elasticsearch to Vespa]] · [[Reddit - Vector Database Selection]] · [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]]

## Videos

Conference talks and recorded presentations.

[[Max Irwin - The Search Engine Migration Circus]] — Haystack Live; search-engine migration playbook, "Hello Search", feature parity, the "damage" metric & war stories

[[Rene Kriegler - Query Relaxation]] — OpenSource Connections; query relaxation as a recommendation problem, comparing heuristic, term-frequency, word2vec and neural approaches to predicting which query term to drop

[[Roman Grebennikov - Personalizing Search Results in Real-Time]] — Findify @ MICES 2019; real-time LTR personalization, position-bias feedback loops, shuffled exploration segments, purchase-weighted perfect rankings

[[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — Qdrant @ MICES 2026; why off-the-shelf [[SPLADE]] misfires on catalogs, the ANCE [[Hard Negative Mining]] loop, full vs inference-free SPLADE, specialize vs generalize

[[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] — Qdrant @ [[Berlin Buzzwords]] 2026; index-native [[Relevance Feedback]] steering [[HNSW]] traversal, distilling a reranker into the index, and the case against black-box search engines

## Key People

[[Daniel Tunkelang]] · [[Doug Turnbull]] · [[James Rubinstein]] · [[Omar Khattab]] · [[Jo Kristian Bergum]] · [[Trey Grainger]] · [[Andreas Wagner]] · [[Giovanni Fernandez-Kincade]] · [[Wolf Garbe]] · [[Eugene Yan]] · [[Andrew Kornilov]]

## Stats
Counted 2026-07-30.

- **306** article notes
- **163** concept notes (incl. Brute-Force Vector Search, Zero-Shot Retrieval, MUVERA, PCA, t-SNE, UMAP, TurboQuant, RaBitQ, BBQ, HNSW, SQ, BQ, Search-R1)
- **52** topic notes (incl. Vector Search Tradeoffs, PCA vs t-SNE for Retrieval, Federated vs Unified Search, Migration between Search Engines, Elasticsearch Learning to Rank, Vespa Learning to Rank, Late Interaction in Vespa, Elasticsearch vs OpenSearch)
- **125** people notes (incl. Roy Keyes, Davit Khachaturyan, Andrew Kornilov, Geoffrey Hinton, Laurens van der Maaten)
- **13** case study notes (incl. Hybrid Fusion Failure - BM25 Displacing Reference Documents, Vinted - Migrating Search from Elasticsearch to Vespa)
- **46** company nodes (incl. Amazon Web Services, Elsevier)
- **33** tool notes (incl. ann-benchmarks, Quepid, Querqy, Elasticsearch, OpenSearch, Solr, Qdrant Vector DB, Weaviate Vector DB, FAISS)
- **7** dataset notes ([[Amazon ESCI Dataset]], [[BEIR]], [[ESCI-S Dataset]], [[Home Depot Product Search Relevance]], [[MS MARCO]], [[SIFT1M]], [[WANDS Dataset]])
- **6** Maps of Content

See [[History]] for the full note-addition log.
