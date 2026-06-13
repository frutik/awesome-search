---
created: 2026-05-16
type: article
tags: [article, ab-testing, experimentation, randomization, carry-over, company-blog]
source: "https://www.searchhub.io/en/common-pitfalls-of-search-experimentation/"
author: [Andreas Wagner]
company: [searchHub]
concepts: [A-B Testing]
topics: [A-B Testing for Search]
---

# Common Pitfalls of Onsite Search Experimentation

**[[Andreas Wagner]]** (searchHub) identifies two major A/B testing traps in onsite search.

## Pitfall 1: Test Scope Too Broad

Small configuration changes (e.g., adding vector search for long-tail queries) won't move average-across-all-traffic metrics. Solution: **segment by affected queries** (e.g., queries > 5 words) and test only within that segment. Positive in sum doesn't mean positive for everyone.

## Pitfall 2: Session-Level Randomization + Late-Stage KPIs = Carry-Over Effect

Using session-level randomization with ARPU (Average Revenue Per User) as the primary metric is dangerous because:

- Users have memory across sessions. A user exposed to treatment in session 1 may return to buy in session 2 (assigned to control).
- This **misattributes** the positive effect of the treatment to the control group.

**Simulation results**: When sessions genuinely independent → A/B test correctly detects effect 100% of time. When sessions non-independent (carry-over) → correctly detects only 90% of time and **underestimates effect size by ~30%** (detects 1.4% instead of 2%).

## Solution

1. **User-level randomization**: each user always sees the same variant across all sessions
2. **Guardrail metrics**: add earlier-funnel KPIs (e.g., Average Added Basket Value Per User) alongside ARPU to detect assignment persistence issues

## Key Rule

If sessions might not be independent, randomize at user level. Cookie-based user-level randomization is imperfect but far better than session-level for purchase funnels.
