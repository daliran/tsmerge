# tang2025merging — Merging on the Fly Without Retraining: A Sequential Approach to Scalable Continual Model Merging

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 140 claims, every Table 1 cell and bold mark correct: 3 misstatements, 2 unsupported details and 4 omissions, all fixed)
- **Reference:** Tang, Yang, Shen, Luo, Hu, Zhang, Du, Tao; NeurIPS 2025; arXiv 2501.09522 (arXiv title: "Merging Models on the Fly Without Retraining") ([references.bib](references.bib))
- **Version read:** NeurIPS 2025 camera-ready, 38 pages: main text pp. 1–10, references pp. 10–16, NeurIPS checklist pp. 17–23, appendix pp. 24–38 (the printed page numbers match the PDF pages)
- **Read:** main text in full (pp. 1–10, up to the acknowledgments); appendix A (proofs, pp. 24–26), B (complexity, p. 27), C (fine-tuned models, pp. 27–28), D.1–D.4 (pp. 32–38) and E (p. 38), including Figure 9 (p. 29) and Figure 10 (p. 30). Checklist: items 1–2 (p. 17), 5–7 (p. 19), 13–16 (pp. 22–23). Not read: Figure 11 (p. 31, cosine similarities for ViT-L/14), checklist pp. 18, 20–21, references (pp. 10–16) beyond looking up single entries. Tables 3–5 (per-task accuracies, pp. 28, 35, 36) were looked at but not copied
- **Code:** <https://github.com/tanganke/opcm/> (p. 1)

## In one paragraph

The paper studies **continual model merging**: fine-tuned models of the same pre-trained network arrive one at a time, and each new one is merged into the current merged model without access to the earlier ones or to any training data (pp. 1–3). It proposes **OPCM** (Orthogonal Projection-based Continual Merging), a training-free method that (1) projects each new task vector, layer by layer, onto the subspace orthogonal to the dominant singular directions of the current merged task vector, and (2) rescales the sum with an adaptive factor $\lambda^{(t)}$ that keeps the distance from the pre-trained model roughly constant (pp. 4–6). Memory stays $O(|\theta|)$ whatever the number of tasks (p. 4). On CLIP-ViT-B/32, B/16 and L/14 with 8, 14 and 20 image classification tasks, OPCM beats the strongest baseline by about 4.6–8 points of average accuracy in each setting (Table 1, p. 7), which the authors round to "improvements of 5-8% over continual Task Arithmetic and continual Ties-Merging" (p. 8), with small standard deviations over 10 random task orders (Table 1, p. 7). Continual fine-tuning (sequential training on the data) is still better in 4 of 9 settings (Table 6, p. 36).

## Problem

Conventional model merging assumes all expert models are available at once and merges them in one step (Definition 3.1, p. 3). The paper argues that this does not fit settings where models "become available sequentially" (p. 1), and that it costs memory linear in the number of models (p. 2, p. 4).

**Setting** (p. 3):

- A pre-trained model $f_{\theta^{(0)}}: \mathcal{X} \to \mathcal{Y}$ and $T$ task-specific models $f_{\theta^{(1)}}, \dots, f_{\theta^{(T)}}$, each fine-tuned from $\theta^{(0)}$ on its own data set $D_i$.
- Each model may have a task-specific head $h_{\phi_i}: \mathcal{Y} \to \mathcal{Z}_i$; the goal is one merged model that does well on all $T$ tasks "while preserving task-specific heads" (p. 3).
- Models arrive one at a time; at each step only the current merged model, the new model and optionally the pre-trained model are stored (p. 4).

**Definitions** (p. 3):

- Conventional merging (Eq. 1):

  $$\theta_{\text{merged}} = \text{Merge}(\theta^{(0)}; \theta^{(1)}, \theta^{(2)}, \dots, \theta^{(T)})$$

- Continual merging (Eq. 2):

  $$\theta^{(t)}_{\text{merged}} = \text{ContinualMerge}(\theta^{(t-1)}_{\text{merged}}; \theta^{(0)}, \theta^{(t)}), \quad t \geq 2$$

  where "typically" $\theta^{(1)}_{\text{merged}} = \theta^{(1)}$, and $\theta^{(t)}_{\text{merged}}$ "aims to minimize the expected risk" $\theta^{(t)}_{\text{merged}} = \arg\min_\theta \mathbb{E}_{(x,y) \sim \mathcal{D}_1 \cup \dots \cup \mathcal{D}_t} \mathcal{L}_t(f_\theta(x), y)$ (p. 3).

**Challenges named by the paper** (p. 4):

- **Non-commutativity:** standard merging is commutative (Eq. 3), $\text{Merge}(\theta^{(0)}; \theta^{(i)}, \theta^{(j)}) = \text{Merge}(\theta^{(0)}; \theta^{(j)}, \theta^{(i)})$; continual merging (CM) may not be (Eq. 4):

  $$\text{CM}\left(\text{CM}\left(\theta^{(i-1)}_{\text{merged}}; \theta^{(0)}, \theta^{(i)}\right); \theta^{(0)}, \theta^{(i+1)}\right) \overset{?}{=} \text{CM}\left(\text{CM}\left(\theta^{(i-1)}_{\text{merged}}; \theta^{(0)}, \theta^{(i+1)}\right); \theta^{(0)}, \theta^{(i)}\right), \ \forall i$$

  so the final model depends on the order in which models are merged (p. 4).
