---
title: "This is what agentic retrieval looks like"
source: "https://hornet.dev/blog/this-is-what-agentic-retrieval-looks-like"
author:
  - "[[Jo Kristian Bergum]]"
published: 2026-05-20
created: 2026-05-31
description: "GPT-5 searches like a power user. Phrase quotes in 98% of sessions. Median query length past the human 99th percentile (AOL query log). The new user of search."
tags:
  - "clippings"
---
GPT-5 searches like a power user. Phrase quotes in 98% of sessions. Median query length past the human 99th percentile (AOL query log). The new user of search.

![This is what agentic retrieval looks like](https://hornet.dev/blog/this-is-what-agentic-retrieval-looks-like/hero.webp)

*Part 2 of a series on agentic retrieval. Part 1: [Deep research is a retrieval problem](https://hornet.dev/blog/deep-research-is-a-retrieval-problem).*

The median BrowseComp-Plus answer with GPT-5 + BM25 takes 24 search calls. The questions are riddle-like and multi-hop, the agent has only a search tool, and it assembles the answer one search at a time from a fixed corpus.

![Four-box flow showing the BrowseComp-Plus setup: a question goes to GPT-5, which calls a search tool that returns five snippets from a BM25 retriever over 100,195 web pages. The agent loops on the search tool a median of 24 times per question](https://hornet.dev/blog/this-is-what-agentic-retrieval-looks-like/pipeline.webp)

[Part 1](https://hornet.dev/blog/deep-research-is-a-retrieval-problem) showed that retrieval is a dominant bottleneck in BrowseComp-Plus: In an oracle setting where GPT-4.1 is given the required evidence documents, it answers 93% of questions correctly; with a weak retriever baseline it answers 14%.

This post zooms into the agentic query workload.

## Why retrieval at all?

That oracle accuracy number comes from a specific trick: the evidence documents for each question are hand-picked from the corpus and stuffed into the context window. It tells you how the model would perform if retrieval was perfect.

Real systems can't do that. The BrowseComp-Plus corpus contains 100,195 web pages, about 736 million GPT-4.1 tokens. A 128k context window holds about 0.017% of the corpus; even a 1M window holds about 0.14%. There is no fitting the corpus into the prompt.

So the agent has to search. Retrieval determines what slice of the corpus GPT-5 gets to read.

## A session of 24 search calls

The full [search trajectories](https://huggingface.co/datasets/Tevatron/browsecomp-plus-runs) are public, so we can read them end to end. The published GPT-5 + BM25 trace file contains 830 questions and 19,279 search calls. That works out to a median of 24 search calls per question, p90 35, max 63.

Inside a session, each search call becomes context for the next one. A useful document missed on turn 3 means turn 4 is reasoning over a different set of snippets, and the miss affects every subsequent turn. Poor retrieval compounds across the session.

## The search API is one string

In the standard BrowseComp-Plus protocol harness, the search tool exposes one query-string parameter. Each call returns the top 5 snippets of at most 512 tokens.

Names, dates, phrases, and any query operators GPT-5 has learned to use have to fit inside that one query string parameter. If the backend implementation ignores some of that query syntax, GPT-5 may think it applied a constraint the retriever never enforced. That one-string query interface is a holdover from human search. [Davis Treybig](https://davistreybig.substack.com/p/how-agents-use-systems-differently) describes the shift: systems assume a "dumb client, smart server" (a human typing two words into a box backed by a server that does the heavy lifting), while agents are smart clients that can recognize entities and write long, well-specified queries.

## Long queries

Across all search calls, the average query is 11.03 terms, median 10, p90 17, max 78. For reference, the [AOL search log](https://hornet.dev/blog/the-scaling-dimensions-of-keyword-search) puts the median human query at 2 terms and the 99th percentile at 8. GPT-5's median query sits past the human 99th percentile.

![Bar comparison of query length percentiles between the AOL search log (2006, 36 million human queries) and the GPT-5 + BM25 BrowseComp-Plus run (19,279 agent queries): human median 2, p90 5, p99 8; agent median 10, p90 17, first-query mean 19. The agent median is longer than 99% of human queries.](https://hornet.dev/blog/this-is-what-agentic-retrieval-looks-like/human-vs-agent-query-length.webp) *Bar comparison of query length percentiles between the AOL search log (2006, 36 million human queries) and the GPT-5 + BM25 BrowseComp-Plus run (19,279 agent queries).*

![Average query length by turn position across 830 GPT-5 + BM25 BrowseComp-Plus sessions: turn 1 averages 19.1 terms, drops to 12.5 at turn 2, and plateaus near 10 for the rest of the session](https://hornet.dev/blog/this-is-what-agentic-retrieval-looks-like/query-length-by-turn.webp) *Average query length by turn position across 830 GPT-5 + BM25 BrowseComp-Plus sessions.*

Question 786 is a good first trace to read. GPT-5 takes 46 searches to answer it.

**Turn 1, 26 terms**

query decrypted in browser

> "Perfectly formed" described themselves "Perfectly formed" born in the 1950s first- and second-generation Indian immigrants film 1 hour and 31 minutes nephew directed a short film

**Turn 7, 8 terms**

query decrypted in browser

> "1 hour and 31 minutes" film Kevin Connor

**Turn 46, 3 terms**

query decrypted in browser

> "Kiran Shah" "nephew"

Each of those queries hits a backend tuned for the short, single-shot human distribution. We wrote about the serving side of that problem in [the scaling dimensions of keyword search](https://hornet.dev/blog/the-scaling-dimensions-of-keyword-search).

## GPT-5 writes web-search syntax

The queries performed by GPT-5 look like an expert web searcher using advanced query operators.

![Operator usage in GPT-5's BrowseComp-Plus queries: phrase quotes appear in 66% of queries and 98% of sessions, year operators in 46% and 95%, multiple years in 17% and 74%, and site: filters in 6% of queries but 48% of sessions](https://hornet.dev/blog/this-is-what-agentic-retrieval-looks-like/operator-usage.webp)

GPT-5 uses quotation marks (phrase search) in 65.56% of individual queries and 98.19% of sessions, writing as if exact strings matter to the backend and quoting proper names, publication titles, and verbatim fragments from the original question.

Four-digit years appear in 45.60% of queries and 95.42% of sessions; 73.61% of sessions contain more than one. Many BrowseComp-Plus questions hinge on a specific year (a publication, a conference, an appointment), so GPT-5 carries dates the way it carries names.

`site:` is a query operator supported by Google and Bing that restricts a search to a specific domain. It appears in 6.43% of individual queries, but 48.07% of sessions reach for it at least once. Whether or not the backend honors the filter, GPT-5 uses it actively.

The trace also contains operator combinations humans almost never type:

**`OR` across a year range**

query decrypted in browser

> "born June" "video game composer" 1971 OR 1970 OR 1969

**Wildcard subdomain**

query decrypted in browser

> site:\*.org "January 28, 2019" "Blog" art

**`filetype:` stacked with `site:` and phrase quotes**

query decrypted in browser

> site:surrey.ac.uk filetype:pdf "student numbers" "2018/19" "University of Surrey"

**Negation**

query decrypted in browser

> "Memphis 13" -football -soccer Wikipedia

Major web search engines spent the last decade deprecating operators because humans stopped using them. Davis Treybig argues operators ["will need to make a come back for agents"](https://davistreybig.substack.com/p/how-agents-use-systems-differently) : the agent understands which operator applies, and uses it. The trace above demonstrates that GPT-5 reaches for those operators.

Meng et al. ([*Revisiting Text Ranking in Deep Research*](https://arxiv.org/abs/2602.21456) ) see the same query style in open-source agents. The pattern is not unique to GPT-5 or the BrowseComp-Plus harness. Meng et al. also find that the queries GPT-5 asks are out of distribution for neural retrievers. They are trained on [MS MARCO](https://arxiv.org/abs/1611.09268) and [Natural Questions](https://ai.google.com/research/NaturalQuestions) , where queries are fluent natural-language questions. This distribution shift between train and test causes trained neural retrievers to underperform.

## Building for a different user

Retrieval infrastructure was built and tuned to match the workloads generated by humans. Inverted indexes are tuned for short queries, and BM-WAND-style pruning [degrades past about 7 terms](https://hornet.dev/blog/the-scaling-dimensions-of-keyword-search) when term weights are uniform. Neural retrievers are trained on MS MARCO and Natural Questions, where queries are short and fluent. Search APIs expose one string of input because that is what a human at a search box typed; operators were deprecated for the same reason. Benchmarks score the original question once because that is what humans asked. None of those choices were wrong for the workload they targeted. They just do not describe the workload in this trace.

Part 1 showed that retrieval is the dominant bottleneck in BrowseComp-Plus. The 79-point gap between oracle retrieval and weak BM25 sits where the distributions diverge: 24 calls per question, 19-term first queries, phrase quotes in 98% of sessions, operators reached for in nearly half, every call conditioned on the last.

This is the workload we are building [Hornet](https://hornet.dev/blog/the-case-for-a-new-retrieval-engine-for-agents) for.

---

*Part 3 examines why BM25 looks weak in the one-shot retrieval table but considerably stronger inside the agent loop, and what that means for how you evaluate retrieval.*

*Part 4 looks at what happens when you put the best retrieval strategies together.*

*We're building Hornet for teams working on agentic retrieval. To be notified about new posts, benchmarks, and early product notes,.*