---
title: "What is a 'Relevant' Search Result?"
aliases: ["Relevant Search Result", "OSC Relevance Definition", "Turnbull Relevance"]
tags:
  - clippings
  - search
  - relevance
  - evaluation
  - company-blog
source: "https://opensourceconnections.com/blog/2017/03/08/what-is-relevant/"
author: "Doug Turnbull"
created: 2026-05-15
concepts:
  - Search Evaluation
  - Judgment Lists
  - Query Understanding
---

# What is a 'Relevant' Search Result?

**Source:** https://opensourceconnections.com/blog/2017/03/08/what-is-relevant/
**Author:** [[Doug Turnbull]]

## Summary

"Relevance" sounds obvious but is deeply context-dependent. Turnbull unpacks the definition and shows why a rigorous, task-centered framing is necessary for search evaluation.

### The Naive Definition
"Relevant = about the topic of the query." But this fails in practice:
- "python" → a snake documentary is "about python" but not relevant to a programmer
- "cheap flights" → a philosophy essay on cheapness is "about cheapness" but not relevant

### Relevance as "Verb the Item"
Turnbull proposes framing relevance around **user task completion**:
> A result is relevant if it helps the user accomplish their goal.

This requires knowing the user's goal — which is why query understanding is prerequisite to relevance judgments.

For product search: "verb the item" means "can the user [buy/learn about/compare] this item?" A listing for "Nike Air Max" is relevant to "running shoes" because the user can buy it and it matches their need.

### Contrasting Options Framework
Relevance is not absolute — it's **comparative**. A result is relevant relative to the alternatives:
- If all results are equally bad, none are "relevant" in a useful sense
- A mediocre result can be "relevant" if it's the best available
- This motivates **graded relevance** (0-3 or 0-4 scales) over binary

### Information Completeness
A result is also relevant if it contains the **complete information** needed for the task:
- A product page missing the price is less relevant (user must navigate further)
- A recipe missing ingredient quantities is less relevant
- Completeness is a component of relevance, not separate from it

### Implications for Judgment Lists
When designing relevance judgment tasks:
1. Give raters the user **task/goal**, not just the query
2. Use graded scales (4-point minimum) to capture partial relevance
3. Define clear criteria for each grade level
4. Test rater agreement (inter-annotator agreement > 0.7 is a reasonable threshold)

### Dynamic vs. Static Relevance
Relevance changes over time:
- News queries: a 3-day-old article is less relevant than a 3-hour-old one
- Product queries: discontinued items are suddenly irrelevant
- Search systems must model freshness as a relevance component

## Key Concepts
- **Relevance as task completion** — "verb the item" framing
- **Contrasting options** — relevance is comparative, not absolute
- **Information completeness** — complete answers are more relevant
- **Graded relevance** — 0-N scales for nuanced judgment
- **Dynamic relevance** — freshness affects relevance over time

## Related Concepts
- [[Search Evaluation]]
- [[Judgment Lists]]
- [[Query Understanding]]
- [[NDCG]]
- [[Search Intent]]

## Related Articles
- [[Evaluating Good Search - Measure It]]
- [[Setting Up a Relevance Evaluation Program]]
- [[Understanding BERT and Search Relevance]]

## People
- [[Doug Turnbull]]
