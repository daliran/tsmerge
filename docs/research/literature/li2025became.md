# li2025became — BECAME: BayEsian Continual Learning with Adaptive Model MErging

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 170 claims, every table cell correct: 4 overstatements and 1 missing inconsistency, all fixed)
- **Reference:** Li, Lu, Dai, Huang, Ding, Lu; ICML 2025 (PMLR 267); arXiv 2504.02666 ([references.bib](references.bib))
- **Version read:** arXiv v2 (29 May 2025), 21 pages: main text pp. 1–9 (with conclusion and impact statement), references pp. 10–12, appendix pp. 13–21
- **Read:** main text in full (pp. 1–9); appendix in full: A (p. 13), B.1–B.5 (pp. 13–15), C.1–C.5 (pp. 15–21), including all appendix tables and figures. Not read in detail: the reference list (pp. 10–12), only consulted to identify cited works
- **Code:** <https://github.com/limei0818/BECAME> (p. 1, p. 9)

## In one paragraph

The paper studies continual learning (CL) where, at each new task, two models are available:

- one trained with **gradient projection** (stable, little forgetting, limited plasticity) and
- one trained **without constraints** from it (plastic, more forgetting) (pp. 2, 5–7).

It proves that somewhere on the straight line between the previous model and the new one, the cumulative loss over all tasks seen so far is no higher than at either endpoint (Lemma 3.1, p. 4).

Writing CL as sequential Bayesian inference with a Laplace (Gaussian) approximation of the posterior, it derives a **closed-form merging coefficient** $\lambda_t^*$ from the curvature of the new task's loss and the accumulated curvature (precision) of the old tasks,
approximated with the Fisher information (Eqs. 17, 20, p. 5).

The two-stage method, BECAME, plugs into four GPM-family methods and Adam-NSCL and improves average accuracy on all reported benchmarks,
e.g. GPM from 71.81 to 75.05 on 10-Split CIFAR-100 and Adam-NSCL from 72.91 to 81.66 (Tables 1–2, pp. 6–7).

It also beats fixed or tuned merging coefficients ($1/t$, CoMA, CoFiMA) (Table 3, p. 8; Table 11, p. 17).

All reported methods stay below the multi-task upper bound (Tables 1–2, pp. 6–7).

## Problem

Two questions, as the paper states them (p. 2):

- Can model merging improve the stability-plasticity trade-off in continual learning?
- Can the optimal merging coefficient be derived in closed form, instead of averaging (equal weights) or grid-searching a hyperparameter (p. 2, p. 3)?

**Setting** (pp. 3, 7):

- A network $f_\theta$ with parameters $\theta \in \mathbb{R}^{|\theta|}$ is trained sequentially on $T$ tasks;
  task $t$ has data $\mathcal{D}_t = \{(\mathbf{x}_t^{(n)}, \mathbf{y}_t^{(n)})\}_{n=1}^{|\mathcal{D}_t|}$ from a distribution $\mathbb{D}_t$, each $\mathbb{D}_t$ independent of the others (p. 3).
- While learning task $t$ only $\mathcal{D}_t$ is accessible, yet the goal is to minimize the cumulative loss over all tasks so far (p. 3).
- **Task-incremental:** each task has a separate classifier head (p. 7).
- All benchmarks are image classification (p. 7).

**The gap it addresses** (p. 2, p. 3):

- Prior merging-for-CL methods (IMM) approximate each task's posterior with an independent Gaussian, assuming new learning is minimally influenced by previous knowledge;
  the authors argue this does not match CL, where tasks are interrelated (p. 2).
- Merging coefficients in prior work are either:
  - the plain average,
  - a constant tied to the number of tasks (Connector),
  - or set manually through exhaustive tuning (IMM, CoMA) (p. 2, p. 3).

## Method

**Objective** (Eq. 1, p. 3):

$$\theta_t^* = \arg\min_\theta \mathcal{L}_{1:t}(\theta; \mathcal{D}_{1:t}) = \arg\min_\theta \sum_{i=1}^{t} \mathcal{L}_i(\theta; \mathcal{D}_i)$$

with $\mathcal{D}_{1:t} = \bigcup_{i=1}^t \mathcal{D}_i$; written $\mathcal{L}_i(\theta)$ and $\mathcal{L}_{1:t}(\theta)$ below (p. 3).

**Lemma 3.1: a better point exists on the merging path** (Eq. 2, p. 4).

Given $\theta_{t-1}^*$ minimizing $\mathcal{L}_{1:t-1}$, and $\hat\theta_t$ optimized from $\theta_{t-1}^*$ to a local minimum of $\mathcal{L}_t$, there exists $\lambda \in [0,1]$ with

$$\mathcal{L}_{1:t}\big((1-\lambda)\theta_{t-1}^* + \lambda\hat\theta_t\big) \le \min\{\mathcal{L}_{1:t}(\theta_{t-1}^*), \mathcal{L}_{1:t}(\hat\theta_t)\}$$

Proof sketch (Eqs. 3–5, p. 4), with $\theta(\lambda) = (1-\lambda)\theta_{t-1}^* + \lambda\hat\theta_t$:

$$\frac{\partial \mathcal{L}_{1:t}(\theta(\lambda))}{\partial \lambda} = \left(\frac{\partial \mathcal{L}_{1:t-1}(\theta(\lambda))}{\partial \theta(\lambda)} + \frac{\partial \mathcal{L}_t(\theta(\lambda))}{\partial \theta(\lambda)}\right)^\top (\hat\theta_t - \theta_{t-1}^*)$$

