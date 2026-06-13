---
created: 2026-05-16
type: article
tags: [article, tf-idf, bm25, e-commerce, relevance, ranking, medium]
source: "https://medium.com/empathyco/the-influence-of-tf-idf-algorithms-in-ecommerce-search-e7cb9ab8e662"
author: [David Argüello Sánchez]
company: [Empathy]
concepts: [BM25, Learning to Rank, Results Boosting]
topics: [E-commerce Search]
---

# The Influence of TF-IDF Algorithms in E-commerce Search

**[[David Argüello Sánchez]]** (Empathy) shows two concrete ways TF-IDF harms e-commerce search relevance, and why disabling it often helps.

## Problem 1: TF Inflates Accessory Rankings

**Query**: "iPad"  
TF-IDF ranks "Black mini iPad cover compatible with iPad 2 and iPad mini 3" **above** "iPad 2" because the accessory repeats "iPad" 3 times while the actual iPad product mentions it once.

Even adding a category boost doesn't fully fix this when TF scores dominate.

**Fix**: Disable TF-IDF (set `similarity: boolean`) — use presence/absence only. Then category boosts work as intended.

## Problem 2: IDF Inflates Brand Matches

**Query**: "Polo" (user means polo shirts)  
"Polo" appears in 150 product *names* but only 50 *brand* fields. IDF considers the brand field signal rarer → scores "Polo Ralph Lauren" brand products higher than polo shirts, even with 2× name field weight.

**Fix**: Again, boolean similarity makes field weights behave predictably.

## Core Insight

TF-IDF was designed for long-form text (newspapers, articles) where repetition implies topicality. Product titles and structured catalog data don't follow this assumption. In e-commerce:
- Products are tagged for marketing, not IR
- Accessories often repeat the main product name
- Field rarity and frequency don't correlate with user intent

Boolean similarity + explicit field weights + merchandising rules gives more predictable, tunable behavior.

## Related Concepts

[[BM25]] · [[Learning to Rank]] · [[E-commerce Search]]
