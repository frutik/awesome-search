---
type: topic
aliases:
  - search team management
  - search org
  - managing search
tags:
  - topic
  - management
  - team
  - org-design
  - search-team
related_concepts:
  - "[[Search Relevance]]"
  - "[[Search Quality]]"
related_topics:
  - "[[Hiring for Search]]"
  - "[[Economics of Search]]"
  - "[[A-B Testing for Search]]"
  - "[[Understaffed Search Team]]"
articles:
  - "[[Thoughts about Managing Search Teams]]"
  - "[[Search is a Team Sport]]"
  - "[[On Search Leadership]]"
  - "[[Search Product Management - The Most Misunderstood Role]]"
  - "[[Search Relevance for Understaffed Teams]]"
  - "[[Getting Started on Search Relevance for the Understaffed Search Team]]"
people:
  - "[[Daniel Tunkelang]]"
  - "[[Lester Solbakken]]"
created: 2026-05-16
---

# Managing a Search Team

Organizational and leadership decisions that determine whether a search team succeeds. Search is unusual enough that generic engineering management advice breaks down.

---

## What Makes Search Teams Different

Search teams sit at the intersection of:
- **Engineering** (indexing, serving, infrastructure)
- **Data science / ML** (ranking models, evaluation, experimentation)
- **Product** (query understanding, UX, business rules)
- **Domain expertise** (knowing what "good" looks like for your corpus)

Most teams underinvest in one of these quadrants, which creates a ceiling on quality. The rarest skill is someone who can hold all four together.

---

## Tunkelang's Four Principles (from "Thoughts about Managing Search Teams")

1. **Combine product and engineering** — don't silo them. Search PMs who can't read a ranking formula will make bad tradeoffs. Search engineers who don't think about user intent will optimize the wrong metrics.

2. **Be data-driven** — measure everything. Gut-feel relevance decisions are almost always wrong at scale. Build evaluation infrastructure early; it pays for itself.

3. **Incremental execution** — ship small improvements continuously rather than big bang rewrites. Relevance is a compound interest game.

4. **Holistic approach** — search quality is the product of many systems. Fixing just the ranking model while ignoring query understanding or indexing freshness produces marginal gains.

---

## Team Structures

### Centralized Search Team
One team owns all search across the product. 
- **Pros**: deep expertise, shared tooling, consistent quality bar
- **Cons**: bottleneck for product teams that want search customization; coordination overhead

### Embedded Search Roles
Relevance engineers sit within product teams.
- **Pros**: close to domain, fast iteration for that vertical
- **Cons**: skills fragment; no shared eval infrastructure; hard to maintain quality bar

### Platform + Vertical Model (Recommended for scale)
Central platform team owns core infrastructure (indexing, serving, LTR framework, eval harness). Vertical teams own relevance configuration and features.
- **Pros**: leverage + customization; shared tooling reduces duplication
- **Cons**: requires clear API contracts between platform and vertical teams

---

## The Search PM Role

Search PM is one of the hardest PM roles because:
- Success metrics are indirect (conversion, not just engagement)
- "Everything is an experiment" — no feature ships without measurement
- Technical depth required: understanding precision/recall tradeoffs, index design, model behavior
- Constant tension between short-term relevance fixes and long-term infrastructure

A weak search PM leads to a backlog of one-off tuning requests with no coherent strategy. A strong one builds evaluation culture and protects engineering time for compound investments.

Key skills: comfort with ambiguity, ability to communicate tradeoffs to non-technical stakeholders, obsession with measurement.

---

## Building an Evaluation Culture

The single highest-leverage management decision is investing in evaluation infrastructure early:

1. **Query log and annotation pipeline** — human-labeled relevance judgments, even a small set (1000 queries), are transformative
2. **Offline eval harness** — run NDCG/MAP/MRR against labeled data on every code change
3. **A/B framework** — no change ships without an experiment; teams that skip this build up technical debt in the form of unknown regressions
4. **Dashboard** — business metrics (conversion, zero-results, CTR) visible to the whole team, updated daily

Without evaluation culture, teams argue about relevance instead of measuring it.

---

## Cross-Functional Collaboration

Search quality is determined by inputs from many teams:

| Team | What they control | How it affects search |
|---|---|---|
| Content / catalog | Data quality, completeness | Garbage in, garbage out |
| Design | SERP layout, click affordances | Affects CTR signals used in LTR |
| Analytics | Conversion tracking | Powers implicit relevance signals |
| Legal / compliance | What can be indexed/surfaced | Creates invisible constraints |
| Customer support | Top complaint themes | Surfaces head-query failures |

A search lead who doesn't have relationships with these teams will hit invisible walls.

---

## Common Management Mistakes

**Treating search as plumbing.** Search is a product, not infrastructure. If leadership treats it as a utility, it gets starved of resources until it becomes a crisis.

**Hiring only engineers.** A team of engineers with no evaluation mindset will keep building without knowing if it works.

**Chasing NDCG.** Teams that optimize offline metrics without validating online often ship neutral or negative changes. Online validation is non-negotiable.

**No search-specific onboarding.** New hires who join a search team with no prior background need weeks of domain ramp-up. Invest in that investment.

**Letting the backlog run the roadmap.** One-off query fixes (typo-tuning, edge cases) feel productive but compound into an unmaintainable mess. Reserve capacity for systematic improvements.

---


**Metric worship.** Single-metric optimization destroys overall quality. A team watching only NDCG will ship changes that hurt diversity, freshness, or user trust without noticing.

**Relevance by anecdote.** Acting on individual user complaints or executive query demos without data produces a whack-a-mole backlog — each fix creates new failures. The antidote is a judgment set representing the full query distribution, not just the loudest tickets.

**Siloed evaluation.** Great per-component metrics (index freshness, query parsing, ranker NDCG) don't guarantee system-level quality. Always run end-to-end evaluation alongside component metrics.

## For Small / Understaffed Teams

When you have 1-2 engineers and no dedicated data science support:
- Prioritize zero-results and head query quality first (highest ROI)
- Use off-the-shelf relevance signals (BM25 + basic field weighting) before custom models
- Invest in a minimal eval harness even before a proper A/B framework
- Lean on open-source (Elasticsearch, Vespa, OpenSearch) to avoid building infrastructure
- Delegate domain expertise to other teams (catalog, content) rather than trying to own it

---

## Related

- [[Hiring for Search]] — who to hire and what to look for
- [[Economics of Search]] — org decisions have direct cost implications
- [[A-B Testing for Search]] — evaluation culture depends on a working experiment framework
- [[Daniel Tunkelang]] — canonical voice on search team management
- [[Understaffed Search Team]] — focused topic on resource-constrained teams
