# wang2026revitalizing — Revitalizing the Beginning: Avoiding Storage Dependency for Model Merging in Continual Learning

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 150 claims, no wrong numbers: 1 misstatement, 1 wrong page, 2 rewordings, 4 omissions, all fixed)
- **Reference:** Wang, Deng; preprint, 2026; arXiv 2605.08311 ([references.bib](../references.bib))
- **Version read:** arXiv v1, dated 8 May 2026 (p. 1, side stamp); 13 pages: main text pp. 1–8, references pp. 9–10, appendix pp. 11–13
- **Read:** everything: main text (Sections 1–6, pp. 1–8), references (pp. 9–10), appendices A, B, C.1–C.4 with Tables 8–10 and Figures 6–7 (pp. 11–13)
- **Code:** no code link is given in the paper

## In one paragraph

The paper studies model merging used as a continual learning (CL) strategy under a **strict storage constraint**: after each task, only the merged model of the previous step, the model just fine-tuned on the current task, and the pre-trained model may be kept; no older task vectors, models, Fisher matrices or data (p. 1, p. 2, p. 8). It argues that existing merging methods (TIES, Model Stock, MagMax) then degrade, by up to 6% (p. 1), and traces this to three causes: the merged model sits outside the current task's low-loss basin, its deeper-layer representations drift, and its gradients near the start of the next task are weak ("optimization stagnation") (pp. 3–4). It proposes **Trajectory Regularized Merging (TRM)**: the merged task vector is searched in a 2-dimensional subspace, the line between the previous and current task vectors plus one random orthogonal direction (Eqs. 4–6, p. 4), with coefficients $\alpha, \beta$ optimized on current-task data by a loss with three terms: cross-entropy on the current task, a layer-weighted representation consistency term, and a term that *maximizes* the gradient norm (Eqs. 7–12, pp. 4–5). On class-incremental CIFAR100, ImageNet-R and Stanford Cars with CLIP ViT-B/16 it reports the best last accuracy in 8 of 9 settings (Table 1, p. 6), e.g. 83.2% on ImageNet-R with 10 tasks against 80.1% for MagMax and 86.5% for joint training.

## Problem

How to use model merging for continual learning when nothing from earlier tasks may be stored except the current merged model (pp. 1–2).

**Setting** (Section 3.1, p. 2):

- Supervised continual learning from a pre-trained model $f(\cdot;\theta_{\text{init}})$ that learns a sequence of $\mathcal{T}$ tasks in order.
- Each task dataset $\mathcal{D}^t$ holds different classes $C^t$, with no overlap: $C^i \cap C^j = \emptyset$ for $i \neq j$ (class-incremental).
- Training on task $t$ "is strictly initialized from the model $f(:,\theta_{t-1})$ obtained after task $t-1$" (p. 2).
- Task vector of the model after task $t$: $\tau_t = \theta_t - \theta_{\text{init}}$; superscripts distinguish the fine-tuned model $\tilde{\theta}_t$ from the merged model $\theta_t$ (p. 3).
- The paper's framing of the constraint: "only the current expert and the immediately merged model are available" (p. 1); in the conclusion, "only the pre-task and post-task models are accessible, and the merged model must serve as the initialization for future training" (p. 8).

**Why existing methods break it** (p. 1): most merging methods "require access to all previous task vectors and the initial model during the merging phase", which is "functionally equivalent to storing the entire ensemble of prior experts"; MagMax and BECAME still retain accumulated task vectors or Fisher information matrices.

**Our reading:** the sentence in Section 3.1 that "any previous models or knowledge are permitted to be stored in any form except for $f(:,\theta_{\text{init}})$" (p. 2) reads literally as the opposite of the constraint described elsewhere; we take the intended meaning to be that nothing except the pre-trained model (plus the previous merged model) is stored, which matches p. 1, p. 6 and p. 8.

## Method

### Diagnosis (Section 3.2, pp. 3–4)

Protocol: three disjoint tasks $\{\mathcal{T}_0, \mathcal{T}_1, \mathcal{T}_2\}$ from ImageNet-R, 20 non-overlapping classes each; $\tilde{\theta}_0$ trained on $\mathcal{T}_0$; merging paradigms compared: MagMax, TIES, Model Stock (p. 3). $\tilde{\theta}_1$ is fine-tuned from $\tilde{\theta}_0$ on $\mathcal{T}_1$, and $\theta^{\zeta}_{0,1}$ is the merged model, $\zeta \in \{\text{TIES}, \text{Model Stock}, \text{MagMax}\}$ (p. 3).

