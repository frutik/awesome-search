---
title: "PCA vs t-SNE: which one should you use for visualization"
source: "https://medium.com/analytics-vidhya/pca-vs-t-sne-17bcd882bf3d"
author:
  - "[[Namratesh Shrivastav]]"
published: 2019-12-28
created: 2026-06-01
description: "More"
tags:
  - "clippings"
---
Dimensionality is the major factor in any dataset. We humans can’t [**visualize**](https://www.analyticsvidhya.com/blog/2021/04/a-complete-beginners-guide-to-data-visualization/?utm_source=Backlink&utm_medium=SEO) more than 3d properly so to understand we have to reduce the size of dimension so we can visualize properly. There are many methods to reduce dimension for visualization but here we are going to discuss PCA and t-SNE.

We are using MNIST dataset for knowing more about PCA and t-SNE. A little bit about MNIST data:

- mnist\_train.csv file contains the 60,000 training examples and labels.
- mnist\_test.csv contains 10,000 test examples and labels.
- Each row consists of 785 values: the first value is the label (a number from 0 to 9) and the remaining 784 values are the pixel values (a number from 0 to 255).
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*T7DVYVqZ6-yjOIZU)

[https://i1.wp.com/varianceexplained.org/images/mnist.png?w=584](https://i1.wp.com/varianceexplained.org/images/mnist.png?w=584)

## PCA(Principal Component Analysis):

PCA is one of the most important methods of dimensionality reduction for visualizing data. [**PCA**](https://www.analyticsvidhya.com/blog/2022/07/principal-component-analysis-beginner-friendly/?utm_source=Backlink&utm_medium=SEO) is a technique that converts n-dimensions of data into k-dimensions while maintaining as much information from the original dataset. Suppose you have given data of 100 dimensions now, you need to convert it into low dimension let’s say in 50 dimensions. So for that, we can use PCA. There are few steps in PCA to reduce the dimension.

![](https://miro.medium.com/v2/resize:fit:1384/format:webp/0*tcoQiyzqV1K66do0.png)

[https://blog.bioturing.com/wp-content/uploads/2018/11/Blog\_pca\_6b.png](https://blog.bioturing.com/wp-content/uploads/2018/11/Blog_pca_6b.png)

- calculate the mean of each column
- center the value in each column by subtracting the mean column value
- calculate covariance matrix of centered matrix
- calculate eigendecomposition of the covariance (eigenvectors represent the magnitude of directions or components for the reduce subspace)

If all Eigenvalue has a similar value, then we know that the existing representation may already be compressed.

## t-SNE(T- distributed Stochastic Neighbor Embedding):

t-SNE is also a method to reduce the dimension. One of the most major differences between PCA and t-SNE is it preserves only local similarities whereas PA preserves large pairwise distance maximize variance.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*tZjSp7iCt3DG7biOS1-pxA.png)

Suppose we have these points x1,x2,x3. Then t-SNE will try to preserve the local neighbors. It will convert in two points because there is almost

```c
d(x1,x2) - N((x2',x3')
```
- It takes a set of points in high dimensional data and converts it into low dimensional data.
- It’s a non-linear method and adapts to the underlying data performing different transformations in different regions.
- It’s incredibly flexible and often finds a structure where other dimensionality reduction algorithms can’t.

**CODE:**

**Loading dataset**

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*PkQq0ZbE82pnBY8nN1_5vw.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*JjC3MA4Y29K1SgNaxInpYg.png)

Some pre-processing in a dataset

- storing all labels in l
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*oNEMIJkNVx1IxS1fyjc-jg.png)

- dropping label from data and storing data by new variable d
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*DPj1a3JXu-umAgpqK40-nQ.png)

- checking the shape of data
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*0W7FgDBwRe6yVq5Y_pxZtQ.png)

**Visualizing data:**

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*RMFArxntTs_bZ5dvpUN_VA.png)

- Taking only the first 15000 points to reduce computation.
![](https://miro.medium.com/v2/resize:fit:1290/format:webp/1*irIjbE7T6ZI3C7R2F4LT2g.png)

- Standardizing data
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Fvj3iRWaNtHQbML9eIgdow.png)

## PCA

- co-variance of matrix
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*1xko_jI-Y6qK3FpEGyw4gw.png)

- finding eigenvalue and corresponding vectors.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*R0zVlrahWmONx50oV7hmLw.png)

- projecting the original data sample on the plane formed by two principal eigen vectors by vector-vector multiplication.
![](https://miro.medium.com/v2/resize:fit:1308/format:webp/1*dWdLhg3re0BZ6xeuePwktg.png)

- appending label to the 2d projected data
- creating a new data frame for plotting the labeled points
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*31_B7U-BYitj3BAFc9XJLQ.png)

![](https://miro.medium.com/v2/resize:fit:1320/format:webp/1*AyaBz6daieSRwtxApmMeNg.png)

- plotting the 2d data points with seaborn
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*dOhItxEOaYcFEfdI6C8MPg.png)

- initializing the pca
![](https://miro.medium.com/v2/resize:fit:1162/format:webp/1*L3YlAMrzLctDnfaVsXKxcg.png)

- configuring the parameters, the number of components = 2
![](https://miro.medium.com/v2/resize:fit:1282/format:webp/1*DVFWqdut6thlxg2MN_2_sg.png)

- attaching the label for each 2-d data point,creating a new data fram which help us in ploting the result data
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ook8TLJOEn45s1Hqe8Vv-w.png)

![](https://miro.medium.com/v2/resize:fit:1292/format:webp/1*V6muKB5mzdFPS_-TUQ6IkA.png)

- PCA for dimensionality redcution (non-visualization)
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*V2_qMyvgrlTRAmI1KweBnw.png)

## t-SNE

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*j76hauNMqUASH67nHRQkzA.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zRIRI2LVV-1dcMNVRx9qYw.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*BDigfRccl0YP8MvQ_wMWvw.png)

[**Notebook**](https://github.com/namratesh/Machine-Learning/blob/master/_28_DEC_PCA%20vs%20tsne.ipynb) **link**

Suggestions are welcome.

Thanks for reading!!!

References:

- [https://colah.github.io/posts/2014-10-Visualizing-MNIST/](https://colah.github.io/posts/2014-10-Visualizing-MNIST/)
- [https://distill.pub/2016/misread-tsne/](https://distill.pub/2016/misread-tsne/)