- At $\lambda = 0$ (Eq. 4): $\left(\frac{\partial \mathcal{L}_t}{\partial\theta}\big|_{\theta=\theta_{t-1}^*}\right)^\top(\hat\theta_t - \theta_{t-1}^*) \le 0$,
  "because $\hat\theta_t$ is obtained by gradient descent from $\theta_{t-1}^*$",
  so the direction is aligned with the negative gradient of $\mathcal{L}_t$ there (p. 4).
- At $\lambda = 1$ (Eq. 5): $\left(\frac{\partial \mathcal{L}_{1:t-1}}{\partial\theta}\big|_{\theta=\hat\theta_t}\right)^\top(\hat\theta_t - \theta_{t-1}^*) \ge 0$,
  "as learning a new task generally increases the loss over previous tasks" (p. 4).
- By continuity in $\lambda \in [0,1]$ the claim follows (p. 4).
- Motivation: models trained sequentially likely lie in the same loss basin, with no significant loss barrier along the linear path (p. 4, citing linear mode connectivity work).

**Bayesian view** (Eqs. 6–9, p. 4):

$$p(\theta|\mathcal{D}_{1:t}) \propto p(\theta)\prod_{i=1}^t p(\mathcal{D}_i|\theta) \propto p(\mathcal{D}_t|\theta)\,p(\theta|\mathcal{D}_{1:t-1})$$

$$\theta_t^* = \arg\max_\theta \log p(\theta|\mathcal{D}_{1:t}) = \arg\max_\theta \log p(\mathcal{D}_t|\theta) + \log p(\theta|\mathcal{D}_{1:t-1})$$

- With $-\log p(\mathcal{D}_i|\theta)$ as the task loss $\mathcal{L}_i(\theta)$ and a uniform prior $p(\theta)$, MAP equals minimizing the cumulative loss of Eq. 1 (Eq. 8, p. 4).
- **Laplace approximation** (p. 4): $p(\theta|\mathcal{D}_{1:t-1}) \approx q_{t-1}(\theta) = \mathcal{N}(\theta; \mu_{t-1}, \Lambda_{t-1}^{-1})$, $\Lambda_{t-1}$ positive semi-definite.
  - Similarly $q_t(\theta) = \mathcal{N}(\theta; \mu_t, \Lambda_t^{-1})$.
- Hence (Eq. 9, p. 4; Eq. 10, p. 5), with $\mu_{t-1} = \theta_{t-1}^*$:

$$\theta_t^* = \arg\min_\theta \mathcal{L}_t(\theta) + \frac{1}{2}(\theta - \theta_{t-1}^*)^\top \Lambda_{t-1} (\theta - \theta_{t-1}^*)$$

**Optimal coefficient** (Eqs. 11–17, p. 5). Restrict $\theta$ to the path $\theta(\lambda) = (1-\lambda)\theta_{t-1}^* + \lambda\hat\theta_t$ and set $\Delta\theta = \hat\theta_t - \theta_{t-1}^*$:

$$\tilde{\mathcal{L}}_{1:t}(\lambda) = \mathcal{L}_t\big(\hat\theta_t + (\lambda-1)\Delta\theta\big) + \frac{1}{2}\lambda^2 \Delta\theta^\top \Lambda_{t-1} \Delta\theta$$

- Second-order Taylor expansion of $\mathcal{L}_t$ around $\hat\theta_t$; the gradient vanishes there (local minimum) and the Hessian is positive semi-definite (Eq. 12, p. 5):

$$\mathcal{L}_t(\theta(\lambda)) \approx \mathcal{L}_t(\hat\theta_t) + \frac{1}{2}(\lambda-1)^2 \Delta\theta^\top \nabla_\theta^2 \mathcal{L}_t|_{\theta=\hat\theta_t} \Delta\theta$$

- Derivative (Eq. 13): $\frac{\partial \tilde{\mathcal{L}}_{1:t}}{\partial\lambda} = (\lambda-1)\Delta\theta^\top \nabla_\theta^2 \mathcal{L}_t|_{\theta=\hat\theta_t}\Delta\theta + \lambda\Delta\theta^\top\Lambda_{t-1}\Delta\theta$.
  - It is $\le 0$ at $\lambda=0$ (Eq. 14) and $\ge 0$ at $\lambda=1$ (Eq. 15).
  - The second derivative is $\ge 0$ (Eq. 16), so $\tilde{\mathcal{L}}_{1:t}$ is convex along the path and has a unique optimum in $[0,1]$ (p. 5).
- Closed form (Eq. 17, p. 5):

$$\lambda_t^* = \frac{\Delta\theta^\top \nabla_\theta^2 \mathcal{L}_t|_{\theta=\hat\theta_t} \Delta\theta}{\Delta\theta^\top\big(\nabla_\theta^2 \mathcal{L}_t|_{\theta=\hat\theta_t} + \Lambda_{t-1}\big)\Delta\theta}$$

**Precision update and Fisher approximation** (Eqs. 18–20, p. 5):

$$\Lambda_t = -\nabla_\theta^2 \log p(\theta|\mathcal{D}_{1:t})|_{\theta=\mu_t} \approx -\nabla_\theta^2 \log p(\mathcal{D}_t|\theta)|_{\theta=\mu_t} + \Lambda_{t-1}$$

- $\mu_t = \theta_t^*$; the recursion is initialized by the Hessian of the negative log prior, "typically constant" (p. 5).
- The Hessian is expensive and not always positive semi-definite, so the Fisher Information Matrix is used instead, positive semi-definite by construction (Eq. 19, p. 5):

