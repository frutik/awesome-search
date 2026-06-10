---
tags:
  - meta
  - history
---
# Awesome Search — Note History

Chronological log of notes added to this knowledge graph. Newest first.

## 2026-06-01 — History Audit & Comprehensive Catch-Up (~175 notes)
## 2026-06-02 — WAND & Block-Max WAND Article (2 notes)

**Articles** — [[WAND and Block-Max WAND - Efficient Algorithms for Top-k Document Retrieval]] ([[Jithendrasaikilaru]], Medium, 2025-10-31). Paywalled; content from public summary. Introductory overview of dynamic pruning algorithms for top-k retrieval, covering WAND (Broder et al. 2003), Block-Max WAND (Ding & Suel 2011), MaxScore lineage, and DAAT context.

**People** — [[Jithendrasaikilaru]] (Medium writer, IR/AI/cybersecurity).

**Updated** — [[WAND]], [[Block-Max WAND]] concept notes linked to new article.


Catch-up log — notes present in the vault but not individually recorded in prior entries (initial import, May 16 batch, and later additions).

**Articles** — [[RRF is Not Enough]] (by [[Doug Turnbull]], 2024-11-03), [[Agentic search models]] (by [[Doug Turnbull]], 2026-05-11), [[Agents turn simple keyword search into compelling search experiences]] (by [[Doug Turnbull]]), [[Beyond Semantic Similarity - Rethinking Retrieval for Agentic Search via Direct Corpus Interaction]] (TIGER-Lab, 2026-05-08), [[Superintelligent Retrieval Agent SIRA]] (Meta / Rice University, 2026), [[You Say Search I Say Recs - Spotify Agentic Query Understanding]] (Spotify Research, 2025), [[Qwen3 Embedding Series]] (Alibaba Qwen Team, 2025-06-05), [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]], [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] (by [[Aparna Dhinakaran]], 2025-08-20), [[Incremental AI Adoption for E-commerce Search]] (2026-01-18), [[On Search Leadership]] (by [[Daniel Tunkelang]]), [[Canva Search Pipeline Part I]], [[Bayesian BM25 is Cool]], [[Can BM25 be a Probability]], [[Broad and Ambiguous Search Queries]], [[Click Residual - A Query Success Metric]], [[Deconstructing E-Commerce Search - The 12 Query Types]], [[Diversity Metrics for Recommender Systems]], [[Ecommerce Search Governance - Move Faster Not Slower]], [[How Context-Aware Embeddings Are Transforming Enterprise Search]], [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]], [[LLM-Powered Query Extraction for Autocomplete]], [[Metadata - The 3rd Kind of Retrieval]], [[Mirror Mirror - All About Search Suggestions]], [[Mutually Assured Distraction]], [[My Journey Building Elasticsearch for Retail]], [[Patterns for Personalization]], [[Probability-Proportional-to-Size Sampling for Relevance Evaluation]], [[Real Talk About Synonyms and Search]], [[Searching for Goldilocks]], [[Session vs Query based Search Evals]], [[Statistical and Human-Centered Approaches to Search Improvement]], [[Three Pillars of Search Quality - Findability]], [[Three Pillars of Search Quality - Discovery and Inspiration]], [[Autosuggest Ranking]], [[Autosuggest Retrieval Data Structures and Algorithms]].

**New Section — Case Studies** (9 notes) — [[Airbnb - ML-Powered Experiences Ranking]], [[Canva - Search Pipeline Modernization]], [[Etsy - Search Quality and Query Understanding]], [[Kleinanzeigen - Vespa Migration for Homepage Feed]], [[Netflix - Content Search Architecture]], [[Skyscanner - Learning to Rank for Flights]], [[Slack - Enterprise Message Search with LTR]], [[Uber Eats - Scaling Search for Food Delivery]], [[Zalando - Self-DoS via Facet Aggregation]]. Structured use-case notes synthesising engineering lessons from each company's published work.

**New Section — Datasets** (4 notes) — [[Amazon ESCI Dataset]], [[ESCI-S Dataset]], [[Home Depot Product Search Relevance]], [[WANDS Dataset]]. Benchmark datasets for search relevance evaluation.

**Concepts** — [[Bag-of-Documents Model]], [[Clean Context]], [[Click Signals]], [[Direct Corpus Interaction]], [[GGUF]], [[Hit Rate at K]], [[Intent Drift]], [[IVF]], [[LoRA]], [[PEFT]], [[QLoRA]], [[SIRA]], [[Session-Based Evaluation]], [[Task-Aware Embeddings]], [[Token Pooling]], [[UDCG]], [[WAND]].

