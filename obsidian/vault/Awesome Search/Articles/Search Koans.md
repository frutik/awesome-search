---
type: article
title: "Search Kōans"
aliases: ["Search Koans", "Bonsai Search Koans"]
source: "https://bonsai.io/blog/search-koans/"
author: "[[Max Irwin]]"
company: "[[Bonsai]]"
published: 2025-12-05
tags: [article, company-blog, philosophy, opinion, search-craft, relevance]
topics: ["[[Fun and Philosophy]]"]
concepts: ["[[Search Evaluation]]", "[[Search Observability]]", "[[Semantic Search]]", "[[RAG]]"]
created: 2026-06-27
---

# Search Kōans

A short, reflective [[Bonsai]] piece by [[Max Irwin]] distilling ~15 years of search engineering into Zen-style kōans. Framed not as riddles but as contemplative statements on *the identity of opposites* — each is a small, true story whose lesson sits in the tension it exposes. The genre belongs squarely to [[Fun and Philosophy]]: it asks *what is search work really like?* rather than *how do we tune the model?*

---

## The Kōans

Each story is paired with the hard-won lesson it teaches.

1. **The irrelevant query no one searches.** A stakeholder insists results are bad for a query customers have never actually typed. → *Perceived problems ≠ real problems; validate against real query logs.* See [[Before You Fix Your Search, Know What's Actually Broken]].
2. **Fast in test, slow in life.** New queries take over a minute — because testing used customer-style queries, not production load patterns. → *Test the load you'll actually get, not the query you imagine.*
3. **Two experts, one document, no agreement.** Two subject-matter experts judge the same result oppositely. → *Relevance is subjective; judgments need adjudication, not a single oracle.* See [[Search Evaluation]].
4. **The comma that helped, then hurt.** One comma in an 800-token prompt improved metrics; a second comma regressed them. → *LLM prompts are brittle; small edits are not small.*
5. **More heap, same saturation.** Raising the Java heap 32→48 GB still saturates. → *When more resources don't help, the bottleneck isn't resources — it's growth or inefficiency.*
6. **The migration only the engineers wanted.** A re-platforming with no articulated customer benefit; only the team expects to be happier. → *If the user gains nothing, ask why you're doing it.* See [[Economics of Search]].
7. **Summaries that bury the source.** A RAG project replaces original research with summaries; customers prefer the summaries despite the loss of fidelity. → *Convenience and source integrity pull in opposite directions.* See [[RAG]].
8. **Two demos, no yardstick.** Two engineers show two prototypes with no shared evaluation frame. → *Without a measurement protocol, "better" is just a vibe.* See [[Search Quality Assurance]].
9. **Coverage up, relevance down.** Adding content sources improves recall but degrades relevance on existing searches. → *Every corpus you add is also noise added to what already worked.*
10. **The search that broke quietly.** Site search fails and no alert fires; nobody knows. → *Unmonitored search fails silently; observability is not optional.* See [[Search Observability]].
11. **Better vectors, worse snippets.** Moving to vector search lifts relevance but loses keyword highlighting in snippets. → *Semantic gains can quietly cost lexical affordances users relied on.* See [[Semantic Search]], [[Full-Text Search]].
12. **The Friday insight, gone by Wednesday.** An elegant fix conceived on Friday is forgotten under a pile of support tickets. → *Context-switching destroys solutions; protect the thinking.*
13. **"Why can't the computer just do it?"** A child asks why the work is manual when computers exist — exposing the engineer's own assumption that "fixing relevance" is straightforward. → *Relevance is human judgment; it does not automate away.*

## Why It Matters

The collection is a compact catalogue of search's recurring, irreducible tensions: perception vs. reality, coverage vs. precision, semantic vs. lexical, convenience vs. fidelity, automation vs. judgment. Several map directly to documented [[Search Problem Archetypes|problem archetypes]] and to the discipline of [[Search Quality Assurance]] — which is what gives the "fun" framing its bite.

## Related Topics
- [[Fun and Philosophy]]
- [[Search Problem Archetypes]]
- [[Search Quality Assurance]]
- [[Search Observability]]

## Related Articles
- [[Before You Fix Your Search, Know What's Actually Broken]] — kōan #1 as a full essay
- [[What is a Relevant Search Result]] — the subjectivity of relevance (kōan #3)
- [[Mutually Assured Distraction]] — more content can mean worse retrieval (kōan #9)
- [[How to Really Design Search for a Database]] — also [[Bonsai]] / [[Max Irwin]]

## People
- [[Max Irwin]]

## Source
- https://bonsai.io/blog/search-koans/
