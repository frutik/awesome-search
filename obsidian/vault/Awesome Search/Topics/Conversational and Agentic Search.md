---
type: topic
tags: [topic, conversational-search, agentic-search, llm, rag, multi-turn]
related_concepts: [RAG, LLM, Query Understanding, Embeddings]
related_topics: [Query Understanding in Practice, Personalization in Search, Autocomplete and Autosuggest, E-commerce Search]
articles:
  - "[[Agentic Search for Context Engineering]]"
  - "[[Agentic Search as an Agile Engineering Process]]"
  - "[[You Say Search I Say Recs - Spotify Agentic Query Understanding]]"
  - "[[Superintelligent Retrieval Agent SIRA]]"
  - "[[Incremental AI Adoption for E-commerce Search]]"
  - "[[SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs]]"
  - "[[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]]"
companies: [Spotify, Elastic, Cohere]
people: []
---

# Conversational and Agentic Search

Search is shifting from single-turn keyword queries toward multi-turn dialogue and autonomous agent-driven retrieval. This topic covers the spectrum from conversational interfaces to fully agentic pipelines, along with the engineering and product tradeoffs at each level.

---

## The Adoption Spectrum

Spotify's framework for "incremental AI adoption" in search offers a useful mental model:

| Level | Description | Example |
|-------|-------------|---------|
| 0 | Classic keyword / BM25 | Legacy search boxes |
| 1 | Neural ranking / dense retrieval | Embedding-based ANN |
| 2 | LLM-enhanced query understanding | Intent classification, rewriting |
| 3 | LLM as ranker or reranker | Cross-encoder with LLM scores |
| 4 | Conversational interface | Multi-turn clarification |
| 5 | Agentic retrieval | Autonomous multi-step retrieval + synthesis |

Most production teams operate at levels 1–3. Jumping to level 5 without level 3 infrastructure typically fails.

---

## Conversational Search

### What Changes in Multi-Turn

In single-turn search, each query is independent. In conversational search:
- **Context carryover**: "What about their album from 2019?" requires knowing the prior query was about an artist.
- **Anaphora resolution**: "it", "they", "that one" must be resolved to entities from prior turns.
- **Reformulation tracking**: User may be refining, pivoting, or correcting — detect which.
- **Session state**: The system must maintain a session representation and update it cheaply per turn.

### Clarification Strategies

When intent is ambiguous, the system can:
1. **Ask**: "Did you mean X or Y?" — high precision but interrupts flow; use sparingly.
2. **Show and branch**: Present results for both interpretations with clear labels.
3. **Implicit disambiguation**: Use prior turn context to guess; reveal reasoning ("Showing results for jazz guitar because you mentioned Miles Davis earlier").

Rule of thumb: ask at most once per session; users abandon after two clarifying questions.

### LLM as Conversational Layer

An LLM can manage conversational context:
- Maintain a **running summary** of the session (cheaper than full context replay)
- Rewrite each new query with session context appended ("iPhone 13" → "iPhone 13 price in Malaysia, user previously browsed Samsung Galaxy")
- Use tool calls to invoke the underlying search index, then synthesize results

**Latency budget**: Each LLM call adds 200–800ms. For low-latency search UX, cache session state aggressively and limit LLM calls to query rewriting, not ranking.

---

## Agentic Search

### What "Agentic" Means

An agentic search system autonomously decides:
- *What* to retrieve (query formulation)
- *Where* to retrieve (which index, which tool)
- *How much* to retrieve (when to stop; when to retrieve again)
- *What to do* with results (synthesize, compare, route to another tool)

**Spotify** ships an LLM-based router that decides whether to handle a query with search, recommendations, or a hybrid blend. The router is trained on user intent labels derived from engagement data.

### SIRA Insight: Simplicity First

Meta / Rice University's SIRA paper showed that a single well-formed BM25 query outperformed complex multi-step retrieval agents on most benchmarks. The lesson: **orchestration overhead compounds errors**. Every retrieval step adds noise; agents that retrieve 4× and cross-reference often perform worse than one precise retrieval.

**Practical implication**: Don't add agentic complexity until you've exhausted single-turn retrieval quality. An LLM that writes a better query is almost always cheaper and more reliable than an agent that retrieves, reflects, and retrieves again.

### RAG in Agentic Pipelines

For document-synthesis tasks, agentic RAG typically:
1. **Decomposes** the user query into sub-questions
2. **Retrieves** per sub-question
3. **Filters** retrieved chunks (Clean Context principle: high precision > high recall)
4. **Synthesizes** a final answer

**Clean Context** principle (from agentic search research): feeding an LLM a smaller set of highly relevant documents produces better answers than flooding it with loosely related context. This implies a reranking step (cross-encoder or LLM-as-judge) before synthesis is more valuable in agentic pipelines than in classic search.

### Multi-Agent Search Architectures

For complex enterprise search (Slack, Notion, GitHub combined):
- **Orchestrator agent** decomposes the query and routes to specialized sub-agents
- **Sub-agents** each own one data source (email agent, code agent, wiki agent)
- **Merge layer** deduplicates and ranks results across agents

This is essentially federated search with LLM-mediated result fusion. The key engineering challenge is latency: fan-out to N agents in parallel, enforce hard timeouts, merge partial results.

---

## Search + Recommendations Boundary

As search becomes conversational, it overlaps with recommendations:
- "Find me something to watch" → recommendation problem with search UI
- "More like this" → similarity search + collaborative filtering
- "What should I look for?" → proactive suggestion, not reactive retrieval

**Spotify** explicitly routes these intents to different backends. The routing decision is itself a personalization decision (see [[Personalization in Search]]).

---

## Evaluation Challenges

| Challenge | Approach |
|-----------|---------|
| No single right answer | LLM-as-judge for answer quality; human eval for critical use cases |
| Session-level quality vs. turn-level | Track task completion, not just per-turn NDCG |
| Hallucination in synthesis | Citation accuracy; grounding verification |
| Latency compounding | Profile per-agent; enforce SLOs on each hop |

---

## Common Mistakes

- **Premature agentic complexity**: Adding multi-step retrieval before single-step retrieval is good enough. SIRA shows this regresses quality.
- **No fallback to classic search**: When LLM/agent fails or is slow, users need a degraded-but-functional keyword search path.
- **Session state explosion**: Storing full conversation history in context; use rolling summaries instead.
- **Ignoring citation quality**: In synthesis responses, broken or hallucinated citations erode user trust rapidly.

---

## Further Reading

- [[Spotify]] — LLM router for search vs. recommendations routing
- [[Query Understanding in Practice]] — intent classification as the foundation for routing
- [[Personalization in Search]] — session-aware personalization
- [[Autocomplete and Autosuggest]] — conversational entry points
- [[RAG]] — retrieval-augmented generation as the synthesis layer
- [[Search-R1]] — RL-trained multi-turn search-and-reasoning agent; the current frontier of agentic retrieval
- [[SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs]] — technical paper breakdown; token-level loss masking; PPO vs GRPO
- [[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]] — accessible RAG vs Search-R1 comparison