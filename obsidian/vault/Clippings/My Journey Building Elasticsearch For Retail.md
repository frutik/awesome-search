---
title: "My Journey Building Elasticsearch For Retail"
source: "https://www.searchhub.io/en/my-journey-building-elasticsearch-for-retail/"
author:
  - "[[Rudolf Batt]]"
published: 2021-02-11
created: 2026-05-16
description: "If, like me, you’ve taken the journey that is building an Elasticsearch retail project, you’ve inevitably experienced many challenges. Challenges like, how do"
tags:
  - "clippings"
---
**If, like me, you’ve taken the journey that is building an Elasticsearch retail project, you’ve inevitably experienced many challenges. Challenges like, how do I index data, use the query API to build facets, page through the results, sorting, and so on? One aspect of optimization that frequently receives too little attention is the correct configuration of search analyzers. Search analyzers define the architecture for a search query. Admittedly, it isn’t straightforward!**

The Elasticsearch documentation provides good examples for every kind of query. It explains which query is best for a given scenario. For example, “Phrase Match” queries find matches where the search terms are similar. Or “Multi Match” with “most field” type are “useful when querying multiple fields that contain the same text analyzed in different ways”.

All sounds good to me. But how do I know which one to use, based on the search input?

## Where to Begin? Search query examples for Retail.

Let’s pretend we have a data feed for an electronics store. I will demonstrate a few different kinds of search inputs. Afterward, I will briefly describe how search should work in each case.

### Case #1: Product name.

For example: “ **MacBook Air** ”

Here we want to have a query that matches both terms in the same field, most likely the title field.

### Case #2: A brand name and a product type

For example: **“Samsung Smartphone”**

In this case, we want each term to match a different field: brand and product type. Additionally, you want to find both terms as a pair. Modifying the query in this way prevents other smartphones or Samsung products from appearing in your result.

### Case #3: The specific query that includes attributes or other details

For example: **“notebook 16 GB memory”**

This one is tricky because you want “notebook” to match the product type, or maybe your category is named such. On the other hand, you want “16 GB” to match the memory attribute field as a unit. The number “16” shouldn’t match some model number or other attribute.

For example: “MacBook Pro **16** inch“ is also in the “ **notebook** ” category and has some “ **GB** ” of “ **memory** “. To further complicate matters, search texts might not contain the term “memory”, because it’s the attribute name.

As you might guess, there are many more. And we haven’t even considered word composition, synonyms, or typos yet. So how do we build one query that handles all cases?

### Preparation

Before striving for a solution, take two steps back and prepare yourself.

#### Analyze your data

First, take a closer look at the data in question.

- How do people search on your site?
- What are the most common query types?
- Which data fields hold the required content?
- Which data fields are most relevant?

