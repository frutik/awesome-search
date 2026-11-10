---
type: topic
aliases:
  - behavioural effects in search
  - behavioral effects in search
  - cognitive biases in search
  - psychological effects in search
  - user biases in search
tags:
  - topic
  - bias
  - behaviour
  - search-evaluation
  - e-commerce
related_concepts:
  - "[[Position Bias]]"
  - "[[Presentation Bias]]"
  - "[[Impression Bias]]"
  - "[[Click Models]]"
  - "[[Click Signals]]"
  - "[[Implicit Judgments]]"
  - "[[Learning to Rank]]"
  - "[[Exploration vs Exploitation]]"
  - "[[Autocomplete]]"
  - "[[LLM as Judge]]"
  - "[[NDCG]]"
related_topics:
  - "[[Search UX]]"
  - "[[Search UX Research]]"
  - "[[E-commerce Search]]"
  - "[[A-B Testing for Search]]"
  - "[[Search Quality Assurance]]"
  - "[[Personalization in Search]]"
articles:
  - "[[Why nDCG Misleads eCommerce Search]]"
  - "[[Query Understanding - Autocomplete and User Experience]]"
  - "[[Good Abandonment on Search Results Pages]]"
  - "[[Beyond Algorithms - Ranking at Scale at Booking.com]]"
  - "[[Roman Grebennikov - Personalizing Search Results in Real-Time]]"
  - "[[Do LLM Judges Actually Agree With Us]]"
created: 2026-11-10
---

# Psychological and Behavioural Effects and Biases in Search

People do not read a results page the way a ranking metric assumes. They look at the top more than the bottom, trust some sources more than others, let suggestions finish their query for them, click things they will never buy, and judge one product by what sits next to it. These effects shape what users choose, what clicks get logged, and therefore what every click-trained ranker and click-based metric learns. This topic gathers them in four groups: effects on the choice itself, biases in how results are examined, biases in what data gets collected, and the same biases showing up in experiments and machine judges.

---

## 1. Effects on the choice itself

These come from marketing and behavioural economics. They change *what a user decides*, not just what gets recorded.

- **Attention spillovers, halo effects and decoy effects.** [[Andreas Wagner]] reports products with many clicks and almost no sales (high CTR, low CVR) whose neighbours on the page appeared more likely to be purchased. His example: the latest iPhone draws clicks from people who cannot afford it, and the cheaper phones beside it start to look more appealing. If the effect is real, a product's value depends on what surrounds it, and ranking each product by its own conversion probability can produce a worse page. He stresses that this is correlation and needs controlled experiments. See [[Why nDCG Misleads eCommerce Search]].
- **Curiosity clicks.** The opposite reading of the same signal: in [[Roman Grebennikov]]'s Findify story, a giant bong rose to the top of a collection because everyone clicked it out of curiosity and nobody bought it. Weighting purchases above clicks sent it back down. See [[Roman Grebennikov - Personalizing Search Results in Real-Time]] and [[Learning to Rank]]. Together with Wagner's case, it shows that a high-CTR, low-CVR item can be noise to demote or a decoy that helps sell its neighbours, and the click log alone cannot tell which.
- **Anchoring on autocomplete.** [[Daniel Tunkelang]] notes that users anchor strongly on autocomplete, often picking a suggestion rather than finishing their own query, so suggestions effectively co-author the search. That is a lever for steering users to productive queries and a responsibility when suggestions are misleading or biased. See [[Query Understanding - Autocomplete and User Experience]] and [[Autocomplete]].
- **Social proof.** Items with more ratings and reviews get clicked more regardless of how well they match the query ([[Position Bias]]). Friends' purchases also appear as a personalization signal ([[Personalization]]).
- **Satisficing and "Google gullibility".** Users who stop at the first answer that looks good enough can trust an incomplete or wrong extracted snippet and leave misinformed, which turns good abandonment bad. See [[Good Abandonment on Search Results Pages]].

## 2. Biases in how results are examined

These change *which results get looked at*, which [[Click Models]] model as an examination probability separate from relevance.

