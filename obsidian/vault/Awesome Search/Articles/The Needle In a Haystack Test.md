---
type: article
title: "The Needle In a Haystack Test"
source: "https://towardsdatascience.com/the-needle-in-a-haystack-test-a94974c1ad38"
author: ["Aparna Dhinakaran"]
published: 2024-02-15
tags:
  - clippings
  - llm
  - evaluation
  - context
  - rag
concepts:
  - Needle in a Haystack Test
  - Long-Context RAG
created: 2026-09-05
---

# The Needle In a Haystack Test

**Source**: https://towardsdatascience.com/the-needle-in-a-haystack-test-a94974c1ad38
**Published**: 15 February 2024 · **Author**: [[Aparna Dhinakaran]]

## Summary

An account of the needle-in-a-haystack evaluation — originated by Greg Kamradt, extended by Arize — which embeds **"a specific, targeted piece of information (the needle) within a larger body of text (the haystack)"** and measures whether the model can use it.

## Method

An out-of-place statement is inserted into essay text at varying **depths** (0–100%) and **context lengths** (1K to the model's limit). The model answers using only the provided context; accuracy is charted across both axes.

## Results

| Model | Finding |
|---|---|
| ChatGPT-4 | Decline below 64K tokens; sharp decline past 100K. Overall leader. |
| Claude 2.1 | 27% retrieval accuracy initially → **98% with prompt adjustments** |
| Mixtral-8x7B-v0.1 / 7B Instruct | Outperformed expectations for their size |

Arize's follow-up cut Claude 2.1's misses from 165 to 74 through revised prompting alone.

## Reading It Critically

A 71-point swing on prompt phrasing means the benchmark partly measures [[Prompt Sensitivity]] rather than context capability — worth holding in mind before citing any single number from it.

## Related Concepts

- [[Needle in a Haystack Test]] — primary topic
- [[Long-Context RAG]] · [[Prompt Sensitivity]] · [[RAG]]

## Related People

- [[Aparna Dhinakaran]]
