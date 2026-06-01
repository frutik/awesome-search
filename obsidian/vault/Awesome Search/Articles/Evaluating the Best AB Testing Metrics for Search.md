---
type: article
tags: [article, ab-testing, metrics, ctr, conversion, directionality, sensitivity, company-blog]
source: "https://www.algolia.com/blog/engineering/a-b-testing-metrics-evaluating-the-best-metrics-for-your-search"
author: []
company: [Algolia]
concepts: [A-B Testing, Click Signals]
topics: [A-B Testing for Search, Search Quality Assurance]
---

# Evaluating the Best AB Testing Metrics for Search

**Algolia** introduces a two-dimensional framework for evaluating A/B testing metrics: **directionality** and **sensitivity** (from Yandex Research).

## The Framework

| Property | Definition |
|----------|-----------|
| **Directionality** | A clear, unambiguous interpretation — higher is always better (or lower is always better) |
| **Sensitivity** | Ability to detect statistically significant differences with reasonable sample sizes and time |

The fundamental tension: directional metrics (revenue) are slow to reach significance; sensitive metrics (CTR) are fast but gameable.

## Common Metrics Compared

| Metric | Directional? | Sensitive? | Pitfall |
|--------|-------------|------------|---------|
| Revenue | High | Low | Needs months; confounded by product launches |
| Conversion rate | Medium | Medium | Treats all sales as equal; doesn't capture margin |
| CTR | Low | High | Gameable (clickbait); misleading in knowledge-query domains |
| Margin-weighted CR | High | Medium | Best of both worlds for margin-focused businesses |

## Key Pitfalls

1. **Conversion rate boosting high-margin items**: System B boosts expensive items → lower CR but higher revenue. CR misleads.
2. **CTR in knowledge queries**: Adding snippet answers drops CTR — but that's actually better relevance. Use time-between-sessions instead.
3. **Metric gaming**: Authors publish clickbait titles → CTR rises without relevance improvement.

## Recommendations

- Use a **directional primary metric** (revenue or margin-weighted conversion) to define "better"
- Use **sensitive secondary metrics** (CTR, session conversion) for fast signal
- Never rely on a single metric — combine and watch for directional alignment
- Check whether your metric can be **gamed**, intentionally or accidentally

## Related Concepts

[[A-B Testing]] · [[Click Signals]] · [[A-B Testing for Search]] · [[Search Quality Assurance]]
