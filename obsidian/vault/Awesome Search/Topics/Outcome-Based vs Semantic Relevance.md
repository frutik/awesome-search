---
type: topic
title: Outcome-Based vs Semantic Relevance
aliases:
  - semantic vs engagement relevance
  - relevance vs engagement
  - accuracy vs outcome-based relevance
related_concepts:
  - "[[Semantic Relevance]]"
  - "[[Outcome-Based Relevance]]"
  - "[[Click Signals]]"
  - "[[Implicit Judgments]]"
  - "[[Ranking Signal Selection]]"
  - "[[Judgment Lists]]"
  - "[[LLM as Judge]]"
  - "[[ESCI Label Scheme]]"
  - "[[Position Bias]]"
  - "[[Staged Judging]]"
  - "[[Learning to Rank]]"
  - "[[LTR Feature Engineering]]"
related_topics:
  - "[[E-commerce Search]]"
  - "[[Two-Sided Marketplace Ranking]]"
  - "[[E-commerce Search Evaluation Datasets]]"
  - "[[Conversational and Agentic Search]]"
articles:
  - "[[How Etsy Uses LLMs to Improve Search Relevance]]"
  - "[[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic
    Recommendation Systems]]"
  - "[[Introducing CLEPR, our model for semantic understanding]]"
  - "[[Beyond Algorithms - Ranking at Scale at Booking.com]]"
  - "[[When There's No Conversion Rate]]"
  - "[[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]]"
companies:
  - "[[Etsy]]"
  - "[[Criteo]]"
  - "[[Booking.com]]"
  - "[[Allegro]]"
tags:
  - topic
  - relevance
  - search-evaluation
  - e-commerce
  - ranking
created: 2026-10-04
---

# Outcome-Based vs Semantic Relevance

Two different questions can be asked of a search result. **Semantic relevance** asks whether it matches what the query means. **Outcome-based relevance** asks whether users act on it: click, buy, book, stay. The answers don't always agree, and Etsy has seen engagement sometimes drop as semantic relevance rose. The fixes also run in opposite directions: [[Etsy]] adds semantic relevance to an engagement-trained ranker, while [[Criteo]] adds commerce signals to a semantically trained one. This page covers where the two signals come from, why they diverge, and the patterns for combining them.

---

## The Two Questions

| | [[Semantic Relevance]] | [[Outcome-Based Relevance]] |
|---|---|---|
| Asks | Does the result match the query's meaning? | Did users click, buy or book it? |
| Also called | accuracy, intent-based relevance | engagement-based relevance, performance-based recommendation |
| Evidence | human or LLM [[Judgment Lists]], graded labels such as [[ESCI Label Scheme\|ESCI]] | [[Click Signals]], conversions, [[Implicit Judgments]] |
| Scale and cost | expensive, scaled by [[LLM as Judge\|LLM judges]] and distillation | already collected, millions of events a day |
| Characteristic bias | annotation bias, hard graded boundaries | [[Position Bias]], popularity, items nobody was shown |
| Fails when | the match is right but nobody wants it | the item is popular but off-intent |

The comparison between human judgments and click signals in [[Click Signals]] is the same split seen from the data side: clicks are free, fresh and noisy; judgments are expensive, slow and clean when the guidelines are good.

## Where Each Signal Comes From

**Semantic.** Relevance labels come from guidelines and annotators. [[Etsy]] defines relevant, partially relevant and irrelevant from user research rather than engagement data. Human golden labels anchor an LLM annotator, which scales labelling to millions of query–listing pairs and is then distilled to a real-time model ([[How Etsy Uses LLMs to Improve Search Relevance]]). The [[ESCI Label Scheme]] grades shopping intent, not text match: a phone case is topically about the phone, but it is a Complement, not an answer.

**Outcome.** Labels come from behaviour, and choosing *which* behaviour is the real decision ([[Ranking Signal Selection]]). [[Booking.com]] weighs each candidate action on four axes: relation to satisfaction, volume, delay, and bias. Clicks are plentiful and weak; a completed stay with a good review is close to ground truth and far too sparse. The usual answer is layered: a conversion as the primary positive, with clicks as secondary positives ([[Beyond Algorithms - Ranking at Scale at Booking.com]]). Sometimes even clicks are not logged directly. [[Criteo]] rebuilds them by stitching searches to later product-page views in the same session ([[Introducing CLEPR, our model for semantic understanding]]).

## Why They Diverge

- **Popularity.** Engagement favours listings that are already popular, whatever the query. Optimising on it alone entrenches that, so popular items keep winning regardless of fit ([[Semantic Relevance]]).
- **Exposure.** Items ranked higher get clicked more whether or not they are better ([[Position Bias]]). Items that are never shown never earn a signal, a loop that is permanent in marketplaces where new supply keeps arriving ([[Two-Sided Marketplace Ranking]]).
- **Content doesn't decide purchase.** Several products can match a query equally well on content, and only some get bought. Criteo's case for outcome-based relevance rests on this gap ([[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]]).
- **The metrics can move in opposite directions.** Etsy reports engagement sometimes *dropping* as semantic relevance improves, because a relevant but less familiar result can draw fewer clicks than a popular, loosely related one.

## How Systems Combine Them

The two signals are rarely traded off one-for-one. Each tends to take a distinct job.