$$F_t(\theta) = \mathbb{E}\big[\nabla_\theta \log p(\mathcal{D}_t|\theta)\,\nabla_\theta \log p(\mathcal{D}_t|\theta)^\top\big]$$

- The coefficient actually computed (Eq. 20, p. 5):

$$\lambda_t^* = \frac{\Delta\theta^\top F_t(\hat\theta_t)\Delta\theta}{\Delta\theta^\top\big(F_t(\hat\theta_t) + \sum_{i=1}^{t-1} F_i(\theta_i^*)\big)\Delta\theta}$$

- The FIM "can be simplified with a diagonal approximation" (p. 5).

**BECAME: two stages per task** (Section 3.4, pp. 5–7; Algorithm 1, p. 5):

1. Train on task 1 to get $\theta_1^*$; set $\Lambda_1 = F_1(\theta_1^*)$.
2. For $t = 2, \dots, T$:
   - **Stage 1:** from $\theta_{t-1}^*$, train on $\mathcal{D}_t$ with gradient projection, giving $\theta_t^{\text{GP}}$.
   - **Stage 2:** from $\theta_t^{\text{GP}}$, train on $\mathcal{D}_t$ without constraints, giving $\hat\theta_t$ (p. 6).
   - Compute $F_t(\hat\theta_t)$; compute $\lambda_t^*$ with Eq. 20.
   - Merge: $\theta_t^* = (1-\lambda_t^*)\theta_t^{\text{GP}} + \lambda_t^*\hat\theta_t$.
   - Update: $\Lambda_t = F_t(\theta_t^*) + \Lambda_{t-1}$.

**Why the merge starts from $\theta_t^{\text{GP}}$ instead of $\theta_{t-1}^*$** (pp. 6–7):

- Gradient projection keeps outputs on old inputs nearly unchanged, so $\mathcal{L}_{1:t-1}(\theta_t^{\text{GP}}) \approx \mathcal{L}_{1:t-1}(\theta_{t-1}^*)$ and the gradients of the old losses are $\approx 0$ at both points (Eq. 21, p. 6).
  - Lemma 3.1 then still holds with $\theta_t^{\text{GP}}$ as the starting point, and $\Delta\theta$ in Eq. 20 becomes $\hat\theta_t - \theta_t^{\text{GP}}$ (p. 6).
- Proof that Eq. 10 holds with $\theta_{t-1}^*$ replaced by $\theta_t^{\text{GP}}$ (Eqs. 22–26, p. 6):
  - with $d = \theta_t^{\text{GP}} - \theta_{t-1}^*$, the Taylor expansion and $\mathcal{L}_{1:t-1}(\theta_t^{\text{GP}}) \approx \mathcal{L}_{1:t-1}(\theta_{t-1}^*)$ give $d^\top \nabla_\theta^2 \mathcal{L}_{1:t-1}|_{\theta=\theta_{t-1}^*} d = 0$ (Eq. 24),
  - hence $d^\top\Lambda_{t-1}d = 0$ (Eq. 25);
  - since $\Lambda_{t-1}$ is positive semi-definite, $\Lambda_{t-1}d = 0$, and

$$(\theta - \theta_t^{\text{GP}})^\top\Lambda_{t-1}(\theta - \theta_t^{\text{GP}}) = (\theta - \theta_{t-1}^*)^\top\Lambda_{t-1}(\theta - \theta_{t-1}^*) \quad \text{(Eq. 26)}$$

- Since training reduces the new task's loss, $\mathcal{L}_{1:t}(\theta_t^{\text{GP}}) < \mathcal{L}_{1:t}(\theta_{t-1}^*)$, which "guarantees a better upper bound on the merged model's loss" (pp. 6–7).

**Metrics** (B.5, p. 15; Eqs. 27–28, pp. 8–9):

$$\text{ACC} = \frac{1}{T}\sum_{i=1}^T A_{T,i}, \quad \text{BWT} = \frac{1}{T-1}\sum_{i=1}^{T-1} A_{T,i} - A_{i,i}, \quad \text{IM} = \sum_{i=1}^T A_i^* - A_{i,i} \quad \text{(Eq. 29)}$$

- $A_{t,i}$: test accuracy on task $i$ after training on task $t$; $A_i^*$: accuracy on task $i$ of a model trained from random initialization on $\bigcup_{k=1}^i \mathcal{D}_k$ (p. 15).
- IM (Intransigence Measure) measures plasticity, lower is better; BWT measures stability, higher is better (p. 7, p. 8).
- Per task: $A_{T,i} = A_i^* - \text{IM}_i + \text{BWT}_i$ (Eq. 27, p. 8).
- After One epoch Accuracy, a new metric for forward transfer (Eq. 28, p. 9): $\text{AOA} = \frac{1}{T-1}\sum_{i=2}^T A_i^{\text{epoch}=1}$,
  the test accuracy on task $i$ after one epoch of the first stage on $\mathcal{D}_i$.
- Averaged Anytime Accuracy, as printed (C.2, p. 16): $AAA = \sum_{i=1}^T AA_i$ with $AA_i = \frac{1}{T}\sum_{j=1}^t A_{ij}$.
  - **Our reading:** as printed, the formula is malformed (no averaging on the outer sum, and $t$ undefined); don't implement it literally.

## Experimental setup

**Baselines** (p. 7; B.1, pp. 13–14):

- "GPM-based experiments": GPM and its extensions TRGP, SGP, GPCNS.
- "NSCL-based experiments": Adam-NSCL.
- Also compared: OWM, Connector, SI, LwF, GD-WILD, A-GEM, FS-DGPM, ER-Res, EWC.
- Merging strategies compared (p. 8): $1/t$ (IMM), CoMA, CoFiMA.
  - CoMA and CoFiMA rely on a pre-trained model in their own papers; here they are implemented within this framework with the hyperparameters reported in their papers (p. 8).

