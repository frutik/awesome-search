---
type: concept
title: "Prompt Optimization"
aliases: ["prompt optimisation", "automatic prompt engineering", "prompt tuning", "instruction optimization"]
tags:
  - concept
  - llm
  - prompting
  - optimization
  - search-evaluation
created: 2026-09-20
---

# Prompt Optimization

## Definition

**Prompt optimization** treats the instruction given to a model as a *parameter to be searched*
rather than a string to be authored. Given a metric and a set of labelled examples, a search
procedure proposes instruction variants, scores them, and keeps what wins — the same loop as
hyperparameter tuning, with natural language in the parameter slot.

It is the direct structural answer to [[Prompt Sensitivity]]. If reworded instructions produce
materially different labels, the wording is part of the measuring instrument, and hand-authoring
it means shipping an untuned instrument.

## The Shape of the Loop

Approaches differ in how variants are proposed, but the frame is constant:

1. **A metric**, computed on held-out examples. Everything depends on choosing this well — the
   optimizer will faithfully maximize whatever you name.
2. **A proposal mechanism.** Reflective methods have a generative model read the current
   instruction and its failures and write a better one; others mutate, recombine, or select
   few-shot exemplars.
3. **A selection rule.** Greedy hill-climbing commits early; Pareto-style selection keeps several
   candidates that win on *different* examples.
4. **A held-out split that the search never sees**, because an optimized prompt overfits as
   readily as any other fitted parameter.

Two tools in this vault implement the frame: [[GEPA]] (reflective proposals, Pareto selection)
and [[DSPy]] (signatures and modules with pluggable optimizers). The relationship worth noting is
that the model being optimized and the model doing the proposing need not be the same — or even
the same *kind* of model.

## Why It Matters for Search

Three places the lever applies directly.

**Judge rubrics.** An [[LLM as Judge]] rubric is a prompt, and
[[Levels of Judge Agreement|agreement figures]] are uninterpretable without it. Optimizing the
rubric against human labels makes the judge a fitted artifact with a held-out score, rather than
a hand-written one with an anecdote.

**Non-generative scorers.** A [[System One Model]] like [[Jev]] writes no text and cannot reflect
on its own mistakes — but it returns a probability, which is all a metric needs.
[[Adapting Jev to Your Domain with GEPA]] optimizes a [[Jev]] instruction with an assistant
supplying the proposals, and the result reframes what published zero-shot numbers mean: an
untuned prompt is a **lower bound**, not a measurement of the model.

**Calibration as a target.** That same study optimized against [[Brier Score|Brier score]]
instead of accuracy, and got both — Brier down 44.9%, F1 up 10.62 points on a fresh split. Naming
the probability rather than the label as the objective is the more interesting half of the
result, because it means [[Calibrated Relevance Probability|calibration]] is something you tune
rather than something you inherit.

## What Can Go Wrong

- **It optimizes the metric, not the goal.** A prompt fit against a labelled corpus can learn
  that corpus's *annotation conventions* rather than the underlying truth — stated as an explicit
  limitation in the worked example above, where nobody independently adjudicated the labels.
- **It overfits a small validation set.** A 100-example validation split carrying 21 positives
  gives a very coarse signal about where a threshold belongs.
- **Cost moves too.** The winning prompt in that study grew from 503 to 2,020 characters, raising
  input tokens per request by about 64% — cheap when billing is input-only, less so otherwise.
- **The optimizer's own cost is invisible.** Reflection calls and orchestration are usually
  excluded from the reported bill for the optimized system.
- **It is fitted to a distribution.** An optimized prompt is a tuned parameter and, like any
  tuned parameter, needs re-checking when the corpus moves ([[Out-of-Time Validation]]).

## Related Concepts

- [[Prompt Sensitivity]] — the problem this answers
- [[Brier Score]] · [[Expected Calibration Error]] — objectives worth optimizing that are not accuracy
- [[Calibrated Relevance Probability]] — what optimizing a probability metric improves
- [[LLM as Judge]] · [[Levels of Judge Agreement]] — rubrics as fitted artifacts
- [[Context Engineering]] · [[Clean Context]] — the neighbouring lever: what goes in, not how it is asked
- [[Statistical Significance in Search Evaluation]] — a prompt delta needs an interval
- [[System One Model]] — a model class that can be optimized without being able to reflect
- [[Out-of-Time Validation]] — revalidating a fitted prompt

## Related Tools

- [[GEPA]] — reflective prompt evolution with Pareto selection
- [[DSPy]] — declarative programs whose prompts are compiled by optimizers

## Related Articles

- [[Adapting Jev to Your Domain with GEPA]] — [[Praneeth Paikray]]; optimizing a non-generative model's instruction against a calibration metric
