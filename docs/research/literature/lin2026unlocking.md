# lin2026unlocking — Unlocking the Potential of Continual Model Merging: An ODE Perspective

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 140 claims: 2 wrong table cells, checked on the page and corrected; 5 overstatements or unsupported details, and 3 omissions, all fixed)
- **Reference:** Lin, Kang; preprint, 2026; arXiv 2605.19409 ([references.bib](references.bib))
- **Version read:** arXiv v3, 21 pages: main text pp. 1–9 (with conclusion, impact statement and acknowledgments on p. 9), references pp. 9–11, appendix pp. 12–21
- **Read:** all 21 pages: main text in full; appendix overview and A (theorem proofs, pp. 12–14), B (experimental settings and more results, pp. 14–17, with Figures 5–8 and Tables 6–7; Figure 8, p. 21, is the 20-task stream under heterogeneous utility), C (procedure and Algorithm 1, pp. 16, 18), D (baselines under heterogeneous utility, pp. 16–19), E (discussion and limitations, p. 19). The references (pp. 9–11) were only skimmed. Figures 2, 7 and 8 (radar plots, pp. 3, 20, 21) were looked at, not read off: they print no values
- **Code:** <https://github.com/yohbii/ODE-M> (p. 1, footnote)

## In one paragraph

The paper studies **continual model merging (CMM)**: task-adapted models from the same pre-trained backbone arrive one at a time, and the deployed merged model is updated after each arrival without retraining (p. 2).

Instead of a one-step merge rule, **ODE-M** treats each update as a trajectory in parameter space from the current merged model $\theta_0 = \Psi_k$ to the incoming model $\theta_1 = \psi_{k+1}$ (p. 2):

- The trajectory follows a velocity field that points toward $\theta_1$, whose loss-increasing component (along the loss gradient on a small **calibration set**) is damped (pp. 4–5).
- The next merged model is the point reached at an **operating time** $t_k = w_k / \sum_{i=1}^k w_i$, which reduces to $1/k$ with equal task utilities (p. 5).

The paper also proposes **utility-weighted** versions of the ACC and BWT metrics (p. 3).

On CLIP ViT-B/32, ViT-B/16 and ViT-L/14 with streams of 8, 14 and 20 image classification tasks:

- ODE-M has the highest final ACC among the merging methods in every setting (the C. Fine-Tuned row is higher in 2 columns: ViT-B/32 and ViT-L/14 with 8 tasks), e.g. 79.6 vs 75.5 for OPCM on ViT-B/32 with 8 tasks (Table 1, p. 6),
- while its BWT is often worse than the baselines, especially on 20-task streams (Table 1, p. 6).

## Problem

How to update a deployed merged model when task-adapted models arrive sequentially, so that the update controls both **where** the next model lies and **how much** previously accumulated knowledge is kept relative to the incoming task (p. 2).

**Setting** (p. 2, p. 3, p. 14):

- A stream $\{\psi_k\}_{k=1}^K \subset \mathbb{R}^d$ of trained models, each specialized for a task or domain, all in the same parameter space (p. 2).
- All task models are fine-tuned from the same pre-trained CLIP backbone $\psi_0$, each with a task-specific classification head (p. 14).
- After receiving $\psi_k$, the merging algorithm updates the deployed model "without additional training on past-task data (unless explicitly stated)" (p. 14).

**Two criticisms of existing CMM methods** (p. 2):

- An endpoint-only update rule doesn't regulate the transition between current and incoming models; if it passes through high-loss regions, the result may suffer functional degradation and interference.
- It gives only a coarse handle on the stability–plasticity trade-off, since the relative contribution of old and new model is set implicitly by the merging rule.

**Objective mismatch** (p. 3): macro-averaging over tasks "is equivalent to evaluating the deployed model under a uniform mixture over tasks".

Tasks may differ in frequency or importance, so the paper models system performance as an expected utility under a non-uniform task mixture (p. 3).

## Method

**Continual merging** (Eq. 1, p. 3), with $\mathcal{M}$ the merging algorithm and $\psi_0$ the pre-trained weights:

$$\Psi_{k+1} = \mathcal{M}(\Psi_k, \psi_{k+1}, \psi_0), \quad \Psi_1 = \psi_1$$

**Utility-weighted metrics** (Eqs. 2–3, p. 3). Each task $\mathcal{T}_i$ has a non-negative weight $w_i$; $a_{k,i}$ is the performance of $\Psi_k$ on $\mathcal{T}_i$ after merging the first $k$ tasks:

$$\mathrm{ACC}_w(\Psi_k) = \frac{1}{\sum_{i=1}^k w_i} \sum_{i=1}^k w_i \, a_{k,i}$$

$$\mathrm{BWT}_w(\Psi_k) = \frac{1}{\sum_{i=1}^{k-1} w_i} \sum_{i=1}^{k-1} w_i \, (a_{k,i} - a_{i,i})$$

With uniform $w_i$ these are the standard macro-averaged ACC and BWT (p. 3).

