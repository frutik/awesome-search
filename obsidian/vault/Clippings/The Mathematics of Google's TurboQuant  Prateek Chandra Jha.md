---
title: "The Mathematics of Google's TurboQuant | Prateek Chandra Jha"
source: "https://prateekchandrajha.github.io/turboquant-math.html"
author:
published:
created: 2026-05-16
description:
tags:
  - "clippings"
---
## The Mathematics of Google's TurboQuant

In March 2026, Google Research published a paper that rattled memory chip stocks and made Cloudflare's CEO call it "Google's DeepSeek moment." The paper is about compressing numbers. Specifically, it describes an algorithm called **TurboQuant** that compresses the key-value cache of large language models to ~3 bits per value — a 6x reduction — with effectively no loss in quality.

What makes this interesting is not the engineering result (impressive as it is) but the mathematics underneath. TurboQuant is a clean demonstration of how three old ideas — random rotations, optimal quantization, and the Johnson-Lindenstrauss lemma — combine into something greater than the sum of their parts.

This post walks through the math. I'll start with a puzzle, then build up each piece of the algorithm, and end with why the result is close to the best anyone can ever do.

## A Puzzle to Start

### The Random Rotation Puzzle

Imagine you have a vector in 1000 dimensions. All of its energy is concentrated in a single coordinate:

$$
\mathbf{v} = \left(\right. 1000 , 0 , 0 , 0 , \ldots , 0 \left.\right) \in \mathbb{R}^{1000}
$$

Now apply a random rotation to this vector — pick a uniformly random orthogonal matrix $Q$ and compute $Q \mathbf{v}$.

**Question:** After the rotation, roughly what does each coordinate of $Q \mathbf{v}$ look like? Are most of them still zero? Are a few of them large? Or does something else happen entirely?

**Bonus:** What probability distribution do the individual coordinates follow?

## The Problem: LLMs Are Drowning in Memory

Large language models like Llama, Gemini, and GPT run on a mechanism called **attention**. Every time the model processes a new token, it computes inner products between the current token's query vector and the key vectors of all previous tokens. The key and value vectors from all past tokens are stored in something called the **KV cache**.

The KV cache grows linearly with context length. For Llama 3.1 70B processing a 128K-token context, the KV cache alone consumes roughly 40 GB of GPU memory — often more than the model weights themselves.

The question is: can we store these vectors at lower precision without breaking the attention computation?

This is a **vector quantization** problem, and it has been studied since Shannon's 1959 source coding theory. The challenge is that naive quantization (just round each number to the nearest low-precision value) introduces errors that accumulate as bias in the attention scores. TurboQuant solves this elegantly.

## The Three-Paper Arc

TurboQuant didn't appear from nowhere. It's the final piece of a research program spanning three papers:

AAAI 2025 — **QJL (Quantized Johnson-Lindenstrauss)**  
Showed that the sign of a random projection preserves enough angular information to debias dot product estimates at a cost of 1 bit per dimension.

AISTATS 2026 — **PolarQuant**  
Showed that randomly rotating a vector makes each coordinate follow a known Beta distribution, enabling precomputed optimal scalar quantizers with zero calibration.

ICLR 2026 — **TurboQuant**  
Combined PolarQuant (rotation + Lloyd-Max quantization) with QJL (1-bit residual correction) to achieve near-optimal distortion with unbiased inner products.

Let's look at each piece.

## Stage 1: PolarQuant — Rotation Makes Everything Predictable

Consider a vector $\mathbf{x} \in \mathbb{R}^{d}$ that we want to quantize. In a KV cache, $d$ is the head dimension (typically 64–128). The vector could have any shape — some coordinates large, others small, the distribution varying from token to token.

PolarQuant's insight is to apply a random orthogonal rotation first:

$$
\overset{\sim}{\mathbf{x}} = Q \mathbf{x}
$$

where $Q \in \mathbb{R}^{d \times d}$ is a random orthogonal matrix (generated once, shared across all vectors). This is exactly the setup from our puzzle.

### Why does rotation help?

After rotation, each coordinate $\overset{\sim}{x}_{i}$ of the transformed vector follows a distribution that depends only on $\parallel \mathbf{x} \parallel$ and $d$, not on the direction of $\mathbf{x}$. Specifically:

$$
\overset{\sim}{x}_{i} = \parallel \mathbf{x} \parallel \cdot z_{i}
$$

where $z_{i}$ is the $i$ -th coordinate of a uniformly random unit vector in $\mathbb{R}^{d}$. This coordinate follows a **shifted and scaled Beta distribution**:

$$
z_{i}^{2} sim Beta \left(\right. \frac{1}{2} , \frac{d - 1}{2} \left.\right)
$$

For large $d$, the central limit theorem kicks in and $z_{i} \approx \mathcal{N} \left(\right. 0 , 1 / d \left.\right)$. Moreover, distinct coordinates become nearly independent.

**The key consequence:** Because the post-rotation distribution is known analytically and does not depend on the input data, we can precompute the optimal quantizer once, before seeing any data. This is what makes TurboQuant *data-oblivious* — no calibration set, no fine-tuning, no codebook training.

### The Lloyd-Max Quantizer

Given a known probability distribution $p \left(\right. z \left.\right)$ and a budget of $b$ bits (giving $2^{b}$ possible output levels), the **Lloyd-Max quantizer** is the scalar quantizer that minimizes mean squared error (MSE).

It works by solving a one-dimensional optimization: partition the real line into $2^{b}$ intervals and assign a representative value to each interval, chosen to minimize:

$$
MSE = \int_{- \infty}^{\infty} \left(\right. z - Q_{b} \left(\right. z \left.\right) \left.\right)^{2} p \left(\right. z \left.\right) d z
$$

where $Q_{b} \left(\right. z \left.\right)$ maps $z$ to its nearest representative. The optimal partition boundaries and representatives satisfy a pair of necessary conditions (essentially: boundaries are midpoints of adjacent representatives, and representatives are conditional means within their intervals). These can be solved numerically by alternating between the two conditions — which is exactly Lloyd's algorithm (also known as k-means in one dimension).

Because the Beta distribution is known, PolarQuant precomputes the Lloyd-Max quantizer for each target bitwidth once. At runtime, quantizing a coordinate is a table lookup.

This is easier to understand with examples. Let's build up from the simplest case.

#### Example: 1-bit quantizer for a uniform distribution

Suppose our values are drawn from a uniform distribution on $\left[\right. - 1 , 1 \left]\right.$, and we have 1 bit — just 2 possible output levels. Where should we place them?

Lloyd-Max says: partition $\left[\right. - 1 , 1 \left]\right.$ into two intervals, and set each representative to the conditional mean within its interval. By symmetry, the boundary is at 0:

\-1 0 +1 |------\[--x--\]--|--\[--x--\]------| r₁=-0.5 r₂=+0.5 Interval 1: \[-1, 0) → output -0.5 Interval 2: \[0, +1\] → output +0.5

The representative for $\left[\right. - 1 , 0 \left.\right)$ is $\mathbb{E} \left[\right. z \mid z \in \left[\right. - 1 , 0 \left.\right) \left]\right. = - 0.5$. Similarly for the other half. Any value in $\left[\right. - 1 , 0 \left.\right)$ gets mapped to $- 0.5$; any value in $\left[\right. 0 , 1 \left]\right.$ gets mapped to $+ 0.5$.

The MSE is $\mathbb{E} \left[\right. \left(\right. z - Q \left(\right. z \left.\right) \left.\right)^{2} \left]\right. = \frac{1}{12} \approx 0.083$. (Each half contributes the variance of a uniform on an interval of width 1, which is $1 / 12$.)

#### Example: 2-bit quantizer for a uniform distribution

Now we have 2 bits — 4 output levels. For the uniform distribution on $\left[\right. - 1 , 1 \left]\right.$, Lloyd-Max splits into 4 equal intervals:

\-1 -0.5 0 +0.5 +1 |--\[x\]---|---\[x\]---|---\[x\]---|---\[x\]--| r₁=-0.75 r₂=-0.25 r₃=+0.25 r₄=+0.75 Interval 1: \[-1, -0.5) → output -0.75 Interval 2: \[-0.5, 0) → output -0.25 Interval 3: \[0, +0.5) → output +0.25 Interval 4: \[0.5, +1\] → output +0.75

