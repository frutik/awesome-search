---
type: video
title: "Relevance Feedback Inside the Search Engine"
speaker: "[[Evgeniya Sukhodolskaya]]"
company: "[[Qdrant]]"
medium: talk / video
url: https://www.youtube.com/watch?v=7E6Ls1Gk0-g
published: 2026-06-09
conference: "[[Berlin Buzzwords]]"
duration: 20:46
tags:
  - video
  - relevance-feedback
  - vector-search
  - hnsw
  - reranking
  - agentic-search
topics:
  - "[[Conversational and Agentic Search]]"
  - "[[Reasoning Reranking]]"
concepts:
  - "[[Relevance Feedback]]"
  - "[[HNSW]]"
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Dense Vector Retrieval]]"
  - "[[Reranking]]"
  - "[[Cross-Encoder]]"
  - "[[Knowledge Distillation]]"
  - "[[Learning to Rank]]"
  - "[[Position Bias]]"
  - "[[Presentation Bias]]"
tools:
  - "[[Qdrant Vector DB]]"
  - "[[qdrant-relevance-feedback]]"
people:
  - "[[Evgeniya Sukhodolskaya]]"
created: 2026-07-29
---

# Relevance Feedback Inside the Search Engine

📺 **Watch:** https://www.youtube.com/watch?v=7E6Ls1Gk0-g

Talk by [[Evgeniya Sukhodolskaya]] (Senior Developer Advocate, [[Qdrant]]) at [[Berlin Buzzwords]] 2026. The claim: every existing implementation of [[Relevance Feedback]] works *around* the search engine, because engines are black boxes. Qdrant owns its index, so it pushed feedback into the [[HNSW]] traversal itself — presented as the first vector-index-native relevance feedback API.

The mechanism shipped in **Qdrant 1.17.0** (February 2026). The talk gives the intuition and skips the maths; the formula, training procedure and [[BEIR]] numbers are in her companion article [[Relevance Feedback in Qdrant]], and the literature survey behind it is [[Relevance Feedback in Informational Retrieval]].

## Key Moments