**Path formulation** (Eq. 4, p. 4). For one update, $\theta_0 = \Psi_k$ (current), $\theta_1 = \psi_{k+1}$ (incoming) (p. 3); a continuous path:

$$\theta : [0, 1] \to \mathbb{R}^d, \quad \theta(0) = \theta_0, \ \theta(1) = \theta_1$$

**Loss barrier** (Definition 3.1, Eq. 5, p. 4; from Entezari et al., 2021), along the linear path:

$$\sup_t \big[\mathcal{L}(t\theta_1 + (1-t)\theta_0)\big] - \big[t\mathcal{L}(\theta_1) + (1-t)\mathcal{L}(\theta_0)\big]$$

**Loss barrier along a path** (Definition 3.2, Eq. 6, p. 4), and the goal of minimizing it (Eq. 7, p. 4):

$$B(\theta) = \sup_t \big[\mathcal{L}(\theta(t))\big] - \big[t\mathcal{L}(\theta_1) + (1-t)\mathcal{L}(\theta_0)\big]$$

$$\min_{\theta(\cdot)} B(\theta) \quad \text{s.t.} \quad \theta(0) = \theta_0, \ \theta(1) = \theta_1$$

**Base velocity field** (Eqs. 8–10, p. 4). The linear path $\theta(t) = t\theta_1 + (1-t)\theta_0$ has constant velocity $\frac{d\theta}{dt} = \theta_1 - \theta_0$; extended to the whole parameter space:

$$\frac{\partial \theta}{\partial t} = u_t(\theta) = \alpha(t)(\theta_1 - \theta), \quad \alpha(t) = \frac{1}{1-t}$$

$\alpha(t)$ is a "velocity scheduler", set to $\frac{1}{1-t}$ so the field yields a constant velocity (p. 4).

**Decomposition along the loss gradient** (Eq. 11, p. 4), with $g_t = \nabla_{\theta_t}\mathcal{L}$ and $\mathcal{P}_{g_t}$ the projection onto the span of $g_t$:

$$u_\parallel = \mathcal{P}_{g_t}(u_t) \triangleq \frac{\langle u_t, g_t \rangle}{\|g_t\|^2} g_t, \quad u_\perp = (I - \mathcal{P}_{g_t}) u_t$$

$u_\parallel$ changes the loss most directly; $u_\perp$ moves along the tangent space of the local iso-loss manifold (p. 4).

**Rectified field** (Eq. 12, p. 4), with an adaptive factor $\gamma(\theta, t) \in [0, 1]$:

$$v_t(\theta) = u_\perp + \gamma(\theta, t) u_\parallel$$

**Choice of $\gamma$** (Eqs. 13–14, p. 5), with $\Delta\mathcal{L} = \mathcal{L}(\theta_1) - \mathcal{L}(\theta_0)$:

$$\gamma(\theta, t) = 1 \quad \text{if } \langle g_t, u_t \rangle \le 0$$

$$\gamma(\theta, t) = \mathrm{clip}\left(\frac{\Delta\mathcal{L}}{\langle g_t, u_t \rangle}, 0, 1\right) \quad \text{if } \langle g_t, u_t \rangle > 0$$

In words: motion that decreases or keeps the loss is unrestricted; motion that increases it is damped so the loss increase stays within a budget (p. 5).

**Theory** (Section 3.3, p. 5; proofs in Appendix A, pp. 12–14):

- **Theorem 3.3 (convergence)** (p. 5):
  - if $g_t = \nabla\mathcal{L}(\theta(t)) \neq 0$ for almost every $t \in [0, 1)$, and there is $\rho \in [0, 1)$ with $\frac{\|\mathcal{P}_{g_t}(u_t)\|}{\|u_t\|} \le \rho$ along the trajectory,
  - then the trajectory admits a continuous endpoint extension at $t = 1$ and $\lim_{t \to 1} \theta(t) = \theta_1$ (Eq. 15).
- The proof gives the rate $\|e(t)\| \le \|e(0)\| (1-t)^{1-\rho}$ for $t \in [0, 1)$, with $e(t) = \theta(t) - \theta_1$ (Eq. 31, p. 13).
- **Theorem 3.4 (bounded loss barrier)** (p. 5): assuming a continuous endpoint extension $\theta(1) = \theta_1$ and differentiable $\gamma$ and $\mathcal{L}$, for all $t \in [0, 1)$:

  $$\mathcal{L}(\theta(t)) \le \mathcal{L}(\theta_0) + t \cdot \max\{\Delta\mathcal{L}, 0\} \quad (16)$$

  $$B(\theta) \le \max\{\mathcal{L}(\theta_0) - \mathcal{L}(\theta_1), 0\} \quad (17)$$

**Operating time** (Section 3.4, Eq. 18, p. 5). With $w_k$ the utility of task $k$ and $W_{k-1} = \sum_{i=1}^{k-1} w_i$:

$$t_k = \frac{w_k}{W_{k-1} + w_k} = \frac{w_k}{\sum_{i=1}^k w_i}, \quad \Psi_k = \theta(t_k)$$

