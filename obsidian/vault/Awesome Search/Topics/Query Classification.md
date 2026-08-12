---
type: topic
title: "Query Classification"
aliases: ["query categorization", "search term classification", "classification for query understanding", "query taxonomy assignment"]
tags: [topic, query-understanding, classification, taxonomy, llm, e-commerce-search]
related_concepts: [
  "[[Query Understanding]]",
  "[[Query Types]]",
  "[[Search Intent]]",
  "[[Search Scopes]]",
  "[[Hypothetical Document Embeddings]]",
  "[[Knowledge Distillation]]",
  "[[Out-of-Vocabulary]]",
  "[[Intent Drift]]",
  "[[Judgment Lists]]",
  "[[Query Specificity]]"
]
related_topics: [
  "[[Query Understanding in Practice]]",
  "[[E-commerce Search]]",
  "[[Multilingual Search]]",
  "[[Synonyms and Vocabulary Management]]",
  "[[Search Observability]]"
]
articles: [
  "[[Don't Classify, Hallucinate]]",
  "[[Query Understanding - Query Scoping]]",
  "[[Ecommerce Search UX - 8 Query Types]]",
  "[[Classic ML to Cope with Dumb LLM Judges]]",
  "[[Semantic Equivalence of e-Commerce Queries]]",
  "[[Metadata - The 3rd Kind of Retrieval]]",
  "[[Semantic Search Without Embeddings]]",
  "[[Fine-Tuning Qwen3 Embeddings for Product Category Classification]]",
  "[[Query Understanding - Entity Recognition]]",
  "[[Query Understanding - Language Identification]]",
  "[[Query Understanding - Taxonomies and Ontologies]]",
  "[[You Say Search I Say Recs - Spotify Agentic Query Understanding]]",
  "[[Food Discovery with Uber Eats - Building a Query Understanding Engine]]",
  "[[Broad and Ambiguous Search Queries]]"
]
people: ["[[Doug Turnbull]]", "[[Daniel Tunkelang]]", "[[Hailey Cheong]]"]
companies: ["[[Delivery Hero]]", "[[Etsy]]", "[[Uber]]", "[[Spotify]]", "[[Baymard Institute]]"]
created: 2026-08-12
---

# Query Classification

Assigning a query to a label from a fixed vocabulary — an intent, a query type, a catalog category, a brand, a downstream service. It is the most deployed piece of [[Query Understanding]] and the least discussed, because the interesting difficulty is rarely in the model. It is in the **label set**: production classifiers fail at the seam between what the model can emit and what the system will accept.

---

## What actually gets classified

Five jobs are routinely called "query classification" and have different label spaces, owners, and consumers:

| Job | Label space | Owner | Consumed by |
|---|---|---|---|
| **Intent** | ~3–10 flat classes (navigational / informational / transactional / …) | search team | retrieval strategy, UI treatment |
| **Query type** | ~8–12 structural classes (exact, feature, use case, symptom, non-product …) | search team | evaluation sampling, ranking policy |
| **Catalog category** | hundreds to tens of thousands of hierarchical nodes | merchandising / catalog | scoping, filtering, boosting |
| **Attributes and entities** | open-ended (brand, colour, material, dietary, market-local names) | catalog + local ops | facet pre-selection, implicit filters, attribute-match ranking |
| **Constraint strength** | binary per facet (hard filter vs. soft preference) | search team | whether a selection eliminates or merely demotes |

The first two are covered by [[Search Intent]] and [[Query Types]]. The third is [[Search Scopes]] — [[Daniel Tunkelang]]'s [[Query Understanding - Query Scoping]] frames it as deciding which part of the catalog a query should be searched against, and notes that getting scope right also determines which facets are worth showing. The fourth is treated as a retrieval strategy in its own right in [[Metadata - The 3rd Kind of Retrieval]], where "crimson suede couch" decomposes into colour, material and category, each with its own similarity function. The fifth comes from [[Facets - Constraints or Preferences]]: whether a user's facet selection means "only this" or "preferably this" is itself a prediction over user, query and facet.

---

## The central tension: closed vocabulary, open traffic