- **Fading of early tasks:** earlier parameter information may be gradually diminished along the sequence (p. 4, quoted below).
- **Existing related practice:** LAWA, EMA and SWA average along a training trajectory, but were not designed for large distribution shifts between consecutive models (p. 4).

**Continual task arithmetic baseline** (Baseline 3.3, Eq. 5, p. 4), with a scalar hyperparameter $\lambda$:

$$\theta^{(t)}_{\text{merged}} = \theta^{(t-1)}_{\text{merged}} + \lambda(\theta^{(t)} - \theta^{(0)})$$

## Method

**Three design goals** (pp. 4–5): orthogonality preservation (new updates approximately orthogonal to the merged ones), magnitude control (parameter changes stay stable, no drift from the pre-trained loss basin), information retention (keep all earlier tasks).

**Which parameters are projected** (p. 5): weight matrices of linear layers go through the orthogonal projection; "other parameters, such as biases and those in non-linear layers, are averaged directly" (p. 5).

**Update rule for a linear-layer weight** $W \in \mathbb{R}^{m \times n}$ (Eq. 6, p. 5):

$$W^{(t)}_{\text{merged}} = W^{(0)} + \frac{\lambda^{(t-1)} \Delta W^{(t-1)}_{\text{merged}} + \mathcal{P}^{(t-1)}_\alpha\left(\Delta W^{(t)}\right)}{\lambda^{(t)}}$$

with $\Delta W^{(t-1)}_{\text{merged}} = W^{(t-1)}_{\text{merged}} - W^{(0)}$ and $\Delta W^{(t)} = W^{(t)} - W^{(0)}$ (the task vectors) (p. 5).

**General term** (Eq. 7, p. 5; proved by induction as Theorem A.1, Eqs. 12–18, pp. 24–25, with $\mathcal{P}^{(0)}_\alpha$ the identity and $\lambda^{(1)} = 1$):

$$W^{(t)}_{\text{merged}} = W^{(0)} + \frac{1}{\lambda^{(t)}} \sum_{i=1}^{t} \mathcal{P}^{(i-1)}_\alpha\left(\Delta W^{(i)}\right)$$

The paper reads this as "a more generalized form of Task Arithmetic" (p. 5).

**Other parameters** (p. 5): $\mathcal{P}$ is the identity, so

$$p^{(t)}_{\text{merged}} = p^{(0)} + \left(\lambda^{(t-1)} \Delta p^{(t-1)}_{\text{merged}} + \Delta p^{(t)}\right)/\lambda^{(t)}, \qquad p^{(t)}_{\text{merged}} = p^{(0)} + \frac{1}{\lambda^{(t)}} \sum_{i=1}^{t} \Delta p^{(i)}$$

**Projection mapping** (pp. 5–6). Full SVD of the previous merged task vector, $\Delta W^{(t-1)}_{\text{merged}} = U^{(t-1)} \Sigma^{(t-1)} V^{(t-1)}$ (as printed on p. 5; written $U^{(t-1)}\Sigma^{(t-1)}V^{(t-1)T}$ in the proof, p. 25), with $U^{(t-1)} \in \mathbb{R}^{m \times m}$, $V^{(t-1)} \in \mathbb{R}^{n \times n}$ orthonormal and $\Sigma^{(t-1)} \in \mathbb{R}^{m \times n}$ rectangular diagonal. Then (p. 6):

$$\mathcal{P}^{(t-1)}_\alpha\left(\Delta W^{(t)}\right) = \sum_{i,j=r_\alpha, i \neq j}^{m,n} \left\langle \Delta W^{(t)}, u_i v_j^T \right\rangle_F u_i v_j^T$$

- $u_i$, $v_j$: the $i$-th column of $U^{(t-1)}$ and the $j$-th column of $V^{(t-1)}$ (p. 6).
- $\alpha$: the projection threshold hyperparameter, balancing retention of existing knowledge against new knowledge (p. 6).
- $r_\alpha$: the minimal rank of $\Delta W^{(t-1)}_{\text{merged}}$ such that $\sum_{i=1}^{r_\alpha} \sigma_i \geq \alpha \sum_{i=1}^{\min(m,n)} \sigma_i$ (p. 6).
- The stated aim: orthogonality between the projected new task vector and $\Delta W^{(t-1)}_{\text{merged}}$, "while maintaining proximity" between $\mathcal{P}^{(t-1)}_\alpha(\Delta W^{(t)})$ and $\Delta W^{(t)}$ (p. 5).

**Adaptive scaling factor** (p. 6), meant to keep $\|W^{(t)}_{\text{merged}} - W^{(0)}\|_2$ stable over time:

$$\lambda^{(1)} = 1, \qquad \lambda^{(t)} = \left\| \lambda^{(t-1)} \Delta\theta^{(t-1)}_{\text{merged}} + \mathcal{P}^{(t-1)}_\alpha\left(\Delta\theta^{(t)}\right) \right\|_2 \Big/ \text{Avg}\left(\|\Delta\theta^{(t)}\|_2\right)$$

with $\Delta\theta^{(t-1)}_{\text{merged}} = \theta^{(t-1)}_{\text{merged}} - \theta^{(0)}$ and $\Delta\theta^{(t)} = \theta^{(t)} - \theta^{(0)}$ as flattened vectors over all parameters, and $\text{Avg}(\|\Delta\theta^{(t)}\|_2) = \frac{1}{t} \sum_{i=1}^{t} \|\Delta\theta^{(i)}\|_2$ (p. 6). The notation applies $\mathcal{P}$ to the whole task vector "for notational simplicity" (p. 6).

- **Simpler alternative:** $\lambda^{(t)} = \sqrt{t}$, motivated by task vectors being approximately orthogonal, $\langle \Delta\theta^{(i)}, \Delta\theta^{(j)} \rangle \approx \delta_{ij}$ (p. 6).
- **Empirically,** the adaptive $\lambda^{(t)}$ "closely follow[s]" a $\sqrt{t}$ curve for all three models (Figure 7b, p. 9).

**Algorithm 1, OPCM** (p. 5), step by step:

1. Initialize $\theta^{(1)}_{\text{merged}} = \theta^{(1)}$, average task-vector norm $n = \|\Delta\theta^{(1)}\|_2$, $\lambda^{(1)} = 1$.
2. For $t = 2, \dots, T$:
   - for each linear-layer weight $W$: $\Delta W^{(t-1)}_{\text{merged}} \leftarrow W^{(t-1)}_{\text{merged}} - W^{(0)}$; $\Delta W^{(t)} \leftarrow W^{(t)} - W^{(0)}$; $\Delta W^{(t)}_{\text{proj}} \leftarrow \mathcal{P}^{(t-1)}_\alpha(\Delta W^{(t)}; \Delta W^{(t-1)}_{\text{merged}})$;
   - for every other parameter $p$: $\Delta p^{(t)} \leftarrow p^{(t)} - p^{(0)}$;
   - $\Delta\theta^{(t-1)}_{\text{merged}} \leftarrow \theta^{(t-1)}_{\text{merged}} - \theta^{(0)}$; concatenate $\Delta W^{(t)}_{\text{proj}}$ and $\Delta p^{(t)}$ into $\Delta\theta^{(t)}_{\text{proj}}$;
   - $n \leftarrow \frac{t-1}{t} n + \frac{1}{t} \|\Delta\theta^{(t)}\|_2$;
   - $\lambda^{(t)} \leftarrow \left\| \lambda^{(t-1)} \Delta\theta^{(t-1)}_{\text{merged}} + \Delta\theta^{(t)}_{\text{proj}} \right\|_2 / n$;
   - $\theta^{(t)}_{\text{merged}} \leftarrow \theta^{(0)} + \left(\lambda^{(t-1)} \Delta\theta^{(t-1)}_{\text{merged}} + \Delta\theta^{(t)}_{\text{proj}}\right) / \lambda^{(t)}$.
3. Return $\theta^{(T)}_{\text{merged}}$.

**Theory** (Section 5, pp. 6–7; proofs pp. 24–26):

- **Theorem 5.1, orthogonality** (Eq. 8, p. 6): $\left\langle \mathcal{P}^{(t-1)}_\alpha(\Delta W^{(t)}), \Delta W^{(t-1)}_{\text{merged}} \right\rangle_F = 0$. The proof (Eqs. 19–21, p. 25) uses $\langle u_i v_j^T, U \Sigma V^T \rangle_F = 0$ for $i \neq j$.
- **Merging gap** (Eq. 9, p. 6), "similar to [89]", as printed:

  $$G_i = \mathcal{L}_i\left(\theta^{(0)} + \sum_{j=1}^{t} \eta_j \mathcal{P}^{(j-1)}_\alpha\left(\Delta\theta^{(i)}\right)\right) - \mathcal{L}_i\left(\theta^{(0)} + \eta_i \mathcal{P}^{(i-1)}_\alpha\left(\Delta\theta^{(i)}\right)\right)$$

  A first-order Taylor expansion at $\theta^{(0)}$ gives $G_i \approx \nabla_{\theta^{(0)}} \mathcal{L}_i^\top \left(\sum_{j=1, j \neq i}^{t} \eta_j \mathcal{P}^{(j-1)}_\alpha(\Delta\theta^{(i)})\right)$; with $\eta_i = 1/\lambda^{(t)}$, $G_t \approx \nabla_{\theta^{(0)}} \mathcal{L}_t^\top \left(\frac{\lambda^{(t-1)}}{\lambda^{(t)}} \Delta\theta^{(t-1)}_{\text{merged}}\right)$ (p. 6). Treating the task vector as accumulated gradients, $G_t \approx C \, \Delta\theta^{(t)\top} \Delta\theta^{(t-1)}_{\text{merged}}$ with $C$ a constant, so orthogonality "serves to minimize the gap $G_t$" (p. 7).
