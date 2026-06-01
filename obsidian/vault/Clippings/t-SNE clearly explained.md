---
title: "t-SNE clearly explained"
source: "https://medium.com/data-science/t-sne-clearly-explained-d84c537f53a"
author:
  - "[[Kemal Erdem (burnpiro)]]"
published: 2020-04-13
created: 2026-06-01
description: "An intuitive explanation of t-SNE algorithm and why it’s so useful in practice."
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*gjhEXfy5r3L4S1ZYlBYdKw.png)

Source: K. Movahedi, Y. Saeys, http://www.brainimmuneatlas.org/tsne-cp-irf8.php

## What is t-SNE?

Many of you already heard about dimensionality reduction algorithms like **PCA**. One of those algorithms is called **t-SNE** (t-distributed Stochastic Neighbor Embedding). It was developed by Laurens van der Maaten and Geoffrey Hinton in 2008. You might ask “Why I should even care? I know PCA already!”, and that would be a great question. t-SNE is something called **nonlinear dimensionality reduction**. What that means is this algorithm allows us to separate data that cannot be separated by any straight line, let me show you an example:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*rPhupOA95cU_GmCD.png)

Linearly nonseparable data, Source: https://distill.pub/2016/misread-tsne/ CC-BY 2.0

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*4Uv73sfML2MrEtoK.png)

Linearly nonseparable data, Source: https://distill.pub/2016/misread-tsne/ CC-BY 2.0

If you want to play with those examples go and visit [Distill](https://distill.pub/2016/misread-tsne/).

As you can imagine, those examples won’t return any reasonable results when parsed through PCA (ignoring the fact that you’re parsing 2D into 2D). That’s why it’s important to know at least one algorithm that deals with linearly nonseparable data.

==You need to remember that t-SNE is iterative so unlike PCA you cannot apply it on another dataset.== PCA uses the global covariance matrix to reduce data. You can get that matrix and apply it to a new set of data with the same result. That’s helpful when you need to try to reduce your feature list and reuse matrix created from train data. t-SNE is mostly used to understand high-dimensional data and project it into low-dimensional space (like 2D or 3D). That makes it extremely useful when dealing with CNN networks.

## How t-SNE works?

### Probability Distribution

Let’s start with **SNE** part of t-SNE. I’m far better with explaining things visually so this is going to be our dataset:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*NYve_va3wHU4zNnj.png)

It has 3 different classes and you can easily distinguish them from each other. The first part of the algorithm is to create a **probability distribution** that represents similarities between neighbors. What is “similarity”? [Original paper](http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf) states “ **similarity of datapoint** xⱼ **to datapoint** xᵢ **is the conditional probability** p\_{j|i}**, that** xᵢ **would pick** xⱼ **as its neighbor** “.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*ETuCH0wXgSyit1i3.png)

We’ve picked one of the points from the dataset. Now we have to pick another point and calculate Euclidean Distance between them |xᵢ — xⱼ|

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*g1bTTv6Wu632piCu.png)

The next part of the original paper states that it has to be ==**proportional to probability density under a Gaussian centered**== **at** xᵢ. So we have to generate Gaussian distribution with mean at xᵢ*,* and place our distance on the X-axis.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*j6P77qstfwQ6mkT8.png)

Right now you might wonder about *σ²* (variance) and that’s a good thing. But let’s just ignore it for now and assume I’ve already decided what it should be. After calculating the first point we have to do the same thing for every single point out there.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*Afr8xsKrl6dwZ10Q.png)

You might think, we’re already done with this part. But that’s just the beginning.

### Scattered clusters and variance

Up to this point, our clusters were tightly bounded within its group. What if we have a new cluster like that:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*nZrA0hPQqM1Ce7-j.png)

We should be able to apply the same process as before, shouldn’t we?

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0MzS6wydzd5Dr02Y.png)

We’re still not done. You can distinguish between similar and non-similar points but absolute values of probability are much smaller than in the first example (compare Y-axis values).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*kpctqZwCMDkqJK3u.png)

We can fix that by dividing the current projection value by the sum of the projections.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*1gBOzGPwWEN4L_HhYLN-VQ.png)

Which if you apply to the first example will look sth like:

