---
title: "Agentic Search as an Agile Engineering Process"
source: "https://dtunkelang.medium.com/agentic-search-as-an-agile-engineering-process-5514b0790e8e"
author:
  - "[[Daniel Tunkelang]]"
published: 2026-03-26
created: 2026-05-15
description: "More"
tags:
  - "clippings"
---
*(co-authored with* [*Asif Makhani*](https://www.linkedin.com/in/asifmakhani/)*, co-founder of* [*Infino AI*](https://infino.ai/)*)*

Search is usually framed as [retrieval](https://medium.com/search?q=retrieval+tunkelang): given a query, return the most [relevant](https://dtunkelang.medium.com/ranking-vs-relevance-ba672c79625e) documents. Today, that framing is breaking down.

[Agentic search](https://medium.com/search?q=agent+tunkelang) systems do more than retrieve: they plan, decompose, execute, verify, and refine. They behave less like function calls and more like software engineering teams pursuing goals under uncertainty.

Once you see this, a natural question follows: If agentic search is a form of engineering, what methodology should guide it?

[Agile software engineering](https://en.wikipedia.org/wiki/Agile_software_development) offers a compelling answer — not just as an analogy, but as a control system.

## Search as Engineering without a Specification

A traditional software project starts with a specification. Search does not.

A query is an incomplete, often ambiguous description of a goal. The system must infer intent, explore interpretations, and iteratively construct an answer.

From this perspective:

- The query is a partial specification.
- Retrieval and reasoning comprise implementation.
- Results represent candidate solutions.
- Interaction becomes part of the evaluation loop.

Search is what engineering looks like when the specification is missing.

## Agentic Search as Managing a Workflow

Traditional search executes in a single pass. Agentic systems do not.

Agentic search:

- Breaks problems into subtasks.
- Delegates subtasks to tools.
- Explores multiple paths.
- Refines based on intermediate results.

Agentic search no longer executes queries. It manages workflows. This is exactly the kind of process agile methods are designed for.

## Iteration as Uncertainty Reduction

Agile development is fundamentally about reducing uncertainty through iteration. The same is true for agentic search.

Each step should be evaluated not just by what it produces, but by how much uncertainty it removes per unit of cost.

This reframes the agentic search process as a sequence of uncertainty-reducing experiments.

## The Tradeoff: Scope, Cost, Quality

Perhaps the most important foundation of software engineering is the classic [scope-time-quality triangle](https://en.wikipedia.org/wiki/Project_management_triangle): you want to optimize scope, time, and quality, but you cannot achieve all three. At most, you can pick two.

In agentic search, we can translate engineering time into cost, so the tradeoff becomes:

- Scope: how much of the problem space the search covers.
- Cost: aggregate spend on tokens, tool calls, and other computation.
- Quality: a combination of correctness, completeness, and confidence.

As in software engineering, it is always possible to mitigate uncertainty by [reducing scope](https://dtunkelang.medium.com/reduce-scope-9c46d7632b60). However, the critical constraint is likely to be cost, since projects have finite budgets. These three levers define the tradeoff in every agentic search workflow.

## The Triangle in Practice

Here are three common strategies for managing this tradeoff in practice:

- Treat cost and quality as fixed, and reduce scope. This strategy takes a narrow focus, only explores high-confidence paths, and stops early. This tends to be the default strategy for agentic search.
- Treat scope and quality as fixed, and increase cost. This strategy emphasizes broader exploration, aggressive verification, and conflict resolution. This is what many systems expose as “deep research”.
- Treat scope and cost as fixed, and sacrifice quality. This strategy leads to skimming content, summarization, and accepting lower confidence. This is often exposed as a “quick overview” mode.

Each strategy makes a different tradeoff and can produce dramatically different results. Also, unlike in most software engineering contexts, the tradeoffs can be adjusted dynamically throughout the process.

## Searchers as Product Owners, Agents as Engineers

In agile software development, there are two key [roles](https://en.wikipedia.org/wiki/Scrum_\(project_management\)#Scrum_team). The product owner defines and prioritizes goals. Engineers own all aspects of execution.

In agentic search, the searcher is the product owner, while agents fill the roles of engineers.

However, much as can happen with software development, searchers may not know what they want until they see it. The process is iterative: requirements evolve as results come in.

But unlike software development, where [iterations](https://en.wikipedia.org/wiki/Timeboxing) are measured in days, agentic search iterations are measured in minutes or even seconds. This makes the loop tighter, faster, and more volatile.

## Task Sizing: A Critical Challenge

A central challenge in both agile and agentic systems is decomposition. Larger tasks increase efficiency by reducing coordination overhead, but they also increase risk. Smaller tasks reduce risk but decrease efficiency.

The optimal tradeoff balances the cost of coordination against the [expected cost of errors](https://dtunkelang.medium.com/to-ask-or-not-to-ask-that-is-the-question-for-ai-agents-8735027ecd67). This tradeoff determines:

- How many steps an agent takes.
- How much reasoning an agent packs into each step.
- How often the agent verifies that it is on the right path.

This is one of the most important — and underexplored — design decisions in agentic search workflows.

## The Cost of Iteration: Unpredictability

One of the classic frustrations with agile software development — especially for product managers! — is its lack of predictability. It is impossible to know exactly when a project will finish.

Agentic search inherits — and amplifies — this property.

The searcher does not know:

- The number of steps required.
- The number of branches to be explored.
- The sources of uncertainty.

However, as with software engineering, trying to force predictability leads to worse outcomes:

- Premature stopping.
- Shallow exploration.
- Lower-quality results.

So it is important to remember that predictability is not the goal for which agentic search can or should optimize.

## Replacing Predictability with Evaluability

Agile development replaces predictable completion with predictable progress. Agentic search takes this idea one step further: it does not define “done” upfront; instead, it detects completion using evaluation.

This framing informs the entire iterative workflow. The question is never “How many steps remain?”; rather, it is “Is further work worth the cost?”

An agentic system is “done” when spending more is not expected to improve the quality of the outcome. In other words, does the expected marginal gain justify the marginal cost?

## Testing is the Definition of Done

In software engineering, “done” is defined by passing tests. In agentic search, evaluation replaces this “definition of done”.

What needs to be evaluated?

- Outcome: correctness, completeness, and usefulness.
- Process: validation of exploration and verification strategies.
- Efficiency: maximization of ROI, minimization of wasted effort.

While some of this evaluation can be automated, the searcher plays a critical role in evaluating outcomes.

## Testing Replaces Explainability

People like explainability. Unfortunately, we have learned from the evolution of search that explainability is incompatible with the modern neural [AI-powered search](https://dtunkelang.medium.com/ai-powered-search-embedding-based-retrieval-and-retrieval-augmented-generation-rag-cabeaba26a8b) methods that achieve the best performance.

For the most part, we have learned to accept reduced explainability in exchange for better outcomes, and that also holds true for agentic search.

However, what we need is not explainability, but the ability to test the process. We need to be able to evaluate outcomes and audit processes.

## Putting it all Together

Agentic search brings together three interacting layers:

- An agile, iterative workflow to reduce uncertainty.
- The constraints and tradeoffs of the scope–cost–quality triangle.
- An evaluation process that establishes a definition of done.

Together, these form a control system for reasoning under uncertainty.

This framing suggests concrete design principles:

- Prioritize steps that maximize uncertainty reduction per unit of spend.
- Dynamically adjust scope based on budget and confidence.
- Size tasks to balance coordination costs against expected costs of errors.
- Integrate verification into the iteration and refinement processes.
- Define and enforce evaluation-driven stopping criteria.

## Final Thought

The agile development methodology recognizes and accepts that we cannot predict exactly when the work will be complete.

Agentic search goes further: it is not just a question of whether the process is complete, but rather whether the results are good enough and further effort does not justify the cost.

This shift — from execution to evaluation — is what turns search into an engineering problem and motivates an agile approach.

## Related Concepts
- [[Agentic Search]] — the paradigm this article frames
- [[RAG]] — retrieval component of agentic search
- [[Search Evaluation]] — evaluation as the "definition of done" in agentic systems
- [[LLM as Judge]] — automated evaluation in the agentic loop

## People
- [[Daniel Tunkelang]] — co-author
- [[Asif Makhani]] — Infino AI; co-author