- **Theorem 5.2, bounded distance** (Eq. 10, p. 7), with $\lambda^{(t)} = \sqrt{t}$:

  $$\left\| W^{(t)}_{\text{merged}} - W^{(0)} \right\|_F^2 \leq \max_{i \in [1,t]} \left\| \Delta W^{(i)} \right\|_F^2$$

  Proof by induction (Eqs. 22–25, pp. 25–26), using orthogonality to split the norm into $\frac{t-1}{t}\|\Delta W^{(t-1)}_{\text{merged}}\|_F^2 + \frac{1}{t}\|\mathcal{P}(\Delta W^{(t)})\|_F^2$ and $\|\mathcal{P}(\Delta W^{(t)})\|_F^2 \leq \|\Delta W^{(t)}\|_F^2$.
- **Corollary 5.3, preservation of task information** (Eq. 11, p. 7): $W^{(t)}_{\text{merged}} - W^{(0)} = \frac{1}{\lambda^{(t)}} \sum_{i=1}^{t} \mathcal{P}^{(i-1)}_\alpha(\Delta W^{(i)})$, i.e. a weighted combination of all earlier (projected) task vectors.
- **Corollary A.2, correlated task vectors** (p. 26): writing $\Delta W^{(t)} = \rho \Delta W^{(t-1)}_{\text{merged}} + \eta$ with $\eta$ orthogonal to $\Delta W^{(t-1)}_{\text{merged}}$ (Eq. 26), the projection gives $\mathcal{P}^{(t-1)}_\alpha(\Delta W^{(t)}) = \eta$ (Eq. 29), so a highly correlated new model contributes only its novel part (Eq. 30, p. 26).

**Computational cost** (Appendix B, p. 27): dominated by the full SVD, $O(\min(m^2 n, n^2 m))$ per weight matrix; "approximately $O(TL\min(mn, mn))$" for $T$ tasks and $L$ linear layers (as printed, p. 27).

## Experimental setup

**Models and tasks** (p. 7, pp. 27–28):

- CLIP-ViT-B/32, ViT-B/16, ViT-L/14; only the vision encoder is fine-tuned (p. 27).
- Classification heads built from the frozen pre-trained text encoder (zero-shot heads) and kept fixed during fine-tuning, so pre-trained and fine-tuned models share the same head per task (pp. 27–28, p. 32).
- 20 image classification tasks, setup following [83] (p. 27):
  - **8 tasks:** SUN397, Cars, RESISC45, EuroSAT, SVHN, GTSRB, MNIST, DTD (p. 28).
  - **14 tasks:** the 8 plus Flowers102, PCAM, FER2013, OxfordIIITPet, STL10, CIFAR100 (p. 28).
  - **20 tasks:** the 14 plus CIFAR10, Food101, FashionMNIST, EMNIST, KMNIST, RenderedSST2 (p. 28).

**Fine-tuning** (p. 27): cross-entropy loss, Adam, cosine annealing with maximum learning rate 1e-5, batch size 128, 4000 steps; models fine-tuned and evaluated with FusionBench (p. 27, footnote 2).

**OPCM** (p. 8): $\alpha = 0.5$ in every experiment; each experiment repeated 10 times with shuffled task order, mean and standard deviation reported (p. 8, p. 32).

**Baselines** (p. 8; Appendix D.3.1, pp. 32–33):

- **Continual fine-tuning** (Eq. 33, p. 32): $\theta^{(t)} = \text{Fine-tune}(\theta^{(t-1)}, \mathcal{D}_t)$, same schedule (lr 1e-5, batch 128, 4000 steps per task); a **single run** with random seed 42 and a shuffled task order (p. 32; Table 4 caption, p. 35). Each task takes 20–30 minutes of fine-tuning, so a 20-task run takes 8–10 hours (p. 36).
- **SWA** (Eqs. 34–35, p. 32): $\theta^{(1)}_{\text{SWA}} = \theta^{(1)}$, $\theta^{(t)}_{\text{SWA}} = \frac{\theta^{(t-1)}_{\text{SWA}}(t-1) + \theta^{(t)}}{t}$, i.e. $\theta^{(t)}_{\text{SWA}} = \frac{1}{t}\sum_{i=1}^{t} \theta^{(i)}$.
- **Continual task arithmetic** (Eq. 37, p. 33): $\theta^{(0)}_{\text{merged}} = \theta^{(0)}$, $\theta^{(t)}_{\text{merged}} = \theta^{(t-1)}_{\text{merged}} + \lambda(\theta^{(t)} - \theta^{(0)})$. $\lambda$ chosen as "the value of $\lambda$ that achieves the highest average accuracy" in $\{0.1, 0.2, \dots, 1.0\}$: **0.3 for 8 tasks, 0.1 for 14 and 20 tasks** (p. 33, p. 38).
- **Continual Ties-Merging** (Eq. 40, p. 33): $\theta^{(1)}_{\text{merged}} = \theta^{(0)} + \lambda(\theta^{(1)} - \theta^{(0)})$, $\theta^{(t)}_{\text{merged}} = \theta^{(0)} + \lambda\left(\tau^{(t-1)}_{\text{Ties-merged}} + \tau^{(t)}_{\text{Ties}}\right)$, (the where-clause prints $\theta^{(t)}_{\text{Ties}}$ on its left-hand side, p. 33), where TiesMerging is applied to the pair $\{\theta^{(t-1)}_{\text{merged}} - \theta^{(0)}, \theta^{(t)} - \theta^{(0)}\}$; same $\lambda$ as task arithmetic (p. 33).
- **Continual AdaMerging and TSVM** (Appendix E, p. 38): $\theta^{(0)}_{\text{merged}} = \theta^{(0)}$, $\theta^{(t+1)}_{\text{merged}} = \text{AdaMerging}(\theta_0; \theta^{(t)}_{\text{merged}}, \theta^{(t+1)})$ (and likewise for TSVM); a single run, task order SUN397, Cars, RESISC45, EuroSAT, SVHN, GTSRB, MNIST, DTD (p. 38).

