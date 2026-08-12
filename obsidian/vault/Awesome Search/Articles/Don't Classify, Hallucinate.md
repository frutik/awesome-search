---
type: article
created: 2026-08-12
title: "Don't classify. Hallucinate!"
source: "https://softwaredoug.com/blog/2026/08/10/hypothetical-classifications"
author: "[[Doug Turnbull]]"
published: 2026-08-10
tags: [query-understanding, classification, taxonomy, llm, embeddings, e-commerce-search]
concepts: ["[[Query Understanding]]", "[[Hypothetical Document Embeddings]]", "[[Embeddings]]", "[[Query Types]]"]
topics: ["[[Query Classification]]", "[[E-commerce Search]]"]
---

# Don't classify. Hallucinate!

**Author:** [[Doug Turnbull]]

Using an LLM to classify products and queries is by now routine. The awkward part is constraining its output to the legal vocabulary of brands, colours, and categories the system actually allows. This post proposes skipping the constraint entirely: ask a cheap model to *invent* a category, then resolve the invention into the real taxonomy with embeddings.

---

## The Problem With Structured Outputs

In the Wayfair WANDS e-commerce dataset, classifying a query like "wood coffee table" means choosing among hundreds of category paths:

```
Furniture / Office Furniture / Desks
Furniture / Living Room Furniture / Coffee Tables & End Tables / Coffee Tables
Furniture / Living Room Furniture / Coffee Tables & End Tables / End & Side Tables
Décor & Pillows / Decorative Pillows & Blankets / Throw Pillows
Furniture / Bedroom Furniture / Dressers & Chests
```

The classic implementation constrains the model with structured outputs — in Pydantic, a `Literal` enumerating every legal value, "times 500" — and parses the response into a `QueryClassification` model.

This works. Two costs make it unattractive at scale:

- The full schema is transmitted on **every single call**.
- Providers cap how many enumerated values a structured output can carry.

## The Pattern: Hallucinate, Then Resolve

Instead, prompt a cheap model to "create novel, never seen before" classifications that fit the query, showing a handful of example paths purely as a format demonstration — not as legal values. Nothing about the real vocabulary is sent.

For "brown coffee table" the model returns something that does not exist in the taxonomy:

```
Furniture / Living Room / Tables / Coffee
```

Turnbull's point is that this apparently useless output is *extremely* helpful, because it is now trivially resolvable:

1. Embed every real classification path once, in memory (MiniLM in the accompanying notebook).
2. Embed the hypothetical path returned by the LLM.
3. Dot product the fake embedding against the real ones; take the most similar.

Which resolves to the correct legal value:

```
Furniture / Living Room Furniture / Coffee Tables & End Tables / Coffee Tables
```

## Why It Works

The fabricated path is not a guess at the answer — it is a **query rewritten into category register**. Comparing "brown coffee table" directly against taxonomy paths compares two different kinds of text; comparing an invented path against real paths compares like with like. The LLM supplies domain reasoning; the embedding index supplies vocabulary safety.

This is the same manoeuvre as [[Hypothetical Document Embeddings]], with the target swapped: HyDE writes a fake *document* to retrieve real documents, this writes a fake *category* to retrieve a real category.

## Consequences

- The task can be handed to "dumb / cheap" LLMs — the model never has to know or respect the taxonomy.
- The schema never ships with the request, sidestepping both payload cost and provider limits on enumerated values.
- Vocabulary safety is guaranteed by construction: output is whatever the nearest-neighbour lookup returns, so an illegal value cannot escape.
- The taxonomy can change without touching prompts; only the embedded label index is rebuilt.

## Key Insight

> Just ask a dumb LLM to invent plausible, fake classifications for your query.

Constraining an LLM to a vocabulary is expensive. Letting it be wrong in a *structured, resolvable* way, and repairing the output downstream, is cheap.

## Resources

- Colab notebook demonstrating the approach on WANDS: https://colab.research.google.com/drive/1ljk72SBRuqWIijuEusCnDbhG1WAfZFcC
- `cheat-at-search` vocabulary utility: https://github.com/softwaredoug/cheat-at-search/blob/main/cheat_at_search/enrich/vocabulary.py
- Model referenced in the examples: `gpt-5.4-mini`

## Related Concepts

- [[Hypothetical Document Embeddings]] — the same generate-then-retrieve structure, aimed at documents
- [[Query Understanding]] — where query classification sits
- [[Embeddings]] — the resolution step
- [[Out-of-Vocabulary]] — the failure this pattern is engineered to prevent

## Related Articles

- [[Semantic Search Without Embeddings]] — Turnbull's earlier case for taxonomies as the semantic layer, which already floats hallucinated category paths as HyDE-style retrieval
- [[Classic ML to Cope with Dumb LLM Judges]] — same author, same WANDS dataset; the ensemble answer to the same cost problem
- [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] — the trained-classifier alternative to the same task

## Related Topics

- [[Query Classification]]

## People

- [[Doug Turnbull]]
