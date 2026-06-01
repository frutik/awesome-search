---
title: "t-SNE Explained: Visualising High-Dimensional Data"
source: "https://medium.com/data-science-explained/t-sne-explained-visualising-high-dimensional-data-4f556041a80e"
author:
  - "[[Billy Chan]]"
published: 2025-12-26
created: 2026-06-01
description: "More"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*1rzwPndh_GpQrc9R)

t-SNE is a bit like a child’s drawing: it simplifies something complicated while keeping the important shapes recognisable. (Photo by Jerry Wang on Unsplash )

t-SNE (t-distributed stochastic neighbor embedding) is one of the most popular algorithms for dimensionality reduction. When we want to turn a dataset with many features into something we can visualise beautifully in two dimensions.

It **transforms distances into probabilities** and then **searches for a low-dimensional layout** that **preserves those probabilities** as closely as possible.

It took me a long time to understand the math, so this post is written for future-me (when I forget about everything) and for anyone who wants a clear, friendly explanation.

## High-D vs Low-D Setup

Imagine a dataset with two features, *x1* and *x2*. You can easily plot it and see clusters.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zRnMkIml77qS6MWtC_oEqg.png)

A tiny dataset with two features: x1 and x2.

![](https://miro.medium.com/v2/resize:fit:1152/format:webp/0*QzoT3NxdNo6wGygR.png)

We can easily see the structure of a 2-dimensional dataset.

When the dataset has 100 features, the structure still exists, but we can’t visualise it. We’re essentially blind.

To make the explanation manageable, I’ll keep the “high-dimensional” space at two features and map it to another two-dimensional space. I’ll call the original space **high-D** (imaginatively) and the projected space **low-D**.

## Step 1: Pick a Point

Take the first data point (1, 2). Call it *i*. All other points are *j* ’s: *j1*, *j2*, *j3*, *j4*.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KGr6TO-s7bYYjCPBVV7lvA.png)

## Step 2: Compute Euclidean Distances

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ZeLv59gLNWkO6Drqcu2htA.png)

We measure how far each *j* is from *i*:

![](https://miro.medium.com/v2/resize:fit:1232/format:webp/1*RuDrsCVGcj42A6D4UHr0lw.png)

In 100 dimensions, we simply continue the sum until x100. (x3,i — x3,j)² + (x4,i — x4,j)² + …

Take i and j1 as an example:

![](https://miro.medium.com/v2/resize:fit:1348/format:webp/1*YzWxfXPwPkQ1kCwK8ijpPA.png)

Distance for each *j* from *i*:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*CRh4OXJUVJrSjlL9ht__wA.png)

Distances alone aren’t ideal for comparing neighbourhoods across points with different densities, so t-SNE converts distances into probabilities.

### Extra: Why are probabilities better than distances?

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*DPLsE05wy_GgKnds.png)

In the dataset above, the distances among a dense cluster are not comparable to those among a sparse cluster.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*sD44b4giFQ9Nd0Sq.png)

Using probabilities normalises distance scale locally, allowing fair comparison between points in dense and sparse regions. In the right chart, t-SNE can visualise the two clusters well regardless of their within-cluster density. In the left chart, a distance-based algorithm fails to unveil the cluster that is sparse in a high-D space.

## Step 3: Convert Distances to Gaussian Similarity Scores

Centre a Gaussian distribution at point *i*. Each *j* gets a score from the curve.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*5wd3wodGylmUptIL.png)

j1 and j2 have the same distance from i, so their labels overlap.

This function used to derive the corresponding value from the curve is called radial basis function kernel (**RBF**), also known as the **Gaussian kernel**. The equation:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*OV-F6eiy4UfWXonp3t_rXA.png)

exp() computes e ^x, where e is Euler’s number.

*j* ’s that are closer to *i* get higher scores.

## Step 4: Convert Scores to Conditional Probabilities

We only evaluate the Gaussian at a few points, so the similarity scores do not sum to 1. To convert a score into a probability, we need to normalise the scores by adding all scores to the denominator:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*zjeRln2R6yLobgwizIWYyg.png)