MSE = $\frac{1}{48} \approx 0.021$. Going from 1 bit to 2 bits cut the MSE by 4x. This is the $4^{- b}$ scaling: each extra bit reduces MSE by a factor of 4 (for well-behaved distributions).

#### Example: 2-bit quantizer for a Gaussian — non-uniform intervals

Now the values follow a standard normal $\mathcal{N} \left(\right. 0 , 1 \left.\right)$ instead of a uniform. Most values cluster near 0, with rare outliers. If we used equal-width intervals (like above), we'd waste two output levels on the tails where almost no data lives.

Lloyd-Max adapts: it places narrower intervals where the density is high (near 0) and wider intervals in the sparse tails:

density: \_\_\_ / \\ / \\ / \\ \_\_/ \\\_\_ \_\_\_\_/ \\\_\_\_\_ ---|-----|---------|---------|-----|--- -∞ -1.51 -0.45 +0.45 +1.51 +∞ Interval 1: (-∞, -0.9816) → output -1.51 Interval 2: \[-0.9816, 0) → output -0.45 Interval 3: \[0, +0.9816) → output +0.45 Interval 4: \[+0.9816, +∞) → output +1.51

Notice the asymmetry in interval widths: the inner intervals (covering the dense center) are narrower ($\approx 0.98$ wide) than the outer intervals (stretching to infinity). This is *not* something you can get from simple "round to nearest" quantization — it specifically accounts for where the data actually lives.

The MSE for this optimal 2-bit Gaussian quantizer is about 0.2356, compared to the variance of 1.0 — so we capture about 76% of the signal with just 4 levels.

The representatives ($\pm 0.45$, $\pm 1.51$) and boundaries ($\pm 0.98$) are computed once by running Lloyd's algorithm on the known Gaussian density. They never change.

#### Example: What PolarQuant actually precomputes

In TurboQuant, after rotation, each coordinate follows approximately $\mathcal{N} \left(\right. 0 , 1 / d \left.\right)$. Rescaling by $\parallel \mathbf{x} \parallel$, the distribution is known. PolarQuant precomputes a Lloyd-Max quantizer for this distribution at each bitwidth.

For a 3-bit quantizer ($2^{3} = 8$ levels) on a standard Gaussian, the precomputed table looks roughly like:

Level Interval Representative Probability ----- -------- -------------- ----------- 0 (-∞, -1.748) -2.152 3.6% 1 \[-1.748, -1.050) -1.344 6.4% 2 \[-1.050, -0.501) -0.756 12.7% 3 \[-0.501, 0) -0.245 19.2% 4 \[ 0, +0.501) +0.245 19.2% 5 \[+0.501, +1.050) +0.756 12.7% 6 \[+1.050, +1.748) +1.344 6.4% 7 \[+1.748, +∞) +2.152 3.6%

At runtime, quantizing one coordinate means: compare it against 7 boundaries, pick the matching interval, store a 3-bit index (0–7). Dequantizing means: look up the representative from a table of 8 values. No floating-point arithmetic, no per-vector statistics, no calibration. The boundaries and representatives are baked in at compile time.

This is what makes TurboQuant fast: the entire quantization step is 7 comparisons and a table index per coordinate.

### Eliminating normalization overhead

A subtle but important advantage: traditional quantization schemes (like min-max or absmax) need to store per-block scale factors, typically adding 1–2 extra bits per coordinate of overhead. PolarQuant eliminates this entirely. Since the distribution after rotation is fixed, the quantizer boundaries are fixed. No per-vector metadata is needed.

The only thing we need to store alongside the quantized coordinates is $\parallel \mathbf{x} \parallel$ (a single scalar per vector) to reconstruct the scale. This is negligible overhead.

## Stage 2: QJL — Fixing the Bias with One Bit

Stage 1 gives us excellent MSE. But there's a problem that MSE doesn't capture.

In attention, we don't care about reconstructing the vector itself — we care about **inner products**. The attention score between a query $\mathbf{q}$ and a key $\mathbf{k}$ is $\langle \mathbf{q} , \mathbf{k} \rangle$. If we quantize $\mathbf{k}$ to $\hat{\mathbf{k}}$, we need $\langle \mathbf{q} , \hat{\mathbf{k}} \rangle \approx \langle \mathbf{q} , \mathbf{k} \rangle$.

The problem is that MSE-optimal quantizers introduce **systematic bias** in inner product estimates. The quantization error $\mathbf{e} = \mathbf{k} - \hat{\mathbf{k}}$ is correlated with $\hat{\mathbf{k}}$, which means:

$$
\mathbb{E} \left[\right. \langle \mathbf{q} , \hat{\mathbf{k}} \rangle \left]\right. \neq \langle \mathbf{q} , \mathbf{k} \rangle
$$

This bias accumulates across tokens in the attention softmax, silently degrading output quality. TurboQuant fixes this with a 1-bit correction based on the **Johnson-Lindenstrauss lemma**.

### The Johnson-Lindenstrauss Lemma

The JL lemma (1984) is one of the most useful results in high-dimensional geometry. It says:

**JL Lemma:** For any set of $n$ points in $\mathbb{R}^{d}$, there exists a linear map $A : \mathbb{R}^{d} \rightarrow \mathbb{R}^{k}$ with $k = O \left(\right. log ⁡ n / \epsilon^{2} \left.\right)$ that preserves all pairwise distances within a factor of $\left(\right. 1 \pm \epsilon \left.\right)$. Moreover, a random Gaussian matrix works with high probability.

In other words: random projections preserve geometry, even when you're projecting into a much lower-dimensional space.

### How QJL corrects the bias

Let $\mathbf{e} = \mathbf{k} - \hat{\mathbf{k}}$ be the residual error from Stage 1. We want to estimate $\langle \mathbf{q} , \mathbf{e} \rangle$ — the part of the inner product lost to quantization — so we can add it back. But we can't store $\mathbf{e}$ itself (that would defeat the purpose of compression). QJL stores a 1-bit sketch of $\mathbf{e}$ instead.

### Step 1: Storing the sketch (1 bit per projection)

Fix $m$ random Gaussian vectors $\mathbf{g}_{1} , \ldots , \mathbf{g}_{m} \in \mathbb{R}^{d}$, drawn once and shared across all keys. For each key's residual $\mathbf{e}$, store:

$$
s_{i} = sign \left(\right. \langle \mathbf{g}_{i} , \mathbf{e} \rangle \left.\right) \in \left{\right. - 1 , + 1 \left.\right} \text{for } i = 1 , \ldots , m
$$

Each $s_{i}$ is a single bit. The inner product $\langle \mathbf{g}_{i} , \mathbf{e} \rangle$ is a real number, but we only keep its sign. This feels like throwing away almost all the information — how can a sign bit help estimate an inner product?

### Step 2: Where π comes from — the sign-angle identity

The key mathematical fact is a classical result about Gaussian random projections. For any two fixed vectors $\mathbf{a} , \mathbf{b} \in \mathbb{R}^{d}$ and a random Gaussian vector $\mathbf{g} sim \mathcal{N} \left(\right. 0 , I_{d} \left.\right)$:

$$
\mathbb{E} \left[\right. sign \left(\right. \langle \mathbf{g} , \mathbf{a} \rangle \left.\right) \cdot \langle \mathbf{g} , \mathbf{b} \rangle \left]\right. = \sqrt{\frac{2}{\pi}} \parallel \mathbf{a} \parallel cos ⁡ \theta
$$

Wait — let me derive this from scratch so the $\pi$ doesn't feel like magic.

Consider the simpler 1D case first. Let $g sim \mathcal{N} \left(\right. 0 , 1 \left.\right)$. What is $\mathbb{E} \left[\right. sign \left(\right. g \left.\right) \cdot g \left]\right.$?

$$
\mathbb{E} \left[\right. sign \left(\right. g \left.\right) \cdot g \left]\right. = \mathbb{E} \left[\right. \left|\right. g \left|\right. \left]\right. = \int_{- \infty}^{\infty} \left|\right. g \left|\right. \cdot \frac{1}{\sqrt{2 \pi}} e^{- g^{2} / 2} d g = 2 \int_{0}^{\infty} g \cdot \frac{1}{\sqrt{2 \pi}} e^{- g^{2} / 2} d g
$$

