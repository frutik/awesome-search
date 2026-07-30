---
tags:
  - meta
  - history
---
# Awesome Search — Notes History

Chronological log of notes added to this knowledge graph. Newest first.

## 2026-07-30 — Ranking a corpus with three labeled queries: the Vespa zero-shot series (12 notes)

Processed all three posts of [[Jo Kristian Bergum]]'s January–February 2023 sequence at [[Vespa]]. They already existed in the vault only as URLs in the External References of [[Three mistakes when introducing embeddings and vector search]], which compresses the whole argument into one bullet. Read in order they are a single piece of work: state the problem, build a baseline that survives it, then stop having the problem.

**Part one** ([[Improving Zero-Shot Ranking with Vespa Hybrid Search]]) is measurement discipline. What [[BEIR]] actually contains, why its per-dataset judgment depth ranges over three orders of magnitude ([[TREC-COVID]] at ~493.5 judgments per query against [[Natural Questions]] at ~1.2), and [[Dense Passage Retriever]] as the concrete case: trained on NQ, strong in-domain, beaten by [[BM25]] on [[MS MARCO]] zero-shot. The corpora differ by a few words of query length. That narrowness is the argument. Also the source of **"LGTM (*Looks Good To Me*)@10"** as a name for how the industry actually evaluates.

**Part two** ([[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]]) is the method, and two findings worth more than its headline. First, its own tuned BM25 (k1=0.9, b=0.4, title and text scored separately) **beat the BM25 numbers published with BEIR** — 0.453 vs 0.440 average, 0.393 vs 0.315 on ArguAna — so "we beat BM25" is partly a claim about someone else's configuration. Second, the distilled 22M [[ColBERT]] reranker scores **0.363, below BM25's 0.453, and still lifts the hybrid to 0.481** across 13 datasets. A component that loses standalone can be the reason a fusion wins; don't screen candidates on their solo score. The one loss, CLIMATE-FEVER, is a truncation artifact — 20.2-word queries against a 32-wordpiece limit.

The mechanism that made [[Score Normalization]] worth revisiting: min-max is trivial arithmetic until the index is sharded, because min and max are properties of a *result set* and each node sees only its shard. Vespa computes them in a custom searcher at the query dispatcher, fed by match-features carried up from the content nodes — score-based fusion belongs at the first point in the topology that sees the whole candidate set. A second reason [[Reciprocal Rank Fusion|RRF]] is robust: ranks are comparable across shards in a way raw scores are not.

**Part three** ([[Improving Search Ranking with Few-Shot Prompting of LLMs]]) stops being zero-shot for the price of three labeled queries. `flan-t5-xl` (3B) generates a query per document, [[Consistency Filtering]] keeps the 43% whose source document ranks #1 (33,099 → 14,156), negatives come free from the same retrieval pass, and a 22M [[Cross-Encoder|cross-encoder]] trained two epochs reaches **80.2 nDCG@10** — above [[PROMPTAGATOR]]'s 76.2, which used a **137B** generator. The transferable finding is a sentence: adding *"The query must be specific and detailed"* to the prompt was what separated usable training data from generic queries. Note the bootstrap — part two's model is what filters part three's data, so tuning the baseline paid off twice.

Three grounding decisions recorded rather than smoothed over: part two's PROMPTAGATOR averages don't reconcile with the four rows extractable from its table, so the comparison spans datasets not captured here and the averages are cited as stated; part three quotes its TREC-COVID baselines as 70.0/76.0 where part two's table gives 0.690/0.750, and both are recorded as each article states them; and [[FLAN-T5]] beating a 137B generator is one dataset, not a scaling law.

**New** — [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] · [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] · [[Improving Search Ranking with Few-Shot Prompting of LLMs]] · [[Synthetic Query Generation]] · [[Consistency Filtering]] · [[Dense Passage Retriever]] · [[PROMPTAGATOR]] · [[FLAN-T5]] · [[TREC-COVID]] · [[Natural Questions]] · [[Vespa - Ranking Without Labels on CORD-19]]

