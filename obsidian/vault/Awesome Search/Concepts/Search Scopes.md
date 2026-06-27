---
title: "Search Scopes"
aliases: ["search scope", "scoped search", "search scope selector", "search within", "scope filter"]
tags:
  - concept
  - search-ux
  - e-commerce-search
  - search
created: 2026-06-27
---

# Search Scopes

## Definition

A search scope restricts a query to a **subset of the index** *before* retrieval runs — a department, category, content type, site section, or "search within these results". Where [[Faceted Search]] refines a result set *after* the query, scoping narrows the searchable space *up front*. The two are complementary: scope first, facet second.

Scopes surface in the UI as a selector next to the search box (a dropdown, tabs, or pills), as a contextual "Search within *Category*" affordance on a listing page, or implicitly when [[Query Understanding]] auto-detects a category from the query itself ([[Query Specificity]], query scoping).

---

## Why Scopes Matter

- **Precision on broad indexes.** On a large catalog or multi-content-type site (products + articles + help + community), an unscoped query mixes incompatible result types. A scope keeps "returns" (the policy) from drowning under "returns" (the product).
- **Faster reformulation.** Letting a user say "just in Electronics" is cheaper than rewriting the whole query.
- **Intent signalling.** A chosen scope is an explicit, high-confidence intent signal — more reliable than inferred [[Search Intent]].

Baymard finds e-commerce sites should support **several** distinct scope mechanisms (category dropdown, scoped autocomplete, in-category search, etc.), not just one — different shoppers reach for different ones.

## Scope Mechanisms

| Mechanism | Where | Notes |
|---|---|---|
| Scope dropdown | Beside the search box | "All / Electronics / Books"; classic but easy to miss |
| Tabs / verticals | Above results | Federated result types (see [[Federated Search]]) |
| Search-within | On a category or results page | Contextual; scope = current page |
| Auto-scoping | Backend | Query Understanding maps "kids shoes" → Kids > Footwear |

## The Sticky-Scope Failure Mode

The signature danger of scoped search ([[Nielsen Norman Group]], [[Scoped Search - Dangerous but Sometimes Useful|Scoped Search: Dangerous, but Sometimes Useful]]): a scope set on one query **persists** into the next, so the user searches the whole site in their head but only one section in reality — and gets a wrongly-empty or wrongly-narrow result page. They blame the catalog, not the stale scope.

Mitigations:
- Make the active scope **highly visible** in the search box and on the results page.
- Default back to all-content (reset the scope) on a new session or after N queries.
- When a scoped query returns few/zero results, **offer the unscoped fallback**: "No matches in Electronics — 240 results across all categories." This ties scoping directly to [[Zero Results]] recovery.

## Scopes vs. Facets vs. Federation

- **Scope** — chosen *before* the query; defines what is searched.
- **[[Faceted Search|Facet]]** — chosen *after* the query; refines what was found.
- **[[Federated Search|Federation]]** — runs the query across multiple sources/scopes at once and blends or tabs the results.

A well-designed system uses all three: federate by default for discovery, let power users scope for precision, and facet to refine either way.

## Related Concepts

- [[Faceted Search]] — post-query refinement; the complement to pre-query scoping
- [[Federated Search]] — querying multiple scopes simultaneously
- [[Zero Results]] — stale or over-narrow scopes are a top cause of empty pages
- [[Query Understanding]] — automatic scope detection from the query
- [[Search Intent]] — an explicit scope is a strong intent signal
- [[Search Result Diversity]] — federation/scoping trade precision against discovery breadth

## People

- [[Daniel Tunkelang]] — query scoping and search-within patterns in the Query Understanding series
