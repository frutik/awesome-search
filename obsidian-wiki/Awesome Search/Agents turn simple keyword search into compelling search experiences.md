---
title: "Agents turn simple keyword search into compelling search experiences"
source: "https://softwaredoug.com/blog/2025/09/22/reasoning-agents-need-bad-search"
author:
  - "[[Doug Turnbull]]"
published:
created: 2026-05-15
description: "Agents need tools they understand, like simple keyword search. They can reason about these tools, evaluate the results, refine, and iterate to deliver rather interesting results. But maybe with some caveats."
tags:
  - "clippings"
---
A traditional RAG system often looks like the search we’ve built for years. An LLM calls a search API. We have query understanding and reranking functionality under the hood. All optimized for user engagement.

This thick-daddy search API does quite a bit, as shown below:

![image.png](https://softwaredoug.com/assets/media/reasoning-agents-need-bad-search/image.png)

With small modifications (chunking, a focus on vector retrieval) the RAG implementations look familiar.

Agents, however, come with the ability to reason. And like human users, they might try a query, see the results, adjust their query, and zero-in on the best search terms to find what they want.

Like human users, the agent can build a “mental model” of how the search tool works. If there’s a clear, predictable correspondence between stimulus and output, the agent will figure it out. However, a large, complex system might not be as transparent.

Because of this, **I’d argue the traditional, thick search APIs are counterproductive to being used by agents.** They may be too complex for agents to reason about effectively.

So lately, I’ve tried a rather stupid search backend. More like this image:

In the furniture search examples I use in my [Cheat at Search course](http://maven.com/softwaredoug/cheat-at-search), I tried this out.

Instead of a big, complex search system, I tell the agent about this dumb thing it can use to search. It then applies its own intelligence to use the tool correctly.

```python
def search_products(query: str, top_k: int = 5) -> List[Dict]:
    """
    Search for furniture products.

    This is direct keyword search, no synonyms, only BM25 scoring on product name 
    and description and basic snowball tokenization of query and document.

    Args:
        query: The search query string.
        top_k: The number of top results to return.

    Returns:
        A list of dictionaries containing product information.
    """
   ...
```

*( the doc string here becomes part of the prompt, see the [source code](https://github.com/softwaredoug/cheat-at-search/blob/main/cheat_at_search/agent/chat.py))*

I slimmed the search down to fairly simple keyword search, and told GPT-5 exactly how it works. It behaves predictably, if stupidly.

And that’s a good thing.

I’m fairly surprised how well it works at solving user queries. Albeit slowly.

Here I am finding couches that would be good for a vampire.

```python
User: A couch fit for a vampire

...

Assistant: Here are some dramatically tufted, velvet/chesterfield options with a suitably vampiric vibe:

Chesterfield-style sofas (timeless, tufted, dramatic arms/back)
- Porter 80" Velvet Rolled Arm Chesterfield Sofa (ID 4306)
- Rolled Arm Chesterfield Sofa (ID 28854)
- Quitaque 88" Rolled Arm Chesterfield Sofa (ID 17093)

Velvet sofas with luxe flair
- 85" Velvet Tuxedo Arm Sofa (ID 29613) — velvet with nailhead trim
- Camren 72" Velvet Round Arm Sofa (ID 40049)
- 112" Wide Velvet Sofa & Chaise (ID 27546)

Chaise lounges (fainting-couch energy)
- Rosemead Velvet Chaise Lounge (ID 40626)
- Avondale Velvet Chaise Lounge (ID 6452)
- Brighouse Chaise Lounge (ID 6392)
- Tilstone Chaise Lounge (ID 18643) — velvet with silver nailhead accents
```

Or asking for the ugliest chair

```python
User: ugliest chair in the catalog

Assistant: I ran several targeted searches to surface the most over-the-top
chairs. Here are the top contenders for “ugliest chair” in our catalog:

- Zebra Arm Chair (ID 18587) — bold zebra upholstery, statement piece energy
- Toby Cow Print Task Chair (ID 5002) — desk chair in full cow print
- Gaudy 47" Wide Chenille Armchair (ID 8921) — it literally says “Gaudy” in the name
- The Abbey Gothic Revival 19" Wide Side Chair (ID 36608) — ornate, carved gothic look
```

## Helping the agent remember as it goes

The agent can track how well a tool call works as it goes. In my code, the agent stores its evaluation of each tool’s results. Essentially “LLM-as-a-judge as you go”. The next time a search happens, the agent can recall what it liked / didn’t like last time.

```
system_prompt = """
    You take user search queries and use a search tool to find furniture products.
    
    Look at the search tools you have, their limitations, how they work, etc when forming your plan.

    Before searching you MUST use the "get_past_queries" to get similar, past queries
    the user has made

    Remember every tool usage you make. After searching with a tool, evaluate the results,
    then save the interaction (immediately after tool usage) with the "save_queries_used" tool
"""
```

Below are search tool queries my code saved after I searched for the `ugliest chair in the catalog`

You see the user’s query, along with the query used at the tool (ie `cow print chair` ):

```python
Saved interaction: user_query='ugliest chair in the catalog' 
search_tool_name='mcp_search-server.search_products' 
search_tool_query='cow print chair'
quality='good'
reasoning="Returned an adult 'cow print task chair' that clearly fits a loud/novelty aesthetic; strong candidate for 'ugliest chair' request."

Saved interaction: user_query='ugliest chair in the catalog'
search_tool_name='mcp_search-server.search_products' 
search_tool_query='patchwork accent chair'
quality='meh'
reasoning="Found a kids patchwork chair; adult options not surfaced. Only tangentially relevant to 'ugliest chair' intent."

Saved interaction: user_query='ugliest chair in the catalog' 
search_tool_name='mcp_search-server.search_products'
search_tool_query='skull chair'
quality='bad'
reasoning='No chair products matched; results were decor and textiles unrelated to chairs.'
```

I’ll be able to recall what worked well for this query. I could even remember these expansions later if I build a normal site search without LLMs.

Semantic caching gives us another bonus. Later, when I search for a similar query, say `ugly chair`, I can take `ugly chair` and find past queries most similar to this query, like below.

The agent can see what’s worked well / hasn’t worked well for friends of `ugly chair`:

```python
Getting past queries for: ugly chair

Matched query: 
  ugliest chair in the catalog, 
  similarity: 0.8236806392669678, 
  interaction: user_query='ugliest chair in the catalog' 
  search_tool_name='mcp_search-server.search_products'
  search_tool_query='novelty chair'
  quality='meh' reasoning="Found novelty chairs but primarily for kids; may not match adult seating requestfor 'ugliest chair'."
Matched query: ugliest chair in the catalog, 
  similarity: 0.8236806392669678, interaction: user_query='ugliest chair in the catalog' search_tool_name='mcp_search-server.search_products' search_tool_query='weird chair'
  quality='bad'
  reasoning="Keyword 'weird' mostly matched non-chair textiles and generic chair listings; not  helpful for surfacing intentionally odd or gaudy chairs."
Matched query: ugliest chair in the catalog, 
  similarity: 0.8236806392669678,
  interaction: user_query='ugliest chair in the catalog'
  search_tool_name='mcp_search-server.search_products'
  search_tool_query='zebra accent chair'
  quality='good'
  reasoning="Surfaced a 'zebra arm chair' (animal print) that fits an intentionally loud/gaudy aesthetic often perceived as ugly; results include a clear adult armchair option."
```

As the agent searches, it’s little vector lookup of user queries turns into a knowledge graph. User queries connected to other user queries via similarity. And each with notes on what’s worked / not worked when calling the search tool.

It’s the ultimate learning machine.

At least as far as its own preferences.

## Only as good as the agent’s ability to evaluate results

The LLM must be able to evaluate the results that come back. It needs to be a reasonable LLM judge. That means:

- Did we return useful metadata for the agent to use in its evaluation? (Here we use product / description). But should we return images? Any other metadata?
- Does the LLM actually have domain expertise to evaluate the results? (Note above it returns a brand “Gaudy”, which is not the adjective “gaudy” — as in ugly)

Finally the big one:

### What about the user’s input?

The agent’s judgment is bound to be flawed / limited. Even in an ideal setting, it will *always* be disjoint from what users want. Lack of user clickstream feedback is a [huge gap in RAG](https://softwaredoug.com/blog/2025/05/16/rags-big-blindspot) that continues here.

We can’t expect LLMs to have any idea of the crazy, insane things, humans do when nobody is watching. I’ve seen users do all sorts of things:

- Users often click black / boring colors, not loud ones
- Users click on spicy topics or images that have nothing to do with their query
- Users get what they need from the search page, and never click anything
- Users click because of the relationship between an image and its neighbor
- Click data itself is sparse and noisy, and may require a lot in aggregate to make sense of

There are dozens of biases cataloged in user clickstream interactions with search results.

The search field has spent decades interpreting clickstream data, and the RAG world continues to lack good answers to getting that data back into the agent.

Maybe you’ve seen good research here? Please share!

## Are reasoners actually actively harmful rankers?

Reasoning involves taking a base set of facts and deriving a solution. This, however, is different from directly optimizing for what users want (as expressed through clickstream data). We don’t have the technology for an LLM or agent to churn over millions of user sessions to become a better judge of search result quality.

Even if we gave the agent an oracle - labeled each result with user engagement data, could it make sense of latent patterns? Or would it simply be confused at the strange inconsistent behavior of humans that don’t act like math proofs or programming conpetitions?

Any ranking model optimized to engagement would more likely be implemented outside the agent: In a classic, thick search stack. The agent’s inner LLM judge, might look at model-ranked results and assume they’re bad. Why would users want such bland products? Why would the search have interpreted “Gaudy” to be a brand name, when its obviously “ugly”?

In short, users’ chaotic, implicit search expectations — as expressed in their clickstream — go against the agent’s orderly, explicit reasoning + judgment. An agent may issue a search and think “oh this result set was meh” when in reality, its the most engaging search results for that query.

Reasoning about search tool output might be very dangerous if the agent discards actually relevant results.

So take this article with this big grain of salt and be careful.

But still, it’s pretty fun.

---

### Enjoy softwaredoug in training course form!

#### Starting May 18!

Signup here - [http://maven.com/softwaredoug/cheat-at-search](http://maven.com/softwaredoug/cheat-at-search) [![](https://softwaredoug.com/assets/media/2026/cheat-at-search-social.png) ](https://maven.com/softwaredoug/cheat-at-search)I hope you join me at [Cheat at Search with Agents](https://maven.com/softwaredoug/cheat-at-search) to learn use agents in search. build better RAG and use LLMs in query understanding.

---


## Related Concepts

- [[Agentic Search]]
- [[BM25]]
- [[LLM as Judge]]
- [[Semantic Search]]
- [[Search Evaluation]]

## People

- [[Doug Turnbull]]
