---
type: concept
title: "ESCI Label Scheme"
aliases: ["ESCI labels", "ESCI scale", "ESCI relevance scale", "ESCI annotation scheme", "Exact/Substitute/Complement/Irrelevant", "E/S/C/I"]
tags:
  - concept
  - search-evaluation
  - e-commerce
  - relevance-labels
created: 2026-10-01
---

# ESCI Label Scheme

The ESCI label scheme grades a (query, product) pair as **Exact**, **Substitute**, **Complement** or **Irrelevant**. It was introduced with Amazon's [[Amazon ESCI Dataset|Shopping Queries Dataset]] and has since travelled well beyond it: in-house judgment programs, LLM-judge guidelines and relevance models now use the four grades without touching the dataset itself. The scheme matters because it labels *shopping intent* rather than text match.

---

## The Four Grades

| Grade | Label | Meaning |
|---|---|---|
| E | **Exact** | The product directly matches the query |
| S | **Substitute** | The product could stand in for what was asked, but isn't an exact match |
| C | **Complement** | The product goes with what was asked — an accessory or companion item |
| I | **Irrelevant** | The product is not relevant to the query |

Substitute and Complement are the two near-misses that dominate [[E-commerce Search|product search]]: a product that could replace the requested one, and a product that is used together with it. A binary relevant/not-relevant scale has to fold one or both of them into a single bucket; ESCI keeps them apart.

## Why It Differs from Topical Relevance

In web or document search, relevance is mostly topicality — is the result about the query? For e-commerce, [[Do LLM Judges Actually Agree With Us]] argues that the useful grading is substitutability: ESCI is a judgment about shopping intent rather than about text, and that relocates the hard boundary. A phone case is topically about the phone, but it is a Complement, not an answer to the query for the phone.

Compared with the label schemes of the other public e-commerce sets (see [[E-commerce Search Evaluation Datasets]]):

| Scheme | Used by | Grades |
|---|---|---|
| ESCI | [[Amazon ESCI Dataset]], [[ESCI-S Dataset]] | Exact / Substitute / Complement / Irrelevant |
| Exact / Partial / Irrelevant | [[WANDS Dataset]] | Near-misses collapsed into one Partial grade |
| Continuous 1–3 | [[Home Depot Product Search Relevance]] | Averaged crowd scores |
| Binary | [[MS MARCO]] | Relevant / not relevant |

WANDS's single Partial grade is simpler to annotate, but you can't tell a substitute from an accessory.

## Using the Grades

**As graded evaluation labels.** Because the grades are ordinal, they can serve as gain values for [[NDCG]] directly, which binary relevance sets cannot.

**As training data.** The standard construction for fine-tuning a retriever treats **Exact and Substitute as positives** and drops Complement, since a complementary product is a different intent rather than a relevance signal. [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] trains [[SPLADE]] this way.

**As a diagnostic.** The grades can also be turned into retrieval metrics. In [[Distilling Retrieval Pipelines to a Single Embedding Model 1|Distilling Retrieval Pipelines to a Single Embedding Model]], [[Daniel Tunkelang]] tracks an "ESCI precision" and a complement retrieval rate: across 74K queries, his fine-tuned query encoder moved ESCI precision from 96.0% to 97.0% and cut the complement retrieval rate from 14.2% to 7.7% compared with the model before fine-tuning — one experiment on his own pipeline.

## Adoption Beyond the Dataset

- **[[Allegro]]** modeled the labeling guidelines for its 380K+ multilingual judgment set on the ESCI scale, built by 30 experts with dual blind annotation and expert arbitration — see [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]].
- **[[Etsy]]** plans to split its "partially relevant" grade into complements vs. substitutes, taking inspiration from ESCI — see [[Semantic Relevance]] and [[How Etsy Uses LLMs to Improve Search Relevance]].
- **sQuIrRel** uses a relevance model that predicts the ESCI labels, keeping only confident *exact* matches to derive query-to-product-type labels. It never uses the public dataset; the connection is the taxonomy alone — see [[sQuIrRel - Large-Scale Evaluation of E-commerce Query Classification Models]].

## Where the Scheme Is Hard

The grade boundaries are not equally easy to judge.

- **Graded near-misses are the weak boundary for [[LLM as Judge|LLM judges]].** Allegro's judge reached per-class F1 around 0.94 on exact matches and 0.83 on complements, but only 0.51 and 0.33 on its own finer split of the substitute region ("highly substitutable" vs. "substitutable"). Exact-vs-garbage is easy; substitute-vs-slightly-worse-substitute is not.
- **Exact vs. Complement leaks.** sQuIrRel's one systematic error was complementary product-type confusion, which the paper puts at around 20% — `vacuum cleaner` for the query "vacuum cleaner handle" — and which looks like an exact-versus-complement miss.
- **Human labels are noisy too.** The public ESCI labels were crowdsourced before LLM labeling, so label noise should be expected.

## Related Concepts

- [[Judgment Lists]] — the artifact ESCI-graded pairs make up
- [[Semantic Relevance]] — Etsy's graded relevance, heading toward the same substitute/complement split
- [[LLM as Judge]] — ESCI-style grades as the target for LLM labeling
- [[NDCG]] — the metric the ordinal grades feed
- [[Search Evaluation]] — the enclosing practice
- [[Embedding Fine-tuning]] — Exact + Substitute as positives

## Related Topics

- [[E-commerce Search Evaluation Datasets]] — ESCI compared with WANDS and Home Depot label schemes
- [[E-commerce Search]]
- [[Search Quality Assurance]]

## Datasets

- [[Amazon ESCI Dataset]] — where the scheme was introduced
- [[ESCI-S Dataset]] — same labels, enriched product metadata

## Related Articles

- [[Do LLM Judges Actually Agree With Us]] — relevance as substitutability, and where ESCI-shaped labels break LLM judges
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — Allegro's ESCI-inspired judgment set
- [[How Etsy Uses LLMs to Improve Search Relevance]] — a planned ESCI-style split of partial relevance
- [[sQuIrRel - Large-Scale Evaluation of E-commerce Query Classification Models]] — the label scheme reused without the dataset
- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — Exact and Substitute as training positives
- [[Distilling Retrieval Pipelines to a Single Embedding Model 1|Distilling Retrieval Pipelines to a Single Embedding Model]] — ESCI precision and complement rate as retrieval metrics

## People

- [[Daniel Tunkelang]] — complement retrieval rate as a diagnostic
- [[Andrew Kornilov]] — relevance as substitutability in product search