![](https://miro.medium.com/v2/resize:fit:1228/format:webp/1*r3tuMMndpFZswRfIVNCEaw.png)

And for the second example:

![](https://miro.medium.com/v2/resize:fit:1262/format:webp/1*9XfcJTE-gFjGxFgdqOQKsQ.png)

This scales all values to have a sum equal to 1. It’s a good place to mention that p\_{i|i} is set to be equal to 0, not 1.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*2oCxcLq7hvxQcrjmFiClMA.png)

### Dealing with different distances

If we take two points and try to calculate conditional probability between them then values of p\_{i|j} and p\_{j|i} will be different:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*pTTqRArwYV_tGnF0.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*-JXLaDNYjjSSGVdf.png)

The reason for that is because they are coming from two different distributions. Which one should we pick to the calculation then?

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*gFbUxuUZlcRhIzYXvYzUCA.png)

Where *N* is a number of dimensions.

### The lie:)

Now when we have everything scaled to 1 (yes, the sum of all equals 1), I can tell you that I wasn’t completely honest about while the process with you:) Calculation all of that would be quite painful for the algorithm and that’s not what exactly is in [t-SNE paper](http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf).

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*J4lRX3F6qR9TF9VgH6Vd1Q.png)

This is an original formula to calculate p\_{j|i}. Why did I lie to you? First, because it’s easier to get an intuition about how it works. Second, because I was going to show you the trough either way.

### Perplexity

If you look at this formula. You can spot that our

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*2q0ECctHTmnbCop71LlJOQ.png)

is

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*3_qQH7KjQR89ymcDk0Y5Yw.png)

If I would show you this straight away, it would be hard to explain where *σ²* is coming from and what is a dependency between it and our clusters. Now you know that variance depends on Gaussian and the number of points surrounding the center of it. This is the part where **perplexity** value comes. A perplexity is more or less a target number of neighbors for our central point. Basically, the higher the perplexity is the higher value variance has. Our “red” group is close to each other and if we set perplexity to 4, it searches the right value of to “fit” our 4 neighbors. If you want to be more specific then you can quote the original paper:

> *SNE performs a binary search for the value of sigma that produces probability distribution with a fixed perplexity that is specified by the user*

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Csv1yl-2zOxC42wV-WGVkQ.png)

Where

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*jhLo78eY9Jky4vMP42RC8Q.png)

is **Shannon entropy**. But unless you want to implement t-SNE yourself, the only thing you need to know is that perplexity you choose is positively correlated with the value of \\mu\_i *μi* and for the same perplexity you will have multiple different \\mu\_i *μi*, base on distances. Typical perplexity value ranges between 5 and 50.

### Original formula interpretation

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*J4lRX3F6qR9TF9VgH6Vd1Q.png)

When you look on this formula you might notice that our Gaussian is converted into

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*xi6CUrwPLG4-1CZwt-hX0Q.png)

Let me show you how that looks like:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*sNHrck20Xt7uS7X9.png)

If you play with *σ²* for a while you can notice that the blue curve remains fixed at point *x* =0. It only stretches when *σ²* increases.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*SQWPC3TlgUqnsuSu.png)

That helps distinguish neighbor’s probabilities and because you’ve already understood the whole process you should be able to adjust it to new values.

### Create low-dimensional space

The next part of t-SNE is to create low-dimensional space with the same number of points as in the original space. Points should be spread randomly on a new space. The goal of this algorithm is to find similar probability distribution in low-dimensional space. The most obvious choice for new distribution would be to use Gaussian again. That’s not the best idea, unfortunately. One of the properties of Gaussian is that it has a “short tail” and because of that it creates a **crowding problem**. To solve that we’re going to use ==**Student t-distribution**== ==with a single degree of freedom==. More of how this distribution was selected and why Gaussian is not the best idea you can find in the [paper](http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf). I decided not to spend much time on it and allow you to read this article within a reasonable time. So now our new formula will look like:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*ZDiRzmCfK1xuCzldJ8-tvQ.png)

instead of:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Hax1tT4LMqH9RqUN4d7ulA.png)

If you’re more “visual” person this might help (values on X-axis are distributed randomly):

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*z_xyrUJsAlkdKNjX.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*SEhDsFAK-qH6fLJv.png)

Using Student distribution has exactly what we need. It “falls” quickly and has a “long tail” so points won’t get squashed into a single point. This time we don’t have to bother with *σ²* because we don’t have one in q\_{ij} formula. I won’t generate the whole process of calculating q\_{ij} because it works exactly the same as p\_{ij}. Instead, just leave you with those two formulas and skip to sth more important:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*l4Gjd2F_cnZQDvSi6zlu1w.png)

