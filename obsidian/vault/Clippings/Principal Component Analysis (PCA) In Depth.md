---
title: "Principal Component Analysis (PCA) In Depth"
source: "https://medium.com/@fraidoonomarzai99/principal-component-analysis-pca-in-depth-93c871f25dfa"
author:
  - "[[Fraidoon Omarzai]]"
published: 2024-07-20
created: 2026-06-01
description: "More"
tags:
  - "clippings"
---
This blog presents a comprehensive guide to the essentials of the PCA algorithm.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*aEzC_T8gjhUkqEuBPLFhAQ.png)

## How does PCA work?

→ PCA is a powerful tool for reducing the dimensionality of data while preserving its essential information. The goal is to get the best principle components that capture maximum variance.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*qt6cFehN_aJuZnsAfv0Gow.png)

- Given a dataset with *m* observations and *n* features, PCA calculates the covariance matrix of the data
- It then finds the eigenvectors and eigenvalues of this covariance matrix
- The eigenvectors represent the directions (principal components) of maximum variance in the data, and the corresponding eigenvalues represent the magnitude of this variance along each eigenvector
- By sorting the eigenvectors based on their corresponding eigenvalues in descending order, PCA identifies the most significant principal components

## Steps In PCA:

1. **Standardization**: Scale the features to have a mean of 0 and a standard deviation of 1 (optional but recommended).
2. **Compute Covariance Matrix**: This captures how the features vary together.
3. **Compute Eigenvectors and Eigenvalues**: Eigenvectors represent the directions of greatest variance, and eigenvalues tell you how much variance each eigenvector explains.
4. **Select Principal Components**: Choose the top *k* eigenvectors based on their corresponding eigenvalues to form the new feature subspace.
5. **Projection**: Project the original data onto the new feature subspace formed by the selected eigenvectors. Or project the original data points onto the new principal component axes.

## Practical Example

- The table below displays scores on math, English, and art tests for 5 students
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*7fJiDsHVhe1ltKOatwItiA.png)

**Step 1-** Compute Covariance Matrix:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*zTZ-l5KCToOqBiGBx3NL7Q.png)

> \- **cov(X,Y)**: covariance between X and Y
> 
> **\- X, Y**: features X and Y
> 
> **\- x̄, ȳ**: mean of features X and Y

- Below is our matrix A which represents our above data in matrix format
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*JTiRmvfEEo-icIOPPXJLcQ.png)

- When we compute the covariance matrix for matrix A, our output is:
![](https://miro.medium.com/v2/resize:fit:1184/format:webp/1*0H400zgbhzHvBaMB4dZskw.png)

**A few points that can be noted here are:**

> \- Shown in *Blue* along the diagonal, we see the variance of scores for each test
> 
> \- The art test has the biggest variance (720)
> 
> \- The English test, the smallest (360), so we can say that art test scores have more variability than English test scores
> 
> \- The covariance is displayed in black in the off-diagonal elements of the matrix **A**
> 
> \- The covariance between math and English is positive (360)
> 
> \- The covariance between math and art is positive (180)
> 
> \- The covariance between English and art, however, is zero. This means there tends to be no predictable relationship between the movement of English and art scores

**Step 2-** Compute Eigenvectors and Eigenvalues:

- *Let* ***A*** *be a square matrix,* ***ν*** *a vector, and* ***λ*** *a scalar that satisfies* ***A*** *ν* ***\= λ*** *ν, then* ***λ*** *is called the eigenvalue associated with eigenvector* ***ν*** *of* ***A***
![](https://miro.medium.com/v2/resize:fit:1328/format:webp/1*-ZgZq9IDbhRKnk7e0p4sSQ.png)

**Step 3-** Sort the eigenvectors based on their corresponding eigenvalues in descending order, and choose the top *k* eigenvectors based on their corresponding eigenvalues to form the new feature subspace.

> `*Note*`: The lowest eigenvalues bear the least information about the distribution of the data, and those are the ones we want to drop.

- Sorting eigenvalues in decreasing order
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*iwcoW_MoVC5LfFjhSD-SRg.png)

- For this example, our goal is to reduce a 3-dimensional feature space to a 2-dimensional feature space
- So eigenvectors corresponding to two maximum eigenvalues are:
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*-PZKO6wcdO-0IZ3ULs0kXg.png)

**Step4-** Projection or Transform the samples onto the new subspace:

- In the last step, we use the 3x2 dimensional matrix ***W*** that we just computed to transform our samples onto the new subspace via the equation ***y = W′ × x*** where ***W′*** is the *transpose* of the matrix ***W.***

## Pros:

- **Reduced complexity:** Makes data easier to visualize, manage, and interpret by reducing the number of features
- **Improved algorithm performance:** Many machine learning algorithms struggle with high-dimensional data. PCA reduces training time and improves the accuracy of some algorithms by reducing irrelevant features
- **Reduced redundancy:** Eliminates redundant features, focusing on the unique information each piece of data provides. This can be especially helpful when dealing with datasets with a lot of correlated features

## Cons:

- **Information loss:** PCA discards information in the process of dimensionality reduction. There’s a trade-off between the number of features retained and the amount of information preserved
- **Assumes linearity:** PCA works best when the relationships between features are linear. It may not be effective if the data has complex non-linear relationships
- **Interpretability of new features:** The principal components (PCs) created by PCA can be difficult to interpret in the context of the original features

## Python Implementation

```c
import numpy as np
from sklearn.decomposition import PCA

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
pca = PCA(n_components=2)
pca.fit(X)
print(pca.explained_variance_ratio_)
print(pca.singular_values_)
```