The denominator is the sum of scores for j1 + j2 + j3 + j4.

This is the probability that *j* is a neighbour of *i*. *j* ’s that are closer to *i* get higher probabilities.

## Step 5: Choose Sigma Using Perplexity

To calculate the probabilities, we need to find an ideal value for σ *i*.

t-SNE chooses it by controlling the **entropy** of the conditional distribution. P *i* = { p *j|i* }.

In this example, the conditional distribution P *i* = \[ p *j1|i*, p *j2|i*, p *j3|i*, p *j4|i* \].

The [entropy](https://medium.com/data-science-explained/entropy-explained-simply-measuring-uncertainty-in-data-37de408d27b1) of P *i*:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*dnYLTpvAaBqgS_-XU-Tzuw.png)

We use log base 2 here.

That is, \[( p *j1|i* ) \* ( log p *j1|i* )\] + \[( p *j2|i* ) \* ( log p *j2|i* )\] + …, then multiply the total sum by -1. The entropy represents the uncertainty of the array of probabilities for the *j* ‘s being the neighbours of *i*.

We choose σ *i* to satisfy:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*RkaDUKK-qk4aTR15WSnX_A.png)

The definition of perplexity is based on the Shannon entropy, which is defined using the log base 2.

**Perplexity** is a hyper-parameter whose value we manually assign to the algorithm, usually from 5 to 50.

When perplexity = 5, then log (5) = 2.32. The algorithm therefore searches the optimal value for σ *i*, which returns probabilities whose distribution has an entropy equals 2.32.

### Why increasing perplexity increases sigma

- Higher perplexity ⇒ higher required entropy
- ⇒ more spread-out probabilities
- ⇒ the Gaussian must be wider
- ⇒ σ *i* must increase.

### Intuition behind perplexity

**Perplexity** ≈ the “ **effective number of neighbours** ” for point *i*.

- Perplexity = 1 ⇒ entropy = 0 ⇒ all mass on one neighbour ⇒ distribution like \[1, 0, 0, 0, …\].
- Perplexity = 2 ⇒ entropy = 1 ⇒ distribution like \[0.5, 0.5, 0, 0, …\].
- Perplexity = 30 ⇒ entropy = 4.9 ⇒ roughly equal mass over ~30 neighbours ⇒ distribution like \[0.033, 0.033, 0.033, …\].

Once the perplexity value is assigned, it stays the same for the entire process. In this toy example so far, we have only been treating point ID 1 as *i*. Once we have found the σ and calculated all the conditional probabilities for this point ID 1 which satisfies the required entropy, we move on to treat point ID 2 as *i*, and repeat the process.

This means t-SNE lets each *i* adapt its own σ so that *i* ‘s in dense regions use smaller sigmas, and sparse regions use larger ones:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yr9olAzZi4qxpanZpzcK0g.png)

### Why i in dense region use a smaller sigma

![](https://miro.medium.com/v2/resize:fit:1134/format:webp/0*17QooVxZi3GTIdRn.png)

Imagine we set the perplexity to 10 ≈ 10 neighbours for *i*. When *i* is in a dense region, we need a narrower curve (black) to include only 10 neighbours, and push all the others into the very end with extremely low probabilities. In a sparse region, a wider curve (green) can spread out such that we catch the 10 neighbours.

## Step 6: Collect All Conditional Probabilities

Now we have all p *j|i* values, forming a **conditional probability matrix** where each row sums to 1. These probabilities explain how each point *i* sees its own neighbourhood.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*kmYqAc731Dv4wMjNCD_3aQ.png)

Perplexity = 2 in this toy example.

We can read the table like this:

- In row one where *i* = 1, point ID 2 is very close, giving a probability = 0.5
- Point ID 3 is equally close, giving a probability = 0.5.
- Point ID 4 and 5 are both far away from i, giving extremely low probabilities.
- As perplexity = 2, each row has entropy ≈ log(2) = 1.

