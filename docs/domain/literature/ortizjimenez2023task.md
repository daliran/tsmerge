# ortizjimenez2023task — Task Arithmetic in the Tangent Space: Improved Editing of Pre-Trained Models

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 150 claims: 3 small errors and 3 omissions, all fixed)
- **Reference:** Ortiz-Jimenez, Favero, Frossard; NeurIPS 2023; arXiv 2305.12827 ([references.bib](../references.bib))
- **Version read:** arXiv v3, 28 pages: main text pp. 1–10 (conclusion on p. 10), references pp. 10–17, appendix pp. 18–28
- **Read:** main text in full (pp. 1–10); appendix in full: A (p. 18), B (pp. 18–20), C (p. 20), D–D.9 (pp. 21–28). References (pp. 10–17) only looked up where needed, not read
- **Code:** <https://github.com/gortizji/tangent_task_arithmetic> (p. 3, footnote 2)

## In one paragraph

The paper asks why task arithmetic works, and how to make it work better (p. 2). It shows that CLIP models do **not** fine-tune in the linear (NTK) regime, so linearity can't explain task arithmetic (Section 3, pp. 3–5). It proposes instead that the necessary condition is **weight disentanglement**: distinct directions in weight space change the network's output only on separate, localized regions of the input space, one per task (Section 4, p. 5). It then proposes **linearized fine-tuning**: fine-tuning the first-order Taylor expansion of the model around its pre-trained weights, i.e. fine-tuning in the tangent space (Section 5, pp. 6–7). Linearized models are more weight-disentangled, and on the paper's vision-language benchmark (8 CLIP tasks in Tables 1–2) they reach up to 5.8 points more accuracy in task addition and 13.1 points less in task negation than standard (non-linear) fine-tuning (p. 2, p. 7). Weight disentanglement is linked to NTK eigenfunctions localized on each task's domain (Section 6.1), and is shown to be an emergent property of pre-training: task arithmetic fails from random initialization (Section 6.2, Table 3, pp. 8–9).

## Problem

Task arithmetic (adding or subtracting fine-tuned weight differences to a pre-trained model) is cheap and scalable, but its "underlying principles" and "general effectiveness" are not understood; this limits its reliability, and understanding it could improve it (p. 2).

**Specific questions** (pp. 2–3):

- Is task arithmetic explained by models fine-tuning in a linear regime, governed by the finite-width NTK (a hypothesis attributed to Wortsman et al.)? (p. 2, p. 3)
- If not, what is the necessary condition? (p. 5)
- Can the method be improved by acting on that condition? (p. 6)

**Setting:**

