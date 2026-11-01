# E-commerce Search Best Practices

Most advice about product search is about techniques: synonyms, LTR, embeddings, LLM judges. The techniques matter less than the order you apply them in. A team that ships a dense retriever before it can measure relevance cannot tell whether the retriever helped. This is that order, put together from notes on [[E-commerce Search]] and the case studies around it.

---

## 1. Know Your Queries Before You Tune Anything

Product search traffic is a mix of very different problems. Baymard's [[Query Types]] separate exact-product queries ("iPhone 15 Pro Max") from category, feature, thematic, symptom, compatibility, use-case and inspirational ones. Most systems are built for the first two, and symptom, thematic and inspirational queries are where they fail. A fix for one type can hurt another, so classify first.

Volume matters as much as type. [[Relevance Program Setup]] splits traffic into head, torso and tail: head queries already have click data and reward small improvements, while tail queries have no click signal and are the hardest to judge. Segment everything you measure by these tiers.

The classification itself can be the first finding. When [[foodpanda - Classifying 300K Noisy Search Terms Across 16 Markets|foodpanda]] classified 300,000 search terms across 16 markets, the first pass put 37% into `Others`. That was not noise. It was Turkish offal dishes, Taiwanese beverage chains and food written in Lao script, which the label set had no words for. Two habits are worth stealing: collapse spelling variants to a canonical label before classifying, and read the residual bucket as a report on missing vocabulary. Their end product was also deterministic: an LLM helped write regex patterns and market-scoped brand lists, and no model ran in the serving path. See [[Query Classification]].

## 2. Build Measurement Before You Change Ranking

You can't improve what you can't compare. Set a baseline on the current system before any change, and measure every experiment as a delta from it ([[Relevance Program Setup]]). Choose one primary metric and one guardrail. [[NDCG]]@10 is the usual primary metric for graded e-commerce relevance, and tail-query coverage is a good guardrail, because it stops a team from improving the head while the tail regresses.

For labels, use a scale that captures shopping intent rather than text match. The [[ESCI Label Scheme]] grades a query–product pair as Exact, Substitute, Complement or Irrelevant. Substitutes and complements are the two near-misses specific to product search, and a binary scale has to merge them. A phone case is topically about the phone, but it doesn't answer a query for the phone. The grades are ordinal, so they can feed NDCG directly. [[Allegro]] modelled its judging guidelines on ESCI, and [[Etsy]] plans to split its "partially relevant" grade the same way.

LLM judges make labelling affordable at scale, but anchor them to human labels and check them where they are weakest. In Allegro's results, exact matches and complements were easy for the judge and fine distinctions among substitutes were not. Etsy's approach is the template: an LLM judge anchored to human labels, distilled into a model cheap enough for real-time ranking ([[How Etsy Uses LLMs to Improve Search Relevance]]). [[E-commerce Search Evaluation Datasets]] covers when public sets like ESCI and WANDS help, and why one catalog's results don't transfer to another.

A small team doesn't need much to start. [[Understaffed Search Team]] suggests a judgment set of a few hundred graded queries, a regular review of the worst-performing queries, a zero-results dashboard with alerting, and a basic A/B split. Interleaving is a lighter option where A/B testing isn't available yet.

## 3. Fix Findability Cheapest First

Vocabulary mismatch is the most common root cause of failure. Sellers write titles in one vocabulary and buyers search in another: "Bohemian Macramé Wall Hanging" has to surface for "boho wall art". The hub note's order of fixes is synonyms, then spelling correction, then query expansion, then dense retrieval. Don't jump straight to dense retrieval. The earlier steps are cheaper and easier to control ([[Synonyms and Vocabulary Management]], [[Spelling Correction in Search]]).

[[Zero Results]] are the easiest failures to fix. They are easy to detect and measure, and the [[Search Observability]] note calls the zero-result rate the one unambiguous failure signal. [[Query Relaxation]] targets them directly. [[Rene Kriegler - Query Relaxation]] shows an ML-driven version for e-commerce.

Lexical ranking is worth a look before anything learned. Product data is unusual: six-word titles, one-token brands, attribute lists and repetitive merchant descriptions. [[Tuning BM25 for E-commerce Search]] concludes that per-field `k1`/`b` tuning can make sense, but not to expect miracles.

## 4. Watch Production for Silent Failures

