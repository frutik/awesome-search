---
type: topic
tags: [topic, personalization, user-modeling, embeddings, bandits, recommendations]
related_concepts: [Embeddings, Learning to Rank, Contextual Bandits]
related_topics: [E-commerce Search, Conversational and Agentic Search, Search Result Diversity, Query Understanding in Practice]
articles: []
companies: [Airbnb, Slack, Netflix, Spotify]
people: [Mihajlo Grbovic, Isabella Tromba]
---

# Personalization in Search

Personalization adapts search results to the individual user — their history, preferences, context, and intent — rather than returning the same ranked list for everyone. Done well, it dramatically improves relevance. Done poorly, it creates filter bubbles, cold-start failures, and privacy concerns.

---

## The Core Tradeoff

**Generic relevance** optimizes for the average user. **Personalized relevance** optimizes for *this* user right now. The gap between the two is largest when:
- User intent is ambiguous ("Python" — language or snake?)
- Users have strong, stable preferences (music taste, clothing style)
- The corpus is large enough that personalized re-ranking meaningfully changes the top-k

---

## Five Personalization Patterns

### 1. Contextual Bandits

Use a bandit (e.g., LinUCB, Thompson Sampling) to learn which results to promote for a user given their context (device, time, location, recency).

**When to use**: Click-through rate optimization; relatively stateless; fast feedback loops.  
**Limitation**: Doesn't model user taste deeply; optimizes short-term engagement.

### 2. User Embeddings

Encode a user's historical behavior (clicks, purchases, dwell time) into a dense vector. At query time, blend the user embedding with the query embedding for retrieval or reranking.

**Airbnb** uses listing embeddings trained on booking sequences (word2vec-style on session data). User embeddings are the average of listings the user clicked/booked. At retrieval, the user vector biases the ANN search toward similar listing clusters.

**Slack** builds a "work graph" — a bipartite graph of users × channels × messages — and derives user embeddings from graph structure (co-membership, interaction frequency). Search personalization scores results by graph proximity between the querying user and the result's author/channel.

### 3. Sequential / Session Models

Model the query session as a sequence and use the prior queries to predict intent for the current query. Transformer-based session encoders are state-of-the-art.

**When to use**: Multi-turn search sessions; when reformulation rate is high (users struggle to articulate intent on first try).  
**Limitation**: Cold start within a new session; sequential models add latency.

### 4. Graph-Based Personalization

Use a knowledge graph or interaction graph (user–item–entity) to propagate signals. PersonalizedPageRank biases random walks toward entities the user has interacted with.

**When to use**: Domains with rich entity structure (e-commerce with categories + brands; knowledge graphs).

### 5. Collaborative Filtering Signals in Ranking

Embed CF signals (users who searched X also clicked Y) as features in an LTR model. Weaker personalization than explicit user embeddings, but easy to implement as an additional feature.

---

## Cold Start

New users have no history. Strategies:
- **Demographic fallback**: Segment by device, locale, referral source; use segment-level defaults.
- **Onboarding signals**: Explicit preference collection at signup (Spotify's taste survey).
- **Implicit early signals**: First query intent, first click — update user representation in real time.
- **Popularity fallback**: Serve the globally popular result until personalized signal accumulates.

---

## Personalization vs. Diversity

Personalization and diversity are in tension: a highly personalized ranker surfaces familiar items and suppresses serendipity.

**Spotify** resolved this by routing exploratory queries (detected via intent classifier) to a search+recommendations hybrid that deliberately injects unfamiliar results. Discovery is itself a personalization signal — users who engage with novel results get more of them.

See [[Search Result Diversity]] for the diversity side of this tradeoff.

---

## Privacy and Filter Bubbles

**Privacy**:
- Don't log PII in search queries without consent (medical, financial domains especially)
- User embeddings should be anonymized; avoid memorizing rare personal events
- GDPR / CCPA: users must be able to request deletion of their behavioral profile

**Filter bubbles**:
- Over-personalization can prevent users from discovering content outside their known preferences
- Inject diversity budget (e.g., 10–20% of results not explained by user history)
- Monitor coverage metrics: are certain content types systematically suppressed for certain user segments?

---

## Evaluation

Personalization is harder to evaluate offline than generic ranking:

| Method | Limitation |
|--------|-----------|
| Replay evaluation (logged clicks) | Position bias; doesn't reflect counterfactual |
| User-split A/B tests | Need large enough cohorts per segment |
| Interleaving | Better sensitivity than A/B; works for item-level preferences |
| Diversity-aware metrics (α-nDCG) | Measures coverage, not personal fit |

**Ground truth problem**: Personalization quality is inherently subjective. The best signal is long-term engagement (return visits, session depth), not single-query CTR.

---

## Implementation Checklist

- [ ] Define which signals you'll use: clicks, purchases, dwell time, explicit ratings
- [ ] Decide personalization layer: retrieval-time (query expansion / ANN bias) vs. reranking-time (score adjustment)
- [ ] Build cold-start fallback before launching personalization
- [ ] Add a diversity budget to the ranker
- [ ] Measure filter bubble effect: track result overlap across user sessions over time
- [ ] Privacy review: what's stored, for how long, and under what consent model?

---

## Further Reading

- [[Airbnb]] — listing embeddings + experiences reranking (Grbovic et al.)
- [[Slack]] — work graph embeddings for search personalization (Tromba et al.)
- [[Spotify]] — agentic LLM router for exploratory vs. focused search
- [[Mihajlo Grbovic]] — embedding-based personalization at Airbnb
- [[Isabella Tromba]] — search infrastructure and personalization at Slack
- [[Search Result Diversity]] — the counterbalance to personalization
- [[Conversational and Agentic Search]] — personalization within multi-turn sessions