- With equal utilities, $t_k = 1/k$, so the retained contribution of the previous merged model grows as $(k-1)/k$ (p. 5).
- A smaller operating time keeps more historical knowledge; a larger one gives more influence to the incoming model (p. 5).

**Algorithm 1** (p. 18; description in Appendix C, p. 16).

Inputs:

- the stream $\{\psi_k\}_{k=1}^K$, $\psi_0$,
- a calibration set $\mathcal{D}_{\text{cal}}$,
- a loss $\mathcal{L}(\theta; \mathcal{D}_{\text{cal}})$,
- step size $h$,
- scheduler $\alpha(t)$,
- time rule $t_k$.

Steps:

1. $\Psi_1 \leftarrow \psi_1$.
2. For $k = 2, \dots, K$: $\theta_0 \leftarrow \Psi_{k-1}$, $\theta_1 \leftarrow \psi_k$, $\theta \leftarrow \theta_0$, $t \leftarrow 0$.
3. While $t < t_k$:
   - $g \leftarrow \nabla_\theta \mathcal{L}(\theta; \mathcal{D}_{\text{cal}})$; $u \leftarrow \alpha(t)(\theta_1 - \theta)$;
   - $u_\parallel \leftarrow \frac{\langle u, g \rangle}{\|g\|^2} g$, $u_\perp \leftarrow u - u_\parallel$;
   - $\Delta\mathcal{L} \leftarrow \mathcal{L}(\theta_1; \mathcal{D}_{\text{cal}}) - \mathcal{L}(\theta_0; \mathcal{D}_{\text{cal}})$;
   - $\gamma \leftarrow 1$ if $\langle g, u \rangle \le 0$, else $\gamma \leftarrow \mathrm{clip}(\Delta\mathcal{L} / \langle g, u \rangle, 0, 1)$;
   - $v \leftarrow u_\perp + \gamma u_\parallel$; $\theta \leftarrow \theta + h v$ (Euler update); $t \leftarrow t + h$.
4. $\Psi_k \leftarrow \theta$. Return $\Psi_K$.

Note the appendix indexes the update as $\Psi_{k-1}, \psi_k \to \Psi_k$ (p. 16, p. 18), the main text as $\Psi_k, \psi_{k+1} \to \Psi_{k+1}$ (p. 2).

**Cost** (p. 16): each merge needs $O(\lceil t_k / h \rceil)$ first-order gradient evaluations on $\mathcal{D}_{\text{cal}}$.

**Our reading:**

- With $\gamma \equiv 1$, $v_t = u_t$ and the trajectory is the linear path, so ODE-M stopped at $t_k = 1/k$ would give $\Psi_k = (1 - 1/k)\Psi_{k-1} + (1/k)\psi_k$, the running average (the C.SWA recursion of Eq. 45, p. 17).
  - ODE-M is therefore a gradient-rectified version of continual weight averaging, not of task arithmetic with a $\lambda$.
- With $h = 0.05$ and $t_k = 1/k$, the number of Euler steps $\lceil t_k / h \rceil$ falls from 10 at $k = 2$ to 1 at $k = 20$: late in long streams the trajectory is a single rectified step.
- $\Delta\mathcal{L}$ depends only on the endpoints, so it is constant within one merge although Algorithm 1 recomputes it inside the loop (p. 18).
- The paper doesn't state which loss $\mathcal{L}$ is used on $\mathcal{D}_{\text{cal}}$, nor whether the classification heads enter the merge.
  - With classification heads, cross-entropy on labeled calibration samples is the natural guess, but it isn't written.

## Experimental setup

**Models** (p. 5, p. 6, p. 14):

- CLIP image encoders: `openai/clip-vit-base-patch32` (ViT-B/32), `openai/clip-vit-base-patch16` (ViT-B/16), `openai/clip-vit-large-patch14` (ViT-L/14) (p. 14).
- Task-adapted models:
  - "We obtain the stream of task-adapted models and the corresponding datasets from FusionBench (Tang et al., 2025a) by fine-tuning each pre-trained backbone sequentially on 20 tasks" (p. 6);
  - §4.2 adds "we construct a set of task-specific fine-tuned checkpoints starting from the same CLIP pre-trained weights" (p. 6),
  - and p. 14 says each model comes from fine-tuning the backbone on its task: so "sequentially" means one task after another, each from the pre-trained weights, each with a task-specific classification head (p. 14);
  - the setup follows OPCM (Tang et al., 2025b) (p. 5).

**Task streams** (p. 14):

- **8 tasks:** SUN397, Stanford-Cars, RESISC45, EuroSAT, SVHN, GTSRB, MNIST, DTD.
- **14 tasks:** the 8 plus Flowers102, PCAM, FER2013, Oxford-IIITPet, STL10, CIFAR100.
- **20 tasks:** the 14 plus CIFAR10, Food101, FashionMNIST, EMNIST, KMNIST, RenderedSST2.
- At step $k$, the merged model is evaluated on the test split of all tasks seen so far (p. 14).
- Each setting is repeated over **10 randomly permuted task orders**, results aggregated (p. 6).

