---
type: case-study
company: "[[Etsy]]"
articles:
  - "[[Targeting Broad Queries in Search]]"
  - "[[How Etsy Uses Thermodynamics for Search]]"
  - "[[Modeling Spelling Correction for Search at Etsy]]"
topics:
  - "[[Query Understanding in Practice]]"
  - "[[Search Result Diversity]]"
  - "[[Spelling Correction in Search]]"
  - "[[E-commerce Search]]"
---

# Etsy — Search Quality and Query Understanding

Etsy is a global handmade/vintage marketplace with a highly heterogeneous catalog — items have non-standard names, niche categories, and long-tail vocabulary that standard search techniques handle poorly. Their engineering blog documents several years of search quality work focused on query understanding, diversity, and spelling correction.

## Key Insight

Etsy's catalog is fundamentally different from a structured product catalog. Queries like "cottagecore", "steampunk necklace", or "geeky gift" are valid search intents that map to thousands of unique artisan items — not a single best answer. This drives their approach: **broad queries need diversity, not precision**.

## Challenge 1: Broad and Head Queries

High-volume queries like "necklace", "bag", or "geeky" span enormous semantic space. Standard relevance scoring (BM25) produces "winner takes all" results — the most popular category dominates, ignoring other valid interpretations.

**Solution**: Query classification → entropy-based diversification.

- Classify queries as broad (head) vs. navigational/specific
- For broad queries, shift the objective from precision to diversity
- Measure result diversity using **Shannon entropy** over category and attribute distributions
- Set per-query entropy targets; re-rank or inject results to meet the target

See: [[Targeting Broad Queries in Search]], [[How Etsy Uses Thermodynamics for Search]]

## Challenge 2: Entropy-Based Diversity (Thermodynamics Analogy)

Etsy borrowed the concept of **thermodynamic entropy** to quantify result diversity:

- **Low entropy** = results all look similar (converged, narrow)
- **High entropy** = results span many categories and styles

For a query like "geeky", optimal results should include geeky necklaces, t-shirts, mugs, art prints, and posters — not five variations of the same item. Entropy measurement over the result set's category distribution drives re-ranking toward that target.

## Challenge 3: Domain-Specific Spelling Correction

Generic dictionaries fail for Etsy's vocabulary — "cottagecore" is not in Merriam-Webster, but it is a major search category.

**Solution**: Noisy-channel model trained on Etsy's own query logs.

- **Error model**: confusion matrices from common user typo patterns
- **Language model**: trained on Etsy query logs (domain-specific corpus, not Wikipedia/news)
- **Precision guards**: click data validates that a correction actually improves results; suppresses correction of valid uncommon terms
- **Key principle**: the correction system must know what's on the platform

See: [[Modeling Spelling Correction for Search at Etsy]]

## What to Steal

| Pattern | Application |
|---|---|
| Classify queries as broad vs. navigational | Apply diversity logic only where needed |
| Entropy-based diversity metric | Measurable objective for re-ranking diversity |
| Domain query logs as spelling LM corpus | Far more accurate than generic corpus for vertical search |
| Click signals to validate corrections | Prevents correcting valid niche terms |
| Precision guard for correction | Never correct what users successfully click on |

## Related Case Studies

- [[Airbnb - ML-Powered Experiences Ranking]] — also uses entropy/diversity thinking in ranking
- [[Zalando - Self-DoS via Facet Aggregation]] — another e-commerce search architecture lesson