**Metrics** (Appendix D.2, p. 32), as printed:

$$\text{ACC}_{\text{avg}} = \frac{1}{T} \sum_{t=1}^{T} \text{ACC}_i\left(W^{(T)}_{\text{merged}}\right)$$

As printed (p. 32), the sum runs over $t$ but indexes $\text{ACC}_i$, and uses $W$ where Eq. 32 uses $\theta$; **our reading:** $\frac{1}{T}\sum_i \text{ACC}_i(\theta^{(T)}_{\text{merged}})$.

$$\text{BWT} = \frac{\sum_{i=1}^{T-1} \text{ACC}_i\left(\theta^{(T)}_{\text{merged}}\right) - \text{ACC}_i\left(\theta^{(i)}_{\text{merged}}\right)}{T-1}$$

where $\text{ACC}_i(\cdot)$ is accuracy on the $i$-th task's test data (p. 32). The **accuracy matrix** (p. 34): row $i$ is the model after merging the $i$-th model, column $j$ is $\text{ACC}_j(\theta^{(i)}_{\text{merged}})$.

**Hardware** (p. 32): one machine with 8 NVIDIA RTX 4090 (24 GB each); PyTorch, Python 3.12.

**Hyperparameter grids** (p. 37): task arithmetic $\lambda \in \{0.0 \text{ (zero-shot)}, 0.1, \dots, 1.0\}$; OPCM $\alpha \in \{0.1, 0.2, \dots, 1.0\}$.

## Results

**Main comparison** (Table 1, p. 7). Average accuracy (ACC, %) and backward transfer (BWT, %) of the final merged model; "C." means continual; ± over 10 task orders:

| Method | B/32 8 | B/32 14 | B/32 20 | B/16 8 | B/16 14 | B/16 20 | L/14 8 | L/14 14 | L/14 20 |
|---|---|---|---|---|---|---|---|---|---|
| Pre-Trained | 48.1 | 56.9 | 55.6 | 55.4 | 62.0 | 59.8 | 64.9 | 69.1 | 65.6 |
| Fine-Tuned | 90.4 | 89.3 | 89.8 | 92.4 | 91.3 | 91.6 | 94.3 | 93.4 | 93.5 |
| C. Fine-Tuned | 79.8 | 67.4 | 62.6 | 82.9 | 72.2 | 68.2 | 90.0 | 70.9 | 77.7 |
| ACC: Average (SWA) | 66.3±0.0 | 65.4±0.0 | 61.1±0.0 | 72.3±0.0 | 69.7±0.0 | 64.8±0.0 | 80.0±0.0 | 77.5±0.0 | 71.1±0.0 |
| ACC: C. Task Arithmetic | 67.5±0.0 | 66.5±0.0 | 60.6±0.0 | 77.1±0.0 | 70.9±0.0 | 64.2±0.0 | 82.1±0.0 | 77.9±0.0 | 70.3±0.0 |
| ACC: C. Ties-Merging | 49.0±10.2 | 66.2±0.6 | 59.9±0.7 | 66.8±3.7 | 70.5±0.8 | 63.0±1.6 | 64.3±7.0 | 78.0±0.6 | 68.3±0.9 |
| ACC: OPCM | **75.5**±0.5 | **71.9**±0.3 | **65.7**±0.2 | **81.8**±0.3 | **77.1**±0.5 | **70.3**±0.2 | **87.0**±0.4 | **83.5**±0.2 | **76.0**±0.2 |
| BWT: Average (SWA) | -11.5±2.2 | -8.0±1.3 | -7.1±2.1 | -9.7±1.5 | -7.1±1.4 | -7.3±1.7 | -7.3±1.4 | -5.8±1.0 | -6.4±1.5 |
| BWT: C. Task Arithmetic | -9.6±1.5 | -1.3±0.3 | -3.4±0.4 | **-4.2**±1.0 | -1.3±0.4 | -3.6±0.4 | -7.1±0.8 | -1.8±0.3 | -3.3±0.3 |
| BWT: C. Ties-Merging | -15.3±8.0 | **1.9**±0.6 | **-1.5**±0.7 | -5.5±0.4 | **1.4**±0.7 | **-1.5**±1.2 | -13.0±5.7 | **1.1**±0.4 | **-2.9**±1.0 |
| BWT: OPCM | **-6.3**±1.1 | -6.0±1.0 | -7.8±1.5 | -4.8±0.7 | -5.1±1.4 | -6.3±2.2 | **-2.6**±1.0 | -4.3±0.7 | -6.5±1.8 |