**Datasets** (p. 7; B.2, p. 14; Tables 5–6, p. 14):

| Setting | Benchmark | Tasks | Input | Classes/task | Train/task | Val/task | Test/task |
|---|---|---|---|---|---|---|---|
| GPM-based | 20-Split CIFAR-100 | 20 | 3×32×32 | 5 | 4,750 | 250 | 1,000 |
| GPM-based | 10-Split CIFAR-100 | 10 | 3×32×32 | 10 | 4,750 | 250 | 1,000 |
| GPM-based | 20-Split MiniImageNet | 20 | 3×84×84 | 5 | 2,375 | 125 | 500 |
| NSCL-based | 20-Split CIFAR-100 | 20 | 3×32×32 | 5 | 5,000 | - | 1,000 |
| NSCL-based | 10-Split CIFAR-100 | 10 | 3×32×32 | 10 | 5,000 | - | 1,000 |
| NSCL-based | third column of Table 6 | 25 | 3×64×64 | 8 | 4,000 | - | 400 |

- The third column of Table 6 (p. 14) is headed "20-Split MiniImageNet", but its values (25 tasks, 3×64×64) match the 25-Split TinyImageNet used in the NSCL experiments (p. 7).
  - **Our reading:** a header typo.
- GPM-based: 95%/5% train/validation split, no data augmentation; NSCL-based: the whole training set, with random crop (4-pixel padding) and random horizontal flip (p. 14).
- Additional benchmarks (C.1, p. 15): 5-Datasets (SVHN, CIFAR-10, not-MNIST, Fashion-MNIST, MNIST; 10 classes each, one task per dataset) and CIFAR-100 Superclass.
  - 3 different dataset orders (Table 8, p. 16).

**Architectures** (p. 7; B.3, p. 14):

- GPM-based:
  - 5-layer AlexNet-like network for 10- and 20-Split CIFAR-100 (three conv layers with 64, 128, 256 filters and kernels 4×4, 3×3, 2×2, batch norm except in the classifier, two fully connected layers of 2048 units, ReLU, 2×2 max-pooling, dropout 0.2 for the first two layers and 0.5 for the rest);
  - reduced ResNet-18 for 20-Split MiniImageNet.
- NSCL-based: ResNet-18 on all datasets.

**Training** (p. 7; B.4, pp. 14–15):

- Task 1 is trained exactly as in the corresponding baseline; tasks $t \ge 2$ use the two stages (p. 7).
- Hyperparameters in both stages are "mostly consistent" with the baselines', with "subtle adjustments" (p. 7); in C.1, the second stage's training configuration follows the first stage's (p. 15).
- 5 random seeds, mean and standard deviation reported (p. 7).
- GPM-based:
  - learning rate divided by `lr_factor` when validation loss does not improve for `lr_patience` epochs;
  - training stops when the rate falls below `lr_min` or at `n_epochs`;
  - the basis-selection threshold starts at $\epsilon_0$ and grows by $\epsilon_\Delta$ per task;
  - $\alpha$ is SGP's scale coefficient (p. 14).
- NSCL-based:
  - Adam, learning rate $10^{-4}$ for the first task and $5\times10^{-5}$ afterwards;
  - decayed by 0.5 when training loss does not decrease for 3 consecutive epochs;
  - each stage stops when this happens the third time;
  - at most 80 epochs per stage;
  - batch size 32 (10-Split CIFAR-100) or 16 (20-Split CIFAR-100, 25-Split TinyImageNet);
  - batch-norm parameters regularized with EWC, coefficient 100;
  - Adam-NSCL's $a$ = 30 for 20-Split CIFAR-100, 10 otherwise;
  - only the backbone and the current task's classifier are updated (p. 15).
- Hardware: a single NVIDIA GeForce RTX 4080 GPU (p. 15).

**GPM-based hyperparameters** (Table 7, p. 15; * = from the original papers, others from code):

| Hyperparameter | CIFAR GPM | CIFAR TRGP | CIFAR SGP | CIFAR GPCNS | Mini GPM | Mini TRGP | Mini SGP | Mini GPCNS |
|---|---|---|---|---|---|---|---|---|
| lr | 0.01* | 0.01* | 0.05* | 0.05* | 0.1* | 0.1* | 0.1* | 0.1* |
| lr_min | 10⁻⁵ | 10⁻⁵ | 5×10⁻⁵ | 5×10⁻⁵ | 10⁻³ | 10⁻³ | 10⁻³ | 10⁻³ |
| lr_patience | 6 | 6 | 6 | 6 | 5 | 5 | 5 | 5 |
| lr_factor | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 |
| n_epochs | 200* | 200* | 200* | 200* | 10* | 100* | 10* | 200* |
| batchsize | 64* | 64* | 64* | 64 | 10* | 64* | 10* | 64 |
| $\epsilon_0$ | 0.97* | 0.97* | 0.97* | 0.97 | 0.985* | 0.985* | 0.985* | 0.98 |
| $\epsilon_\Delta$ | 3×10⁻³* | 3×10⁻³* | 3×10⁻³* | 3×10⁻³ | 3×10⁻⁴* | 3×10⁻⁴* | 3×10⁻⁴* | 10⁻³ |
| $\alpha$ | - | - | 10* | 5* | - | - | 1* | 3* |

"CIFAR" is the shared 20/10-Split CIFAR-100 column group; "Mini" is 20-Split MiniImageNet (p. 15).

