---
title: "Agentic Search Models with OpenSearch and Elasticsearch"
source: "https://bonsai.io/blog/agent-search-with-sid/"
author:
  - "[[SID.ai]]"
published: 2026-06-05
created: 2026-06-18
description: "We introduce agentic tool-based retreival models, and show how they are shaping the future of search quality."
tags:
  - "clippings"
---
Tuning search is tricky, and the tools of yesterday are good but require lots of effort and data to get right. In this post I'm going to introduce purpose-built agentic LLMs for searching and reranking, which are an easy drop-in solution for relevance improvement.

Specifically, I got preview access to the [SID-1](https://www.sid.ai/research/sid-1) model, which I'll demonstrate after introducing the problems it is meant to solve. I'll walk you through implementing the model in an accessible search experience, building on an existing search application I made for my [last post for the Gutenberg project corpus](https://bonsai.io/blog/managed-search-on-render-with-bonsai/).

> “
> 
> SID-1 is our first model for agentic retrieval: 1.9x more likely to surface the right results than embedding-only search across general knowledge, finance, science, legal, and email. It is more accurate than agentic retrieval based on Gemini 3 Pro, Sonnet 4.5, and GPT-5.1 at its highest compute setting, while being 24x faster (144 vs 5.7 seconds).
> 
> ”

Before diving in to the post, let's start with a quick demo. Try a couple searches, observe what's happening, and then keep that experience in your head as I unfold the details in the rest of the article.

This demo is actually usable in this page. Try it out! <iframe src="https://bonsai-training-example-7zmt.onrender.com/books/agent"></iframe>*Try the interactive search above, or go to a [full demo](https://bonsai-training-example-7zmt.onrender.com/books/agent)!*

## Problems

I always like to start my posts with a list of problems we have. And here are some really challenging gaps that exist in pretty much every hybrid search solution:

- The best results might not be at the top
- Noisy/irrelevant results might polute the page
- The user's query might not match the corpus/domain language
- Vector search has no cutoff (everything is a "match")

In search, each of these is the deepest of rabbit holes. I've cumulatively spent YEARS trying to solve these problems in various products. SID and other multi-turn retrieval models do a great job of generalizing a solution path that gets you most of the way there.

## LLMs to the rescue?

Generally, the recent consensus has been "the AI should do it". But finding the best way for AI to solve these problems has been a rough road.

We tried using [LLMs for judgements](https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree). Which is hit or miss, and even before ChatGPT was around I ran up against this paradox in February 2022:

![The paradox of synthesized relevance judgements is that if you could automate them successfully then that would be your ranking model.](https://bonsai.io/blog/agent-search-with-sid/synthesized-judgements-paradox.png?h=t4DQhl1ND6Q183orp9ngA25sOJEGehgNQeAVeBGGA2U=)

But when automatically judging every result pair at query time and reranking we quickly ran into "oh my goodness this is very slow and expensive" problems...especially as [pair-wise judgements](https://softwaredoug.com/blog/2026/02/27/consider-pairwise-evals-instead-of-pointwise) is where we found the best effectiveness.

So lots of teams just start with RAG: tune a prompt to summarize the results, and deprioritize the results themselves. I've had some grievances with RAG for a while - summaries are hard to [wrangle and evaluate](https://maxirwin.com/articles/interleaving-rag/). Also, while RAG fills a certain need, sometimes we just want the actual search results. We're smart and we want to look at source information and decide for ourselves. Not to mention that RAG gets in the way of discovery - one of the best parts of search.

![Anyone use just simple retrieval without the generation part?](https://bonsai.io/blog/agent-search-with-sid/retrieval-without-the-generation-part.png?h=yIZW9l27pLwWDp5DLHN9DIegyEXuazG+Byf3vgr+MX8=)

## Agentic retrievers as a solution

One pattern that has emerged recently is tool-based search aka agentic retrieval aka multi-turn retrieval. You've seen this pattern before running in the background of your coding agent or chat - several web searches get executed by the LLM to grab source material, then the best results are pulled out and used to bolster the context and improve the outcome.

This solution has several characteristics which solve the problems listed above. The agent using this technique does the following:

- Writes several variants on a query to improve recall
- Executes the queries and gathers the results
- Picks the best results from all of the responses (and ignores noise)
- Iterates on the process based on what it found

We call each iteration of this process a "turn" in agent lingo.

After several turns, you have a short-list of really good results. Agents like ChatGPT or Claude can sometimes take 7 or 8 turns on this process.

SID will usually only take 2 or 3 turns, and then goes one step further with a specialized reranking turn. If the query is particularly long (I experimented with entire paragraphs as well), SID will then take 6 to 7 turns at most for retrieval, and 1 turn for rerank. The reranker will look at the final list, and reorder the results for relevance based on everything it gathered along the way.

Here's an illustrated example. In a Gutenberg books corpus, we search for the query *"novels inspired by early cultures"*. I'm not showing the actual results here, because first it's important to understand the process.

![3 turns for the query 'novels inspired by early cultures'](https://bonsai.io/blog/agent-search-with-sid/sid-turns.png?h=f3LEvqcEwrFCILyGiBYfnq6QkcMAAe37GgRBgdcmFQ4=)
- Turn 1: The model wrote 4 queries, we execute them all and gather ids
- Turn 2: The model wrote 2 more queries, we executes them all and gather ids
- Turn 3: The model has enough context and chooses the reranking "report\_helpful\_ids" tool.

Note that the model leans on its training data to add synonyms and narrow searches to try and find content. Query rewriting, especially when many queries are tried and sifted through, is a really nice pattern.

Also, I found that after a bit of learning, it was really easy to integrate into the existing search application. The model is built to work on anything with a search backend. The tool based approach is a good abstraction on top of any existing corpus and query you already have.

## Sequence of execution

Who doesn't love a sequence diagram or two?

Let's look at a basic pre-LLM 2-tier search architecture. There's a Search App, and an OpenSearch service. The user submits a query, and the search app executes a QueryDSL on an OpenSearch index. The app then takes the results and shows them to the user.

![A basic 2-tier search app](https://bonsai.io/blog/agent-search-with-sid/search-sequence-basic.png?h=D5+u0qpC4Q6p2gl6+WQmlnTuTqRljBTm4Y2PmvTwirY=)

With a turn-based search model like SID, the sequence is a bit more complicated. The Search App orchestrates invoking chat completions and tool execution when the model outputs the reply. This can happen up to 8 turns, and each turn the app requests a chat completion from the model API, gets a list of search tools to execute, runs the tools and processes the results. If the tool provided is `report_helpful_ids`, then there are no more turns and we finish up by fetching the documents for our reranked set and rendering for the user.

![An agentic search application flow](https://bonsai.io/blog/agent-search-with-sid/search-sequence-agentic.png?h=UVsPFJjLPSrQURKR+rT7d0q/NrZ9+56MSGanqe0cxpE=)

*Both diagrams generated at sequencediagrams.org*

## Dollars and Seconds

Purpose built agentic search models also excel at cost and speed when compared to the bigger general-purpose models. The SID team told me that they will price it similar to that of gpt-5.4-mini but their testing results show it is more accurate than the larger GPT-5.1 (which is a big and expensive model). If you're from the future using GPT-17.1, here's a cost comparison memory refresher for you:

After testing, a typical search for SID (with my example Gutenberg project dataset) uses about 10k tokens input and 400 tokens output.

| model | input | output | Average cost per query |
| --- | --- | --- | --- |
| gpt-5.4-mini | $0.75 | $4.50 | $0.00093 |
| gpt-5.1 | $1.50 | $10.0 | $0.0019 |

*input/output costs are per million tokens*

Here's a monthly cost table for you, based on how many queries per second (qps) you'd need to support:

| model | $ per query | 1 qps | 5 qps | 10 qps |
| --- | --- | --- | --- | --- |
| SID-1 | $0.00093 | $2,411 | $12,053 | $24,106 |
| gpt-5.1 | $0.0019 | $4,925 | $24,624 | $49,248 |

The GPT prices will also be higher than listed above, as the model would incur more turns per query (and therefore more tokens).

And, if you want to see how far a dollar goes:

| model | $ per query | queries per dollar |
| --- | --- | --- |
| SID-1 | $0.00093 | 1075 |
| gpt-5.1 | $0.0019 | 526 |

Let's move on to latency. In my testing, full 'took' time for the entire search has scaled in time with the length of the query, minimum 2 seconds maximum of 7 seconds. Note that this is specific to my dataset and setup. I'm using a Bonsai Standard Fir cluster and a Standard tier Render application both hosted in US East. I'm not sure where the SID model is hosted, but I don't notice any network latency - the bottleneck is of course the generation by the causal model. To make things snappy, I use `_msearch` per turn to batch all my queries in the same OpenSearch request.

## How it all works

So what's going on here? Why is SID beating GPT even though it's much smaller? GPT is a model for a general solution across many tasks, it can call any tool you throw at it and it's been trained with every conceivable knowledge task you can think of. SID, however, is a specialized model trained on just the rewrite/retreive/rerank toolset and outcome. This allows the team to use a smaller model and train it for this focussed task. Even though the model is small, the specialization and training regimen enable it to outperform the general model.

But what about implementation in a search application? I built upon the bonsai-training-example repo and dataset I used for my previous post on using [Render with Bonsai](https://bonsai.io/blog/managed-search-on-render-with-bonsai/).

Here is how I expanded the application:

The whole thing is three new files (`sid.js`, `agent.ejs`, `agent.css`) and minor additions to three existing files (`server.js`, `package.json`, `index.ejs`). About 800 lines of code total, and the only new dependency is the `openai` package since SID uses an OpenAI-compatible API.

### Talking to SID

The agent module (`sid.js`) points the OpenAI client at `api.sid-1.com/v1` and defines four tools for the model:

- `search` - runs a multi\_match across title, summary, author, and subject fields
- `text_search` - runs a query\_string for advanced syntax (wildcards, phrases, boolean)
- `read` - fetches a single document by ID so the model can inspect it more closely
- `report_helpful_ids` - the termination tool, returns the final ranked list

An important note: SID doesn't use the `tools` field in the OpenAI api chat completions request like you'd expect. You pass a dummy stub there (literally `{name: "dummy"}`), and your actual tool definitions go in the system prompt as structured text. This is in their docs but it's easy to gloss over. If you miss this, the model will bug out with fake tool calls against a schema that doesn't exist.

The agent loop itself runs up to 8 turns maximum. Each turn, SID returns tool calls, we execute them against OpenSearch, feed the XML results back, and the model decides whether to keep searching or finalize with `report_helpful_ids`. As I showed earlier, it typically wraps up in 2-3 turns.

### Batching queries with \_msearch

SID tends to fire off 3-4 search queries per turn. Running those as individual OpenSearch requests would add unnecessary round-trips, so I batch all `search` and `text_search` calls within a turn into a single `_msearch` request. The `_msearch` API takes alternating header/body pairs and returns responses in order, so mapping results back to their originating tool calls is just index bookkeeping. Any `read` calls (typically 0-1 per turn) run in parallel alongside the batch via `Promise.all`.

Over 3 turns, this is the difference between ~12 requests to your cluster and ~3.

### Execution transparency

This is an example training application meant to show what's going on behind the scenes, and I didn't want the user staring at a spinner for 3 seconds with no idea what's happening. So while the App and SID are looping turns, events fire to update the UI on progress. It's fast and you might miss it, so at the end we show the full execution workflow in the sidebar. Every turn gets token and latency reports and every query gets hits and the search result IDs.

Results render in the right column as ranked book cards, with a header reporting something like "5 results ranked by relevance in 2.4 seconds" measured client-side from query submission to the results event.

The sidebar takes the place of facets, and is a tradeoff for the demonstration. But in my opinion, I still believe facets and filters have a place in an agentic search experience - this is one of my major qualms with RAG and chat search in general. Sometimes agents get things wrong, and I want to filter to help scope what I'm looking for!

The whole thing sits alongside the existing [10-blue-links search](https://bonsai.io/blog/managed-search-on-render-with-bonsai/) without touching any of the original code. Set a `SID_API_KEY` environment variable alongside your [`BONSAI_URL`](https://app.bonsai.io/signup?utm_source=bonsai_blog&utm_campaign=agent-search-with-sid) and the agent search is ready to go.

## Try it yourself

Working with SID-1 has been lots of fun. When you've been in the search space for as long as I have (15 years now!), its incredible seeing the tools you dreamed of a decade ago come to fruition before your very eyes. The past 4 years have been a rollercoaster, and for a while people didn't really know the best way to apply LLMs to search. SID represents a solid first step for a drop-in relevance improvement model.

Here's a link to the [full demo](https://bonsai-training-example-7zmt.onrender.com/books/agent) running SID-1 with a Bonsai OpenSearch cluster. The full source is in the [bonsai-training-example repo](https://github.com/omc/bonsai-training-example). Clone it, add your credentials, load the Gutenberg dataset, and you have an agent-powered search running against your own cluster.

If you're starting fresh, the [Render deployment guide](https://bonsai.io/blog/managed-search-on-render-with-bonsai/) walks through setting up the base application, indexing the data, and deploying. This agentic search feature builds directly on top of that.

If you want to talk through how agentic search could work for your use case, reach out at [support@bonsai.io](mailto:support@bonsai.io). See you next time!