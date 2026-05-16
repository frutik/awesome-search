---
title: "Mutually assured distraction"
source: "https://hornet.dev/blog/mutually-assured-distraction"
author:
  - "[[Lester Solbakken]]"
published: 2026-01-30
created: 2026-05-15
description: "Why better retrieval and better reasoning can make agentic systems less reliable."
tags:
  - "clippings"
---
Why better retrieval and better reasoning can make agentic systems less reliable.

![Mutually assured distraction](https://hornet.dev/blog/mutually-assured-distraction/hero.webp)

What seems like a very long time ago, I studied neuroscience. At my university the Mosers had recently won a Nobel Prize, and naturally every department scrambled to associate itself with their success. Mine, the fringe science department of AI at the time, also vectored in that direction. Computational neuroscience, but still.

One thing that stuck with me was what we, as humans, do *not* attend to. As our species evolved by rummaging through savannas and jungles and forests, we were bombarded with perception signals. Very little of that was relevant for spotting that lion or finding those berries. But the ability to focus on what matters and drown out the rest was a survival necessity. This spotlight attention mechanism suppresses the irrelevant to focus on the salient.

Which brings me to my current work: search and retrieval. For the longest time, search has been a list of more or less relevant items we skim through to find what we need. When presented with such a list, humans are remarkably adept at filtering out the irrelevant. The mental cost of skipping to the next result is low.

AIs, however, have evolved along a different path.

For an LLM, retrieval is not skimming through a list of results, it is context injection. The retrieved documents are not presented for review but are ingested in parallel and actively shape the model's probabilistic reasoning. Unlike the human brain, which can compartmentalize and discard noise, the Transformer architecture processes input through a mechanism of self-attention where every token competes for probability mass. There is no "ignore".

The real threat is the distractor. Text that is plausible, semantically adjacent, high-confidence, and wrong. Distractors look like evidence. They survive ranking. And the moment they enter the context window, reliability degrades rapidly. Irrelevance becomes destabilizing.

This is what I mean by mutually assured distraction (MAD): a dynamic where locally rational optimizations in retrieval and reasoning lead to global system instability. Better retrievers produce more convincing distractors; better reasoners trust those distractors more deeply. Both sides improve; both sides lose.

Most current retrieval pipelines are measuring the wrong variables and are thus optimizing for fragility. A more defensive approach to retrieval, one based on utility-based metrics, verifiable infrastructure, and distraction-aware ranking, can help. But without it, autonomous agents face a hard reliability ceiling.

## Lost in the noise

Recent evidence for this comes from a study in ["Lost in the Noise"](https://arxiv.org/abs/2601.07226). They stress-tested models across many tasks by injecting different kinds of noise: random documents, irrelevant chat history, and hard negative distractors. The findings regarding hard negatives are particularly brutal. In some specific tasks, such as multi-hop reasoning and tool-use scenarios, accuracy dropped by up to 80%.

The danger is plausible irrelevance. A document that "looks right" but is wrong survives the initial phase of retrieval because it scores high on signals such as similarity. By the time the model attempts to reason over the data, the distractor has already been integrated into the context as a valid premise.

Here is an uncomfortable part for retrieval. As retrievers improve, their mistakes get better too. Stronger retrievers create better distractors.

Counterintuitively, ["The Power of Noise"](https://arxiv.org/abs/2401.14887) finds that padding context with random documents can actually improve accuracy. The hypothesis is that random noise increases attention entropy, preventing the model from latching onto any single source. Distractors, the plausibly irrelevant, do the opposite. They look credible, so attention sharpens around the wrong evidence.

What I find unsettling is the phenomenon of "inverse scaling under noise". This challenges the prevailing "scale is all you need" orthodoxy. In clean, sanitized benchmarks, allowing a model to generate intermediate reasoning steps significantly boosts accuracy. However, this study reveals that this relationship inverts in the presence of distractors. When the context is polluted with hard negatives, giving the model more time to think (generating a longer chain of thought) actually lowers accuracy.

You cannot reason your way out of bad context, and you cannot compute your way out of distraction.

## Agentic collapse

The risks of distraction are compounded when we move from transactional RAG (a single query-response cycle) to agentic workflows (loops of reasoning-acting-observing). In an agentic loop, the output of step `t` becomes part of the context for step `t+1`. If a distractor causes a minor error in step `t`, that error is re-injected into the context window for the next iteration, which creates a feedback loop of error propagation.

A system with a 90% success rate per step will have a roughly 53% success rate after just 6 steps. In a transactional RAG system, a distractor ruins one answer. In an agentic system, a distractor can ruin the entire workflow.

## Measuring the wrong thing

The root cause of mutually assured distraction is the misalignment between what we optimize for and what actually matters. The industry has historically relied on Information Retrieval metrics like nDCG, MAP, and MRR. These metrics were designed for the era of human search and are fundamentally flawed when applied to agentic retrieval.

For language models, "irrelevant" is not one thing. Some passages are actively harmful. A retriever can score high on nDCG while consistently injecting distractors that sabotage downstream reasoning.

To address this, Trappolini et al. introduced UDCG (Utility and Distraction-aware Cumulative Gain). This metric assigns negative utility scores to distractors. Utility is derived from model behavior: if a passage makes the model answer correctly it is positive, and if it makes the model answer when it should abstain it is negative. In their experiments, they report up to a 36% improvement in correlation with end-to-end answer accuracy compared to traditional metrics.

UDCG exposes that precision is more valuable than recall in the agentic era, because a miss costs less than a distractor.

## Breaking the cycle

We can break the MAD cycle with more defensive retrieval, where we treat context like an interface with failure modes. This changes three things:

- What you measure: move from relevance to utility, and explicitly assign negative utility to distractors.
- What you inject: treat every extra chunk as a liability unless it increases sufficiency, and prefer dynamic-k over "always return k".
- What you do under uncertainty: make abstention a first-class outcome, and use it as a control signal to retry with a different query, different filters, or a different tool.

Clean context becomes a premium asset. Data providers and retrieval engines may begin to compete not on the size of their index, but on the purity and verifiability of the context they can deliver.