## Gradient descent

To optimize this distribution t-SNE is using [**Kullback-Leibler divergence**](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) between the conditional probabilities p\_{j|i} and q\_{j|i}

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*xi-IjvMSJmNu-jfHlZ0qvA.png)

I’m not going through the math here because it’s not important. What we need is a derivate for (it’s derived in **Appendix A** inside the [original paper](http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf)).

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*WK-kP2JJsAbYgw49hQENhA.png)

You can treat that gradient as repulsion and attraction between points. A gradient is calculated for each point and describes how “strong” it should be pulled and the direction it should choose. If we start with our random 1D plane and perform gradient on the previous distribution it should look like this.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*gx5m_CS7gVUn8WLH.gif)

Ofc. this is an exaggeration. t-SNE doesn’t run that quickly. I’ve just skipped a lot of steps in there to make it faster. Besides that, the values here are not completely correct, but it’s good enough to show you the process.

### Tricks (optimizations) done in t-SNE to perform better

t-SNE performs well on itself but there are some improvements allow it to do even better.

### Early Compression

To prevent early clustering t-SNE is adding L2 penalty to the cost function at the early stages. You can treat it as standard regularization because it allows the algorithm not to focus on local groups.

### Early Exaggeration

This trick allows moving clusters of (q\_{ij}) more. This time we’re multiplying p\_{ij} in early stages. Because of that clusters don’t get in each other’s ways.

## Examples

If you remember examples from the top of the article, not it’s time to show you how t-SNE solves them.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*e9VGikGkIF2HwSDt.png)

Source: https://distill.pub/2016/misread-tsne/ CC-BY 2.0

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*FqyHg8h-8ODS513w.png)

Perplexity 5, Source: https://distill.pub/2016/misread-tsne/ CC-BY 2.0

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*XUmdoGc5EGiY1rHR.png)

Source: https://distill.pub/2016/misread-tsne/ CC-BY 2.0

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*EEWMIAKFCB6B0PnX.png)

Perplexity 5, Source: https://distill.pub/2016/misread-tsne/ CC-BY 2.0

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*Kvy_VFV4jyvFlP1e.png)

Perplexity 5, Source: https://distill.pub/2016/misread-tsne/ CC-BY 2.0

All runs performed 5000 iterations.

### CNN application

t-SNE is also useful when dealing with [CNN](https://en.wikipedia.org/wiki/Convolutional_neural_network) feature maps. As you might know, deep CNN networks are basically black boxes. There is no way to really interpret what’s on deeper levels in the network. A common explanation is that deeper levels contain information about more complex objects. But that’s not completely true, you can interpret it like that but data itself is just a high-dimensional noise for humans. But, with the help of t-SNE you can create maps to display which input data seams “similar” for the network.

One of those translations was done by [Andrej Karpathy](https://cs.stanford.edu/people/karpathy/) and it’s available here [https://cs.stanford.edu/people/karpathy/cnnembed/cnn *embed* 6k.jpg](https://cs.stanford.edu/people/karpathy/cnnembed/cnn_embed_6k.jpg).

What Karpathy did? He took 50k images from [LSVRC 2014](http://www.image-net.org/challenges/LSVRC/2014/) and extracted a 4096-dimensional CNN feature map (to be more precise, that 4096 map comes from fc7 layer).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*ZolEq54VtcgnT3zL.png)

CNN Network, Source: Hierarchical Localization in Topological Models Under Varying Illumination Using Holistic Visual Descriptors

After getting that matrix for every single image, he computed a 2D embedding using t-SNE. In the end, he just generated that map with original images on 2D chart. You can easily spot which images are “similar” to each other for that particular CNN Network.

## Conclusions

t-SNE is a great tool to understand high-dimensional datasets. It might be less useful when you want to perform dimensionality reduction for ML training (cannot be reapplied in the same way). It’s not deterministic and iterative so each time it runs, it could produce a different result. But even with that disadvantages it still remains one of the most popular method in the field.

## References:

- L. Maaten, G. Hinton. Visualizing Data using t-SNE, 2008 [http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf](http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf)
- Cristobal Parra, Sergio Cebollada, Luis Payá, Mathew Holloway, Oscar Reinoso, “A Novel Method to Estimate the Position of a Mobile Robot in Underfloor Environments Using RGB-D Point Clouds”, *Access IEEE*, vol. 8, pp. 9084–9101, 2020.