- $T$ tasks, each a triplet $(\mathcal{D}_t, \mu_t, f_t^\star)$: a data support $\mathcal{D}_t \subseteq \mathcal{X}$, an input distribution $\mu_t$ with $\operatorname{supp}(\mu_t) = \mathcal{D}_t$, and a target function $f_t^\star : \mathcal{D}_t \to \mathcal{Y}$ (p. 3).
- Network $f : \mathcal{X} \times \Theta \to \mathcal{Y}$, with $\mathcal{X} \subseteq \mathbb{R}^d$, $\Theta \subseteq \mathbb{R}^m$, $\mathcal{Y} \subseteq \mathbb{R}^c$ (p. 3).
- All tasks are fine-tuned from the **same pre-trained weights** $\theta_0$, giving $\theta_t^\star$ (p. 3).
- The formal property assumes **non-intersecting** task supports: $\mathcal{D}_t \cap \mathcal{D}_{t'} = \varnothing$ for $t \neq t'$ (p. 3).

## Method

**Task vector** (p. 3):

$$\tau_t = \theta_t^\star - \theta_0$$

**Property 1, task arithmetic** (p. 3). Given task vectors $\mathcal{T} = \{\tau_t\}_{t \in [T]}$ with non-intersecting supports $\mathcal{D} = \{\mathcal{D}_t \subset \mathcal{X}\}_{t \in [T]}$, $f$ satisfies the task arithmetic property around $\theta_0$ if

$$f\left(x; \theta_0 + \sum_{t=1}^{T} \alpha_t \tau_t\right) = \begin{cases} f(x; \theta_0 + \alpha_t \tau_t) & x \in \mathcal{D}_t \\ f(x; \theta_0) & x \notin \bigcup_{t=1}^{T} \mathcal{D}_t \end{cases} \tag{1}$$

with $(\alpha_1, \dots, \alpha_T) \in \mathcal{A} \subseteq \mathbb{R}^T$. In words: adding $\tau_t$ does not modify the model's output outside $\mathcal{D}_t$ (p. 3).

**Linearization and the NTK** (p. 3). First-order Taylor expansion around $\theta_0$:

$$f(x; \theta) \approx f(x; \theta_0) + (\theta - \theta_0)^\top \nabla_\theta f(x; \theta_0) \tag{2}$$

- This is a kernel predictor with the neural tangent kernel $k_{\text{NTK}}(x, x') = \nabla_\theta f(x; \theta_0)^\top \nabla_\theta f(x'; \theta_0)$ (p. 3).
- Training is in the **linear regime** when Eq. (2) closely approximates the network during fine-tuning, and in the **non-linear regime** otherwise (p. 3).

**Property 2, post-hoc linearization** (p. 3): the model is in the linear regime if

$$f(x; \theta^\star) - f(x; \theta_0) \approx (\theta^\star - \theta_0)^\top \nabla_\theta f(x; \theta_0)$$

**Post-hoc linearized model** (p. 3): the task vector of the normally (non-linearly) fine-tuned model, $\tau = \theta^\star - \theta_0$, applied to the linear approximation of $f$ at $\theta_0$:

$$f_{\text{lin}}(x; \theta_0 + \tau) = f(x; \theta_0) + \tau^\top \nabla_\theta f(x; \theta_0) \tag{3}$$

**Property 3, weight disentanglement** (p. 5). $f$ is weight disentangled with respect to $\mathcal{T}$ and $\mathcal{D}$ if

$$f\left(x; \theta_0 + \sum_{t=1}^{T} \alpha_t \tau_t\right) = \sum_{t=1}^{T} g_t(x; \alpha_t \tau_t) + g_0(x) \tag{4}$$

where $g_t(x; \alpha_t \tau_t) = 0$ for $x \notin \mathcal{D}_t$ and $t = 1, \dots, T$, and $g_0(x) = 0$ for $x \in \bigcup_{t \in [T]} \mathcal{D}_t$.

- Weight disentanglement is **equivalent** to Property 1, since Eq. (1) can always be written as (p. 5):

  $$f\left(x; \theta_0 + \sum_{t=1}^{T} \alpha_t \tau_t\right) = \sum_{t=1}^{T} f(x; \theta_0 + \alpha_t \tau_t)\, \mathbb{1}(x \in \mathcal{D}_t) + f(x; \theta_0)\, \mathbb{1}\left(x \notin \bigcup_{t \in [T]} \mathcal{D}_t\right) \tag{5}$$

  with $g_t(x; \alpha_t \tau_t) = f(x; \theta_0 + \alpha_t \tau_t)\mathbb{1}(x \in \mathcal{D}_t)$ and $g_0(x) = f(x; \theta_0)\mathbb{1}(x \notin \mathcal{D}_t)$ (p. 5, as printed).
- The decomposition **does not imply linearity**: the $g_t$ need not be linear in the parameters (p. 5).
- It is a property of the predictor, **not of task performance**: a model can be weight disentangled and still perform poorly on a task (p. 5).

**Disentanglement error** (p. 5), for two tasks:

$$\xi(\alpha_1, \alpha_2) = \sum_{t=1}^{2} \mathbb{E}_{x \sim \mu_t}\left[\operatorname{dist}\left(f(x; \theta_0 + \alpha_t \tau_t),\ f(x; \theta_0 + \alpha_1 \tau_1 + \alpha_2 \tau_2)\right)\right] \tag{6}$$

- For classification, $\operatorname{dist}(y_1, y_2) = \mathbb{1}(y_1 \neq y_2)$, the prediction error (p. 5).
- Smaller $\xi(\alpha_1, \alpha_2)$ means more weight disentangled at $(\alpha_1, \alpha_2)$ (p. 5).

**Linearized fine-tuning** (the proposed method, Section 5, pp. 6–7):

- Instead of fine-tuning $f$ and applying its task vector to $f_{\text{lin}}$, fine-tune $f_{\text{lin}}$ around $\theta_0$ directly, with the same protocols, using the parameterization of Eq. (3) (p. 6).
- This is "essentially the same as training a kernel predictor with kernel $k_{\text{NTK}}$" (p. 7).
- Result: fine-tuned weights $\theta_{\text{lin}}^\star$ and task vector (p. 7):

  $$\tau_{\text{lin}} = \theta_{\text{lin}}^\star - \theta_0$$

- Since CLIP models don't fine-tune linearly, this differs from post-hoc linearization: $f_{\text{lin}}(x; \theta_0 + \tau_{\text{lin}}) \neq f_{\text{lin}}(x; \theta_0 + \tau)$ (p. 7).
- Both share the same kernel $k_{\text{NTK}}$, but $\tau_{\text{lin}}$ is explicitly optimized for the linearized model, so linearized fine-tuning outperforms post-hoc linearization "by construction" (p. 7).
- Task arithmetic is then applied to $f_{\text{lin}}$ with the $\tau_{\text{lin}}$ vectors: addition $f_{\text{lin}}(\cdot; \theta_0 + \tau_{\text{lin}})$, negation $f_{\text{lin}}(\cdot; \theta_0 - \tau_{\text{lin}})$ (Tables 1–2, p. 4).

**Implementation** (B, pp. 18–19, Listing 1):

- A `LinearizedModel` wrapper around any `nn.Module`, using `functorch`'s `make_functional_with_buffers` and `jvp` (Jacobian-vector product). It stores frozen initial parameters `params0` and trainable copies `params`, and returns `out + dp`, where `out, dp = jvp(func0, (params0,), (params - params0,))` (p. 19, Listing 1).
- Only the CLIP **image encoder** (ViT) is linearized; the text encoder is frozen (p. 19).
- The image encoder's output is normalized before the inner product with the text embeddings; this doesn't change the classification decision at inference, but rescales the loss; the authors found it has "a clearly positive effect in single-task accuracy" for both non-linear and linearized models (p. 19).

**Computational cost** (pp. 19–20):

- Main text: training and inference in linearized networks need only an $\mathcal{O}(1)$ increase in cost (p. 7).
- Inference: "around two or three times more" than the non-linear model, since every forward operation also computes its derivative (p. 19).
- Training: the gradient of $f_{\text{lin}}$ costs "roughly twice" that of $f$ (p. 19); the memory footprint of training is "also double" (p. 20).

**Normalized accuracy** for task addition (A, p. 18), relative to each task's own fine-tuned model:

$$\text{Normalized accuracy} = \frac{1}{T} \sum_{t=1}^{T} \frac{\operatorname{acc}_{x \sim \mu_t}\left[f(x; \theta_0 + \sum_{t'} \tau_{t'})\right]}{\operatorname{acc}_{x \sim \mu_t}\left[f(x; \theta_0 + \tau_t)\right]} \tag{7}$$

Normalization is with respect to the single-task accuracy "achieved by the model fine-tuned on each task" (p. 18); the Table 1 caption says each method is normalized "by their single-task accuracies" (p. 4). Eq. 7 itself is written only with the non-linear model $f$ (p. 18). **Our reading:** each method's normalized accuracy uses that method's own single-task accuracies (linearized fine-tuned model for linearized FT, post-hoc model for post-hoc linearization); this is consistent with Table 1's absolute and normalized columns against Figure 7's bars (p. 21), e.g. ViT-B/32 non-linear 71.4 / 0.765 ≈ 93.3.

**Eigenfunction localization** (Section 6.1, pp. 7–8; C, p. 20):

- A kernel $k$ decomposes into eigenfunction-eigenvalue pairs $\{(\phi_\rho, \lambda_\rho)\}_{\rho \in \mathbb{N}}$; it can only represent $f^\star(x) = \sum_{\rho=1}^{\infty} c_\rho \phi_\rho(x)$ with finite kernel norm $\|f^\star\|_{\mathcal{H}}^2 = \sum_{\rho=1}^{\infty} c_\rho^2 / \lambda_\rho < +\infty$ (p. 7).
- **Proposition 1 (simplified)** (p. 8): $k$ can perform task arithmetic with respect to $\{f_t^\star\}$ and $\{\mathcal{D}_t\}$ if, for each task $t$, there is a subset of localized eigenfunctions with $\operatorname{supp}(\phi) \subseteq \mathcal{D}_t$, and $f_t^\star$ is represented only with these.
- **Proposition 2** (formal version, p. 20): if for all $t, \rho$ either $c_{t,\rho}^\star = 0$ or $\operatorname{supp}(\phi_\rho) \subseteq \mathcal{D}_t$, then $k$ has the task arithmetic property. The proof writes the requirement as Eq. (8) and rewrites it as (p. 20):

  $$\int_{\mathcal{D}_{t'}} \left(\sum_{t \in [T],\, t \neq t'} \sum_{\rho \in \mathbb{N}} c_{t,\rho}^\star \phi_\rho(x)\right)^2 dx = 0 \tag{9}$$

- **Localization is not always necessary** (Remark, p. 8): eigenfunctions can cancel out on a single domain. But if eigenfunctions are **locally linearly independent** on each domain, localization becomes necessary: **Proposition 3** (p. 20) gives "if and only if" under that assumption.
- Fully-connected and convolutional networks at initialization, with data uniform on a ring or torus, have NTKs diagonalized by Fourier series, whose atoms are linearly independent and not localized; by Proposition 3 they "cannot perform task arithmetic" in those settings (p. 20).
- **Local energy** (p. 8): $\mathcal{E}_{\text{loc}}(x) = \sum_\rho \phi_\rho^2(x)$, the summed power of all eigenfunctions at $x$; computed by diagonalizing $(K_{\text{NTK}})_{ij} = k_{\text{NTK}}(x_i, x_j)$ with $x_i \in \mathcal{D}_t$ and $x_j \in \mathcal{D}_t \cup \mathcal{D}_{t'}$, i.e. the training task's points against the union with a control task's points (p. 8).

## Experimental setup

**Models and tasks:**

- CLIP ViT-B/32, ViT-B/16, ViT-L/14 (Tables 1–3, pp. 4, 9), from the same `open_clip` pre-trained checkpoint (p. 18).
- 8 tasks, as in the task-arithmetic benchmark of Ilharco et al.: Cars, DTD, SUN397, EuroSAT, GTSRB, MNIST, SVHN, RESISC45 (p. 4).
- **Task addition:** $\tau = \sum_t \tau_t$ added to the pre-trained checkpoint; success is the maximum average accuracy over the tasks (p. 4).
- **Task negation:** a task vector subtracted to forget a task while retaining performance on a control task (ImageNet); success is the maximum accuracy drop on the target that retains the control performance; averaged over tasks (p. 4).
- Extra architectures (D.5–D.7, p. 25): CLIP ConvNeXt pre-trained on LAION-400M; a ViT-B/16 pre-trained on ImageNet-1k with standard supervised learning (closed vocabulary); T5-Base fine-tuned on IMDB (sentiment) and QASC (question answering), for disentanglement only.

**Fine-tuning** (A, p. 18):

- Same protocol as Ilharco et al., with minor changes to use linearized models (p. 18).
- 2,000 iterations, batch size 128, learning rate $10^{-5}$, cosine annealing schedule with 200 warm-up steps, AdamW (p. 18).
- Classification layer, built by encoding a standard set of zero-shot template prompts per dataset, is **frozen**: no extra learnable parameters (p. 18).
- Same protocol for non-linear and linearized models; **no hyperparameter search** of any kind (p. 18).
- **Closed-vocabulary model** (D.6, p. 25): a randomly initialized head must also be fine-tuned per task; when interpolating task vectors, the resulting heads are frozen to build the final models.

**Choosing the scaling coefficient $\alpha$** (A, p. 18; p. 5):

- One single coefficient, $\alpha = \alpha_1 = \dots = \alpha_T$ in Eq. (1), as in Ilharco et al. (p. 18).
- Searched in $\alpha \in \{0.0, 0.05, 0.1, \dots, 1.0\}$, on "a small held-out proportion of the training set" (p. 18).
- Criterion: addition, maximum normalized average accuracy; negation, minimum target accuracy on each dataset that still retains at least 95% of the pre-trained model's control accuracy (p. 18).
- Tuned independently for non-linear FT, linearized FT and post-hoc linearization (p. 18 for all three; p. 5 states it for the non-linear and post-hoc models, "to ensure a fair comparison").

**Disentanglement error** (A, p. 18): $\xi(\alpha_1, \alpha_2)$ on a $20 \times 20$ grid of equispaced values in $[-3, 3] \times [-3, 3]$, using a random subset of 2,048 test points per dataset.

**NTK eigenfunctions** (A, p. 18): finite-width NTK from PyTorch's `functorch`; a random subset of 200 training points per dataset; SVD of $K_{\text{NTK}}$ to estimate $\phi_\rho$; one set of singular vectors per output class (one kernel matrix per output logit), with little variability across classes.

**Hardware** (A, p. 18): four NVIDIA V100 GPUs with 32 GB each; everything reproducible in less than 350 GPU hours.

## Results

**Task addition, 8 tasks** (Table 1, p. 4). Average absolute and normalized accuracy (%), higher is better:

| Method | ViT-B/32 Abs. | ViT-B/32 Norm. | ViT-B/16 Abs. | ViT-B/16 Norm. | ViT-L/14 Abs. | ViT-L/14 Norm. |
|---|---|---|---|---|---|---|
| Pre-trained $f(\cdot; \theta_0)$ | 48.4 | – | 55.2 | – | 64.4 | – |
| Non-lin. FT $f(\cdot; \theta_0 + \tau)$ | 71.4 | 76.5 | 75.5 | 80.0 | 85.1 | 88.8 |
| Post-hoc lin. $f_{\text{lin}}(\cdot; \theta_0 + \tau)$ | 57.1 | 81.9 | 65.0 | 85.2 | 75.2 | 90.0 |
| Linear. FT $f_{\text{lin}}(\cdot; \theta_0 + \tau_{\text{lin}})$ | **76.5** | **85.4** | **81.3** | **86.0** | **88.5** | **93.5** |

**Task negation, 8 tasks** (Table 2, p. 4). Minimum target accuracy (%, lower is better) while retaining 95% of the control (ImageNet) performance, and control accuracy (%, higher is better); bold as printed:

| Method | ViT-B/32 Targ. | ViT-B/32 Cont. | ViT-B/16 Targ. | ViT-B/16 Cont. | ViT-L/14 Targ. | ViT-L/14 Cont. |
|---|---|---|---|---|---|---|
| Pre-trained $f(\cdot; \theta_0)$ | 48.4 | 63.4 | 55.2 | 68.3 | 64.4 | 75.5 |
| Non-lin. FT $f(\cdot; \theta_0 - \tau)$ | 24.0 | 60.7 | 19.2 | 64.6 | 18.0 | **72.5** |
| Post-hoc lin. $f_{\text{lin}}(\cdot; \theta_0 - \tau)$ | 14.8 | 60.3 | **10.8** | **64.8** | 12.1 | 71.8 |
| Linear. FT $f_{\text{lin}}(\cdot; \theta_0 - \tau_{\text{lin}})$ | **10.9** | **60.8** | 11.3 | **64.8** | **7.9** | **72.5** |

**Headline gains** (p. 2, p. 7): linearized fine-tuning gives "up to 5.8 points more" in task addition and "up to 13.1 points more" forgetting in task negation, at a similar control accuracy (p. 7). **Our reading** of Tables 1–2: 5.8 matches ViT-B/16 absolute addition accuracy (81.3 − 75.5), and 13.1 matches ViT-B/32 negation target accuracy (24.0 − 10.9).

**Model size** (p. 7): the advantage of linearized over non-linear models is higher for ViT-B/32 and diminishes as model size grows up to ViT-L/14. **Our reading:** in normalized addition accuracy the gain is 8.9, 6.0 and 4.7 points (B/32, B/16, L/14); in absolute accuracy it is 5.1, 5.8 and 3.4, so the trend is not monotonic in absolute terms.

**Linear regime test** (Section 3, pp. 4–5; Figure 2, p. 4):

- Post-hoc linearized single-task accuracy is "significantly lower" than non-linear fine-tuning, for ViTs of all sizes: the **non-linear advantage** (p. 4).
- Task addition with post-hoc linearization drops in absolute accuracy (Table 1), consistently across tasks (D.2), so task arithmetic in non-linear models "leverages the non-linear components of $f$, as well" (p. 5).
- Yet post-hoc linearized models do better at negation, and reach higher **normalized** addition accuracy (p. 5).

**Disentanglement** (Figure 3, pp. 5–6):

- ViT-B/32, pairs EuroSAT–SVHN, DTD–SUN397, Cars–RESISC45: minimal disentanglement error in a small region around $\theta_0$, increasing for $\alpha_1, \alpha_2 > 1$ (p. 5).
- Post-hoc linearized models show larger low-error regions than non-linear ones (p. 6); linearly fine-tuned models too, "similar to the findings obtained for post-hoc linearization" (D.4, p. 24, Figure 10).
- Linearized fine-tuning raises single-task performance without compromising weight disentanglement (p. 7, D.4).
- Low-error regions grow with model scale (D.3, p. 23, Figure 9; footnote 3, p. 7). Figure 9's caption calls its bottom row "their post-hoc linearizations", while the panels are labeled "Linearized FT" (p. 23). The authors' "plausible explanation": larger models stay closer to the NTK approximation during fine-tuning (p. 23).

**Single-task accuracies** (D.1, pp. 21–22, Figure 7): non-linear FT is consistently the most accurate; the gap between non-linear, linear and post-hoc linearized models shrinks as the model grows (p. 22). Values are only plotted, not printed. **Our reading** of Figure 7 (p. 21): linearized FT is close to non-linear FT on most tasks, with the largest gap on SVHN for ViT-B/32 and ViT-B/16.

**Per-task addition** (D.2, p. 22, Figure 8): linearized task arithmetic gives the highest accuracy on all datasets for all models except SUN397; the gap between linear and non-linear task vectors decreases with model size (p. 22). Values plotted only.

**Task addition from random initialization** (Table 3, p. 9). Average single-task accuracy after fine-tuning ("Sing.") and multi-task accuracy via task addition ("Multi"), %:

| Method | ViT-B/32 Sing. | ViT-B/32 Multi | ViT-B/16 Sing. | ViT-B/16 Multi | ViT-L/14 Sing. | ViT-L/14 Multi |
|---|---|---|---|---|---|---|
| Random init $f(\cdot; \theta_0^{\text{rd}})$ | 5.3 | – | 4.8 | – | 5.2 | – |
| Non-lin. FT $f(\cdot; \theta_0^{\text{rd}} + \tau^{\text{rd}})$ | 48.5 | 5.5 | 40.6 | 4.5 | 18.0 | 4.8 |
| Linear. FT $f_{\text{lin}}(\cdot; \theta_0^{\text{rd}} + \tau_{\text{lin}}^{\text{rd}})$ | 27.8 | 3.8 | 24.7 | 4.0 | 24.8 | 6.1 |

- Task addition doesn't significantly improve over random chance from random initialization, with either kind of task vector (pp. 8–9).
- Randomly initialized models can still learn the single tasks (non-trivial or moderate accuracy for the base models), so the failure is a lack of weight disentanglement, not of learning (D.9, p. 27, Figure 16 p. 28); the disentanglement error is high everywhere (D.4, p. 24, Figure 11) and eigenfunction localization is poor (D.8, p. 26, Figure 15 p. 27).
- The randomly initialized large model does worse than the base ones, attributed to overfitting (p. 27).

**Other architectures** (D.5–D.7, p. 25):

| Model (Table) | Method | Abs. (%) | Norm. (%) |
|---|---|---|---|
| CLIP ConvNeXt (Table 4) | Pre-trained | 57.5 | – |
| CLIP ConvNeXt (Table 4) | Non-lin. FT | 79.1 | 83.6 |
| CLIP ConvNeXt (Table 4) | Linear. FT | **81.1** | **85.7** |
| ViT-B/16, supervised ImageNet-1k (Table 5) | Pre-trained | 2.3 | – |
| ViT-B/16, supervised ImageNet-1k (Table 5) | Non-lin. FT | **54.9** | 52.2 |
| ViT-B/16, supervised ImageNet-1k (Table 5) | Linear. FT | 41.8 | **66.1** |

- In Tables 4–5 the rows are labeled with $\theta_0^{\text{rd}}$ and $\tau^{\text{rd}}$, as printed, although the models are pre-trained (p. 25).
- The closed-vocabulary model does task arithmetic at lower absolute and normalized accuracy than the open-vocabulary ones; linearized FT gives higher normalized accuracy but not higher absolute accuracy, "due to its lower single-task performance" (p. 25).
- T5-Base (IMDB–QASC) shows a notable low-error region around the pre-trained checkpoint; the tangent space of CLIP ConvNeXt is more disentangled than its non-linear function space; the same holds for the closed-vocabulary model (p. 25; Figures 12–13, p. 26).

**Eigenfunction localization** (Figure 6, p. 8; D.8, pp. 26–27): for a ViT-B/32 trained on RESISC45 with Cars as control, the local energy is "significantly higher" on training-set points; the same holds for DTD–SUN397 and MNIST–EuroSAT (Figure 14, p. 27).

## Assumptions and limitations

- **Same pre-trained initialization** for all task vectors, and element-wise operations on weights (p. 3).
- **Non-intersecting task supports** in the formal definitions (Property 1, p. 3; Proposition 2, p. 20). **Our reading:** real tasks may share inputs, and the paper's datasets are only treated as disjoint by assumption.
- **One single $\alpha$** for all task vectors, chosen on held-out training data (p. 18), within a search box around $\theta_0$: "The red box delimits the search space used to compute the best α" (Figure 3, p. 6; also Figures 9–11 and 13, pp. 23–24, 26).
- **No explicit limitations section.** The authors list as open: how weight disentanglement arises during pre-training and algorithms that enhance it; tangent spaces for other pre-trained models; more efficient linearized models (p. 10); and the trade-off between computational cost and performance (p. 7).
- **Cost:** linearized models cost about 2–3 times more at inference, and about twice in gradient computation and memory at training time (pp. 19–20).
- **Linearized FT lowers single-task accuracy** (the non-linear advantage, Figure 7, p. 21); with the closed-vocabulary model this makes linearized task addition worse in absolute terms (Table 5, p. 25).
- **Disentanglement error is measured on pairs of tasks** only (Eq. 6, p. 5).
- **Our reading:**
  - No joint multi-task training baseline is reported: comparisons are only among task-arithmetic variants (non-linear, post-hoc, linearized) and the pre-trained model.
  - Classification only for the task-arithmetic numbers (images; T5 only for disentanglement heatmaps); nothing on regression, forecasting, time series or anomaly detection. The disentanglement metric uses the 0–1 prediction error, which has no direct counterpart in regression.
  - Results are single-run as reported (no seeds or error bars in Tables 1–5).
  - The fine-tuning protocol is fixed, with no hyperparameter search (p. 18), so linearized FT may be disadvantaged or advantaged by a schedule tuned for the non-linear model.

## Relevance to this thesis

**Our reading:**

- **A second task-arithmetic variant to test:** besides standard task vectors, linearized fine-tuning ($\tau_{\text{lin}}$, evaluated with $f_{\text{lin}}$) is a direct, cheap-to-implement alternative (Listing 1, p. 19, is a few lines with `jvp`). It should be compared against joint training on the same tasks, which this paper does not do.
- **Weight disentanglement as a diagnostic:** $\xi(\alpha_1, \alpha_2)$ (Eq. 6) can be computed for our task pairs. For forecasting and anomaly scores, $\operatorname{dist}$ would need a regression distance (e.g. MSE between outputs) or a distance on anomaly decisions; this is a choice we'd have to make and justify.
- **The disjoint-support assumption is a key question for time series:** if our tasks are different machines or datasets, supports may be nearly disjoint; if they are successive periods of the same signal, supports overlap heavily, and Property 1 may not even be well-posed. This could explain where task arithmetic falls behind joint training.
- **Pre-training matters:** task arithmetic fails from random initialization (Table 3). If our time-series backbones are small or trained from scratch, task arithmetic may fail for the same reason; a pre-trained (or jointly pre-trained) $\theta_0$ is probably required, and worth testing explicitly.
- **Heads:** the closed-vocabulary setup (D.6, p. 25), with per-task heads fine-tuned and then frozen while merging the backbone, is the closest to forecasting or anomaly heads that can't be built from text prompts; it shows lower task-arithmetic performance.
- **Protocol details to reuse:** one $\alpha$ searched in $\{0.0, 0.05, \dots, 1.0\}$ on held-out training data, tuned separately per method; normalized accuracy (Eq. 7), normalized, on our reading, by each method's own single-task accuracies (see Method).
- **Cost:** linearized training is about 2× in compute and memory (pp. 19–20), relevant for the cluster budget.

## Quotes worth keeping

> "We present a comprehensive study of task arithmetic in vision-language models and show that weight disentanglement is the crucial factor that makes it effective." (p. 1)

> "In short, a model satisfies Property 1 if adding τ_t does not modify the output of the model outside D_t." (p. 3)

> "It is important to highlight, however, that this additive decomposition does not imply linearity, as the local functions {g_t}_{t∈[T]} are not required to be linear with respect to the parameters." (p. 5)

> "This explains why task arithmetic performs better in a small neighborhood of θ_0 – task arithmetic is more effective when fine-tuning with small learning rates and few training steps [39] – with the optimal value of α typically being less than 1." (p. 5)

> "This suggests that closing the single-task performance gap between linearized and non-linear models could be a way to enhance task arithmetic." (p. 6)

> "Therefore, we conclude that task arithmetic is a property acquired during pre-training." (p. 9)