- **[[Position Bias]]**: higher-ranked results get clicked more regardless of relevance, because they are examined more.
- **Cascade behaviour**: users read top to bottom and stop at the first satisfying result, so lower results are examined only if everything above failed.
- **Trust bias (in sources)**: users click trusted sources, such as Wikipedia or Amazon, even at lower ranks ([[Position Bias]]).
- **Position trust bias**: a separate, rank-linked variant. [[Beyond Algorithms - Ranking at Scale at Booking.com|Booking.com]]'s survey lists modelling it as position-dependent noise among the mitigations.
- **Grid and viewport effects**: on product grids attention drops in steps at row and viewport boundaries that differ by device, not along the smooth log curve [[NDCG]] assumes ([[Why nDCG Misleads eCommerce Search]], part 2).

## 3. Biases in what data gets collected

These come from the system, not the user's head, but they compound the effects above because they decide which behaviour is ever observed.

- **[[Presentation Bias]]**: users can only interact with what is shown, so unshown results never accumulate signal and the system entrenches its own choices.
- **[[Impression Bias]]**: whether an item was ever examined is set by the rankers used in the past, so new or low-ranked items stay unseen. Remedies need deliberate exposure ([[Exploration vs Exploitation]]); reweighting by rank alone cannot fix what was never observed.
- **User bias**: heavy users generate far more training rows and skew the ranker toward themselves ([[Beyond Algorithms - Ranking at Scale at Booking.com]]).
- **Exposure bias in click-trained labels**: the reason given in [[sQuIrRel - Large-Scale Evaluation of E-commerce Query Classification Models|sQuIrRel]] for not evaluating query classifiers on aggregated [[Click Signals|click data]].

## 4. The same effects in experiments and machine judges

- **Novelty and primacy effects** in [[A-B Testing for Search]]: users adapt to a new ranking over time, so a real improvement can look small in week one and a regression can be masked by novelty curiosity. Run long enough to wash these out.
- **LLM judges have biases too.** Zheng et al.'s MT-Bench work named position bias (preferring whichever option comes first), verbosity bias and self-enhancement bias among [[LLM as Judge|LLM-judge]] failure modes. Swapping option order across the sample measures the position effect. See [[Position Bias]] and [[Do LLM Judges Actually Agree With Us]].

## Why it matters

Most ranking objectives and offline metrics treat each result's value as its own property, discounted by position. The effects above break both halves of that assumption: position is not the only thing driving attention, and value can depend on neighbours. The practical responses recurring across these notes are to model examination explicitly ([[Click Models]], inverse propensity weighting), to create the exposure the logs lack ([[Exploration vs Exploitation]]), to keep human or [[Implicit Judgments|implicit]] judgments and business KPIs separate, and to confirm suspected effects with controlled experiments, not log correlations.

## Related Concepts

- [[Position Bias]] · [[Presentation Bias]] · [[Impression Bias]]
- [[Click Models]] · [[Click Signals]] · [[Implicit Judgments]]
- [[Learning to Rank]] · [[Exploration vs Exploitation]]
- [[Autocomplete]] · [[Personalization]] · [[LLM as Judge]] · [[NDCG]]

## Related Topics

- [[Search UX]] · [[Search UX Research]] · [[E-commerce Search]]
- [[A-B Testing for Search]] · [[Search Quality Assurance]] · [[Personalization in Search]]

## Related Articles

- [[Why nDCG Misleads eCommerce Search]]
- [[Query Understanding - Autocomplete and User Experience]]
- [[Good Abandonment on Search Results Pages]]
- [[Beyond Algorithms - Ranking at Scale at Booking.com]]
- [[Roman Grebennikov - Personalizing Search Results in Real-Time]]
- [[sQuIrRel - Large-Scale Evaluation of E-commerce Query Classification Models]]
- [[Do LLM Judges Actually Agree With Us]]

## People

- [[Andreas Wagner]] · [[Daniel Tunkelang]] · [[Roman Grebennikov]]
