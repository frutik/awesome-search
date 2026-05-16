---
title: "Finding the relevance cutoff: when to stop showing search results"
source: "https://softwaredoug.com/blog/2021/05/05/finding-the-cutoff-when-search-results-stop-being-relevant.html"
author:
  - "[[Doug Turnbull]]"
published:
created: 2026-05-16
description: "In this article: we assume users review every search result. So we need to find that sweet spot when we get to look reaaalllly fricken smart and declare, with confidence,"
tags:
  - "clippings"
---
Usually in search, you don’t care if there’s millions of results or ten. If the top ranked results are relevant, you can safely ignore the rest. As is commonly joked in the search world, “where’s the best place to hide an elephant? On the 2nd page of Google!”

However, with progressive scrolling, users seamlessly scan many results at once. Sometimes you need to look holistically at the returned set and *stop* showing users results past a certain point. In this article: we assume users review *every* search result. So we need to find that sweet spot when we get to look *reaaalllly fricken smart* and declare, with confidence, *“we have nothing else that matches your query”*.

This article is about **establishing an evaluation methodology** to find that cutoff sweet spot. We need to solve the problem below - eliminating the irrelevant cruft from the end of first result set, and instead trimming down to the one on the right:

![The goal: find the cutoff where results stop being relevant](https://softwaredoug.com/assets/media/cutoff_tail_of_results.png)

With the right measurement structure in place we can try any number of approaches like simple tweaks to [minimum\_should\_match](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-minimum-should-match.html) or something more complex.

## Needed: a relevance metric to stop doomscrollers

*(“But doesn’t DCG do that?”)*

Classic relevance metrics typically zero in on the top N search results. By design, they don’t consider the full result set’s quality. In fact, metrics like [Discounted Cumulative Gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) (DCG) make the *opposite* assumption that we do! DCG [and friends](https://shopify.engineering/evaluating-search-algorithms) assume users primarily examine the top results and ignore the rest. If we return many bad results towards the bottom (such as the example on the left above) then that’s no big deal.

What we need, however, is a metric that captures user satisfaction scanning *all the results declared relevant by the search engine*. We note in many contexts in today’s search UXs, scanning many results is *cheap*, like in [Instagram’s search](https://www.instagram.com/explore/search/keyword/?q=hamster) or [Twitter’s](https://twitter.com/search?q=hamster&src=typed_query&f=live). For many search and discovery use cases, the user is casually browsing a topic. It’s not crucial that they take an explicit action. You want your app to be a fun place to “window shop” so users come back (maybe to purchase when they know exactly what they want!). This is quite different than when users know exactly what they want, and your search engine’s job is to give it to them quickly.

In other words, we need a metric that captures the sweet spot between relevance and result set size, like our user below desperately trying to watch *all the adorable hamster olympics videos*!!:

![](https://softwaredoug.com/assets/media/cutoff_loses_relevant_result.png)

## Option 1: Variable Precision - proportion of relevant results

One attempt is a pretty simple metric we call *variable precision* at Shopify.

Basically the algorithm is a simple sum of the relevance grades (whether something is relevant or not) divided by the total result set size. Here’s the Python code:

```
def variable_precision(graded_results):
    return sum(graded_results[:n]) / n if n != 0 else 0.0
```

Notice `variable_precision` is different from classic precision examining a top N. We look at the precision - the proportion of relevant search results - of the full returned set, not just top 10 or 50 results.

Comparing our three relevance solutions for query `hamster olympics` above, we can see the score of our algorithms, starting with algorithm A (too many results), to algorithm B (we lose a relevant result), to C (the most hamster olympics goodness!)

```
# Relevance Algo A's results for \`hamster olympics\`
>> variable_precision([1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0])
0.42857142857142855

# Algo B for \`hamster olympics\`
>> variable_precision([1.0, 0.0, 1.0])
0.6666666666666666

# Algo C - Just right!
>> variable_precision([1.0, 0.0, 1.0, 1.0])
0.75
```

(As I assume this user is scrolling over `hamster olympics` videos, I randomly give you this video, aprospros of nothing.)

![](https://www.youtube.com/watch?v=7CW9udETj2k)

ANYWAY

### The fatal flaw!

Variable precision, unfortunately, has a fatal flaw. Consider this simple case of where `variable_precision` perhaps isn’t giving us what we want:

```
# Algo D - But, we lost 2 relevant results!
>> variable_precision([1.0])
1.0
```

The solution returning just 1 result shouldn’t be seen as more valuable than the one that gives 3/4 relevant results (Algorithm C) for that query. The upshot: a simple proportion doesn’t work well for small numbers of N. Because - THERE ARE MORE HAMSTER VIDEOS AND I WANT THEM ALL.

Now it turns out, for the most part its still a pretty decent metric, because it can be hard to shrink search results down to just one or few results with most techniques available to us. So fret not hamster enthusiasts. Nevertheless, if we want to automate an optimization over this metric, then we probably would like to choose something different.

## Option 2: F1-score

You might not like *variable\_precision* if you are, indeed, in the mood for *all the hamster videos*. To get all the hamster videos, but skip other annoying videos, we can rethink the problem as one of maximizing both precision and recall over the full result set.

With *variable\_precision* we only measure the precision of the full result set. That is, we count the proportion of returned results that are relevant. If we’re fishing for tuna, and we look in our net and half the fish are tuna, our catch’s precision is 50% or 0.5.

*Recall*, on the other hand, measures the proportion of relevant results that made it into the result set. To abuse our fishing metaphor, and an entire species, recall would be counting whether we indeed, caught *all the tuna in the sea*. If our net had 500 tuna, and 5 million were out in the sea, we would say the recall is 500 / 5000000 = 0.0001.

This great graphic [from wikipedia](https://en.wikipedia.org/wiki/F-score#/media/File:Precisionrecall.svg) captures the concept beautifully.

![The goal: find the cutoff where results stop being relevant](https://softwaredoug.com/assets/media/precision_recall.png)

In our case, the light green above is hamster olympics videos in our result set. The darker green on the left are hamster video olympics we missed:’(. We want to push out the non hamster olympics content (the red false positives), and push more hamster olympics into our lives.

The [F1 Score](https://en.wikipedia.org/wiki/F-score) measures the sweet spot between precision and recall. In the function below, we take the search results (`grades`) as well as the `total_positives` - the total number of relevant results out there. The number of tuna in the sea, or the number of hamster olympics videos out there to watch.

```
def f1_score(grades, total_positives):
    true_positives = sum(grades)
    false_positives = len(grades) - true_positives
    false_negatives = total_positives - true_positives
   
    recall = true_positives / total_positives
    precision = true_positives / len(grades)
    return precision * recall / (precision + recall)
```

What’s important is the last line: `precision * recall / (precision + recall)`. This rewards relevance solutions that maximize BOTH precision and recall. If either is wanting, the `f1_score` will be pulled down significantly.

We’ll assume there’s 9, adorable and hilarious hamster olympics videos out there. Let’s start by looking at the “fatal flaw” use case from `variable_precision`, to see if we’ve solved that problem:

```
>> f1_score([1.0], 9)
0.09999999999999999
```

In this case, precision is 1.0 (everything in our result set is relevant). Yet recall is quite low. We’re missing 8 relevant results. Our recall is only 1/9 = 0.1111. The `f1_score` is thus `1.0 * 0.1111.. / (1.0 + 0.1111..) = 0.0999...`. This is what we want: a low score for cutting out too many relevant results from the full result set. Only when precision and recall are close to 1.0 can we get close to an f\_score of 1.0.

Let’s keep examining the other cases above:

```
# Relevance Algo A's results for \`hamster olympics\`
>> f1_score([1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0], 9)
0.1875

# Algo B for \`hamster olympics\`
>> f1_score([1.0, 0.0, 1.0], 9)
0.16666666666666666

# Algo C - best!
>> f1_score([1.0, 0.0, 1.0, 1.0], 9)
0.23076923076923078
```

Relevance Algorithm C has the highest `f1_score` as it has the highest precision (3/4) AND recall (3/9) of the available algorithms. Great! F1 overcomes the “fatal flaw” of just looking at precision with `variable_precision`.

### A flaw?

One problem with `f1_score`, it doesn’t explicitly look at the tail of the results to see if we cutoff an irrelevant result before the end. In other words these examples have the same `f1_score` s:

```
# Solution with 2 irrelevant at end
>> f1_score([1.0, 1.0, 1.0, 0.0, 0.0], 9)
0.21428571428571427
```
```
# Solution with irrelevant interspersed?
>> f1_score([1.0, 0.0, 1.0, 0.0, 1.0], 9)
0.21428571428571427
```

Is this an issue? Depends on the use case. In both cases, we’re burdened with 2 non hamster olympics results (not goood) before the result set ends.

## Option 3: Modeling wasted time…

*(Note: for this example, we assume hamster olympic videos are a good use of your time)*

The next thought might be to model the user’s satisfaction or frustration as they scroll through relevant / irrelevant results. Users collect “rewards” (the relevant results) or they collect “frustration” (the irrelevant ones), as they scroll the result set. An ideal situation is a search session where time is well spent collecting many rewards, and avoiding all the frustrating irrelevant stuff.

The “Time Well Spent” metric attempts to capture this:

```
def time_well_spent(grades, median_grade=0.5):
    received_reward = 0.0
    for grade in grades:
        received_reward += grade - median_grade

    return received_reward
```

In this metric, we accumulate `grade - median_grade`. You can see if `grade` is 1.0, the we add a reward of 0.5 (hamsters, yay!). On the other hand, scrolling over an irrelevant result receives -0.5 (squirrels, boo!). The algorithm where users experience the total overall reward wins.

This works pretty well for almost all the cases f1\_score seemed to work well for:

```
# Relevance Algo A's results for query \`hamster olympics\`
>> time_well_spent(grades=[1.0])
0.5

# Algorithm B - more \`hamster olympics\` goodness
>> time_well_spent(grades=[1.0, 0.0, 1.0, 1.0])
1.0
```

We prefer accumulating 3 relevant results about “hamster olympics” (algo B) even if there is a little sting in the middle.

And to check our previous case, do we still give a low score to a big dropoff in relevance in the full result set?

```
# Algorithm C - ugh! I stopped seeing the \`hamster olympics\` awesomeness
>> time_well_spent(grades=[1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0])
-0.5
```

In algorithm C, the user’s time is wasted more, and so our metric decreases. They must have gotten exposed to those annoying human olympics videos…

### New flaws and same issues as f1\_score…

One flaw in this metric is that if, after a significant drop off in relevance, we encounter a string of relevant results, the metric can recover just by accumulating rewards that make up for the wasted time. For example, consider this case, where the user saw plenty of ‘hamster olympics’ videos, but then got mired down in non-hamster olympics videos, before recovering.

```
>> time_well_spent(grades=[1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0])
0.0
```

It feels like, maybe, it would have been better to only show the first four results above? Improving precision, but reducing recall?

Add to this the cases that confounded `f1_score`. A tail of irrelevant results at the end, gets the same score as when they are mixed up:

```
>> time_well_spent(grades=[1.0, 1.0, 1.0, 0.0, 0.0])
0.5
```
```
>> time_well_spent(grades=[1.0, 0.0, 1.0, 0.0, 1.0])
0.5
```

It seems, arguably, that we might want user’s frustration to really add up. They shouldn’t need to go over a long string of irrelevant, frustrating results, to get to a reward.

### Compounding rewards and frustrations

Almost done, then you can go watch [more hamster olympics](https://www.youtube.com/results?search_query=hamster+olympics)

In our final attempt, we’ll compound the rewards gathered. As the user examines the full result set, they get increasingly more delighted or frustrated as they encounter adjacent relevant / irrelevant results. You can see this in the code below:

```
def time_well_spent_compounding(grades, median_grade=0.5, compounding_factor=0.1):
    received_reward = 0.0
    last_grade = 0.0
    compound = 1
    for grade in grades:
        reward = (grade - median_grade) * compound
        received_reward += reward
        if grade != last_grade:
            compound = 1
        else:
            compound += compounding_factor
        last_grade = grade

    return received_reward
```

This works well to overcome some flaws in `f1_score`:

```
# Rewards accumulate at least once
>> time_well_spent_compounding(grades=[1.0, 0.0, 1.0, 1.0, 0.0])
0.44999999999999996

# Frustration reset every other result
>> time_well_spent_compounding(grades=[1.0, 0.0, 1.0, 0.0, 1.0])
0.5

# Rewards accumulate twice, frustration accumulates once (last two)
>> time_well_spent_compounding(grades=[1.0, 1.0, 1.0, 0.0, 0.0])
0.44999999999999996
```

And finally, the issue with a long string of irrelevant that recovers:

```
>> time_well_spent_compounding(grades=[1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0])
-0.10000000000000009
```

In this metric, it’s hard for the user to recover their patience with your app. They had to go over a string of irrelevant junk before getting to the good stuff.

## Closing thoughts - all metrics have their flaws

Exploring this data has pointed out how crucial it is to explore the pros/cons to any possible metric. Yet chasing the perfect metric will only increase the complexity of your implementation, and likely hide many non-obvious edge cases. Compounding rewards / frustrations, like out final example, is arguably harder to understand and reason about than less complex `f1_score` or other approaches.

To me, there’s no replacement for combining qualitative + quantitative understanding of search quality. Targeted, simple metrics, with well known flaws, beat complex metrics that try to “capture everything”.

Our qualitative “instincts” trying different search use cases point us to better quantitative approaches… including exposing the limits of those metrics. We can use data to inform our decisions, but we need to also be *data skeptics*: balancing what the numbers are telling us with common sense and qualitative feedback of what “good” looks like.

## Feedback VERY welcome - (and come work with me!!)

Love to hear feedback on this article! In particular any research or other approaches to this problem you know of. Or new flaws you’ve found here. The best place to contact me is at [LinkedIn](https://www.linkedin.com/in/softwaredoug) - (I know I’m like some kinda grownup now!). And, have I mentioned, my amazing team at Shopify is hiring? [Contact me](https://www.linkedin.com/in/softwaredoug), and I’d love to get an opportunity to work with you!

---

### Enjoy softwaredoug in training course form!

#### Starting May 18!

Signup here - [http://maven.com/softwaredoug/cheat-at-search](http://maven.com/softwaredoug/cheat-at-search) [![](https://softwaredoug.com/assets/media/2026/cheat-at-search-social.png) ](https://maven.com/softwaredoug/cheat-at-search)I hope you join me at [Cheat at Search with Agents](https://maven.com/softwaredoug/cheat-at-search) to learn use agents in search. build better RAG and use LLMs in query understanding.

---