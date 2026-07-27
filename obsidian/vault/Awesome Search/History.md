---
tags:
  - meta
  - history
---
# Awesome Search — Notes History

Chronological log of notes added to this knowledge graph. Newest first.

## 2026-07-27 — SPLADE domain fine-tuning: MICES talk + Qdrant's five-part series (8 notes)

Processed [[Evgeniya Sukhodolskaya]]'s [[MICES]] 2026 talk [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] from YouTube captions, then followed it to its written source and captured that too — the talk deliberately quotes **no numbers**, so [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] ([[Thierry Damiba]], [[Qdrant]], Parts 1–5) carries the evidence and the video note carries the argument, each pointing at the other.

The central claim: off-the-shelf [[SPLADE]] is trained on [[MS MARCO]] — web queries against Wikipedia passages — and catalogs are not web search. Fine-tuning on [[Amazon ESCI Dataset]] (Exact + Substitute as positives, from `distilbert-base-uncased`) reached **nDCG@10 0.389 vs BM25's 0.305 (+27.5%)** where the off-the-shelf model managed +7.2%. The **negative results matter as much**: the ESCI-tuned model *loses* to off-the-shelf SPLADE on [[Home Depot Product Search Relevance]] (0.384 vs 0.391) and collapses on MS MARCO (0.751 vs BM25's 0.915) — a model tuned on one catalog is not a general e-commerce model. Multi-domain training trades −4.4% in-domain for +6.8% Home Depot and +10.4% MS MARCO recovery.

**Concepts** — [[Hard Negative Mining]] (new hub; the vault referenced hard negatives across 8+ notes with no note of its own — the ANCE loop that indexes each checkpoint into a live search engine, retrieves, and keeps what the model wrongly believes relevant; worth 5–10% on top of basic training, plus the false-negative risk conceded in Q&A). [[miniCOIL]] (new — Sukhodolskaya's BM25-extending sparse retriever, 4 dims per word, notable for the **BM25 fallback on out-of-vocabulary terms** that SPLADE structurally lacks; wins 4 of 5 BEIR datasets it wasn't trained on).