**People** — [[Omar Khattab]] (Stanford, ColBERT author), [[Aparna Dhinakaran]] (Arize AI), [[Thibault Formal]] (SPLADE co-author), [[Stéphane Clinchant]] (SPLADE co-author), [[Antoine Chaffin]], [[Florent Krzakala]], [[Han Xiao]] (Jina AI), [[James Briggs]], [[Shaw Talebi]], [[Matei Zaharia]] (Databricks / MLflow), [[Laura Ham]] (Weaviate), [[Marianne Haugvaldstad]], [[Lester Solbakken]], [[Brage Vik]], [[Rudolf Batt]], [[Nicolò Rinaldi]], [[Luca Arnaboldi]], [[Hugo Galvão]], [[Honza Král]], [[Jodi Sloan]], [[Michael Ryaboy]], [[Michael Hannecke]], [[Peter Straßer]], [[Siegfried Schüle]], [[Andrea Schütt]], [[Andreas Wagner]], [[Alexander Marquardt]], [[Amélie Chatelain]], [[Asif Makhani]], [[Benjamin Trent]], [[Dai Sugimori]], [[Daniel Doro]], [[David Argüello Sánchez]], [[Dima Kan]], [[Dmitriy Meyerzon]], [[Jaideep Ray]], [[Maryna Kryvko]], [[Prateek Chandra Jha]], [[Ravindra Harige]], [[Taylor Roy]], [[Trey Grainger]].

**Companies** — [[Empathy]], [[Jina AI]], [[LightOn AI]], [[Meta]], [[Sease]], [[searchHub]], [[Shopify]].

**Topics** — [[Elasticsearch vs OpenSearch]], [[Multilingual Search]], [[Personalization in Search]], [[Relevance Program Setup]], [[Search Platforms]], [[Search UX]], [[Spelling Correction in Search]].

**Tools** — [[OpenSearch]].

---

## 2026-05-31 — LLM Judges, Agentic Retrieval & Bias Concepts (~20 notes)

**Articles** — [[Classic ML to Cope with Dumb LLM Judges]] (by [[Doug Turnbull]], published 2025-01-21), [[What AI Engineers Should Know about Search]] (by [[Doug Turnbull]], published 2024-06-25), [[Search Quality Assurance with AI as a Judge]] (by [[Tao Ruangyam]] at [[Zalando]], published 2026-03-17), [[This Is What Agentic Retrieval Looks Like]] (by [[Jo Kristian Bergum]] at [[Hornet]], published 2026-05-20), [[Agentic Search for Context Engineering]] (by [[Leonie Monigatti]] at [[Elastic]], published 2026-05-27).

**Concepts** — [[LLM as Judge]], [[Pointwise Relevance Evaluation]], [[Pairwise Relevance Evaluation]], [[Listwise Relevance Evaluation]], [[Position Bias]], [[Presentation Bias]], [[Relevance Feedback]], [[Context Engineering]].

**Companies** — [[Hornet]] (agentic retrieval infrastructure), [[Zalando]] (European fashion e-commerce).

**People** — [[Jo Kristian Bergum]] (Hornet co-founder, former Vespa AI Chief Scientist), [[Tao Ruangyam]] (Zalando search engineering), [[Leonie Monigatti]] (Elastic developer advocate).

**Topics** — [[Search Quality Assurance]] and [[Conversational and Agentic Search]] expanded.

---

## 2026-05-28 — Topic Expansion (1 note)

**Topics** — [[Enterprise Search]] — new topic page covering enterprise-specific search challenges, internal knowledge bases, and vendor landscape.

---

## 2026-05-26 — Recent Articles (2 notes)

**Articles** — [[When Reranking Becomes a System Boundary]] (by [[Ravindra Harige]], published 2026-05-25), [[From Elasticsearch to Vespa - Rebuilding the Kleinanzeigen Homepage Feed Part 1]] (by [[Andre Charton]] at [[Kleinanzeigen]], published 2026-05-22).

---

## 2026-05-19 — Tools, Vector DBs & Hybrid Search (~9 notes)

**Tools** — [[Elasticsearch]], [[Qdrant Vector DB]], [[Weaviate Vector DB]].

**Companies** — [[MongoDB]], [[Voyage AI]].

**Concepts** — [[Semantic Boosting]], [[Relative Score Fusion]].

**People** — [[Erik Hatcher]] (MongoDB).

**Articles** — [[Hybrid Search Blueprint Series Semantic Boosting]].

---

## 2026-05-17 — Consultancy, Tools & Niche Topics (~12 notes)