- **Suboptimal local convergence** (Figure 1, p. 3): projected on the loss landscape of $\mathcal{T}_1$, the merged models "invariably reside in high loss regimes, far removed from the optimal basins of $\mathcal{T}_1$" (p. 3).
- **Representation drift** (Eq. 1, p. 3), the expected $L_2$ distance between hidden states at layer $l$:

  $$\Delta^l_{out} = \frac{1}{|\mathcal{D}^1|} \sum_{j=1}^{|\mathcal{D}^1|} \left| h^l(x_j;\theta^{\zeta}_{0,1}) - h^l(x_j;\tilde{\theta}_1) \right|_2$$

  The drift "is particularly pronounced in deeper layers" (Figure 2, p. 3).
- **Loss of plasticity** (Eq. 2, p. 3): starting from $\tilde{\theta}_1$ and from $\theta^{\zeta}_{0,1}$, fine-tune on $\mathcal{T}_2$, interpolate along the trajectories, and measure the angle between the gradient at a point and at a neighboring point:

  $$\Delta_\theta(\delta) = \arccos\left( \frac{\langle \nabla_\theta \mathcal{L}(\theta), \nabla_\theta \mathcal{L}(\theta+\delta) \rangle}{|\nabla_\theta \mathcal{L}(\theta)|_2 \, |\nabla_\theta \mathcal{L}(\theta+\delta)|_2} \right)$$

  The merged models show "a strikingly lower angular deviation" than the directly fine-tuned baseline, which the authors read as being trapped in a flat or saturated region (Figure 3, p. 4).

Figure 2 legend values (p. 3), mean $L_2$ distance over the 12 transformer layers (layers 0–11 on the axis):

| Method | Mean (legend) |
|---|---|
| MagMax | 0.9317 |
| TIES | 1.0706 |
| Model Soup | 1.5595 |
| Ours (TRM) | 0.8183 |

The figure legend says "Model Soup" while the text compares Model Stock (p. 3). **Our reading** of the plot: MagMax, TIES and TRM nearly coincide up to layer 5, with Model Soup/Stock about 0.2 higher throughout (about 0.55–0.7 against 0.35–0.5); the distance grows quickly from layer 6–7 onward, most for Model Soup/Stock (up to about 4.3 at layer 11).

### Augmented trajectory subspace (Section 4, p. 4)

Training phase: fine-tuning on task $t$ starts from $\theta_{t-1} := merge(\theta_{t-2}, \tilde{\theta}_{t-1})$ and produces $\tilde{\theta}_t$ with cross-entropy $\mathcal{L}_{ce}$ (p. 4).

Conventional merging in the 1D span of the two task vectors (Eq. 3, p. 4), $\alpha \in [0, 1]$:

$$\tau_{mrg}(\alpha) = \alpha \cdot \tau_t + (1 - \alpha) \cdot \tau_{t-1}$$

Under the CL constraint the admissible subspace "undergoes a catastrophic dimensionality collapse", from a $t$-dimensional subspace spanned by all task vectors to a one-dimensional trajectory between $\tau_{t-1}$ and $\tau_t$ (p. 4).

**Perturbation vector** (Eq. 4, p. 4), with $d = \tau_t - \tau_{t-1}$:

$$P = \text{Normalize}\left( \tilde{r} - \frac{\langle \tilde{r}, d \rangle}{\|d\|^2} d \right), \quad \tilde{r} \sim \mathcal{N}(0, I)$$

The text says $P$ is "orthogonal to $\text{span}(v_{t-1}, v_t)$" (p. 4).

**Augmented merged task vector** (Eq. 5, p. 4), $\alpha, \beta \in \mathbb{R}$ (interpolation and expansion coefficients):

$$\tau_t^{mrg}(\alpha, \beta) = \alpha \cdot \tau_t + (1 - \alpha) \cdot \tau_{t-1} + \beta \cdot P$$

**Merged model** (Eq. 6, p. 4):

$$\theta_t := merge(\theta_{t-1}, \widetilde{\theta}_t) = \theta_{\text{init}} + \tau_t^{mrg}$$

**Our reading:**