**Updated** — [[Zero-Shot Retrieval]] (measured hybrid gain, compression and length-limit degradation, the baseline-is-a-variable section) · [[Score Normalization]] (distributed min-max via match-features) · [[Hybrid Search]] (the BEIR table and the losing-component lesson) · [[BM25]] ("BM25" in a results table is not one number) · [[ColBERT]] (the earlier 22M/32-dim model and its zero-shot cost) · [[Cross-Encoder]] (training without labels; the versioning argument) · [[Knowledge Distillation]] (generative teacher via generated data; compression costs more out-of-domain) · [[Hard Negative Mining]] (negatives from the consistency-check pass) · [[Linear Score Combination]] · [[Late Interaction in Vespa]] · [[Presentation Bias]] (synthetic queries as a mitigation) · [[ONNX]] · [[BEIR]] · [[MS MARCO]] · [[Jo Kristian Bergum]] · [[Vespa]] · [[global_toc]] · [[index|index.md]] · [[Index]]

---

## 2026-07-30 — Two notes disagreed about what Bayesian BM25 is (0 notes, 1 correction)

Surfaced while grounding [[Out-of-Vocabulary]]. [[BM25]] carried a stub describing [[Bayesian BM25]] as treating *"BM25 parameters as priors"*, updating *"based on collection statistics"*, and being *"particularly useful for out-of-vocabulary and low-frequency terms"* — while the dedicated [[Bayesian BM25]] note described something else entirely: logistic calibration of the score into a probability. Both cannot be right, and the new OOV note had inherited the stub's version.

Checked against both [[Doug Turnbull]] sources. [[Bayesian BM25 is Cool]] (2021) gives `BB25 = σ(a × BM25 + b) = P(R | BM25)` for principled fusion. [[Can BM25 be a Probability]] (2026) decomposes it explicitly: a **prior** from term frequency and field length, a **likelihood** from the BM25 score through a sigmoid, and a Bayesian **posterior**, with `ALPHA`/`BETA` learned from labels by gradient descent.

Verdict on the stub: "priors" was garbled — there *is* a prior, but it comes from TF and field-length normalization, not from `k1`/`b`. "Collection statistics" was half-right — `BETA` is the corpus median BM25 score. **"Useful for out-of-vocabulary and low-frequency terms" appears in neither source and is not what BB25 does at all.** BB25 is about making a lexical score commensurable with probability-calibrated signals; rare-term handling is unrelated.

