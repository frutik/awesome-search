---
tags:
  - meta
  - history
---
# Awesome Search — Note History

Chronological log of notes added to this knowledge graph. Newest first.

## 2026-06-25 — Search Communities & Women of Search (3 notes)

Added a **community / careers** cluster, distinguishing standing people-networks from the events where they gather. Decision: [[Women of Search]] is a *community*, not a conference — it does not belong under [[Events and Conferences]]/Haystack, so a dedicated [[Search Communities]] hub was created as its parent.

**Topics** — [[Search Communities]] (new hub — identity/mentorship communities, meetups, and Slack/online communities; why communities are the field's learning + hiring pipeline; explicitly distinct from [[Events and Conferences]]), [[Women of Search]] (new — international community for women in search, founded May 2021; mission, core leadership, mentorship program, Haystack talks; sourced from women-of-search.org).

**People** — [[Audrey Lorberfeld]] (new — librarian-turned-software engineer; founder of [[Women of Search]]; AI-driven IR). Seven WoS leadership names ([[Erika Cardenas]], [[Atita Arora]], [[Elzbieta Jakubowska]], [[Meghan Boyd]], [[Olena Gorbatiuk]], [[Samdisha Kapoor]]) left as ready-to-fill wikilinks.

**Updated** — [[Events and Conferences]] frontmatter repair; [[Weaviate]] referenced as employer of WoS core member [[Erika Cardenas]].

---

## 2026-06-23 — Federated Search Concept (1 note)

Added a dedicated concept note for **federated search** in its information-retrieval sense — distributed IR / metasearch — deliberately kept distinct from the "federated *graph*" data-unification sense (Netflix), which is entity modeling rather than a retrieval problem.

**Concepts** — [[Federated Search]] — querying multiple independent collections/engines and merging results; the three sub-problems (resource/collection selection, query routing, results merging), cooperative vs. uncooperative environments, and its relationship to [[Hybrid Search]] (federation over representation spaces vs. over collections).

**Updated** — [[Multilingual Search]] (per-language-index fan-out linked), [[Enterprise Search]] (multi-source retrieval linked), [[Search Architecture]] (Netflix "federated graph" disambiguated), [[Reciprocal Rank Fusion]] (added as the standard merger for fan-out), [[Knowledge Graph Search]] (callout disambiguating federated-graph vs. federated-search) cross-linked into the new note.

---

## 2026-06-22 — Region-Based Embeddings & Generative Retrieval / Semantic IDs (~27 notes)

Two related embedding-geometry clusters. First, the **region-based representation** lineage — words/items as *regions* (boxes, Gaussians, hyperbolic balls) rather than points — and its search payoff for set-theoretic/compositional queries. Second, the **generative retrieval** cluster — discrete [[Semantic IDs]] as the identifier scheme behind sequence-to-sequence retrieval, anchored to its IR-native origin [[Differentiable Search Index]] rather than framed as pure recsys.

**Articles** — [[Express Words in a Box - Understanding Box Embedding from the Basics]] (by [[Shun Tsukagoshi]], Behitek / *State of AI Guide*, 2022-12-16; paywalled — processed from supplied text). From-the-basics tutorial on box embeddings as a [[Region-Based Representation]], walking the lineage from point embeddings to [[Word2Box]]. [[Answering Compositional Queries with Set-Theoretic Embeddings]] (by [[Shib Sankar Dasgupta]], [[Andrew McCallum]], [[Steffen Rendle]], [[Li Zhang]], arXiv:2306.04133, 2023-06-07). The search/IR payoff of box embeddings — representing item–attribute relations as "learnable Venn diagrams" answers AND/OR/NOT [[Compositional Queries]] better than dot-product vectors. [[Semantic IDs for Recommendation Systems]] (by [[Janu Verma]], *Incomplete Distillation*, 2025-08-04). Hands-on build of [[Semantic IDs]] from vector quantization through [[RQ-VAE]], reproducing a [[TIGER]]-style generative pipeline on Amazon Beauty.

**Concepts** — region-based family: [[Box Embedding]], [[Region-Based Representation]], [[Gaussian Embedding]], [[Poincaré Embedding]], [[Word2Box]], [[Set-Theoretic Embeddings]], [[Compositional Embeddings]], [[Compositional Queries]]. Generative-retrieval family: [[Generative Retrieval]], [[Differentiable Search Index]], [[Semantic IDs]], [[RQ-VAE]], [[TIGER]]. Foundations & interpretability: [[Word2Vec]], [[Concept Vectors]], [[Steering Vectors]].

**People** — [[Shib Sankar Dasgupta]] (Word2Box / set-theoretic embeddings lead author), [[Andrew McCallum]] (UMass; box-embedding line), [[Steffen Rendle]] and [[Li Zhang]] (compositional-queries co-authors), [[Luke Vilnis]] (box/order embeddings), [[Shun Tsukagoshi]] (Nagoya; box-embedding tutorial), [[Tomas Mikolov]] (Word2Vec), [[Janu Verma]] (*Incomplete Distillation*; semantic IDs).

**Updated** — [[Embeddings]], [[Dense Embeddings]], [[Faceted Search]], [[Vector Quantization]] cross-linked into the two new clusters.

---

## 2026-06-19 — Frontier-of-Search Period Pages & Late Interaction in Elasticsearch (~4 notes)

Made the "frontier" concept year-anchored and processed [[Elastic]]'s two-part ColPali series into a dedicated topic.

**Topics** — [[Frontier of Search]] (new year-by-year index/TOC linking each period page), [[Frontier of Search 2025]] (new period page — late interaction goes multimodal & production-scale, embeddings as a commodity, vector quantization/ANN engineering, the keyword-efficiency renaissance, and the first RL/agentic seeds), [[Late Interaction in Elasticsearch]] (new — `rank_vectors` + `maxSimDotProduct` in ES 8.18, bit/average vectors, [[Token Pooling]], two-stage rescore).

**Articles** — [[ColPali & Elasticsearch - How to Search Complex Documents]] (by [[Peter Straßer]] at [[Elastic]], 2025-03-16). Part 1 of the ColPali series — what [[ColPali]] is, the ViDoRe benchmark, the `rank_vectors` field, and `maxSimDotProduct` scoring. (Part 2, [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]], already existed.)

