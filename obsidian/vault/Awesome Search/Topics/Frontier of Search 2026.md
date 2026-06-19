---
type: topic
title: "Frontier of Search 2026"
aliases: ["Agentic Search Frontier", "The New User of Search"]
tags: [topic, agentic-search, frontier, llm, retrieval, reranking, commoditization, neural-ir]
related_concepts: [Agentic Search, Direct Corpus Interaction, Purpose-Built Agentic Search Models, Agentic Query Workload, Reranking, Block-Max WAND, Late Interaction, ColPali, BBQ]
related_topics: [Frontier of Search, Frontier of Search 2025, Late Interaction in Elasticsearch, Conversational and Agentic Search, Reasoning Reranking, RL-Trained Search Agents, Elasticsearch vs OpenSearch, Search Platforms]
articles:
  - "[[Agentic Search Models with OpenSearch and Elasticsearch]]"
  - "[[The Scaling Dimensions of Keyword Search]]"
  - "[[This Is What Agentic Retrieval Looks Like]]"
  - "[[Beyond Semantic Similarity - Rethinking Retrieval for Agentic Search via Direct Corpus Interaction]]"
  - "[[Agentic search models]]"
companies: [Hornet, SID.ai, Bonsai, Elastic, Weaviate, Vespa]
people: [Jo Kristian Bergum, Skip Everling, Doug Turnbull]
created: 2026-06-18
---

# Frontier of Search 2026

The frontier of search in 2026 is moving in **two directions at once**, and it is a mistake to see only one of them.

**Up the stack — agents become the user.** Retrieval is increasingly consumed by agents that search on their own, nothing like people do. This drives two converging research-and-product fronts:

1. **Search systems built for the specific needs of agents** — infrastructure re-tuned for the agentic query workload.
2. **Purpose-built agentic LLMs for searching and reranking** — specialized models that orchestrate retrieval instead of general-purpose frontier models.

**Out to everyone — yesterday's frontier becomes commodity.** Just as importantly, the advanced neural retrieval that needed a research team a few years ago is now shipping as built-in features of mainstream engines. Ordinary teams get late interaction, multi-vector, learned sparse, quantization, and rerankers as *configuration*, not a project.

These are not the same story. The agentic shift is about a *new consumer* of search; the commoditization shift is about *who can wield* the previous cutting edge — and for most teams the second one matters more day to day. This topic tracks both. See [[Agentic Query Workload]] for the agentic shift and [[Late Interaction in Elasticsearch]] for the clearest example of the commoditization one.

---

## Search Systems Covering the Specific Needs of Agents

Retrieval infrastructure was built and tuned for human workloads — short queries, dozens per session, one string in a search box. Agents break every one of those assumptions, so a wave of work is re-engineering the serving side for them.

### What changes when the user is an agent
- **Query length & structure** — agent queries run 8–15 terms with web-search operators (phrase quotes, `site:`, `filetype:`, year ranges, `OR`, negation). GPT-5 used phrase quotes in 98% of BrowseComp-Plus sessions. (See [[This Is What Agentic Retrieval Looks Like]].)
- **Volume & multi-turn compounding** — a median of ~24 search calls per question; each call conditions the next, so retrieval misses compound across the session.
- **Cost sensitivity** — at thousands of queries per minute, the algorithm choice is a direct cost multiplier.

### Where current infrastructure strains
- **Dynamic pruning degrades.** [[Block-Max WAND]] can fall *below* exhaustive scoring past ~7 terms when query term weights are uniform — exactly the regime long agent queries push into. ([[The Scaling Dimensions of Keyword Search]].)
- **One-string search APIs** — a holdover from the human search box — can't express the constraints agents intend, and operators that web engines deprecated must come back.
- **Neural retrievers go out of distribution** — trained on short fluent MS MARCO / Natural Questions queries, they underperform on long structured agent queries.

### The emerging response
- **Workload-adaptive execution** — choose scoring/pruning strategy by query structure rather than a fixed pipeline. [[Hornet]] is explicitly building a retrieval engine for the volume, complexity, and variability of agentic workloads.
- **Higher-resolution interfaces** — [[Direct Corpus Interaction]] (DCI) drops the fixed similarity interface entirely and lets the agent search raw text with `grep`/`bash`, outperforming sparse, dense, and reranking baselines on agentic tasks. ([[Beyond Semantic Similarity - Rethinking Retrieval for Agentic Search via Direct Corpus Interaction]].)
- **Drop-in agentic layers over existing engines** — agentic models orchestrating standard [[OpenSearch]] / [[Elasticsearch]] backends via batched `_msearch`. ([[Agentic Search Models with OpenSearch and Elasticsearch]].)