## Results

**GPM-based** (Table 1, p. 6). Mean ± std over 5 seeds; * = results from previous work:

| Method | 20-Split CIFAR-100 ACC | BWT | 10-Split CIFAR-100 ACC | BWT | 20-Split MiniImageNet ACC | BWT |
|---|---|---|---|---|---|---|
| Multi-task | 85.24 ± 0.59 | - | 79.52 ± 0.59 | - | 77.78 ± 1.49 | - |
| EWC* | 75.30 ± 0.70 | -6.30 ± 0.60 | 68.80 ± 0.88 | -20.00 ± 1.00 | 52.10 ± 1.10 | -9.30 ± 1.40 |
| A-GEM* | - | - | 63.98 ± 1.22 | -15.00 ± 2.00 | 57.24 ± 0.72 | -12.00 ± 1.00 |
| FS-DGPM* | 80.50 ± 0.40 | -3.30 ± 0.40 | 74.33 ± 0.31 | -3.00 ± 0.00 | - | - |
| ER-Res* | 79.20 ± 0.40 | -4.90 ± 0.50 | 71.73 ± 0.63 | -6.00 ± 1.00 | 55.20 ± 2.90 | -5.70 ± 0.80 |
| GPM | 77.34 ± 0.55 | 0.01 ± 0.07 | 71.81 ± 0.10 | -0.11 ± 0.33 | 63.90 ± 1.05 | -1.30 ± 1.27 |
| GPM + Ours | 80.57 ± 0.18 | -0.06 ± 0.15 | 75.05 ± 0.27 | 0.02 ± 0.39 | 67.62 ± 1.40 | 0.87 ± 0.26 |
| TRGP | 81.68 ± 0.69 | -0.13 ± 0.15 | 75.01 ± 0.63 | -0.01 ± 0.16 | 62.68 ± 2.49 | -1.04 ± 0.78 |
| TRGP + Ours | **82.61** ± 0.38 | -0.32 ± 0.18 | 75.87 ± 0.43 | -0.77 ± 0.27 | 65.09 ± 1.81 | -0.65 ± 1.08 |
| SGP | 80.21 ± 0.68 | -0.88 ± 0.29 | 74.97 ± 0.31 | -0.98 ± 0.30 | 66.99 ± 2.33 | -2.46 ± 1.28 |
| SGP + Ours | 81.94 ± 0.40 | -1.22 ± 0.25 | **76.74** ± 0.36 | -1.42 ± 0.25 | **70.06** ± 2.12 | -0.26 ± 0.72 |
| GPCNS | 78.63 ± 0.63 | -1.93 ± 0.42 | 71.84 ± 0.93 | -3.44 ± 0.85 | 62.85 ± 2.18 | -1.90 ± 1.75 |
| GPCNS + Ours | 80.87 ± 0.24 | -1.96 ± 0.24 | 73.89 ± 0.52 | -3.46 ± 0.68 | 64.79 ± 1.71 | -2.07 ± 1.66 |

- The paper says the method "boosts the accuracy of GPM by over 3% on all datasets" (p. 8).

**NSCL-based** (Table 2, p. 7). * = results from Connector's paper, without standard deviation:

| Method | 20-Split CIFAR-100 ACC | BWT | 10-Split CIFAR-100 ACC | BWT | 25-Split TinyImageNet ACC | BWT |
|---|---|---|---|---|---|---|
| Multi-task | 90.81 ± 0.10 | - | 95.06 ± 0.18 | - | 82.55 ± 0.12 | - |
| OWM* | 68.47 | -3.37 | 68.89 | -1.88 | 49.98 | -3.64 |
| EWC* | 71.66 | -3.72 | 70.77 | -2.83 | 52.33 | -6.17 |
| SI* | 59.76 | -8.62 | 60.57 | -5.17 | 45.27 | -4.45 |
| LwF* | 74.38 | -9.11 | 70.70 | -6.27 | 56.57 | -11.19 |
| GD-WILD* | 77.16 | -14.85 | 71.27 | -18.24 | 42.74 | -34.58 |
| Connector* | 80.80 | -5.00 | 79.79 | -0.92 | 64.61 | -6.00 |
| Adam-NSCL | 75.66 ± 0.39 | -3.85 ± 0.45 | 72.91 ± 0.30 | -1.76 ± 0.20 | 58.57 ± 0.40 | -5.74 ± 0.61 |
| Adam-NSCL + Ours | **81.88** ± 0.37 | -4.56 ± 0.42 | **81.66** ± 0.51 | -0.80 ± 0.53 | **66.49** ± 0.48 | -4.97 ± 0.73 |

- The paper reports an ACC gain "by over 6%" on 20-Split CIFAR-100 and "an ACC increase of 8%" on 10-Split CIFAR-100 and 25-Split TinyImageNet (p. 8).
- **Our reading:** from the table, the TinyImageNet gain is 66.49 − 58.57 = 7.92 points, slightly under 8; and BWT gets worse with BECAME on 20-Split CIFAR-100 (-3.85 → -4.56), so the gains there come from plasticity.

**Merging strategies, with gradient projection (GPM)** (Table 3, p. 8):