- Eq. 4 removes only the component along $d$, so $P$ is orthogonal to $d$ but not, in general, to $\tau_{t-1}$ and $\tau_t$ separately, despite the text's "orthogonal to $\text{span}(v_{t-1}, v_t)$"; the symbols $v_{t-1}, v_t$ aren't defined.
- Since p. 3 defines $\tau_t = \theta_t - \theta_{\text{init}}$ from the *merged* $\theta_t$, which would make Eq. 3 circular, we take, from context (p. 4: "we first construct the task vectors $\tau_{t-1}$ and $\tau_t$"), $\tau_{t-1} = \theta_{t-1} - \theta_{\text{init}}$ (the previous *merged* model) and $\tau_t = \tilde{\theta}_t - \theta_{\text{init}}$ (the current *fine-tuned* model); the paper doesn't write these two out explicitly.
- Only two scalars ($\alpha$, $\beta$) appear to be searched, with a single global $P$; whether $\alpha$, $\beta$ are per-layer isn't stated.

### The three objectives (Sections 4.1–4.3, pp. 4–5)

$\theta^{mrg}_{t-1,t}$ denotes the candidate merged model.

**Task alignment** (Eq. 7, p. 4): empirical risk on the current task.

$$\mathcal{L}_{align} = \mathbb{E}_{(x,y)\sim\mathcal{D}^t} \left[ \mathcal{L}ce\left(f(x;\theta^{mrg}_{t-1,t}), y\right) \right]$$

**Prediction consistency** (Eq. 8, p. 5): the merged model's hidden states stay close to the mean of those of the current fine-tuned model and the previous merged model ("functional centroid").

$$\mathcal{L}_{pre} = \mathbb{E}_{x\sim\mathcal{D}^t} \left[ \sum_{l=1}^{L} \omega_l \left\| h^l(x;\theta^{mrg}_{t-1,t}) - \frac{1}{2}\left( h^l(x;\widetilde{\theta}_t) + h^l(x;\theta_{t-1}) \right) \right\|_2^2 \right]$$

Layer weights (Eq. 9, p. 5), emphasizing higher layers; the 7th layer as dividing point "is based on the results shown in Figure 2" (p. 5):

$$\omega_l = \frac{\exp\left(\max\{1, l-7\}\right)}{\sum_{i=1}^{L} \exp\left(\max\{1, i-7\}\right)}$$

**Our reading:** with this formula, layers $1$–$8$ get the same weight ($e^1$ before normalization) and weights grow from layer 9 on.

**Gradient responsiveness** (Eqs. 10–11, p. 5). The paper calls it "the first-order Taylor expansion of the loss function during a single gradient descent step" (p. 5), but Eq. 10 also includes the second-order (Hessian) term, labeled as such; with learning rate $\eta$ (Eq. 10):

$$\mathcal{L}_{ce}(\theta^+) \approx \mathcal{L}_{ce}(\theta) - \eta \|\nabla_\theta \mathcal{L}_{ce}(\theta)\|_2^2 + \frac{\eta^2}{2} \nabla_\theta \mathcal{L}_{ce}(\theta)^\top H(\hat{\theta}) \nabla_\theta \mathcal{L}_{ce}(\theta)$$

the loss reduction for small $\eta$ is proportional to the squared gradient norm, so the regularizer *maximizes* it (Eq. 11):

$$\mathcal{L}_{res} = -\|\nabla_\theta \mathcal{L}_{ce}(\theta^{mrg}_{t-1,t})\|_2^2$$

The gradient is computed on current-task data, since $\mathcal{D}^{t+1}$ is unavailable; the authors justify this by assuming that successive tasks overlap in low-level features (edges, textures), so the local landscape on $\mathcal{D}^t$ is "a reliable proxy" for $\mathcal{D}^{t+1}$ (p. 5).

**Total objective** (Eq. 12, p. 5), minimized over $\{\alpha, \beta\}$:

$$\mathcal{L}_{total} = \mathcal{L}_{align} + \lambda_1 \mathcal{L}_{pre} + \lambda_2 \mathcal{L}_{res}$$

**Initialization of the search** (p. 5): to avoid early convergence to a local optimum, $\theta_{\text{init}}$ in Eq. 6 is initialized "with a randomly generated point in the search space by randomly place a part parameters in $\theta_0$ from the corresponding positions in $\theta_{t-1}$ and $\tilde{\theta}_t$". The replacement ratio is set to 0.6 (Section 5.4.2, p. 7), where the replacement is said to act on "the parameters in the initial model θ_init" (p. 7): so the p. 5 quote's "θ0" means $\theta_{\text{init}}$.