**Metrics:** ACC and BWT (Lin et al., 2022) (p. 6); their utility-weighted versions $\mathrm{ACC}_w$, $\mathrm{BWT}_w$ for Section 4.3 (p. 3, p. 6).

**Baselines** (p. 6): parameter averaging (SWA), Continual Task Arithmetic, Continual Ties-Merging, OPCM.

Their utility-aware forms (Appendix D, pp. 16–19), with $W_k = \sum_{i=1}^k w_i$ (Eq. 43) and $\eta_k = w_k / W_k$ (Eq. 44, p. 17), which is $1/k$ with equal utilities:

- **Continual averaging** (Eqs. 45–46, p. 17):

  $$\Psi_k^{\text{C.SWA}} = (1 - \eta_k)\Psi_{k-1}^{\text{C.SWA}} + \eta_k \psi_k = \sum_{i=1}^k \frac{w_i}{W_k} \psi_i$$

- **Continual Task Arithmetic** (Eqs. 47–49, pp. 17–18), with $\delta_k = \psi_k - \psi_0$:

  $$\bar\delta_k^{\text{TA}} = (1 - \eta_k)\bar\delta_{k-1}^{\text{TA}} + \eta_k \delta_k, \quad \Psi_k^{\text{C.TA}} = \psi_0 + \lambda_{\text{TA}} \bar\delta_k^{\text{TA}}$$

  With $\lambda_{\text{TA}} = 1$ this reduces to weighted averaging (p. 18). The value of $\lambda_{\text{TA}}$ used isn't given.

- **Continual Ties-Merging** (Eqs. 50–53, p. 18):
  - a pairwise Ties merge of $(1 - \eta_k)\Delta_{k-1}^{\text{TIES}}$ and $\eta_k \delta_k$, with $\Delta_{k-1}^{\text{TIES}} = \Psi_{k-1}^{\text{C.TIES}} - \psi_0$,
  - then $\Psi_k^{\text{C.TIES}} = \psi_0 + \lambda_{\text{TIES}} \bar\delta_k^{\text{TIES}}$;
  - trimming ratio, sign election and $\lambda_{\text{TIES}}$ follow the OPCM configuration (p. 18).
- **OPCM** (Eqs. 54–58, pp. 18–19):
  - the incoming task vector is projected with OPCM's orthogonal projection, $\hat\delta_k = \mathcal{P}_\alpha^{(k-1)}(\delta_k; \Delta_{k-1}^{\text{OPCM}})$ (applied to weight matrices of linear layers);
  - $A_k^{\text{OPCM}} = (1 - \eta_k)A_{k-1}^{\text{OPCM}} + \eta_k \hat\delta_k$;
  - $\Psi_k^{\text{OPCM}} = \psi_0 + A_k^{\text{OPCM}} / \lambda_k^{\text{OPCM}}$, with $\lambda_k^{\text{OPCM}}$ from OPCM's original scaling strategy (p. 19).

**ODE-M implementation** (p. 6, p. 16):

- Calibration set: "aggregates samples from previously seen tasks, with a total of 1024 examples" (p. 6); $|\mathcal{D}_{\text{cal}}| = 1024$ unless stated otherwise (p. 16).
- Euler integration, fixed step size $h = 0.05$ (p. 6, p. 16).

**Heterogeneous utility** (Section 4.3, p. 6): in each run, $\{w_i\}$ are sampled "from a fixed distribution" and normalized so that $\sum_i w_i = 1$; 10 independent draws.

The distribution itself isn't specified.

Baselines' sequential coefficients are modified to respect $\{w_i\}$ (p. 6, p. 7).

## Results

**Main results, uniform utility** (Table 1, p. 6). Final ACC and BWT (%), aggregated over 10 task orders (p. 6); the caption doesn't say what ± denotes. "C." marks continual variants (p. 6).

