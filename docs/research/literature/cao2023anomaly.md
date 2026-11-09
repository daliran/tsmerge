# cao2023anomaly — Anomaly Detection under Distribution Shift

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 150 claims, every table cell correct: 2 misstatements, including one non-verbatim quote, and 4 precision issues, all fixed)
- **Reference:** Cao, Zhu, Pang; ICCV 2023; arXiv 2303.13845 ([references.bib](references.bib))
- **Version read:** the ICCV 2023 Open Access version from the Computer Vision Foundation (watermark on p. 1; proceedings pages 6511–6523 printed at the bottom), 13 pages: main text pp. 1–9, references pp. 10–13. The Appendix the paper refers to (p. 6, p. 7) is not part of this version
- **Read:** all 13 pages: main text (Sections 1–6, Figures 1–5, Tables 1–7) and the reference list
- **Code:** <https://github.com/mala-lab/ADShift> (p. 1, abstract)

## In one paragraph

The paper studies **unsupervised anomaly detection (AD) when the test data come from a shifted distribution** (new lighting, poses, backgrounds, styles), while training sees only normal data from the source distribution (p. 1, p. 3).

It builds benchmarks from four datasets (MVTec and CIFAR-10 with four synthetic corruptions; MNIST → MNIST-M; PACS Photo → Art, Cartoon, Sketch) (p. 6), and shows

- that AD methods lose much of their AUROC on the shifted data,
- and that plugging out-of-distribution (OOD) generalization methods into a state-of-the-art AD model (RD4AD) barely helps (p. 7).

It proposes **generalized normality learning (GNL)**, built on RD4AD:

- at training time, a loss makes the features of a normal sample and of its augmented copies similar, at the bottleneck and at the last decoder block;
- at test time, the features of each test sample are matched to the feature distribution of a random normal training sample (Exact Feature Distribution Matching, EFDM) in the first two encoder blocks (pp. 4–5).

GNL gives the best OOD AUROC on almost all shifted test sets, e.g. 70.87 vs 59.61 for the best baseline on MNIST-M (Table 3, p. 7), while staying close to the best on the in-distribution (ID) test data (Tables 1–4, p. 7).

## Problem

**The issue** (pp. 1–3):

- Existing AD methods "generally assume that the training and test data are drawn from the same data distribution" (p. 1).
  - In practice the test data can shift because of "new lighting conditions, object poses, or background appearances" (p. 1).
- Under shift, **normal** test samples can differ from the normal training data "in terms of foreground and/or background features" and be "falsely detected as anomaly" (p. 2, Figure 1, p. 1).
- Conversely, some abnormal OOD samples may share background or style features with the training data and get low anomaly scores (p. 3).
- OOD generalization methods usually need class labels, domain labels, or diverse source data.
  - AD training data "consists of only one class, and the data is monotonous" (p. 2), so those methods are hard to adapt (p. 2, p. 3).

**What the problem is and isn't** (p. 2): the authors frame it as

- an **OOD generalization** problem (detect normal and anomalous samples in shifted test data, while staying effective on ID test data),
- different from **OOD detection** (rejecting OOD samples as unknown in supervised models).

**Formal setting** (Section 3.1, p. 3):

- $\mathcal{X}_s$: source (ID) distribution, used in training and testing; $\mathcal{X}_t$: target (OOD) distribution, used only at inference.
- Training: only normal source data, $\mathcal{D}_s = \{x \in \mathcal{X}_s \mid y = 0\}$, with $y \in \{0, 1\}$ (0 normal, 1 abnormal).
- Testing: normal or abnormal samples from either distribution, $\mathcal{D}_t = \{x \in \mathcal{X}_s \cup \mathcal{X}_t \mid y = \{0, 1\}\}$ (as printed).
- Goal: an unsupervised anomaly scorer $f : \mathcal{X} \to \mathbb{R}$ such that $\forall x_i, x_j \in \mathcal{D}_t,\ f(x_i) < f(x_j)$ when $y_i = 0$ and $y_j = 1$.

**What is known when** (p. 3, p. 6):

- At training: only ID normal images; no OOD data ("assuming the OOD data is not available during training", p. 6), no anomalies, no domain labels.
- At test: ID and OOD test sets are both used (p. 6), without being told which a sample comes from.
  - **Our reading:** the test-time step treats every sample the same way, p. 5.
  - The method does use **normal training samples at inference** (a random $q \in \mathcal{D}_s$ per test sample, p. 5).