The stub is rewritten to match the sources, and [[Bayesian BM25]] gained the 2026 formulation it was missing (it had only ever reflected the 2021 post, and didn't link the later article), the alternatives Turnbull weighs against it — rescaling the *other* signals à la Craswell, learning the boosts directly, scaling BM25 itself — plus `type: concept` and links to [[Score Normalization]] and [[Linear Score Combination]], the α-tuning problem it exists to remove. The ungrounded claim was isolated to that one stub; nothing else in the vault repeated it.

**Updated** — [[BM25]] (stub corrected) · [[Bayesian BM25]] (2026 formulation, alternatives, frontmatter) · [[Out-of-Vocabulary]] (inherited claim removed)

## 2026-07-30 — The vocabulary boundary: Tokenization and Out-of-Vocabulary (2 notes)

Two gaps in very different states. **Tokenization** was referenced in ~40 notes and defined in none — load-bearing in [[Full-Text Search]] ("analysis"), [[Query Understanding in Practice]] (its whole Layer 1), [[Search using PostgreSQL]] (the parser≈tokenizer mapping), [[Multilingual Search]] (script diversity), [[Semantic Search Without Embeddings]] (the hierarchical-tokenizer trick *is* the article's mechanism) and [[Autocomplete]] (edge-ngram). The only note titled for it was [[Query Understanding - Tokenization]], a [[Daniel Tunkelang]] article note. **Out-of-vocabulary** was the opposite: already explained substantively in eight places — six concept notes ([[miniCOIL]], [[SPLADE]], [[Sparse Embeddings]], [[Learned Sparse Retrieval]], [[BM25]], [[Zero-Shot Retrieval]]) plus [[Three mistakes when introducing embeddings and vector search]] and the Q&A in [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — but with no node holding the argument the vault kept re-deriving.

[[Tokenization]] carries the same two-senses-one-word structure as [[Pooling]], and the split is worth stating plainly: **analyzer** tokenization has an open vocabulary (whatever the corpus contains), is configurable per field, and fails by recall loss from mismatched analysis; **model** tokenization has a vocabulary fixed at pre-training, is not configurable at all, and fails by [[Out-of-Vocabulary]]. A [[Hybrid Search]] system runs both at once, and they do not agree on what a token is. Tunkelang's load-bearing point gets its own callout: query-time and index-time tokenization must agree, and a mismatch doesn't error — it silently returns fewer results.

[[Out-of-Vocabulary]] frames why lexical search barely has the problem (an inverted index's vocabulary *is* the corpus; a rare term gets high IDF rather than no representation) against why neural retrieval has it acutely. One correction made deliberately: [[Three mistakes when introducing embeddings and vector search]] says unknown words "collapse to a single `UNK`", which is the common simplification. Subword schemes normally *fragment* an unfamiliar word into known pieces — true `[UNK]` is the residual case for input that can't be decomposed at all. The note states the accurate mechanism, and the article is left as a faithful record of its source. The practical problem is subtler than erasure anyway: decomposition is not understanding, so a novel brand name split into three familiar fragments yields a representation, just not a useful one.

The [[SPLADE]]/[[miniCOIL]] contrast is now anchored where it belongs: SPLADE's output dimensions *are* its base model's vocabulary, so OOV terms are unrepresentable with no fallback; miniCOIL falls back to plain [[BM25]] inside the same sparse vector, and works at word level precisely to avoid the subword tokenization that made COIL impractical. Which makes keeping a lexical leg in [[Hybrid Search]] a *vocabulary* mitigation and not only a semantic one.

**Concepts** — [[Tokenization]] (new) · [[Out-of-Vocabulary]] (new)
**Updated** — [[SPLADE]] · [[miniCOIL]] · [[Sparse Embeddings]] · [[Learned Sparse Retrieval]] · [[BM25]] · [[Zero-Shot Retrieval]] · [[Full-Text Search]] · [[Query Understanding]] · [[Query Understanding in Practice]] · [[Multilingual Search]] · [[Search using PostgreSQL]] · [[Collocations]] · [[Query Segmentation]] · [[Query Understanding - Tokenization]] · [[Concepts]] · [[global_toc]]

## 2026-07-30 — One word, six operations: splitting Pooling out of Token Pooling (1 note)

The vault had exactly one pooling note — [[Token Pooling]], the ColPali multi-vector *compression* technique — and nothing at all on **sequence pooling**, the step where a transformer collapses its per-token output matrix into the single vector a [[Bi-Encoder]] stores. That gap showed up as plain-text mentions with no home in [[Vector Search Tradeoffs]], [[ColBERT]], [[Vector Similarity Metrics]] and elsewhere, and as a misdirected link in [[Three mistakes when introducing embeddings and vector search]] — "average pooling across the 512 outputs" pointing at the compression note. Same shape as the UBI → [[Implicit Judgments]] aliasing problem logged earlier today. [[Bi-Encoder]] itself never mentioned pooling at all, despite it being the architecture's defining lossy step.

[[Pooling]] now owns the general concept and sense 1 in detail (mean/average, CLS, max, attention-weighted), and routes to the other five. The senses are genuinely unrelated beyond the name, and they pool along **different axes** — which is the part worth remembering:

| Sense | Collapses | Axis | Home |
|---|---|---|---|
| Sequence pooling | Per-token vectors → one document vector | Sequence length | [[Pooling]] |
| Token pooling | Many token vectors → fewer | Sequence length, partially | [[Token Pooling]] |
| Vocabulary pooling | Per-token vocab distributions → one sparse vector | Vocabulary | [[SPLADE]] |
| Judgment pooling | Many systems' top-k → one judged set | Result sets | [[Judgment Lists]] |
| Behavioral pooling | Interaction history → one preference vector | Time / events | [[Personalization]] |
| Similarity-matrix pooling | Query×document score matrix → one relevance score | Similarity scores | [[Late Interaction]] |

Two distinctions actually mislead. [[SPLADE]]'s `SpladePooling` is max pooling, but over the *vocabulary* axis, so it emits a vocabulary-sized sparse vector rather than a dense one — not a variant of mean pooling. And MaxSim's `max_j` is max pooling over a *similarity matrix*: the cleanest way to separate it from sense 1 is **what** gets pooled, since senses 1–3 pool representations at index time while MaxSim pools scores at query time, after the comparison has already happened.

The framing that ties it to the rest of the graph: sequence pooling forces the model to decide **at training time** which distinctions survive the collapse, against the training query distribution — which is exactly what [[Late Interaction]] defers by keeping per-token vectors, with [[Token Pooling]] as the tunable middle (average vectors being its `pool_factor = ∞` limiting case).

**Concepts** — [[Pooling]] (new)
**Updated** — [[Token Pooling]] (reverted to its narrow multi-vector-compression scope, gains a disambiguation callout) · [[Bi-Encoder]] (new `The pooling step` subsection — previously silent on it) · [[Personalization]] (new `Sequence Pooling over Behavioral History` subsection) · [[SPLADE]] · [[Judgment Lists]] · [[Late Interaction]] · [[ColBERT]] · [[Vector Similarity Metrics]] · [[Vector Search Tradeoffs]] · [[Sentence Transformers]] · [[Three mistakes when introducing embeddings and vector search]] (misdirected link repointed) · [[Patterns for Personalization]] · [[Concepts]] · [[global_toc]]

## 2026-07-30 — The two missing thirds of the MongoDB hybrid search series (3 notes)

The vault already held part 3 of [[Erik Hatcher]]'s MongoDB hybrid search series — [[Hybrid Search Blueprint Series Semantic Boosting]] — whose opening list named parts 1 and 2 in plain text, as neither existed. Both are now in.

[[Survey of the Hybrid Search Landscape]] (2025-04-01) supplies the framing the other two lean on: hybrid defined experientially as *combining two or more search techniques to produce results better than any single technique alone*, with **better** as the word that makes measurement a precondition rather than a follow-up. It orders the available techniques by **rankability** — key/value matching has none intrinsically, vector search has geometric distance, lexical search has the richest scoring surface — and prescribes the logging practice (queries with context, clicks *with the position they were at*, zero-result and session-trail analysis) that must precede any tuning. It also reclaims "hybrid" for the older signals-loop pattern: collect signals → ML-aggregate into insights → look up per user/context/query → augment the request. Hatcher's tuning-surface analogy is a 747 cockpit; his closing test is whether information is *ambiently findable*.

[[Reciprocal Rank Fusion and Relative Score Fusion]] (2025-11-20) is the arithmetic. Its methodological move is to drop lexical and vector entirely — nine restaurants with a distance and a rating, two independent variables — on the grounds that fusion is mathematically unconcerned with how the ranked lists were produced. Two findings worth having: the **weight-30 trick** (since 60 is a fixed built-in in the RRF denominator, a weight of 30 on each of two pipelines rescales the fused score into ~0.0–1.0, each contributing at most ~0.5), and that equal weights produce **structural ties** — rank 1 in list A and rank 1 in list B are indistinguishable to RRF, so breaking ties means differentiating weights.

The RSF half motivated the one new concept. [[Score Normalization]] had been referenced inline across [[Hybrid Search]], [[Relative Score Fusion]], [[Linear Score Combination]], [[BM25]], [[OpenSearch]] and [[Elasticsearch]] without a note of its own. The article supplies the non-obvious failure: sigmoid **saturates**. With one pipeline on a 0–100 scale and the other on 0–5, a raw distance score of 85.0 normalizes to exactly 1.0 — erasing every gradation inside that pipeline — while the 0–5 pipeline keeps its resolution, and the fusion then averages a flattened signal against a live one. The companion asymmetry: `$vectorSearch` scores already arrive in 0.0–1.0, whereas lexical `$search` [[BM25]] scores have no defined range at all, so normalization pressure falls almost entirely on the lexical leg.

**Articles** — [[Survey of the Hybrid Search Landscape]] (new) · [[Reciprocal Rank Fusion and Relative Score Fusion]] (new)
**Concepts** — [[Score Normalization]] (new)
**Updated** — [[Reciprocal Rank Fusion]] (weighting, ties, explainability) · [[Relative Score Fusion]] (`$scoreFusion`, the three normalization modes, saturation) · [[Hybrid Search]] (Hatcher's definition + the rankability spectrum) · [[Semantic Boosting]] (why it sidesteps normalization entirely) · [[Hybrid Search Blueprint Series Semantic Boosting]] (series list now links parts 1–2) · [[Erik Hatcher]] · [[MongoDB]] (fusion stage table) · [[MOC - Ranking and Retrieval]] · [[Concepts]] · [[global_toc]]

## 2026-07-30 — The clickstream standard the vault had been aliasing away (1 note)

A broken link found in [[Search Relevance Workbench]]: every mention of **User Behavior Insights** was an aliased link pointing at [[Implicit Judgments]] — `[[Implicit Judgments|UBI]]` — because no UBI note existed. That conflates two different things: implicit judgments are *labels derived from behavior*, UBI is the *standard for capturing the behavior in the first place*.

[[User Behavior Insights]] now stands on its own. It is a JSON Schema data standard (query request / query response / event) plus engine plugins, whose load-bearing idea is the **`query_id` join key** tying every downstream event back to the exact query and result set that produced it — alongside `client_id` and the `event_attributes` payload, which records both the item acted on (`object.object_id`) and its `position` in the result set. The OpenSearch reference plugin (first released for **2.15**, recent builds targeting spec **1.3.0**) writes `ubi_queries` and `ubi_events`, captures a query when the request carries a `ubi` section in its `ext` block, and generates + returns a UUID `query_id` when the client doesn't supply one. Notably it *persists* events but does not *capture* them — that is the separate `ubi-javascript-collector`. Engine-neutral by design: OpenSearch, Solr, Elasticsearch, and the Chorus reference stack. Sponsored by Eric Pugh ([[OpenSource Connections]]), Jeff Zemerick, Stavros Macrakis, and [[Charlie Hull]] ([[The Search Juggler]]).

**Tools** — [[User Behavior Insights]] (new)
**Updated** — [[Search Relevance Workbench]] (4 misdirected links repointed) · [[Relevance Evaluation Tools Compared]] (3) · [[Implicit Judgments]] (backlink to the capture standard) · [[Quepid]] · [[Search Evaluation]]

## 2026-07-30 — When *not* to buy a vector database, and what the fusion arithmetic costs you (10 notes)

Three sources processed, all circling the same theme: the machinery people adopt for vector search is frequently unnecessary, and when it is necessary the failure modes are silent.

Started with [[Doug Turnbull]]'s [[Just brute force your embeddings]] — one NumPy dot product serving ~1M 384-dim vectors at **79.7 QPS and 12ms single-threaded on an M4**, and 8.8M at 9.34 QPS / 106ms. The argument: at ~1m documents, low query traffic and embeddings written up front, *"they don't need to buy a multi-million dollar vector database, or spend 6 months learning to operate it."* Following its citation led to [[Jo Kristian Bergum]]'s [[Three mistakes when introducing embeddings and vector search]] (2023, paywalled), the origin of *"an exhaustive search might be all you need"* — which reports the same shape three years earlier at **~100ms single-threaded for 1M × 128 dims, ~25ms on four threads until memory bandwidth hits**. The two are *not* comparable (different hardware, dims, measurement), and both notes say so rather than manufacturing a speedup.

That article carries two more mistakes worth their own notes. Mistake #1: representations from a model that has only been pre-trained give *"next to random ranking results"* — pre-training optimises a masked-language objective, not a ranking one. Mistake #2 became [[Zero-Shot Retrieval]], a hub the vault had been missing while eight notes referenced "zero-shot" and [[BEIR]] carried the concept as a *dataset* note: in-domain performance does not predict out-of-domain performance, [[BM25]] has no learnable parameters and therefore nothing to overfit, and multi-vector [[ColBERT]] transfers better than a pooled [[Bi-Encoder]]. The vault's own [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] is the worked counter-example — +27.5% in-domain, losing to off-the-shelf on [[Home Depot Product Search Relevance]].

The third source, [[Davit Khachaturyan]]'s production post-mortem, became [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]]. Adding a BM25 branch to a working vector retriever made the query class it was meant to fix *worse*: the correct document left the candidate set entirely. In a `bool` query a document matching several `should` clauses scores the **sum**, and the engine does not normalize across clauses — unbounded BM25 plus bounded cosine means the lexical branch decides the ranking. The Redis worked example is exact: a ~700-word blog post repeating `maxmemory-policy` ~15 times outscores the reference document that states `noeviction` once, and the generated answer comes back fluent without ever naming the default. **Nothing alerts, and users file no ticket.** This forced a correction to the vault itself — [[Hybrid Search]]'s "Implementation in Elasticsearch" section had been presenting exactly this `bool`/`should` construct with no caveat.

Closed with [[Vector Search Tradeoffs]], an umbrella Topic synthesising all of it plus existing vault material into seven axes — do you need an index at all, recall/latency/memory, bytes per vector (delegating to [[Dimensionality Reduction vs Quantization]]), filtering, build-and-update cost, one-vector-or-many, and cost/topology — anchored by [[Reddit - Vector Database Selection]]'s 340M-vector evaluation, where deployment architecture and organisational fit decided it rather than recall.

**Articles** — [[Just brute force your embeddings]] · [[Three mistakes when introducing embeddings and vector search]]
**Case Studies** — [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]]
**Topics** — [[Vector Search Tradeoffs]]
**Concepts** — [[Brute-Force Vector Search]] · [[Zero-Shot Retrieval]]
**Tools** — [[ann-benchmarks]] (recall-vs-QPS curves, and its three blind spots: indexing cost, CRUD support, open-source only)
**Datasets** — [[SIFT1M]]
**People** — [[Roy Keyes]] (*"Embeddings are learned transformations to make data more useful"*) · [[Davit Khachaturyan]]
**Updated** — [[Hybrid Search]] (bool/should warning) · [[Linear Score Combination]] (L2 normalization, geometric mean) · [[BM25]] (unboundedness in fusion) · [[Reranking]] · [[Retrieval Pipeline]] (the candidate set as a hard ceiling) · [[Relative Score Fusion]] · [[OpenSearch]] · [[Search Quality Assurance]] · [[Approximate Nearest Neighbor Search]] · [[Dense Vector Retrieval]] · [[Vector Search Evaluation]] (fidelity vs relevance quality) · [[Vector Filtering]] · [[HNSW]] · [[IVF]] · [[LSH]] · [[Vector Quantization]] · [[MUVERA]] · [[ColBERT]] · [[Embedding Fine-tuning]] · [[FAISS]] · [[BEIR]] · [[MS MARCO]] · [[Vespa]] · [[Doug Turnbull]] · [[Jo Kristian Bergum]] · [[RRF is Not Enough]] · [[Dimensionality Reduction vs Quantization]]

**Defect found and fixed:** [[HNSW]] stated "~600–1600 MB / 1M **768-dim** float32 vectors", which fails arithmetic — 1M × 768 × 4 bytes is 3.07 GB for the payload alone. Tracing it back, the numbers were never wrong, only stripped of context: they come from [[Nearest Neighbor Indexes for Similarity Search 1]], whose table is explicitly labelled *"Sift1M, 128d, M1 chip"*, and 1M × 128 × 4 = **exactly 512 MB**, matching its "~500 MB" Flat and "~520 MB" IVF rows. [[Dense Vector Retrieval]] had copied the same table without the dimensionality qualifier. Both now state the 128-dim basis; [[HNSW]] gains a first-principles memory model (`n × d × bytes` for vectors plus `n × ~2M × 4` for links) that reproduces the measured 600–1600 MB range across `M=16`→`M=128`, and shows that at 768 dims the graph is a few percent of the total while the float32 payload is everything. [[Vector Search Tradeoffs]] cites no absolute memory figures, so nothing propagated.

## 2026-07-29 — Relevance feedback pushed *into* the index (5 notes)

Processed [[Evgeniya Sukhodolskaya]]'s [[Berlin Buzzwords]] 2026 talk [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] from YouTube captions, and followed it to her two written sources at [[Qdrant]] for the maths the talk skips.

The vault already covered [[Relevance Feedback]] thoroughly — explicit / pseudo / implicit, Rocchio, the bias caveats — but every note treated it as something you do *around* the engine: rewrite the query, or over-fetch and rerank. This talk fills the gap. Decompose search into query, documents and scoring function: everyone adapts the query, nobody rewrites the corpus, and the scoring function goes untouched **because search engines are black boxes you must build around**. Qdrant owns its index, so 1.17 (Feb 2026) modifies the [[HNSW]] hop-selection function itself — the next neighbour is chosen by a mix of query similarity and feedback from the previous round (`F = a·score + Σ confidence^b · c · delta`), so feedback bends the *path* through the graph and reaches the whole collection rather than a retrieved top-k. Three parameters, fitted once per (feedback model, collection, retriever) rather than per query; the objective is [[Knowledge Distillation]] — make cheap dense retrieval rank the way a [[Cross-Encoder]] or LLM would, since that judge could never be run over the full corpus. Reported [[BEIR]] gains span −3.9% to +38.7% relative.

Second thread, and the honest limit: **model-generated feedback replaces the user**, because explicit feedback doesn't scale (*"people are lazy"* — Google shipped thumbs up/down on its results page and removed it). Q&A pushed hard on the consequence — documents never surfaced never earn feedback, so [[Presentation Bias]] and [[Position Bias]] survive intact. Her own boundary: not for [[E-commerce Search]], where you want a human in the loop; better for scientific or medical literature where humans can't stay in it.

Then followed the talk to its two written sources, both by the same author, which turn out to be a **thesis and its follow-through**. [[Relevance Feedback in Informational Retrieval]] (2025) is a literature survey organised on two axes — feedback type (pseudo / binary / re-scored) against what it modifies (query refinement vs similarity scoring) — covering RM3, BERT-QE (+11% NDCG@20 for 11.01× the compute), ANCE-PRF/ColBERT-PRF, Rocchio, TOUR, ReFit, kNN scoring and reranker fine-tuning. Its diagnosis is the interesting part: the literature over-represents query rewriting **because that's the only thing reachable from outside a black box** — *"researchers have no direct access to retrieval systems… this is sufficient for query-adjusting methods but not for similarity scoring function adjustment."* [[Relevance Feedback in Qdrant]] (2026) is the answer to its own closing requirement that a solution *"needs to be integrated directly into the retrieval system itself"*, with the full formula (context pairs, `confidence`, `delta`, and why each edge case defers to the retriever), the training setup, and per-dataset [[BEIR]] results.

Two honest caveats worth carrying: the gains are measured against the **feedback model** as ground truth (`abovethreshold@10`, not human judgments — it bounds how well the index imitates the judge), and several pairings **regress**. Benefit requires that the judge disagree with the retriever *and* that the retriever's space can represent the distinction — *"the retriever operates in a lower-dimensional space and can't capture all the distinctions the feedback model makes."*

New: [[qdrant-relevance-feedback]] (Tools) — the parameter-fitting package; [[BEIR]] (Datasets) — a hub the vault had lacked despite ~12 notes citing BEIR numbers ([[Elastic Learned Sparse Encoder (ELSER) Retrieval Performance]] +17% over BM25, [[ColBERT-Zero - To Pre-train Or Not To Pre-train ColBERT Models]] 55.43 nDCG@10, [[miniCOIL]] 4-of-5, [[psql_bm25s]] ~3.97× QPS), with the subset caveat that a "BEIR average" usually covers 12–15 of 18 datasets. Updated [[Relevance Feedback]] with a *Where the Feedback Is Applied* section (query vs documents vs scoring function) plus the index-native variant and model-generated feedback; [[HNSW]] with a *Steering the Traversal* section tying this to [[Vector Filtering]] and [[ACORN-1]] as instances of the same seam. Backlinked from [[Evgeniya Sukhodolskaya]], [[Qdrant]], [[Berlin Buzzwords]], [[MS MARCO]]; registered in [[global_toc]], [[Videos]], [[Tools]], [[Index]] and [[All about Information Retrieval & Search]].

## 2026-07-27 — Why t-SNE is disqualified for retrieval, and the DR-vs-quantization hot take (1 note)

Created [[PCA vs t-SNE for Retrieval]], a Topic hub for a claim the vault previously only *asserted*: [[t-SNE]]'s note carried a bare "not suitable for search/retrieval" line and [[Dimensionality Reduction vs Quantization]] lumped t-SNE and [[UMAP]] into one dismissive bullet, neither giving the mechanism. The note separates **two independent disqualifiers** — t-SNE is non-parametric (its optimization variables *are* the output coordinates, so there is no transform to apply to a query; refitting per query is O(n log n) over the corpus *and* non-deterministic, invalidating the index every run), and its KL(P‖Q) objective is not a distance-preservation loss (the asymmetry makes false neighbours nearly free, precisely search's worst failure mode, while the Student-t heavy tail deliberately discards between-cluster distance — the very quantity ranking sorts on). [[UMAP]] is the case proving the disqualifiers are independent: parametric, so #1 dissolves, but the same local-structure bias remains. Framed by the general principle that **visualization DR optimizes for human perception of cluster structure while retrieval DR optimizes for metric fidelity** — a category difference, not a quality gap.

Also updated [[Dimensionality Reduction vs Quantization]] with a **Hot Take: The "vs" Is a False Taxonomy** section, from a Relevance Slack thread ([[Search Communities]]): the two are independent multipliers on `bytes = dims × bits/dim`, not competing choices. Documents [[Doug Turnbull]]'s stacked flow — PCA → random rotation → [[Scalar Quantization]] — where the middle stage exists because PCA output is anisotropic *by construction*, the worst input for a uniform quantizer ([[TurboQuant]]/[[RaBitQ]]'s core insight); the unrotated stack underperforming is likely why the "vs" framing persists. Reframes the real decision axis as **where the fit cost is paid** (none for scalar/binary, offline for PCA and PQ/[[IVF]], at pretraining for [[Matryoshka Embeddings]]) — a point from Mohammad Hasnain in the same thread. The note's old *Structural Difference* section was folded in as redundant.

Backlinked from [[PCA]], [[t-SNE]], [[UMAP]], [[Dimensionality Reduction vs Quantization]], and [[MOC - Agentic Search and Embeddings]]; registered in [[global_toc]] (Topics → Retrieval & Ranking Techniques), [[Topics]], [[Index]], and [[All about Information Retrieval & Search]].

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

**Tools** — [[Search Relevance Workbench]] (new — OpenSearch 3.1+ native tool: query sets / search configurations / judgments / experiments; three judgment sources incl. [[User Behavior Insights|UBI]] COEC implicit judgments and LLM-as-judge; unique hybrid-search grid-search optimization; imports Quepid CSV; Dashboards visualizations in 3.2); [[Elasticsearch Relevance Studio]] (new — Elastic's experimental React+Flask lifecycle app over the ES Search API: scenarios / judgements / strategies / benchmarks; drag-slider judging; NDCG/Precision/Recall/MRR + unrated-doc reporting; headline **MCP server** for agentic AI workflows); [[Rated Ranking Evaluator]] (new — [[Sease]]'s open-source, CI/CD-oriented offline evaluation *library* for Solr/Elasticsearch; JVM/Maven modules, corpus→topics→query-groups→queries domain model, immutable version-over-version delta tracking, broad metric set incl. ERR/F-measure, RRE Server dashboard + RRE Enterprise; resolves a long-standing dead link).

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