**Renamed** — "Current Frontier of Search" → [[Frontier of Search 2026]] (future-proofing; all 25 wikilinks + frontmatter references updated). Dropped the now-ambiguous "Frontier of Search" alias since it is now a real index note.

**Updated** — [[Late Interaction]], [[ColPali]], [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]], [[Peter Straßer]], [[Frontier of Search 2026]] cross-linked into the new cluster; [[index|index.md]] Topics + Stats refreshed.

---

## 2026-06-18 (evening) — Agentic Search Frontier & Reasoning Reranking (~14 notes)

Built out the "agents as the new user of search" cluster, spanning purpose-built retrieval models, the agentic query workload, and the shift of reranking toward LLMs.

**Articles** — [[Agentic Search Models with OpenSearch and Elasticsearch]] (by [[Bonsai]], 2026-06-05). Hands-on integration of the [[SID-1]] model into a managed OpenSearch cluster as a drop-in relevance layer; tool-based rewrite/retrieve/rerank loop. [[The Scaling Dimensions of Keyword Search]] (by [[Skip Everling]] at [[Hornet]], 2026-02-06). Benchmark arguing document count is only one scaling dimension — query length and structure matter too, and [[Block-Max WAND]] pruning can fall *below* exhaustive scoring on the long queries agents emit.

**Concepts** — [[Purpose-Built Agentic Search Models]] (LLMs trained specifically on the rewrite/retrieve/rerank loop — smaller/faster/cheaper than frontier models on domain retrieval), [[Agentic Query Workload]] ("agents are the new user of search" — long, structured, high-volume, out-of-distribution queries that strain serving infrastructure), [[RankGPT]] (listwise LLM reranker, sliding-window permutation, no fine-tuning), [[RankLLaMA]] (stub — LLaMA-based pointwise reranker), [[MonoT5]] (stub — T5 pointwise seq2seq reranker).