Bold as printed. "C. Fine-Tuned" is one run of continual fine-tuning (p. 32, p. 35). **Our reading:** "Fine-Tuned" is the average of the individual fine-tuned models: Table 3 (p. 28) gives, for ViT-B/32 on 8 tasks, a fine-tuned average of 723.1/8 = 90.4 and a pre-trained average of 48.1, both matching Table 1. C. Fine-Tuned on ViT-L/14 is non-monotonic (70.9 on 14 tasks, 77.7 on 20), from a single run; the paper doesn't comment.

**What the authors draw from it** (p. 8):

- The authors report "improvements of 5-8% over continual Task Arithmetic and continual Ties-Merging" (p. 8); against the strongest baseline in each setting, Table 1 gives about 4.6–8 points (e.g. ViT-B/32, 20 tasks: 65.7 − 61.1 = 4.6), and against continual Ties-Merging on 8 tasks much more (ViT-B/32: 75.5 − 49.0 = 26.5).
- ViT-L/14 forgets least, with a BWT of -2.6% on 8 tasks.
- Degradation at 20 tasks "compared to individuals": -17.5% for ViT-L/14, 24.1% for ViT-B/32 and 21.3% for ViT-B/16 (p. 8).
- Robustness to task order: narrow confidence bands (Figure 5) and small standard deviations (Table 1) (p. 8); Continual Ties-Merging has much larger standard deviations, i.e. it is more sensitive to task order (p. 35).
- Accuracy falls as tasks are added (Figure 5, p. 8): from around 90% for all models, ViT-L/14 keeps approximately 75–80% by task 20, the smaller models drop to around 65–70% (p. 8, as stated in the text).
- In the per-task tables, EMNIST and KMNIST stay hard for all continual methods (p. 35); in the SWA accuracy matrices the decline is "particularly significant" for KMNIST and EMNIST, attributed to their divergence from the pre-trained model and the other tasks (p. 34).

**OPCM vs continual fine-tuning** (Table 6, p. 36). Average accuracy (%); continual fine-tuning is a single run, OPCM is 10 runs:

| Setup | Continual fine-tuning | OPCM (10 runs) |
|---|---|---|
| ViT-B/32, 8 tasks | 79.8 | 75.5±0.5, Min: 74.8, Max: 76.5 |
| ViT-B/16, 8 tasks | 82.9 | 81.8±0.3, Min: 81.3, Max: 82.3 |
| ViT-L/14, 8 tasks | 90.0 | 87.0±0.4, Min: 86.6, Max: 87.7 |
| ViT-B/32, 14 tasks | 67.4 | 71.9±0.3, Min: **71.3**, Max: 72.5 |
| ViT-B/16, 14 tasks | 72.2 | 77.1±0.5, Min: **76.2**, Max: 77.8 |
| ViT-L/14, 14 tasks | 70.9 | 83.5±0.2, Min: **83.1**, Max: 83.8 |
| ViT-B/32, 20 tasks | 62.6 | 65.7±0.2, Min: **65.3**, Max: 66.0 |
| ViT-B/16, 20 tasks | 68.2 | 70.3±0.2, Min: **69.8**, Max: 70.7 |
| ViT-L/14, 20 tasks | 77.7 | 76.0±0.2, Min: 75.6, Max: 76.4 |

In 5 of 9 settings (bold) OPCM's minimum exceeds the continual fine-tuning run; in the rest OPCM is "within 1-5%" of it (p. 36). OPCM needs "only a few seconds versus 20-30 minutes per task for continual fine-tuning" (p. 37).

**Comparison with conventional (all-at-once) merging** (Table 7, p. 38). Eight tasks, CLIP-ViT-B/32, accuracy (%):

