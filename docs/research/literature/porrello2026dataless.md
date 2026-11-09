# porrello2026dataless — Dataless Weight Disentanglement in Task Arithmetic via Kronecker-Factored Approximate Curvature

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 190 claims, every table cell correct: 2 misstatements, 1 unsupported detail and 4 omissions, all fixed)
- **Reference:** Porrello, Buzzega, Dangel, Sommariva, Salami, Bonicelli, Calderara; ICLR 2026; arXiv 2602.17385 ([references.bib](references.bib))
- **Version read:** arXiv v2 (23 Feb 2026, p. 1 margin), 25 pages: main text pp. 1–10, acknowledgments, reproducibility statement, LLM disclosure and references pp. 11–15, appendix pp. 16–25
- **Read:** main text in full (pp. 1–10); acknowledgments, reproducibility statement and LLM disclosure (p. 11); appendix A–G in full (pp. 16–25). Not read: the reference list (pp. 11–15, only skimmed on pp. 11, 12, 14, 15; p. 13 not opened)
- **Code:** integrated into the Mammoth framework, <https://github.com/aimagelab/mammoth>; the paper says it "will be made publicly available" (p. 11)

## In one paragraph

Adding task vectors suffers from cross-task interference: a new task vector changes the representations other tasks rely on (p. 1).

Regularizing against this **representation drift** usually needs the other tasks' data (p. 1).

The paper shows that, for a **linearized** model, the drift regularizer is a quadratic form in the network Jacobian's Gramian, which equals the **generalized Gauss-Newton (GGN)** matrix of a squared loss;
this matrix can be computed once per task and shared instead of the data (pp. 1–4).

The Gramian is approximated with **KFAC** (Kronecker-Factored Approximate Curvature),
and the per-task factors of all other tasks are merged into one Kronecker product, so cost is constant in the number of tasks (pp. 2, 5).

The method, **TAK** (Task Arithmetic with KFAC regularization, p. 2):

- reaches state-of-the-art task addition and negation among dataless methods on 8 vision tasks with CLIP (Tables 1–2, pp. 6–7),
- makes plain addition with $\alpha = 1$ nearly as good as tuned $\alpha$ (Table 1, p. 6; Fig. 4a, p. 8), and
- makes each task vector act mostly on its own input distribution (Fig. 5, p. 8).

## Problem

How to train task vectors that can be added (or subtracted) with little interference, **without access to the other tasks' training data** (p. 1).

> "Therefore, our goal is to design a computationally efficient regularizer for weight disentanglement that can be used without requiring access to the training data." (p. 1)

**Weight disentanglement** (p. 1, citing Ortiz-Jimenez et al., 2023): distinct directions in parameter space lead to changes confined to non-overlapping regions of the input space.

**Setting** (p. 2):

- A network $f : \mathbb{R}^D \times \mathbb{R}^P \to \mathbb{R}^C$,
- pre-trained weights $\theta_0$ from a source dataset $\mathcal{D}_0$,
- $T$ downstream tasks with data $\mathcal{D}_t$,
- fine-tuned weights $\theta_t^\star$,
- task vectors $\tau_t := \theta_t^\star - \theta_0$.

The composed model is $\theta_0 + \sum_{t=1}^T \alpha_t \tau_t$, with $\alpha_t \in \mathbb{R}$ ($\alpha_t = 1$ in the simplest case) (p. 2).

## Method

**Linearized fine-tuning** (Eq. 1, p. 2), following Ortiz-Jimenez et al. (2023):

$$f_{\text{lin}}(x, \theta) = f(x, \theta_0) + J_\theta f(x, \theta_0)(\theta - \theta_0)$$

with $J_\theta f(x, \theta_0) \in \mathbb{R}^{C \times P}$ the Jacobian at $\theta_0$ (p. 2).

**Representation drift, two tasks** (Eq. 2, p. 3).

