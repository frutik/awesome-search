---
title: "Personalization"
aliases: ["personalized search", "user personalization", "search personalization", "contextual ranking"]
tags:
  - concept
  - ranking
  - personalization
  - search
---

# Personalization

## Definition

Personalization adapts search results to individual user preferences, history, and context — returning different results for different users submitting the same query, based on signals like their browsing history, purchase behavior, location, and demographics.

## Why Personalize?

The same query "shoes" means different things to different users:
- A runner → technical running shoes
- A parent → children's shoes
- A fashion-conscious shopper → trendy sneakers
- A formal dresser → dress shoes

Generic ranking serves the "average user" — personalization serves the actual user.

## Personalization Signals

| Signal Type | Examples | Freshness |
|-------------|---------|-----------|
| Explicit preferences | Saved searches, wishlists | Static |
| Purchase history | Bought brands, price range | Medium |
| Browse history | Categories, products viewed | Fresh |
| Search history | Previous queries, clicked results | Fresh |
| Demographics | Age, gender, location | Static |
| Session context | Current session queries | Real-time |
| Social proof | Friends' purchases | Medium |

## Personalization Approaches

### Re-ranking
Run generic retrieval → re-rank based on user preferences.
- Simple to implement (add user features to [[Learning to Rank]])
- Doesn't change candidate set — limited recall personalization

### Query Rewriting
Modify the query before retrieval based on user profile:
- "shoes" → "Nike women's running shoes" (based on user history)
- Improves both recall and precision

### Embedding-Based Personalization
Airbnb's approach: learn user embeddings alongside listing embeddings in the same space.
- Query embedding → user-contextualized embedding
- Personalized ANN search over listing embeddings
- Published as "Listing Embeddings in Search Ranking"

### Feature Engineering for Personalized LTR
Add user features to the [[Learning to Rank]] model:
- User's average purchase price range
- User's brand affinities
- User's category preferences
- Session recency signals

## Privacy Considerations

Personalization requires collecting and using personal data:
- Compliance: GDPR, CCPA require consent and right to erasure
- User trust: explicit personalization signals (wishlists) are trusted; opaque behavioral targeting is not
- Security: personalization profiles are sensitive data — must be protected

Facebook/Meta's 98 personal data points for ad targeting is the extreme example of what's possible (and controversial).

## Airbnb Case Study

Airbnb's personalization system (Eugene Yan et al.):
- Trains user embeddings from booking sequences
- Listing embeddings from viewing sequences
- Online: user embedding → approximate nearest neighbor search over listings
- Result: +21% booking lift in A/B test

The key insight: user preferences are encoded in their past interactions, not in their profile form. Embeddings capture implicit preferences.

## Related Concepts

- [[Learning to Rank]] — personalization features in LTR models
- [[Dense Vector Retrieval]] — user and item embeddings for personalized ANN
- [[Semantic Search]] — personal context modifies query meaning
- [[Click Signals]] — behavioral personalization signals
- [[Session-Based Evaluation]] — personalization evaluated at session level
- [[Search Intent]] — personalization refines intent interpretation

## People

- [[Daniel Tunkelang]] — personalization in search; QueryUnderstanding.com series


## Elastic Governed Personalization (Ecommerce)

Two mechanisms extending a governance control plane without replacing it:
1. **Purchase history boosting** — query `user_purchases` index in parallel with governance; logarithmic frequency + exponential decay recency weights; governance still controls what appears
2. **Cohort-aware policy activation** — cohort policies stored in same policy engine; `terms` filter `{"cohorts": ["_all", "vegan"]}` narrows candidate policy set

### Ordering (innermost → outermost)
1. Base query (keyword/semantic)
2. Governance policy layer (hard filters + soft boosts)
3. Business-signal boosts (margin, popularity)
4. Purchase history boosts (outermost)

## Articles

- [[Elasticsearch Personalized Search in Ecommerce - Improve Relevance]] — [[Alexander Marquardt]], [[Honza Král]], [[Taylor Roy]]
- [[Using LLMs to Amplify Human Labeling and Improve Dash Search Relevance]] — [[Dmitriy Meyerzon]] (Dropbox Dash enterprise search)

## People (additional)

- [[Alexander Marquardt]] — Elastic governed personalization
- [[Honza Král]] — Elastic governed personalization
- [[Taylor Roy]] — Elastic governed personalization
- [[Dmitriy Meyerzon]] — Dropbox Dash relevance labeling
