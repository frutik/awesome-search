---
type: concept
title: "Query Routing"
aliases: ["routing", "query router", "semantic router", "RAG routing", "router", "hierarchical routing", "multi-route routing", "retriever routing", "hybrid routing"]
tags:
  - concept
  - rag
  - query-understanding
  - architecture
related_concepts:
  - "[[RAG]]"
  - "[[Query Understanding]]"
  - "[[Query Classification]]"
  - "[[Adaptive Retrieval]]"
  - "[[Vertical Selection]]"
  - "[[Federated Search]]"
created: 2026-09-05
---

# Query Routing

## Definition

Directing a query to one of several downstream paths based on its intent. [[Sami Maameri]]'s framing is deliberately unglamorous: **"routers are essentially just If/Else statements we can use to direct the control flow."** [[Roger Oriol]] defines it as a technique that takes the user's query and uses it to decide the next action "from a list of predefined choices."

Routing decides *which* index, tool, prompt or engine handles a query — as distinct from [[Query Classification]], which assigns a query to a taxonomy label. Classification is a labelling task; routing is a control-flow decision that may or may not use a classifier to make it. It is the archetypal "smart if-statement" workload that [[System One Model|System One models]] are pitched at.

## Why It Matters

Not every query should hit the vector index. Some are better served by structured filters, some by a keyword engine, some by a tool call, some by no retrieval at all. A single fixed pipeline forces one answer for every query; a router lets a system be several pipelines wearing a trenchcoat. It is the mechanism behind the "should we retrieve?" decision in [[LLM Guardrails]] and the per-query strategy choice in [[Agentic Search]].

Two arguments for it recur across sources:

- **Cost and latency.** Searching every source makes cost proportional to the number of sources ([[Query Routing - Direct Queries to the Right Source]]); selecting sources cut communication by up to 80.65% and latency by 52.50% at unchanged accuracy in [[Efficient Federated Search for RAG using Lightweight Routing|RAGRoute]]; complexity routing matched always-multi-step RAG at under half the time in [[Adaptive-RAG - Learning to Adapt Retrieval-Augmented LLMs through Question Complexity|Adaptive-RAG]].
- **Quality.** No retriever or strategy wins on every query ([[LTRR - Learning To Rank Retrievers for LLMs|LTRR]], [[Lightweight Query Routing for Adaptive RAG - A Baseline Study on RAGRouter-Bench|RAGRouter-Bench]]), fusion can rank below either of its inputs ([[Andrei Cristea - Qdrant Vector Search and Hybrid Routing|Qdrant's hybrid routing]]), and irrelevant context actively hurts — RAGRoute's random source selection scored below not retrieving at all.

## What Gets Routed

"Router" names the same mechanism over very different sets of routes:

| Routes are… | Example | Note |
|---|---|---|
| **Data sources / collections** | FAQ vs docs vs catalog vs tickets; hospital corpora in a federation | [[Query Routing - Direct Queries to the Right Source]], [[Efficient Federated Search for RAG using Lightweight Routing]] |
| **Web verticals** | News, images, local, shopping — or none | [[Vertical Selection]], the pre-LLM production form |
| **Retrieval strategies of different cost** | No retrieval / single-step / multi-step; Naive / Hybrid / Graph / Iterative RAG | [[Adaptive Retrieval]] |
| **Retrievers over one corpus** | Sparse vs dense vs RRF; BM25 vs E5 ± reranking | [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]], [[LTRR - Learning To Rank Retrievers for LLMs]] |
| **Encoders** | Domain-expert embedding models | [[RouterRetriever - Routing over a Mixture of Expert Embedding Models]] |
| **Retrieval policy** | Lexical / semantic / hybrid after business rules apply | [[Search Governance]] |
| **Systems** | Search vs recommendations | [[You Say Search I Say Recs - Spotify Agentic Query Understanding]] |
| **Tools** | Web search, a weather API | [[Build an Advanced RAG App - Query Routing]] |

Every choice needs a description; for LLM-based routers that description *is* the decision boundary, so it has to say precisely what each path is good for. In a RAG pipeline the router usually sits after query rewriting and guardrails; in [[Search Governance]] strategy routing runs after intent classification and business constraints.

## Router Types

| Type | How it decides | Cost |
|---|---|---|
| **LLM completion / selector router** | Model is prompted with every choice and its description and outputs one | LLM call |
| **LLM function-calling router** | Each choice is exposed as a tool; the model picks one | LLM call |
| **Semantic router** | Embedding similarity against example utterances (nearest example, or a per-route centroid of examples) | Embedding only — cheap |
| **Trained classifier** | A small model on labelled query→route pairs: T5-Large, a shallow neural net, an SVM over TF-IDF, a network over embeddings + n-grams + lexical shape | Small model inference |
| **Learning-to-rank router** | Ranks the candidate routes by predicted utility and takes the top | Model inference; may need post-retrieval features |
| **Zero-shot classification router** | A model assigns a label from a set; Oriol's version fine-tunes a small LLM on labelled query→route examples | Model inference |
| **Language classification router** | Detects query language, routes accordingly | Cheap (`langdetect`) |
| **Keyword router** | Matches keywords or regex patterns against route lists | Trivial |
| **Logical router** | Discrete checks — string length, file type, value comparisons | Trivial |

The list is ordered roughly by cost. Routing by embedding similarity rather than an LLM call is also what [[NeMo Guardrails - The Missing Manual|NeMo Guardrails]] does for its dialogue flows. If the router is an LLM, it adds latency to every request — worth budgeting before committing ([[Linear Score Combination]]).

**Cheap features go further than expected.** On RAGRouter-Bench, TF-IDF + SVM (93.2% accuracy) beat MiniLM sentence embeddings for predicting query type; Qdrant's router leans on n-grams and lexical shape signals alongside an encoder; web [[Vertical Selection]] started from keyword triggers. At Qdrant, an LLM router tried first mostly collapsed to the safe default (RRF), and a small trained classifier replaced it.

## Hard vs Soft Routing

A router can commit to one route or **weight** several:

- **Hard**: pick sparse *or* dense *or* RRF ([[Andrei Cristea - Qdrant Vector Search and Hybrid Routing|Qdrant]]).
- **Soft**: set the hybrid mixing weight α per query. [[DAT - Dynamic Alpha Tuning for Hybrid Retrieval in RAG|DAT]] has an LLM grade the top-1 result of BM25 and of dense retrieval and derives α from the two grades — up to ~7.5% Precision@1 over a fixed α on queries where the two retrievers disagree.
- **Budgeted**: allocate result slots by estimated intent, e.g. "80% semantic, 20% phrase" ([[RRF is Not Enough]]).

## Hierarchical (Cascade) Routing

Chain routers from cheapest to most expensive and stop at the first confident answer. [[Query Routing - Direct Queries to the Right Source]] sketches three levels: regex keywords (any hit wins), then an embedding router accepted above a cosine confidence of 0.85, then an LLM router only for the remainder. Logging which level decided each query lets routing accuracy be tracked per method; stored user corrections can override the router on repeat queries.

## Single vs Multi-Route

A router can pick one path or several. Questions that span topics, or whose answer differs by source, need multiple sources queried and consolidated into one answer — [[Build an Advanced RAG App - Query Routing|Oriol]] makes this a design decision to take up front; the Ailog guide scores every source and queries all above a relevance threshold; RAGRoute thresholds a per-source relevance probability. Contextual signals (developer vs customer, current page, open tickets) can also re-weight routes — a light form of [[Personalization]].

## Always Have a "None" Route

Every mature router has an abstain or default path: "no relevant vertical" (about a quarter of web queries in [[Sources of Evidence for Vertical Selection]]), "no retrieval" (Adaptive-RAG's label A, LTRR's R₀), the cascade's `default`. The costs of a wrong route are asymmetric — an irrelevant vertical block may annoy users more than a missing one, and a wrong route sends a query to a system that cannot answer it at all ([[Query Classification]]).

## Where Routing Labels Come From

A trained router needs query → best-route labels, and nobody annotates those by hand at scale. The recurring trick is **labelling by outcome**:

- Run every route and label with the cheapest one that answered correctly (Adaptive-RAG), or with each route's gain in answer quality over no retrieval (LTRR).
- Retrieve from every source, rerank jointly, and mark a source relevant if it placed a document in the global top-k — or have an LLM grade the retrieved documents (RAGRoute).
- Use dataset structure as a prior when outcomes are ambiguous (Adaptive-RAG labels unresolved single-hop questions B and multi-hop ones C).
- Past traffic as evidence: queries users typed directly into each vertical ([[Vertical Selection]]).

Label balance matters: Qdrant found a better-balanced route distribution produced a better classifier.

## Evaluating a Router

Three layers, which can disagree:

1. **Routing accuracy** — did it pick the labelled route? Adaptive-RAG's classifier is only ~55% accurate, yet the system matches always-multi-step F1 at under half the time, because most errors lean toward retrieving more than necessary.
2. **Downstream quality** — relevance, [[NDCG]], answer correctness. LTRR found that the utility metric used for labels decided whether gains were significant at all (Answer Correctness yes, BEM no).
3. **Cost** — tokens, latency, calls per query. RAGRouter-Bench's 28.1% token saving is *simulated* from a type-to-strategy mapping; RAGRoute measures communication and latency directly.

Always compare against **route-everything**, **route-nothing** and **random routing** — RAGRoute's random baseline scoring below no retrieval shows why the last one is not a formality. And check what the router needs to see: LTRR's post-retrieval features mean running every retriever first, which optimises quality but not cost.

## Classic IR Roots

Routing predates RAG by decades under other names:

- **Resource (collection) selection** in distributed IR / [[Federated Search]] — ranking which collections to query from sampled content (CORI, ReDDE, GlOSS).
- **[[Vertical Selection]]** in web aggregated search — deciding which verticals a query should trigger, from query strings, vertical query logs and vertical corpora ([[Sources of Evidence for Vertical Selection]], 2009). Query logs were the strongest single signal.

LTRR and RAGRoute both cite this lineage explicitly: RAG routing is resource selection with LLM answer quality as the objective.

## Implementations

- [[LlamaIndex]] — LLM Selector router, Pydantic Router; a Router Query Engine choosing among Query Engine Tools via a selector (single selector = exactly one tool)
- [[Haystack (deepset)]] — `ZeroShotTextRouter`, `TextClassificationRouter`, `ConditionalRouter`, `FileTypeRouter`
- [[LangChain]]
- `semantic-router` (standalone Python package), OpenAI Encoder, Hugging Face models, `langdetect`
- [[Sentence Transformers]] — embedding routers (e.g. `BAAI/bge-m3`)
- Research code: [Adaptive-RAG](https://github.com/starsuzi/Adaptive-RAG) · [RouterRetriever](https://github.com/amy-hyunji/RouterRetriever) · [LTRR](https://github.com/kimdanny/Starlight-LiveRAG)

## Related Concepts

- [[Adaptive Retrieval]] — routing between retrieval strategies of different cost
- [[Vertical Selection]] · [[Federated Search]] — the classic IR forms
- [[RAG]] · [[Query Understanding]] · [[Query Classification]] · [[Search Intent]]
- [[Agentic Search]] — routing chosen per step rather than once; Oriol calls agents the next stepping stone after routing
- [[Search Governance]] — strategy routing inside a policy layer
- [[LLM Guardrails]] · [[Search Scopes]]
- [[Hybrid Search]] · [[Reciprocal Rank Fusion]] · [[Linear Score Combination]] — hard and soft routing between retrievers
- [[Learning to Rank]] — routing as ranking the routes

## Articles

- [[Routing in RAG Driven Applications]] — [[Sami Maameri]]; the seven-router taxonomy
- [[Build an Advanced RAG App - Query Routing]] — [[Roger Oriol]]; router choices and types, with a LlamaIndex walkthrough
- [[Query Routing - Direct Queries to the Right Source]] — [[Ailog]]; keyword → embedding → LLM cascade, multi-route and contextual routing
- [[Adaptive-RAG - Learning to Adapt Retrieval-Augmented LLMs through Question Complexity]] — routing by predicted question complexity (NAACL 2024)
- [[Lightweight Query Routing for Adaptive RAG - A Baseline Study on RAGRouter-Bench]] — TF-IDF + SVM as a strong cheap baseline
- [[LTRR - Learning To Rank Retrievers for LLMs]] — routing as learning to rank retrievers, "no retrieval" included (SIGIR 2026)
- [[RouterRetriever - Routing over a Mixture of Expert Embedding Models]] — routing between domain-expert encoders (AAAI 2025)
- [[Efficient Federated Search for RAG using Lightweight Routing]] — RAGRoute; resource selection for federated RAG
- [[DAT - Dynamic Alpha Tuning for Hybrid Retrieval in RAG]] — soft routing via per-query hybrid weights
- [[Sources of Evidence for Vertical Selection]] — [[Jaime Arguello]], [[Fernando Diaz]], [[Jamie Callan]]; web vertical selection (SIGIR 2009)
- [[RRF is Not Enough]] — intent-based allocation between retrieval strategies
- [[Why Ecommerce Search Needs Governance and How It Improves Retrieval]] — strategy routing after governance
- [[NeMo Guardrails - The Missing Manual]] — embedding-similarity routing of dialogue flows

## Videos

- [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]] — [[Haystack EU]] lightning talk