Adding task vector $\tau_{t'}$ on top of $\tau_t$ changes task $t$'s last-layer activations from $z_t(x) = f_{\text{lin}}(x, \theta_0 + \alpha_t \tau_t)$
to $z_{t,t'}(x) = f_{\text{lin}}(x, \theta_0 + \alpha_t \tau_t + \alpha_{t'} \tau_{t'})$:

$$\Delta_{t \to t,t'}(x) := \| z_{t,t'}(x) - z_t(x) \|_2^2$$

If the drift vanishes for all $x \in \mathcal{D}_t$, $\tau_{t'}$ doesn't interfere with task $t$ (p. 3).

The data-dependent regularizer is $\mathcal{L}^{\text{drift}}_{t \to t,t'}(\tau_{t'}) := \frac{1}{|\mathcal{D}_t|} \sum_{x \in \mathcal{D}_t} \Delta_{t \to t,t'}(x)$ (p. 3).

**Dataless form** (Eq. 3, p. 3). Under linearization the drift reduces to $\alpha_{t'}^2 \| J_\theta f_{\text{lin}}(x, \theta_0) \tau_{t'} \|_2^2$, so:

$$\mathcal{L}^{\text{drift}}_{t \to t,t'}(\tau_{t'}) = \alpha_{t'}^2 \, \tau_{t'}^\top G_t(\theta_0) \, \tau_{t'} \quad \text{with} \quad G_t(\theta_0) = \frac{1}{|\mathcal{D}_t|} \sum_{x \in \mathcal{D}_t} J_\theta f(x, \theta_0)^\top J_\theta f(x, \theta_0)$$

$G_t(\theta_0) \in \mathbb{R}^{P \times P}$ (the Jacobian's Gramian) needs no further data access once pre-computed (p. 3); but at $P \times P$ it is infeasible even for small networks (p. 3).

**Link to the GGN** (Eqs. 4–5, p. 4).

For a loss $\ell_n = c_n \circ f_n$ and empirical risk $\mathcal{L}(\theta) = \frac{1}{|\mathcal{D}|} \sum_n (c_n \circ f_n)(\theta)$ (Eq. 4), the Hessian splits into the GGN plus a residual:

$$\nabla^2 \mathcal{L}(\theta) = G(\theta) + R(\theta) := \frac{1}{|\mathcal{D}|} \sum_n (J_\theta f_n)^\top \nabla^2 c_n (J_\theta f_n) + \frac{1}{|\mathcal{D}|} \sum_n \sum_{m=1}^{C} [\nabla c_n]_m \nabla^2 [f_n]_m$$

- $R(\theta)$ vanishes for models linear in the parameters, where the GGN equals the Hessian; for likelihood-based losses the GGN equals the Fisher information matrix (p. 4).
- With squared error $c_n(f) = \frac{1}{2}\|f - y_n\|_2^2$, $\nabla^2 c_n = I_C$, so the GGN **is exactly** the Jacobian Gram matrix of Eq. 3 (p. 4).

**KFAC** (Eq. 6, p. 4). The GGN is approximated as block-diagonal over the $L$ layers, each block as a Kronecker product $G(\theta^l) \approx B^l \otimes A^l$.

Storing the per-task factors $\{(B_t^l, A_t^l)\}_l$, the regularizer is evaluated without instantiating the Kronecker product:

$$\mathcal{L}^{\text{drift}}_{t \to t,t'}(\tau_{t'}) = \alpha_{t'}^2 \, \tau_{t'}^\top G_t(\theta_0) \, \tau_{t'} \overset{\text{KFAC}}{\approx} \alpha_{t'}^2 \sum_{l=1}^{L} \tau_{t'}^{l\top} (B_t^l \otimes A_t^l) \, \tau_{t'}^l$$

where $\tau^l$ is the part of $\tau$ for layer $l$ (p. 4).

**KFAC for one fully-connected layer** (p. 4). Weights $W^l \in \mathbb{R}^{D_1 \times D_2}$ (no bias), input $a_n^l \in \mathbb{R}^{D_2}$, output $z_n^l = W a_n^l \in \mathbb{R}^{D_1}$:

$$G(\mathrm{vec} W^l) \overset{\text{KFAC}}{\approx} \left( \frac{1}{|\mathcal{D}|} \sum_n (J_{z_n^l} f_n)^\top \nabla^2 c_n (J_{z_n^l} f_n) \right) \otimes \left( \frac{1}{|\mathcal{D}|} \sum_n a_n^l a_n^{l\top} \right) := B^l \otimes A^l$$

with $A^l \in \mathbb{R}^{D_2 \times D_2}$ and $B^l \in \mathbb{R}^{D_1 \times D_1}$ (p. 4).

The approximation assumes $\mathbb{E}_n[\bullet_n \otimes \star_n] \approx \mathbb{E}_n[\bullet_n] \otimes \mathbb{E}_n[\star_n]$ (p. 4).

**Computing $B^l$** (p. 5).
$A^l = \mathbb{E}_n[a_n^l a_n^{l\top}]$ is the input covariance;
$B^l = \mathbb{E}_{n,m}[g_{n,m}^l g_{n,m}^{l\top}]$ is the covariance of pseudo-gradients $g_{n,m}^l := (J_{z_n^l} f_n)^\top s_{n,m}$, obtained by backpropagating vectors $s_{n,m} \in \mathbb{R}^C$ related to $\nabla^2 c_n$.

Two variants:

- **Exact** (Botev et al., 2017): $C$ backpropagations per datum, computes $B^l$ exactly (p. 5).
- **Monte-Carlo** (Martens & Grosse, 2015): unbiased estimate with $M < C$ backpropagations per datum, typically $M = 1$ (p. 5).
  - The experiments use a single MC sample (p. 9, p. 18).

**Multi-task objective** (Eq. 7, p. 5).
Training $\tau_{t'}$ with the standard loss $\mathcal{L}_{\mathcal{D}_{t'}}(\tau_{t'}) = \frac{1}{|\mathcal{D}_{t'}|} \sum_{(x,y) \in \mathcal{D}_{t'}} c(f_{\text{lin}}(x, \tau_{t'} + \theta_0), y)$
plus drift penalties toward every other task:

$$\mathcal{L}_{\mathcal{D}_t}(\tau_{t'}) + \beta \sum_{t \neq t'} \lambda_t \mathcal{L}^{\text{drift}}_{t \to t,t'}(\tau_{t'}) \overset{\text{KFAC}}{\approx} \mathcal{L}_{\mathcal{D}_{t'}}(\tau_{t'}) + \beta \sum_{t \neq t'} \lambda_t \sum_{l=1}^{L} \tau_{t'}^{l\top} (B_t^l \otimes A_t^l) \, \tau_{t'}^l$$

(the first term's subscript is printed as $\mathcal{D}_t$ on the left and $\mathcal{D}_{t'}$ on the right, p. 5).

$\beta$ sets the overall strength, $\lambda_t$ the per-task strength, with tasks weighted by dataset size: $\lambda_t = |\mathcal{D}_t| / \sum_{t \neq t'} |\mathcal{D}_t|$ (p. 5).

**Accumulated regularizer** (Eq. 8, p. 5).
Eq. 7 stores factors for every task: $\mathcal{O}(T)$ memory and run time (p. 5).
TAK merges them into one Kronecker product per layer:

$$G_{-t'}(\theta_0^l) \overset{\text{KFAC}}{\approx} \sum_{t \neq t'} \lambda_t B_t^l \otimes A_t^l \overset{\text{merge}}{\approx} \left( \sum_{t \neq t'} B_t^l \right) \otimes \left( \sum_{t \neq t'} \lambda_t A_t^l \right)$$

"Empirically, this heuristic (Eq. (8)) matches the un-merged formulation's performance (Eq. (7))." (p. 5)

**Procedure** (Algorithms 1–2, p. 3):

- Algorithm 1:
  - compute per-task GGNs (approximated with KFAC),
  - merge over tasks $G_{-t'} = \sum_{t \neq t'} \lambda_t G_t$ (optionally merging the KFAC factors, Eq. 8),
  - return the quadratic form $\tau \mapsto \tau^\top G_{-t'} \tau$.
- Algorithm 2:
  - linearize the net;
  - until convergence, draw a mini-batch from $\mathcal{D}_{t'}$ and minimize Eq. 7 on it with respect to $\tau_{t'}$;
  - return $\tau_{t'}$.

**Error of the merge** (Appendix C, pp. 16–17). For one layer, all layers weighted equally and $\lambda_t$ omitted, the heuristic is written as (Eq. 9, p. 16):

$$\sum_{t=1}^{T} B_t \otimes A_t \approx \left( \sum_{t=1}^{T} B_t \right) \otimes \left( \frac{1}{T} \sum_{t=1}^{T} A_t \right)$$

With $\bar{A}, \bar{B}$ the means over tasks and $\Delta A_t = A_t - \bar{A}$, $\Delta B_t = B_t - \bar{B}$ (Eq. 10),
the error is exactly $E = \sum_{t=1}^T \Delta B_t \otimes \Delta A_t$ (p. 17),
bounded by (Eqs. 16–18, p. 17):

$$\|E\|_F \le T \, \sigma_A \, \sigma_B, \qquad \sigma_A := \sqrt{\frac{1}{T} \sum_{t=1}^{T} \|\Delta A_t\|_F^2}, \quad \sigma_B := \sqrt{\frac{1}{T} \sum_{t=1}^{T} \|\Delta B_t\|_F^2}$$

The error is small when the per-task factors cluster around their means,
which the authors expect with a fixed pre-trained backbone such as CLIP, whose activation and gradient statistics vary mildly across tasks (p. 17).

**Disentanglement error** (Eq. 19, pp. 17–18), from Ortiz-Jimenez et al. (2023):

$$\xi(\alpha_1, \alpha_2) = \sum_{t=1}^{2} \mathbb{E}_{x \sim \mu_t} \left[ \mathrm{dist}\left( f(x; \theta_0 + \alpha_t \tau_t), f(x; \theta_0 + \alpha_1 \tau_1 + \alpha_2 \tau_2) \right) \right]$$

with $\mathrm{dist}(y_1, y_2) = \mathbb{1}(y_1 \neq y_2)$; $\xi = 0$ means no interference at those coefficients (p. 18).

**Normalcy score / task localization** (p. 8).
For an input $x$ and task vector $\tau_t$, $\|J_\theta f(x, \theta_0) \tau_t\|_2^2$ is read as a "normalcy score" for task $t$;
the regularizer forces it low for inputs outside task $t$'s training distribution (p. 8).

## Experimental setup

**Vision, 8 Vision benchmark** (p. 5; E.1, p. 19):

- Backbones: CLIP ViT-B/32, ViT-B/16, ViT-L/14 (Table 1, p. 6).
- Tasks: Stanford Cars, DTD, EuroSAT, GTSRB, MNIST, RESISC45, SUN397, SVHN (p. 19).
- One checkpoint per task and method, merged into one model (p. 5); absolute and normalized accuracy reported, following Ortiz-Jimenez et al. (2023) (p. 5).
- $\alpha$: either $\alpha_t = \alpha = 1$ for all tasks (plain addition) or tuned on a cross-task validation set ("Best") (p. 5).
- Training (p. 19):
  - batch size 128;
  - AdamW, learning rate $3 \times 10^{-4}$, weight decay 0.1, cosine annealing;
  - no gradient clipping.
  - The learning rate is higher than in previous work, which the explicit regularizer allows "without introducing interference across tasks" (p. 19).
- Regularization weight: $\lambda = 100$ (ViT-B/32), $\lambda = 500$ (ViT-B/16), $\lambda = 2000$ (ViT-L/14) (p. 19).
- The regularization weight of the last layer of the CLIP visual encoder is rescaled by 0.1 (p. 19).

**Text, 6NLI** (p. 7; E.2, pp. 19–20):

- T5-base; tasks SNLI, MultiNLI, SICK (three-way), SciTail, RTE, QNLI (binary); fine-tuning and evaluation restricted to two labels (pp. 19–20).
- Batch size 128;
  AdamW, learning rate $3 \times 10^{-4}$, iteration-based cosine annealing, weight decay 0.01;
  no gradient clipping;
  $\lambda = 20$ for KFAC, $\lambda = 0.1$ for the diagonal regularization (p. 20).

**Curvature estimation** (p. 9; E, p. 18):

- One Monte Carlo sample; GGN computed on 33% of the training data, though 250–300 training points were found sufficient (p. 18).
- Main-text timing: 128 examples per task, all 8 Vision tasks in 4 minutes (p. 9).
- KFAC for all linear projections (attention and feed-forward); the full, exact GGN for LayerNorm parameters and the class token, whose size grows linearly with the embedding dimension (p. 18).
- The KFAC loss is applied to all fine-tuned layers (p. 19).

**Regimes compared** (p. 6–7):

- **Linearized:** linear FT, $\tau$Jp (Yoshida et al., 2025, uses other tasks' data), a diagonal-GGN regularizer inspired by Porrello et al. (2025), TAK.
- **Non-linear:** non-linear FT, attention-only FT (Jin et al., 2025), TaLoS (Iurada et al., 2025; numbers taken from its paper), and attention-only FT + TAK.
  - TAK is not exact outside the linearized regime;
    it's paired with attention-only FT, which "has been shown to induce approximately linear fine-tuning dynamics in Transformers" (p. 7).

**Post-hoc merging methods** (p. 8): TIES, TSV, ISO, applied to non-linear checkpoints and to linearized checkpoints with and without KFAC.

**Negation** (p. 7, Table 2):

- Each task vector subtracted from the pre-trained model;
- ImageNet as the control task;
- reported is the minimum target accuracy keeping at least 95% of the pre-trained control accuracy (Table 2 caption, p. 7).

**Class-incremental partitions** (F.7, p. 24): one dataset split into disjoint class partitions:

- ImageNet-R: 10 tasks of 20 classes;
- RESISC45: 9 tasks of 5;
- EuroSAT: 5 tasks of 2.

Models fine-tuned on each partition are merged and evaluated on the union of all classes (joint classification), following Porrello et al. (2025).

## Results

**Task addition, 8 Vision** (Table 1, p. 6). Accuracy (%), absolute and normalized. "1.0" = all coefficients fixed to 1.0; "Best" = tuned $\alpha$. TaLoS numbers are taken from its paper (†).

| Method | Dataless | $\alpha$ | B/32 Abs. | B/32 Norm. | B/16 Abs. | B/16 Norm. | L/14 Abs. | L/14 Norm. |
|---|---|---|---|---|---|---|---|---|
| Pre-trained | – | – | 48.4 | – | 55.4 | – | 65.0 | – |
| Individual | – | – | 90.9 | – | 92.4 | – | 93.8 | – |
| *Linear fine-tuning* | | | | | | | | |
| Linear FT | – | 1.0 | 76.7 | 87.2 | 80.2 | 88.9 | 88.0 | 94.8 |
| Linear FT | – | Best | 78.8 | 89.9 | 82.0 | 90.9 | 88.0 | 94.8 |
| $\tau$Jp | no | 1.0 | 85.0 | 97.4 | 88.2 | 98.3 | 90.9 | 98.3 |
| $\tau$Jp | no | Best | 85.6 | 98.2 | 88.6 | 98.7 | 91.1 | 98.5 |
| Diag. GGN | yes | 1.0 | 80.1 | 92.3 | 82.9 | 93.2 | 87.9 | 96.3 |
| Diag. GGN | yes | Best | 80.2 | 92.5 | 83.0 | 93.3 | 88.0 | 96.4 |
| TAK | yes | 1.0 | 85.8 | 97.6 | 88.3 | 97.9 | 91.6 | 99.3 |
| TAK | yes | Best | 86.0 | 97.8 | 88.3 | 98.1 | 91.6 | 99.3 |
| *Non-linear fine-tuning* | | | | | | | | |
| Non-linear FT | – | 1.0 | 32.0 | 32.9 | 27.4 | 28.2 | 45.3 | 47.5 |
| Non-linear FT | – | Best | 73.5 | 80.4 | 77.0 | 82.9 | 84.5 | 89.7 |
| Attn. Only FT | – | 1.0 | 22.5 | 23.3 | 22.8 | 23.4 | 66.2 | 69.7 |
| Attn. Only FT | – | Best | 78.2 | 86.3 | 80.4 | 87.1 | 88.2 | 93.8 |
| TaLoS† | yes | Best | 79.7 | 90.8 | 82.6 | 92.4 | 88.3 | 95.2 |
| Attn. Only FT + TAK | yes | 1.0 | 60.3 | 64.5 | 59.0 | 62.3 | 82.1 | 87.2 |
| Attn. Only FT + TAK | yes | Best | 83.1 | 91.3 | 84.3 | 91.0 | 89.9 | 95.9 |

The paper's comments on Table 1:

- TAK performs "on par with" $\tau$Jp "while avoiding any reliance on external data from other tasks" (p. 6).
- Plain addition ($\alpha = 1$) "performs competitively, suggesting that post-hoc tuning can be safely omitted" (p. 6).
- On ViT-B/32, the smaller the model, the more curvature regularization matters (p. 6);
  - ViT-L/14 gains least, especially in the non-linear regime, consistent with Ortiz-Jimenez et al. (2023): very large models "may already display an implicit form of regularization" (F.1, p. 20).
- Even the diagonal regularizer beats plain linear fine-tuning (p. 6).
- In the non-linear regime, $\alpha$ "has a stronger impact on the final accuracy" (p. 7).

**Task negation, 8 Vision** (Table 2, p. 7). Minimum target accuracy (↓) keeping at least 95% of pre-trained control accuracy (↑), in %:

| Method | Dataless | B/32 Targ. | B/32 Cont. | B/16 Targ. | B/16 Cont. | L/14 Targ. | L/14 Cont. |
|---|---|---|---|---|---|---|---|
| Pre-trained | – | 48.4 | 63.3 | 55.4 | 68.3 | 65.0 | 75.5 |
| Non-linear FT | – | 20.4 | 60.5 | 20.4 | 65.3 | 18.1 | 72.4 |
| Linear FT | – | 9.3 | 60.5 | 8.3 | 65.5 | 7.5 | 72.1 |
| TaLoS† | yes | 11.0 | 60.7 | 10.6 | 66.1 | 10.7 | 73.6 |
| $\tau$Jp | no | 6.7 | 60.8 | 4.7 | 66.0 | 3.7 | 73.0 |
| TAK | yes | 3.4 | 62.4 | 3.4 | 66.4 | 3.5 | 72.6 |

**Task addition, T5-base, 6NLI** (Fig. 3a, p. 7: best-performing $\alpha$; Table 8, p. 25: $\alpha = 1$). Accuracy (%):

| Method | Dataless | Abs. (Best $\alpha$) | Norm. (Best $\alpha$) | Abs. ($\alpha = 1$) | Norm. ($\alpha = 1$) |
|---|---|---|---|---|---|
| Individual | – | 85.9 | – | 85.9 | – |
| MTL | – | 83.6 | – | not reported | not reported |
| Non-lin. FT | – | 75.7 | 87.7 | 65.5 | 75.9 |
| Linear FT | – | 76.9 | 92.8 | 76.1 | 92.0 |
| Attn. Only FT | – | 72.9 | 85.2 | 67.0 | 78.3 |
| TaLoS | yes | 76.3 | 93.4 | 75.8 | 92.8 |
| $\tau$Jp | no | 81.3 | 100 | 81.0 | 99.5 |
| TAK | yes | 78.7 | 98.9 | 78.6 | 98.7 |

TAK "consistently outperforms the baselines, particularly under non-linear fine-tuning",
but $\tau$Jp, which uses other tasks' data, gains more on text, "suggesting that textual domains may still benefit from even more accurate curvature estimation" (p. 7).

**Accumulated vs. per-task regularizer** (Table 3, p. 9).

- "Naïve Multi-Task FT" here is the per-task objective of Eq. 7 ($\mathcal{O}(T)$), not joint training on all tasks;
- "Accumulated reg." is TAK with Eq. 8 ($\mathcal{O}(1)$):

| Method | Complexity | $\alpha$ | B/32 Abs. | B/32 Norm. | B/16 Abs. | B/16 Norm. | T5 Abs. | T5 Norm. |
|---|---|---|---|---|---|---|---|---|
| Naïve Multi-Task FT | $\mathcal{O}(T)$ | 1.0 | 86.5 | 98.4 | 88.0 | 97.5 | 78.5 | 97.0 |
| Naïve Multi-Task FT | $\mathcal{O}(T)$ | Best | 86.6 | 98.5 | 88.1 | 97.6 | 78.5 | 97.0 |
| Accumulated reg. (TAK) | $\mathcal{O}(1)$ | 1.0 | 85.8 | 97.6 | 88.3 | 97.9 | 78.6 | 98.7 |
| Accumulated reg. (TAK) | $\mathcal{O}(1)$ | Best | 86.0 | 97.8 | 88.3 | 98.1 | 78.7 | 98.9 |

The gap is "marginal" for ViT-B/16 and T5-base; for ViT-B/32 a "small but consistent gap" favors the per-task objective (p. 9).

**Post-hoc merging, linearized checkpoints** (Table 4, p. 20), accuracy (%):

| Method | $\alpha$ | B/32 Abs. | B/32 Norm. | B/16 Abs. | B/16 Norm. |
|---|---|---|---|---|---|
| Linear FT + TIES | 1.0 | 77.1 | 87.8 | 80.1 | 88.7 |
| Linear FT + TIES | Best | 77.2 | 87.8 | 80.3 | 88.9 |
| Linear FT + TSV | 1.0 | 84.2 | 96.3 | 86.7 | 96.5 |
| Linear FT + TSV | Best | 84.2 | 96.3 | 86.8 | 96.6 |
| Linear FT + ISO | 1.0 | 83.8 | 95.8 | 86.9 | 96.7 |
| Linear FT + ISO | Best | 84.4 | 96.4 | 87.3 | 97.1 |
| TAK + TIES | 1.0 | 81.8 | 92.7 | 86.6 | 95.9 |
| TAK + TIES | Best | 82.0 | 92.8 | 87.1 | 96.6 |
| TAK + TSV | 1.0 | 84.7 | 96.3 | 87.6 | 97.2 |
| TAK + TSV | Best | 84.7 | 96.3 | 87.7 | 97.3 |
| TAK + ISO | 1.0 | 84.2 | 95.6 | 87.2 | 96.8 |
| TAK + ISO | Best | 84.2 | 95.6 | 87.3 | 96.9 |

- TA and TIES gain most from curvature regularization; ISO and TSV already do well without it; all stay below TAK with plain addition (p. 8; Table 1: 85.8/86.0 on B/32, 88.3 on B/16).
- **$\alpha$-sweep over $[0, 2]$** for $\theta_0 + \alpha \mathcal{M}(\{\tau_t\}_{t=1}^T)$ on ViT-B/32 (Fig. 4a, p. 8):
  - with KFAC, plain TA reaches the best peak and stays stable "over a wide interval of $\alpha$ values" (p. 8);
  - same trends on ViT-B/16 (F.2, p. 21; Fig. 11, p. 20).
  - **Our reading** of Fig. 4a:
    - TA with KFAC is already at about 84 at $\alpha = 0.25$ and stays near its peak up to 2.0;
    - TIES and TSV on non-linear checkpoints peak at about $\alpha = 0.75$–1.0 and fall off on both sides;
    - ISO peaks at about 1.25–1.5 (about 84.5) and degrades only mildly up to $\alpha = 2$ (about 82).
- In the non-linear regime, attention-only FT and its KFAC variant are more robust to $\alpha$ than standard non-linear FT, but much more sensitive than linearized TAK (F.2, p. 21; Fig. 12, p. 21).

**Ablation of the regularization weight $\lambda$** (Table 5, p. 21). Absolute accuracy (%), $\alpha = 1$, three seeds.

These runs use the hyperparameters of Sec. E, so they differ from Table 1, whose linear fine-tuning follows Ilharco et al. (2022) (p. 21):

| ViT-B/32 $\lambda$ | Seed 7 | Seed 21 | Seed 42 | Avg. |
|---|---|---|---|---|
| 0 | 75.0 | 75.4 | 75.1 | 75.2 ± 0.028 |
| 1 | 82.2 | 82.4 | 80.6 | 81.7 ± 0.648 |
| 10 | 85.2 | 85.1 | 85.1 | 85.1 ± 0.002 |
| 100 | 86.2 | 85.8 | 86.0 | 86.0 ± 0.026 |
| 1000 | 86.5 | 86.4 | 86.4 | 86.4 ± 0.002 |
| 10000 | 84.5 | 84.4 | 84.3 | 84.4 ± 0.006 |

| ViT-B/16 $\lambda$ | Seed 7 | Seed 21 | Seed 42 | Avg. |
|---|---|---|---|---|
| 0 | 79.1 | 78.7 | 79.1 | 79.0 ± 0.188 |
| 1 | 83.2 | 83.4 | 83.8 | 83.5 ± 0.265 |
| 50 | 86.9 | 86.8 | 87.0 | 86.9 ± 0.059 |
| 500 | 88.0 | 87.9 | 88.2 | 88.0 ± 0.114 |
| 5000 | 88.3 | 88.4 | 88.4 | 88.4 ± 0.015 |
| 50000 | 86.7 | 86.6 | 86.6 | 86.6 ± 0.002 |

The authors: optimal between $10^2$ and $10^3$, minor degradation at $\lambda = 10$ and $\lambda = 10^4$; "no precise tuning of $\lambda$ is required" (pp. 21–22).

**Universal KFAC from ImageNet-1k** (Table 6, p. 22). One pair of $A/B$ factors per layer computed on ImageNet-1k replaces the task-specific ones:

| Method | $\alpha$ | B/32 Abs. | B/32 Norm. | B/16 Abs. | B/16 Norm. |
|---|---|---|---|---|---|
| Linear FT | 1.0 | 76.7 | 87.2 | 80.2 | 88.9 |
| Linear FT | Best | 78.8 | 89.9 | 82.0 | 90.9 |
| TAK | 1.0 | 85.8 | 97.6 | 88.3 | 97.9 |
| TAK | Best | 86.0 | 97.8 | 88.3 | 98.1 |
| ImageNet-TAK | 1.0 | 84.7 | 97.0 | 86.0 | 95.4 |
| ImageNet-TAK | Best | 84.7 | 97.0 | 86.0 | 95.4 |

The proxy recovers "approximately 97–99%" of the full task-specific performance (p. 22).

**Class-incremental partitions, ViT-B/16** (Table 7, p. 24), accuracy (%) on the joint problem:

| Model | ImageNet-R | EuroSAT | RESISC45 |
|---|---|---|---|
| Zero-shot | 77.72 | 49.48 | 66.02 |
| Non-linear FT | 82.32 | 71.21 | 73.85 |
| Linear FT | 81.66 | 70.40 | 72.28 |
| Linear FT w. Diag. GN | 81.64 | 73.94 | 74.04 |
| $\tau$jP (Yoshida et al., 2025) | 81.28 | 84.36 | 84.83 |
| TAK (naive penalty) | 82.64 | 79.64 | 78.91 |
| TAK (aggregated penalty) | 82.63 | 79.64 | 78.30 |

The authors claim "state-of-the-art performance even under this more challenging setting" (p. 24).

**Our reading:** this holds among dataless methods only, since $\tau$jP (which uses other tasks' data) is higher on EuroSAT and RESISC45.

**Task localization** (Fig. 5, p. 8; F.5, pp. 22–23; F.6, p. 24).

- With KFAC, the distribution of $\|J_\theta f(x, \theta_0)\tau_t\|_2^2$ is pushed toward zero for inputs of other tasks and clearly separated from task $t$'s own inputs;
  with plain linear fine-tuning the separation is "much less clear" (p. 8).
- The separation persists under non-linear fine-tuning with KFAC; TaLoS and attention-only FT show a weaker separation (p. 23, Fig. 13).
- Block-compressed KFAC keeps it (p. 24, Fig. 14).
- The authors suggest a "natural use of our method for out-of-distribution detection" (p. 9).

**Costs** (p. 9; Fig. 6, p. 9):

- No overhead at inference (p. 9).
- KFAC estimation for the 8 Vision tasks (128 examples per task, one MC sample): 3.9 minutes, against 198.7 with the exact approach;
  per batch of 8 examples, $A$ takes 1.4 s in both and $B$ 91.5 s (exact) vs 0.2 s (MC) (Fig. 6b, p. 9).
- Training time per forward-backward pass, as printed on the bars (Fig. 6a, p. 9; backbone not stated):
  - non-linear 0.5 s, non-linear (attention) 0.4 s, non-linear (attention) with KFAC 0.6 s;
  - linear FT 1.1 s, linear FT with KFAC 1.3 s, $\tau$Jp 3.2 s.
  - KFAC takes "roughly one third of the training time of $\tau$Jp" (p. 9).
- Peak VRAM: linearized +12% (11.5 → 12.9 GB); non-linear attention-only +22% (6.8 → 8.3 GB); $\tau$Jp 12.3 GB; standard non-linear FT 8.5 GB (p. 9).

**KFAC estimation and compression** (Fig. 7, p. 10; F.6, p. 23):

- 128–256 examples already saturate performance, comparable to using 30% of each training set; final performance is generally on par with the exact approach (p. 10).
- 1–2 MC samples per example suffice; more MC samples worsen performance, with variance across seeds growing (p. 10).
- Compression on ViT-B/16: the block-diagonal strategy (8 blocks per factor) cuts memory from about 550 MB to about 70 MB (87% reduction)
  for about a 1-point drop in absolute accuracy (88.3 → 87.1) (p. 10).
  - Other strategies tested: truncated SVD (rank 32, or 25% of the rank), magnitude pruning (keep 30% or 15%), dynamic 8-bit quantization (p. 23).
- **Applying the loss every $N$ steps** (Fig. 8, p. 10), absolute accuracy (%) as printed on the bars (Best $\alpha$ / $\alpha = 1$):
  - $N = 1$: 88.3 / 88.3;
  - $N = 2$: 88.2 / 88.2;
  - $N = 4$: 87.5 / 87.4;
  - $N = 8$: 87.1 / 87.1;
  - $N = 16$: 87.0 / 87.0;
  - no KFAC: 82.0 / 80.2.
  - The text calls the $N = 16$ loss "∼1.4 points" (p. 10), while the bars give 88.3 − 87.0 = 1.3.
  - **Our reading:** the backbone isn't stated; the values (88.3; no KFAC 82.0 / 80.2) match the ViT-B/16 rows of Table 1, so it is probably ViT-B/16.

**Weight disentanglement maps** (Fig. 9, p. 18; Fig. 1, p. 2):

- On ViT-B/16, linearized fine-tuning improves disentanglement and the KFAC regularizer improves it further;
- darker regions remain mostly for $\alpha > 1$;
- the error is "consistently close to zero along the diagonals", the common choice $\alpha_1 = \dots = \alpha_n$ (p. 18).

## Assumptions and limitations

- **Linearization:** the regularizer is derived for the linearized model (Eqs. 1–3, p. 3); it is "not theoretically exact in the non-linear regime" (p. 7).
- **Squared-error drift:** the Jacobian Gramian is the GGN of a squared loss (p. 4), so drift is measured as squared $\ell_2$ distance of outputs (Eq. 2, p. 3), whatever the training loss.
- **Shared factors still needed:** the method removes the need for other tasks' raw data but still needs their pre-computed KFAC factors (F.4, p. 22);
  a task-agnostic ImageNet factor recovers most of the benefit (Table 6, p. 22).
- **Memory:** KFAC stores two matrices per layer, each quadratic in the number of units, which can become problematic for large models (B, p. 16); compression helps (p. 10).
- **Text:** results "indicate room for improvement" (B, p. 16); $\tau$Jp stays ahead on T5-base (Fig. 3a, p. 7).
- **Merge heuristic:** Eq. 8 is a heuristic whose error grows with the spread of per-task factors (C, p. 17); it matches Eq. 7 empirically (Table 3, p. 9), with a small gap on ViT-B/32 (p. 9).
- **Future work named by the authors:** curvature approximations that merge without loss (B, p. 16); full or parameter-efficient fine-tuning (p. 10).
- **Our reading:**
  - In Eq. 7, every task $t'$ is trained against the factors of **all other tasks**, so all tasks' factors must exist before training;
    no stream of tasks arriving one at a time is tested.
    The paper's own answer for tasks "not known in advance at training time" is task-agnostic factors from ImageNet (F.4, p. 22; see "Task-agnostic factors" below).
  - Two weights are both called $\lambda$:
    - the per-task weights $\lambda_t$ of Eq. 7 (p. 5) and
    - the regularization weights of Sec. E and Table 5 ($\lambda = 100, 500, 2000, 20$; pp. 19–21).
    - We read the latter as playing the role of $\beta$ in Eq. 7; the paper doesn't say so explicitly.
  - The amount of data used for KFAC is stated four ways:
    - 128 examples per task (p. 9);
    - 128–256 examples, "comparable to" 30% of each training set (p. 10);
    - a red reference line labeled "0.3% of all data" in Fig. 7a, whose x-axis stops at 128 examples and whose backbone isn't stated (p. 10); and
    - 33% of the training data with 250–300 points sufficient (p. 18).
  - "Best" $\alpha$ is tuned on a cross-task validation set (p. 5), so the "Best" rows aren't dataless at selection time; the $\alpha = 1$ rows are.
  - The experiments are all classification (images, NLI); nothing on regression, time series or anomaly detection.

## Relevance to this thesis

**Our reading:**

- **A third option between joint training and plain task arithmetic.**
  - TAK keeps training per task (modular, no shared data) but adds a curvature penalty that approximates "don't change the other tasks' outputs".
  - It is a natural candidate next to our two main arms: joint training and plain task arithmetic.
- **A joint-training number exists only for text:** on T5-base, MTL (undefined in the paper; presumably joint multi-task training) reaches 83.6, individual models 85.9, TAK 78.7 (Fig. 3a, p. 7).
  - The vision tables have no joint-training row; Table 3's "Naïve Multi-Task FT" is the per-task regularizer, not joint training (p. 9).
  - We should not cite Table 3 as a joint-training comparison.
- **Forecasting fits the derivation well:** with a squared-error loss, the GGN equals the Jacobian Gram matrix exactly (p. 4),
  so for MSE-trained forecasters the regularizer measures exactly the output drift we'd want to control.
- **Anomaly detection may reuse the localization score:**
  - $\|J_\theta f(x, \theta_0)\tau_t\|_2^2$ separates a task's inputs from other tasks' inputs (Fig. 5, p. 8), and the authors themselves suggest out-of-distribution detection (p. 9).
  - Whether this score works as an anomaly score on time series is untested.
- **Continual setting needs an adaptation:** Eq. 7 assumes factors for all other tasks are available when training each task vector.
  - In a sequential stream we would only have past tasks' factors;
  - the accumulated form of Eq. 8 (one running pair of sums per layer) fits a sequential update, but the paper doesn't test it.
- **Robustness to $\alpha$** (Fig. 4a, p. 8; Table 1, p. 6) matters when there's no validation set to tune $\alpha$, which is common in anomaly detection without labeled anomalies.
- **Task-agnostic factors** (Table 6, p. 22): factors from the pre-training data could serve as a universal prior, removing any coupling between tasks;
  for time series, the analogue would be factors from the pre-training corpus.
- **Settings that may not carry over:** the merge error bound relies on factors varying little across tasks under a fixed strong backbone (p. 17);
  our tasks may come from a much smaller pre-trained model, and the paper finds smaller models more sensitive to the quality of the approximation (p. 9).
- **Costs to plan for:** linearized fine-tuning roughly doubles training time per step relative to non-linear (1.1 s vs 0.5 s, Fig. 6a, p. 9) and raises VRAM; KFAC itself adds little on top.

## Quotes worth keeping

> "Therefore, our goal is to design a computationally efficient regularizer for weight disentanglement that can be used without requiring access to the training data." (p. 1)

> "Hence, the matrix $G_t(\theta_0)$ of the quadratic form in Eq. (3) corresponds to a curvature matrix: the GGN of the loss $\mathcal{L}(\theta)$ (Eq. (4)) when the training criterion is the squared loss." (p. 4)

> "Empirically, this heuristic (Eq. (8)) matches the un-merged formulation's performance (Eq. (7))." (p. 5)

> "Furthermore, whereas competing methods often require coefficient grid search, TAK proves highly robust: even a simple addition of task vectors (α = 1) performs competitively, suggesting that post-hoc tuning can be safely omitted." (p. 6)

> "Moreover, this property suggests a natural use of our method for out-of-distribution detection, as it provides a principled mechanism to assess whether an input lies within the model training distribution." (p. 9)

> "In this regard, although our regularization is not theoretically exact in the non-linear regime, its applicability can still be justified whenever linearized behavior is implicitly enforced." (p. 7)