| Method | B/32 8 | B/32 14 | B/32 20 | B/16 8 | B/16 14 | B/16 20 | L/14 8 | L/14 14 | L/14 20 |
|---|---|---|---|---|---|---|---|---|---|
| Pre-Trained | 48.1 | 56.9 | 55.6 | 55.4 | 62.0 | 59.8 | 64.9 | 69.1 | 65.6 |
| Fine-Tuned | 90.4 | 89.3 | 89.8 | 92.4 | 91.3 | 91.6 | 94.3 | 93.4 | 93.5 |
| C. Fine-Tuned | 79.8 | 67.4 | 62.6 | 82.9 | 72.2 | 68.2 | 90.0 | 70.9 | 77.7 |
| **ACC ↑** | | | | | | | | | |
| Average (SWA) | 66.3±0.0 | 65.4±0.0 | 61.1±0.0 | 72.3±0.0 | 69.7±0.0 | 64.8±0.0 | 80.0±0.0 | 77.5±0.0 | 71.1±0.0 |
| C. Task Arithmetic | 67.5±0.0 | 66.5±0.0 | 60.6±0.0 | 77.1±0.0 | 70.9±0.0 | 64.2±0.0 | 82.1±0.0 | 77.9±0.0 | 70.3±0.0 |
| C. Ties-Merging | 49.0±10.2 | 66.2±0.6 | 59.9±0.7 | 66.8±3.7 | 70.5±0.8 | 63.0±1.6 | 64.3±7.0 | 78.0±0.6 | 68.3±0.9 |
| OPCM | 75.5±0.5 | 71.9±0.3 | 65.7±0.2 | 81.8±0.3 | 77.1±0.5 | 70.3±0.2 | 87.0±0.4 | 83.5±0.2 | 76.0±0.2 |
| ODE-M | 79.6±1.9 | 74.1±1.5 | 67.1±0.8 | 85.3±0.6 | 78.5±0.9 | 70.4±0.5 | 87.7±0.9 | 85.8±1.2 | 81.1±1.0 |
| **BWT ↑** | | | | | | | | | |
| Average (SWA) | -11.5±2.2 | -8.0±1.3 | -7.1±2.1 | -9.7±1.5 | -7.1±1.4 | -7.3±1.7 | -7.3±1.4 | -5.8±1.0 | -6.4±1.5 |
| C. Task Arithmetic | -9.6±1.5 | -1.3±0.3 | -3.4±0.4 | -4.2±1.0 | -1.3±0.4 | -3.6±0.4 | -7.1±0.8 | -1.8±0.3 | -3.3±0.3 |
| C. Ties-Merging | -15.3±8.0 | 1.9±0.6 | -1.5±0.7 | -5.5±0.4 | 1.4±0.7 | -1.5±1.2 | -13.0±5.7 | 1.1±0.4 | -2.9±1.0 |
| OPCM | -6.3±1.1 | -6.0±1.0 | -7.8±1.5 | -4.8±0.7 | -5.1±1.4 | -6.3±3.8 | -2.6±1.0 | -4.3±0.7 | -6.5±1.8 |
| ODE-M | -4.2±3.9 | -7.8±3.2 | -9.4±2.2 | -6.6±2.8 | -8.1±3.0 | -9.9±3.5 | -4.0±2.4 | -7.4±2.5 | -10.3±2.7 |

- The paper's summary: ODE-M "achieves the highest overall accuracy and ranks first for every stream length" (p. 6).
- On BWT:
  - "all methods exhibit negative BWT as the stream grows" and ODE-M "remains competitive with or better than prior baselines in most settings, especially for shorter streams";
  - improving ACC "can come with a more aggressive update and thus more negative BWT in some long-stream configurations" (p. 6).
- The paper doesn't define the "Fine-Tuned" and "C. Fine-Tuned" rows.
  - **Our reading:**
    - "Fine-Tuned" is presumably the individual task models, each on its own task, and "C. Fine-Tuned" sequential fine-tuning on the stream; there is **no joint multi-task training** baseline.
    - C. Fine-Tuned beats ODE-M in 2 columns: ViT-B/32 8 tasks (79.8 vs 79.6) and ViT-L/14 8 tasks (90.0 vs 87.7) (Table 1, p. 6).
- **Our reading:**
  - ODE-M's BWT is the worst of all methods in 5 of 9 columns (B/32 20, B/16 14 and 20, L/14 14 and 20) and second worst in B/32 14 and B/16 8 (7 of 9 columns worst or second worst; best only in B/32 8, −4.2),
  - and C. Ties-Merging even has positive BWT on 14-task streams;
  - a high final ACC here goes with more forgetting, not less.

**Heterogeneous utility** (Table 2, p. 8). $\mathrm{ACC}_w$ and $\mathrm{BWT}_w$ (%), over 10 draws of $\{w_i\}$ (p. 6); the caption doesn't say what ± denotes:

| Method | B/32 8 | B/32 14 | B/32 20 | B/16 8 | B/16 14 | B/16 20 | L/14 8 | L/14 14 | L/14 20 |
|---|---|---|---|---|---|---|---|---|---|
| **ACC_w ↑** | | | | | | | | | |
| Average (SWA) | 65.1±0.9 | 64.3±0.8 | 60.2±0.7 | 71.5±0.9 | 69.2±0.8 | 63.7±0.8 | 79.2±0.8 | 76.8±0.7 | 70.0±0.7 |
| C. Task Arithmetic | 66.8±0.8 | 65.7±0.9 | 60.0±0.8 | 76.3±0.8 | 70.5±0.7 | 63.4±0.8 | 81.5±0.7 | 77.1±0.7 | 69.5±0.7 |
| C. Ties-Merging | 58.4±6.1 | 65.0±1.4 | 59.1±1.2 | 69.1±3.0 | 70.0±1.2 | 62.0±1.5 | 72.0±4.5 | 77.3±1.0 | 67.0±1.2 |
| OPCM | 74.2±0.7 | 70.8±0.6 | 64.5±0.5 | 81.0±0.6 | 76.5±0.6 | 69.4±0.6 | 86.2±0.6 | 82.9±0.6 | 75.0±0.6 |
| ODE-M | 77.9±1.4 | 73.2±1.1 | 66.0±0.9 | 84.6±0.7 | 78.0±0.8 | 70.0±0.6 | 87.0±0.8 | 84.6±0.9 | 80.0±0.8 |
| **BWT_w ↑** | | | | | | | | | |
| Average (SWA) | -10.8±1.8 | -7.6±1.3 | -6.9±1.6 | -9.0±1.6 | -6.8±1.2 | -7.1±1.4 | -6.8±1.2 | -5.4±0.9 | -6.1±1.2 |
| C. Task Arithmetic | -8.7±1.5 | -1.6±0.5 | -3.1±0.7 | -3.9±1.2 | -1.5±0.6 | -3.3±0.6 | -5.5±0.8 | -1.9±0.5 | -3.0±0.5 |
| C. Ties-Merging | -12.0±5.5 | 1.1±0.9 | -1.2±1.0 | -5.0±1.8 | 0.8±0.9 | -1.3±1.3 | -9.5±3.8 | 0.6±0.7 | -2.5±1.1 |
| OPCM | -5.9±1.0 | -5.6±0.9 | -7.0±1.4 | -4.2±0.9 | -4.6±1.2 | -5.8±2.5 | -2.8±0.8 | -4.1±0.8 | -5.9±1.5 |
| ODE-M | -5.8±1.6 | -4.9±1.4 | -8.1±1.7 | -4.5±1.1 | -5.9±1.2 | -6.2±1.9 | -2.5±1.0 | -4.4±1.1 | -7.8±1.4 |