Note that the matrix is **asymmetric**: p *j|i* ≠ p *i|j*. For example, p(1|2) ≠ p(2|1). This is because when i = 2, it has its own σ which determines p(1|2). When i = 1, it also has its own σ which determines p(2|1).

## Step 7: Make a Symmetric Joint Probability Matrix

t-SNE merges the two direction-specific probabilities:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*8elvCRmmgfV2duTV8pBvyg.png)

N represents the total number of data points.

The denominator 2N ensures all joint probabilities across all *i* ‘s sum to 1.

### Joint Probability Matrix:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_l6vPt3qfwuDQ7OoYDjb8w.png)

We can read the table like this:

- Row name is *i*. Column name is *j*.
- p(2, 1) = 0.102125, representing the joint probability of 2 and 1, or the probability of seeing 2 and 1 are neighbours.
- p(1, 2) = 0.102125, too.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*66ncdDz-GNbEmP69WnAurA.png)

Since the matrix is symmetrical, we can only use half of it as the second half is redundant. We can see a total of 10 joint probabilities, hence the denominator for the normalisation is 2N = 10. These 10 probabilities sum to 1. This joint distribution P represents neighbour relationships in high-D space.

## Step 8: Model Probabilities in the Low-D Space

In low-D, we start with random positions y *i*, and compute probabilities using a **Student-t distribution with 1 degree of freedom (also called Cauchy distribution)**:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*PGXTW0WmSGcOYvbM4i4sGg.png)

This looks very similar to the conditional probability equation in the high-D space. The numerator represents the function for the Cauchy distribution. || y *i* — y *j* || represents the Euclidean distance between y *i* and y *j*. y *i* is the coordinate, or a vector, for point *i*.

Then we symmetrise again:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*GKSXfQgdRD19zYK4j-XKWg.png)

### Why Student-t instead of Gaussian?

In high-D space, distances tend to concentrate. Most points are almost equally far apart. When we try to represent these high-D neighbourhood relationships in a low-D space, there simply isn’t enough room. Points that should be moderately far apart get pushed too close together. This is known as the crowding problem.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*3hbMibnVEFpNWP4o.png)

Gaussian tails drop too fast. Student-t is a heavy-tailed distribution which allows distant points to remain meaningfully far in probability terms, reducing cluster “crowding.” In a Gaussian kernel, distant points all get extremely tiny similarity values, making them indistinguishable. The Student-t kernel avoids this.

## Step 9: Minimise the Difference Between High-D and Low-D Probabilities

We already have the value for each p *ij* in high-D (the 10 joint probabilities), Now, we want to find the 5 optimal y *i* in low-D, which is determined by q *ij* matching p *ij*.

t-SNE measures the mismatch using a cost function, **Kullback–Leibler divergence**:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*w1tLuqrB6iqzx2XTmiPSGA.png)

The log here is a natural log.

To break down this equation:

1. We take a pair of *i* and *j* from both the high-D and low-D space. For example, *i* = point ID 1 and *j* = point ID 2.
2. We already have the p *ij* value from the high-D space. That can be found in the joint probability matrix.
3. We randomly assign the coordinates for *i* in the low-D space. In the toy example, we have 5 data points. So we have 5 random y *i*.
4. Since each *i* takes turn to be *j*, we now also have all the random y *j*.
5. With y *i* and y *j* in place, we can calculate all the 10 q *ij*, which are the joint probabilities in the low-D space.
6. With both the p *ij* and q *ij* for *i* = point ID 1 and *j* = 2, we can multiply p *ij* by the log of p *ij* / q *ij*, as shown in the equation.
7. We then repeat the same process for *i* = point ID 1 and *j* = 3, and so on. Then sum the results up.
8. The total sum is the cost that we want to minimise.

### Why does KL behave this way?

