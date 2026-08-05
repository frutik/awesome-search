---
title: "MIRACL"
aliases: ["MIRACL benchmark", "Multilingual Information Retrieval Across a Continuum of Languages"]
tags:
  - dataset
  - benchmark
  - multilingual
  - retrieval
  - search-evaluation
type: dataset
source: University of Waterloo and collaborators (Zhang et al., 2022–2023)
domain: multilingual retrieval over Wikipedia, 18 languages
website: https://github.com/project-miracl/miracl
created: 2026-08-05
---

# MIRACL

## Overview

**MIRACL** (Multilingual Information Retrieval Across a Continuum of Languages) is a multilingual retrieval benchmark covering **18 languages** over Wikipedia corpora, with queries written and relevance judged by **native speakers** of each language.

That last point is the reason it exists. Most multilingual retrieval evaluation before it relied on machine-translated queries or labels, which bakes in translation artifacts: translated queries carry source-language phrasing and vocabulary, so a model that is merely good at English-shaped queries scores better than it deserves. MIRACL's native annotation avoids that and produces a genuinely harder, more honest test.

The language set deliberately spans typologically diverse and lower-resource languages, not just the European languages that dominate most benchmarks.

## Why It Matters

Nearly every current embedding model advertises support for "100+ languages" — see [[Embedding Models Compared]]. That claim is close to meaningless on its own, because coverage and quality are different things: a model trained on 100 languages is not equally good in all of them, and the tail languages are usually far weaker than the headline suggests.

MIRACL, along with MMTEB, is where those claims get checked. For any team with real multilingual traffic, per-language MIRACL results are far more informative than a multilingual average — and the average is what vendors quote.

## How to Use It

Read the **per-language table**, not the mean. Find your actual languages. A model with a strong average can be mediocre in the specific language that carries your traffic, and the aggregate will never tell you.

See [[Multilingual Search]] for the broader practice, and [[Model Selection and Fine-Tuning Evaluation]] for turning this into a decision.

## Related

- [[Retrieval Benchmarks and Leaderboards]] — the wider landscape
- [[Multilingual Search]] — the practice this benchmark serves
- [[MTEB]] — MMTEB is the other multilingual board
- [[BEIR]] — the English-centric zero-shot counterpart
- [[Embedding Models Compared]] — whose multilingual claims this tests