- The text states ODE-M improves $\mathrm{ACC}_w$ over OPCM "from 74.2 to 77.9 on ViT-B/32 with 8 tasks, from 81.0 to 84.6 on ViT-B/16 with 8 tasks", and "from 75.0 to 80.0 at 20 tasks" on ViT-L/14 (p. 7); these match Table 2.
- The text also states ODE-M "improves upon OPCM in $\mathrm{BWT}_w$ across all settings (e.g., from −5.9 to −4.8 on ViT-B/32 with 8 tasks and from −5.9 to −4.8 on ViT-L/14 with 20 tasks)" (p. 7).
  - **Our reading:** Table 2 doesn't support this:
    - on ViT-B/32 with 8 tasks it prints OPCM −5.9, ODE-M −5.8;
    - on ViT-L/14 with 20 tasks OPCM −5.9, ODE-M −7.8;
    - and ODE-M is below OPCM in 6 of 9 columns.

**Calibration set size** (Table 3, p. 8). Average accuracy (%) of ODE-M, 8-task stream, mean ± std over 5 runs, by number of calibration samples $n$:

| Model | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 |
|---|---|---|---|---|---|---|---|---|---|
| ViT-B/32 | 62.8±3.5 | 64.9±3.0 | 70.1±2.6 | 73.0±2.3 | 75.0±2.1 | 76.8±2.0 | 79.4±1.9 | 79.6±1.5 | 79.8±1.8 |
| ViT-B/16 | 68.5±1.6 | 70.6±1.3 | 75.8±1.1 | 78.7±0.9 | 80.7±0.8 | 82.5±0.7 | 85.1±0.6 | 85.3±0.4 | 85.1±0.6 |
| ViT-L/14 | 70.9±1.8 | 73.0±1.5 | 78.2±1.3 | 81.1±1.1 | 83.1±1.0 | 84.9±0.9 | 87.5±0.8 | 87.7±0.9 | 87.8±0.9 |

The paper: diminishing returns beyond a moderate budget, "a few hundred samples already provide strong accuracy" (p. 7).

**Our reading:** with $n \le 128$, ODE-M on ViT-B/32 (62.8–75.0) is below OPCM's 75.5 (Table 1), which needs no calibration data.

**Euler step size** (Table 4, p. 8). Average accuracy (%), ViT-B/32, 8-task stream, five trials:

| Step size | 1e-3 | 2.5e-3 | 5e-3 | 1e-2 | 2.5e-2 | 5e-2 | 1e-1 | 2e-1 |
|---|---|---|---|---|---|---|---|---|
| ViT-B/32 | 80.2 ± 0.5 | 80.1 ± 0.5 | 80.0 ± 0.5 | 79.8 ± 0.5 | 79.6 ± 0.6 | 79.4 ± 0.6 | 79.5 ± 0.6 | 78.7 ± 0.7 |

- The paper uses 5e-2 "as a robust default" (p. 7).
- The text gives "80.0 ± 0.5 at $10^{-2}$" (p. 7), while Table 4 prints 79.8 ± 0.5 for 1e-2 and 80.0 ± 0.5 for 5e-3 (p. 8).
- The default step 5e-2 gives 79.4 ± 0.6 in Table 4 (p. 8), against 79.6±1.9 in Table 1 (p. 6) and 79.6±1.5 at $n$ = 1024 in Table 3 (p. 8) for what should be the same configuration.

**Runtime** (Table 5, p. 8): average wall-clock time to merge one incoming model over a 20-task stream:

- 123.9 s (ViT-B/32),
- 200.8 s (ViT-B/16),
- 246.8 s (ViT-L/14).