| Method | SUN397 | Cars | RESISC45 | EuroSAT | SVHN | GTSRB | MNIST | DTD | Avg. |
|---|---|---|---|---|---|---|---|---|---|
| *Conventional* | | | | | | | | | |
| Fisher Merging | 66.7 | 64.0 | 72.2 | 91.6 | 69.0 | 64.3 | 83.5 | 53.7 | 70.6 |
| RegMean | 67.8 | 68.9 | 82.5 | 94.4 | 90.6 | 79.2 | 97.6 | 63.2 | 80.5 |
| Task Arithmetic | 57.1 | 55.7 | 64.9 | 76.7 | 77.9 | 68.5 | 96.1 | 47.2 | 68.0 |
| Ties-Merging | 67.1 | 64.2 | 74.1 | 76.8 | 77.7 | 69.4 | 94.1 | 54.0 | 72.2 |
| Task-wise AdaMerging | 58.6 | 56.9 | 69.8 | 82.4 | 70.3 | 58.9 | 97.2 | 55.3 | 68.7 |
| Layer-wise AdaMerging | 67.9 | 71.3 | 83.5 | 92.7 | 87.4 | 92.9 | 98.2 | 67.0 | 82.6 |
| TSVM | 67.6 | 71.6 | 84.7 | 93.4 | 91.9 | 92.5 | 98.9 | 63.8 | 83.1 |
| *Continual* | | | | | | | | | |
| C. Layer-wise AdaMerging | 62.2 | 64.6 | 71.1 | 70.6 | 91.2 | 94.5 | 98.4 | 35.3 | 73.5 |
| C. TSVM | 59.9 | 59.5 | 64.0 | 64.7 | 87.9 | 86.1 | 99.5 | 34.3 | 68.5 |
| OPCM (10 runs) | 66.2±0.5 | 63.5±0.5 | 78.0±2.2 | 86.5±1.9 | 82.4±1.3 | 74.3±1.4 | 96.9±0.7 | 56.4±1.3 | 75.5±0.5 |

AdaMerging drops from 82.6% (conventional) to 73.5% when used continually (p. 38). OPCM is better than "most" conventional methods (p. 38), though not RegMean, layer-wise AdaMerging or TSVM in this table.

