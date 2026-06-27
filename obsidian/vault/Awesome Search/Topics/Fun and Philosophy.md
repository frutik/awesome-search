---
type: topic
aliases:
  - philosophy of search
  - search philosophy
  - search metaphors
  - fun search
tags:
  - topic
  - philosophy
  - opinion
  - metaphor
related_concepts:
  - "[[Search Intent]]"
  - "[[Economics of Search]]"
  - "[[Diversity Metrics]]"
  - "[[Personalization]]"
  - "[[Search Governance]]"
  - "[[Search Evaluation]]"
  - "[[Agentic Search]]"
  - "[[UDCG]]"
  - "[[Position Bias]]"
  - "[[MMR]]"
  - "[[Search Architecture]]"
related_topics:
  - "[[Search Result Diversity]]"
  - "[[Economics of Search]]"
  - "[[Conversational and Agentic Search]]"
  - "[[E-commerce Search]]"
  - "[[Search Quality Assurance]]"
  - "[[Relevance Program Setup]]"
articles:
  - "[[Mutually Assured Distraction]]"
  - "[[How Etsy Uses Thermodynamics for Search]]"
  - "[[What is a Relevant Search Result]]"
  - "[[Search - Intent Not Inventory]]"
  - "[[Putting Search Ranking in Perspective]]"
  - "[[Thoughts on Search Result Diversity]]"
  - "[[Searching for Goldilocks]]"
  - "[[Rethinking Spotify Search]]"
  - "[[Search Koans]]"
people:
  - "[[Daniel Tunkelang]]"
  - "[[Doug Turnbull]]"
  - "[[Lester Solbakken]]"
  - "[[Max Irwin]]"
created: 2026-05-17
---
	
# Fun and Philosophy

Reflective, opinionated, and conceptually provocative writing about search — pieces that ask *what is search, really?* rather than *how do we tune the model?* Includes metaphors, thought experiments, ethical framings, and challenges to conventional assumptions.

---

## Core Philosophical Questions

### What is search *for*?
Most systems are built as inventory systems: find documents that match the query. [[Search - Intent Not Inventory]] argues this is the wrong frame — users search to accomplish goals, not to find documents. This reframes the entire design problem.