- Differs from cross-domain AD methods, which "require class labels in the ID data or few training samples from the target domain" (p. 3).

**Types of shift used** (p. 6):

| Dataset | ID (train and ID test) | OOD test | Kind of shift |
|---|---|---|---|
| MVTec | original images | Brightness, Contrast, Defocus Blur, Gaussian noise; severity 3 | synthetic corruptions [22] |
| CIFAR-10 | original images | same 4 corruptions; severity 5 | synthetic corruptions [22] |
| MNIST / MNIST-M | MNIST | MNIST-M (random colored patches superimposed on MNIST) | appearance / background |
| PACS | Photo | Art, Cartoon, Sketch | domain (style) |

**Our reading:**

- in all four benchmarks the shift changes the appearance of the inputs while the definition of "normal" (which class is normal) stays fixed;
- the paper doesn't use the terms covariate or concept shift, but this is a covariate-type shift, with no change in what counts as an anomaly.

## Method

**Base model: RD4AD** (reverse distillation, [13]) (p. 4):

- A fixed teacher encoder, a trainable one-class bottleneck embedding module, and a student decoder.
- The teacher extracts multi-scale representations; the student decoder learns to reconstruct them from the bottleneck embedding.
- At test time the student fails to reconstruct the teacher's features of anomalous samples; low similarity means "highly abnormal" (p. 4).
- Figure 3 (p. 4): teacher blocks E1, E2, E3, bottleneck, decoder blocks D3, D2, D1; $\mathcal{L}_{ori}$ links each $E_i$ to its $D_i$.
- GNL keeps RD4AD's settings: image size, optimizer, anomaly score computation and other parameters, detailed in the Appendix (p. 6), which this version doesn't include.
- **Our reading:** the paper never writes out $\mathcal{L}_{ori}$ or the anomaly score; they come from RD4AD.

### Training: distribution-invariant normality learning (DINL) (Section 4.1, pp. 4–5)

For a normal sample $x \in \mathcal{D}_s$, augmented copies $x'_k = \mathcal{T}(x)$, $k \in [1, N]$, with $N$ the number of augmented normal samples (p. 4). $\phi$ maps the raw image into the embedding space at the bottleneck layer (p. 4).