---

## Purpose-Built Agentic LLMs for Searching and Reranking

The second front is the model itself. Rather than wrap a general frontier model (GPT-5, Sonnet, Gemini) in constraints and context engineering, train a **smaller model specifically on the search task** — rewrite, retrieve, rerank — and let it orchestrate simple retrieval primitives. See [[Purpose-Built Agentic Search Models]] for the full concept.

### Why specialize
- Frontier models nail the "80% case" but miss the **domain-specific last 20%** (e.g. "bistro tables" = small outdoor tables in a furniture store). They also treat "search" as near-flawless *web search*, unlike the focused backends most teams run.
- A specialized model is **smaller, faster, cheaper**, and converges in 2–3 turns where a general agent takes 7–8 — plus a dedicated [[Reranking|rerank]] turn.
- It **unbundles the retrieval monolith**: query classification, multiple backends, and reranking collapse into thin tool wrappers orchestrated by one model that sees the whole problem. ([[Doug Turnbull]], [[Agentic search models]].)

### The models
| Model | Maker | Notes |
|---|---|---|
| **[[SID-1]]** | [[SID.ai]] | First mover; OpenAI-compatible API; ~1.9x over embedding-only search; beats Gemini 3 Pro / Sonnet 4.5 / GPT-5.1 while ~24x faster and cheaper |
| Waldo | Glean | Enterprise search model |
| (corpus-tailored) | Charcoal | Tailors a model to your corpus |

### How they run in practice
A multi-turn tool loop against an existing backend: write several query variants → execute (batched) → pick the best, ignore noise → iterate → finish with a `report_helpful_ids`-style rerank turn. [[Bonsai]] demonstrates SID-1 dropped into a managed OpenSearch cluster in ~800 lines of code with no changes to the original search path. ([[Agentic Search Models with OpenSearch and Elasticsearch]].)

### Open questions
- Latency still rules these out for high-QPS site search today — but that is expected to change.
- Quality depends on training data matching the deployment domain; expect a *family* of domain-tuned models (e-commerce, legal, finance, job search) the way embedding models proliferated.
- Train-a-model (SID/Waldo) vs no-retriever-at-all ([[Direct Corpus Interaction|DCI]]) vs [[RL-Trained Search Agents|train-the-search-policy-with-RL]] are competing bets on where agentic retrieval intelligence should live.

---

## The Agentic Shift: Two Fronts

| | Search systems for agents | Purpose-built agentic models |
|---|---|---|
| **Layer** | Serving / infrastructure | Model / orchestration |
| **Question** | How do we serve agent queries efficiently? | How do we make the searcher itself smart about our domain? |
| **Examples** | [[Hornet]], DCI, workload-adaptive pruning | [[SID-1]], Waldo, Charcoal |
| **Key articles** | [[The Scaling Dimensions of Keyword Search]], [[This Is What Agentic Retrieval Looks Like]] | [[Agentic Search Models with OpenSearch and Elasticsearch]], [[Agentic search models]] |

Both fronts respond to the same fact: *within the agentic shift*, the new user of search is an agent. But that is only one of two shifts redrawing the frontier.

---

## Yesterday's Frontier Becomes a Built-In Feature

The agentic headlines obscure a quieter — and arguably broader — shift: the **commoditization of neural retrieval**. Techniques that required a research team a few years ago now ship as supported, configurable features of mainstream engines ([[Elasticsearch]], [[OpenSearch]], [[Vespa]], [[Weaviate]], Solr), usable by teams with no ML specialists.

