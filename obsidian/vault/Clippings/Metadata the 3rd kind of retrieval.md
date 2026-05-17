---
title: "Metadata: the 3rd kind of retrieval"
source: "https://softwaredoug.com/blog/2026/04/21/metadata-the-3rd-kind-of-retrieval"
author:
  - "[[Doug Turnbull]]"
published:
created: 2026-05-16
description: "In search we talk about lexical embedding retrieval But we miss another retrieval philosophy metadata And with LLMs its never..."
tags:
  - "clippings"
---
In search, we talk about lexical + embedding retrieval. But we miss another retrieval philosophy: *metadata*. And with LLMs, its never been easier to implement.

What do we mean by metadata?

A query `crimson suede couch` can be understood as specifying a relevant product. We can rewrite the query as:

| Color | Material | Category |
| --- | --- | --- |
| Red | Leather > Suede | Furniture > Living Room > Couches |

The ideal product comes as close as possible to this specification. Our task would be to decide which of these products is most similar:

| Product Name | Color | Material | Category |
| --- | --- | --- | --- |
| Red suede sofa | Red | Leather > Suede | Furniture > Living Room > Couches |
| Pink barbie recliner | Pink | Leather > Imitation | Furniture > Living Room > Recliners |
| Mr. Beast neon desk | Green | Wooden | Furniture > Office > Desks |

How would we rank these against our query?

In color, *Red* is more similar to our specification. Then we would rank *Pink* next*.* Green isn’t a match at all, so should be excluded.

In material, maybe imitation leather would be ok to show? So long as we put Suede above Imitation leather?

Each attribute has its own notion of similarity. To rank furniture colors, for example, you need to think about primary / secondary colors. A solution would need to consider patterns like stripes and plaid. Each attribute becomes a problem to solve in and of itself. (perhaps using embedding + lexical approaches).

## Not just filters - ranking accessible to anyone

What we’re really talking about is explainable ranking: ranking in a way that could evoke a conversation. Would imitation leather be an acceptable result for a search for suede? And if so how does it relate to other attributes?

Explainable ranking turns into tightly controlled ranking. Ranking where correctness could be objectively defined, measured, and tested without extensive user evals.

After all, users often describe their queries via attributes. Their complaints look like:

> I searched for earnings reports on stock XYZ. This result is not an earnings report, and its not about XYZ”.

That ones a fairly obvious filter, easy to write a test for.

What about:

> Its ok these tangential financial reports show up below earnings reports, but it absolutely must be about the XYZ company

OK that’s testable. Or perhaps:

> The top leggings are knee-length, clearly I searched for ankle-length, show ankle length, then calf, and exclude knee length altogether.

Again, testable in the “unit test” meaning of the world. If we know these attributes, we can test whether we fulfill the promise.

You don’t need to carefully analyze user data to discover these. Your internal stakeholders can tell you what’s broken through their own use. Turning ranking from an abstract problem, into one expressible in the language of the user.

In today’s LLM world, it’s never been easier classify queries + content into attributes. We can now [Cheat at Search](http://maven.com/softwaredoug/cheat-at-search) - a problem that took extensive NLP research, now can be done painlessly.

Because of how easy its become, we might be veering towards a place where we can solve a fair number of search problems with less sophistication. Even [“semantic” problems](https://softwaredoug.com/blog/2026/01/08/semantic-search-without-embeddings). Just by having a conversation with a stakeholder.

\-Doug

**PS come to today’s talk on agentic retrieval if you want to hang out:)**

[https://maven.com/p/7105dc/rag-is-the-what-agentic-search-is-the-how](https://maven.com/p/7105dc/rag-is-the-what-agentic-search-is-the-how)

*This is part of Doug’s Daily Search tips - [subscribe here](http://softwaredoug.kit.com/)*

---

### Enjoy softwaredoug in training course form!

#### Starting May 18!

Signup here - [http://maven.com/softwaredoug/cheat-at-search](http://maven.com/softwaredoug/cheat-at-search) [![](https://softwaredoug.com/assets/media/2026/cheat-at-search-social.png) ](https://maven.com/softwaredoug/cheat-at-search)I hope you join me at [Cheat at Search with Agents](https://maven.com/softwaredoug/cheat-at-search) to learn use agents in search. build better RAG and use LLMs in query understanding.

---