**Bottleneck loss** (Eq. 1, p. 4), with $\mathcal{L}_{sim}(\cdot, \cdot)$ "a cosine similarity-based loss function" (its exact form isn't given):

$$\mathcal{L}_{\text{abs}} = \sum_{k=1}^{N} \frac{1}{N} \left\{ \mathcal{L}_{sim}\big(\phi(x), \phi(x'_k)\big) \right\}$$

**Low-level feature loss** (Eq. 2, p. 4), with $\omega$ the reconstruction from the abstract features to the low-level features at the final block of the decoder:

$$\mathcal{L}_{lowf} = \sum_{k=1}^{N} \frac{1}{N} \left\{ \mathcal{L}_{sim}\big(\omega(\phi(x)), \omega(\phi(x'_k))\big) \right\}$$

**Total loss** (Eq. 3, p. 4; "distribution-invariant, normality-preserved loss function"):

$$\mathcal{L} = \lambda_{ori} * \mathcal{L}_{ori} + \lambda_{abs} * \mathcal{L}_{abs} + \lambda_{lowf} * \mathcal{L}_{lowf}$$

where $\mathcal{L}_{ori}$ is RD4AD's original loss and the $\lambda$ are weights (p. 5).

**Augmentation** (p. 5): AugMix [24], with the augmentation types that may create anomalies removed ("shear_x", "shear_y", "translate_x", "translate_y"), "to ensure that all generated data are normal samples".

**Rationale** (p. 5):

- the last decoder block reconstructs low-level features (edges, corners, blobs), the bottleneck extracts high-level features;
- the bottleneck representation of the same image under different synthetic transformations "must be the same", while keeping enough information for reconstruction.

(The text says this is achieved "by minimizing the loss function in Eq. 5", p. 5; **our reading:** Eq. 3 is meant, since Eq. 5 is the FDM step.)

### Inference: AD-oriented test-time augmentation (ATTA) (Section 4.2, p. 5)

Goal: inject the training distribution into each test sample through **feature distribution matching (FDM)** in the first two residual blocks of the teacher encoder.
From the third block on, and for the anomaly score, inference follows RD4AD unchanged (p. 5; Figure 3b, p. 4).

For a test sample $p \in \mathcal{D}_t$, pick a **random** normal training sample $q \in \mathcal{D}_s$; $\mathcal{P}^m$, $\mathcal{Q}^m$ are their features at residual encoding block $E^m$ (Eq. 4, p. 5):

$$
\begin{cases}
\mathcal{P}^{m+1} = \text{FDM}\big(E^{m+1}(\mathcal{P}^m), \mathcal{Q}^{m+1}, \alpha\big) \\
\mathcal{Q}^{m+1} = E^{m+1}(\mathcal{Q}^m) \\
\mathcal{P}^0 = p, \ \mathcal{Q}^0 = q,
\end{cases}
\qquad m \in \{0, 1\}
$$

$\alpha$ balances "the severity for mixing the style" between test and normal sample (p. 5). $\mathcal{P}^1$, $\mathcal{P}^2$ then go into the bottleneck and the anomaly score as in RD4AD (p. 5).

**FDM = EFDM** [86] (Eq. 5, p. 5):

$$\text{FDM}(\mathcal{C}, \mathcal{V}, \alpha) : \ \mathcal{C}_{\tau_i} = (1 - \alpha)\, \mathcal{C}_{\tau_i} + \alpha\, \mathcal{V}_{\kappa_i}$$

- $\{\mathcal{C}_{\tau_i}\}_{i=1}^{n}$ and $\{\mathcal{V}_{\kappa_i}\}_{i=1}^{n}$: the values of the embedded features $\mathcal{C}$ and $\mathcal{V}$ sorted in ascending order; $n$ is the number of elements in each vector (p. 5).
- $\mathcal{C}$: test sample's feature, carrying the appearance information; $\mathcal{V}$: random normal training sample's feature, carrying the style information (p. 5).
- EFDM matches empirical cumulative distribution functions of features, so it matches mean, standard deviation and higher-order statistics (p. 5).
- Why a random $q$: the training data are monotonous, so any training sample carries the training distribution, avoiding a costly sample selection (p. 5).
- Claimed effect: for OOD test samples, the gap to the normal training feature distribution shrinks; for ID test samples, the feature distribution "remains nearly unchanged" (p. 5).
- Difference from Mixstyle and EFDMix (printed "EDFMix", p. 5): those use FDM **during training** to create new distributions; here FDM is used **at inference** (p. 5).

## Experimental setup

**Datasets** (Section 5.1, p. 6):

- **MVTec:** 15 subsets for industrial defect inspection (5 texture, 10 object); training: 3,629 images, all normal; test: 1,725 images, defective and non-defective.
- **CIFAR-10:** 50,000 training and 10,000 test images in 10 equally sized classes.
- **MNIST / MNIST-M:** MNIST, 70,000 grayscale handwritten digits (ID); MNIST-M, 68,000 images (OOD); 10 shared classes.
- **PACS:** 9,991 images, seven classes, four domains (Art, Cartoon, Photo, Sketch); Photo is ID, the other three OOD.
- **Corruptions** (MVTec, CIFAR-10): Brightness, Contrast, Defocus Blur, Gaussian noise from [22]; severity 3 on MVTec, 5 on CIFAR-10.
- **Protocol:** one-versus-all [58] (one class normal, the rest anomalies) for MNIST and PACS; plus a **multi-class** setting on MNIST/MNIST-M: even digits normal, odd digits anomalies.
- Training uses only the ID dataset; inference uses the ID and OOD test sets (p. 6).

**Baselines** (Section 5.2, p. 6):

- AD methods: Deep SVDD, f-AnoGAN, KDAD, RD4AD, with their official implementations.
  - On PACS (not in the original papers), the MVTec hyperparameters (p. 6).
- OOD generalization methods combined with RD4AD: Augmix, Mixstyle, EFDM (data augmentation), Jigsaw (self-supervised), and the combinations Augmix+Mixstyle, Augmix+EFDM (p. 6, Tables 1–4).
- Augmix: online augmentation severity 3.
  - All augmentation types for MNIST and PACS.
  - On MVTec and CIFAR-10, Brightness and Contrast excluded because they overlap with the test corruptions (p. 6).
- Mixstyle and EFDM (feature-level): applied to the encoders in the first two network layers, following RD4AD's settings.
- Jigsaw: fitted into the bottleneck component.
- All RD4AD training hyperparameters kept (p. 6).

**GNL hyperparameters** (Section 5.3, p. 6):

| Hyperparameter | Value |
|---|---|
| $N$ (augmented normal samples per sample) | 2 |
| $\lambda_{ori}, \lambda_{abs}, \lambda_{lowf}$ | 0.9, 0.05, 0.05 (default) |
| $\alpha$ (inference style mixing) | 0.5 for MVTec, PACS, CIFAR-10; 0.9 for MNIST/MNIST-M |
| FDM technique | EFDM [86] ("the latest and shows SOTA performance") |
| Other settings (image size, optimizer, anomaly score) | as RD4AD, in the Appendix (not in this version) |

**Metric and averaging:**

- AUROC (p. 6), averaged over three independent runs (p. 6).
- The tables report the average over the classes of each dataset; per-class results are in the Appendix (p. 7).
- Runtime: one RTX 3090 24GB GPU (Table 7, p. 9).

## Results

All tables: AUROC (%), averaged over the classes of each dataset (p. 7). Bold in the paper marks the best per column; marked here with **bold** as printed.

**MVTec and its corruptions** (Table 1, p. 7):

| Method | ID: MVTec | Brightness | Contrast | Blur | Noise |
|---|---|---|---|---|---|
| Deep SVDD | 69.98 | 55.18 | 50.07 | 68.82 | 59.11 |
| f-AnoGAN | 75.65 | 48.36 | 49.29 | 37.98 | 39.10 |
| KDAD | 85.50 | 83.81 | 64.03 | 84.17 | 82.04 |
| RD4AD | **98.64** | 96.50 | 94.12 | **98.9** | 90.14 |
| Augmix | 96.29 | 95.10 | 94.51 | 95.39 | 90.99 |
| Mixstyle | 98.58 | 96.60 | 94.45 | 98.27 | 88.92 |
| EFDM | 98.64 | 96.78 | 94.77 | 98.25 | 89.29 |
| Augmix+Mixstyle | 96.78 | 96.86 | 94.57 | 98.73 | 90.12 |
| Augmix+EFDM | 97.04 | 96.83 | 95.21 | 98.11 | 90.18 |
| Jigsaw | 73.97 | 73.36 | 67.88 | 73.88 | 72.60 |
| GNL (Ours) | 97.99 | **97.43** | **97.46** | 97.77 | **94.10** |

**CIFAR-10 and its corruptions** (Table 2, p. 7):

| Method | ID: CIFAR | Brightness | Contrast | Blur | Noise |
|---|---|---|---|---|---|
| Deep SVDD | 64.62 | 59.13 | 55.94 | 62.13 | 54.46 |
| f-AnoGAN | 70.25 | 54.62 | 57.23 | 60.74 | 51.76 |
| KDAD | 84.21 | 75.91 | 64.37 | 63.49 | 56.87 |
| RD4AD | **84.62** | 75.89 | 65.34 | 66.67 | 58.82 |
| Augmix | 82.83 | 74.15 | 62.48 | **66.92** | 57.36 |
| Mixstyle | 83.68 | 76.07 | 63.87 | 65.74 | 57.74 |
| EFDM | 83.92 | 76.19 | 63.92 | 64.81 | 57.63 |
| Augmix+Mixstyle | 83.87 | 76.02 | 65.55 | 63.89 | 58.04 |
| Augmix+EFDM | 82.96 | 75.73 | 64.39 | 63.83 | 57.14 |
| Jigsaw | 71.29 | 66.86 | 61.45 | 60.12 | 55.29 |
| Ours | 82.29 | **77.94** | **66.13** | 64.04 | **61.51** |

**MNIST (ID) and MNIST-M (OOD)** (Table 3, p. 7):

| Method | One-vs-All ID | One-vs-All OOD | Multi-class ID | Multi-class OOD |
|---|---|---|---|---|
| Deep SVDD | 97.73 | 49.92 | 86.94 | 51.19 |
| f-AnoGAN | 97.52 | 52.72 | 88.45 | 51.85 |
| KDAD | 98.87 | 54.87 | **90.43** | 52.84 |
| RD4AD | **98.89** | 58.09 | 88.70 | 51.74 |
| Augmix | 98.26 | 59.61 | 88.76 | 52.19 |
| Mixstyle | 98.84 | 57.22 | 87.36 | 52.13 |
| EFDM | 98.62 | 57.23 | 87.78 | 52.36 |
| Augmix+Mixstyle | 98.12 | 58.89 | 89.23 | 52.45 |
| Augmix+EFDM | 98.24 | 58.91 | 90.04 | 52.64 |
| Jigsaw | 98.90 | 58.51 | 87.29 | 52.87 |
| GNL (Ours) | 96.91 | **70.87** | 88.59 | **58.50** |

(As printed, Jigsaw's one-vs-all ID value, 98.90, is higher than the bold RD4AD 98.89.)

**PACS: Photo (ID) and Art, Cartoon, Sketch (OOD)** (Table 4, p. 7):

| Method | ID: Photo | Art | Cartoon | Sketch |
|---|---|---|---|---|
| Deep SVDD | 40.87 | 53.42 | 41.23 | 39.48 |
| f-AnoGAN | 61.34 | 50.15 | 52.42 | 63.77 |
| KDAD | **88.17** | 62.86 | 62.64 | 51.40 |
| RD4AD | 81.49 | 61.07 | 60.34 | 55.06 |
| Augmix | 76.35 | 60.50 | 58.96 | 57.86 |
| Mixstyle | 78.23 | 60.93 | 60.93 | 54.89 |
| EFDM | 78.47 | 60.55 | 62.15 | 55.63 |
| Augmix+Mixstyle | 76.12 | 60.16 | 61.29 | 55.76 |
| Augmix+EFDM | 77.28 | 60.93 | 63.18 | 56.67 |
| Jigsaw | 62.19 | 52.55 | 53.83 | 62.15 |
| GNL (Ours) | 87.67 | **65.62** | **67.96** | **62.39** |

(As printed, f-AnoGAN's Sketch value, 63.77, is higher than the bold GNL 62.39.)

**What the authors conclude from Tables 1–4** (pp. 7–8):

- All AD methods drop on OOD data across the four datasets; on MNIST → MNIST-M "by about 30-40%"; on MVTec and CIFAR-10 the drop is "less severe" (p. 7).
- Combining OOD generalization methods with RD4AD doesn't significantly improve detection (p. 7). Their explanation:
  - these methods enrich data "based on its own distribution", but AD training data are "monotonous and unimodal", so the added diversity is too small (p. 7);
  - and they "have a tendency to generate undesired anomaly data", like injecting noise into training (pp. 7–8).
- GNL on MNIST-M: "increasing by at least 10 AUROC scores" over all other methods (p. 8).
- GNL on PACS: "increasing by at least 5% on the Art and Cartoon datasets over the competing models" (p. 8).
  - It also improves over RD4AD on the ID Photo data, which the authors attribute to Photo containing several sub-domains on which RD4AD may overfit (p. 8).
  - Against KDAD (best on ID, 0.8817 vs GNL's 0.8767), GNL is better on the three OOD sets "by about 3%-10%" (p. 8).
  - **Our reading:** in points, +2.76 on Art, +5.32 on Cartoon and +10.99 on Sketch (Table 4).
- Contributions (p. 2; the abstract, p. 1, says only "substantially outperforms"): GNL beats state-of-the-art AD and OOD generalization methods "by over 10% in AUCROC [sic] on data with various distribution shifts" (p. 2).
- **Our reading:** in absolute points, GNL's margin over the best competitor is 2.76 on Art (65.62 vs 62.86) and 4.78 on Cartoon (67.96 vs 63.18) (Table 4, p. 7).
  - So the "at least 5%" on p. 8 fails on Art both in points and relatively (2.76/62.86 = 4.4%) and holds on Cartoon only relatively (4.78/63.18 = 7.6%).
  - Likewise "at least 10 AUROC scores" on MNIST-M (p. 8) holds only one-vs-all (multi-class: 58.50 vs 52.87 = 5.63, Table 3).
  - The "over 10%" holds for MNIST-M one-vs-all (70.87 vs 59.61, Table 3), not across all shifted sets (e.g. MVTec Blur, where GNL is below RD4AD, Table 1).

**Robustness to shift severity** (Section 5.5, p. 8; Figure 4, p. 8). MVTec, 'Contrast' corruption at severities 1–5, against RD4AD, Augmix, EFDM:

- The baselines decline significantly as severity grows.
- GNL is stable for severities 1–3 and "reduces to an AUROC of about 0.90 when the severity is 4 and 5, decreasing about 5% AUROC vs. about 30%-35% decrease in the competing methods" (p. 8).
- **Our reading** of the plot (approximate):
  - all methods near 97 at severity 1;
  - at severity 4, GNL about 94.5;
  - at severity 5, GNL about 89, Augmix about 66, RD4AD and EFDM about 60.
  - GNL's plotted drop from severity 1 to 5 is about 8–9 points, more than the "about 5%" in the text.

**Ablation on PACS** (Section 5.6, pp. 8–9; Table 5, p. 9). Baseline is RD4AD:

| Method | ID: Photo | Art | Cartoon | Sketch |
|---|---|---|---|---|
| Baseline | 81.49 | 61.07 | 60.34 | 55.06 |
| $\mathcal{L}_{abs}$ only | 82.02 | 60.59 | 63.93 | 56.81 |
| $\mathcal{L}_{lowf}$ only | 82.90 | 61.27 | 62.25 | 55.52 |
| DINL | 85.71 | 62.34 | 65.63 | 57.12 |
| ATTA | 81.05 | 64.36 | 62.04 | 57.04 |
| DINL+ATTA | **87.67** | **65.62** | **67.96** | **62.39** |

Authors' reading (p. 9):

- ATTA alone gives about 2% AUROC on the OOD sets but slightly lowers ID;
- DINL alone improves both ID and OOD, "having 4%-7% AUROC improvement";
- both together are best, so the two components complement each other.

**Our reading:**

- Table 5 gives DINL over the baseline +4.22 (Photo), +1.27 (Art), +5.29 (Cartoon), +2.06 (Sketch), i.e. 1.3–5.3 points, not 4–7;
- ATTA's "about 2%" roughly matches (+3.29, +1.70, +1.98 on the OOD sets).

**Sensitivity to $\alpha$** (Section 5.7, p. 9; Figure 5, p. 9), PACS, $\alpha$ from about 0.1 to 1.0 (a smaller $\alpha$ means a milder style transfer):

- Stable on Photo and Cartoon; Art improves as $\alpha$ grows; Sketch peaks at $\alpha = 0.4$ and then slightly decreases (p. 9).
- "a medium value, e.g., α = 0.5, is generally recommended in practice" (p. 9).
- **Our reading** of the plot (approximate): Photo about 87–89; Cartoon about 67–68; Art from about 62.5 to about 68.5; Sketch from about 59 to a peak near 63.7.

**Sensitivity to the $\lambda$ weights** (Section 5.7, p. 9; Table 6, p. 9). DINL, weights summing to one, $\lambda_{abs} = \lambda_{lowf}$:

| $\lambda_{ori}; \lambda_{abs}; \lambda_{lowf}$ | Photo (ID) | Art | Cartoon | Sketch |
|---|---|---|---|---|
| 0.95, 0.025, 0.025 | 85.90 | 62.71 | 64.28 | 59.97 |
| 0.90, 0.050, 0.050 | 85.71 | 62.34 | 65.63 | 57.12 |
| 0.85, 0.075, 0.075 | 85.60 | 63.23 | 65.03 | 58.57 |
| 0.80, 0.100, 0.100 | 84.89 | 61.45 | 65.12 | 56.84 |

The authors call DINL robust across these ratios (p. 9). **Our reading:** the 0.90 row equals the DINL row of Table 5, so Table 6 is DINL without ATTA.

**Time and space** (Section 5.8, p. 9; Table 7, p. 9). Runtime (s) on the 'Dog' class of PACS, one RTX 3090 24GB GPU; no extra parameters, since RD4AD's architecture is unchanged:

| Model | Training (per epoch) | Inference (per image) |
|---|---|---|
| RD4AD | 2.5726 | 0.0282 |
| Ours | 7.2557 | 0.0356 |

## Assumptions and limitations

- **Only normal ID data at training;** no OOD data, no labels of any kind (p. 3, p. 6).
- **Access to normal training samples at test time:** each test sample is mixed with a random normal training sample (p. 5).
- **Augmentations must not create anomalies:** the authors remove the shear and translate operations by hand (p. 5); which augmentations are safe depends on the domain.
- **Built on one AD model** (RD4AD, teacher-student reverse distillation).
  - The losses live at its bottleneck and decoder, the test-time step in its teacher encoder (pp. 4–5).
- **ID cost:** on some datasets GNL is below the best ID method (MNIST one-vs-all 96.91 vs 98.89, Table 3; CIFAR-10 82.29 vs 84.62, Table 2, p. 7).
  - ATTA alone slightly lowers ID AUROC (p. 9).
- **Image data only;** the paper contrasts itself with cross-domain AD work on video ("They focus on video data, while we focus on image data", p. 3).
- **Missing details:** $\mathcal{L}_{ori}$, $\mathcal{L}_{sim}$, the anomaly score, the image size and the optimizer are not given in the main text.
  - They are deferred to RD4AD and to an Appendix not included in the version read (p. 4, p. 6).
- **Small inconsistencies in the text,** as printed:
  - "the loss function in Eq. 5" for the training loss (p. 5);
  - "$\mathcal{L}_{abs}$ and $\mathcal{L}_{abs}$ individually" in the ablation (p. 8);
  - the CIFAR-10 paragraph refers to "the native MVTec ID data" (p. 8);
  - two bold values that aren't the column maximum (Table 3 and Table 4, p. 7), and a tie not marked bold (EFDM 98.64 = RD4AD on MVTec ID, Table 1, p. 7);
  - "all four OOD datasets of PACS", which has three (p. 8);
  - GNL's 0.6404 on Defocus_blur called "enhanced" though below RD4AD (66.67) and Augmix (66.92) (p. 8; Table 2, p. 7);
  - and the ablation attributing $\mathcal{L}_{abs}$ and $\mathcal{L}_{lowf}$ to "low-level and high-level features respectively" (p. 8), the reverse of p. 5.
- **Our reading:**
  - the shifts are a fixed, single step from one source to one target, never a sequence;
  - robustness is studied only for one corruption type (Contrast on MVTec) across severities;
  - there is no statistical spread reported beyond the three-run average;
  - and no method adapts to the target data, even when unlabeled target data would be available.

## Relevance to this thesis

**Our reading:**

- **The evaluation protocol transfers directly:** report AUROC on the ID test set and on each shifted test set separately, so that robustness gains are weighed against ID losses.
  - For time series, "ID" and "OOD" map to test windows from the training period and from a later, drifted period.
- **A no-adaptation reference point:** GNL handles shift without ever seeing target data, by making normality features invariant to augmentations and aligning test features to training statistics.
  - Our continual strategies (joint training, task arithmetic, sequential fine-tuning) instead see data from each new period.
  - GNL-style robustness is the "what if we don't update at all" alternative, and a fair comparison would include a model trained once on the first period.
- **Feature distribution matching at test time** (Eq. 5) is a cheap, model-agnostic operation that could apply to the intermediate features of a time-series encoder (sorting feature values per channel and mixing with a stored normal window).
  - Whether it helps under drift in sensor signals, where shift often changes level, scale or correlation between channels rather than texture or style, is open.
- **The "safe augmentations" constraint matters more for time series:** many natural transformations of a signal (shifts in time, scaling, injected noise) can create exactly the anomalies a detector should catch, so an invariance loss like Eqs. 1–2 would need a domain-specific list of transformations that keep a window normal.
- **The paper's negative result** (OOD generalization add-ons barely help a strong AD model, p. 7) is a warning for our baselines:
  - generic robustness tricks may not move AUROC under drift;
  - the gain came from methods designed for the one-class setting.
- **Our setting differs** in that drift in industrial time series (e.g. a water-treatment testbed) is gradual and sequential, and the definition of normal may itself change; the paper covers neither.

## Quotes worth keeping

> "Most existing AD studies assume that the training and test data are drawn from the same data distribution, but the test data can have large distribution shifts arising in many real-world applications due to different natural variations such as new lighting conditions, object poses, or background appearances, rendering existing AD methods ineffective in such cases." (p. 1; printed as "studiesassume")

> "It is an OOD generalization problem, aiming at learning generalized detection models to accurately detect normal and anomalous samples in test data with distribution shifts, while maintaining the effectiveness on in-distribution test data." (p. 2)

> "However, the training data in the AD task consists of only one class, and the data is monotonous." (p. 2)

> "During training, we only use images in the ID dataset, i.e., assuming the OOD data is not available during training. During inference, test sets of both ID and OOD are used." (p. 6)

> "Furthermore, FDM ensures that the feature distribution remains nearly unchanged if inference samples come from ID sets, since the distribution of the test sample is aligned with its own distribution." (p. 5)

> "This lack of improvement can be attributed to the fact that these OOD methods attempt to increase the diversity of data by enriching the available data based on its own distribution." (p. 7)