- **Late interaction / ColPali as a feature.** [[ColBERT]]-style [[Late Interaction]] and visual [[ColPali]] retrieval are now first-class in Elasticsearch (8.18 `rank_vectors` + `maxSimDotProduct`) with a documented production playbook — bit vectors, average vectors, [[Token Pooling]], rescore retriever. A 2020 research artifact is a 2026 config option. See [[Late Interaction in Elasticsearch]].
- **Quantization built in.** [[BBQ]] / scalar / binary quantization live inside the engine, so billion-vector indexes fit in RAM without a custom serving stack.
- **Semantic & hybrid as defaults.** Learned sparse ([[ELSER]] / [[SPLADE]]), one-call semantic fields, hybrid retrieval with [[Reciprocal Rank Fusion|RRF]], and built-in reranker / inference endpoints turn yesterday's bespoke pipeline into checkboxes.

The pattern: the frontier doesn't only advance — it **descends**. Each year's research edge becomes the next year's default, and the population that can use it grows by an order of magnitude. For many teams the most consequential 2026 change isn't an agent at all — it's that capabilities once out of reach are now a setting they can switch on.

---

## Two Shifts, Not One

| | Agents become the user | Frontier becomes commodity |
|---|---|---|
| **Direction** | *Up the stack* — a new consumer of search | *Out to everyone* — the previous cutting edge as built-in features |
| **Driven by** | LLM agents emitting long, structured, high-volume queries | Mainstream engines absorbing neural-retrieval research |
| **Examples** | [[Hornet]], [[Direct Corpus Interaction]], [[SID-1]], purpose-built models | [[Late Interaction in Elasticsearch]], [[BBQ]], learned sparse, built-in rerankers |
| **Who benefits** | Autonomous agents | Ordinary teams, no ML specialists required |

The agentic story dominates the headlines, but it is only half the frontier. The other half is **democratization** — the lag between "research result" and "feature you can turn on" has collapsed to about a year. Watching only the agents misses where most of the practical value is actually landing.

---

## Adjacent Frontiers

Two more live edges feed directly into this shift and have their own topic pages:

- **[[RL-Trained Search Agents]]** — instead of *prompting* an LLM to search, train the search policy itself with reinforcement learning (outcome reward, token-level loss masking). [[Search-R1]] is the canonical framework. This is the "train the searcher" sibling to [[Purpose-Built Agentic Search Models]].
- **[[Reasoning Reranking]]** — the rerank step is now an LLM problem: listwise rerankers ([[RankGPT]]), fine-tuned LLM rerankers ([[RankLLaMA]], [[MonoT5]]), and reasoning/CoT judges. Agentic loops (and [[SID-1]]) terminate in exactly this step, and [[UDCG]] reframes its goal as removing distractors, not just ordering relevance.

---

## Related Concepts
- [[Agentic Query Workload]] — how and why agents query differently
- [[Agentic Search]] — the multi-turn plan/execute/verify paradigm
- [[Direct Corpus Interaction]] — raw-corpus retrieval as a frontier interface
- [[Purpose-Built Agentic Search Models]] — the specialized-model category
- [[Block-Max WAND]] — the keyword-pruning optimization under stress
- [[Reranking]] — the terminal step agentic models specialize in
- [[Late Interaction]] — research-grade retrieval now shipping as an engine feature
- [[ColPali]] — visual late interaction, commoditized in Elasticsearch 8.18
- [[BBQ]] — built-in quantization that makes billion-vector indexes ordinary

## Related Topics
- [[Frontier of Search]] — year-by-year index of the search frontier
- [[Frontier of Search 2025]] — the prior period (late interaction, embeddings economics, quantization)
- [[Conversational and Agentic Search]] — the adoption spectrum and conversational layer
- [[Elasticsearch vs OpenSearch]] — the backends agentic layers wrap
- [[Search Platforms]] — the engines being adapted
- [[Late Interaction in Elasticsearch]] — the clearest case of the frontier becoming a built-in feature
- [[RL-Trained Search Agents]] — training the search policy with RL (Search-R1)
- [[Reasoning Reranking]] — LLM / generative / reasoning rerankers

## Related Articles
- [[Agentic Search Models with OpenSearch and Elasticsearch]]
- [[The Scaling Dimensions of Keyword Search]]
- [[This Is What Agentic Retrieval Looks Like]]
- [[Beyond Semantic Similarity - Rethinking Retrieval for Agentic Search via Direct Corpus Interaction]]
- [[Agentic search models]]

## People
- [[Jo Kristian Bergum]] — [[Hornet]]; agentic query workload analysis
- [[Skip Everling]] — [[Hornet]]; scaling dimensions of keyword search
- [[Doug Turnbull]] — the case for agentic search models
