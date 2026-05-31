---
title: "Classic ML to cope with Dumb LLM Judges"
source: "https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree"
author:
  - "[[Doug Turnbull]]"
published:
created: 2026-05-31
description: "Taking the output of many dumb LLM search relevance judges and feeding the output to a decision tree to improve precision"
tags:
  - "clippings"
---
In [previous](https://softwaredoug.com/blog/2025/01/13/llm-for-judgment-lists) [posts](https://softwaredoug.com/blog/2025/01/19/llm-as-judge-both-ways) I use a local LLM to choose which two products were more relevant for a search query (see [this github repo](https://github.com/softwaredoug/local-llm-judge/tree/main)) to guide search relevance improvements. Using human labels in an open e-commerce search dataset as a baseline ([WANDS from Wayfair](https://github.com/wayfair/WANDS/)), I measure the LLM’s preference for a product, seeing if it matches human search relevance raters. If I can do this, then I can use my laptop as the search relevance evaluator / judge. This can then guide search quality tuning and iterations, without an expensive OpenAI bill.

My goal, not so much to replace other labels but to at least be a reliable to flag what looks amiss / promising much faster without needing to always recruit humans.

In this post I’ll talk through how I combine many dumb LLM decisions on single product attributes into a smart decision. And compare it to an agent with all the product metadata.

As an example, from the dumb decisions, my plucky laptop search relevance judges looked at prompts such as:

```
Which of these product names (if either) is more relevant to the furniture e-commerce search query:

Query: entrance table

Product LHS name: aleah coffee table
    (remaining product attributes omited)
Or
Product RHS name:  marta coffee table
    (remaining product attributes omited)
Or
Neither / Need more product attributes

Only respond 'LHS' or 'RHS' if you are confident in your decision

RESPONSE:
Neither
```

Collecting 1000 agent preferences, I compare them to human preferences. Then I see if the agent is any good at predicting relevance. Then I can gain confidence, unleashing it on a pair of products for a query, and trust the results accordingly. (all assuming human evaluators are any good at this!)

In my posts, I look at a bunch of different variants on the above prompt:

- Forcing a decision to LHS / RHS OR allowing “Neither”/ “I don’t know” (see [first post](https://softwaredoug.com/blog/2025/01/13/llm-for-judgment-lists))
- One pass “dont double check”, OR Checking both sides, marking “Neither” if repeating the prompt swapping LHS with RHS disagreed (see [second post](https://softwaredoug.com/blog/2025/01/19/llm-as-judge-both-ways))

I crafted prompts for 4 product attributes:

- Product name (as above)
- Product taxonomic categorization (ie Which is more relevant? `Outdoor Furniture > chairs > ... > adirondack chairs` vs \`\`Outdoor Furniture > accesorries > …\`
- Product classification (ie `outdoor furniture` vs `living room chairs`)
- Product description (see below)

As examples of these variants, here’s description prompt same two products above:

```
Which of these product descriptions (if either) is more relevant to the furniture e-commerce search query:

Query: entrance table

Product LHS description: This coffee table is great for your entrance, use it to put in your doorway...
    (remaining product attributes omited)
Or
Product RHS description:  You'll love this table from lazy boy. It goes in your living room. And you'll find ...
    (remaining product attributes omited)
Or
Neither / Need more product attributes

Only respond 'LHS' or 'RHS' if you are confident in your decision

RESPONSE:
LHS
```

And as an example the variant where we double check, we can confirm we get the same preference swapping LHS/RHS:

```
Which of these product descriptions (if either) is more relevant to the furniture e-commerce search query:

Query: entrance table

Product LHS description:  You'll love this table from lazy boy. It goes in your living room. And you'll find ...
    (remaining product attributes omited)
Or
Product RHS description: This coffee table is great for your entrance, use it to put in your doorway...
    (remaining product attributes omited)
Or
Neither / Need more product attributes

Only respond 'LHS' or 'RHS' if you are confident in your decision

RESPONSE:
RHS
```

Now we say the first preference is consistent. We can truly say the product description “coffee table for your entrance” is the best preference for “entrance table”.

All of these permutations (fields, double checking, allowing neither) are experiments I’ve run, with results below. When the agent chickens-out (or isn’t consistent in double checking) we improve precision, but lose recall.

On the bottom right of the table for product name below, double checking AND allowing the LLM to say “Neither”, gives us preference on 11.9% of 1000 product pairs. Within that 11.9%, we correctly predict relevance preference 90.76% of the time. That’s up considerably from the upper left - getting a decision on each pair, but with precision degraded to 75.08%.

![](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzQ1aHN6NjN2b2ZldWIwZDg3Y3J4dDhtZ3d0aXNtYnVjeW16bTRiYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/DloYCssHhX1K0/giphy.gif)

All permutations of field x allowing neither x double checking all listed below

### Product Name

|  | Dont double check | Double check |
| --- | --- | --- |
| Force | 75.08% / 100% | 87.99% / 65 % |
| Allow Neither | 85.38% / 17.10% | 90.76% / 11.90% |

### Product classification

|  | Dont double check | Double check |
| --- | --- | --- |
| Force | 70.5% / 100% | 87.76% / 58.0% |
| Allow Neither | 87.01% / 17.70% | 84.47% / 10.3% |

### Categorization Hierarchy

|  | Dont double check | Double check |
| --- | --- | --- |
| Force | 74.6% / 100% | 86.1% / 69.70% |
| Allow Neither | 85.71% / 18.20% | 89.91% / 10.8% |

### Description

|  | Dont double check | Double check |
| --- | --- | --- |
| Force | 70.31% / 98.70% | 76.58% / 72.60% |
| Allow Neither | 79.21% / 10.10% | 83.02% / 5.3% |

## Putting products back together

Finally, with all we’ve learned, we can try an uber prompt with all 4 fields listed.

```
Which of these furniture products is more relevant to the furniture e-commerce search query:

Query: entrance table
Product LHS name: aleah coffee table
Product LHS description:  You'll love this table from lazy boy. It goes in your living room. And you'll find ...
 ...
Or
Product LHS name: marta coffee table
Product RHS description: This coffee table is great for your entrance, use it to put in your doorway...
 ...
Or
Neither / Need more product attributes

Only respond 'LHS' or 'RHS' if you are confident in your decision

RESPONSE:
RHS
```

When we apply all variants to the uber prompt. We get fairly useful results on upper right below (force / double check)

|  | Dont double check | Double check |
| --- | --- | --- |
| Force | 78.10% / 100.0% | 91.72% / 65.2% |
| Allow Neither | 91.89% / 11.10% | 88.90% / 2.7% |

## Improving further with decision trees

Instead of an uber prompt, another strategy might be to somehow combine the individual attribute decisions into an overall decision.

One way of capturing all the variants above, we have a set of agent predictions for each strategy:

| Query | LHS product | RHS Product | Name | Desc | Category | Class. | Human Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| entrance table | alea coffee table | marta coffee Table | Neither | LHS | LHS | RHS | LHS |

Combining these dumb agents individual decisions into a smarter overall decision seems promising…

The first thought is we should use an ensemble! The more votes of these little attribute-specific agents wins! If they mostly point to LHS, then just choose LHS, its that easy!

OR… OR… and hear me out.

Look at the data above, imagine repeating it over 1000s of query product pairs, like:

| Query | LHS product | RHS Product | Name | Desc | Category | Class. | Human Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| entrance table | alea coffee table | marta coffee Table | Neither | LHS | LHS | RHS | LHS |
| leather couch | lazy boy recliner | suede love seat | RHS | LHS | RHS | Neither | RHS |
| … | … | … | … | … | … | … | … |

The really astute reader will notice something.

![](https://softwaredoug.com/assets/media/2025/unix-system.jpg)

It’s a Machine Learning problem!

We have a set of **features** - the individual predictions of each attribute We have a **label** we want to predict - the human preference

The table above becomes a classification problem!

We can “learn” the right ensemble. Perhaps with a decision tree or other simple classifier.

First step, bulid up a big table like the one above with 1000s of LLM evaluations of individual fields and variants on or off. So in reality we have:

| Query | LHS product | RHS Product | Name | Name (double check) | Name (allow neither) | Name (double check/allow neither) | Desc | … | Human Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| entrance table | alea coffee table | marta coffee Table | Neither | LHS | LHS | RHS | RHS | … | LHS |
| … | … | … | … | … | … | … | RHS | … | … |

So I collect N of each type of LLM evaluation with a [script](https://github.com/softwaredoug/local-llm-judge/blob/main/collect.sh):

```bash
#!/bin/bash

N="$1"

poetry run python -m local_llm_judge.main --verbose --eval-fn category_allow_neither --N $N
poetry run python -m local_llm_judge.main --verbose --eval-fn category --N $N
poetry run python -m local_llm_judge.main --verbose --eval-fn category_allow_neither --check-both-ways --N $N

...
poetry run python -m local_llm_judge.main --verbose --eval-fn name --N $N
...
```

I stressed my laptops heat disapation capabilities by running `./collect.sh 7000` to get 7000 examples (first 1000 the same test used above, next 6000 I’ll use for training).

Each run above has an output of the query, LHS, RHS product with human and agent preference. The agent preference in each is our feature.

Finally, we can point a [training script](https://github.com/softwaredoug/local-llm-judge/blob/main/local_llm_judge/train.py) to the outputs generated by each LLM run from the script above:

```
$ poetry run python -m  local_llm_judge.train --feature_names data/both_ways_category.pkl data/both_ways_name.pkl  data/both_ways_desc.pkl data/both_ways_classs.pkl data/both_ways_category_allow_neither.pkl data/both_ways_name_allow_neither.pkl data/both_ways_desc_allow_neither.pkl data/both_ways_class_allow_neither.pkl
```

The training script builds out our training features (the agent preference of the agent variants we’re using) along with human pairwise preference we want to predict.

As a basic spike, I just use a simple Scikit decision tree to try to predict human\_preference from the agent\_preferences:

```python
def train_tree(train, test):
    clf = DecisionTreeClassifier()
    clf.fit(train.drop(columns=['query', 'product_id_lhs', 'product_id_rhs', 'human_preference']),
            train['human_preference'])
    ...
```

And finally, when using the tree, we make a precision / recall tradeoff. We enforce a threshold on the prediction probability to accept the decision, otherwise label as “Neither”:

```python
def predict_tree(clf, test, threshold=0.9):
    """Only assign LHS or RHS if the probability is above the threshold"""
    probas = clf.predict_proba(test.drop(columns=['query', 'product_id_lhs', 'product_id_rhs', 'human_preference']))
    definitely_lhs = probas[:, 0] > threshold
    definitely_rhs = probas[:, 1] > threshold
```

The script tries every variant:

```
['both_ways_desc_allow_neither', 'both_ways_class_allow_neither'] 1.0 0.013
['both_ways_name', 'both_ways_class_allow_neither'] 0.9861111111111112 0.072
['both_ways_category', 'both_ways_name', 'both_ways_classs', 'both_ways_name_allow_neither', 'both_ways_class_allow_neither'] 0.9673366834170855 0.398
['both_ways_category', 'both_ways_name', 'both_ways_classs', 'both_ways_class_allow_neither'] 0.9668508287292817 0.362
['both_ways_desc', 'both_ways_class_allow_neither'] 0.9666666666666667 0.06
['both_ways_desc', 'both_ways_desc_allow_neither', 'both_ways_class_allow_neither'] 0.9666666666666667 0.06
['both_ways_name', 'both_ways_desc_allow_neither', 'both_ways_class_allow_neither'] 0.9666666666666667 0.09
['both_ways_category', 'both_ways_name', 'both_ways_classs'] 0.9665738161559888 0.359
['both_ways_category', 'both_ways_name', 'both_ways_desc', 'both_ways_classs', 'both_ways_category_allow_neither'] 0.9659367396593674 0.411
['both_ways_category', 'both_ways_name', 'both_ways_classs', 'both_ways_category_allow_neither', 'both_ways_name_allow_neither'] 0.9654320987654321 0.405
...
```

Many caveants to this data - how reproducible is this? What happens when we do some cross-validation or on more test data? Treat it as an interesting data point in a scientific lab notebook, not a guarantee it will definitely work.

The data though is quite interesting. One variant appears to be able to classify every human label in test correctly. But only for 1.3% of the data. Another does 96.5% precision on 40.5% of the data.

Trees allow us to see the dependencies between features when predicting relevance. We can use this as an exploratory tool to guide searc solutions. We can dump the tree with `print(export_text(clf, feature_names=feature_names))`, noting how the tree thinks about the dependencies in the data, helping you plan, prioritize, and strategize how search should work.

```
|--- both_ways_category <= 0.50           # category preference is either LHS (-1) or neither (0)
|   |--- both_ways_category <= -0.50          # category preference is LHS (-1)
|   |   |--- both_ways_name <= 0.50               # Name preference is LHS (-1) or neither (0)
             |--- class: -1                          # Then prediction is "LHS"
...
```

According to this tree, any search solution might want to focus on category first before considering name, for example.

Finally, this is just the start. A dumb decision tree classifier may not be the best choice. Perhaps we want to do some kind of gradient boosting instead of a tree? Given trees tend to overfit, perhaps another solution would be best.

But the upshot of all this is we can take lots of dumb agents, making single, basic decisions, and combine their outputs into something smarter using traditional ML. We can use them to understand the reasoning behind human labels, helping inform how we build solutions. Local LLMs could become ML feature generators, maybe heavily cachable ones at that! We keep their decisions dumb, simple, and interpretable combining them at the end with fast boring, old ML that can finish the job.

---

### Enjoy softwaredoug in training course form!

#### Starting May 18!

Signup here - [http://maven.com/softwaredoug/cheat-at-search](http://maven.com/softwaredoug/cheat-at-search) [![](https://softwaredoug.com/assets/media/2026/cheat-at-search-social.png) ](https://maven.com/softwaredoug/cheat-at-search)I hope you join me at [Cheat at Search with Agents](https://maven.com/softwaredoug/cheat-at-search) to learn use agents in search. build better RAG and use LLMs in query understanding.

---