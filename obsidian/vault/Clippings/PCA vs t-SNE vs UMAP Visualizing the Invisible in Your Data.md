---
title: "PCA vs t-SNE vs UMAP: Visualizing the Invisible in Your Data"
source: "https://medium.com/@laakhanbukkawar/pca-vs-t-sne-vs-umap-visualizing-the-invisible-in-your-data-92cb2baebdbb"
author:
  - "[[Lakhan Bukkawar]]"
published: 2025-05-05
created: 2026-06-01
description: "More"
tags:
  - "clippings"
---
*See how each technique reveals hidden structure — with real-world cases, code, and interactive visualizations*

> ***“Dimensionality reduction is like giving eyes to a machine — it finally sees the forest, not just the trees.”***

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*oWJqURIB0Z3Y6lmNjp6EYQ.png)

## Why Dimensionality Reduction Matters

Imagine trying to explore a galaxy through a tiny telescope — that’s how machine learning models feel when dealing with raw high-dimensional data. Dimensionality reduction **transforms complex, high-dimensional datasets** into simpler forms, helping both humans and machines discover hidden patterns.

But with so many techniques available, which one should you use?

In this blog, we’ll **compare PCA, t-SNE, and UMAP** in terms of:

- Intuition
- How they work
- Real-world use cases
- Visual examples
- Python implementation
- Pros, cons, and best-fit scenarios

💡 And yes, we’ll wrap it up with a cheat sheet, comparison visuals, and handpicked resources to deepen your understanding.

## 1\. Principal Component Analysis (PCA)

## Intuition

PCA **projects data into a new coordinate system** where the axes (principal components) maximize variance. It’s like rotating your dataset to align it with the directions that capture the most spread.

> *Use PCA when you want* ***speed, interpretability, and compatibility with ML models****.*

### How PCA Works

1. **Standardize** the data
2. **Compute covariance matrix**
3. **Find eigenvectors and eigenvalues**
4. **Project data** onto top-k components

### Real-World Use Cases

- **Finance**: Risk modeling, credit scoring
- **Genomics**: Reducing gene expression features
- **Preprocessing**: Before clustering or modeling

**Python Code**

```c
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import seaborn as sns
import matplotlib.pyplot as plt

iris = load_iris()
X = StandardScaler().fit_transform(iris.data)
y = iris.target

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=iris.target_names[y])
plt.title("PCA on Iris Dataset")
plt.show()
```
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*RqbB7XjLWNMM438XpVecNw.png)

### Pros

- Very fast
- Preserves **global structure**
- ML-friendly

### Cons

- Linear only
- No clustering insights

## 2\. t-SNE (t-distributed Stochastic Neighbor Embedding)

### Intuition

t-SNE maps high-dimensional data into 2D or 3D space, preserving **local neighborhoods** — meaning similar points stay close.

> *Use t-SNE for* ***cluster visualization and exploratory analysis****.*

### How t-SNE Works

1. Compute similarities in high-dim space
2. Model low-dim similarities with Student-t distribution
3. Minimize divergence between both

### Real-World Use Cases

- **Computer Vision**: Visualize CNN embeddings
- **Bioinformatics**: Cell type clustering
- **Analytics**: App behavior segmentation

**Python Code**

```c
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=300)
X_tsne = tsne.fit_transform(X)

sns.scatterplot(x=X_tsne[:, 0], y=X_tsne[:, 1], hue=iris.target_names[y])
plt.title("t-SNE on Iris Dataset")
plt.show()
```
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Db6NxLp7VuOvJi7PJKivlg.png)

### Pros

- Excellent for **visualizing clusters**
- Captures **local structures** well

### Cons

- Computationally expensive
- No inverse transform or ML compatibility
- Sensitive to hyperparameters

## 3\. UMAP (Uniform Manifold Approximation and Projection)

### Intuition

UMAP preserves **both local and some global structure** using graph theory and manifold learning. It’s like t-SNE’s smarter, faster cousin.

