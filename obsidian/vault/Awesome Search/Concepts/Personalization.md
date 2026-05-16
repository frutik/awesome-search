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