- If p *ij* is **large** but q *ij* is **small**, the term becomes very large.
- This means *i* and *j* are close in high-D but far in low-D → an error worth strongly correcting.
- The optimisation process then makes q *ij* larger by pulling *i* and *j* closer in the low-D space.
- If p *ij* is **small**, the term contributes very little, even if q *ij* is moderately large. Imagine when p *ij* ≈ 0, the whole term becomes 0.
- This means pairs far apart in high-D matter less. KL divergence **does not care** whether q *ij* is large or small. It doesn’t waste effort pushing them farther in low-D.

### Wouldn’t far points get too close in low-D?

Theoretically, yes. KL divergence therefore emphasises preserving **local structure**.Cluster shape is preserved, but cluster distances are arbitrary. This is why **between-cluster spacing is meaningless** in t-SNE plots.

In practice, far-away points rarely end up on top of each other. The heavy-tailed t-distribution creates strong repulsion in low-D. Even pairs getting too close and generate large q *ij*, the Student-t kernel can still push them apart.

### Optimisation

t-SNE uses gradient descent to adjust all y *i* so that Q approaches P. P is the matrix of all pairwise joint probabilities in high-D. Q is the matrix of low-D joint probabilities.

Below is a beautiful interactive that shows how KL divergence gradually pulls the randomly assigned y *i* closer. Notice, the three 10-dimensional clusters are at different distances from each other. But in the 2D space, they have similar distances. This shows “between-cluster spacing is meaningless.”

## [How to Use t-SNE Effectively](https://distill.pub/2016/misread-tsne/?source=post_page-----4f556041a80e---------------------------------------#perplexity=20&epsilon=5&demo=2&demoParams=50,10)

### Although extremely useful for visualizing high-dimensional data, t-SNE plots can sometimes be mysterious or misleading.

distill.pub

## How to Run t-SNE in Python

Let’s use one of the classic high-D datasets in scikit-learn: the handwritten digits dataset.

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*A-wcHDHHqhwj-ay-.png)

( scikit-learn )

Each digit is an 8×8 image, flattened into **64 features**. This means every data point lives in a 64-dimensional space. t-SNE compresses those 64 dimensions down to **just two**, while preserving the neighbourhood structure as faithfully as possible.

```c
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE

# Load a popular high-dimensional dataset: handwritten digits
digits = load_digits()
X = digits.data        # shape: (1797, 64)
y = digits.target      # digit labels: 0–9

print("Original shape:", X.shape)   # (1797, 64)

# Run t-SNE to reduce 64-D data down to 2-D
tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate=200,
    init="random",
    random_state=0
)
X_2d = tsne.fit_transform(X)

print("Embedded shape:", X_2d.shape)  # (1797, 2)

# Plot the 2D embedding, coloured by digit label
plt.figure(figsize=(7, 6))
scatter = plt.scatter(
    X_2d[:, 0],
    X_2d[:, 1],
    c=y,
    cmap="tab10",
    s=15,
    alpha=0.8
)

plt.title("t-SNE visualisation of handwritten digits (64-D → 2D)")
plt.xlabel("Component 1")
plt.ylabel("Component 2")

# Add a legend for digit labels
handles, _ = scatter.legend_elements(prop="colors")
labels = [str(i) for i in range(10)]
plt.legend(handles, labels, title="Digit")

plt.tight_layout()
plt.show()
```
![](https://miro.medium.com/v2/resize:fit:1380/format:webp/0*Eh3pBk2yP5F3GLNh.png)

Points that represent similar digits (for example, lots of “1”s or lots of “8”s) end up forming tight clusters. Even though the original data lived in 64-D, t-SNE can uncover meaningful structure and show it to us in a way we can understand at a glance.

## Key Takeaway

t-SNE works by turning distances into probabilities so that every point, whether in a dense or sparse region, gets a fair chance to define its neighbourhood.

By matching these probabilities in low-D using a heavy-tailed distribution, t-SNE preserves local structure (but not large-scale global structure) while giving us a meaningful visualisation of high-dimensional data.

The Python code for the plots in this blog post is [here](https://www.kaggle.com/code/billychanhub/t-sne).