1. **Semantic as a gate, outcome as the order.** Candidates must pass a semantic threshold, then commerce signals rank what remains. Criteo's [[CLEPR]] score works this way as a guardrail for sponsored-product ads. In Criteo's own offline benchmark over 400 retrieved candidates, re-ranking by recent sales share raised the purchased product's normalized rank score about 2.5×. One of Etsy's four production uses has the same shape: listings predicted irrelevant are dropped before ranking.
2. **Learning to Rank: semantic features, outcome labels.** This is the most general form. A [[Learning to Rank|LTR]] model, typically [[LambdaMART]], re-ranks a fast first stage: BM25 or a bi-encoder fetches the top 1,000, and LTR orders the top 20. Its features mix both sides: text match such as [[BM25]] scores and embedding similarity, next to click rate, sales and user affinity ([[LTR Feature Engineering]]). Behavioural labels are the dominant training signal for production LTR ([[Implicit Judgments]]), so the model learns, query by query, how far to trade text match for behaviour. Etsy's other three uses sit here: its relevance score enters the ranker as a feature, re-weights training loss, and boosts highly relevant listings in the final results.
   - **The label, not the algorithm, decides which relevance it optimises.** Trained on human [[Judgment Lists]], the same model optimises semantic relevance, with behaviour reduced to a feature. Choosing which behaviour becomes the label is the step [[Ranking Signal Selection]] treats as foundational. At Findify, a ranker trained on raw clicks pushed a curiosity item to the top of a collection: everyone clicked it and nobody bought it. Weighting purchases far above clicks sent it back down ([[Roman Grebennikov - Personalizing Search Results in Real-Time]]).
   - **A learned blend can let outcome override match.** With popularity features carrying enough weight, a popular, loosely related item can outrank an exact one. That is why Etsy also filters irrelevant listings before ranking and Criteo sets a hard threshold, as in pattern 1. Trained on clicks over its own rankings, LTR also reinforces whatever it already ranks high. At Findify, A/B gains decayed from +8% to +6% until only a small shuffled slice of traffic fed training ([[Exploration vs Exploitation]]).
3. **Outcome as training data for a semantic model.** CLEPR learns query–product matching from filtered click pairs. It uses a contrastive objective and counts each pair once to keep popularity out, then judges quality against human labels instead of clicks. Running the other way, [[sQuIrRel - Large-Scale Evaluation of E-commerce Query Classification Models|sQuIrRel]] derives evaluation labels for query-classification models from a relevance model, because clicks and annotators both serve that task poorly.
4. **Outcome to decide what to judge.** Behavioural performance can split query–document pairs into easy positives and suspect pairs, so only the suspect ones go to an expensive semantic judge. One team's production figures report this pruning about 93% of pairs at e-commerce scale ([[Implicit Judgments]], [[Staged Judging]]).

## Measuring Each

- **Semantic:** agreement with golden labels, such as Etsy's Macro F1 across its three-tier model stack, or the share of fully relevant results (Etsy's rose from 58% to 62% between August and October 2025). Graded labels feed [[NDCG]] directly.
- **Outcome:** rank of the clicked or purchased item within a candidate set, as in Criteo's reciprocal-rank benchmarks ([[MRR]]), or conversion in an A/B test.
- **No conversion event at all.** Enterprise, long-document and exploratory search have no purchase to count. Proxies include dwell time, session behaviour such as reformulation and pogo-sticking, scroll depth, and retention ([[When There's No Conversion Rate]]).

## Pitfalls

- **Optimising outcome alone** entrenches popularity and can't see relevant items nobody clicked.
- **Graded semantic labels are hard at the boundaries.** [[Allegro]]'s LLM judge reached F1 around 0.94 on exact matches but only 0.33–0.51 on degrees of substitutability ([[ESCI Label Scheme]]).
- **Offline outcome benchmarks favour models trained on the same behaviour.** A click-trained encoder evaluated on finding clicked products starts with an advantage over zero-shot models. Criteo's own human-labelled comparison shows a much smaller gap ([[Model Selection and Fine-Tuning Evaluation]]).
- **Business objectives are a third axis.** Margin, inventory, promoted placement and supplier exposure also shape ranking, and conflict with both kinds of relevance ([[E-commerce Search]], [[Two-Sided Marketplace Ranking]]).

## Related Concepts

- [[Learning to Rank]] · [[LTR Feature Engineering]] — the standard way to put outcome labels on top of semantic features

- [[Semantic Relevance]] · [[Outcome-Based Relevance]] — the two sides
- [[Ranking Signal Selection]] · [[Implicit Judgments]] · [[Click Signals]] — the outcome side's evidence
- [[Judgment Lists]] · [[LLM as Judge]] · [[ESCI Label Scheme]] — the semantic side's evidence
- [[Position Bias]] — the main distortion in behavioural labels
- [[Staged Judging]] — behaviour deciding what gets judged

## Related Articles

- [[How Etsy Uses LLMs to Improve Search Relevance]] — semantic relevance added to an engagement-trained stack
- [[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]] — commerce signals added to a semantic stack
- [[Introducing CLEPR, our model for semantic understanding]] — semantic guardrail trained on clicks
- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — which behaviour becomes the label
- [[When There's No Conversion Rate]] — outcome measurement without a conversion
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — where graded semantic labels get hard

## Related Topics

- [[E-commerce Search]] · [[Two-Sided Marketplace Ranking]] · [[E-commerce Search Evaluation Datasets]] · [[Conversational and Agentic Search]]

## Companies

- [[Etsy]] · [[Criteo]] · [[Booking.com]] · [[Allegro]]

## People

- [[Daniel Tunkelang]] — measuring outcomes without a conversion event
- [[Maxime Vono]] — outcome-based relevancy for agentic commerce
- [[Paul Coursaux]] — CLEPR as a semantic guardrail

- [[Roman Grebennikov]] — the Findify cases: click labels optimising curiosity, and feedback loops in LTR