> *Use UMAP when you want* ***speed + cluster visualization + scalability****.*

### How UMAP Works

1. Builds a fuzzy graph in high-dim space
2. Optimizes layout in low-dim space
3. Preserves relationships with minimal distortion

### Real-World Use Cases

- **NLP**: Word embedding visualization
- **Medical Imaging**: Feature extraction
- **Marketing**: Customer segmentation

**Python Code**

```c
import umap

umap_model = umap.UMAP(n_components=2, random_state=42)
X_umap = umap_model.fit_transform(X)

sns.scatterplot(x=X_umap[:, 0], y=X_umap[:, 1], hue=iris.target_names[y])
plt.title("UMAP on Iris Dataset")
plt.show()
```
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*6FLmjPzmNXCa3onZJwMObw.png)

### Pros

- Fast, scalable
- Good for both ML and visualization
- Cluster-friendly

### Cons

- Slightly complex to interpret
- Parameters affect output

### Visual Comparison: PCA vs t-SNE vs UMAP

Dataset: Iris — 3 Species

> Each method tells a different story — use the one that suits your goal best.

### Cheat Sheet: When to Use What?

**Decision Tree**

```c
Need dimensionality reduction?
├── Modeling performance ➝ PCA or UMAP
│   └── Interpretability needed? ➝ PCA
├── Visualization?
│   ├── Small dataset ➝ t-SNE
│   └── Large + noisy ➝ UMAP
```

**Summary Table**

```c
| Feature             | PCA     | t-SNE       | UMAP                |
|---------------------|---------|-------------|---------------------|
| Type                | Linear  | Non-linear  | Non-linear          |
| Preserves           | Global  | Local       | Local + some global |
| Speed               | Fast    | Slow        | Fast                |
| Use in ML Models    | ✅ Yes  | ❌ No       | ✅ Yes              |
| Clustering friendly | ❌ No   | ✅ Yes      | ✅ Yes              |
| Interpretability    | ✅ High | ❌ Low      | ❌ Medium           |
| Inverse Transform   | ✅ Yes  | ❌ No       | ❌ No               |
```

**Preprocessing Tips (Don’t Skip!)**

- Always **scale your features** (`StandardScaler` or `MinMaxScaler`)
- **Remove outliers** to avoid skewing distances
- Tune parameters carefully in t-SNE (`perplexity`, `learning_rate`)
- Use **sufficient sample size** in UMAP for meaningful manifolds

## Conclusion

Dimensionality reduction isn’t just a preprocessing step — it’s a **powerful lens** that helps you explore, visualize, and understand complex data.

```c
| Goal                   | Best Tool     |
| ---------------------- | ------------- |
| Speed + Simplicity     | PCA           |
| Cluster Visualization  | t-SNE or UMAP |
| Large Datasets + Speed | UMAP          |
| Interpretability       | PCA           |
```

## Further Reading & Resources

- 📘 [The Illustrated t-SNE by Distill.pub](https://distill.pub/2016/misread-tsne/) — Deep, intuitive visualization
- 🧾 [UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction](https://arxiv.org/abs/1802.03426) — The original research paper
- 🧪 [UMAP GitHub Repo](https://github.com/lmcinnes/umap)
- 🎥 [StatQuest: PCA, t-SNE, and UMAP Explained](https://www.youtube.com/user/joshstarmer) — Simplified explanations with visuals

## Final Thoughts

Dimensionality reduction isn’t just a preprocessing step — it’s a gateway to seeing your data in an entirely new light. Whether you’re simplifying data for modeling or visualizing complex relationships, **PCA**, **t-SNE**, and **UMAP** each offer unique strengths.

PCA brings speed and clarity for linear patterns. t-SNE dives deep into preserving local structures for visualizations. UMAP balances both local and global insights — often making it the go-to for modern applications like NLP and image processing.

Now that you’ve explored their intuition, use cases, and implementation — **which method will you try first in your next project?** Share your thoughts or experiences in the comments! 🚀