| Dataset | Strategy | ACC | BWT |
|---|---|---|---|
| 10-Split CIFAR-100 | - (GPM, no merging) | 71.81 | -0.11 |
| 10-Split CIFAR-100 | $1/t$ | 74.71 | -0.40 |
| 10-Split CIFAR-100 | CoMA | 74.07 | -2.79 |
| 10-Split CIFAR-100 | CoFiMA | 74.36 | -1.77 |
| 10-Split CIFAR-100 | Ours | **75.05** | **0.02** |
| 20-Split MiniImageNet | - (GPM, no merging) | 63.90 | -1.30 |
| 20-Split MiniImageNet | $1/t$ | 66.09 | 0.57 |
| 20-Split MiniImageNet | CoMA | 66.91 | -0.82 |
| 20-Split MiniImageNet | CoFiMA | 64.19 | 0.54 |
| 20-Split MiniImageNet | Ours | **67.62** | **0.87** |

- All merging strategies improve over no merging (p. 8).
- CoMA, with a fixed coefficient, "falls short in BWT as it tends to prioritize the most recent tasks" (p. 8).
- Strategy descriptions (p. 8): $1/t$ or a tunable constant found by grid search (Connector, IMM, CoMA); CoFiMA adds parameter-wise Fisher-weighted averaging with a tunable hyperparameter.

**Merging strategies, without gradient projection** (C.3, pp. 16–17; Table 11, p. 17). Same configuration as Table 3 but without the first (gradient projection) stage:

| Method | 10-Split CIFAR-100 ACC | BWT | 20-Split MiniImageNet ACC | BWT |
|---|---|---|---|---|
| Finetune | 57.98 | -20.19 | 57.06 | -10.93 |
| $1/t$ | 60.69 | -1.44 | 47.54 | 0.91 |
| CoMA | 64.42 | -9.79 | 60.99 | -5.00 |
| CoFiMA | 61.17 | -0.38 | 62.26 | -1.40 |
| Ours | **65.03** | -1.26 | **64.75** | -2.11 |

- The paper: highest ACC on both, with "a relatively high BWT" (pp. 16–17).
- **Our reading:**
  - Without gradient projection, every merging strategy stays far below the GPM-based numbers of Table 3 (65.03 vs 75.05 on 10-Split CIFAR-100), so most of BECAME's accuracy comes from combining merging with a stability-preserving first stage, not from merging alone.
  - On MiniImageNet, $1/t$ (47.54) is worse than plain fine-tuning (57.06).

**Merge coefficient vs cumulative training loss** (C.5, p. 18; Figures 12–13, p. 21).

- $\lambda$ swept from 0 to 1 in steps of 0.05 on 10-Split CIFAR-100;
- the computed $\lambda_t^*$ is printed on the plots;
- the authors state that the values "identify a point with the minimum cumulative loss" (p. 18).

The C.5 text says Figures 12 and 13 are "based on GPM and Adam-NSCL, respectively" (p. 18),
while the captions say the opposite (Figure 12 NSCL, Figure 13 GPM, p. 21); we follow the captions:

| Merge after task | NSCL-based $\lambda^*$ (Fig. 12) | GPM-based $\lambda^*$ (Fig. 13) |
|---|---|---|
| 2 | 0.6102 | 0.5396 |
| 3 | 0.3419 | 0.3294 |
| 4 | 0.3228 | 0.2318 |
| 5 | 0.2769 | 0.1668 |

- The paper: optimal coefficients differ across models on the same dataset, and the method identifies them adaptively (p. 18).
- **Our reading:**
  - In both cases $\lambda^*$ decreases with the task index, and the GPM-based values are close to $1/t$ (0.5, 0.333, 0.25, 0.2);
  - on the plots, the dashed line sits at the loss minimum for the four GPM panels (Figure 13), but is off by about 0.1 for NSCL task 3 (line at 0.3419, minimum near 0.45) and slightly off for NSCL task 4 (Figure 12).