**People** — [[Charlie Hull]] (The Search Juggler, 25+ years in search).

**Tools** — [[Querqy]] (query rewriting library), [[Quepid]] (search relevance evaluation platform).

**Companies** — [[The Search Juggler]].

**Concepts** — [[Signal Downboosting]].

**Topics** — [[Understaffed Search Team]], [[Search Consultancy]], [[Events and Conferences]], [[Fun and Philosophy]], [[Books]].

**Articles** — [[Your Obsidian Vault Is a Knowledge Graph]], [[Getting Started on Search Relevance for the Understaffed Search Team]].

---

## 2026-05-16 — Concepts, Companies & Topics Expansion (~49 notes)

**Concepts** — [[BERT]], [[Reranking]], [[TurboQuant]], [[RaBitQ]], [[Query Expansion]], [[Collocations]], [[Stopwords]], [[Clicks Residual]], [[MMR]], [[APD]], [[Linear Score Combination]], [[Modality Gap]], [[Contrastive Gap]], [[Conversational Search]], [[Knowledge Distillation]], [[Dimensionality Reduction]], [[Click Models]], [[Query Sampling]].

**Companies** — [[Qdrant]], [[Netflix]], [[Canva]], [[Carousell]], [[Etsy]], [[Twitter]], [[Spotify]], [[OpenSource Connections]], [[Skyscanner]], [[Grubhub]], [[Cohere]].

**Topics** — [[A-B Testing for Search]], [[Economics of Search]], [[E-commerce Search]], [[Autocomplete and Autosuggest]], [[Synonyms and Vocabulary Management]], [[Query Understanding in Practice]], [[Managing a Search Team]], [[Search Quality Assurance]], [[Search Result Diversity]], [[Hiring for Search]].

**People** — [[Ivan Pleshkov]], [[Jonas Schulz]] (Qdrant engineers), [[Neal Lathia]] (Skyscanner), [[Stuart Cam]] (Canva), [[Hassam Chundrigar]] (Daraz), [[Isabella Tromba]] (Slack), [[Mihajlo Grbovic]] (Airbnb), [[Sergey Feldman]] (AI2).

**Articles** — [[TurboQuant in Qdrant]].

---

## 2026-05-15 — Initial Import (~200+ notes)

The founding batch. Core articles, concept definitions, MOCs, and key people were imported from the [Awesome Search](https://github.com/frutik/awesome-search) curated list.

**Articles** — full Query Understanding series ([[Query Understanding - Introduction]] through all sub-topics by [[Daniel Tunkelang]]), ranking articles ([[Multi-Stage Ranking]], [[Compute Mean Reciprocal Rank (MRR) using Pandas]]), embedding articles ([[Hypothetical Document Embeddings (HyDE)]], [[Fine-tuning Multimodal Embedding Models]]), and many more.

**Concepts** — foundational IR concepts: [[BM25]], [[Reciprocal Rank Fusion]], [[Hybrid Search]], [[Synonyms]], [[Bayesian BM25]], [[Knowledge Graph Search]], [[Query Understanding]], [[Autocomplete]], [[Faceted Search]], [[Spelling Correction]], [[Embeddings]], [[Learning to Rank]], [[NDCG]], [[MRR]], [[RAG]], and many others.

**MOCs** — 6 Maps of Content created: [[MOC - Search UX and Discovery]], [[MOC - Ranking and Retrieval]], [[MOC - Agentic Search and Embeddings]], [[MOC - Search Quality Assurance and Query Understanding]], [[MOC - Architecture and Search Team]].

**People** — [[Daniel Tunkelang]], [[Doug Turnbull]], [[James Rubinstein]], [[Giovanni Fernandez-Kincade]], [[Wolf Garbe]], [[Eugene Yan]], [[Piotr Mazurek]], [[Karthik Ramasamy]], [[Janani Narayanan]], [[Thomas Veasey]], [[Quynh Nguyen]], [[David Albrecht]], [[Max Irwin]], [[Ted Underwood]], and others.

---

## Stats Over Time

| Date | Notes Added | Running Total (approx.) |
|------|------------|------------------------|
| 2026-06-01 | ~175 | ~468 |
| 2026-05-31 | ~20 | ~293 |
| 2026-05-28 | 1 | ~273 |
| 2026-05-26 | 2 | ~272 |
| 2026-05-19 | ~9 | ~270 |
| 2026-05-17 | ~12 | ~261 |
| 2026-05-16 | ~49 | ~249 |
| 2026-05-15 | ~200 | ~200 |

See [[All about Information Retrieval & Search]] for current vault totals.