A classifier's output must land in the system's legal vocabulary — you cannot boost a category that does not exist, or filter on a brand ID you invented. But query traffic is open: users type transliterations, local brand nicknames, single characters, and things the taxonomy has no word for.

Every production approach is a way of resolving that mismatch, and the two clearest recent examples resolve it in opposite directions:

- **Loosen the model, then snap it back.** In [[Don't Classify, Hallucinate]], [[Doug Turnbull]] stops shipping the taxonomy to the LLM at all. A cheap model invents a plausible-but-fake category path for the query, and an embedding lookup resolves that invention onto the nearest real node. The vocabulary constraint moves out of the prompt and into a similarity step.
- **Tighten the taxonomy until it fits the traffic.** In [[foodpanda - Classifying 300K Noisy Search Terms Across 16 Markets]], 37% of terms landed in an `Others` bucket — not because the classifier was weak, but because the label set was too anglocentric for 16 markets. The fix was iterating the vocabulary and canonicalising query variants, not swapping the model.

Both are correct. Which one applies depends on whether your taxonomy is *right but unwieldy* or *wrong for your traffic*.

---

## The residual class

Every classifier needs somewhere to put what it cannot label. That bucket is the most informative output the system produces, and the most commonly misread.

- **A large residual is a vocabulary report, not a noise measurement.** At foodpanda the `Others` bucket held Turkish offal dishes, Taiwanese beverage chains, and food written in Lao script — real demand with no label.
- **Classification rate is a coverage metric, distinct from accuracy.** A model can be highly accurate on what it labels and still leave a third of traffic dark. Track both; they move independently.
- **Driving the residual to zero is not automatically a win.** Forcing a label onto every term converts unknown coverage into unknown error. foodpanda mitigated this by having the model assign the residual a graded confidence (33% / 66% / 99%) of belonging to a category rather than a hard label.

The taxonomy side of the same gap is documented from the UX end in [[Ecommerce Search UX - 8 Query Types]]: the query types sites handle worst are precisely the ones a category taxonomy has no node for — non-product searches (66% of sites have issues), abbreviation and symbol searches (54%), use case searches (43%). Downstream, the same gap surfaces as [[Zero Results]] and [[Out-of-Vocabulary]] terms.

---

## The method ladder

Roughly ordered by cost per query and by how much vocabulary drift they absorb:

1. **Keyword and regex rules.** Cheap, deterministic, auditable, blind to anything not enumerated. Still the right answer for global brands and closed attribute lists.
2. **Behavioural association.** Learn query→category associations from historical engagement rather than from text at all. The classical approach to scoping in [[Query Understanding - Query Scoping]]; its stated failure cases are ambiguous queries spanning several categories and rare queries with too little history to be confident. Strong on the head, useless on the tail.
3. **Supervised classifier.** Trained on labelled or behaviourally-derived data. [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] is a worked example: LoRA over a 0.6B embedding model, 6 classes, macro F1 0.836 — with labels taken free from merchant SEO markup rather than annotators.
4. **Embedding nearest-neighbour against label text.** Embed the label paths once; embed the query; take the nearest. No training, degrades gracefully, but query text and category text sit in different registers ("brown coffee table" vs. a four-level path).
5. **LLM zero-shot with the taxonomy in the prompt.** Structured outputs constrain the model to legal values. Works, but the schema rides along on every call, and large taxonomies hit provider limits on enumerated values.
6. **Generate-then-resolve.** Let the model produce a free-form hypothetical label, then resolve it into the real vocabulary by similarity — the [[Don't Classify, Hallucinate]] pattern. The register mismatch of (4) is fixed by making the LLM write in category register first. Structurally the same manoeuvre as [[Hypothetical Document Embeddings]], aimed at a taxonomy instead of a corpus.
7. **Ensemble of deliberately dumb calls.** Rather than one constrained expert call, run many cheap single-attribute judgements and let classical ML combine them. [[Classic ML to Cope with Dumb LLM Judges]] does exactly this on the same WANDS dataset: per-attribute LLM verdicts become features, a decision tree learns the weighting, and precision goes from 91.7% on one strong prompt variant to 96.7% over 40% of pairs. Each call stays simple and cacheable.
8. **LLM at build time, rules at run time.** Use the model to *author* the classifier, ship something deterministic. foodpanda's final artifact was a BigQuery classifier of regex patterns, country-scoped brand lists, and keyword lists — no LLM in the serving path. A form of [[Knowledge Distillation]] where the student is a rule set rather than a smaller model.

| | Cost/query | Vocabulary safety | Cold start | Absorbs drift |
|---|---|---|---|---|
| Rules | ~0 | Guaranteed | Manual | No |
| Behavioural | ~0 at serve | Guaranteed | Needs traffic history | Recompute |
| Supervised | Low | Guaranteed | Needs labels | Retrain |
| Embedding kNN | Low | Guaranteed | Immediate | Re-embed labels |
| LLM + structured output | High | Guaranteed | Immediate | Yes |
| Generate-then-resolve | Low–medium | Guaranteed by the resolve step | Immediate | Yes |
| Dumb-call ensemble | Medium, cacheable | Guaranteed | Needs labelled pairs | Retrain the combiner |
| LLM-authored rules | ~0 | Guaranteed | Build-time effort | Re-author |

Note what the last column costs: everything that absorbs drift automatically also drifts silently.

---

## Where the LLM sits

The sharpest architectural question is not *which model* but *when it runs*.

- **Run time.** Every query pays latency and cost; behaviour changes when the provider updates the model; the taxonomy can be edited without redeploying anything.
- **Build time.** The LLM is an authoring tool. The shipped artifact is inspectable and free to run, which matters at the head of the distribution where terms are stable and volume is enormous. Re-running the authoring loop is a deliberate, reviewable act.
- **Hybrid, by frequency.** Distributions are heavy-headed: the head can be a frozen lookup table built offline, with a live model reserved for the tail. This mirrors the head/torso/tail split in [[Query Types]] and the specificity gradient in [[Query Specificity]].

---

## Classification as routing

The label does not always select a filter. Sometimes it selects **which system answers at all**.

[[You Say Search I Say Recs - Spotify Agentic Query Understanding]] puts an LLM router in front of the query: exploratory requests like "new releases for me" or "similar artists to X" are classified as recommendation problems and delegated to the recommendation API, while the rest go to search. Reported gains are large precisely because the previous system had no way to express "this is not a search query": +115% on similar-artist discovery, +91% on new releases, +25% on broad music searches.

Two consequences for classifier design:

- **Routing raises the cost of a mistake.** A wrong category boost degrades a result set; a wrong route sends the query to a system that cannot answer it at all. Routing classifiers want precision and an explicit abstain path more than coverage.
- **The label set now spans teams.** Search and recommendations usually have separate owners, metrics and evaluation harnesses, so the routing vocabulary is a contract between them rather than a search-team artifact.

The same pattern appears at smaller scale wherever classification chooses a retrieval strategy — lexical vs. semantic vs. metadata matching, as laid out in [[Metadata - The 3rd Kind of Retrieval]].

---

## Canonicalise before you classify

Classifying raw traffic makes the model resolve variant spellings and the label simultaneously. Splitting the two is usually cheaper and always more debuggable.

foodpanda hit this directly: "McDonald's" appears as `mc`, `mcd`, `麥當勞`, and 1,355 further variants, and the model was over-matching on fragments — reading "pu" in the Philippines as Puregold while missing "panda" → Pandamart. Their fix was an intermediate cleanup step grouping variants under a canonical label *before* reclassification.

[[Semantic Equivalence of e-Commerce Queries]] gives the principled version of that step. Two queries are equivalent if a user would be equally satisfied by either result set — measured by aggregating clicks into per-query vectors over items, or by fine-tuning a bi-encoder on equivalent/non-equivalent pairs. The hybrid is the useful part here: use behavioural similarity on high-traffic pairs as weak supervision, then apply the trained model to the low-traffic queries where behaviour is too sparse to help. That is the same head/tail division that governs where the LLM sits.

---

## Multilingual and noisy traffic

Multi-market search breaks classifiers in ways single-market benchmarks never show:

- **Language identification comes first.** [[Query Understanding - Language Identification]] notes the compounding problem: short queries carry little signal, users mix languages within one query, and brand names look identical across languages — yet nearly every downstream step depends on getting it right.
- **Market-scoped ambiguity.** The same string means different things per market, so the label set must be scoped by market rather than shared globally. A single character can simultaneously be a brand abbreviation, a typo, and a dead end.
- **Script and cognate gaps.** Terms with no English cognate fall into the residual by default. See [[Multilingual Search]].
- **Domain vocabulary churn.** [[Query Understanding - Entity Recognition]] makes the general case: search vocabularies move fast and are dense with proper nouns, product identifiers and abbreviations that general-purpose models handle poorly.

---

## Labels are not stable

A classifier is usually treated as a fixed function and is not one.

- **Seasonal reinterpretation.** [[Query Understanding - Seasonality]] observes that the same query carries different intent by time of year, day of week, even time of day — so the *correct* label for a fixed string changes without the string changing.
- **Drift in the population.** [[Intent Drift]] covers the slower version: what users mean by a term migrates.
- **Catalog motion.** Categories are added, merged and renamed by a team that does not own the classifier. Every rename silently invalidates part of the label index.

A rising residual share is the cheapest early warning for all three — worth a dashboard, see [[Search Observability]].

---

## What you do with the label

Classification only pays off downstream, and the options are broader than filtering:

- **Scope retrieval** — restrict or boost within a category ([[Query Understanding - Query Scoping]]).
- **Populate facets** — pre-select filters from detected attributes, as in [[Food Discovery with Uber Eats - Building a Query Understanding Engine]], where a NER query builder turns entities into implicit filters.
- **Route to a system** — search vs. recommendations, per above.
- **Show the interpretation to the user.** [[Incremental AI Adoption for E-commerce Search]] treats this as a deployment ladder: level 1 suggests an interpretation asynchronously after results load, level 2 executes it and displays "Interpreted as: Property Type: Condo". Surfacing the label converts a silent classifier error into a correctable one.
- **Decline to commit.** For broad and ambiguous queries the right response is diversity, not a confident label — see [[Broad and Ambiguous Search Queries]], [[Targeting Broad Queries in Search]] and [[Etsy - Search Quality and Query Understanding]].

---

## Evaluation

Query understanding is upstream of retrieval, so classifier metrics alone are never sufficient.

- **Coverage** — share of traffic (and of *distinct* terms) receiving a label. Report both; they diverge sharply on heavy-headed traffic.
- **Accuracy on a sample** — a labelled sample stratified by head/torso/tail and by market, not a uniform draw. See [[Query Sampling]] and [[Judgment Lists]].
- **Downstream effect** — the only metric that matters commercially. Does the label change retrieval, and does that change help? Zero-results rate and NDCG, not classifier F1.
- **Hierarchical credit** — a four-level taxonomy makes flat accuracy misleading; a prediction wrong at the leaf but right at the parent is not the same failure as one wrong at the root.
- **Qualitative triage** — [[Query Triage - The Secret Weapon for Search Relevance]] applies classification to *failures* rather than queries: a cross-functional group categorises bad queries against a shared vocabulary. It is the fastest way to discover that your label set is the problem.
- **Residual watch** — a rising `Others` share is an early signal of catalog or market drift. See [[Search Observability]].

---

## Related

- [[Query Understanding in Practice]] — the surrounding pipeline; classification is its annotation layer
- [[Query Types]] / [[Search Intent]] — the two small-vocabulary classification jobs
- [[Query Understanding - Taxonomies and Ontologies]] — where the label sets come from
- [[Semantic Search Without Embeddings]] — the argument for taxonomies as the semantic layer, with LLM classifiers maintaining them
- [[Etsy - Search Quality and Query Understanding]] — broad queries where the right answer is diversity, not a single confident label
- [[Uber Eats - Scaling Search for Food Delivery]] — query annotation feeding implicit filters in a live system
- [[Synonyms and Vocabulary Management]] — the neighbouring vocabulary problem