**Tools** — [[Sentence Transformers]] (new — referenced by 20+ notes as plain text with no page; v5 sparse-encoder modules `MLMTransformer`/`SpladePooling` and `SpladeLoss`), [[qdrant-sparse-finetune]] (new — the framework the series produced; synthetic query generation via litellm, config defaults, CLI/Python/dashboard, and its author's own "slightly shaky" caveats including evaluation that runs on training data by default).

**People** — [[Evgeniya Sukhodolskaya]] (new — Qdrant DevRel, Munich; miniCOIL), [[Thierry Damiba]] (new — Qdrant; the five-part series).

**Updated** — [[SPLADE]] (new *Domain Fine-Tuning* section: the numbers, full vs inference-free for intent-heavy e-commerce, and the vocabulary limit), [[Learned Sparse Retrieval]] (ANCE + domain fine-tuning under Training Paradigms; miniCOIL added to the model family), [[Amazon ESCI Dataset]] (new *Use as Training Data* section — the E+S-as-positives convention and the transfer caveat), [[Sparse Embeddings]], [[Embedding Fine-tuning]], [[Qdrant]], [[MICES]], [[Videos]]. Registered in [[global_toc]] (Concepts, a new Tools › Embedding Training group, Videos, People), [[Concepts]], [[Tools]], [[People]], [[Index]], [[index|index.md]], and [[All about Information Retrieval & Search]].

## 2026-07-27 — PCA embedding compression, with the vault's first measured DR numbers (2 notes)

Processed [[Doug Turnbull]]'s [[Principal Component Analysis - an embedding shrink-ray]] from the `Clippings/` capture — covariance matrix → eigendecomposition → truncation, framed for search people as "a series of 'scoring functions' of decreasing importance," with the food-embedding analogy (sweet-ness / fruit-ness / vegetable-ness) carrying the intuition. Created [[MS MARCO]], filling a long-standing gap: the corpus was referenced across ~15 existing article notes with no note of its own.

The substantive addition is **hard data**. [[PCA]] gained a *Measured Cost on Real Embeddings* section — MiniLM on MS MARCO at 384→200 dims holds 0.879 recall (88.5% eigenvalue coverage), 384→100 drops to 0.5714, 384→50 collapses to 0.2029 — the vault's first measured recall-vs-dimensions curve, where [[Dimensionality Reduction vs Quantization]] previously carried only rules of thumb. Also captured the **flat-spectrum diagnostic**: an already-efficient embedding model ("1st eigenvalue is 15 and the 384th is 13") has no redundancy to harvest, so inspect the explained-variance curve before committing to PCA. The measured 1.9× usable ceiling tempers that topic note's "2–4× compression is common" heuristic.

Backlinked from [[Doug Turnbull]], [[PCA]], [[Dimensionality Reduction]], [[Dimensionality Reduction vs Quantization]]; [[Courses]] gained Turnbull's *Build your own vector database* (maven.com/softwaredoug/vectordb), announced in the article. Registered in [[global_toc]] (Datasets), [[Index]], and [[All about Information Retrieval & Search]] — both stats blocks gained a dataset-notes line, which neither previously had.

## 2026-07-19 — LTR concept enriched with Grebennikov's two training lessons (0 new notes)

Enriched [[Learning to Rank]] with the two production lessons from [[Roman Grebennikov - Personalizing Search Results in Real-Time]] that previously lived only in the video note: a new section **"What the Model Optimizes Is a Business Decision"** (the Stanley bong story — raw clicks reward curiosity; weighting purchases in the [[NDCG]] perfect ranking encodes the business goal, and the same lever optimizes margin) and a new subsection **"Feedback Loops: Don't Train on Data Your Model Produced"** under Position Bias in LTR Training (the +8% → +6% degradation from training on the model's own clicks; fix via an [[Exploration vs Exploitation]] ~1% shuffled exploration segment, with IPS as the alternative). Also expanded the video's blurb in the note's Articles list to name both lessons.

## 2026-07-12 — Grebennikov MICES 2019 real-time personalization talk (2 notes)

Processed the [[MICES]] 2019 talk [[Roman Grebennikov - Personalizing Search Results in Real-Time]] (Findify) from YouTube captions — real-time LTR across ~1,500 merchants: [[Position Bias]] feedback-loop degradation, the shuffled ~1% exploration segment, one generic cross-merchant model with feature scaling, and purchase-weighted perfect rankings for [[NDCG]] (the Stanley bong story). Includes a clickable Key Moments timestamp table derived from caption timings (the video's official chapters cover only the first half). Also created [[Exploration vs Exploitation]] (Concepts → Behavioral Signals & Bias). Backlinked from [[Roman Grebennikov]], [[MICES]], [[Learning to Rank]], [[LambdaMART]], [[NDCG]], [[Position Bias]], [[Personalization in Search]], [[E-commerce Search]]; registered in [[global_toc]], [[Videos]], [[index|index.md]], [[Index]], and [[All about Information Retrieval & Search]]. (A Findify company note was deliberately not kept — mentions stay as plain text.)

## 2026-07-06 — Federated vs Unified Search topic (1 note)

Created [[Federated vs Unified Search]], a Topic hub anchoring a comparison the vault previously held only as two separate concepts: [[Federated Search]] (query-time fan-out + merge) vs [[Unified Search Index]] (index-time consolidation). Framed around one question — *where does integration happen, query time or index time?* — with a trade-off analysis (freshness / ranking consistency / latency / governance) and a **terminology trap** section disambiguating three senses of “federated”: classic distributed IR, the [[Algolia]]/e-commerce multi-index UI (a unified engine with federated *presentation*), and [[Netflix]]’s federated *data* graph (made searchable by indexing into a unified index). Documents the convergence pattern — unified core with federated edges — grounded in vault case studies ([[Canva - Search Pipeline Modernization]], [[Reddit - Vector Database Selection]], [[Netflix - Content Search Architecture]], [[Bonsai - Designing Search for a Relational Database]]). Backlinked from both concept notes and [[MOC - Architecture and Search Team]] (System Architecture); registered in [[global_toc]] (Topics → Domains & Platforms), [[index|index.md]], [[Index]], and [[All about Information Retrieval & Search]].

## 2026-07-05 — Conferences MOC + wikilink sweep

Added a [[Conferences]] MOC indexing the four conference notes ([[Haystack US]], [[Haystack EU]], [[Berlin Buzzwords]], [[MICES]]) and linked it from [[global_toc]]'s Maps of Content. Swept previously plain-text conference mentions into wikilinks across curated hub notes ([[Search Communities]], [[Search Consultancy]], [[How to Start a Career in Search]], [[Women of Search]], [[Search Result Diversity]], [[Events and Conferences]], [[The Search Juggler]], [[Audrey Lorberfeld]], [[Rene Kriegler]]) and two factual article references (Block-Max WAND / Metarank citing [[Berlin Buzzwords]]). Deliberately left untouched: the unrelated **deepset Haystack** framework references (HyDE notes, `django-haystack`), the **Haystack Live** meetup mentions, markdown-hyperlinked citations, `Clippings/`, and the link-dump README.

## 2026-07-05 — Haystack US + Haystack EU conference notes (2 notes)

Added [[Haystack US]] and [[Haystack EU]] to the `Conferences/` folder — the two editions of [[OpenSource Connections]]' search *relevance* conference (US original in Charlottesville, VA; European edition in Berlin). Cross-linked to each other, to [[Doug Turnbull]] and [[Charlie Hull]] (organizer), the [[Max Irwin - The Search Engine Migration Circus|Haystack Live]] meetup talk, and [[Berlin Buzzwords]] / [[MICES]] as the other Berlin search events. Wikilinked from [[Events and Conferences]] and [[Charlie Hull]]; registered in [[global_toc]] Conferences.

## 2026-07-05 — MICES + Berlin Buzzwords conference notes + new Conferences content type (2 notes)

Created [[MICES]] (Mix-Camp E-Commerce Search) in a new `Conferences/` folder — the Berlin e-commerce search conference organized by [[Rene Kriegler]], co-located with Berlin Buzzwords and overlapping [[E-commerce Search]]. Consolidates references previously scattered as plain text across [[Events and Conferences]], [[Andreas Wagner]] ([[MICES]] talk on result diversity / basket composition), and the Kriegler notes. Backlinked from [[Rene Kriegler]], [[Rene Kriegler - Query Relaxation]], [[Andreas Wagner]], and [[Events and Conferences]] (all now wikilinking [[MICES]]); registered in [[global_toc]] under a new **Conferences** section. Also added [[Berlin Buzzwords]] — the open-source Berlin search/data conference (co-located with [[MICES]]) that recurs across the vault as plain text — linked to [[Lester Solbakken]]'s [[Hybrid search > sum of its parts? Berlin Buzzwords 2022]] talk and wikilinked from [[Events and Conferences]] and the Kriegler notes.

## 2026-07-05 — René Kriegler's "Query Relaxation" talk (2 notes)

Added the video [[Rene Kriegler - Query Relaxation]] — a 2019 [[OpenSource Connections]] talk (introduced by [[Charlie Hull]]) reframing [[Query Relaxation]] not as query *repair* but as a **query recommendation** problem: the aim is to keep the user in the conversation, not reconstruct exact intent. Walks the zero-result strategy spectrum ([[Query Expansion]] → spelling → low-quality fields → Boolean loosening → hypernyms → related queries → recommendations) and benchmarks term-drop predictors on freq vs. session co-occurrence datasets: random baseline → shortest/digit word-shape heuristics → least-frequent index term → (entropy fails) → **[[Word2Vec]]** cosine similarity → [[Mihajlo Grbovic|Grbovic]]-style query embeddings → a **multi-layer neural network** on word2vec + word-shape features (best, ~0.9 P/R), running real-time via TensorFlow. Created the new person [[Rene Kriegler]] (e-commerce relevance consultant, maintainer of [[Querqy]], organizer of MICES). Backlinked from [[Query Relaxation]], [[Querqy]] (added Kriegler as maintainer), [[Charlie Hull]], [[Daniel Tunkelang]] (blog-post inspiration), [[Mihajlo Grbovic]], [[OpenSource Connections]], [[E-commerce Search]], and [[Query Understanding in Practice]]; registered in [[global_toc]] (Videos + People), the [[Videos]] MOC, [[Index]], and [[All about Information Retrieval & Search]].

## 2026-07-05 — FAISS index tutorial video + ANN/FAISS/LSH hubs (4 notes)

Added the video [[Choosing Indexes for Similarity Search (Faiss in Python)]] by [[James Briggs]] ([[Pinecone]]) — a hands-on [[FAISS]] walkthrough of the four index families (**Flat, [[LSH]], [[HNSW]], [[IVF]]**) benchmarked on Sift1M, the video companion to the existing [[Nearest Neighbor Indexes for Similarity Search]] article. Filled three long-standing hub gaps discovered while linking: [[FAISS]] (tool — previously referenced by 30+ notes as plain text with no page), [[LSH]] (concept), and [[Approximate Nearest Neighbor Search]] (the parent ANN concept that [[HNSW]]/[[IVF]] linked to but never existed). Backlinked from [[James Briggs]], [[HNSW]], [[IVF]], and the Pinecone article; registered in [[global_toc]] (ANN Indexing, Search & Vector Engines, Videos), [[Concepts]], [[Tools]], and the [[Videos]] MOC.

## 2026-07-05 — Videos section + Max Irwin's "Search Engine Migration Circus" (1 note, new content type)

Introduced a new **Videos** content type for conference talks and recorded presentations, with its own folder (`Videos/`) and a section across all indexes. First entry: [[Max Irwin - The Search Engine Migration Circus]], a Haystack Live talk by [[Max Irwin]] ([[OpenSource Connections]]) drawn from his Wolters Kluwer / MediRegs migrations. Covers the OSC migration **playbook** (define success → measure baseline → "Hello Search" PoC → feature-parity analysis → risk register → gradual customer migration), the observation that **content is the timeline killer** and 100% feature parity is impossible, the **"damage" metric** (top-N result-set diff between legacy and target engines), and practical war stories (FAST ESP deprecation, the AWS lift-and-shift mistake, staggered query-parser/highlighter releases, forced-cutover vs. gradual migration). Q&A touches re-rank-only latency fixes and the [[Quepid]] / [[Rated Ranking Evaluator]] tooling. Companion to the [[Migration between Search Engines]] topic. Backlinked from [[Max Irwin]] (new Talks & Videos section) and [[Migration between Search Engines]] (Related Notes); registered in [[global_toc]] (new Videos section + MOC pointer), [[Index]], and [[All about Information Retrieval & Search]].

## 2026-07-03 — NDCG Variants topic (the "Flavors of NDCG")

Created [[NDCG Variants]], a Topic hub synthesizing [[Doug Turnbull]]'s "flavors of NDCG" across **two independent axes**: the *gain function* (Järvelin grade-gain vs. Burges exponential `2^rel−1`) and the *normalization target* ("normalized to what?" — local / recall / global / max), plus `@k` cutoffs and per-library defaults (scikit-learn, RankLib, [[LightGBM]], MS MARCO / BEIR, [[Quepid]]). Consolidates the two existing article clippings ([[Flavors of NDCG]], [[Flavors of NDCG - normalized to what]]) that each covered only one axis. Backlinked from the [[NDCG]] concept, both source articles (new Related Topics sections), [[global_toc]], [[Index]], [[Topics]], and [[All about Information Retrieval & Search]].

## 2026-07-03 — Hooking Quepid to Vespa (1 note)

Added [[How to Securely Hook Up Quepid to Vespa]] by [[Charlie Hull]] ([[The Search Juggler]]). A proof-of-concept for the vault's recurring theme — driving [[Quepid]] against a non-Lucene backend as a **custom search API**. Here the backend is [[Vespa]] Cloud, authenticated with a read-only **token** (Quepid can't use Vespa's self-signed client certs) and parsed via JavaScript result mappers. Fills Vespa's gap in interactive offline relevance testing and points toward exporting Quepid ratings as re-ranking training data. Companion to a Maven Lightning Lesson co-presented with [[Trey Grainger]]. Backlinked from [[Charlie Hull]], [[Quepid]], [[Vespa]], and the [[MOC - Search Quality Assurance and Query Understanding|Search QA MOC]] (Quepid in Practice).

## 2026-07-03 — OpenSearch Search Relevance Workbench & Elastic Relevance Studio (4 notes)

Filled the vault's biggest relevance-tooling gap: the vault had deep [[Quepid]] coverage but nothing on the **engine-native** evaluation tools that have emerged to rival it. Added both, plus a comparison note anchoring the three-way choice. Cross-engine takeaway: Elastic and OpenSearch are absorbing Quepid's offline-evaluation loop *into the engine itself*, adding behavior-driven (UBI/click) and agent-driven (LLM/MCP) judgments — and notably [[OpenSource Connections]] (Quepid's authors) also drove the OpenSearch tool, so it's the same community pushing the practice into the engines.

**Tools** — [[Search Relevance Workbench]] (new — OpenSearch 3.1+ native tool: query sets / search configurations / judgments / experiments; three judgment sources incl. [[Implicit Judgments|UBI]] COEC implicit judgments and LLM-as-judge; unique hybrid-search grid-search optimization; imports Quepid CSV; Dashboards visualizations in 3.2); [[Elasticsearch Relevance Studio]] (new — Elastic's experimental React+Flask lifecycle app over the ES Search API: scenarios / judgements / strategies / benchmarks; drag-slider judging; NDCG/Precision/Recall/MRR + unrated-doc reporting; headline **MCP server** for agentic AI workflows); [[Rated Ranking Evaluator]] (new — [[Sease]]'s open-source, CI/CD-oriented offline evaluation *library* for Solr/Elasticsearch; JVM/Maven modules, corpus→topics→query-groups→queries domain model, immutable version-over-version delta tracking, broad metric set incl. ERR/F-measure, RRE Server dashboard + RRE Enterprise; resolves a long-standing dead link).

**Topics** — [[Relevance Evaluation Tools Compared]] (new — four-way Quepid vs. Workbench vs. Relevance Studio vs. [[Rated Ranking Evaluator|RRE]]; at-a-glance / judgment-sources / experiment-capabilities / metrics tables + a "how to choose" guide).

**People** — [[Daniel Wrigley]] linked (authored the OpenSearch SRW/judgments blog as well as the Quepid guide).

**Updated** — [[Quepid]] (Related Tools → SRW/ESRS/RRE + comparison pointer), [[OpenSearch]] (Related Tools → SRW), [[Elasticsearch]] (Related Tools → ESRS), [[Search Evaluation]] (new Tools section), [[Sease]] (added RRE as its product), [[Relevance Program Setup]] (RRE wikilinked), [[Tools]], [[global_toc]], [[index|index.md]] / [[Index]] / [[All about Information Retrieval & Search]] (Tools highlight lists).

**Correction** — [[OpenSource Connections]] previously mis-listed [[Rated Ranking Evaluator]] as an OSC product; RRE is [[Sease]]'s. OSC's products corrected to [[Quepid]] + the Elasticsearch LTR plugin, with a note pointing RRE to Sease.

---

## 2026-07-01 — Solr↔Vespa Onboarding & AI-Assisted Migration (7 notes)

Processed two Clippings articles that both orbit **cross-engine migration** — and created a [[Migration between Search Engines]] topic to anchor them alongside the existing ES→Vespa case studies.

**Articles** — [[How I learned Vespa by thinking in Solr]] (new — [[Sujit Pal]], [[Elsevier]] Labs, 2021-02-24; a Solr→Vespa mapping table — core≈application, `managed-schema`≈`.sd`, MLT≈`nearestNeighbor` ANN, YQL≈SQL — MVP on CORD-19 + SPECTER embeddings via [[HNSW]]); [[Amazon OpenSearch Service now offers AI-assisted migrations]] (new — [[Amazon Web Services]], 2026-06-23; Migration Assistant's agent-guided (Kiro / Claude Code) workflow for Solr/ES/OpenSearch → Amazon OpenSearch, now with live-traffic capture/replay for Solr).

**Topics** — [[Migration between Search Engines]] (new hub — schema/analyzer parity, historical + live-traffic sync, relevance validation; groups the hand-built Vinted/Kleinanzeigen ES→Vespa migrations, AWS's tool-assisted OpenSearch migration, and Solr→Vespa mental mapping).

**Tools** — [[Solr]] (new — Apache Lucene-based engine; cores, `managed-schema`/`solrconfig.xml`, MLT, function queries; common migration source).

**People** — [[Sujit Pal]] (new — Technology Research Director, Elsevier Labs).

**Companies** — [[Elsevier]] (new — Elsevier Labs), [[Amazon Web Services]] (new — Amazon OpenSearch Service / Migration Assistant).

**Updated** — [[Vespa]] + [[OpenSearch]] (article lists), [[Vinted - Migrating Search from Elasticsearch to Vespa]] + [[Kleinanzeigen - Vespa Migration for Homepage Feed]] (linked to the migration topic), [[People]], [[global_toc]] (Tools/Companies/Topics/People), [[index|index.md]] (Tools/Companies/Stats: 7 tools, 30 companies, 28 topics).

---

## 2026-06-29 — Vinted Dense Retrieval & Billion-Scale (2 notes)

Finished the Vinted Vespa arc from the "Search Scaling" series — importing only the Vespa-era, retrieval-relevant posts (all pre-Vespa/ops chapters deliberately skipped).

**Articles** — [[Dense Retrieval at Vinted]] (new — [[Laurynas Jasiukėnas]] & [[Dainius Jocas]], 2025-11-18; frozen multilingual-CLIP two-tower query/item towers, 256-dim, hybrid ANN-supplements-lexical capped to top-K, contrastive training 7–10k negatives/positive over >100M pairs, HNSW on 30 content nodes/group × 3 market indices, 500ms budget w/ 350ms approx + 150ms exact fallback, GraalVM/ZGC, <0.02% error, ~50 A/B tests).

**People** — [[Laurynas Jasiukėnas]] (new — Vinted; dense-retrieval co-author).

**Folded in (no new note)** — Search Scaling Chapter 9 "Billion-Scale Search" ([[Dainius Jocas]], 2025-01-10; 1B docs by Nov 2024, ~10× since 2019, mean <20ms at data layer, ~2× headroom) added as a **Postscript** section to [[Vinted - Migrating Search from Elasticsearch to Vespa]].

**Updated** — [[Dense Vector Retrieval]] (Vinted as a production example), [[Vinted]] + [[Dainius Jocas]] (article lists), [[global_toc]] (People L).

---

## 2026-06-29 — Vinted Vespa Match-Features (3 notes)

Captured Vinted's [[Vespa]] `match-features` post — a sharp engineering result tying into [[Vespa Learning to Rank]]: using `match-features` as an in-engine feature store (replacing Redis round-trips) and, more surprisingly, to **cut latency** by skipping the document-summary `.fill()` fetch (two-phase scatter-gather → single round-trip; **P99 ~9ms→3ms**, mean ~430µs at 7.5k RPS). The companion 2023 recommendation-retrieval post was already in the vault — only its authorship was filled in.

**Articles** — [[Optimizing Vespa Latency with Match-Features at Vinted]] (new — [[Dainius Jocas]], 2025-11-06; `match-features` declaration/tensors, Vespa-as-feature-store vs Redis, summary-fetch elimination, latency results).

**People** — [[Dainius Jocas]] (new — Vinted; author of both Vinted Vespa posts), [[Aleksas Kateiva]] (new — Vinted; co-author of the recommendation post).

**Updated** — [[Vespa Learning to Rank]] (`match-features` bullet → online-serving/latency note + link), [[Adopting Vespa for Recommendation Retrieval at Vinted]] (real authors + People section), [[Vinted]] (article list + people), [[global_toc]] (People A/D).

---

## 2026-06-29 — Vinted ES→Vespa Search Migration (2 notes)

Processed Vinted Engineering's "Search Scaling Chapter 8: Goodbye Elasticsearch, Hello Vespa" into a case study — a rare concrete account of a **billion-item, 20k-RPS** production search platform moving off [[Elasticsearch]] to [[Vespa]]. Decisive wins were operational (shard toil eliminated, no hot nodes, change-visibility 300s→5s, server fleet halved to 60), enabled by porting Lucene text analyzers into Vespa.

**Case Studies** — [[Vinted - Migrating Search from Elasticsearch to Vespa]] (new — scale, motivations, 60 content / 12 container / 3 config node topology, Flink + open-sourced Vespa Kafka Connect sink, Go "search contract" middleware with 12 query patterns, 3× ranking depth to 200k candidates, May 2023→Apr 2024 timeline, results).

**People** — [[Ernestas Poškus]] (new — Vinted search-platform engineer; author of the Search Scaling series).

**Updated** — [[Vinted]] (new Search Platform Migration section + frontmatter), [[Case Studies]], [[MOC - Case Studies]] (Architecture & Platform Migration), [[global_toc]] (Case Studies + People), [[Index]] / [[All about Information Retrieval & Search]] (Case Studies list + counts 9→10).

---

## 2026-06-29 — Vespa Learning to Rank (2 notes)

Gave [[Vespa]] the same LTR coverage as [[Elasticsearch Learning to Rank]]. Framing: Vespa doesn't add a dedicated LTR subsystem — GBDT LTR, neural reranking, and MaxSim are all just expressions in its one tensor/ranking-expression engine, runnable across first/second/global phases and ensemble-able.

**Topics** — [[Vespa Learning to Rank]] (new — phased ranking `first-phase`/`second-phase`(content-node, `rerank-count`)/`global-phase`(container, cross-hit); native GBDT import via `xgboost("model.ubj")` / `lightgbm("model.json")` and `onnx(...)` neural models in `models/`; rank features `bm25`/`nativeRank`/`fieldMatch`/`attribute`/`closeness` + tensor MaxSim; feature dumping via `match-features`/`summary-features`/`rank-features`; train-offline/serve-in-engine workflow; Vespa-vs-Elasticsearch LTR table).

**Tools** — [[ONNX]] (new — Open Neural Network Exchange + ONNX Runtime; how neural rankers/cross-encoders are served in-engine, esp. Vespa `global-phase`).

**Updated** — [[Learning to Rank]] and [[Elasticsearch Learning to Rank]] (sibling cross-links; Vespa examples linked), [[Vespa]] (company note: LTR capability + Concepts links), [[XGBoost]] / [[LightGBM]] (Related links to Vespa LTR), [[global_toc]] (new ML & Model Serving tools group), [[Concepts]], [[Index]] / [[All about Information Retrieval & Search]] indices.

**Reclassification** — both engine-specific LTR notes ([[Elasticsearch Learning to Rank]], [[Vespa Learning to Rank]]) moved concept → **topic** (folder `Concepts/` → `Topics/`) to match the `Late Interaction in <engine>` topic pattern; indices and counts adjusted (−2 concepts, +2 topics).

---

## 2026-06-29 — Late Interaction in Vespa (1 note)

Completed the four-engine late-interaction set, bringing [[Vespa]] to the same coverage as Elasticsearch / OpenSearch / Qdrant. Framing: Vespa is the **origin engine for production late interaction** ([[Jo Kristian Bergum]]'s native ColBERT embedder + the sign-bit binarization the field later adopted), and the only one that expresses MaxSim as a general **tensor ranking expression** rather than a dedicated field/function.

**Topics** — [[Late Interaction in Vespa]] (new — mixed `tensor<int8>` storage for ColBERT tokens / long-context windows / ColPali patches; MaxSim written as `reduce(...,max,...)`+`sum` tensor expressions; `hamming` + `unpack_bits` 32× binary quantization; native multi-phase ranking with `nearestNeighbor`/BM25 first phase + query-token pruning; billion-scale ColPali by computing on content nodes — "speed of memory not network"; four-engine comparison table).

**Updated** — [[Vespa]] (company note: ColBERT embedder → topic pointer + Concepts link), [[Late Interaction]] and the three sibling topics ([[Late Interaction in Elasticsearch]], [[Late Interaction in OpenSearch]], [[Late Interaction in Qdrant]]) cross-linked, [[global_toc]], [[Topics]], [[Index]] / [[All about Information Retrieval & Search]] indices.

---

## 2026-06-29 — Late Interaction in OpenSearch & Qdrant (3 notes)

Extended the late-interaction cluster sideways from [[Late Interaction in Elasticsearch]] to the other two engines, so the vault now covers how [[ColBERT]]/[[ColPali]] multi-vector reranking is implemented across all three. Cross-engine takeaway: all three converge on late interaction as a **reranker** over a cheap first stage, differing mainly in packaging.

**Topics** — [[Late Interaction in OpenSearch]] (new — native `lateInteractionScore` painless fn in OpenSearch 3.3+, `object`+`float` multi-vector storage, Lucene `LateInteractionField`/`LateInteractionRescorer` 10.3+, ml-inference ingest/search processors, two-phase retrieval, 10–100× storage); [[Late Interaction in Qdrant]] (new — first-class `multivector_config` with `MultiVectorComparator.MAX_SIM`, `hnsw_config m=0` for rerank-only vectors, single-call `prefetch`+`query` retrieve-then-rerank via the Query API, MUVERA/dense/sparse first stage).

**Concepts** — [[MUVERA]] (new — Multi-Vector Retrieval via Fixed Dimensional Encodings; collapses a ColBERT multivector to one ANN-indexable vector for stage-1 retrieval; the Qdrant analogue of Elastic's "average vectors").

**Updated** — [[Late Interaction in Elasticsearch]] and [[Late Interaction]] (sibling cross-links), [[OpenSearch]] and [[Qdrant Vector DB]] (late-interaction capability + links), [[Elasticsearch vs OpenSearch]] (late-interaction feature row + links), [[global_toc]], [[Topics]], [[Concepts]] indices.

---

## 2026-06-28 — Quepid Practical Use Cases: Vector & Image Search Evaluation (8 notes)

Added a cluster of practical, "what actually breaks" use cases for [[Quepid]] beyond the canonical lexical workflow — collaborative team judging, and the hacks needed to evaluate **vector** and **image** search. Anchored by a new [[Vector Search Evaluation]] concept that catalogs why judgment-list tooling built for text queries struggles with embeddings (query-length limits, JSON-validity catch-22, non-human-readable queries, non-text results) and the workarounds.

**Concepts** — [[Vector Search Evaluation]] (new; ties together cross-modal, image-to-image, hybrid evaluation and the Quepid limitations/workarounds).

**Articles** — [[Creating Judgement Lists with Quepid]] ([[Daniel Wrigley]], Elastic Search Labs; collaborative judging, information needs, books of judgements, v8 AI judgements); [[Why Setting Up Quepid for Vector Search Evaluation Went Wrong]], [[Oops, I Did It Again]], [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]], [[How to Evaluate Image Search in Qdrant Using Quepid Part 2]] (all [[Andrew Kornilov]]; the vector/image series — dimension reduction to fit limits, query-option vector injection, Qdrant-as-endpoint, scorer hacks + upstream PR #1683).

**People** — [[Andrew Kornilov]] (vault author; hands-on Quepid/vector series; unofficial Quepid API), [[Daniel Wrigley]] (Quepid judgement-lists guide).

**Updated** — [[Quepid]] (new *Practical Use Cases* section + expanded Related Articles), [[global_toc]], [[Index]] / [[All about Information Retrieval & Search]] (Evaluation concepts + Key People + stats), [[MOC - Search Quality Assurance and Query Understanding]] (Judgment & Annotation + Key People).

---

## 2026-06-27 — Search UX & Discovery, Click Models & UX Research Orgs (13 notes)

A browseability + UX-research build-out, applying README-gap analysis and surfacing the **Search UX & Discovery** and **Lexical Query Operations** families across the indices.

**Concepts** — [[Neural Click Models]] (NCM, CACM, GraphCM, two-tower; deep-learning successors to [[Click Models]]); [[Search Scopes]] (pre-query narrowing vs. post-query [[Faceted Search]]; the sticky-scope failure mode).

**Topics** — [[Search UX Research]] (new hub for independent search-UX research organizations).

**Companies** — [[Baymard Institute]], [[Nielsen Norman Group]], [[Enterprise Knowledge LLC]] (search-UX research orgs).

**People** — [[Heather Hedden]] (*The Accidental Taxonomist*); [[Elzbieta Jakubowska]] (filled a [[Women of Search]] placeholder / dangling link).

**Articles** — four [[Nielsen Norman Group]] studies: [[The Pinball Pattern - Complex Search-Results Pages Change Search Behavior]], [[Scoped Search - Dangerous but Sometimes Useful]], [[Good Abandonment on Search Results Pages]], [[Search-Log Analysis - The Most Overlooked Opportunity in UX Research]].

**MOCs** — [[MOC - Case Studies]] (new curated map; resolved a long-standing dangling link); [[MOC - Search UX and Discovery]] rewritten to surface the full family.

**Index restructuring** — split visible **Search UX & Discovery** and **Lexical Query Operations** families in [[global_toc]] and the home indices; moved [[Knowledge Graph Search]] and [[Results Boosting]] to coherent homes; relocated the [[Search UX]] topic out of Strategy & Meta. Fixed an inverted alias link in [[Neural Click Models]].

---

## 2026-06-27 — Duality in Measuring Search Topic (1 note)

Created a **Topic** hub for [[James Rubinstein]]'s recurring "qual + quant" thesis — that knowing whether search works needs two complementary signals and "it's not one-or-the-other, it's *yes, and!*" The hub organizes the duality under two lenses: *improving* search (statistical / metrics-driven vs. human-centered) and *measuring* search (online / log-based vs. offline / human-rated), reconciled at the [[The Launch Review|launch review]].

**Topics** — [[Duality in Measuring Search]] (new hub — two side-by-side comparison tables for the improvement and measurement lenses; why neither half suffices; how it fits the broader [[Search Evaluation]] / [[Relevance Program Setup]] / [[A-B Testing for Search]] stack; alias "Two Approaches to Measuring Search").

**Updated** — [[Measuring Search - A Human Approach]] and [[Statistical and Human-Centered Approaches to Search Improvement]] (both normalized and marked as paywalled — `access: paywalled`, `paywalled` tag, `published` dates; the second's body left faithful to source; fabricated content in the former replaced with a faithful summary and its accidental duplicate removed). [[James Rubinstein]] (article list extended with the two posts + [[The Launch Review]]).

---

## 2026-06-25 — Interaction Paradigms Topic (1 note)

Extracted the broader idea behind the "Interaction Timeline Comparison" section of [[Late Interaction]] into a dedicated **Topic** hub spanning the *no / late / early* interaction spectrum, which organizes [[Bi-Encoder]], [[ColBERT]] / [[Late Interaction]], and [[Cross-Encoder]] as three points on one axis (when query and document are allowed to interact).

**Topics** — [[Interaction Paradigms]] (new hub — the no/late/early interaction spectrum; both timeline diagrams; comparison table across bi-encoder / late-interaction / cross-encoder covering pre-encoding, granularity, speed, quality, pipeline role; an orthogonal sparse-vs-dense axis tying in [[Learned Sparse Retrieval]] / [[SPLADE]] / [[ELSER]] / [[Hybrid Search]]).

**Updated** — [[Late Interaction]] (pointer added under the comparison section + Related Topics entry), [[Bi-Encoder]] (backlink — the no-interaction endpoint), [[Cross-Encoder]] (backlink — the early-interaction endpoint).

---

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

Updated — [[Late Interaction]], [[ColPali]], [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]], [[Peter Straßer]], [[Frontier of Search 2026]] cross-linked into the new cluster; [[index|index.md]] Topics + Stats refreshed.
---

## Older Entries

Entries for **2026-06-18 and earlier** have been archived to [[History-2]].

---

## Stats Over Time

| Date | Notes Added | Running Total (approx.) |
|------|------------|------------------------|
| 2026-07-27 (SPLADE fine-tuning: MICES talk + Qdrant series) | 8 | ~657 |
| 2026-07-27 (PCA embedding shrink-ray) | 2 | ~649 |
| 2026-07-12 (Grebennikov MICES 2019 personalization talk) | 2 | ~647 |
| 2026-07-03 (relevance workbench, relevance studio & RRE) | 4 | ~645 |
| 2026-07-01 (Solr↔Vespa onboarding & AI-assisted migration) | 7 | ~641 |
| 2026-06-29 (Vinted dense retrieval & billion-scale) | 2 | ~634 |
| 2026-06-29 (Vinted match-features) | 3 | ~632 |
| 2026-06-29 (Vinted ES→Vespa migration) | 2 | ~629 |
| 2026-06-29 (Vespa learning to rank + ONNX) | 2 | ~627 |
| 2026-06-29 (late interaction in Vespa) | 1 | ~625 |
| 2026-06-29 (late interaction in OpenSearch & Qdrant) | 3 | ~624 |
| 2026-06-28 (Quepid vector/image eval) | 8 | ~621 |
| 2026-06-27 (duality topic) | 1 | ~613 |
| 2026-06-27 (search UX & click models) | 13 | ~612 |
| 2026-06-25 (interaction paradigms) | 1 | ~599 |
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