**Additional datasets** (Table 8, p. 16; 3 dataset orders; * = reproduced by the authors from GPCNS's 10-Split CIFAR-100 code):

| Method | 5-Datasets ACC | BWT | CIFAR-100 Superclass ACC | BWT |
|---|---|---|---|---|
| GPM | 84.70 ± 3.17 | -4.88 ± 4.37 | 57.49 ± 0.65 | -1.03 ± 0.37 |
| GPM + Ours | 84.89 ± 3.10 | -3.92 ± 4.61 | 58.21 ± 0.22 | -0.60 ± 0.17 |
| TRGP | 89.99 ± 0.58 | -0.75 ± 0.62 | 57.85 ± 0.43 | -0.93 ± 0.60 |
| TRGP + Ours | **90.63** ± 0.87 | -0.80 ± 0.51 | 58.07 ± 0.56 | -0.71 ± 0.30 |
| SGP | 83.77 ± 3.28 | -6.25 ± 5.94 | 58.24 ± 0.39 | -1.85 ± 0.54 |
| SGP + Ours | 84.02 ± 3.18 | -6.24 ± 6.36 | **59.03** ± 0.32 | -1.13 ± 0.28 |
| GPCNS | 75.89 ± 5.92* | -17.01 ± 8.22* | 57.68 ± 0.84 | -3.23 ± 1.38 |
| GPCNS + Ours | 76.92 ± 5.30 | -15.51 ± 7.32 | 58.41 ± 0.13 | -2.33 ± 0.23 |

- Gains on 5-Datasets are smaller, for two reasons the authors give (p. 16):
  - improvement depends on learning CIFAR-10, while gradients barely matter for tasks like MNIST;
  - and since the model does poorly on CIFAR-10, it assigns a larger weight to CIFAR-10 when merging, which limits gains on the other tasks.
- A similar pattern on CIFAR-100 Superclass, where learning under gradient projection "may also converge to local optima" (p. 16).

**ACC and AAA** (Tables 9–10, pp. 16–17):

| Method | 20-Split CIFAR ACC | AAA | 10-Split CIFAR ACC | AAA | 20-Split MiniImageNet ACC | AAA |
|---|---|---|---|---|---|---|
| GPM | 77.34 | 77.31 | 71.81 | 72.08 | 63.90 | 63.02 |
| GPM + Ours | 80.57 | 79.61 | 75.05 | 74.22 | 67.62 | **66.05** |
| TRGP | 81.68 | 79.96 | 75.01 | 74.24 | 62.68 | 62.55 |
| TRGP + Ours | 82.61 | **80.78** | 75.87 | **74.89** | 65.09 | 64.48 |
| SGP | 80.21 | 78.78 | 74.97 | 73.62 | 66.99 | 61.97 |
| SGP + Ours | 81.94 | 79.44 | 76.74 | 74.82 | 70.06 | 64.98 |
| GPCNS | 78.63 | 76.22 | 71.84 | 71.50 | 62.85 | 60.53 |
| GPCNS + Ours | 80.87 | 78.08 | 73.89 | 72.94 | 64.79 | 61.53 |

| Method (Table 10) | 20-Split CIFAR ACC | AAA | 10-Split CIFAR ACC | AAA | 25-Split TinyImageNet ACC | AAA |
|---|---|---|---|---|---|---|
| Adam-NSCL | 75.66 | 75.43 | 72.91 | 74.77 | 58.77 | 60.21 |
| Adam + Ours | 81.88 | **81.25** | 81.66 | **81.94** | 66.49 | **66.65** |

- **Our reading:** Adam-NSCL's TinyImageNet ACC is 58.77 in Table 10 (p. 17) but 58.57 in Table 2 (p. 7) and Table 13 (p. 18); one of them is likely a typo.

**Plasticity and stability** (Figures 3, 6, 7; pp. 8, 18–19): the method's gain comes mainly from lowering IM (better plasticity) while keeping a good BWT (p. 8, p. 18).

**Our reading** of the bar plots: BECAME's IM bars are visibly shorter than each baseline's, with BWT bars of similar length.

**Balance across tasks** (Figure 4, p. 9; Figures 8–9, pp. 19–20): final per-task accuracy curves are higher, and the paper says the method "achieves a low standard deviation" (p. 18):

- lower STD across tasks in all but one case (SGP on 10-Split CIFAR-100: 3.67 vs 3.68, Figure 8, p. 19)
  - e.g. the legends print STD 5.31 (NSCL) vs 2.85 (Ours) on 10-Split CIFAR-100 and 8.00 vs 7.48 on 25-Split TinyImageNet (Figure 4, p. 9; same values in Figure 9, p. 20).

**Forward transfer, AOA** (Figure 5, p. 9; Figures 10–11, pp. 20–21): higher AOA in nearly all cases,
e.g. NSCL 57.08 vs Ours 63.70 (10-Split CIFAR-100) and 45.77 vs 52.53 (25-Split TinyImageNet), as printed in the legends (Figure 5, p. 9).

The smallest gap in the legends is GPCNS on 20-Split CIFAR-100: 56.57 vs Ours 56.65 (Figure 10, p. 20).

**Efficiency, GPM-based on 20-Split MiniImageNet** (Table 4, p. 9):

| Method | ACC (%) | Training time (s) | GPU memory (MB) |
|---|---|---|---|
| GPM | 63.90 | 434.66 | 347.26 |
| GPCNS | 62.85 | 258.13 | 998.41 |
| SGP | 66.99 | 490.84 | 347.26 |
| TRGP | 62.68 | 776.72 | 1854.32 |
| GPM + Ours | 67.62 | 584.14 | 375.72 |
| SGP + Ours | 70.06 | 675.99 | 375.72 |

- Updating the Fisher information takes 0.69 s per task, "comparable to training for a single epoch"; no overhead at inference (p. 9).

**Memory breakdown** (Table 12, p. 18), in MB:

| Method | ACC (%) | Model parameters | Additional, 1st stage | Additional, 2nd stage | Temporary |
|---|---|---|---|---|---|
| GPM | 63.90 | 4.74 | 37.51 | – | 305.01 |
| GPCNS | 62.85 | 4.74 | 584.26 | – | 409.41 |
| SGP | 66.99 | 4.74 | 53.47 | – | 289.05 |
| TRGP | 62.68 | 73.23 | 1359.18 | – | 421.91 |
| GPM+Ours | 67.62 | 4.74 | 55.88 | **4.73** | 310.37 |
| SGP+Ours | 70.69 | 4.74 | 60.49 | **4.73** | 305.76 |

- The second stage's only extra storage is the precision matrix, about the size of the model parameters (p. 17).
- **Our reading:** SGP+Ours ACC is 70.69 here (p. 18) but 70.06 in Tables 1 and 4 (pp. 6, 9).

**Efficiency, NSCL-based on 25-Split TinyImageNet** (Table 13, p. 18):

| Method | ACC (%) | Training time (h) | GPU memory (MB) |
|---|---|---|---|
| Adam-NSCL | 58.57 | 5.22 | 1728.71 |
| Connector | 64.61 | 8.53 | 1766.66 |
| NSCL+Ours | 66.49 | 6.30 | 1748.77 |

**Landscape visualization** (Figures 1–2, pp. 1, 3; NSCL on 10-Split CIFAR-100, first two tasks):

- $\theta_2^{\text{GP}}$ has a small increase in task-1 loss but high task-2 loss;
- $\hat\theta_2$ minimizes task-2 loss;
- the merged $\theta_2^*$ lies where the cumulative loss along the path is lowest (p. 1, p. 3).

## Assumptions and limitations

Stated or used by the paper:

- **Same loss basin:** sequentially trained models are assumed to lie in the same basin, with no significant loss barrier on the linear path (p. 4).
- **Lemma 3.1 assumptions:** $\hat\theta_t$ is a local minimum of $\mathcal{L}_t$, reached by gradient descent from the start point, and learning the new task increases the old tasks' loss (p. 4).
- **Uniform prior** $p(\theta)$, so MAP equals minimizing the cumulative loss (p. 4).
- **Laplace approximation:** Gaussian posterior around the previous MAP (p. 4).
- **Second-order Taylor expansion** of the new task's loss around $\hat\theta_t$ (p. 5).
- **Fisher instead of Hessian,** with a diagonal approximation (p. 5).
- **Gradient projection keeps old losses unchanged,** approximately (Eq. 21, p. 6); needed to start the merge from $\theta_t^{\text{GP}}$.
- **Task-incremental setting** with a separate head per task (p. 7).
- **Impact statement:** the approach "shares the common limitations of computer vision models, particularly in data usage" (p. 9). There is no limitations section.
- **Weaker gains** when tasks differ greatly in difficulty (5-Datasets: the hard task dominates the merge weight) (p. 16).

**Our reading:**

- The step from Eq. 4's premise to its sign is a heuristic: the displacement after many gradient steps need not align with the initial gradient.
  - The lemma is an existence argument under these assumptions, not a guarantee.
- $\lambda_t^*$ is optimal only for the quadratic surrogate along the line between two models, using training-loss curvature.
  - The paper checks it against the actual cumulative training loss (Figures 12–13), not against validation or test accuracy.
- Only one scalar coefficient per task, chosen along a line: no per-parameter or per-layer weighting (unlike CoFiMA, p. 8).
- Every benchmark is image classification with small networks trained from scratch (AlexNet-like, ResNet-18); no pre-trained foundation models, no regression, no time series.
- The method needs a gradient-projection CL method for its best results (Table 3 vs Table 11); without it, accuracy is much lower.
- The starred rows of Tables 1–2 are copied from other papers, not rerun in the same setting (pp. 6–7);
  and four small inconsistencies are noted above (Table 6 header, Adam-NSCL 58.57/58.77, SGP+Ours 70.06/70.69, and the GPM/NSCL labels of Figures 12–13 between the C.5 text and the captions).

## Relevance to this thesis

**Our reading:**

- **A principled coefficient for continual task arithmetic.**
  - BECAME's merge, $\theta_t^* = \theta_{\text{start}} + \lambda_t^*(\hat\theta_t - \theta_{\text{start}})$, is task arithmetic with one task vector relative to the previous model, and $\lambda_t^*$ (Eq. 20) replaces the validation-tuned $\lambda$ of task arithmetic.
  - It needs no old data: only the accumulated diagonal Fisher $\sum_{i<t} F_i(\theta_i^*)$, about one model's size (p. 17).
- **The simplest variant to reproduce first** is the one without gradient projection (C.3, Table 11): fine-tune from the current model on the new period, then merge with Eq. 20.
  - It applies directly to successive periods of a time series; $1/t$, CoMA-like fixed coefficients and plain fine-tuning are its natural baselines.
- **Fisher for our losses:**
  - For forecasting and reconstruction-based anomaly detection the loss is typically MSE;
  - with a Gaussian likelihood, Eq. 19's Fisher is the expected squared gradient, so Eq. 20 carries over;
  - this should be checked, not assumed.
- **Joint training stays the upper bound:** in Tables 1–2, the only ones with a multi-task row, it beats all CL methods (e.g. 77.78 vs 70.06 on 20-Split MiniImageNet, 95.06 vs 81.66 on NSCL 10-Split CIFAR-100).
  - The same comparison, joint vs merged, is the core of our study.
- **What to measure, following the paper:** ACC, BWT and IM (plasticity, Eq. 29), AOA, and the cumulative training loss as a function of $\lambda$ with the computed $\lambda^*$ marked (Figures 12–13).
  - For anomaly detection and forecasting, ACC becomes the task metric (e.g. F1, MSE).
- **The $1/t$ pattern:** the GPM-based $\lambda^*$ values (Figure 13) look close to $1/t$, the NSCL-based ones (Figure 12) stay above it.
  - Whether Eq. 20 beats a plain $1/t$ running average on our data is a cheap, informative test (Table 3 shows only a 0.3–1.5 point gain over $1/t$ with GPM).
- **Settings that may not carry over:**
  - Task-incremental image tasks with a separate head per task vs our shared regression or scoring head;
  - models trained from scratch vs a pre-trained time-series backbone;
  - very different tasks (5-Datasets) already weaken the method (p. 16), and our periods may differ by drift rather than by task.

## Quotes worth keeping

> "we reformulate the merging mechanism using Bayesian continual learning principles and derive a closed-form solution for the optimal merging coefficient based on the Laplace approximation that adapts to the diverse characteristics of tasks." (p. 1)

> "How can model merging effectively improve the stability-plasticity trade-off in continual learning?" (p. 2)

> "Specifically, we show that along the path connecting the parameters of the old and new tasks, there always exists a point where the cumulative loss across all tasks is lower than at either endpoint." (p. 2)

> "updating the Fisher information is computationally efficient, taking only 0.69s per task – comparable to training for a single epoch – and our method adds no overhead during inference." (p. 9)

> "Second, due to the model's poor performance on CIFAR-10, it tends to assign a larger weight to CIFAR-10 during parameter merging, leading to limited enhancement for other tasks." (p. 16)