| Time | Topic |
|---|---|
| [01:41](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=101s) | Three reasons out-of-the-box results aren't relevant |
| [03:04](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=184s) | Feedback loops as the intuitive fix — and 60 years of academia |
| [04:16](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=256s) | Who provides the feedback? Humans are lazy |
| [04:45](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=285s) | Move the loop inside the application; a model gives the feedback |
| [05:55](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=355s) | Three components of search — and the one nobody adapts |
| [06:27](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=387s) | Black boxes, and the literature's over-fetch-then-rerank workaround |
| [08:07](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=487s) | HNSW traversal recap |
| [08:49](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=529s) | Feedback inside the traversal: changing the hop function |
| [09:48](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=588s) | Three parameters, ~150 training examples |
| [10:17](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=617s) | Objective: distil the feedback model into the index |
| [10:42](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=642s) | The relevance feedback query API |
| [11:41](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=701s) | Tutorial, an agent skill, and a BEIR benchmark repo |
| [12:20](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=740s) | Two modes: cheaper reranking, or complementary |
| [13:10](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=790s) | Wrap-up: against black-box search engines |
| [14:36](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=876s) | Q&A: results never shown can never earn feedback |
| [17:32](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=1052s) | Q&A: position bias |
| [18:46](https://www.youtube.com/watch?v=7E6Ls1Gk0-g&t=1126s) | Q&A: graph topology and rebuilding the index |

---

## The Setup

Results come back not-quite-relevant for one of three reasons: the query was poorly formulated (*"which happens a lot in search, because you don't know what you're searching for"*), the collection holds no good match, or the scoring function isn't calibrated for your queries and documents.

Feedback loops are the intuitive fix, and every search user already runs one by hand: issue a query, judge the results, adapt, repeat. Deep-research agents do the same. In IR this is [[Relevance Feedback]] — *"a mechanism for the retrieval system to iteratively refine results in the direction of relevance"* — dating to Rocchio, roughly sixty years old.

### Humans won't do it

The obvious feedback source is the user, and it doesn't scale: *"people are lazy."* Google once shipped thumbs up/down on the results page and removed it — nobody pressed them.

So move the whole loop **inside** the application and let a model judge: an LLM, an agent, a smart reranker — anything that knows what's truly relevant. The user only ever sees the converged result set.

## The Component Nobody Adapts

Split search into three parts: the **query**, the **documents**, and the **function** matching one to the other.

- **Query** — everyone adapts this. Coding agents and deep-research loops reformulate and expand ([[Query Expansion]]; see [[Query Understanding - Query Rewriting Overview]]).
- **Documents** — you wouldn't rewrite the corpus per query.
- **The search algorithm** — barely touched, because engines don't let you.

> *"Search libraries, search engines are usually like black boxes. So you usually build around them. They don't allow you to access the index anyhow."*

The literature's workaround: pull as many candidates out of the black box as you can, rerank them with the feedback model, show the top. *"If they could they would rerank the whole storage of the documents"* — but they can't. See [[Reranking]].

## Feedback Inside the HNSW Traversal

Vanilla [[HNSW]] search is greedy: at each hop, pick the neighbour most similar to the query vector by cosine, repeat until convergence.

The change is to the hop-selection function. Instead of cosine similarity alone, the next node is chosen by a **combination of cosine similarity and the feedback from the previous loop's results** — so feedback bends the *path* through the graph rather than filtering its output. This is why the effect reaches the whole collection rather than a retrieved top-k.

Three trainable parameters trade off trust in the base retriever against trust in the feedback. In the companion article the score is

```
F = a · score + Σ_pairs confidence_p^b · c · delta_p
```

where `score` is the retriever's own similarity, and each feedback pair contributes a directional `delta` weighted by the feedback model's `confidence`. Roughly: `a` weights the original query direction, `c` how hard to pull toward relevant examples and push from irrelevant ones, `b` how sharply confidence is trusted.

Those parameters are **trained once** per *(feedback model, collection, retriever)* — **not per query**. In the talk she puts it at *"like 150 examples or so"*; the article's experiments use 50–6,000 domain queries depending on collection size, fitted by pairwise ranking loss. A framework ships the weights, so *"nobody needs a machine learning degree to use a search engine."*

### The objective is distillation

Train so that dense retrieval ranks the way the feedback model would — [[Knowledge Distillation]] straight into the index. The point is that the feedback model is one you could never afford to run over the whole collection. Anything that scores a query against a result qualifies: a [[Cross-Encoder]], a custom [[Learning to Rank]] model, a late-interaction model like [[ColBERT]], a bi-encoder, or an LLM.

## Using It

The query carries the target query, the feedback examples with their relevance scores, and the trained parameters. Three entry points: a [hand-written tutorial](https://qdrant.tech/documentation/tutorials-search-engineering/using-relevance-feedback/), a **relevance feedback agent skill** (part of Qdrant's search-engineering skills for agents — she ran it end-to-end with Claude, training included), and a benchmark repository on BEIR.

**Cost.** The formula itself is about as cheap as plain dense search; what costs is calling the feedback model. That yields two modes:

1. **Cheaper alternative to reranking** — collect a few feedback scores, distil, and let the index act as a ranker over a far larger candidate pool.
2. **Complementary to reranking** — combine both; on her BEIR runs this surfaces more relevant results.

Reported gains on [[BEIR]] subsets ([[MS MARCO]], SCIDOCS, Quora, FiQA-2018, NFCorpus), measured with a custom `abovethreshold@10` relevance-recall metric, span **−3.9% to +38.7%** relative depending on the retriever/feedback pairing. Full table and the conditions that decide the sign in [[Relevance Feedback in Qdrant]].

## Q&A

**Results never shown can never earn feedback.** Charlie's question: unreachable documents get no feedback by definition — is that a flaw? Yes, in the same way deep research has it: not enough human in the loop. It works if you trust the model's notion of relevance to match your users'. Her own boundary — *not* for very human-oriented domains like [[E-commerce Search]], where you want a human in the loop; better for medical or scientific literature *"where the humans don't have enough energy to stay in the loop."* Compare [[Presentation Bias]].

**Storing feedback across queries.** Could feedback be persisted and reused at retrieval time to surface what earlier searches missed? Not currently — the loop just gathers results until the model says stop. She likes the idea ("iterative retrieval fixing") and ties it to [[Reinforcement Learning for Search]] over agentic loops. The API is a component; storage is the application's call.

**Position bias.** Does the feedback account for it? Depends on the feedback model — some rankers are trained for it. But bias remains structurally: only top results are sent for feedback, because you can't afford latency or cost on more. See [[Position Bias]].

**Graph topology and rebuilds.** Since the loop depends on graph structure, especially upper layers, should the index be rebuilt to absorb feedback? It's rebuilt anyway as data arrives, and full rebuilds are expensive — *"HNSW is a precise structure but kind of heavy"* — so rebuilding for a couple of accuracy points likely isn't feasible. She is explicit the formula *"is not set in stone."*

## The Argument

> *"I don't like the idea that the search engines are black boxes that you have to build around. Search engines are here just to serve you a useful tooling and adapt to your needs and adapt to your users, be they humans or agents."*

## Related

- Concept: [[Relevance Feedback]] — this talk adds the index-native variant alongside explicit / pseudo / implicit
- [[HNSW]] — the traversal being modified · [[Approximate Nearest Neighbor Search]] · [[Dense Vector Retrieval]]
- [[Reranking]] · [[Cross-Encoder]] — what the feedback model usually is, and what this partly replaces
- [[Knowledge Distillation]] — the training objective · [[Learning to Rank]]
- [[Position Bias]] · [[Presentation Bias]] — the standing limits on any feedback loop
- Articles: [[Relevance Feedback in Qdrant]] — the formula, training and benchmarks · [[Relevance Feedback in Informational Retrieval]] — the literature survey behind the argument
- Same speaker: [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]]
- [[Qdrant]] · [[Qdrant Vector DB]] · [[qdrant-relevance-feedback]] · [[Berlin Buzzwords]]
