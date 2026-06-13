---
type: article
title: "We're Bringing Learning to Rank to Elasticsearch"
source: "https://opensourceconnections.com/blog/2017/02/14/elasticsearch-learning-to-rank/"
author: "[[OpenSource Connections]]"
published: 2017-02-14
created: 2026-06-13
concepts:
  - Elasticsearch Learning to Rank
  - Learning to Rank
  - LambdaMART
topics:
  - Ranking and Retrieval
tags:
  - article
  - ranking
  - learning-to-rank
  - elasticsearch
  - ltr
---

# We're Bringing Learning to Rank to Elasticsearch

**Source:** https://opensourceconnections.com/blog/2017/02/14/elasticsearch-learning-to-rank/
**Author:** [[OpenSource Connections]] (announced by the team behind *Relevant Search*; [[Doug Turnbull]])
**Published:** 2017-02-14

The launch of the `o19s/elasticsearch-learning-to-rank` plugin — for years the only way to do [[Learning to Rank|LTR]] inside [[Elasticsearch]]. See [[Elasticsearch Learning to Rank]] for how it relates to Elastic's later native module and to external re-rankers.

---

## Core idea

Elasticsearch's Query DSL can already compute a wide variety of **query-dependent** relevance signals (TF*IDF on title, recency, price-vs-expectation, conceptual relatedness). The plugin's move: use those Query DSL queries as **feature inputs** to a machine-learned model. Manual relevance tuning is brittle and "good enough"; LTR learns the ranking function from a [[Judgment Lists|judgment list]].

The four LTR steps the post frames: (1) measure relevance → judgment list with grades 0–4; (2) hypothesize features; (3) train a model mapping features → relevance; (4) deploy to the search infrastructure.

## How it works

- Integrates **[[RankLib]]**: takes a judgment file, trains a model (LambdaMART = `-ranker 6`) in its own human-readable format, via CLI or programmatically.
- The plugin adds a custom Elasticsearch script language, **`ranklib`**, that accepts RankLib models as stored scripts.
- It adds a custom **`ltr` query** that takes a list of Query DSL queries (the features) plus a stored model name, and scores results.
- Because LTR is expensive, you almost never run the `ltr` query directly over a whole collection — you **`rescore`** the top-N (e.g. `window_size: 20`). Running the model directly over the full collection took hundreds of ms and doesn't scale.

## The worked example (TMDB movies)

- Start from a minimal judgment file: grade, `qid`, and the Elasticsearch `_id` as a comment per line; keyword strings (`rambo`, `rocky`) mapped to each `qid` in the header.
- Features are Jinja-templated Query DSL queries (`1.json.jinja` = `match` on `title`; `2.json.jinja` = `cross_fields` `multi_match` across overview/genres/title/cast/…).
- `train.py` issues bulk `_msearch` queries to log each feature's relevance score per keyword/document pair, writes a fully-fleshed RankLib training file (`1:9.476 2:25.82 …`), runs `RankLib.jar` to train, and POSTs the model into Elasticsearch as a `ranklib` script.
- Search via a `match` first pass + `rescore` carrying the `ltr` query with the stored model and its feature queries.

## Caveats the post stresses

A real LTR solution is "a tremendous amount of work" — studying users, analytics, data and feature engineering. Smaller orgs may still get better ROI from hand-tuned results. Too many features without enough representative training samples causes problems.

## Related Concepts

- [[Elasticsearch Learning to Rank]] · [[Learning to Rank]] · [[LambdaMART]] · [[RankLib]] · [[Judgment Lists]] · [[Reranking]]

## Related Articles

- [[Learning To Rank (LTR) - Elasticsearch Native]] — Elastic's later first-party module
- [[Search using LTR - Elastic Docs]]
- [[How LambdaMART Works]] — [[Doug Turnbull]]'s explainer of the model this plugin trains via RankLib
- [[Learn-to-Rank with OpenSearch and Metarank]] — the external-re-ranker alternative

## People

- [[Doug Turnbull]] — co-founder of OpenSource Connections; co-author of *Relevant Search*

## Companies

- [[OpenSource Connections]]
