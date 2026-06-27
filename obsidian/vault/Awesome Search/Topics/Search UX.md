---
type: topic
aliases: ["search user experience", "search interface", "search design", "SERP design"]
tags: [topic, ux, search-ux, query-understanding]
related_concepts:
  - "[[Autocomplete]]"
  - "[[Faceted Search]]"
  - "[[Search Scopes]]"
  - "[[Zero Results]]"
  - "[[Position Bias]]"
  - "[[Presentation Bias]]"
  - "[[Query Types]]"
  - "[[Search Intent]]"
  - "[[Query Relaxation]]"
  - "[[Results Merchandising]]"
related_topics:
  - "[[Autocomplete and Autosuggest]]"
  - "[[Spelling Correction in Search]]"
  - "[[Query Understanding in Practice]]"
  - "[[E-commerce Search]]"
  - "[[Search Result Diversity]]"
  - "[[Conversational and Agentic Search]]"
articles:
  - "[[Query Understanding - Search Results Presentation]]"
  - "[[Query Understanding - Autocomplete and User Experience]]"
  - "[[Affordances for Conversational Search]]"
  - "[[13 Design Patterns for Autocomplete Suggestions]]"
  - "[[Facets of Faceted Search]]"
  - "[[Facets - Constraints or Preferences]]"
  - "[[Three Pillars of Search Quality - Discovery and Inspiration]]"
  - "[[Deconstructing E-Commerce Search - The 12 Query Types]]"
people:
  - "[[Daniel Tunkelang]]"
  - "[[Andreas Wagner]]"
created: 2026-05-31
---

# Search UX

Search UX is the design of the interaction loop between a user and a search system — from the moment they express a need to the moment they satisfy it (or abandon). Good search UX reduces the cognitive work the user has to do at every step: forming a query, reading results, refining, and recovering from failure.

---

## The Search Interaction Loop

Every search session follows a loop:

```
Need → Query formulation → Results scan → Click / Refine / Reformulate → Satisfied or Abandoned
```

UX decisions shape each transition. A user who can't formulate a query abandons before retrieval. A user who gets good results but can't read them fails at the scan step. UX failures compound — a poor autocomplete plus a bad results layout plus no facets equals a lost user.

---

## 1. Query Input UX

### Autocomplete and Autosuggest
The most impactful UX surface in search. Autocomplete reduces query formulation effort and steers users toward queries with good result coverage. See [[Autocomplete and Autosuggest]] for full coverage.

Key UX points:
- Show suggestions before the user finishes typing — not after submission
- Limit to 5–7 suggestions (more causes decision paralysis)
- Highlight the typed prefix so users see what they're completing
- Accepting a suggestion that returns zero results is a catastrophic UX failure — validate suggestions against the index

