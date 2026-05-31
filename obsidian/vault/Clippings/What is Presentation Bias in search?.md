---
title: "What is Presentation Bias in search?"
source: "https://softwaredoug.com/blog/2022/07/16/what-is-presentation-bias-in-search"
author:
  - "[[Doug Turnbull]]"
published:
created: 2026-05-31
description: "Let's explore this key bias in search systems towards the old algorithm and how to overcome it!"
tags:
  - "clippings"
---
You’re driving down the highway and you have a sudden craving for tacos🌮! You come up to a major town (Dougville), seeing a sign advertising the dining options. On the tiny sign are six restaurants to represent the entire dining options of this bustling town:

- Three fast-food hamburger restaurants
- The local Dougville diner
- A coffee shop
- A smoothie shop

Yet you’re craving tacos. Do you:

1. Keep driving, hoping the next exit has delicious tortilla filled goodness?
2. Pull off here and pin your hopes on Dougville’s delish cuisine?

As search practitioners, we’re Dougville! Our searchers have a need - a search for tacos. We have the tiniest amount of screen real estate to show them relevant options. Yet shoppers won’t purchase what search doesn’t show them! They don’t know whether to go elsewhere or keep looking.

Let’s take it a step further. Disappointed with the number of visitors to the town’s restaurants, Dougville wants to revise the sign. They ask a couple of questions

1. What restaurants do drive-by travelers like to visit?
2. Maybe we should show those restaurants on the sign?

Lo-and-behold it turns out that the restaurants drive-by travelers like to visit are, you guessed it,

It’s almost like the sign itself is biasing the results of our test! 🤦🏻♂️

Similarly, when we study what our searchers find is relevant for a query, we see this bias towards historical results for that query. This has huge implications:

- New promising algorithms rarely do better than the old algorithm when studying historical search results (because old clicks happened on the previous ranking!).
- Our models learn to parrot old ranking algorithms - We can’t easily train machine learning or NLP models to learn learn relevant results because we’ll just learn what the current ranking algorithm (or highway sign) shows searchers!

## How do we overcome this bias?

At a high level, here’s some solutions

1. **Diversity in search results** - In our Dougville sign, so much space is occupied by three very similar hamburger results. Why not try some different options relevant to the driver needing a bite, reducing the risk that our drivers keep going? Or in search, give searchers both maximally relevant and maximally different results (the cheap option, the fancy option, etc etc). This not only expands the kind of click feedback we get, it also might show the user that our catalog has more to offer
2. **Tighten online (A/B testing) and offline (historical) feedback loops** - instead of a lengthy study with historical data (which we know is biased), then a big bang A/B test to see if it worked, let’s get an early version of our ranking solutions in front of users! This helps us gather clicks to fine-tune our solutions, retrain models again offline, then
3. **Active learning** - Active learning is an approach in machine learning to have models participate in their own learning. In other words, we can see where the gap are in our training data (such as taco restaurants for drive-by diners) then intentionally target those at our searchers. [Chapter 12 of AI Powered Search discusses one such approach.](http://aipoweredsearch.com/)
4. **Don’t just rely on click data** - There are other ways to train models! For example, we can also crowdsource manual labelers. Of course services like Mechanical Turk exist for this, but for search, there are tailored solution like [Appen](https://appen.com/) and [Supahands](https://www.supahands.ai/) that understand search and how to overcome biases inherent in manual rating

But you’ll always have to handle presentation bias in search! When there’s a targeted intent, and only a little bit of screen real estate to handle it, you can only overcome it so much. It’s a core competency of a search team - and perhaps the key problem you need to solve for your search system.

How do you overcome presentation bias? [Get in touch](http://linkedin.com/in/softwaredoug) and let me know!

---

### Enjoy softwaredoug in training course form!

#### Starting May 18!

Signup here - [http://maven.com/softwaredoug/cheat-at-search](http://maven.com/softwaredoug/cheat-at-search) [![](https://softwaredoug.com/assets/media/2026/cheat-at-search-social.png) ](https://maven.com/softwaredoug/cheat-at-search)I hope you join me at [Cheat at Search with Agents](https://maven.com/softwaredoug/cheat-at-search) to learn use agents in search. build better RAG and use LLMs in query understanding.

---