**Companies** — [[Bonsai]] (managed OpenSearch/Elasticsearch hosting), [[SID.ai]] (purpose-built agentic search/reranking models).

**Tools** — [[SID-1]] ([[SID.ai]]'s first agentic retrieval model; OpenAI-compatible API; ~1.9× over embedding-only search, ~24× faster than frontier agentic retrieval).

**People** — [[Skip Everling]] ([[Hornet]]; retrieval infrastructure for agentic workloads).

**Topics** — [[Frontier of Search 2026]] (agents as first-class search users — converging product and research fronts), [[Reasoning Reranking]] (LLMs as rerankers: prompted, fine-tuned, or chain-of-thought), [[RL-Trained Search Agents]] (training the searcher policy with RL — complement to purpose-built models).

**Updated** — [[This Is What Agentic Retrieval Looks Like]], [[When Reranking Becomes a System Boundary]], [[Agentic Search]], [[Reranking]], [[Block-Max WAND]], [[Direct Corpus Interaction]], [[Reinforcement Learning for Search]], [[Search-R1]], [[Doug Turnbull]], [[Vespa]], [[Conversational and Agentic Search]], [[MOC - Agentic Search and Embeddings]] cross-linked into the frontier cluster.

---

## 2026-06-18 (afternoon) — Career & Learning Paths (~2 notes)

Added entry-point topics for people getting into search and curated learning resources.

**Topics** — [[How to Start a Career in Search]] (learning path + the people, books, courses, and communities to follow), [[Courses]] (IR/search training and course resources).

**Updated** — [[Books]], [[Events and Conferences]], [[Hiring for Search]], [[Search Consultancy]], [[Trey Grainger]], [[OpenSource Connections]] cross-linked into the career/learning cluster.

---

## 2026-06-18 — Search Problem Archetypes (~4 notes)

Processed [[Atita Arora]]'s archetype article into a new **Topic** hub. Decision: this article earned a dedicated topic note — it is a self-slotting diagnostic taxonomy spanning ten domains, not a single concept.

**Topics** — [[Search Problem Archetypes]] — the 10 recurring search-problem patterns (Uniqueness, Complexity Machine, Precision Mandate, Firehose, Extraction, Media Vault, Knowledge Graph, Geospatial, Q-commerce, Code Search); diagnosis-before-solution framing (Ackoff); "same symptom, opposite prescription" ([[Zero Results]]); agentic retrieval as a consumption pattern, not an archetype.

**Articles** — [[Before You Fix Your Search, Know What's Actually Broken]] (by [[Atita Arora]], Unscripted AI Substack, 2026-06-16). Argues most search failures are misdiagnoses — teams solve the wrong problem (and skip defining relevance / [[Judgment Lists|judgment lists]]) before reaching for LTR or vectors.

**People** — [[Atita Arora]] (search relevance consultant; Unscripted AI), [[Udi Manber]] (search leader at Amazon/Yahoo/Google/YouTube; "search is essentially a solved problem" misperception).

**Updated** — [[Zero Results]] and [[Agentic Search]] cross-linked to [[Search Problem Archetypes]]; [[index|index.md]] Topics/People/Stats refreshed.

---

## 2026-06-16 — Ranking Objectives & LTR Cluster (~10 notes)

Expanded the [[Ranking Objectives]] stub into a full concept note from Clippings sources: the three families (pointwise / pairwise / listwise), the objective-encodes-business-goals framing, the LambdaMART lambda-swap bridge from pairwise training to a listwise metric, and a per-library objective table ([[LightGBM]] / [[XGBoost]] / [[CatBoost]]).

**Articles** — [[Pointwise vs Pairwise vs Listwise Learning to Rank]] (by [[Nikhil Dandekar]], Medium, 2016-09-29). Canonical taxonomy of LTR approaches by how many documents the loss considers; names RankNet/LambdaRank/LambdaMART (pairwise) and SoftRank/AdaRank/ListNet/ListMLE (listwise).

[[LambdaMART Explained - The Workhorse of Learning-to-Rank]] (by [[Tullie Murrell]] at [[Shaped]], 2025-07-30). RankNet → LambdaRank → LambdaMART lineage, the boosting loop, advantages/limits, library objective strings. [[Learning to Rank - A Complete Guide to Ranking using Machine Learning]] (by [[Francesco Casalegno]], TDS, 2022-02-28). Full objective landscape — MAP/NDCG metrics, pointwise/pairwise/listwise, SoftRank, ListNet, and the [[LambdaLoss]] generalization. [[Building a Large-Scale Recommendation System - People You May Know]] ([[LinkedIn]] Engineering, 2024-02-06). Production multi-stage funnel (L0 recall → L1 light ranker → L2 rich ranker → fairness/diversity re-ranker).

**Concepts** — [[LambdaLoss]] (stub) — generalized listwise framework unifying RankNet/LambdaRank/SoftRank/ListNet.

**People** — [[Nikhil Dandekar]] (search / LTR / NLP practitioner), [[Tullie Murrell]] ([[Shaped]]), [[Francesco Casalegno]] (LTR writer).

**Companies** — [[LinkedIn]], [[Shaped]].

**Updated** — [[Ranking Objectives]] promoted from stub to full note (three families, business-goal framing, lambda-swap bridge, per-library objective table, LambdaLoss); [[LambdaMART]] cross-linked to the two new LTR articles.

---

## 2026-06-13 — Elasticsearch In-Engine LTR (~6 notes)

Filled the Elasticsearch-internal side of the LTR cluster, complementing the existing external/[[Metarank]] coverage.

**Concepts** — [[Elasticsearch Learning to Rank]] — hub note covering two distinctions: external re-ranker (Metarank) vs. in-engine LTR, and the two ES modules — the [[OpenSource Connections]] plugin (RankLib-based, 2017) vs. Elastic **native** LTR (8.12+, GBDT/XGBoost via [[eland]]).

**Articles** — [[We're Bringing Learning to Rank to Elasticsearch]] (by [[OpenSource Connections]] / [[Doug Turnbull]], 2017-02-14). Launch of the o19s `elasticsearch-learning-to-rank` plugin; integrates [[RankLib]]; custom `ltr` query + `ranklib` script; applied via `rescore`. [[Learning To Rank (LTR) - Elasticsearch Native]] (Elastic docs). Native LTR overview — judgment lists, three feature categories, `query_extractor` templated features, GBDT/LambdaMART inference with training outside ES. [[Search using LTR - Elastic Docs]] (Elastic docs). Applying a deployed model as a `learning_to_rank` rescorer (8.12+) or `rescorer` retriever (9.1+); mandatory `window_size`.

**Tools** — [[eland]] — Elastic's Python client; uploads the trained XGBoost ranker into Elasticsearch for native LTR inference.

**Updated** — [[Learning to Rank]], [[Metarank]], [[Elasticsearch]], [[RankLib]], [[OpenSource Connections]], [[MOC - Ranking and Retrieval]] cross-linked to the new cluster.

---

## 2026-06-12 — PostgreSQL Search Extensions (~7 notes)

**Concepts** — [[Search Results Explainability]] (ability to reason about and explain why documents rank as they do), [[Learned Sparse Retrieval]] (family of models learning term weights for sparse retrieval — SPLADE, ELSER, etc.).

**Tools** — [[pg_trgm]] (PostgreSQL built-in trigram similarity extension for fuzzy text search), [[pg_textsearch]] ([[BM25]] for PostgreSQL by [[Tiger Data]]), [[pgvectorscale]] (high-performance ANN vector search extension for PostgreSQL by [[Tiger Data]]), [[VectorChord]] (PostgreSQL vector search extension by TensorChord).

**Companies** — [[Tiger Data]] (formerly Timescale; builds PostgreSQL-native search and vector search extensions).

---

## 2026-06-11 — Metarank / LTR Cluster (~8 notes)

**Articles** — [[Hybrid Search and Learning-to-Rank with Metarank]] (by [[Vsevolod Goloviznin]], Pinecone blog, 2023-06-30). Fusing BM25 + vector retrievers via [[LambdaMART]] as a statistically-valid fusion mechanism; cold-start via [[Interleaving]]. [[Learn-to-Rank with OpenSearch and Metarank]] (by [[Roman Grebennikov]], OpenSearch blog, 2022-10-25). LambdaMART secondary re-ranking on top of [[OpenSearch]]; multi-stage ranking pattern; Remote Ranker Plugin RFC. [[Metarank - Personalized Ranking That Actually Reads Your Clicks]] (by [[Florian Narr]], Codeline, 2025-12-15). Code-level repo review of Metarank's Scala/fs2 architecture (FeatureMapping, MetarankFlow, RankApi). [[OpenSearch vs. Elasticsearch in 2025 - What's Changed and What Hasn't]] (Dattell, 2025-04-03). Balanced licensing/features comparison (SSPL vs. Apache 2.0, plugin incompatibility, performance differences, ecosystem divergence).

**Tools** — [[Metarank]] — open-source [[LambdaMART]] re-ranker and personalization service (Scala + Redis) by [[Roman Grebennikov]] and [[Vsevolod Goloviznin]].

**People** — [[Roman Grebennikov]] (Metarank co-creator), [[Vsevolod Goloviznin]] (Metarank co-creator, Pinecone author), [[Florian Narr]] (Codeline author).

---

## 2026-06-02 — Block-Max WAND Cluster (~7 notes)

**Articles** — [[WAND and Block-Max WAND - Efficient Algorithms for Top-k Document Retrieval]] ([[Jithendrasaikilaru]], Medium, 2025-10-31). Paywalled; content from public summary. Introductory overview of dynamic pruning for top-k retrieval, covering WAND (Broder et al. 2003), Block-Max WAND (Ding & Suel 2011), MaxScore lineage, and DAAT context. [[BlockMax WAND - How Weaviate Achieved 10x Faster Keyword Search]] (by [[André Mourão]] and [[Joon-Pil (JP) Hwang]], [[Weaviate]] blog, 2025-02-26). Technical implementation in Weaviate v1.29 (technical preview): 5–10× p50 latency speedup over plain WAND, 50–91% index size reduction via variable-length block encoding and delta compression of doc IDs; MS MARCO and Fever benchmark results. [[Faster Retrieval of Top Hits in Elasticsearch with Block-Max WAND]] (by [[Adrien Grand]], Elastic blog, 2019-02-05). Original integration into Lucene 8.0 / Elasticsearch 7.0; lineage from MAXSCORE (1995) through WAND (2003); 3×–15× speedup; breaking API changes (non-negative scores, approximate hit counts via `track_total_hits`).

**People** — [[Jithendrasaikilaru]] (Medium writer, IR/AI/cybersecurity), [[André Mourão]] ([[Weaviate]]), [[Joon-Pil (JP) Hwang]] ([[Weaviate]]), [[Adrien Grand]] ([[Elastic]], core Lucene committer).

**Updated** — [[WAND]], [[Block-Max WAND]] concept notes linked to new articles.

---

## 2026-06-01 — History Audit & Comprehensive Catch-Up (~212 notes)

Catch-up log — notes present in the vault but not individually recorded in prior entries (initial import, May 16 batch, and later additions). Also includes post-catchup articles added later the same day.

**Articles** — [[RRF is Not Enough]] (by [[Doug Turnbull]], 2024-11-03), [[Agentic search models]] (by [[Doug Turnbull]], 2026-05-11), [[Agents turn simple keyword search into compelling search experiences]] (by [[Doug Turnbull]]), [[Beyond Semantic Similarity - Rethinking Retrieval for Agentic Search via Direct Corpus Interaction]] (TIGER-Lab, 2026-05-08), [[Superintelligent Retrieval Agent SIRA]] (Meta / Rice University, 2026), [[You Say Search I Say Recs - Spotify Agentic Query Understanding]] (Spotify Research, 2025), [[Qwen3 Embedding Series]] (Alibaba Qwen Team, 2025-06-05), [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]], [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] (by [[Aparna Dhinakaran]], 2025-08-20), [[Incremental AI Adoption for E-commerce Search]] (2026-01-18), [[On Search Leadership]] (by [[Daniel Tunkelang]]), [[Canva Search Pipeline Part I]], [[Bayesian BM25 is Cool]], [[Can BM25 be a Probability]], [[Broad and Ambiguous Search Queries]], [[Click Residual - A Query Success Metric]], [[Deconstructing E-Commerce Search - The 12 Query Types]], [[Diversity Metrics for Recommender Systems]], [[Ecommerce Search Governance - Move Faster Not Slower]], [[How Context-Aware Embeddings Are Transforming Enterprise Search]], [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]], [[LLM-Powered Query Extraction for Autocomplete]], [[Metadata - The 3rd Kind of Retrieval]], [[Mirror Mirror - All About Search Suggestions]], [[Mutually Assured Distraction]], [[My Journey Building Elasticsearch for Retail]], [[Patterns for Personalization]], [[Probability-Proportional-to-Size Sampling for Relevance Evaluation]], [[Real Talk About Synonyms and Search]], [[Searching for Goldilocks]], [[Session vs Query based Search Evals]], [[Statistical and Human-Centered Approaches to Search Improvement]], [[Three Pillars of Search Quality - Findability]], [[Three Pillars of Search Quality - Discovery and Inspiration]], [[Autosuggest Ranking]], [[Autosuggest Retrieval Data Structures and Algorithms]].

**Post-catchup articles (same day)** — [[SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs]] (by [[QvickRead]], Medium, 2025-03-19). RL-based multi-turn search framework; token-level loss masking; PPO and GRPO training; +10–26% on QA benchmarks. [[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]] (by [[Lakshmi Devi Prakash]], Medium, 2025-04-11). Accessible comparison of RAG vs. Search-R1 architectures. [[Observability for AI Workloads A New Paradigm for a New Era]] (by [[Dotan Horovits]], 2026). Observability patterns for AI/search workloads; OpenTelemetry framing. [[Elasticsearch vs. OpenSearch (2025) The Definitive Showdown]] (by [[Jagadeesh Chandra]], Medium). ES vs. OS feature/ecosystem comparison. [[OpenSearch vs. Elasticsearch A Comprehensive Comparison in 2025]] (by [[Frank Goortani]], Medium). Balanced architecture and licensing comparison. Plus 7 dimensionality reduction articles: [[t-SNE Clearly Explained]] ([[Kemal Erdem]]), [[t-SNE Explained - Math and Intuition]] ([[Achinoam Soroker]]), [[t-SNE Explained - Visualising High-Dimensional Data]] ([[Billy Chan]]), [[PCA vs t-SNE - Which One Should You Use for Visualization]] ([[Namratesh Shrivastav]]), [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] ([[Lakhan Bukkawar]]), [[Understanding Principal Component Analysis (PCA)]] ([[Roshmita Dey]]), [[Principal Component Analysis (PCA) In Depth]] ([[Fraidoon Omarzai]]).

**New Section — Case Studies** (9 notes) — [[Airbnb - ML-Powered Experiences Ranking]], [[Canva - Search Pipeline Modernization]], [[Etsy - Search Quality and Query Understanding]], [[Kleinanzeigen - Vespa Migration for Homepage Feed]], [[Netflix - Content Search Architecture]], [[Skyscanner - Learning to Rank for Flights]], [[Slack - Enterprise Message Search with LTR]], [[Uber Eats - Scaling Search for Food Delivery]], [[Zalando - Self-DoS via Facet Aggregation]]. Structured use-case notes synthesising engineering lessons from each company's published work.

**New Section — Datasets** (4 notes) — [[Amazon ESCI Dataset]], [[ESCI-S Dataset]], [[Home Depot Product Search Relevance]], [[WANDS Dataset]]. Benchmark datasets for search relevance evaluation.

**Concepts** — [[Bag-of-Documents Model]], [[Clean Context]], [[Click Signals]], [[Direct Corpus Interaction]], [[GGUF]], [[Hit Rate at K]], [[Intent Drift]], [[IVF]], [[LoRA]], [[PEFT]], [[QLoRA]], [[SIRA]], [[Session-Based Evaluation]], [[Task-Aware Embeddings]], [[Token Pooling]], [[UDCG]], [[WAND]], [[UMAP]], [[Search Observability]], [[PCA]], [[t-SNE]], [[Reinforcement Learning for Search]], [[Search-R1]].

**People** — [[Omar Khattab]] (Stanford, ColBERT author), [[Aparna Dhinakaran]] (Arize AI), [[Thibault Formal]] (SPLADE co-author), [[Stéphane Clinchant]] (SPLADE co-author), [[Antoine Chaffin]], [[Florent Krzakala]], [[Han Xiao]] (Jina AI), [[James Briggs]], [[Shaw Talebi]], [[Matei Zaharia]] (Databricks / MLflow), [[Laura Ham]] (Weaviate), [[Marianne Haugvaldstad]], [[Lester Solbakken]], [[Brage Vik]], [[Rudolf Batt]], [[Nicolò Rinaldi]], [[Luca Arnaboldi]], [[Hugo Galvão]], [[Honza Král]], [[Jodi Sloan]], [[Michael Ryaboy]], [[Michael Hannecke]], [[Peter Straßer]], [[Siegfried Schüle]], [[Andrea Schütt]], [[Andreas Wagner]], [[Alexander Marquardt]], [[Amélie Chatelain]], [[Asif Makhani]], [[Benjamin Trent]], [[Dai Sugimori]], [[Daniel Doro]], [[David Argüello Sánchez]], [[Dima Kan]], [[Dmitriy Meyerzon]], [[Jaideep Ray]], [[Maryna Kryvko]], [[Prateek Chandra Jha]], [[Ravindra Harige]], [[Taylor Roy]], [[Trey Grainger]], [[Jagadeesh Chandra]], [[Frank Goortani]], [[Shay Banon]] (Elasticsearch creator), [[Dotan Horovits]] (observability), [[Lakshmi Devi Prakash]], [[QvickRead]], [[Kemal Erdem]], [[Achinoam Soroker]], [[Billy Chan]], [[Namratesh Shrivastav]], [[Lakhan Bukkawar]], [[Roshmita Dey]], [[Fraidoon Omarzai]], [[Geoffrey Hinton]] (t-SNE co-creator), [[Laurens van der Maaten]] (t-SNE co-creator), [[Chris Fournie]] (Reddit), [[Ritik Jain]], [[Venkat Ram Rao]], [[Freddy Domínguez]].

**Companies** — [[Empathy]], [[Jina AI]], [[LightOn AI]], [[Meta]], [[Sease]], [[searchHub]], [[Shopify]], [[Reddit]].

**Topics** — [[Elasticsearch vs OpenSearch]], [[Multilingual Search]], [[Personalization in Search]], [[Relevance Program Setup]], [[Search Platforms]], [[Search UX]], [[Spelling Correction in Search]].

**Tools** — [[OpenSearch]], [[Milvus Vector DB]].

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
| 2026-06-25 | 3 | ~598 |
| 2026-06-23 | 1 | ~595 |
| 2026-06-22 | ~27 | ~594 |
| 2026-06-19 | ~4 | ~567 |
| 2026-06-18 (evening) | ~14 | ~563 |
| 2026-06-18 (afternoon) | ~2 | ~549 |
| 2026-06-18 (archetypes) | ~4 | ~547 |
| 2026-06-16 | ~10 | ~543 |
| 2026-06-13 | ~6 | ~533 |
| 2026-06-12 | ~7 | ~527 |
| 2026-06-11 | ~8 | ~520 |
| 2026-06-02 | ~7 | ~512 |
| 2026-06-01 | ~212 | ~505 |
| 2026-05-31 | ~20 | ~293 |
| 2026-05-28 | 1 | ~273 |
| 2026-05-26 | 2 | ~272 |
| 2026-05-19 | ~9 | ~270 |
| 2026-05-17 | ~12 | ~261 |
| 2026-05-16 | ~49 | ~249 |
| 2026-05-15 | ~200 | ~200 |

See [[All about Information Retrieval & Search]] for current vault totals.