The cost is mainly numerical integration with per-step gradients on the calibration set (p. 7).

The hardware isn't stated.

**Two-task trajectory sweeps** (Table 6, p. 17).

Accuracy along the ODE trajectory from $\theta_0$ (first task's model, $t = 0$) to $\theta_1$ (second task's model, $t = 1$); bold in the paper marks the best Avg:

| Pair | Metric | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cars → resisc45 | cars | 0.785 | 0.788 | 0.782 | 0.772 | 0.787 | 0.763 | 0.698 | 0.658 | 0.605 | 0.541 | 0.472 |
| | resisc45 | 0.513 | 0.691 | 0.756 | 0.833 | 0.936 | 0.939 | 0.938 | 0.946 | 0.950 | 0.951 | 0.951 |
| | Avg | 0.649 | 0.739 | 0.769 | 0.803 | 0.821 | **0.851** | 0.818 | 0.802 | 0.777 | 0.746 | 0.712 |
| sun397 → eurosat | sun397 | 0.749 | 0.752 | 0.750 | 0.743 | 0.749 | 0.731 | 0.683 | 0.653 | 0.609 | 0.554 | 0.490 |
| | eurosat | 0.467 | 0.704 | 0.865 | 0.950 | 0.971 | 0.979 | 0.983 | 0.987 | 0.988 | 0.990 | 0.991 |
| | Avg | 0.608 | 0.728 | 0.808 | 0.847 | 0.850 | **0.855** | 0.833 | 0.820 | 0.798 | 0.772 | 0.740 |
| dtd → resisc45 | dtd | 0.797 | 0.798 | 0.785 | 0.784 | 0.774 | 0.751 | 0.626 | 0.557 | 0.487 | 0.418 | 0.359 |
| | resisc45 | 0.377 | 0.544 | 0.692 | 0.802 | 0.874 | 0.935 | 0.935 | 0.945 | 0.951 | 0.953 | 0.951 |
| | Avg | 0.587 | 0.671 | 0.739 | 0.793 | 0.824 | **0.843** | 0.781 | 0.751 | 0.719 | 0.685 | 0.655 |
| gtsrb → resisc45 | gtsrb | 0.989 | 0.988 | 0.986 | 0.983 | 0.976 | 0.962 | 0.878 | 0.728 | 0.541 | 0.357 | 0.243 |
| | resisc45 | 0.205 | 0.346 | 0.522 | 0.695 | 0.811 | 0.930 | 0.931 | 0.939 | 0.946 | 0.950 | 0.951 |
| | Avg | 0.597 | 0.667 | 0.754 | 0.839 | 0.893 | **0.946** | 0.904 | 0.834 | 0.743 | 0.653 | 0.597 |
| gtsrb → svn | gtsrb | 0.989 | 0.988 | 0.986 | 0.982 | 0.971 | 0.962 | 0.868 | 0.745 | 0.571 | 0.404 | 0.273 |
| | svn | 0.411 | 0.564 | 0.713 | 0.832 | 0.905 | 0.950 | 0.960 | 0.969 | 0.972 | 0.973 | 0.973 |
| | Avg | 0.700 | 0.776 | 0.850 | 0.907 | 0.938 | **0.956** | 0.914 | 0.857 | 0.771 | 0.689 | 0.623 |

The backbone for Table 6 isn't stated.

**Our reading:**

- in all five pairs the printed Avg row is best at $t = 0.5$, which is $t_k = 1/k$ for $k = 2$;
- but in two pairs the printed Avg doesn't match its own rows at $t = 0.4$:
  - cars→resisc45: (0.787 + 0.936)/2 = 0.8615, printed 0.821;
  - sun397→eurosat: (0.749 + 0.971)/2 = 0.860, printed 0.850,
- and recomputed, those two pairs peak at $t = 0.4$ (p. 17).

**Operating time vs. the $1/k$ schedule** (Table 7, p. 17).

At each merge, candidate operating times $t \in [0, 1]$ at interval 0.05 are evaluated and the best $t_k^\star$ is chosen "according to validation performance" (pp. 15–16).

Spearman rank correlation between $\{1 - t_k^\star\}$ and $\{(k-1)/k\}$:

| Architecture | 8 tasks | 14 tasks | 20 tasks |
|---|---|---|---|
| ViT-B/32 | 0.941 | 0.907 | 0.884 |
| ViT-B/16 | 0.953 | 0.921 | 0.896 |
| ViT-L/14 | 0.936 | 0.912 | 0.889 |

The paper reads this as support for the schedule $t_k = 1/k$ and its utility-aware extension (p. 16).

**Statistics of $\gamma$ and of the alignment ratio** (Figures 5–6, pp. 15–16, 2D histograms, no printed values):

- $\gamma$: the paper reports that the mass "concentrates near $\gamma \approx 1$ over a large portion of the trajectory", with smaller values in localized regions (p. 15).
- $\|\mathcal{P}_{g_t}(u_t)\| / \|u_t\|$: "remains largely concentrated below moderate values throughout the trajectory", consistent with the $\rho < 1$ assumption of Theorem 3.3 (p. 15).
- **Our reading** of Figure 6 (p. 16): a dense band also sits at a ratio of 1.0 along the whole trajectory, so the ratio isn't bounded below 1 everywhere.