> [[Daniel Tunkelang]] — [Search: Intent, Not Inventory](https://medium.com/@dtunkelang/search-intent-not-inventory-289386f28a21) · blog: [queryunderstanding.com](https://queryunderstanding.com)

Related: [[Search Intent]], [[Query Understanding]], [[Conversational and Agentic Search]]

### What does "relevant" even mean?
[[What is a Relevant Search Result]] unpacks why "relevant = about the topic" fails in practice. Relevance is task-centered, comparative (relative to alternatives), and dynamic (changes over time). A result is relevant if it helps the user *verb the item* — accomplish their goal.

> [[Doug Turnbull]] — [What is a 'Relevant' Search Result?](https://opensourceconnections.com/blog/2017/03/08/what-is-relevant/)

Related: [[Search Evaluation]], [[Judgment Lists]], [[NDCG]]

### Who does search serve?
[[Economics of Search]] sits at the intersection of business rules, user needs, and platform incentives. Margin boosting, promoted listings, and seller support all legitimately affect ranking — but how far is too far?

Related: [[Search Governance]], [[Results Merchandising]], [[Results Boosting]], [[E-commerce Search]]

### What are we actually measuring?
[[Mutually Assured Distraction]] makes a sharp philosophical point: traditional IR metrics (nDCG, MAP, MRR) assume irrelevant documents are neutral. In agentic systems they are *harmful*. The [[UDCG]] metric assigns negative utility to distractors — a fundamentally different theory of what "good retrieval" means.

> [[Lester Solbakken]] — [Mutually Assured Distraction](https://hornet.dev/blog/mutually-assured-distraction) · company: [hornet.dev](https://hornet.dev)

Related: [[Search Evaluation]], [[Agentic Search]], [[Retrieval Pipeline]]

---

## Metaphors That Illuminate

### Thermodynamics
[[How Etsy Uses Thermodynamics for Search]] applies Shannon entropy to result diversity. Low entropy = narrow, converged results. High entropy = diverse, exploratory results. For broad queries like "geeky", high entropy is the goal. The metaphor reframes diversity as a measurable physical quantity, not a soft editorial preference.

> Etsy Engineering — [How Etsy Uses Thermodynamics to Help You Search for "Geeky"](https://codeascraft.com/2015/08/31/how-etsy-uses-thermodynamics-to-help-you-search-for-geeky/)

Related: [[Diversity Metrics]], [[Search Result Diversity]], [[MMR]], [[Query Types]]

### The Goldilocks Problem
[[Searching for Goldilocks]] frames diversity through the Wundt Curve: too little diversity wastes rank positions on near-duplicates; too much pushes relevant items down. Finding the optimum is NP-hard — [[MMR]] is the standard greedy approximation.

> [[Daniel Tunkelang]] — [Searching for Goldilocks](https://queryunderstanding.com/searching-for-goldilocks-b7f5c66c5cff)

Related: [[Diversity Metrics]], [[Search Result Diversity]], [[Thoughts on Search Result Diversity]]

### Mutually Assured Destruction
[[Mutually Assured Distraction]] borrows from Cold War deterrence theory: as retrievers and reasoners both improve, the system becomes *less* reliable — sophistication amplifies distractor-induced failure.

> "You cannot reason your way out of bad context, and you cannot compute your way out of distraction."

Related: [[Agentic Search]], [[LLM as Judge]], [[Retrieval Pipeline]]

### The Priority Stack
[[Putting Search Ranking in Perspective]] argues that ranking is the *last* lever to pull, not the first. Query understanding → binary relevance → query-independent signals → personalization → query-dependent signals. Most teams invest in ranking too early.

> [[Daniel Tunkelang]] — [Putting Search Ranking in Perspective](https://dtunkelang.medium.com/putting-search-ranking-in-perspective-1b3094e38105)

Related: [[Learning to Rank]], [[Query Understanding]], [[Personalization]], [[Position Bias]]

---

## Ethical and Social Dimensions

### Diversity and Filter Bubbles
Surfacing diverse results is not just a quality metric — it is an editorial choice about what users get to see. [[Thoughts on Search Result Diversity]] sits at the intersection of technical trade-offs and value judgments.

> [[Daniel Tunkelang]] — [Thoughts on Search Result Diversity](https://queryunderstanding.com/thoughts-on-search-result-diversity-a6d2f2de1a99)

Related: [[Diversity Metrics]], [[MMR]], [[Personalization]], [[Search Governance]]

### Rethinking the Whole System
[[Rethinking Spotify Search]] shows what happens when a team questions every assumption about what search should do — not just how to tune it.

> Spotify Engineering — [Rethinking Spotify Search](https://engineering.atspotify.com/2021/4/rethinking-spotify-search)

---


## Kōans and the Craft

Not every philosophical piece reaches for a grand metaphor — some just hold up a mirror to the daily contradictions of search work. [[Search Koans]] collects ~15 years of field stories as Zen-style kōans, each pivoting on an "identity of opposites": the irrelevant query no one searches, coverage that degrades relevance, better vectors that lose keyword highlighting, the search that breaks silently, and the child's question — *why can't the computer just do it?* The closing lesson is the discipline's deepest one: **relevance is human judgment and does not automate away.**

> [[Max Irwin]] — [Search Kōans](https://bonsai.io/blog/search-koans/) · company: [[Bonsai]]

Related: [[Search Problem Archetypes]], [[Search Quality Assurance]], [[Search Observability]]

## Key Voices

| Person | Blog / Site | Themes |
|---|---|---|
| [[Daniel Tunkelang]] | [queryunderstanding.com](https://queryunderstanding.com) | Relevance, diversity, intent, evaluation |
| [[Doug Turnbull]] | Softwaredoug blog | Relevance definition, BM25, practical search |
| [[Lester Solbakken]] | [hornet.dev](https://hornet.dev) | Agentic retrieval failure modes, UDCG |

---

## Related

- [[Search Result Diversity]] — diversity as both technical and ethical concern
- [[Economics of Search]] — who pays, who benefits, who controls
- [[Conversational and Agentic Search]] — intent-based search as the philosophical endpoint
- [[Search Quality Assurance]] — the tension between what we measure and what we value
- [[Books]] — deeper reading on these themes