Of course, it’s best if you already have a site search running and can, at least, collect query data there. If you don’t have a site search analytics, even access-logs will do the trick. Moreover, be sure to measure which queries work well and which do not provide proper results. More specifically, I recommend taking a closer look at how to implement [tracking](https://blog.searchhub.io/search-event-data-collection-progress-so-far), the [analysis](https://blog.searchhub.io/how-to-diy-site-search-analytics-made-easy), and [evaluation](https://blog.searchhub.io/three-pillars-of-search-quality-in-ecommerce-part-1-findability).

You are welcome to [contact us](https://www.searchhub.io/contact) if you need help with this step. We enjoy learning new things ourselves. Adding searchHub to your mix gives you a tool that combines different variations of the same queries (compound & spelling errors, word order variations, etc.). This way, you get a much better view of popular queries.

#### Track your progress

You’ll achieve good results for the respective queries once you begin tuning them. But don’t get complacent about the ones you’ve already solved! More recent optimizations can break the ones you previously solved.

The solution might simply be to document all those queries. Write down the examples you used, what was wrong with the result before, and how you solved it. Then, perform regression tests on the old cases, following each optimization step.

Take a look at [Quepid](https://quepid.com/) if you’re interested in a tool that can help you with that. Quepid helps keep track of optimized queries and checks the quality after each optimization step. This way, you immediately see if you’re about to break something.

### The Silver-Bullet Query

Now, let’s get it done! Let me show you the perfect query that solves all your problems…

Ok, I admit it, [there is none](https://dzone.com/articles/learning-to-rank-in-elasticsearch-machine-learning). Why? Because it heavily depends on the data and all the ways people search.

Instead, I want to share my experience with these types of projects and, in so doing, present our approach to search with Open Commerce Search Stack (OCSS):

#### Similarity Setting

When dealing with structured data, the [scoring algorithms of Elasticsearch “TF/IDF” and BM25](https://www.elastic.co/guide/en/elasticsearch/reference/7.10/similarity.html) will most likely screw things up. These approaches work well for full-text search, like Wikipedia articles or other kinds of content. And, in the unfortunate case where your product data is smashed into one or [two fields](https://documentation.spryker.com/docs/full-text-search#indexing-text), you might also find them helpful. However, with OCSS (Open Commerce Search Stack), we took a different approach and set the [similarity to “boolean”](https://github.com/CommerceExperts/open-commerce-search/blob/master/indexer-service/src/main/resources/elasticsearch/_template/structured_search.json#L9). This change makes it much easier to comprehend the scores of retrieved results.

#### Multiple Analyzers

Let Elasticsearch analyze your data using different types of analyzers. Do as little normalization as possible and as much as necessary for your base search-fields. Use an analyzer that doesn’t remove information. What I mean with this is no stemming, stop-words, or anything like that. **Instead, create sub-fields with different analyzer approaches**. These “base fields” should always have a greater weight during search time than their analyzed counterparts.

The following shows how we configure search data mappings within OCSS:

```javascript
{
  "search_data": {
    "path_match": "*searchData.*",
    "mapping": {
      "norms": false,
      "fielddata": true,
      "type": "text",
      "copy_to": "searchable_numeric_patterns",
      "analyzer": "minimal",
      "fields": {
        "standard": {
          "norms": false,
          "analyzer": "standard",
          "type": "text"
        },
        "shingles": {
          "norms": false,
          "analyzer": "shingles",
          "type": "text"
        },
        "ngram": {
          "norms": false,
          "analyzer": "ngram",
          "type": "text"
        }
      }
    }
  }
}
```

##### Analyzers used above explained

Let’s break down the different types of analyzers used above.

- The base field uses a customized “minimal” analyzer that removes HTML tags, non-word characters, transforms the text to lowercase, and splits it by whitespaces.
- With the subfield “standard”, we use the “standard analyzer” responsible for stemming, stop words, and the like.
- With the subfield “shingles”, we deal with unwanted composition within search queries. For example, someone searches for “jackwolfskin”, but it’s actually “jack wolfskin”.
- With the subfield “ngram,” we split the search data into small chunks. We use that if our best-case query doesn’t find anything – more about that in the next section, “Query Relaxation”.
- Additionally we copy the content to the “searchable\_numeric\_patterns” field which uses an analyzer that removes everything but numeric attributes, like “16 inch”.

#### The most powerful Elasticsearch Query

Use the “ [query string query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html) ” to build your final Elasticsearch query. This query type gives you all the features from all other query types. In this way, you can optimize your single query without the need to change to another query type. However, it would be best to strip “syntax tokens”; otherwise, you might get an invalid search query.

Alternatively, use the “ [simple query string query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-simple-query-string-query.html),” which can also handle most cases if you’re uncomfortable with the above method.

My recommendation is to use the “ [cross\_fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html#type-cross-fields) ” type. It’s not suitable for all kinds of data and queries, but it returns good results in most cases. Place the search text into quotes and use a different quote\_analyzer to prevent the search input from being analyzed with the same analyzer. Also, if the quoted-string receives a higher weight, a result with a matching phrase is boosted. This is how the query-string could look: “search input “^2 OR search input.

**And remember, since there is no “one query to rule them all,” use query relaxation.**

### How do I use Query Relaxation?

![](https://www.searchhub.io/wp-content/uploads/2022/12/snowy_path_new.jpeg)

After optimizing a few dozen queries, you realize you have to make some compromises. It’s almost impossible to find a single query that works for all searches.

For this reason, most implementations I’ve seen opt for the “OR” operator, thus allowing a single term to match when multiple terms are in the search input. The issue here is that you still end up with results that only partially match. It’s possible to combine the “OR” operator with a “minimum\_should\_match” definition to boost more matches to the top and control the behavior.

Nevertheless, this may have some unintended consequences. First, it could pollute your facets with irrelevant attributes. For example, the price slider might show a low price range just because the result contains unrelated cheap products. It may also have the unwanted effect of making ranking the results according to business rules more difficult. Irrelevant matches might rank toward the top simply because of their strong scoring values.

So instead of the silver-bullet query – build several queries!

#### Relax queries, divide the responsibility, use several

**The first query** is the most accurate and works for most queries while avoiding unnecessary matches. Run a **second query** that is more sloppy and allows partial matches if the initial one leads to zero results. This more flexible approach should work for the majority of the remaining queries. Try using a **third query** for the rest. Within OCSS, at the final stage, we use the “ngram” query. Doing so allows for partial word matches.

“But sending three queries to Elasticsearch will need so much time,” you might think. Well, yes, it has some overhead. At the same time, it will only be necessary for about 20% of your searches. Also, zero-matches are relatively fast in their response. They are calculated pretty quickly on 0 results, even if you request aggregations.

Sometimes, it’s even possible to decide in advance which query works best. In such cases, you can quickly pick the correct query. For example, identifying a numeric search is easy. As a result, it’s simple only to search numeric fields. Also, as there is no need to analyze a second query, it’s easier to handle single-term searches uniquely. Try to improve this process even further by using an external spell-checker like [SmartQuery](https://docs.searchhub.io/module_smartquery.html) and a query-caching layer.

## Conclusion

I hope you’re able to learn from my many years of experience; from my mistakes. Frankly, praying your life away (e.g., googling till the wee hours of the morning), hoping, and waiting for a silver-bullet query, is entirely useless and a waste of time. Learning to combine different query analysis types and being able to accept realistic compromises will bring you closer, faster to your desired outcome: search results that convert more visitors, more of the time than what you previously had.

We’ve shown you several types of analyzers and queries that will bring you a few steps closer to this goal today. Strap in and tune in next week to find out more about OCSS if you are interested in a more automated version of the above.