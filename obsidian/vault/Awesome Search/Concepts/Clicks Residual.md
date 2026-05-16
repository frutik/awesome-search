---
type: concept
aliases: ["click residual", "clicks residual", "residual clicks"]
tags: [concept, metrics, behavioral, evaluation]
related: ["[[Click Signals]]", "[[Zero Results]]", "[[Search Quality Assurance]]", "[[Session-Based Evaluation]]"]
created: 2026-05-16
---

# Clicks Residual

A behavioral success metric that measures the gap between the expected click distribution and the observed click distribution for a query. A positive residual signals query success; a negative residual signals failure.

## Intuition

For any query, there is a "baseline" click distribution based on how users typically interact with results of that type. If a query gets *more* clicks than expected — especially clicks deeper into the result list and across multiple results — that suggests the results are satisfying user intent. If it gets fewer clicks than expected (or only zero-click interactions), something may be wrong with the results.

## Why Not Just CTR

CTR conflates many signals:
- High CTR can mean good results (users found what they wanted) OR bad results (users had to click many things to find anything)
- Zero clicks can mean good results (direct answer displayed) OR bad results (user gave up)

Clicks residual tries to model the *expected* behavior as a baseline, so deviations from it are more meaningful.

## Use Cases

- **Query-level success scoring**: identify queries that are systematically underperforming — good candidates for manual review
- **A/B test signal**: changes that improve clicks residual are more likely to represent genuine quality improvements than raw CTR changes
- **Monitoring**: flag queries where residual degrades over time (index changes, catalog changes, seasonal shifts)

## Limitations

- Requires enough historical data to build a stable expected baseline — doesn't work for rare/new queries
- The baseline model itself can be biased by past ranking decisions
- Sensitive to position — changes in result layout affect click behavior independent of relevance

## Related

- [[Click Signals]] — broader treatment of click-based relevance signals
- [[Zero Results]] — extreme case: no results to click at all
- [[Session-Based Evaluation]] — clicks residual works best in a session context
- [[Search Quality Assurance]] — used as a behavioral dashboard metric
