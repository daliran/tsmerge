# anon2026quasi — Quasi-Orthogonal Model Merging for Continual Learning

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 105 claims: 1 minor misstatement and 1 unsourced detail, fixed; 2 omissions added)
- **Reference:** Anonymous authors; submission under double-blind review at ICLR 2026, so **not peer-reviewed yet** and authors unknown (p. 1) ([references.bib](references.bib))
- **Version read:** the ICLR 2026 review PDF (submission 11188, per its download file name; the number isn't printed in the PDF), 13 pages: main text pp. 1–9, references pp. 10–12, appendix pp. 12–13
- **Read:** everything: main text (Sections 1–6, pp. 1–9), references (pp. 10–12), appendix A.1–A.2 (pp. 12–13)
- **Code:** not available; "Our code will be released." (p. 1)

## In one paragraph

The paper proposes **QOMM**, a model-merging method for continual learning (CL) with two parts (p. 1, p. 4). **Quasi-Orthogonal Projection (QOP)**: at each new task, the new task vector is projected, matrix by matrix, onto the approximate orthogonal complement of the dominant singular subspace of the task vectors merged so far, then added to the merged vector with a $\sqrt{i}$ normalization that keeps the merged update from growing (pp. 4–6). **Attention-Exclusive Fine-Tuning (AEFT)**: only the attention matrices $W_q, W_k, W_v, W_o$ are fine-tuned, which the authors hypothesize makes task vectors more orthogonal and so helps QOP (p. 4, p. 6). With CLIP ViT-B/16 on class-incremental Split-CIFAR100, ImageNet-R, CUB200 and Cars, QOMM reaches **77.49%** average task-agnostic accuracy after the final task, **+2.99** over MagMax, the best prior method (Table 1, p. 8); joint training reaches **87.38%** on the same average (Table 1, p. 8). On domain-incremental DomainNet, EWC is best (70.74%) and QOMM gets 69.32% (Table 2, p. 8).

## Problem

**Model-merging-based continual learning (MMCL)** (p. 3, Section 3.1):

- A sequence of $N$ disjoint task datasets $\mathcal{D} = \{D_i\}_{i=1}^N$; a pre-trained model with parameters $\Theta_0$ "is fine-tuned sequentially on each dataset $D_i$", producing $\Theta_i$ (p. 3).
- Task vector $\Delta\Theta_i = \Theta_i - \Theta_0$; collection $\mathcal{T} = \{\Delta\Theta_i\}_{i=1}^N$ (p. 3).
- At task $i$ the merged model is $\hat{\Theta}_i$, with merged task vector $\Delta\hat{\Theta}_i = \hat{\Theta}_i - \Theta_0$, updated iteratively with the new $\Delta\Theta_i$ "while mitigating interference" (p. 3).
- Goal: a final merged model $\hat{\Theta}_N$ that does well on all $N$ tasks "without access to any individual task dataset $D_i$"; previous training data are not revisited (p. 3).

**The issue addressed:** task interference at consolidation; when task vectors overlap in conflicting directions, naive merging "can overwrite or negate essential knowledge from earlier tasks", with degradation that worsens as the number of tasks grows (pp. 1–2). Heuristic rules such as magnitude-based selection lack "an explicit mechanism to guarantee compatibility between new and accumulated updates" (p. 2).

## Method

**Overview** (Figure 1, p. 4; Algorithm 1, p. 5):

- $\Theta_1 = \mathrm{AEFT}(\Theta_0)$, $\hat{\Theta}_1 = \Theta_1$, $\lambda_1 = 1$ (Algorithm 1, lines 1–3, p. 5).
- For $i = 2, \dots, N$: $\Theta_i = \mathrm{AEFT}(\Theta_{i-1})$, i.e. each task is fine-tuned **starting from the previous fine-tuned model**, not from the merged one or from $\Theta_0$ (Algorithm 1, line 5, p. 5; Figure 1, p. 4); $\lambda_i = \sqrt{i}$ (line 6).
- QOP runs over the attention weight matrices $(W_0, \hat{W}_{i-1}, W_i) \in \mathbb{R}^{m \times n}$ of $(\Theta_0, \hat{\Theta}_{i-1}, \Theta_i)$ (line 7, p. 5); every matrix-level operation is applied "independently and identically to each attention matrix" (p. 5).
- Returns $\hat{\Theta}_N$ (line 16, p. 5).

**Per-matrix notation** (p. 5): for an attention matrix $W \in \mathbb{R}^{m \times n}$ in layer $\ell$: pre-trained $W_0^{(\ell)}$; task-specific $W_i^{(\ell)}$; cumulative merge after tasks $1{:}i-1$, $\hat{W}_{i-1}^{(\ell)}$. Task vectors are always relative to the pre-trained weights:

$$\Delta W_i^{(\ell)} = W_i^{(\ell)} - W_0^{(\ell)}, \qquad \Delta\hat{W}_{i-1}^{(\ell)} = \hat{W}_{i-1}^{(\ell)} - W_0^{(\ell)}$$

**SVD of the merged task vector** (Eq. 1, p. 5), a full SVD:

$$\Delta\hat{W}_{i-1} = U_{i-1} \Sigma_{i-1} \left(V_{i-1}\right)^\top$$

with $U_{i-1} \in \mathbb{R}^{m \times m}$, $V_{i-1} \in \mathbb{R}^{n \times n}$, $\Sigma_{i-1} \in \mathbb{R}^{m \times n}$ diagonal with singular values in descending order (p. 5).

**Basis of matrix space** (Eq. 2, p. 5): $B_{pq} = u_p v_q^\top$, with $u_p, v_q$ the $p$-th and $q$-th columns of $U_{i-1}$ and $V_{i-1}$; $\{B_{pq}\}$ is an orthonormal basis under the Frobenius inner product $\langle \cdot, \cdot \rangle_F$:

$$\Delta\hat{W}_{i-1} = \sum_{p,q} c_{pq} B_{pq}, \qquad c_{pq} = \langle \Delta\hat{W}_{i-1}, B_{pq} \rangle_F$$

**Projection operator** (Eq. 3, p. 5), removing the components along the top $r_\alpha$ singular directions:

$$\mathcal{O}^\perp\left(\Delta W_i, \Delta\hat{W}_{i-1}\right) = \Delta W_i - \sum_{j=1}^{r_\alpha} \langle \Delta W_i, B_{jj} \rangle_F \cdot B_{jj}$$

**Threshold rank** (Eq. 4, p. 5): the smallest rank whose singular values hold a fraction $\alpha$ of the energy:

$$r_\alpha = \min\left\{ k \;\middle|\; \frac{\sum_{j=1}^{k} \sigma_j^2}{\sum_{j=1}^{\min(m,n)} \sigma_j^2} \geq \alpha \right\}, \qquad \alpha \in [0, 1]$$

$\alpha$ is the projection threshold hyperparameter, balancing retained and new knowledge (p. 6). The projection is "quasi"-orthogonal because only the dominant subspace is excluded, a low-rank approximation of an orthogonal projection (p. 2).

**Naive update rule** (Eq. 5, p. 6), printed as:

$$\Delta\hat{W}_i = \Delta\hat{W}_{i-1} + \mathcal{O}^\perp\left(\Delta W i, \Delta\hat{W}_{i-1}\right)$$

Its limitation, as stated (p. 6): the Frobenius norm of $\Delta\hat{W}_i$ "grows monotonically" with the number of tasks, so the merged model drifts ever further from the pre-trained initialization.

**Adaptive update rule** (Eq. 6, p. 6), printed as:

$$\Delta\hat{W}_i = \frac{\lambda_{i-1} \Delta\hat{W}_{i-1} + \mathcal{O}^\perp\left(\Delta W_i, \Delta\hat{W}_i\right)}{\lambda_i}, \qquad \lambda_1 = 1, \; \lambda_i = \sqrt{i}$$

Each task's orthogonal contribution is "treated as equally important" (p. 6). Algorithm 1 writes the same step with $\Delta W_i^\perp \leftarrow \mathcal{O}^\perp(\Delta W_i, \Delta\hat{W}_{i-1})$ and $\Delta\hat{W}_i \leftarrow (\lambda_{i-1}\Delta\hat{W}_{i-1} + \Delta W_i^\perp)/\lambda_i$ (lines 10–11, p. 5).

**Merged parameters** (Eq. 7, p. 6):

$$\hat{W}_i = W_0 + \Delta\hat{W}_i$$

**Attention-Exclusive Fine-Tuning** (Section 4.3, p. 6; Figure 2, p. 6): only $W_q, W_k, W_v, W_o$ are trainable; layer norms and feed-forward layers stay fixed. Motivated by two prior observations: fine-tuning only attention modules improves merged-model performance (Jin et al., 2025), and orthogonality among task vectors is critical for interference (Xiong et al., 2024) (p. 6). The authors hypothesize that AEFT yields more orthogonal task vectors and so improves QOP (p. 4, p. 6).

**Memory** (p. 8): at any step only three models are kept: the current merged one, the incoming one and the pre-trained base, so memory is $\mathcal{O}(|\Theta|)$, independent of the number of tasks.

**Our reading:**

- Eq. 6 as printed projects against $\Delta\hat{W}_i$ (the quantity being defined), and Eq. 5 prints $\Delta W i$; Algorithm 1 (line 10, p. 5) uses $\Delta\hat{W}_{i-1}$, the consistent form of the projection; but Algorithm 1 has index slips too: line 12 writes the merge back as $\hat{W}_{i-1} \leftarrow W_0 + \Delta\hat{W}_i$, and line 14 sets $\hat{\Theta}_i = \hat{\Theta}_{i-1}$ (an in-place update) (p. 5). We take line 10's form as the intended definition.
- Unrolling Algorithm 1 (our derivation, not in the paper): $\sqrt{i}\,\Delta\hat{W}_i = \sqrt{i-1}\,\Delta\hat{W}_{i-1} + \Delta W_i^\perp$, so $\Delta\hat{W}_i = \frac{1}{\sqrt{i}}\left(\Delta W_1 + \sum_{j=2}^{i} \Delta W_j^\perp\right)$. QOP is therefore task arithmetic on projected task vectors, with a scaling coefficient $1/\sqrt{i}$ fixed by the number of tasks instead of tuned. If the projected vectors were mutually orthogonal with equal norms, the merged norm would stay constant.
- Eq. 3 removes only the components along the $r_\alpha$ rank-one matrices $u_j v_j^\top$ ($p = q = j$), not along all $u_p v_q^\top$ with $p, q \le r_\alpha$, nor the full column or row space of the top singular vectors. It is a projection onto the complement of an $r_\alpha$-dimensional subspace of $\mathbb{R}^{m \times n}$.
- Algorithm 1 only loops over attention matrices; with AEFT, the other parameters never change from $\Theta_0$. How QOP alone (without AEFT, Table 3) treats non-attention parameters is not stated.

## Experimental setup

**Datasets** (p. 7), following MagMax's setup:

- **Class-incremental (CIL):** CIFAR100 and ImageNet-R (generic), split into $N \in \{5, 10, 20, 50\}$ tasks; CUB200 and Cars (fine-grained), $N \in \{5, 10, 20\}$, because they are smaller. Each dataset is partitioned into $N$ disjoint subsets of classes.
- **Domain-incremental (DIL):** DomainNet, six tasks, one per domain (clipart, infographics, painting, quickdraw, real, sketch).

**Baselines** (p. 7):

- CL methods: LwF, EWC.
- Merging: ModelSoup, Task Arithmetic (TA), TIES-Merging, MagMax and its two variants RandMix (each parameter sampled at random from one of the fine-tuned models) and MaxAbs (independent fine-tuning instead of sequential adaptation).
- Zero-shot (the pre-trained model) and **Joint** ("a model fine-tuned on the entire dataset").

**Implementation** (pp. 7–8):

- CLIP with a ViT-B/16 image encoder; AdamW with weight decay and a cosine-annealing learning-rate schedule, following Ilharco et al. (2022b) (p. 7).
- Classification layer: built from CLIP's text encoder and kept **frozen** during fine-tuning (pp. 7–8).
- One NVIDIA GeForce RTX 4090 GPU per experiment (p. 8).
- $\alpha = 0.55$ in all experiments (p. 9).
- Per split task (p. 7):

| Dataset | Batch size | Learning rate | Epochs | Weight decay |
|---|---|---|---|---|
| CIFAR-100 | 64 | $1.8 \times 10^{-5}$ | 20 | 0.09 |
| ImageNet-R | 64 | $1.7 \times 10^{-5}$ | 20 | 0.09 |
| CUB-200 | 32 | $3 \times 10^{-5}$ | 24 | 0.09 |
| Cars | 32 | $3 \times 10^{-5}$ | 24 | 0.09 |
| DomainNet | 64 | $1.8 \times 10^{-5}$ | 20 | 0.09 |

**Metric:** task-agnostic accuracy (%) after the final task (Table 1 caption, p. 8).

**Not reported** (our reading): the number of seeds or any variance; how $\alpha$ was selected beyond the sensitivity study on CIFAR100 and CUB200 (p. 9), with no separate validation split mentioned; whether the baselines use full fine-tuning or AEFT.

## Results

**Class-incremental learning** (Table 1, p. 8). Task-agnostic accuracy (%) after the final task; `/N` is the number of tasks; underlined in the paper = prior best (marked here with *); Δ = QOMM minus the prior best:

| Method | CIFAR100 /5 | /10 | /20 | /50 | ImageNet-R /5 | /10 | /20 | /50 | CUB200 /5 | /10 | /20 | Cars /5 | /10 | /20 | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Zero-shot | 66.91 | | | | 77.73 | | | | 56.08 | | | 64.71 | | | 67.21 |
| Joint | 90.94 | | | | 87.55 | | | | 81.57 | | | 88.21 | | | 87.38 |
| LwF | 83.25 | 74.35 | 72.05 | 68.84 | 81.15 | 82.97 | 81.82 | 80.32 | 65.12* | 60.67 | 58.90* | 71.72 | 69.84* | 62.98 | 72.36 |
| EWC | 84.41* | 76.24 | 75.39 | 72.97 | 82.15 | 82.42 | 81.48 | 81.47 | 59.10 | 54.49 | 53.31 | 69.46 | 60.78 | 57.42 | 70.79 |
| RandMix | 81.55 | 77.04 | 75.36 | 72.91 | 83.10 | 81.88 | 80.18 | 78.50 | 59.86 | 58.53 | 58.08 | 67.32 | 65.62 | 64.95 | 71.78 |
| MaxAbs | 81.95 | 76.75 | 74.39 | 73.04 | 83.03 | 82.33 | 80.92 | 79.33 | 60.15 | 58.01 | 56.59 | 67.36 | 63.55 | 58.95 | 71.17 |
| ModelSoup | 81.41 | 77.04 | 75.29 | 72.92 | 83.08 | 81.87 | 80.27 | 78.53 | 59.77 | 58.44 | 58.01 | 67.37 | 65.59 | 64.88 | 71.85 |
| TIES | 81.72 | 77.23 | 74.66 | 73.76 | 83.08 | 82.27 | 80.83 | 79.57 | 60.94 | 58.22 | 56.97 | 70.45 | 64.90 | 61.17 | 71.84 |
| MAGMAX | 84.16 | 80.41* | 78.49* | 76.75* | 83.60* | 83.33* | 82.27* | 81.75* | 63.89 | 60.74* | 58.90* | 73.61* | 69.28 | 65.84* | 74.50* |
| **QOMM (ours)** | **85.20** | **83.09** | **80.69** | **77.84** | **85.77** | **84.52** | **83.05** | **81.78** | **69.02** | **64.84** | **62.10** | **80.54** | **74.90** | **71.50** | **77.49** |
| Performance Δ | +0.79 | +2.68 | +2.20 | +1.09 | +2.17 | +1.19 | +0.78 | +0.03 | +3.90 | +4.10 | +3.20 | +6.93 | +5.06 | +5.66 | +2.99 |

- Zero-shot and Joint are one number per dataset, printed across all its splits (Table 1, p. 8).
- No Task Arithmetic row appears in Table 1, although TA is listed among the baselines (p. 7).
- The authors' summary: QOMM is best in every setting; +2.99 on average over MagMax; up to +2.68 on CIFAR100; +3–4% on CUB200; +5–6% on Cars (p. 8).
- **Our reading:** the Avg column matches the mean of the 14 settings (checked for QOMM and Zero-shot). Joint training stays **9.89 points** above QOMM on average (87.38 vs 77.49), and the gap grows with the number of tasks on CIFAR100 (90.94 vs 85.20 at /5, vs 77.84 at /50).

**Domain-incremental learning** (Table 2, p. 8). Accuracy (%) on DomainNet:

| LwF | EWC | RandMix | MaxAbs | Avg | TIES | MAGMAX | Ours |
|---|---|---|---|---|---|---|---|
| 69.67 | **70.74** | 64.31 | 67.51 | 64.98 | 66.42 | 69.00 | 69.32 |

- EWC is best; the text calls 64.98% (column "Avg") "the simple averaging baseline" (p. 8).
- **Our reading:** LwF (69.67) is also above QOMM (69.32), which the text doesn't mention; no Joint or Zero-shot value is given for DomainNet.

**Ablation: QOP and AEFT** (Table 3, p. 9). CIL accuracy (%):

| Method | CIFAR100 /5 | /10 | /20 | /50 | CUB200 /5 | /10 | /20 |
|---|---|---|---|---|---|---|---|
| MagMax | 84.16 | 80.41 | 78.49 | 76.75 | 63.89 | 60.74 | 58.90 |
| QOP | 82.82 | 78.05 | 69.61 | 52.60 | 64.74 | 57.44 | 45.79 |
| QOP + AEFT | **85.20** | **83.09** | **80.69** | **77.84** | **69.02** | **64.84** | **62.10** |

- QOP alone is comparable to MagMax at 5 tasks but drops severely as tasks increase (52.60 on CIFAR100/50); the authors attribute this to the projection being approximate, "less effective as task interference grows" (p. 9).
- Adding AEFT removes most of the drop; the authors attribute this to AEFT enforcing "stronger orthogonality among task vectors" (p. 9).

**Orthogonality of task vectors: full vs. attention-only fine-tuning** (Section 4.3, p. 7; Figure 3, p. 7):

- Setup: CIFAR-100, ImageNet-R, CUB-200 and Cars, each split into five sequential tasks; five task vectors per fine-tuning paradigm; cosine-similarity matrices $M^{\text{FMFT}}, M^{\text{AEFT}} \in \mathbb{R}^{5 \times 5}$ with $M_{ij} = \cos(\Delta W_i, \Delta W_j)$, and $M^{\text{Diff}} = M^{\text{FMFT}} - M^{\text{AEFT}}$ (p. 7).
- Positive values mean full fine-tuning gives more similar (less orthogonal) task vectors (Figure 3 caption, p. 7).
- Printed off-diagonal values of $M^{\text{Diff}}$ are all non-negative; the largest per dataset: CIFAR100 0.022, ImageNetR 0.007, CUB200 0.009, Cars 0.011; the smallest: 0.009, 0.001, 0.003, 0.001 respectively (Figure 3, p. 7).
- The pattern holds at 10, 20 and 50 tasks on CIFAR100 (Appendix A.2, Figures 5–7, pp. 12–13): off-diagonal entries are "predominantly red" (p. 12).
- **Our reading:** only differences are shown, not the absolute cosine similarities, so how orthogonal either kind of task vector is remains unknown; the differences are small (at most 0.022 at five tasks). It is also not stated whether the full-fine-tuning cosine is computed over all parameters or only the attention matrices.

**Sensitivity to $\alpha$** (Figure 4, p. 9): on CIFAR100 and CUB200, all splits, performance "remains robust within $\alpha \in [0.5, 0.6]$", with $\alpha = 0.55$ near-optimal "in most cases"; $\alpha$ is then fixed at 0.55 everywhere (p. 9). **Our reading** of the plot (accuracy relative to the optimum, %): it falls steeply for small $\alpha$ (down to about −6 around $\alpha \approx 0.2$–0.4, depending on the split) and more gently for large $\alpha$ (about −1 to −2 near $\alpha \approx 0.8$).

## Assumptions and limitations

- **Same pre-trained model and architecture** for all task vectors; task vectors are relative to $\Theta_0$ (p. 3, p. 5).
- **Sequential fine-tuning chain:** each task starts from the previous task's fine-tuned model ($\Theta_i = \mathrm{AEFT}(\Theta_{i-1})$, p. 5), so fine-tuning itself already carries earlier tasks forward.
- **Transformer-specific:** AEFT and Algorithm 1 act on attention matrices only (p. 5, p. 6).
- **Frozen classification heads** built from CLIP's text encoder (pp. 7–8); only vision classification is tested.
- **One hyperparameter fixed for all experiments,** $\alpha = 0.55$, chosen from a sensitivity study on two of the benchmarks (p. 9).
- **The orthogonality mechanism is a hypothesis** supported by the similarity-difference matrices ("We hypothesize", p. 4, p. 6; "supporting hypothesis $H_1$", p. 12); $H_1$ is not defined elsewhere in the paper.
- **Not the best everywhere:** on DomainNet EWC is best (p. 8).
- **Our reading:**
    - Not peer-reviewed yet; no code, seeds or variances, so the margins (some as small as +0.03, Table 1, p. 8) can't be judged against noise.
    - Task Arithmetic is listed as a baseline but no TA result is reported, so there's no direct QOMM-vs-TA number.
    - The equations as printed have inconsistencies (Eq. 5 and Eq. 6 against Algorithm 1, and index slips in Algorithm 1's lines 12 and 14, p. 5).
    - The prose describes $\mathcal{O}^\perp$ as mapping onto "the orthogonal complement of the principal subspace spanned by the previously merged task vectors" (p. 5), a larger subspace than the rank-one directions Eq. 3 actually removes.
    - Table 2 has no ModelSoup column, though ModelSoup is a listed baseline (p. 7); its "Avg" column (64.98) is what the text calls "the simple averaging baseline" (p. 8).
    - QOP alone is worse than MagMax at many tasks (Table 3, p. 9): the gain needs AEFT, i.e. a choice of which parameters to train, not only a merging rule.
    - No ablation of the $\sqrt{i}$ normalization against the naive rule (Eq. 5), and none of fine-tuning from $\Theta_{i-1}$ versus from $\Theta_0$.

## Relevance to this thesis

**Our reading:**

- **A sequential-merging baseline with a fixed recipe:** QOMM is a concrete continual merging rule (project the new task vector away from the merged one's dominant directions, then rescale by $\sqrt{i}$) that we could run on a sequence of time-series tasks, next to plain task arithmetic and MagMax.
- **Joint training vs. merging:** Table 1 (p. 8) gives a reference gap on images: joint 87.38 vs the best merging method 77.49 on average, widening with more tasks on CIFAR100. Whether a similar gap holds for anomaly detection and forecasting is the question we study.
- **The $1/\sqrt{i}$ scaling** (our unrolling above) is a data-free choice of the task-arithmetic coefficient that depends only on the number of tasks; it is cheap to test against a $\lambda$ tuned on validation data.
- **Attention-only fine-tuning** is directly applicable to Transformer forecasters and detectors; for convolutional models (no attention matrices) AEFT has no counterpart, and we would need to choose another parameter subset.
- **Task similarity may break the premise:** our tasks may be successive periods of the same signal, where task vectors share their dominant directions; projecting those directions out could discard most of what a new task adds. Measuring cosine similarity between task vectors (absolute values, not only differences) would tell us whether QOP's assumptions hold.
- **Design choices worth testing ourselves,** because the paper doesn't ablate them: fine-tuning each task from the previous fine-tuned model vs. from the pre-trained one vs. from the merged one; the naive vs. normalized update; the choice of $\alpha$ on a validation split.

## Quotes worth keeping

> "The projection is *quasi*-orthogonal because it excludes only the dominant shared subspace." (p. 2)

> "Intuitively, the parallel component reflects weight changes aligned with prior task directions and is thus more likely to cause interference, while the orthogonal component points in a novel direction and is less likely to conflict with past knowledge." (p. 4)

> "We hypothesize that the gains reported in Jin et al. (2025) stem from an implicit increase in task vector orthogonality, a hypothesis strongly supported by our empirical findings." (p. 4)

> "Although effective in promoting orthogonality, Eq. (5) suffers from an important limitation: as the number of tasks increases, the Frobenius norm of the merged update $\Delta\hat{W}_i$ grows monotonically." (p. 6)

> "When using QOP alone, the performance is comparable to MagMax when the number of tasks is small, for example at 5 tasks on both datasets. However, as the number of tasks increases, QOP suffers from a severe drop in accuracy, whereas MagMax degrades more gradually." (p. 9)

> "Notably, the memory footprint stays invariant to the total count of downstream tasks being processed." (p. 8)