A search system can return HTTP 200 well within its latency SLA while serving irrelevant results. Users abandon or reformulate, and neither triggers an alert. [[Search Observability]] watches three planes: user behaviour (zero-result rate, reformulation, abandonment, dwell), system health (latency, indexing lag, cache hit rate, shard health) and quality trends (NDCG on a locked reference set, run on a schedule).

[[Clicks Residual]] is the most useful single tool for finding which queries to fix. For each query it computes actual clicks minus attempts × the site's average CTR. Ranking queries by residual brings high-traffic failures to the top, where a plain low-CTR list would bury them in the long tail. Charlie Hull's e-commerce extensions add per-category CTR baselines, exit rate and business value for prioritising, and query clustering to catch whole failing families such as misspellings. It shows that a query fails, not why.

## 5. Let Business Signals In Without Losing Relevance

Margin, inventory, promoted listings and new-seller support legitimately affect ranking. Engagement signals are the default ranking proxy, but they favour listings that are already popular, whatever the query. The cleanest pattern separates the two kinds of relevance. [[Criteo]] uses [[Semantic Relevance]] as a guardrail threshold and [[Outcome-Based Relevance]] to order what passes it ([[Outcome-Based vs Semantic Relevance]]).

Keep business rules out of application code. [[Search Governance]] treats them as versioned policies (trigger, rule, priority) that business teams can author, test, promote and disable without a deployment. Because each policy is discrete, its effect can be measured: did the holiday turkey boost improve conversion? [[Results Merchandising]] and [[Results Boosting]] sit on that layer, and [[Two-Sided Marketplace Ranking]] covers catalogs supplied by sellers with their own commercial interests.

## 6. Give Broad Queries Variety

Head queries like "shoes", "necklace" or "bag" cover huge intent spaces. Ranking purely for relevance produces winner-takes-all results, where the most popular subcategory takes every slot. Detect broad queries, inject diversity, and make sure the result set covers several interpretations. Even clear queries suffer from near-duplicates: ten barely different black t-shirts are worse than three variations. Diversity has a sweet spot, and past it the results become incoherent. With [[MMR]] the λ trade-off is set empirically ([[Search Result Diversity]], [[Diversity Metrics]]).

## 7. Treat Facets and Autocomplete as Search

Facets are the main way people navigate a large catalog, and they force a choice. Hard filters suit navigational queries and soft preferences suit exploratory ones. A hybrid applies the hard filter and offers to include similar items ([[Faceted Search]]).

Facets are also a load problem. [[Zalando - Self-DoS via Facet Aggregation|Zalando's outage]] began on an ordinary Sunday. Facet aggregation queries, issued separately from result queries on every search, hit coordinator nodes when caches expired together. Query understanding probes that counted products added hidden load. The cluster stopped responding, and because the AI assistant depended on search, it went down too. The lessons: treat aggregation queries as a separate load class, add cache-stampede protection, and monitor coordinator nodes separately from data nodes.

Autocomplete and autosuggest are two problems with two backends: prefix completion of what the user is typing, and semantic suggestions when the intent is unclear. Use the engine's native suggester unless you need custom ranking ([[Autocomplete and Autosuggest]]).

## 8. Adopt ML in Stages

The [[Understaffed Search Team]] rule applies to everyone: rules before ML. Synonyms, boosts and query rewrites ship faster and are easier to audit than learned models trained on sparse data. Popularity boosting, [[Reciprocal Rank Fusion]] over existing rankers, and manual overrides for embarrassing failures need no training loop. Build a "giant UNDO button" too: disposable indices and aliased index versions that allow instant rollback.

For AI in the query path, the hub note describes four levels. Level 0 is keywords and filters. Level 1 makes an asynchronous suggestion ("did you mean: Property Type: Condo?") with no latency risk. Level 2 executes the rewritten query automatically, adding a few seconds. Level 3 is a multi-turn conversational interface. Start at Level 1, and move up only if an A/B test shows an improvement. [[Learning to Rank]] and fine-tuned embeddings come after you can measure them, which brings the list back to point 2.

---

## The Order, in One List

1. Classify queries by type and traffic tier.
2. Set a baseline, one metric and one guardrail, with ESCI-style labels.
3. Fix findability in cost order: synonyms, spelling, relaxation, then dense retrieval.
4. Monitor quality in production, not just uptime, and rank failures by click residual.
5. Keep business rules as governed, measurable policies.
6. Diversify broad queries.
7. Design facets and autocomplete as part of search, including their load.
8. Add ML one measurable step at a time.
