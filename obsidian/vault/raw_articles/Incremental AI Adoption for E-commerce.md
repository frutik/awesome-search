---
title: "Incremental AI Adoption for E-commerce"
source: "https://arcturus-labs.com/blog/2026/01/18/incremental-ai-adoption-for-e-commerce/"
author:
published: 2026-01-18
created: 2026-05-15
description: "Transform your e-commerce search from basic keyword matching to conversational AI—one step at a time. Learn how to incrementally adopt AI without overhauling your existing infrastructure, starting with simple query suggestions and building up to a full conversational assistant. No search experts required, just a thin AI layer that makes your current search engine smarter."
tags:
  - "clippings"
---
When you think of e-commerce, your mind is probably drawn to Amazon.com as "the definitive" example. But it's actually the exception. The internet is filled with tons of small- and medium-sized e-commerce sites. These sites typically follow the same pattern - a search page with a search box at the top, selectable filters along the left side, and results filling the remainder of the screen. And the whole goal is to quickly usher customers to the products they seek.

For most of these sites, the implementation is quite simple. Product metadata is indexed into a search engine such as Elasticsearch or Algolia. This includes fields like the title of the product, its description, its price, and other relevant features (sizes for shoes, square feet for houses, etc.) And the application is typically quite simple – the user submits a search, and the backend issues a query that *hopefully* captures the customers intent, and then captures the responses and sends them to the frontend for display in the search results.

Unfortunately "right-out-of-the-box" search results are often not that great, and fixing the problem often requires hiring a team of search experts – something that smaller shops are unable to afford. Fortunately, modern AI is coming to the rescue! In this post we'll demonstrate how e-commerce shops can incrementally adopt AI and explore improvements in search which would have been unbelievable just 5 years ago.

> [!note] Want to see it in action?
> Not in the mood for reading? Watch the video version where I walk through the entire progression with live demos:
> 
> ![](https://www.youtube.com/watch?v=zzFd0ThDymk)
> 
> Or jump straight to the live demo to try it yourself: **[CLICK HERE](https://morph-trad-search-into-ai-search.fly.dev/)**

## Dispelling the Magic of RAG and Agentic AI

In 2024 "RAG" – Retrieval-Augmented Generation – became a very popular application of AI. It was sold to us as magic – just plug in RAG and point it at a set of documents and then you would instantly have a world-class agentic search application – like... "poof"! But the problem was that RAG was a black box component, and if something went wrong, then it was nigh impossible to identify the problem and fix it.

In [another post](https://arcturus-labs.com/blog/2026/03/10/make-ai-your-search-team/) I make black-box RAG transparent. I explain how it's really a set of pipelines – one for indexing content, and another for retrieving it – For the sake of this post you just need to know that RAG isn't anything special; it's just a call to an LLM which has access to a well-described product search tool that is backed by any form of search including "old school" lexical search.

2025 was "the year of Agentic AI". This was also amazingly overblown. No one could agree even on the definition of "agentic" at first, and when all the dust settled by the end of the year, we found out that Agentic AI was really, *literally*, just a couple of for-loops. The inner for-loop wrapped the LLM call and allowed "the agent" to make multiple sequential tool calls, learn from the responses, and continue until it had the results it needed. The outer for-loop incorporated the user input so that the agent actually acted like an AI Assistant, responding to the user's course corrections.

But the big point for this post is that nothing is magical. A request to Gen AI is just an HTML request – text in, text out. Build an agent by wrapping that with a couple of for-loops. And make the agent a RAG agent by giving it your current search endpoint as a tool. Easy-peasy!

## Morphing Traditional Search into Modern AI Search

Now let's see what this looks like from your customer's perspective. I'll walk through four levels of AI adoption, each building on the previous.

### Level 0: Traditional Search (Your Current Reality)

Most e-commerce sites today look like this: a keyword search box at the top, a sidebar full of filters, and the remaining space for the search results. The burden is entirely on the user to understand the typical terminology used in the documents, learn what filters exist and how they work, and sort the results correctly.

The reality? Most users type a query, scan the first page, and leave if nothing looks right. Users don't explore filters and often type text in the search box which really should be a selected filter. Unless you've hired that top-notch machine learning team, queries like these aren't parlayed into the relevant results.

### Level 1: Beginner AI (Test the Waters)

A baby step: keep traditional search unchanged, but add only a small suggestion bar that appears after results load. The AI interprets the user's natural language query and suggests a search that takes better advantage of filters and sorting. Users can click to apply these suggestions or ignore them completely.

Implementing this is easy – define a search tool with well-specified arguments associated with the keyword search text, facet selections, and sorting. Then, whenever a user issues a search, you asynchronously send the request to this simple "agent" and instruct it to make the best search it can based upon the users' input.

This baby step is effectively risk-free – the search app works no differently from what users are used to. There is no extra latency incurred because the AI request is asynchronous.

### Level 2: Intermediate AI (Let AI Take the Wheel)

The easy and obvious next step is to let the AI actually execute the recommended search rather than waiting for approval. You're now incurring some real UX risk, because the snappy 10ms response is being replaced by a 2-3 second response. But if the AI can come up with a good query in two seconds when it would take a user 5 seconds, you're actually saving the user effort.

At this level, a new box above the results contains a summary of the results and some recommended next queries. The summary gives the user a holistic understanding of the search results, and the recommended next queries keep the user engaged.

### Level 3: Advanced AI (Full Conversational Assistant)

With the advanced AI experience, we morph the traditional search experience into a guided, conversational experience. We ditch the search box, and replace it with a chat window.

When users start interacting conversationally with your e-commerce app, you'll witness a Cambrian explosion of new user behaviors. Since the conversation is stateful, the user works *with* the assistant to clarify their intent, and the resulting queries are much better targeted, leading to much higher conversion rates.

## Easier Than You Think

The entire demo – including the whole, fake traditional search and fake inventory – took 10 hours to build. If you are interested in incrementally adopting AI, nothing much has to change. Your existing search infrastructure (Elasticsearch, etc.) stays in place. All you have to do is write a thin, completely decoupled endpoint that looks at the user request, and attempts to map that into a proper search request, and you incorporate that into the UI. If that works out to your expectations, then just make the integration thicker, bit-by-bit.

The future of e-commerce search is conversational, and getting there is simpler than ever.