**Runtime** (Table 2, p. 27; the model and number of tasks aren't stated next to the table; **our reading:** every total-to-per-model time ratio is about 8, e.g. 73.26/9.1, so probably 8 models):

| Method | Wall-clock time of merging | Wall-clock time per model |
|---|---|---|
| Continual Task Arithmetic | 0.37s | ≈0.04s |
| Continual Ties Merging | 15.65s | ≈2s |
| AdaMerging (Conventional Model Merging) | 10.47min | ≈78.5s |
| AdaMerging (Continual Model Merging) | 11.85min | ≈88.9s |
| OPCM | 73.26s | ≈9.1s |

**Hyperparameters** (Section 6.2, p. 9; Appendix D.4, pp. 37–38):

- **Task arithmetic is sensitive to $\lambda$:** the text gives 0.3 for 8 tasks and 0.1 for 14 and 20 tasks (pp. 33, 38). **Our reading:** Figures 6a (p. 9) and 13 (p. 37) peak at $\lambda = 0.2$ for ViT-B/32 (about 0.69 vs about 0.675 at 0.3) and ViT-L/14 on 8 tasks; only ViT-B/16 peaks at 0.3. Table 1's continual task arithmetic value for ViT-B/32 on 8 tasks (67.5) matches the $\lambda = 0.3$ point, so this baseline may be under-tuned.
- **OPCM vs $\alpha$:** an inverted U, with the optimum for $\alpha \approx 0.4$–$0.6$ (p. 9), "consistently" within 0.4–0.6 regardless of the number of tasks (p. 38); the optimal $\alpha$ stays around 0.5 across task counts (p. 9) and across model sizes on 20 tasks (Figure 7a, p. 9).
- OPCM beats task arithmetic "across a broad spectrum of $\alpha$ values ($\alpha \leq 0.9$)" (p. 38; Figure 14, p. 37). **Our reading** of Figures 6b and 14: accuracy drops sharply at $\alpha = 1.0$.

**Task-vector similarity** (Figure 4, p. 6; Figures 9–10, pp. 29–30; text p. 28):

- Most off-diagonal cosine similarities between task vectors are 0.01–0.05 (p. 28).
- Related tasks are more similar: digit tasks (SVHN, MNIST, EMNIST, KMNIST) and CIFAR10/CIFAR100 (p. 28). Printed cells: SVHN–MNIST 0.15 for ViT-B/32 (Figure 4, p. 6; Figure 9, p. 29) and 0.25 for ViT-B/16 (Figure 10, p. 30); CIFAR100–CIFAR10 0.11 for both (pp. 29–30).
- ViT-L/14 shows slightly lower similarity overall (p. 28).

**Fine-tuned models** (Table 3, p. 28): per-task test accuracy of pre-trained and fine-tuned models for the 20 tasks; their averages are the "Pre-Trained" and "Fine-Tuned" rows of Table 1.

## Assumptions and limitations

- **Same pre-trained model, same architecture:** every method operates on task vectors $\theta^{(t)} - \theta^{(0)}$ from one shared $\theta^{(0)}$ (p. 3).
- **Heads are frozen and shared with the pre-trained model** (zero-shot CLIP text heads) (pp. 27–28, p. 32): the merged model needs no new parameters per task.
- **Only linear-layer weights are projected;** biases and other parameters are combined without projection (p. 5).
- **Fixed $\alpha = 0.5$** in all experiments (p. 8); the baselines' $\lambda$ is chosen as the value with the highest average accuracy (p. 33), the paper does not say on which split.
- **Continual fine-tuning is a single run** (seed 42) while OPCM is averaged over 10 orders (p. 32, p. 36).
- **Vision only:** "While our current work focuses on vision models, the proposed method's principles are generally applicable to other domains" (p. 10); extensions to language and multimodal models are future work (p. 10).
- **Limitations the authors point to** (checklist, p. 17): the non-commutativity of continual merging (Section 3.2) and the cost of the SVD-based projection (Appendix B).
- **Our reading:**
  - The projection formula sums over $i, j \geq r_\alpha$ with $i \neq j$ (p. 6), which excludes the diagonal components $u_i v_i^T$ beyond $r_\alpha$ as well; the orthogonality proof relies only on $i \neq j$ (p. 25). How exactly the released code builds the projection should be checked before reimplementing.
  - Eq. 9's sum applies $\mathcal{P}^{(j-1)}_\alpha$ to $\Delta\theta^{(i)}$ (as printed, p. 6), which looks like a typo for $\Delta\theta^{(j)}$; the gap argument is first-order and informal.
  - Theorem 5.2 assumes $\lambda^{(t)} = \sqrt{t}$, not the adaptive $\lambda^{(t)}$ used by Algorithm 1; the two are close empirically (Figure 7b, p. 9).
  - The "5–8%" gain is over other merging methods; OPCM stays well below the individual fine-tuned models (e.g. 65.7 vs 89.8 on ViT-B/32, 20 tasks, Table 1) and below conventional (all-at-once) merging methods such as TSVM on 8 tasks (75.5 vs 83.1, Table 7).
  - The degradation figures on p. 8 (17.5, 24.1, 21.3) equal Fine-Tuned minus OPCM in Table 1 (e.g. 93.5 − 76.0), so they are absolute accuracy points, though printed with "%".
  - Conventional task arithmetic on 8 ViT-B/32 tasks scores 68.0 (Table 7) and continual task arithmetic 67.5 (Table 1); with a fixed $\lambda$ the two should give the same final model, so the difference may come from a different $\lambda$ or setup, not explained in the paper.
  - There is no joint multi-task training baseline (all tasks' data at once), only sequential continual fine-tuning.

## Relevance to this thesis

**Our reading:**

- **A formal frame for the sequential setting we study:** Definition 3.2 (continual merging), the non-commutativity issue (Eq. 4) and the metrics ACC and BWT with an accuracy matrix (p. 32, p. 34) map directly onto merging models trained on successive periods or successive datasets of time series.
- **Continual task arithmetic (Eq. 5 / Eq. 37) is the natural sequential baseline:** it needs only the running merged model, and with Eq. 37's start ($\theta^{(0)}_{\text{merged}} = \theta^{(0)}$, p. 33), its final model equals one-shot task arithmetic with the same $\lambda$; Definition 3.2 "typically" starts from $\theta^{(1)}_{\text{merged}} = \theta^{(1)}$ (p. 3), which gives the first task vector weight 1 instead of $\lambda$. We can compare it with joint training, one-shot task arithmetic, continual fine-tuning and OPCM on the same task sequences.
- **What to test for anomaly detection and forecasting:**
  - whether OPCM's projection helps when task vectors are **not** near-orthogonal, as may be the case for consecutive periods of the same signal (the paper's tasks have cosine similarity mostly 0.01–0.05, p. 28); Corollary A.2 (p. 26) predicts that highly correlated updates are mostly filtered out, which could also discard useful drift adaptation;
  - whether $\lambda^{(t)} \approx \sqrt{t}$ holds for our models;
  - the sensitivity to $\alpha$ (paper: optimum 0.4–0.6, sharp drop at 1.0) and to task order (10 shuffled orders, as in the paper);
  - BWT on earlier periods (forgetting) next to accuracy on the latest one.
- **Gaps to fill ourselves:** the paper has no joint multi-task training baseline and only one continual fine-tuning run; our study should add both, with several orders and seeds.
- **Practical constraints:** heads must be shared or frozen for weight-space merging; for forecasting and anomaly scoring heads (regression, reconstruction) this needs a design choice. The full SVD per linear layer is affordable for small time-series models (Table 2 gives about 9 s per model for CLIP, p. 27).
- **Reimplementation:** the code is public (p. 1); the projection's index range (see limitations) should be checked against it.

## Quotes worth keeping

> "However, these conventional approaches are not well-suited for scenarios where models become available sequentially, and they often suffer from high memory requirements and potential interference between tasks." (p. 1)

> "However, the aforementioned methods are all based on learning from the original data. In contrast, the continual merging approach proposed in this paper allows us to directly merge a sequence of models (i.e., tasks) arriving in a stream, offering an orthogonal perspective to continual learning." (p. 3)

> "Moreover, as earlier parameter information is gradually diminished throughout the sequential process, the final model might not completely encapsulate the knowledge from all individual tasks." (p. 4)

> "This formulation can be interpreted as a more generalized form of Task Arithmetic, where the task vectors are projected onto a subspace spanned by the previous merged model." (p. 5)

> "The results in the table demonstrate that AdaMerging in the continual merging setting achieves 73.5% average accuracy, which is notably lower than its performance in the conventional model merging setting (82.6%)." (p. 38)

> "While our current work focuses on vision models, the proposed method's principles are generally applicable to other domains." (p. 10)