**Per-task results** (Figures 2, 7, 8; pp. 3, 20, 21): radar plots of per-task accuracy for the 8- and 20-task streams, no printed values.

## Assumptions and limitations

- **Data from past tasks at merge time:** the calibration set aggregates samples from previously seen tasks (p. 6).
  - The authors state that the method "requires access to a loss function and first-order gradients on a calibration set during merging", which may not hold in black-box deployment, and that results depend on how representative the calibration data is (p. 19).
- **Numerical choices** (step size, time schedule) matter; "extremely coarse discretization or poorly chosen schedules can still degrade performance" (p. 19).
- **Only vision classification:** CLIP ViT backbones and image classification streams; other modalities and larger models are left to future work (p. 19, p. 9).
- **Merge-time overhead:** 123.9–246.8 s per merge (Table 5, p. 8); more efficient integration is future work (p. 9).
- **Theory assumptions:** non-zero gradient almost everywhere and a bound $\rho < 1$ on the alignment ratio (Theorem 3.3, p. 5); differentiable $\gamma$ and $\mathcal{L}$ (Theorem 3.4, p. 5).
- **Our reading:**
  - The calibration set is a small replay buffer: ODE-M isn't data-free, unlike the merging baselines it is compared with, and the comparison doesn't give those baselines the same data.
  - Higher final ACC comes with lower BWT than most baselines on 14- and 20-task streams (Table 1, p. 6).
  - The text's claims on $\mathrm{BWT}_w$ (p. 7) and on the step size 1e-2 (p. 7) don't match the tables (pp. 8).
  - Theorem 3.4 assumes a differentiable $\gamma$, while $\gamma$ is defined with a clip and a case split (p. 5).
  - Unstated: the loss used on $\mathcal{D}_{\text{cal}}$, how heads are handled, $\lambda_{\text{TA}}$, the utility distribution, the backbone of Table 6, the validation data used for $t_k^\star$, and the hardware.
  - No joint multi-task training baseline.

## Relevance to this thesis

**Our reading:**

- **Baseline definitions for sequential merging:** the paper gives explicit recursions for continual averaging (Eq. 45), continual task arithmetic with $\lambda_{\text{TA}}$ (Eqs. 47–49) and continual Ties (Eqs. 50–53), all driven by the ratio $\eta_k = w_k / W_k$.
  - These are a ready template for our sequential merging baselines, and the $\eta_k$ form lets us weight periods differently (e.g. favor recent periods of a drifting signal).
- **A third option between joint training and merging:** ODE-M merges with gradients from a small replay set of past tasks.
  - For time series this is cheap to try:
    - forecasting has a natural loss (e.g. MSE on calibration windows),
    - and reconstruction-based anomaly detection can use an unsupervised loss on normal data, so no labels are needed.
  - It sits between data-free merging and joint training on all data; the comparison must state how much past data each method sees.
- **Joint training is missing here:** the paper compares only to individual and sequentially fine-tuned models (Table 1, p. 6).
  - Our joint-training vs. task-arithmetic comparison has to add that reference itself.
- **What to measure, following the paper:**
  - the loss barrier between the current merged model and the incoming model (Eqs. 5–6),
  - ACC and BWT per step,
  - and the two-model sweeps of Table 6 (accuracy along the path at $t \in \{0, 0.1, \dots, 1\}$).
  - For successive periods of the same signal, barriers may be much lower than between unrelated image tasks.
- **The $1/k$ schedule** (Eq. 18) is the running average.
  - Testing whether the best operating time follows $1/k$ (Table 7) is a direct check for streams of time-series tasks, where the newest data may matter more than $1/k$ allows.
- **Forgetting vs. final accuracy:** the paper's best-ACC method also forgets more on long streams (Table 1); we should report both and not rank on ACC alone.
- **Practical cost:** with 1024 calibration samples and $h = 0.05$, a merge takes minutes on ViT-sized models (Table 5); our models are likely much smaller, so the cost should matter less.

## Quotes worth keeping

> "ODE-M constructs a barrier-aware trajectory using a rectified time-dependent velocity field, where lightweight first-order feedback from a small calibration set suppresses loss-increasing motion while preserving progress toward the incoming model." (p. 1)

> "Specifically, macro-average is equivalent to evaluating the deployed model under a uniform mixture over tasks, where each task is assumed to be equally likely to occur and equally costly to degrade." (p. 3)

> "A smaller operating time keeps the merged model closer to the previously accumulated model, thereby preserving more historical knowledge, whereas a larger operating time assigns more influence to the incoming task model." (p. 5)

> "While improving ACC can come with a more aggressive update and thus more negative BWT in some long-stream configurations, the overall results suggest that our method provides a favorable accuracy–stability trade-off across architectures and task horizons." (p. 6)

> "Our approach requires access to a loss function and first-order gradients on a calibration set during merging." (p. 19)