### Affordances: Showing Users What the System Can Do
[[Daniel Tunkelang]]'s **affordance gap**: users don't know what the system understands, so they either under-use it (keyword mode only) or over-trust it (natural language queries the system can't handle).

Autocomplete is itself an affordance — it reveals in-vocabulary queries. Conversational systems need equivalent mechanisms: structured clarifying questions ("Are you looking for X or Y?") are better than open-ended prompts because they communicate exactly what the system can distinguish.

See [[Affordances for Conversational Search]].

### Query Types Drive UX Expectations
Users arrive with different intents, and each type sets different UX expectations:

| Query type | User expectation | UX implication |
|---|---|---|
| Navigational | One correct answer | Show it first; don't bury it |
| Informational | Relevant content to read | Snippets matter more than titles |
| Transactional | Product to buy | Images, price, rating above the fold |
| Exploratory | Help me browse | Facets, categories, diversity |
| Ambiguous | System figures it out | Surface multiple interpretations |

See [[Deconstructing E-Commerce Search - The 12 Query Types]] for Baymard's full e-commerce taxonomy.

---

## 2. Results Presentation UX

How results are presented is as important as which results are returned. Two systems with identical retrieval quality can have very different user satisfaction based on layout alone.

### Layout: Match Format to Intent
- **List view** — informational and navigational queries (text-heavy, snippet-forward)
- **Grid view** — product and visual queries (images dominant, metadata secondary)
- **Hybrid** — show grid for category pages, list for specific item lookup

Adapt layout to device: mobile screens require fewer results above the fold, larger tap targets, and collapsed facets by default.

### Result Components
What to show per result depends on query type, but the generally important elements are:

| Component | Purpose | When critical |
|---|---|---|
| Title | Primary click signal | Always |
| Snippet | Relevance context | Informational, ambiguous |
| Image/thumbnail | Visual relevance check | Product, image queries |
| Price / rating | Trust + decision signal | Transactional |
| Highlighted terms | Explains why this matched | When query mapping is non-obvious |
| Availability | Prevents wasted clicks | E-commerce |

### Position Bias
Users click top results disproportionately regardless of quality — [[Position Bias]]. This creates a feedback loop: clicked results get labeled as "relevant" in training data, reinforcing rank. Consequences:
- Top results carry much higher responsibility than their position suggests
- A good result buried at position 8 may as well not exist for most users
- Counterfactual learning (IPS, DLA) is needed to de-bias training from click logs

### Adaptive Presentation
Intent-driven layout adjustments:
- Visual queries → thumbnails prominent
- Comparison queries ("X vs Y") → side-by-side or tabular layout
- Question queries → direct answer box before organic results
- Fresh-content queries ("today's news") → recency indicator on each result

---

## 3. Faceted Navigation UX

Facets are the user's primary tool for iterative refinement — they let users navigate a result set without reformulating their query.

### Constraints vs. Preferences (Tunkelang)
The most important facet UX concept: a facet selection can mean "must have this" (constraint) or "prefer this" (preference). Systems that treat all facets as hard constraints produce zero-result pages when users combine too many filters. Best practice: when facet combination produces zero results, relax the weakest constraint rather than showing an empty page.

### How Many Facets?
Users engage with 3–5 facets per session on average. Showing 20 facets doesn't help — it produces analysis paralysis. Guidelines:
- Show 5–8 most discriminating facets by default
- Collapse additional facets behind "More filters"
- Order facets by the degree to which they reduce the result set
- For exploratory queries, prioritize category/type facets over attribute facets

### Dynamic Facets
Advanced: show different facets depending on the query. "Shoes" → brand, size, color. "Laptop" → RAM, storage, screen size. Static facet panels with 20 attributes for every query is a lazy default, not good UX.

### The Facet Counting Problem
Each facet option should show a count of matching results. This must stay accurate as other facets are selected — users rely on counts to know if a filter is worth applying. Showing "0" next to a filter before the user clicks it prevents wasted interactions.

---

## 4. Zero Results: The Worst Failure

A zero-results page is the clearest UX failure. The user had a need; the system declared it unservable. Target: <2% zero-result rate.

### Why Zero Results Happen
- Spelling errors (user's fault, system's problem to fix)
- Over-specific queries (too many qualifiers)
- Vocabulary mismatch (user says "sneakers", index has "trainers")
- Over-filtered facets (too many constraints combined)

### Zero Results UX (Baymard's six elements)
1. Acknowledge the failure explicitly — say "No results for X"
2. Offer spell-corrected alternative — "Did you mean Y?"
3. Suggest a related category to browse
4. Show fallback content (bestsellers, popular in department)
5. Offer to relax the search / remove a filter
6. Provide a contact or help path

What not to do: silently redirect to homepage, show completely unrelated items, or leave the page empty with no navigation.

### Prevention Over Recovery
Better than recovering from zero results: prevent them. [[Autocomplete]] steers users toward in-vocabulary queries. [[Spelling Correction]] fixes errors at query time. [[Semantic Search]] bridges vocabulary gaps. Each layer reduces the chance a user reaches zero results at all.

---

## 5. Discovery UX

Not all search is lookup. [[Andreas Wagner]]'s **Three Pillars** framework distinguishes:

| Pillar | Question | UX goal |
|---|---|---|
| Findability | Can users find what they're looking for? | Precision, zero-results prevention |
| Discovery | Can users find things they didn't know they wanted? | Diversity, exposure, inspiration |
| Relevance | Are results actually good? | Ranking quality |

Discovery UX serves exploratory sessions — browsing, inspiration, gift search. Pure retrieval metrics miss it entirely. Good discovery UX:
- Presents result diversity (multiple interpretations, categories, price points)
- Uses visual merchandising to tell a product story
- Exposes inventory that pure popularity ranking would bury
- Measures exposure rate across catalog, not just top-result CTR

---

## 6. Measuring Search UX

| Metric | What it measures | UX signal |
|---|---|---|
| Zero-result rate | Findability floor | % of sessions that fail completely |
| CTR | Result page engagement | Are users finding something worth clicking? |
| Acceptance rate | Autocomplete utility | Are suggestions actually used? |
| Reformulation rate | Query friction | High rate = results didn't satisfy first try |
| Session abandonment | Session-level failure | User left without satisfying need |
| Average prefix length | Autocomplete efficiency | Shorter = suggestions kicking in earlier |
| Dwell time | Post-click satisfaction | Long dwell = useful result |

Session-level metrics are better than query-level for measuring UX: a user who submits three reformulations before finding the answer has had a poor experience even if the final query got a click.

---

## Related

- [[Autocomplete and Autosuggest]] — query input UX, full topic
- [[Spelling Correction in Search]] — preventing zero results at the query input layer
- [[Query Understanding in Practice]] — the backend that makes UX decisions possible
- [[E-commerce Search]] — UX patterns specific to product search
- [[Search Result Diversity]] — the Discovery UX angle
- [[Conversational and Agentic Search]] — the next evolution of search UX
- [[MOC - Search UX and Discovery]] — link-out index for this whole family
- [[Search Scopes]] — pre-query narrowing; scope-then-facet
- [[Search UX Research]] — the independent research orgs (Baymard, NN/g) whose findings ground these patterns