**Our reading:** this step is underspecified: it seems to replace a random 60% of the entries of the pre-trained weights with entries of $\theta_{t-1}$ or $\tilde{\theta}_t$ before the search, which changes the base point of Eq. 6 away from the pre-trained model; whether the final merged model keeps this modified base isn't stated.

## Experimental setup

**Datasets and protocol** (Section 5.1.1, p. 5):

- Class-incremental learning (CIL) on CIFAR100, ImageNet-R and Stanford Cars, each split into 5, 10 and 20 tasks, following MagMax.
- Extra: ImageNet1K split into 100 tasks of 10 classes (Section 5.4.1, p. 7).
- Extra: domain-incremental learning (DIL) on DomainNet (6 tasks, one per domain) and ImageNet-R (15 tasks), "following the setting of CIL" for the matching CIL splits (C.2, p. 11).

**Metrics** (Section 5.1.2, p. 5): last accuracy (all seen classes after the final task) and average forgetting (average drop from each task's peak to its accuracy after the final task).

**Compared methods** (Section 5.1.3, p. 6): LwF, EWC; PEFT methods L2P, DualPrompt, CODAPrompt, RAPF, CLG-CBM; merging methods Model Stock, TIES; CL merging methods MagMax, PM, BECAME. BECAME is the only one allowed to keep the Fisher information matrix; all others follow the strict constraint; same backbone for all; results re-run "in the same environment and strictly adhering to the source code parameters" (p. 6).

**Implementation** (Section 5.1.4, p. 6):

- Image encoder: OpenAI CLIP ViT-B/16; CLIP's text encoder encodes the labels and is used as the classifier.
- Batch size 128, learning rate $1 \times 10^{-5}$, cosine annealing, AdamW with weight decay 0.1.
- Training: 20 epochs; merging (the $\alpha$, $\beta$ search): 5 epochs, for all datasets.
- $\lambda_1 = 0.1$, $\lambda_2 = 0.01$.
- Everything except the image encoder is frozen.

**Other backbones** (Section 5.4.5, p. 8): ViT-L/14 pre-trained on WebImageText and ViT-B/16 pre-trained on LAION-400M, on ImageNet-R.

## Results

**Last accuracy, class-incremental** (Table 1, p. 6). Columns: number of tasks. Bold in the paper = best, underlined = second; marked here as **b** and _u_. "Zero-shot" and "Joint" have one value per dataset.

| Group | Method (Year) | CIFAR100 5 | 10 | 20 | ImageNet-R 5 | 10 | 20 | Stanford-Cars 5 | 10 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| | Zero-shot | 66.7 | | | 72.2 | | | 64.4 | | |
| | Joint | 89.4 | | | 86.5 | | | 84.4 | | |
| Conventional | LwF (2017) | 68.2 | 67.4 | 67.0 | 66.3 | 60.9 | 55.6 | 65.2 | 61.7 | 57.5 |
| Conventional | EWC (2017) | 69.3 | 64.8 | 57.3 | 74.5 | 66.7 | 54.1 | 65.8 | 61.3 | 58.0 |
| PEFT | L2P (2022) | 77.2 | 73.1 | 68.5 | 77.9 | 75.7 | 72.5 | 67.8 | 66.7 | 65.0 |
| PEFT | DualPrompt (2023) | 77.4 | 73.6 | 70.4 | 78.6 | 75.9 | 73.4 | 68.9 | 67.1 | 65.2 |
| PEFT | CODAPrompt (2023) | 77.3 | 75.0 | 74.1 | 78.9 | 76.0 | 73.7 | 67.4 | 67.4 | 64.9 |
| PEFT | RAPF (2024) | 79.2 | _79.0_ | **79.2** | 80.1 | 79.5 | 78.3 | – | – | – |
| PEFT | CLG-CBM (2025) | 78.1 | 76.8 | 75.9 | 79.2 | 78.8 | 77.5 | _72.8_ | _68.7_ | 64.2 |
| Model Merging | Model Stock (2024) | 76.5 | 70.7 | 68.3 | 79.6 | 77.1 | 76.5 | 66.6 | 64.5 | 64.1 |
| Model Merging | TIES (2023) | 79.8 | 76.3 | 73.6 | 81.5 | 79.5 | 78.4 | 67.9 | 66.1 | 65.3 |
| Model Merging | MagMax (2024) | 80.4 | 75.8 | 72.9 | _82.2_ | _80.1_ | _79.3_ | 68.5 | 65.9 | _65.7_ |
| Model Merging | PM (2025) | – | – | – | 81.4 | 79.9 | 76.3 | – | – | – |
| Model Merging | BECAME (2025) | _80.9_ | 75.2 | 73.5 | 82.1 | 79.8 | 78.7 | – | – | – |
| | **TRM (Ours)** | **83.5** | **80.5** | _78.6_ | **83.6** | **83.2** | **82.7** | **73.2** | **70.4** | **66.9** |

Gains claimed in the text (p. 6): CIFAR100 +3.1% and +1.5% (5 and 10 tasks), slightly below RAPF at 20 tasks; ImageNet-R +1.4%, +3.1%, +3.4%; Stanford Cars +0.4%, +1.7%, +1.2%.

**Our reading:** the CIFAR100 5-task gain of 3.1% matches the gap to MagMax (80.4), not to the second-best BECAME (80.9, gap 2.6). Joint training stays above every CL method in every setting (e.g. ImageNet-R 86.5 vs 83.2 for TRM at 10 tasks).

**Average forgetting** (Table 9, p. 12; lower is better; bold/underline as above):

| Group | Method (Year) | CIFAR100 5 | 10 | 20 | ImageNet-R 5 | 10 | 20 | Stanford-Cars 5 | 10 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| Conv. | LwF (2017) | 18.2 | 22.4 | 26.5 | 15.3 | 19.8 | 24.1 | 16.2 | 20.5 | 25.4 |
| Conv. | EWC (2017) | 14.5 | 19.1 | 28.4 | 10.2 | 16.7 | 22.8 | 12.8 | 18.3 | 23.6 |
| PEFT | L2P (2022) | 4.2 | 5.8 | 7.4 | 3.1 | 4.5 | 5.8 | 5.2 | 6.4 | 7.9 |
| PEFT | DualPrompt (2023) | 3.8 | 5.1 | 6.9 | 2.8 | 4.1 | 5.2 | 4.9 | 6.1 | 7.5 |
| PEFT | CODAPrompt (2023) | _3.2_ | 4.5 | 5.8 | 2.5 | 3.8 | 4.9 | 4.5 | 5.8 | 7.1 |
| PEFT | RAPF (2024) | 3.4 | _4.2_ | _5.2_ | _2.1_ | _3.2_ | _4.4_ | – | – | – |
| PEFT | CLG-CBM (2025) | 3.9 | 4.8 | 6.2 | 2.6 | 3.9 | 5.1 | _3.8_ | _5.2_ | _6.8_ |
| Model Merging | Model Stock (2024) | 6.5 | 8.7 | 10.4 | 4.6 | 6.8 | 8.5 | 7.2 | 9.5 | 11.2 |
| Model Merging | TIES (2023) | 5.8 | 7.5 | 9.2 | 3.9 | 5.4 | 7.1 | 6.5 | 8.1 | 9.8 |
| Model Merging | MagMax (2024) | 5.2 | 7.1 | 8.8 | 3.4 | 4.9 | 6.5 | 6.1 | 7.8 | 9.2 |
| Model Merging | PM (2025) | – | – | – | 3.6 | 5.0 | 6.8 | – | – | – |
| Model Merging | BECAME (2025) | 4.8 | 6.9 | 8.5 | 3.1 | 4.6 | 6.2 | – | – | – |
| | **TRM (Ours)** | **2.5** | **3.6** | **4.2** | **1.8** | **2.6** | **3.5** | **2.9** | **4.6** | **6.0** |

**Merging under storage constraints** (Table 8, p. 11), last accuracy on ImageNet-R. A: all past models stored; B: only feature vectors or distribution statistics stored; C: strictly constrained storage (p. 11).

| Implementation | 10 tasks: TIES | Model Stock | MagMax | BECAME | 20 tasks: TIES | Model Stock | MagMax | BECAME |
|---|---|---|---|---|---|---|---|---|
| A | 82.9 | 83.3 | 83.3 | - | 82.2 | 82.1 | 82.2 | - |
| B | 80.6 | 81.8 | 83.3 | 79.8 | 81.3 | 80.7 | 82.2 | 78.7 |
| C | 79.5 | 77.1 | 80.1 | - | 78.4 | 76.5 | 79.3 | - |

The authors conclude that performance "is strongly correlated with the amount of accessible task-specific information" (p. 11). They note that MagMax's per-position maximum "should yield consistent results regardless of whether merging is performed in a single step using all previous task vectors or incrementally at each stage" (p. 11); yet Table 8 shows MagMax at 83.3 with all models stored (row A) and 80.1 under the strict constraint (row C) at 10 tasks (p. 11).

**Our reading:** Table 8 row C matches the ImageNet-R 10- and 20-task values of Table 1 for all three methods (TIES 79.5/78.4, Model Stock 77.1/76.5, MagMax 80.1/79.3). The 6% degradation in the introduction (p. 1) corresponds to Model Stock at 10 tasks (83.3 → 77.1 = 6.2) or 20 tasks (82.1 → 76.5 = 5.6), by our arithmetic. TRM under constraint C (83.2, 82.7; Table 1) is close to the unconstrained merging methods of row A (82.1–83.3).

**Ablation of the objectives** (Table 2, p. 6), ImageNet-R, 10 tasks. Baseline (a): stochastic parameter crossover only (random replacement of $\theta_{\text{init}}$ entries, p. 7). The table labels task alignment $\mathcal{L}_{task}$ (Eq. 7 calls it $\mathcal{L}_{align}$).

| Variant | $\mathcal{L}_{task}$ | $\mathcal{L}_{pre}$ | $\mathcal{L}_{res}$ | Acc (%) |
|---|---|---|---|---|
| (a) Baseline | – | – | – | 79.3 |
| (b) | ✓ | | | 71.8 |
| (c) | | ✓ | | 72.4 |
| (d) | | | ✓ | 76.5 |
| (e) | ✓ | ✓ | | 70.7 |
| (f) | ✓ | | ✓ | 81.9 |
| (g) | | ✓ | ✓ | 80.6 |
| (h) TRM | ✓ | ✓ | ✓ | 83.2 |

Each constraint alone *lowers* accuracy below the baseline; the two stability terms together lower it by 8.6%; adding $\mathcal{L}_{res}$ to either stability term improves on the baseline by 2.6% and 1.3% (p. 7).

**Search-space dimensionality** (Table 4, p. 8), ImageNet-R, 10 tasks; extra directions made mutually orthogonal with Gram–Schmidt, $P_i \perp span(\tau_t, \tau_{t-1})$ and $P_i \perp P_j$ for $j < i$ (p. 8):

| Subspace components | Acc (%) | Time (min) |
|---|---|---|
| $\tau_{t-1}, \tau_t$ | 79.8 | 25 |
| $\tau_{t-1}, \tau_t, P$ (Ours) | 83.2 | 33 |
| $\tau_{t-1}, \tau_t, P, P_1$ | 83.4 | 42 |
| $\tau_{t-1}, \tau_t, P, P_1, P_2$ | 83.5 | 58 |

**Optimization stability** (Table 3, p. 7), Hessian spectral norm $\lambda_{\max}$ on ImageNet-R, 10 tasks; "Finetune" is $\tilde{\theta}_t$ without merging (p. 7):

| Configuration | $\lambda_{\max}$ |
|---|---|
| Finetune | 8.60 |
| $\lambda_2 = 0$ | 1.15 |
| $\lambda_2 = 0.01$ (Ours) | 5.85 |
| $\lambda_2 = 1.0$ | 45.20 |
| $\lambda_2 = 10.0$ | 96.50 |

The authors read this as TRM restoring gradient impetus while keeping $\lambda_{\max}$ "within a moderate and stable range" (pp. 7–8).

**Other backbones** (Tables 5–6, p. 8), last accuracy on ImageNet-R:

| Method | ViT-B/16 LAION-400M: 5 tasks | 10 tasks | 20 tasks | ViT-L/14 WebImageText: 5 tasks | 10 tasks | 20 tasks |
|---|---|---|---|---|---|---|
| Model Stock | 79.6 | 77.0 | 76.4 | 87.2 | 86.8 | 86.7 |
| TIES | 81.7 | 79.3 | 78.4 | 87.8 | 87.4 | 86.9 |
| MagMax | 82.2 | 80.4 | 79.2 | 89.7 | 89.4 | 89.1 |
| BECAME | 81.2 | 80.0 | 76.1 | 87.9 | 87.8 | 87.1 |
| TRM (Ours) | 83.4 | 83.1 | 82.5 | 90.8 | 90.5 | 89.9 |

**Large scale, ImageNet1K with 100 tasks** (Figure 4, p. 7), accuracy (%) as printed on the bars: Zero-Shot 60.7, CODAPrompt 65.2, RAPF 71.2, CLG-CBM 70.3, Model Stock 72.9, TIES 73.3, MagMax 73.0, BECAME 72.4, Ours 74.6.

**Domain-incremental vs class-incremental** (Table 10, p. 12), complete test set only:

| Method | DomainNet CIL | DomainNet DIL | ImageNet-R CIL | ImageNet-R DIL |
|---|---|---|---|---|
| LwF | 57.3 | 59.5 | 58.2 | 61.7 |
| EWC | 57.9 | 59.2 | 63.5 | 65.1 |
| Model Stock | 63.9 | 70.2 | 77.0 | 82.6 |
| TIES | 66.6 | 66.2 | 78.8 | 83.5 |
| MagMax | 68.4 | 68.7 | 80.0 | 83.9 |
| Ours | 69.5 | 70.3 | 83.1 | 84.9 |

**Time** (Table 7, p. 8), minutes, 10 tasks:

| Dataset | Model Stock | TIES | MagMax | BECAME | Ours |
|---|---|---|---|---|---|
| ImageNet-R | 30 | 30 | 29 | 87 | 33 |
| CIFAR100 | 42 | 42 | 42 | 92 | 44 |

**Sensitivity** (no values printed; trends are **our reading** of the plots):

- **Replacement ratio** (Figure 5, p. 7; 10 runs per ratio, ImageNet-R 10 tasks): the authors report that using the original parameters (ratio 0) gives slightly lower accuracy and a wider best-to-worst range, variance first decreases then increases with the ratio, and they choose 0.6 (p. 7). Ratio 0 means "the original parameters" and 1.0 a full replacement (p. 7). Our reading: average accuracy goes from about 82.3 at ratio 0 to a peak of about 83.1 at 0.6, and about 82.8 at 1.0.
- **$\lambda_1$, $\lambda_2$** (Figure 6, p. 13; ImageNet-R 10 tasks): the authors say the method "remains stable across different hyperparameters" (p. 12). Our reading: for $\lambda_2 \in \{0.003, 0.005, 0.01, 0.02\}$ accuracy stays around 81–83 across $\lambda_1 \in [0, 0.5]$, best near $\lambda_1 = 0.1$, $\lambda_2 = 0.01$; with $\lambda_2 = 0$ it drops to about 70–72. The x-axis is labeled "Epoch" although the caption says it is $\lambda_1$.
- **Merging epochs** (Figure 7, p. 13): performance "became stable after 5 epochs" because the range of $\alpha$ and $\beta$ is kept very small (p. 12). Our reading: about 79.3 at epoch 0, about 83.2 at epoch 5, about 83.4 at epoch 40.

## Assumptions and limitations

- **Class-incremental image classification only** in the main results, with CLIP backbones and a frozen text-encoder classifier (p. 6); DIL only in the appendix (pp. 11–12).
- **Storage constraint**: the method keeps the pre-trained model, the previous merged model and the current fine-tuned model ("pre-task and post-task models are accessible", p. 8; the pre-trained model through Eq. 6, $\theta_t = \theta_{\text{init}} + \tau^{\text{mrg}}$, p. 4), and uses the current task's data for the merging search (Eqs. 7, 8, 11, pp. 4–5): it isn't data-free.
- **The plasticity term relies on an assumption** stated by the authors: successive tasks overlap in low-level features, so current-task gradients proxy the next task (p. 5); the DIL experiments are meant to test its limits (p. 11).
- **The diagnosis is shown on one protocol** (three 20-class ImageNet-R tasks, p. 3), and the 7th-layer split of Eq. 9 is chosen from that figure (p. 5).
- **Baselines re-run by the authors** under the strict constraint, which lowers the numbers of methods designed to store more (Table 8, p. 11; p. 6).
- **Joint and Zero-shot rows** of Table 1 aren't described in the text (p. 6).
- **Presentation inconsistencies:** the "first-order Taylor expansion" whose Eq. 10 includes a second-order term (p. 5); TIES is cited as Ilharco et al., 2023 on p. 3 (TIES is Yadav et al., 2023, p. 10); "Model Soup" in Figure 2's legend vs Model Stock in the text (p. 3); $\mathcal{L}_{task}$ in Table 2 vs $\mathcal{L}_{align}$ in Eq. 7; "Epoch" as Figure 6's x-axis label vs $\lambda_1$ in its caption (p. 13).
- **TRM doesn't fully reach the lowest-loss region:** Appendix B concedes it "does not converge precisely to the lowest loss region" in Figure 1 (p. 11).
- **Our reading:** no variance or seeds are reported for the main tables (only Figure 5 uses 10 runs); the random direction $P$ and the random parameter replacement add stochasticity whose effect on Table 1 isn't quantified; the gradient-norm maximization has no explicit bound other than the small $\lambda_2$ (Table 3 shows $\lambda_{\max}$ growing to 96.50 at $\lambda_2 = 10$); and no time series, regression or anomaly detection is studied.

## Relevance to this thesis

**Our reading:**

- **The strict CL merging protocol is a candidate setting for our sequential merging experiments:** keep only $\theta_{\text{init}}$, the previous merged model and the current fine-tuned model, fine-tune each task from the previous merged model, merge, repeat. This is the realistic constraint for streaming time series, where old periods may not be stored.
- **Table 8 quantifies the cost of that constraint** for TIES, Model Stock and MagMax (up to about 6 points on ImageNet-R); we could measure the same A/B/C gap for forecasting and anomaly detection, comparing sequential merging with merging all stored task vectors.
- **Joint training is the upper bound in every setting** (Table 1): 86.5 vs 83.2 on ImageNet-R 10 tasks, 89.4 vs 83.5 on CIFAR100 5 tasks. The joint-vs-merging gap is the thesis's central question; this paper gives reference gaps for image CIL under strict storage.
- **The 1D merge of Eq. 3 is the simplest sequential task arithmetic baseline** ($\alpha \tau_t + (1-\alpha)\tau_{t-1}$); Table 4's first row (79.8) shows how much a single extra direction adds (83.2). Both are cheap to implement for our models.
- **Diagnostics worth reusing:** the per-layer representation drift of Eq. 1 and the gradient-angle measure of Eq. 2 can tell us whether merged time-series models lose plasticity at the start of the next period, independent of TRM itself.
- **What may not carry over:** the class-incremental setup (disjoint classes, CLIP text classifier) has no direct analogue in forecasting or reconstruction-based anomaly detection; the cross-entropy terms would become a forecasting or reconstruction loss. The low-level-feature overlap assumption behind $\mathcal{L}_{res}$ may hold better for successive periods of the same signal than for disjoint classes, which is worth testing.
- **Open questions it informs:** whether a merging search on current data only (no replay) closes the gap to joint training for our tasks, and whether the gradient-norm term helps under distribution shift (concept drift) as in the DIL results (Table 10).

## Quotes worth keeping

> "the most existing merging methods (Wortsman et al., 2022; Jang et al., 2024; Ilharco et al., 2023; Yadav et al., 2023) require access to all previous task vectors and the initial model during the merging phase. This operational requirement is functionally equivalent to storing the entire ensemble of prior experts" (p. 1)

> "Our experiments reveal that under a strictly CL constraint, where only the current expert and the immediately merged model are available, existing methods suffer from a catastrophic performance degradation of up to 6%." (p. 1)

> "current task-agnostic optimization objectives inadvertently sacrifice task-specific local optimality, leading to the progressive amplification of localized errors across sequential training stages." (p. 3)

> "We conclude that insufficient gradient sensitivity induces a state of kinetic dormancy, which severely erodes the model's plasticity and its capacity to rapidly adapt to similar, non-stationary data streams." (p. 4)

> "Under the strict constraints of CL, however, the admissible subspace undergoes a catastrophic dimensionality collapse, shrinking to a one-dimensional linear trajectory between $\tau_{t-1}$ and $\tau_t$." (p. 4)

> "the performance of existing merging methods in continuous data-stream scenarios is strongly correlated with the amount of accessible task-specific information. As available memory decreases, overall performance consistently deteriorates." (p. 11)
