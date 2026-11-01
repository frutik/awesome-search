# Conversational Product Discovery

A chat window on a shop is easy to build. The arcturus-labs description of a conversational shopping agent is short: text in, text out, an inner loop of LLM and tool calls, and an outer loop of turns with the user. The existing search engine stays where it is, and the AI is a thin layer that turns intent into search calls. That last part is the catch. A conversational layer can only be as good as the search underneath it. What takes it past a search box is memory of the shopper, not the chat interface. This is the order in which to build it, put together from notes on [[Conversational and Agentic Search]], [[Agentic Memory]] and [[E-commerce Search]].

---

## 1. Conversation Is a Level, Not a Product

[[Incremental AI Adoption for E-commerce Search]] gives four levels. Level 0 is the keyword box with sidebar filters, which leaves the shopper to know the terminology and the filter structure. Level 1 keeps that search unchanged and adds an asynchronous "did you mean" bar that suggests a better filter and sort combination after the results load, with no latency risk. Level 2 runs the rewritten query automatically ("Interpreted as: Property Type: Condo") and adds 2–3 seconds. Level 3 replaces the search box with a stateful chat in which the agent clarifies, asks follow-ups and discusses results.

The [[Spotify]] framework in [[Conversational and Agentic Search]] puts a conversational interface at level 4 of 6, above neural retrieval, LLM query understanding and LLM reranking. Its observation is that most production teams operate at levels 1–3, and that jumping to the top without level 3 infrastructure typically fails. Both ladders give the same advice: start at the bottom, and move up only when the metrics improve. The arcturus test for accepting more latency is whether the AI saves the user a lot of effort.

## 2. Fix Single-Turn Retrieval First

The agent's tool is your search engine, so the agent inherits that engine's failures. Meta and Rice University's SIRA paper found that a single well-formed [[BM25]] query outperformed complex multi-step retrieval agents on most benchmarks. Every extra retrieval step adds noise, and agents that retrieve repeatedly and cross-reference often do worse. An LLM that writes a better query is almost always cheaper and more reliable than an agent that retrieves, reflects and retrieves again.

So the work from the companion essay on e-commerce search best practices comes first: vocabulary, zero results, measurement. Then keep a way out. When the LLM fails or is slow, users need a degraded but working keyword search path. That fallback appears in every source here as non-negotiable.

## 3. What Changes When Search Becomes a Conversation

In single-turn search each query stands alone. In a conversation, context carries over ("what about the blue one?"), references like "it" and "that one" have to be resolved, and the system has to tell whether the shopper is refining, pivoting or correcting. That needs session state that is cheap to update every turn.

A running summary of the session beats replaying the full history, and storing the whole conversation in context is a listed failure mode. Each LLM call adds 200–800 ms, so the note's advice is to cache session state aggressively and limit LLM calls to query rewriting, not ranking. [[Query Rewriting]] is the right place for the LLM: it is where an interpretation of the user's words becomes a query the engine can run.

## 4. Ask Sparingly

When intent is ambiguous there are three moves. Ask "did you mean X or Y?" Show results for both interpretations with clear labels. Or infer from earlier turns and say so ("Showing results for jazz guitar because you mentioned Miles Davis earlier"). Asking is the most precise and the most disruptive. The rule of thumb in [[Conversational and Agentic Search]] is to ask at most once per session, because users abandon after two clarifying questions. A good shop assistant asks less as they learn more, which leads to memory.

## 5. Remember the Shopper

This is what a search box cannot do. [[Agentic Memory for Search Personalization]] makes the case with one example. A shopper buys an orange backpack, returns it, and writes "too flashy for my work environment, I prefer neutral tones." A feature-based pipeline learns to decay the colour orange and loses two things. It loses the reason: someone who disliked orange would not have bought it, and the real signal is the work context. And it loses the alternative: "neutral tones" is the actionable half and has nowhere to live. Memory stores both as language. It also absorbs change, such as a student who becomes a professional or a shopper who starts buying for an infant, as a write rather than a retrain.

The architecture splits inference from serving. Offline, filter behaviour down to what defines a profile (purchases, explicit feedback, favourites), and have an LLM write preferences to long-term memory as facts. Online, read them, enrich the query (`backpack` becomes `backpack leather neutral professional`), retrieve, and rerank with the same context. The agent does not reason about preferences online. The operating rules follow from that split:

- Write memory asynchronously, never on the query path.
- Cap retrieval at the top 5–10 facts relevant to the current context.
- Set a TTL so stale preferences expire.
- Prefer soft boosts over hard filters, because a preference is evidence, not a constraint.
- Store aversions as affirmatives ("not flashy" becomes what the user does want), because embedding models handle negation poorly.

[[DICE]] frames the same idea from the domain side. The application's own ontology is the source of truth, not the prompt, and structured facts about the user are extracted from the conversation, persisted and injected into later turns. [[django-dice]] implements it for e-commerce preference inference. Its README pictures a shop assistant who already knows the store's brands, categories, price ranges and colours, and who greets a returning customer with "still looking for something for your husband?" rather than "what are you looking for today?" It makes the freshness trade-off a per-deployment switch. Inline extraction blocks the turn but applies a budget the shopper has just declared. Background extraction keeps turns fast and applies new preferences from the next turn.

## 6. Ground Recommendations in Commerce Signals

Matching the text is not enough. [[Criteo]] serves product recommendations to AI shopping assistants and argues that they should be judged by what shoppers do, not only by textual match. A content match is the entry ticket, but it doesn't reveal which of several matching products people buy. Its pipeline has two stages: KNN retrieval over [[CLEPR]], its commerce-tuned embedding model, then reranking that mixes content match with commerce scores and adds generated explanations ([[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]]).

In Criteo's offline benchmark over 400 candidates, ordering by the share of sales over the previous 7 days instead of CLEPR similarity raised the purchased product's normalized rank score from 0.029 to 0.074. In effect it is a popularity signal on top of semantic ranking. The figures are Criteo's own and offline only, and the authors decline to claim a conversion uplift. The pattern is the useful part: [[Semantic Relevance]] as a guardrail, [[Outcome-Based Relevance]] to set the order ([[Outcome-Based vs Semantic Relevance]]).

## 7. Agents Are a New Kind of User

The assistant also changes the load on search. The [[Agentic Query Workload]] differs from the human one. Agent queries routinely run 8–15 terms, they use operators such as phrase quotes and negation, and they come in volume: dozens of queries in a human session, potentially thousands for an agent testing hypotheses, with each miss compounding through the session.

The dependency also spreads failures. In [[Zalando - Self-DoS via Facet Aggregation|Zalando's outage]], the Elasticsearch cluster feeding both catalog search and the Zalando Assistant stopped responding. Campaigns went dark, and the assistant couldn't fetch products. Because the AI assistant depended on search, the outage did far more damage than a UX failure would have. Plan capacity and monitoring for the assistant as a client of search.

## 8. Evaluate Sessions, Not Turns

Per-query metrics can pass every turn of a failed conversation. [[Session-Based Evaluation]] shows the pattern: "iphone case" and "iphone 15 case" can both score well on [[NDCG]] while the shopper reformulates twice and leaves for a competitor. For conversational search, session-level evaluation is required, not optional. Track task completion, reformulations and abandonment. For agentic retrieval, ask whether the final answer was right, how many retrieval turns it took and whether the cost stayed within budget.

Generated answers need checks of their own. [[Conversational and Agentic Search]] pairs [[LLM as Judge]] for answer quality with human evaluation for critical cases, and adds grounding and citation checks, because broken or hallucinated citations quickly erode trust. Memory needs one more check: an asynchronous judge can compare the query, results and known preferences after the fact and catch mismatches, rather than silently serving a poor list.

---

## The Order, in One List

1. Climb the adoption ladder one A/B-tested level at a time, starting with an async suggestion.
2. Make single-turn retrieval good first, and keep a keyword fallback.
3. Keep session state as a rolling summary, and use the LLM for query rewriting.
4. Clarify at most once per session; infer from context and say so.
5. Remember the shopper: infer offline, apply online, boost rather than filter, expire stale facts.
6. Rerank on what shoppers buy, behind a semantic-relevance guardrail.
7. Plan capacity for the assistant as a heavy, failure-spreading client of search.
8. Judge whole sessions, and check the grounding of every generated answer.