The integral $\int_{0}^{\infty} g e^{- g^{2} / 2} d g = 1$ (substitute $u = g^{2} / 2$), so:

$$
\mathbb{E} \left[\right. \left|\right. g \left|\right. \left]\right. = \frac{2}{\sqrt{2 \pi}} = \sqrt{\frac{2}{\pi}}
$$

**That's where the $\sqrt{2 / \pi}$ comes from** — it's the mean of the half-normal distribution. It arises because we're taking the absolute value (or equivalently, multiplying by the sign) of a Gaussian.

Now generalize to $\mathbb{R}^{d}$. Let $\mathbf{g} sim \mathcal{N} \left(\right. 0 , I_{d} \left.\right)$, and let $\theta$ be the angle between fixed vectors $\mathbf{e}$ and $\mathbf{q}$. We can decompose $\mathbf{g}$ into a component along $\mathbf{e}$ and a component perpendicular to $\mathbf{e}$. The projection $\langle \mathbf{g} , \mathbf{e} \rangle / \parallel \mathbf{e} \parallel$ is a scalar Gaussian, and the sign of $\langle \mathbf{g} , \mathbf{e} \rangle$ depends only on this component. Meanwhile, $\langle \mathbf{g} , \mathbf{q} \rangle$ decomposes as:

$$
\langle \mathbf{g} , \mathbf{q} \rangle = \underset{\text{component along } \mathbf{e}}{\underbrace{\langle \mathbf{g} , \mathbf{q}_{\parallel} \rangle}} + \underset{\text{component } \bot \text{to } \mathbf{e}}{\underbrace{\langle \mathbf{g} , \mathbf{q}_{\bot} \rangle}}
$$

where $\mathbf{q}_{\parallel} = \frac{\langle \mathbf{q} , \mathbf{e} \rangle}{\parallel \mathbf{e} \parallel^{2}} \mathbf{e}$ is the projection of $\mathbf{q}$ onto $\mathbf{e}$, and $\mathbf{q}_{\bot} = \mathbf{q} - \mathbf{q}_{\parallel}$.

The perpendicular part $\langle \mathbf{g} , \mathbf{q}_{\bot} \rangle$ is independent of $sign \left(\right. \langle \mathbf{g} , \mathbf{e} \rangle \left.\right)$ (because $\mathbf{q}_{\bot}$ is orthogonal to $\mathbf{e}$, so this projection involves different Gaussian components). Therefore its contribution vanishes in expectation:

$$
\mathbb{E} \left[\right. sign \left(\right. \langle \mathbf{g} , \mathbf{e} \rangle \left.\right) \cdot \langle \mathbf{g} , \mathbf{q}_{\bot} \rangle \left]\right. = 0
$$

For the parallel part, let $\alpha = \langle \mathbf{g} , \mathbf{e} \rangle / \parallel \mathbf{e} \parallel$ (a standard Gaussian scalar). Then:

$$
\langle \mathbf{g} , \mathbf{q}_{\parallel} \rangle = \frac{\langle \mathbf{q} , \mathbf{e} \rangle}{\parallel \mathbf{e} \parallel} \cdot \alpha
$$

and:

$$
\mathbb{E} \left[\right. sign \left(\right. \langle \mathbf{g} , \mathbf{e} \rangle \left.\right) \cdot \langle \mathbf{g} , \mathbf{q}_{\parallel} \rangle \left]\right. = \frac{\langle \mathbf{q} , \mathbf{e} \rangle}{\parallel \mathbf{e} \parallel} \cdot \mathbb{E} \left[\right. sign \left(\right. \alpha \left.\right) \cdot \alpha \left]\right. = \frac{\langle \mathbf{q} , \mathbf{e} \rangle}{\parallel \mathbf{e} \parallel} \cdot \sqrt{\frac{2}{\pi}}
$$

Combining the parallel and perpendicular parts:

**The sign-projection identity:** 
$$
\mathbb{E} \left[\right. sign \left(\right. \langle \mathbf{g} , \mathbf{e} \rangle \left.\right) \cdot \langle \mathbf{g} , \mathbf{q} \rangle \left]\right. = \sqrt{\frac{2}{\pi}} \cdot \frac{\langle \mathbf{q} , \mathbf{e} \rangle}{\parallel \mathbf{e} \parallel}
$$
 This holds for any fixed $\mathbf{e} , \mathbf{q}$ and random $\mathbf{g} sim \mathcal{N} \left(\right. 0 , I \left.\right)$. The $\sqrt{2 / \pi}$ is the mean absolute value of a standard Gaussian.

### Step 3: Building the unbiased estimator

The identity above tells us that $sign \left(\right. \langle \mathbf{g} , \mathbf{e} \rangle \left.\right) \cdot \langle \mathbf{g} , \mathbf{q} \rangle$ has expected value proportional to $\langle \mathbf{q} , \mathbf{e} \rangle$, but scaled by a factor of $\sqrt{2 / \pi} / \parallel \mathbf{e} \parallel$. To get an unbiased estimator of $\langle \mathbf{q} , \mathbf{e} \rangle$ itself, we need to undo this scaling.

If we knew $\parallel \mathbf{e} \parallel$, the estimator from a single projection would be:

$$
\hat{T}_{i} = \sqrt{\frac{\pi}{2}} \cdot \parallel \mathbf{e} \parallel \cdot s_{i} \cdot \langle \mathbf{g}_{i} , \mathbf{q} \rangle
$$

and by the identity: $\mathbb{E} \left[\right. \hat{T}_{i} \left]\right. = \sqrt{\frac{\pi}{2}} \cdot \parallel \mathbf{e} \parallel \cdot \sqrt{\frac{2}{\pi}} \cdot \frac{\langle \mathbf{q} , \mathbf{e} \rangle}{\parallel \mathbf{e} \parallel} = \langle \mathbf{q} , \mathbf{e} \rangle$. Unbiased.

In practice, TurboQuant stores $\parallel \mathbf{e} \parallel$ alongside the sketch (it's a single scalar per vector, negligible overhead). Averaging over $m$ independent projections reduces variance:

$$
\hat{\langle \mathbf{q} , \mathbf{e} \rangle} = \frac{1}{m} \sum_{i = 1}^{m} \sqrt{\frac{\pi}{2}} \cdot \parallel \mathbf{e} \parallel \cdot s_{i} \cdot \langle \mathbf{g}_{i} , \mathbf{q} \rangle
$$

This is sometimes written more compactly as $\frac{\pi}{2 m} \sum s_{i} \langle \mathbf{g}_{i} , \mathbf{q} \rangle$ (absorbing $\parallel \mathbf{e} \parallel$ into the normalization of $\mathbf{g}_{i}$), which is the formula you see in the paper.

### Step 4: Proving unbiasedness explicitly

Let's verify this end to end. The estimator for the full inner product is:

$$
\hat{\langle \mathbf{q} , \mathbf{k} \rangle} = \underset{\text{from Stage 1}}{\underbrace{\langle \mathbf{q} , \hat{\mathbf{k}} \rangle}} + \underset{\text{QJL correction}}{\underbrace{\hat{\langle \mathbf{q} , \mathbf{e} \rangle}}}
$$

Taking expectations (over the randomness of the Gaussian vectors $\mathbf{g}_{i}$):

$$
\mathbb{E} \left[\right. \hat{\langle \mathbf{q} , \mathbf{k} \rangle} \left]\right. = \langle \mathbf{q} , \hat{\mathbf{k}} \rangle + \mathbb{E} \left[\right. \hat{\langle \mathbf{q} , \mathbf{e} \rangle} \left]\right. = \langle \mathbf{q} , \hat{\mathbf{k}} \rangle + \langle \mathbf{q} , \mathbf{e} \rangle
$$

Now use $\mathbf{e} = \mathbf{k} - \hat{\mathbf{k}}$:

$$
= \langle \mathbf{q} , \hat{\mathbf{k}} \rangle + \langle \mathbf{q} , \mathbf{k} - \hat{\mathbf{k}} \rangle = \langle \mathbf{q} , \hat{\mathbf{k}} \rangle + \langle \mathbf{q} , \mathbf{k} \rangle - \langle \mathbf{q} , \hat{\mathbf{k}} \rangle = \langle \mathbf{q} , \mathbf{k} \rangle
$$

The $\langle \mathbf{q} , \hat{\mathbf{k}} \rangle$ terms cancel perfectly. The estimator recovers the true inner product in expectation, regardless of how large the quantization error $\mathbf{e}$ is.

### Step 5: A concrete numerical example

#### Example: QJL correction in 2D

Let's trace through this with small numbers to see it working.

**Setup:** Dimension $d = 2$. Suppose:

- True key: $\mathbf{k} = \left(\right. 3.0 , 4.0 \left.\right)$
- Quantized key: $\hat{\mathbf{k}} = \left(\right. 2.5 , 4.5 \left.\right)$ (Stage 1 output)
- Residual: $\mathbf{e} = \mathbf{k} - \hat{\mathbf{k}} = \left(\right. 0.5 , - 0.5 \left.\right)$
- Query: $\mathbf{q} = \left(\right. 1.0 , 2.0 \left.\right)$

**True inner product:** $\langle \mathbf{q} , \mathbf{k} \rangle = 1 \cdot 3 + 2 \cdot 4 = 11.0$

**Naive (Stage 1 only):** $\langle \mathbf{q} , \hat{\mathbf{k}} \rangle = 1 \cdot 2.5 + 2 \cdot 4.5 = 11.5$

**Error without correction:** $11.5 - 11.0 = 0.5$ (this is the bias)

**Lost inner product:** $\langle \mathbf{q} , \mathbf{e} \rangle = 1 \cdot 0.5 + 2 \cdot \left(\right. - 0.5 \left.\right) = - 0.5$

**QJL correction with $m = 3$ projections:**

Draw 3 random Gaussian vectors and compute the sketch:

- $\mathbf{g}_{1} = \left(\right. 0.8 , - 0.3 \left.\right)$: $\langle \mathbf{g}_{1} , \mathbf{e} \rangle = 0.4 + 0.15 = 0.55$, so $s_{1} = + 1$
- $\mathbf{g}_{2} = \left(\right. - 1.2 , 0.7 \left.\right)$: $\langle \mathbf{g}_{2} , \mathbf{e} \rangle = - 0.6 - 0.35 = - 0.95$, so $s_{2} = - 1$
- $\mathbf{g}_{3} = \left(\right. 0.1 , 1.5 \left.\right)$: $\langle \mathbf{g}_{3} , \mathbf{e} \rangle = 0.05 - 0.75 = - 0.70$, so $s_{3} = - 1$

Store only: $s_{1} = + 1 , s_{2} = - 1 , s_{3} = - 1$ and $\parallel \mathbf{e} \parallel = \sqrt{0.25 + 0.25} = \frac{1}{\sqrt{2}} \approx 0.707$.

At query time, compute $\langle \mathbf{g}_{i} , \mathbf{q} \rangle$ for each:

- $\langle \mathbf{g}_{1} , \mathbf{q} \rangle = 0.8 + \left(\right. - 0.6 \left.\right) = 0.2$
- $\langle \mathbf{g}_{2} , \mathbf{q} \rangle = - 1.2 + 1.4 = 0.2$
- $\langle \mathbf{g}_{3} , \mathbf{q} \rangle = 0.1 + 3.0 = 3.1$

QJL estimate of $\langle \mathbf{q} , \mathbf{e} \rangle$:

$$
\hat{\langle \mathbf{q} , \mathbf{e} \rangle} = \frac{\sqrt{\pi / 2} \cdot \parallel \mathbf{e} \parallel}{m} \underset{i}{\sum} s_{i} \langle \mathbf{g}_{i} , \mathbf{q} \rangle = \frac{1.253 \cdot 0.707}{3} \left[\right. \left(\right. + 1 \left.\right) \left(\right. 0.2 \left.\right) + \left(\right. - 1 \left.\right) \left(\right. 0.2 \left.\right) + \left(\right. - 1 \left.\right) \left(\right. 3.1 \left.\right) \left]\right.
$$
 
$$
= \frac{0.886}{3} \cdot \left(\right. 0.2 - 0.2 - 3.1 \left.\right) = 0.295 \times \left(\right. - 3.1 \left.\right) = - 0.915
$$

**Corrected estimate:** $11.5 + \left(\right. - 0.915 \left.\right) = 10.585$

**True value:** $11.0$

The correction moved us from an error of $+ 0.5$ to an error of $- 0.415$. On this single draw, the correction overshot — but that's because $m = 3$ is very small and we got unlucky with $\mathbf{g}_{3}$. **In expectation** (averaged over many random draws of the $\mathbf{g}_{i}$), the estimate would be exactly 11.0. With a realistic $m$ (say 64 or 128, matching the head dimension), the variance shrinks dramatically and the estimate would be very close to 11.0 on any single draw.

### Step 6: Why the two stages complement each other

Now we can see precisely how the two stages work together:

- **Stage 1 (PolarQuant)** makes $\parallel \mathbf{e} \parallel$ small. The better the Lloyd-Max quantizer, the smaller the residual. This directly reduces the *variance* of the QJL estimator (which scales with $\parallel \mathbf{e} \parallel^{2}$).
- **Stage 2 (QJL)** makes the estimate unbiased. No matter how large or small $\mathbf{e}$ is, the correction recovers the true inner product in expectation.

Without Stage 1, the residual would be large and the QJL estimator would have high variance. Without Stage 2, the quantized inner product would have low variance but persistent bias. Together: low variance *and* zero bias.

The total inner product estimate is:

$$
\langle \mathbf{q} , \mathbf{k} \rangle \approx \langle \mathbf{q} , \hat{\mathbf{k}} \rangle + \frac{1}{m} \sum_{i = 1}^{m} \sqrt{\frac{\pi}{2}} \cdot \parallel \mathbf{e} \parallel \cdot s_{i} \cdot \langle \mathbf{g}_{i} , \mathbf{q} \rangle
$$

## The Full TurboQuant Pipeline

Input vector x ∈ ℝᵈ | v \[Random Rotation\] x̃ = Qx | v \[Lloyd-Max Quantize\] x̂ = decode(quantize(x̃))... b bits/coord | v \[Compute Residual\] e = x̃ - x̂ | v \[QJL 1-bit Sketch\] sᵢ = sign(⟨gᵢ, e⟩)... 1 bit/coord | v Store: b-bit codes + 1-bit sketch + ∥x∥ At query time: ⟨q, k⟩ ≈ ⟨q, k̂⟩ + (π/2m) Σ sᵢ · ⟨gᵢ, q⟩

TurboQuant compresses each KV vector in two stages: rotation + scalar quantization (PolarQuant), then 1-bit residual correction (QJL).

The total storage per coordinate is $b + 1$ bits (e.g., 3 bits PolarQuant + 1 bit QJL = 4 bits total, compared to 16 bits for FP16). This gives the 4–6x memory reduction.

## How Good Is This? The Information-Theoretic Limit

Now for the punchline. How close is TurboQuant to the best possible?

Shannon's **rate-distortion theory** provides a hard lower bound: for any $b$ -bit quantizer operating on unit-norm vectors in $\mathbb{R}^{d}$, the minimum achievable MSE scales as:

$$
MSE_{min} \geq C \cdot 4^{- b}
$$

for some constant $C$. No quantizer — no matter how clever, how much data it sees, or how much computation it uses — can beat this bound.

The TurboQuant paper (Theorem 3 in [arXiv:2504.19874](https://arxiv.org/abs/2504.19874)) proves that TurboQuant achieves:

$$
MSE_{TurboQuant} \leq \frac{\sqrt{3 \pi}}{2} \cdot 4^{- b} \approx 2.7 \cdot 4^{- b}
$$

TurboQuant is within a factor of **~2.7** of the information-theoretic limit at every bitwidth.

This factor is constant — it does not grow with $d$ or $b$.

To put this in perspective: no future algorithm can improve on TurboQuant by more than 2.7x in MSE, regardless of approach. The remaining gap is between the Lloyd-Max scalar quantizer (optimal for scalar quantization of a known distribution) and the Shannon bound for full vector quantization (which requires exponential codebook searches in theory).

### Inner product guarantee

For the inner product estimator (which is what attention actually uses), TurboQuant provides:

- **Unbiased:** $\mathbb{E} \left[\right. \langle \mathbf{q} , \hat{\mathbf{k}} \rangle_{TQ} \left]\right. = \langle \mathbf{q} , \mathbf{k} \rangle$
- **Variance bound:** $Var \left[\right. \langle \mathbf{q} , \hat{\mathbf{k}} \rangle_{TQ} \left]\right. \leq \frac{\sqrt{3 \pi}}{2} \cdot \frac{\parallel \mathbf{q} \parallel^{2}}{d} \cdot 4^{- b}$

The variance shrinks exponentially with the bit budget and inversely with the dimension. For typical LLM head dimensions ($d = 128$) and 3–4 bit quantization, this variance is tiny.

## What This Looks Like in Practice

| Configuration | Bits per value | KV cache size (Llama 70B, 128K ctx) | Quality |
| --- | --- | --- | --- |
| FP16 (baseline) | 16 | ~40 GB | Full |
| TurboQuant 4-bit | 4 | ~10 GB | Matches FP16 |
| TurboQuant 3.5-bit | 3.5 | ~8.75 GB | Quality-neutral |
| TurboQuant 3-bit | 3 | ~7.5 GB | Near quality-neutral |
| TurboQuant 2.5-bit | 2.5 | ~6.25 GB | Marginal degradation |

At 4-bit precision, TurboQuant also delivers up to 8x speedup for attention logit computation on H100 GPUs, since lower-precision arithmetic is faster.

When benchmarked on long-context tasks (LongBench, Needle-in-a-Haystack, RULER), 3.5-bit TurboQuant is statistically indistinguishable from FP16. The algorithm achieves this without any training, fine-tuning, or calibration data.

## The Deeper Puzzle: Why Is This So Close to Optimal?

The factor of 2.7 deserves a closer look. Where does it come from, and why can't we close the gap?

The gap exists because TurboQuant uses **scalar quantization** (quantizing each coordinate independently) rather than **vector quantization** (quantizing all coordinates jointly). Scalar quantization is fast — $O \left(\right. d \left.\right)$ per vector — but it treats each coordinate in isolation, missing correlations between coordinates.

Full vector quantization could, in theory, exploit these correlations to achieve lower distortion. But it requires a codebook of size $2^{b d}$ and search time exponential in $d$. For $d = 128$ and $b = 3$, that's $2^{384}$ codewords — a number larger than the atoms in the observable universe.

### A Question to Sit With

The random rotation in PolarQuant makes coordinates nearly independent in high dimensions. But "nearly" isn't "exactly." There are residual correlations that the scalar quantizer ignores.

Is there a tractable quantization scheme — one that runs in polynomial time — that could exploit these residual correlations to close the 2.7x gap? Or is there a computational lower bound that says this gap is inherent for efficient algorithms?

As far as I know, this question is open.

## Why This Matters Beyond LLMs

TurboQuant is framed as a KV cache trick, but the mathematics applies to any setting where you need to store high-dimensional vectors compactly while preserving inner products:

- **Vector databases** (Pinecone, Weaviate, etc.): similarity search at lower memory cost
- **Embedding storage**: compress sentence/image embeddings for retrieval
- **Streaming quantization**: the algorithm is online — each vector is quantized independently with no look-ahead, making it suitable for real-time applications
- **Federated learning**: compress gradient updates for communication-efficient training

The data-oblivious property is particularly valuable: you don't need to retrain or recalibrate when the data distribution shifts.

## What's Left on the Table

TurboQuant is close to optimal for compressing the data as-is. But the authors note that most future gains in LLM memory efficiency will likely come from changing what data needs to be stored in the first place:

- **Multi-query attention / grouped-query attention:** share key-value heads across query heads, reducing the number of vectors stored
- **Sliding window attention:** don't store the full context, just a recent window
- **Architectural innovations:** models designed from the start for efficient KV storage

Compression is approaching the theoretical wall. Architecture is where the headroom is.

## Summary

TurboQuant combines three clean mathematical ideas:

1. **Random rotation** makes every coordinate look the same (PolarQuant insight).
2. **Lloyd-Max quantization** exploits the known distribution to minimize MSE with zero calibration.
3. **1-bit JL sketch** of the residual eliminates inner product bias (QJL insight).

The result is within 2.7x of the information-theoretic limit, requires no training data, and runs fast enough for real-time inference. It's a nice example of how theoretical tools from high-dimensional geometry (JL lemma), information theory (rate-distortion bounds), and signal processing (Lloyd-Max quantization) combine to solve a practical engineering problem.

Paper: [arXiv:2504.19874](https://arxiv.org/abs/2504.19874) — Zandieh, Daliri, Hadian, Mirrokni (2025). Accepted at ICLR 2026.

## Further Reading

- [Google Research blog post](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/) on TurboQuant
- [TurboQuant paper](https://arxiv.org/abs/2504.19874) (arXiv:2504.19874)
- [Johnson-Lindenstrauss lemma](https://en.wikipedia.org/wiki/Johnson%E2%80%93Lindenstrauss_lemma) (Wikipedia)
- [Lloyd's algorithm / k-means](https://en.wikipedia.org/wiki/Lloyd%27s_algorithm) (Wikipedia)
- [Rate-distortion theory](https://en.wikipedia.org/wiki/Rate%E2%80%93distortion_theory) (Wikipedia)

---

## Appendix: Mathematical Background

This blog uses several probability distributions and their interrelationships. If you're rusty on any of them, this appendix walks through each one from scratch with worked examples that connect directly to the arguments above.

## A.1 — The Chi-Squared Distribution

**Definition.** If $g_{1} , g_{2} , \ldots , g_{k}$ are independent standard normal random variables ($g_{i} sim \mathcal{N} \left(\right. 0 , 1 \left.\right)$), then the sum of their squares 
$$
X = g_{1}^{2} + g_{2}^{2} + \hdots + g_{k}^{2}
$$
 follows a **chi-squared distribution with $k$ degrees of freedom**, written $X sim \chi^{2} \left(\right. k \left.\right)$.

**Key properties:**

- Mean: $\mathbb{E} \left[\right. X \left]\right. = k$
- Variance: $Var \left(\right. X \left.\right) = 2 k$
- The PDF is $f \left(\right. x \left.\right) = \frac{1}{2^{k / 2} \Gamma \left(\right. k / 2 \left.\right)} x^{k / 2 - 1} e^{- x / 2}$ for $x > 0$.
- Additive: if $X sim \chi^{2} \left(\right. a \left.\right)$ and $Y sim \chi^{2} \left(\right. b \left.\right)$ are independent, then $X + Y sim \chi^{2} \left(\right. a + b \left.\right)$.

**Special case used in this blog:** A single squared Gaussian $g^{2}$ where $g sim \mathcal{N} \left(\right. 0 , 1 \left.\right)$ is $\chi^{2} \left(\right. 1 \left.\right)$. Its mean is 1 and its variance is 2. This is the building block for everything that follows.

#### Worked Example A.1: Sum of squared Gaussians

*Problem:* Let $g_{1} , \ldots , g_{1000} sim \mathcal{N} \left(\right. 0 , 1 \left.\right)$ independently. What is the distribution of $S = \sum_{i = 1}^{1000} g_{i}^{2}$? What are its mean and standard deviation? How tightly is it concentrated?

*Solution:*

- $S sim \chi^{2} \left(\right. 1000 \left.\right)$
- $\mathbb{E} \left[\right. S \left]\right. = 1000$
- $Var \left(\right. S \left.\right) = 2 \times 1000 = 2000$, so $SD \left(\right. S \left.\right) = \sqrt{2000} \approx 44.7$
- Coefficient of variation: $SD / Mean = 44.7 / 1000 \approx 0.045$

The relative fluctuation is under 5%. This is why, in Step 5 of the puzzle solution, we could approximate $\sqrt{\sum g_{j}^{2}} \approx \sqrt{d}$ — the sum $\sum g_{j}^{2}$ is tightly concentrated around its mean $d = 1000$.

#### Worked Example A.2: Moments of χ2(1)

*Problem:* If $X sim \chi^{2} \left(\right. 1 \left.\right)$ (i.e., $X = g^{2}$ for $g sim \mathcal{N} \left(\right. 0 , 1 \left.\right)$), compute $\mathbb{E} \left[\right. X \left]\right.$, $\mathbb{E} \left[\right. X^{2} \left]\right.$, and $Var \left(\right. X \left.\right)$.

*Solution:*

- $\mathbb{E} \left[\right. X \left]\right. = \mathbb{E} \left[\right. g^{2} \left]\right. = 1$ (since $g$ has mean 0 and variance 1).
- $\mathbb{E} \left[\right. X^{2} \left]\right. = \mathbb{E} \left[\right. g^{4} \left]\right.$. For a standard normal, $\mathbb{E} \left[\right. g^{4} \left]\right. = 3$ (this is the fourth moment, equal to $3 ! ! = 3 \cdot 1 = 3$).
- $Var \left(\right. X \left.\right) = \mathbb{E} \left[\right. X^{2} \left]\right. - \left(\right. \mathbb{E} \left[\right. X \left]\right. \left.\right)^{2} = 3 - 1 = 2$. This matches the general formula $Var \left(\right. \chi^{2} \left(\right. k \left.\right) \left.\right) = 2 k$ with $k = 1$.

This is exactly the calculation that produces the " $+ 2$ " in the $d \left(\right. d + 2 \left.\right)$ denominator in Step 6 of the puzzle solution. The second moment of $\chi^{2} \left(\right. 1 \left.\right)$ being 3 (not 1) is what creates that correction term.

## A.2 — The Beta Distribution

**Definition.** A random variable $Z$ follows a **Beta distribution** with parameters $\alpha > 0$ and $\beta > 0$, written $Z sim Beta \left(\right. \alpha , \beta \left.\right)$, if it takes values in $\left[\right. 0 , 1 \left]\right.$ with PDF: 
$$
f \left(\right. z \left.\right) = \frac{z^{\alpha - 1} \left(\right. 1 - z \left.\right)^{\beta - 1}}{B \left(\right. \alpha , \beta \left.\right)} \text{for } z \in \left[\right. 0 , 1 \left]\right.
$$
 where $B \left(\right. \alpha , \beta \left.\right) = \frac{\Gamma \left(\right. \alpha \left.\right) \Gamma \left(\right. \beta \left.\right)}{\Gamma \left(\right. \alpha + \beta \left.\right)}$ is the beta function.

**Key properties:**

- Mean: $\mathbb{E} \left[\right. Z \left]\right. = \frac{\alpha}{\alpha + \beta}$
- Variance: $Var \left(\right. Z \left.\right) = \frac{\alpha \beta}{\left(\right. \alpha + \beta \left.\right)^{2} \left(\right. \alpha + \beta + 1 \left.\right)}$
- Mode (for $\alpha , \beta > 1$): $\frac{\alpha - 1}{\alpha + \beta - 2}$
- If $\alpha = \beta$, the distribution is symmetric around $1 / 2$.
- If $\alpha < 1$ and $\beta \gg 1$, the distribution is concentrated near 0 with a right skew.

**Where it appears in this blog:** The squared coordinate $u_{i}^{2}$ of a uniform random unit vector follows $Beta \left(\right. 1 / 2 , \left(\right. d - 1 \left.\right) / 2 \left.\right)$. This has $\alpha = 1 / 2 < 1$, so the PDF diverges at 0 — most of the probability mass is near zero, which makes sense because each coordinate of a high-dimensional unit vector is small.

**Connection: Chi-squared → Beta.** This is the key link used in Step 3 of the puzzle solution. If $X sim \chi^{2} \left(\right. a \left.\right)$ and $Y sim \chi^{2} \left(\right. b \left.\right)$ are **independent**, then: 
$$
\frac{X}{X + Y} sim Beta \left(\right. \frac{a}{2} , \frac{b}{2} \left.\right)
$$
 In words: the fraction of a total chi-squared sum attributable to one part follows a Beta distribution. The proof goes through the change-of-variables formula for joint densities, transforming $\left(\right. X , Y \left.\right) \rightarrow \left(\right. X / \left(\right. X + Y \left.\right) , X + Y \left.\right)$.

#### Worked Example A.3: The Beta distribution of a single coordinate

*Problem:* A uniform random unit vector $\mathbf{u}$ on the sphere in $\mathbb{R}^{5}$. What is the exact distribution of $u_{1}^{2}$? Compute its mean and variance.

*Solution:* Using the Gaussian construction, $u_{1} = g_{1} / \parallel \mathbf{g} \parallel$, so:

$$
u_{1}^{2} = \frac{g_{1}^{2}}{g_{1}^{2} + g_{2}^{2} + g_{3}^{2} + g_{4}^{2} + g_{5}^{2}} = \frac{X}{X + Y}
$$

where $X = g_{1}^{2} sim \chi^{2} \left(\right. 1 \left.\right)$ and $Y = g_{2}^{2} + \hdots + g_{5}^{2} sim \chi^{2} \left(\right. 4 \left.\right)$, independent of $X$.

By the chi-squared-to-Beta connection:

$$
u_{1}^{2} sim Beta \left(\right. \frac{1}{2} , \frac{4}{2} \left.\right) = Beta \left(\right. \frac{1}{2} , 2 \left.\right)
$$

Now compute moments:

- $\mathbb{E} \left[\right. u_{1}^{2} \left]\right. = \frac{1 / 2}{1 / 2 + 2} = \frac{1 / 2}{5 / 2} = \frac{1}{5}$. Checks out: $d = 5$, and by symmetry each of the 5 coordinates gets $1 / 5$ of the squared norm.
- $Var \left(\right. u_{1}^{2} \left.\right) = \frac{\left(\right. 1 / 2 \left.\right) \left(\right. 2 \left.\right)}{\left(\right. 5 / 2 \left.\right)^{2} \left(\right. 5 / 2 + 1 \left.\right)} = \frac{1}{\left(\right. 25 / 4 \left.\right) \left(\right. 7 / 2 \left.\right)} = \frac{1}{87.5} = \frac{4}{350} = \frac{2}{175}$
- $SD \left(\right. u_{1}^{2} \left.\right) = \sqrt{2 / 175} \approx 0.107$. The mean is $0.2$, so the coefficient of variation is about 0.53 — substantial spread, as discussed in Step 4.

#### Worked Example A.4: Seeing the Gaussian approximation emerge

*Problem:* For $d = 5$ vs. $d = 1000$, compare the Beta distribution of $u_{1}^{2}$ to the Gaussian approximation.

*Solution:* The coordinate $u_{1}$ (not squared) has mean 0 and variance $1 / d$. The Gaussian approximation says $u_{1} \approx \mathcal{N} \left(\right. 0 , 1 / d \left.\right)$.

For $d = 5$: $u_{1} \approx \mathcal{N} \left(\right. 0 , 0.2 \left.\right)$. But the actual distribution of $u_{1}$ has support only on $\left[\right. - 1 , 1 \left]\right.$ (it's a coordinate of a unit vector), and the density has noticeable curvature at the tails. The Gaussian leaks probability outside $\left[\right. - 1 , 1 \left]\right.$. The approximation is rough.

For $d = 1000$: $u_{1} \approx \mathcal{N} \left(\right. 0 , 0.001 \left.\right)$, so $SD \left(\right. u_{1} \left.\right) \approx 0.032$. Almost all probability mass sits in $\left[\right. - 0.1 , 0.1 \left]\right.$, far from the boundary at $\pm 1$. The tails of the Gaussian that leak outside $\left[\right. - 1 , 1 \left]\right.$ have negligible mass ($< 10^{- 200}$). The approximation is excellent.

This is why PolarQuant works well at LLM head dimensions ($d = 64$ to 128) — large enough that the Gaussian approximation to the Beta is already very accurate, and the precomputed Lloyd-Max quantizer designed for this distribution performs nearly optimally.

## A.3 — The Dirichlet Distribution

**Definition.** A random vector $\left(\right. Z_{1} , Z_{2} , \ldots , Z_{d} \left.\right)$ follows a **Dirichlet distribution** with parameters $\left(\right. \alpha_{1} , \alpha_{2} , \ldots , \alpha_{d} \left.\right)$, written $Dir \left(\right. \alpha_{1} , \ldots , \alpha_{d} \left.\right)$, if:
- Each $Z_{i} \geq 0$
- $\sum_{i = 1}^{d} Z_{i} = 1$ (the components live on the probability simplex)
- The joint PDF is $f \left(\right. z_{1} , \ldots , z_{d} \left.\right) = \frac{\Gamma \left(\right. \alpha_{1} + \hdots + \alpha_{d} \left.\right)}{\Gamma \left(\right. \alpha_{1} \left.\right) \hdots \Gamma \left(\right. \alpha_{d} \left.\right)} \prod_{i = 1}^{d} z_{i}^{\alpha_{i} - 1}$
When all $\alpha_{i} = \alpha$, this is a **symmetric Dirichlet** with parameter $\alpha$.

**Key properties:**

- Mean of each component: $\mathbb{E} \left[\right. Z_{i} \left]\right. = \frac{\alpha_{i}}{\alpha_{0}}$ where $\alpha_{0} = \sum \alpha_{j}$
- Variance: $Var \left(\right. Z_{i} \left.\right) = \frac{\alpha_{i} \left(\right. \alpha_{0} - \alpha_{i} \left.\right)}{\alpha_{0}^{2} \left(\right. \alpha_{0} + 1 \left.\right)}$
- Covariance (for $i \neq j$): $Cov \left(\right. Z_{i} , Z_{j} \left.\right) = \frac{- \alpha_{i} \alpha_{j}}{\alpha_{0}^{2} \left(\right. \alpha_{0} + 1 \left.\right)}$
- Each marginal is Beta: $Z_{i} sim Beta \left(\right. \alpha_{i} , \alpha_{0} - \alpha_{i} \left.\right)$

**Connection: Chi-squared → Dirichlet → Beta.** If $X_{1} , \ldots , X_{d}$ are independent with $X_{i} sim \chi^{2} \left(\right. 2 \alpha_{i} \left.\right)$, and $S = \sum X_{i}$, then: 
$$
\left(\right. \frac{X_{1}}{S} , \frac{X_{2}}{S} , \ldots , \frac{X_{d}}{S} \left.\right) sim Dir \left(\right. \alpha_{1} , \ldots , \alpha_{d} \left.\right)
$$
 The Beta distribution is the special case $d = 2$: splitting a total into two parts gives a single ratio that's Beta. The Dirichlet generalizes this to splitting a total into $d$ parts simultaneously.

**Where it appears in this blog:** The vector of squared coordinates $\left(\right. u_{1}^{2} , u_{2}^{2} , \ldots , u_{d}^{2} \left.\right)$ of a uniform random unit vector follows:

$$
Dir \left(\right. \frac{1}{2} , \frac{1}{2} , \ldots , \frac{1}{2} \left.\right) (\text{symmetric Dirichlet with } \alpha = 1 / 2 )
$$

This is because $u_{i}^{2} = g_{i}^{2} / \sum g_{k}^{2}$, and each $g_{i}^{2} sim \chi^{2} \left(\right. 1 \left.\right)$, and $\chi^{2} \left(\right. 1 \left.\right) = \chi^{2} \left(\right. 2 \times 1 / 2 \left.\right)$, so the construction above applies with $\alpha_{i} = 1 / 2$ for all $i$.

#### Worked Example A.5: Dirichlet moments and the d(d+2) formula

*Problem:* For $\left(\right. Z_{1} , \ldots , Z_{d} \left.\right) sim Dir \left(\right. 1 / 2 , \ldots , 1 / 2 \left.\right)$ (the distribution of squared coordinates of a random unit vector), compute $\mathbb{E} \left[\right. Z_{i} Z_{j} \left]\right.$ for $i \neq j$.

*Solution:* We use the general Dirichlet second moment formula. For a Dirichlet with parameters $\left(\right. \alpha_{1} , \ldots , \alpha_{d} \left.\right)$ and $\alpha_{0} = \sum \alpha_{k}$:

$$
\mathbb{E} \left[\right. Z_{i} Z_{j} \left]\right. = \frac{\alpha_{i} \alpha_{j}}{\alpha_{0} \left(\right. \alpha_{0} + 1 \left.\right)} \text{for } i \neq j
$$

Let's derive this. We have:

$$
\mathbb{E} \left[\right. Z_{i} Z_{j} \left]\right. = \mathbb{E} \left[\right. Z_{i} \mathbb{E} \left[\right. Z_{j} \mid Z_{i} \left]\right. \left]\right.
$$

But it's easier to go through the chi-squared construction. Let $X_{k} sim \chi^{2} \left(\right. 2 \alpha_{k} \left.\right)$ independently, $S = \sum X_{k}$, and $Z_{k} = X_{k} / S$. Then:

$$
\mathbb{E} \left[\right. Z_{i} Z_{j} \left]\right. = \mathbb{E} \left[\right. \frac{X_{i} X_{j}}{S^{2}} \left]\right.
$$

Since $X_{i}$ and $X_{j}$ are independent of each other (and of the rest), we can condition on $S$. But actually, the cleanest approach uses the identity: for independent Gamma variables $X_{i} sim \text{Gamma} \left(\right. \alpha_{i} , 1 \left.\right)$, with $S = \sum X_{k}$:

$$
\mathbb{E} \left[\right. \frac{X_{i} X_{j}}{S^{2}} \left]\right. = \frac{\mathbb{E} \left[\right. X_{i} \left]\right. \mathbb{E} \left[\right. X_{j} \left]\right.}{\mathbb{E} \left[\right. S \left]\right. \left(\right. \mathbb{E} \left[\right. S \left]\right. + 1 \left.\right)} = \frac{\alpha_{i} \alpha_{j}}{\alpha_{0} \left(\right. \alpha_{0} + 1 \left.\right)}
$$

(This identity follows from the fact that $Z_{i}$ is independent of $S$ — a defining property of the Dirichlet — and from the formula for $\mathbb{E} \left[\right. 1 / S \left]\right.$ for a Gamma sum.)

In our case, $\alpha_{i} = \alpha_{j} = 1 / 2$ and $\alpha_{0} = d / 2$, so:

$$
\mathbb{E} \left[\right. Z_{i} Z_{j} \left]\right. = \frac{\left(\right. 1 / 2 \left.\right) \left(\right. 1 / 2 \left.\right)}{\left(\right. d / 2 \left.\right) \left(\right. d / 2 + 1 \left.\right)} = \frac{1 / 4}{\left(\right. d / 2 \left.\right) \cdot \left(\right. d + 2 \left.\right) / 2} = \frac{1 / 4}{d \left(\right. d + 2 \left.\right) / 4} = \frac{1}{d \left(\right. d + 2 \left.\right)}
$$

That's the $1 / d \left(\right. d + 2 \left.\right)$ from Step 6. Now the covariance:

$$
Cov \left(\right. Z_{i} , Z_{j} \left.\right) = \mathbb{E} \left[\right. Z_{i} Z_{j} \left]\right. - \mathbb{E} \left[\right. Z_{i} \left]\right. \mathbb{E} \left[\right. Z_{j} \left]\right. = \frac{1}{d \left(\right. d + 2 \left.\right)} - \frac{1}{d} \cdot \frac{1}{d} = \frac{1}{d \left(\right. d + 2 \left.\right)} - \frac{1}{d^{2}}
$$
 
$$
= \frac{d - \left(\right. d + 2 \left.\right)}{d^{2} \left(\right. d + 2 \left.\right)} = \frac{- 2}{d^{2} \left(\right. d + 2 \left.\right)}
$$

For $d = 1000$: $Cov \left(\right. Z_{i} , Z_{j} \left.\right) = - 2 / \left(\right. 1000^{2} \cdot 1002 \left.\right) \approx - 2.0 \times 10^{- 9}$. Tiny.

#### Worked Example A.6: Checking the Dirichlet formula numerically

*Problem:* Verify the formula $\mathbb{E} \left[\right. Z_{i} Z_{j} \left]\right. = 1 / d \left(\right. d + 2 \left.\right)$ for $d = 3$ by computing it from the chi-squared definition.

*Solution:* The formula predicts $\mathbb{E} \left[\right. Z_{1} Z_{2} \left]\right. = 1 / \left(\right. 3 \times 5 \left.\right) = 1 / 15$.

Let's check with the Dirichlet moment formula directly. For $Dir \left(\right. 1 / 2 , 1 / 2 , 1 / 2 \left.\right)$, the general cross-moment is:

$$
\mathbb{E} \left[\right. \prod Z_{i}^{n_{i}} \left]\right. = \frac{B \left(\right. \alpha_{1} + n_{1} , \ldots , \alpha_{d} + n_{d} \left.\right)}{B \left(\right. \alpha_{1} , \ldots , \alpha_{d} \left.\right)}
$$

where $B$ is the multivariate beta function. With $n_{1} = 1 , n_{2} = 1 , n_{3} = 0$:

$$
\mathbb{E} \left[\right. Z_{1} Z_{2} \left]\right. = \frac{\Gamma \left(\right. 1 / 2 + 1 \left.\right) \Gamma \left(\right. 1 / 2 + 1 \left.\right) \Gamma \left(\right. 1 / 2 \left.\right)}{\Gamma \left(\right. 3 / 2 + 2 \left.\right)} \cdot \frac{\Gamma \left(\right. 3 / 2 \left.\right)}{\Gamma \left(\right. 1 / 2 \left.\right) \Gamma \left(\right. 1 / 2 \left.\right) \Gamma \left(\right. 1 / 2 \left.\right)}
$$

Using $\Gamma \left(\right. 1 / 2 \left.\right) = \sqrt{\pi}$, $\Gamma \left(\right. 3 / 2 \left.\right) = \frac{1}{2} \sqrt{\pi}$, $\Gamma \left(\right. 5 / 2 \left.\right) = \frac{3}{4} \sqrt{\pi}$, $\Gamma \left(\right. 7 / 2 \left.\right) = \frac{15}{8} \sqrt{\pi}$:

$$
= \frac{\left(\right. \frac{1}{2} \sqrt{\pi} \left.\right) \left(\right. \frac{1}{2} \sqrt{\pi} \left.\right) \left(\right. \sqrt{\pi} \left.\right)}{\left(\right. \frac{15}{8} \sqrt{\pi} \left.\right)} \cdot \frac{\left(\right. \frac{1}{2} \sqrt{\pi} \left.\right)}{\left(\right. \sqrt{\pi} \left.\right) \left(\right. \sqrt{\pi} \left.\right) \left(\right. \sqrt{\pi} \left.\right)} = \frac{\frac{1}{4} \pi \sqrt{\pi}}{\frac{15}{8} \sqrt{\pi}} \cdot \frac{1}{2 \pi} = \frac{\frac{1}{4}}{\frac{15}{8}} \cdot \frac{1}{2} = \frac{2}{15} \cdot \frac{1}{2} = \frac{1}{15}
$$

Matches $1 / d \left(\right. d + 2 \left.\right) = 1 / 15$.

## A.4 — The Family Tree: How They All Connect

Here is how the three distributions relate, in the order that matters for this blog:

**Level 0: Gaussian.** Start with independent $g_{1} , \ldots , g_{d} sim \mathcal{N} \left(\right. 0 , 1 \left.\right)$.

**Level 1: Chi-squared.** Square them: each $g_{i}^{2} sim \chi^{2} \left(\right. 1 \left.\right)$. Sum $k$ of them: $\sum_{i = 1}^{k} g_{i}^{2} sim \chi^{2} \left(\right. k \left.\right)$.

**Level 2: Beta.** Take the ratio of one part to the whole: $\frac{g_{i}^{2}}{\sum_{j = 1}^{d} g_{j}^{2}} sim Beta \left(\right. 1 / 2 , \left(\right. d - 1 \left.\right) / 2 \left.\right)$. This is a single squared coordinate of a random unit vector.

**Level 3: Dirichlet.** Take all such ratios jointly: $\left(\right. \frac{g_{1}^{2}}{\sum g_{j}^{2}} , \ldots , \frac{g_{d}^{2}}{\sum g_{j}^{2}} \left.\right) sim Dir \left(\right. 1 / 2 , \ldots , 1 / 2 \left.\right)$. This is the full vector of squared coordinates. Each marginal is Beta (Level 2), but the Dirichlet captures the joint structure — including the constraint that they sum to 1, which is what creates the small negative covariances in Step 6.

d independent Gaussians: g₁,..., g⇸ ~ N(0,1) | v Square each: g₁²,..., g⇸² ~ χ²(1) each | +------------------+-------------------+ | | v v Sum all d: Normalize by sum: S = Σ gᵢ² ~ χ²(d) (g₁²/S,..., g⇸²/S) ~ Dir(½,...,½) | v Any single ratio: gᵢ²/S ~ Beta(½, (d-1)/2) | v Take square root: uᵢ = gᵢ/√S ≈ N(0, 1/d) \[coordinate of random unit vector\]

The chain from Gaussians to the coordinate distribution used by PolarQuant. Each level builds on the previous.

#### Worked Example A.7: Tracing through the full chain for d=4

*Problem:* Draw $g_{1} = 1.2$, $g_{2} = - 0.5$, $g_{3} = 0.8$, $g_{4} = - 1.1$ from $\mathcal{N} \left(\right. 0 , 1 \left.\right)$. Compute the unit vector, the Dirichlet vector, and verify the distributions.

*Solution:*

**Chi-squared level:** $g_{1}^{2} = 1.44$, $g_{2}^{2} = 0.25$, $g_{3}^{2} = 0.64$, $g_{4}^{2} = 1.21$. Sum: $S = 3.54$. (One draw from $\chi^{2} \left(\right. 4 \left.\right)$; the mean of $\chi^{2} \left(\right. 4 \left.\right)$ is 4, so 3.54 is a reasonable value.)

**Unit vector (take square root of S):** $\parallel \mathbf{g} \parallel = \sqrt{3.54} = 1.881$.

$$
\left(\right. u_{1} , u_{2} , u_{3} , u_{4} \left.\right) = \frac{1}{1.881} \left(\right. 1.2 , - 0.5 , 0.8 , - 1.1 \left.\right) = \left(\right. 0.638 , - 0.266 , 0.425 , - 0.585 \left.\right)
$$

Check: $0.638^{2} + 0.266^{2} + 0.425^{2} + 0.585^{2} = 0.407 + 0.071 + 0.181 + 0.342 = 1.001 \approx 1$.

**Dirichlet level (squared coordinates):**

$$
\left(\right. u_{1}^{2} , u_{2}^{2} , u_{3}^{2} , u_{4}^{2} \left.\right) = \left(\right. 0.407 , 0.071 , 0.181 , 0.342 \left.\right)
$$

These sum to 1 and each is in $\left[\right. 0 , 1 \left]\right.$ — one draw from $Dir \left(\right. 1 / 2 , 1 / 2 , 1 / 2 , 1 / 2 \left.\right)$. The expected value of each component is $1 / d = 1 / 4 = 0.25$.

**Beta level (single component):** $u_{1}^{2} = 0.407$ is one draw from $Beta \left(\right. 1 / 2 , 3 / 2 \left.\right)$. The mean of this Beta is $\left(\right. 1 / 2 \left.\right) / \left(\right. 1 / 2 + 3 / 2 \left.\right) = 1 / 4 = 0.25$. Our draw of 0.407 is above the mean, which is fine — the distribution has substantial spread at $d = 4$.

**Gaussian approximation:** $u_{1} = 0.638$. The approximation says $u_{1} \approx \mathcal{N} \left(\right. 0 , 1 / 4 \left.\right)$, so $SD = 0.5$. Our value of 0.638 is 1.28 standard deviations out — perfectly typical. At $d = 4$ the approximation is coarse; at $d = 128$ (a real LLM head dimension) it would be far more accurate.

#### Worked Example A.8: Why the Dirichlet constraint matters (and why it doesn't)

*Problem:* In the Dirichlet vector above, suppose you observe that $u_{1}^{2} = 0.9$ (one coordinate hogs 90% of the squared norm). What can you say about the remaining coordinates?

*Solution:* Since $\sum u_{i}^{2} = 1$, the remaining three squared coordinates must share $1 - 0.9 = 0.1$. Their conditional distribution is $Dir \left(\right. 1 / 2 , 1 / 2 , 1 / 2 \left.\right)$ rescaled to sum to 0.1 instead of 1. Each remaining coordinate has conditional mean $0.1 / 3 \approx 0.033$, much less than the unconditional mean of $0.25$.

This is the negative covariance at work: knowing one coordinate is large *forces* the others to be small. But at $d = 1000$, the probability of any single coordinate hogging 90% of the norm is astronomically small (it would require a $Beta \left(\right. 1 / 2 , 499.5 \left.\right)$ random variable to take the value 0.9, which is many hundreds of standard deviations from the mean of 0.001). In practice, no coordinate deviates enough from $1 / d$ to meaningfully constrain the others. That's the concentration of measure argument for near-independence.