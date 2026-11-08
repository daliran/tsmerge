# pang2021deep — Deep Learning for Anomaly Detection: A Review

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 260 claims, all 49 equations and every table cell correct: 2 page references and 1 incomplete reading, fixed)
- **Reference:** Pang, Shen, Cao, van den Hengel; ACM Computing Surveys 54(2), Article 38, 2021; DOI 10.1145/3439950; arXiv 2007.02500 ([references.bib](references.bib))
- **Version read:** ACM published version, 39 PDF pages: ACM Digital Library cover p. 1; article pp. 2–39 (printed 38:1–38:38, so PDF page = printed page + 1); main text pp. 2–33; references pp. 33–39
- **Read:** pp. 1–33 in full (cover, Sections 1–8, Tables 1–3, Figures 1–2); references skimmed on pp. 33–36 and p. 39. Not read: references on pp. 37–38 ([112]–[167]). The "Table A1 in Appendix A" with source-code links (p. 29) is not in this PDF
- **Resources:** a "continuously updated collection of widely used anomaly detection datasets" at <https://git.io/JTs93> (p. 30)

## In one paragraph

The survey reviews deep learning methods for anomaly detection ("deep anomaly detection"), which learn feature representations or anomaly scores with neural networks (p. 3). It first lists the problem complexities of anomaly detection and six largely unsolved challenges (CH1–CH6, pp. 4–6), then organizes the methods into a hierarchical taxonomy of **3 high-level categories and 11 fine-grained categories** (p. 2, p. 7, Figure 1): deep learning for feature extraction; learning feature representations of normality (generic normality feature learning: autoencoders, GANs, predictability modeling, self-supervised classification; anomaly measure-dependent feature learning: distance, one-class classification, clustering); and end-to-end anomaly score learning (ranking, prior-driven, softmax likelihood, end-to-end one-class classification). For each category it gives the assumption, the objective function, advantages, disadvantages and the challenges it targets (pp. 8–28). It then tabulates 30 representative algorithms (Table 2, p. 29) and 21 public datasets with real anomalies (Table 3, p. 30), and closes with future opportunities (pp. 30–33). It contains no new experiments and no cross-method performance comparison (pp. 28–29).

## Problem

**Definition** (p. 2): anomaly detection, "a.k.a. outlier detection or novelty detection", is "the process of detecting data instances that significantly deviate from the majority of data instances".

**Formal setting** (p. 7): given a dataset $\mathcal{X} = \{\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_N\}$ with $\mathbf{x}_i \in \mathbb{R}^D$, and a representation space $\mathcal{Z} \in \mathbb{R}^K$ ($K \ll N$), deep anomaly detection learns either

- a feature representation mapping $\phi(\cdot) : \mathcal{X} \mapsto \mathcal{Z}$, followed by an additional step that computes an anomaly score in $\mathcal{Z}$, or
- an anomaly score learning function $\tau(\cdot) : \mathcal{X} \mapsto \mathbb{R}$ that infers scores directly from raw inputs,

such that anomalies are easily differentiated from normal instances; $\phi$ and $\tau$ are neural networks with $H \in \mathbb{N}$ hidden layers and weight matrices $\Theta = \{\mathbf{M}^1, \mathbf{M}^2, \dots, \mathbf{M}^H\}$. Larger $\tau$ outputs mean more anomalous (p. 7).

**Problem complexities** (pp. 3–4), common to deep and shallow methods:

- **Unknownness:** anomalies remain unknown until they actually occur.
- **Heterogeneous anomaly classes:** one class of anomalies may look completely different from another.
- **Rarity and class imbalance:** large-scale labeled anomaly data are hard or impossible to collect; misclassifying anomalies is normally much more costly than misclassifying normal instances.
- **Diverse types of anomaly** (following [28]):
  - *point anomalies*: individual instances anomalous w.r.t. the majority;
  - *conditional (contextual) anomalies*: anomalous only in a specific context, e.g., "sudden temperature drop/increase in a particular temporal context";
  - *group (collective) anomalies*: a subset anomalous as a whole, whose individual members may not be anomalies.

**Learning settings** (p. 5):

- *Fully supervised*: labeled normal and anomaly training data; often impractical.
- *Unsupervised*: no labeled training data; relies heavily on assumptions about the distribution of anomalies.
- *Semi-supervised*: a set of labeled normal training data. Footnote 1 (p. 5): methods trained on purely normal data, sometimes called unsupervised elsewhere, are called semi-supervised in this survey (following [2, 28]).
- *Weakly supervised*: some labels for anomaly classes, but partial/incomplete, inexact (coarse-grained) or inaccurate.

**The six challenges** (pp. 4–6), "largely unsolved" (p. 4):

| Id | Challenge | Key points (page) |
|---|---|---|
| CH1 | Low anomaly detection recall rate | state-of-the-art methods, especially unsupervised ones, "still often incur high false positives on real-world datasets" (p. 4) |
| CH2 | Anomaly detection in high-dimensional and/or not-independent data | anomalies hidden in high-dimensional spaces; also instances dependent "by temporal, spatial, graph-based and other interdependency relationships" (pp. 4–5) |
| CH3 | Data-efficient learning of normality/abnormality | learning from labeled normal data and a few labeled anomalies; generalizing to anomalies not covered by the labels (p. 5) |
| CH4 | Noise-resilient anomaly detection | noise = mislabeled data or unlabeled anomalies (anomaly-contaminated unlabeled data); the amount of noise varies across datasets (p. 5) |
| CH5 | Detection of complex anomalies | most methods target point anomalies, not conditional/group anomalies; multiple heterogeneous data sources (p. 5) |
| CH6 | Anomaly explanation | black-box detectors in safety-critical domains; possible bias against minority groups (pp. 5–6) |

**Deep vs. traditional methods** (Table 1, p. 6):

| Method | End-to-end optimization | Tailored representation learning | Intricate relation learning | Heterogeneity handling |
|---|---|---|---|---|
| Traditional | × | × | Weak | Weak |
| Deep | ✓ | ✓ | Strong | Strong |
| Challenges | CH1-6 | CH1-6 | CH1, CH2, CH3, CH5 | CH3, CH5 |

## Method

The survey's "method" is its taxonomy (Figure 1, p. 7; Figure 2, p. 8). Three conceptual paradigms (p. 7):

- **Deep learning for feature extraction** (Section 4): deep learning and anomaly scoring "fully separated"; the network is an independent feature extractor (Figure 2(a), p. 8).
- **Learning feature representations of normality** (Section 5): the two modules depend on each other in some form; split by whether existing shallow anomaly measures guide the learning; 7 fine-grained categories (p. 8).
- **End-to-end anomaly score learning** (Section 6): the two modules "fully unified"; 4 subcategories (p. 8).

Challenges each category can address, as given in Figure 1 (p. 7):

| Paradigm | Category | Challenges |
|---|---|---|
| Feature extraction | Deep learning for feature extraction | 1, 2 |
| Normality, generic | Autoencoders | 1, 2, 4, 5 |
| Normality, generic | Generative adversarial networks | 1, 2 |
| Normality, generic | Predictability modeling | 1, 2, 5 |
| Normality, generic | Self-supervised classification | 1, 2, 4 |
| Normality, measure-dependent | Distance-based measures | 1, 2, 3, 4 |
| Normality, measure-dependent | One-class classification measures | 1, 2, 3 |
| Normality, measure-dependent | Clustering-based measures | 1, 2, 4 |
| End-to-end | Ranking models | 1, 2, 3, 4, 6 |
| End-to-end | Prior-driven models | 1, 2, 3, 4 |
| End-to-end | Softmax likelihood models | 1, 2, 5 |
| End-to-end | End-to-end one-class classification | 1, 2 |

### 4. Deep learning for feature extraction (pp. 8–10)

$$\mathbf{z} = \phi(\mathbf{x}; \Theta) \tag{1}$$

with $\phi : \mathcal{X} \mapsto \mathcal{Z}$, $\mathcal{X} \in \mathbb{R}^D$, $\mathcal{Z} \in \mathbb{R}^K$, normally $D \gg K$; an anomaly scoring method $f$ with no connection to $\phi$ is then applied in the new space (p. 8).

- **Assumption** (p. 8): the extracted representations preserve the discriminative information that separates anomalies from normal instances.
- **Two lines** (pp. 8–9): pre-trained models (AlexNet, VGG, ResNet) used as feature extractors, mostly for images and video; or explicitly trained feature extractors (e.g., autoencoders) followed by one-class SVMs or clustering.
- **Advantages** (p. 9): many state-of-the-art (pre-trained) models and off-the-shelf detectors are available; more powerful dimensionality reduction than linear methods; easy to implement.
- **Disadvantages** (p. 9): the fully disjointed feature extraction and scoring "often lead to suboptimal anomaly scores"; pre-trained models are typically limited to specific data types.
- **Challenges targeted** (pp. 9–10): CH2 (lower-dimensional space reveals hidden anomalies), CH1; but the projection may not preserve enough information for detection.

### 5.1 Generic normality feature learning (pp. 10–17)

General framework (p. 10):

$$\{\Theta^*, \mathbf{W}^*\} = \arg\min_{\Theta, \mathbf{W}} \sum_{\mathbf{x} \in \mathcal{X}} \ell\Big(\psi\big(\phi(\mathbf{x}; \Theta); \mathbf{W}\big)\Big) \tag{2}$$

$$s_{\mathbf{x}} = f(\mathbf{x}, \phi_{\Theta^*}, \psi_{\mathbf{W}^*}) \tag{3}$$

where $\psi$ (parameters $\mathbf{W}$) is a surrogate learning task on $\mathcal{Z}$ that enforces learning data regularities, $\ell$ a loss, $f$ a scoring function, $s$ the anomaly score (p. 10). The learning objective "is not primarily designed for anomaly detection" (p. 10).

#### 5.1.1 Autoencoders (pp. 10–12)

- **Assumption** (p. 10): "Normal instances can be better restructured from compressed space than anomalies."
- **Heuristic** (p. 10): representations learn the important regularities to minimize reconstruction error; anomalies are hard to reconstruct and have large reconstruction errors. A bottleneck forces the model to keep information relevant to the dominant (normal) instances.

Formulation (pp. 10–11), encoder $\phi_e$ (parameters $\Theta_e$), decoder $\phi_d$ (parameters $\Theta_d$):

$$\mathbf{z} = \phi_e(\mathbf{x}; \Theta_e), \quad \hat{\mathbf{x}} = \phi_d(\mathbf{z}; \Theta_d) \tag{4}$$

$$\{\Theta_e^*, \Theta_d^*\} = \arg\min_{\Theta_e, \Theta_d} \sum_{\mathbf{x} \in \mathcal{X}} \Big\| \mathbf{x} - \phi_d\big(\phi_e(\mathbf{x}; \Theta_e); \Theta_d\big) \Big\|^2 \tag{5}$$

$$s_{\mathbf{x}} = \Big\| \mathbf{x} - \phi_d\big(\phi_e(\mathbf{x}; \Theta_e^*); \Theta_d^*\big) \Big\|^2 \tag{6}$$

The encoder and decoder can share weights to reduce parameters and regularize learning (p. 11).

- **Regularized variants** (p. 11): sparse AE (e.g., keeping the top-$K$ most active hidden units), denoising AE (reconstruct from corrupted inputs), contractive AE (penalty on the Frobenius norm of the encoder's Jacobian), variational AE (prior distribution over the latent space).
- **Representative methods** (p. 11): Replicator neural network (first reconstruction-based detector, tabular data, three-hidden-layer MLP); RandNet (ensemble of AEs with random constant dropout connections, tabular); "The idea of autoencoder ensembles is extended to time series data in Reference [71]"; RDA (robust-PCA-inspired split into a normal set and an anomaly set, with an $\ell_1$ or $\ell_{2,1}$ penalty).
- **Two adaptations to complex data** (pp. 11–12):
  1. adapt the architecture to the input type: CNN-AE, LSTM-AE [96], Conv-LSTM-AE [92], graph convolutional AE;
  2. learn AE representations first, then learn to predict them: e.g., [91] combines a denoising AE (two hidden layers) for multidimensional inputs at each time step with an RNN (single hidden layer) that predicts those representations, for multivariate sequence data; [97] does similarly for acoustic anomalies with bidirectional LSTMs.
- **Advantages** (p. 12): straightforward and generic to data types; many powerful AE variants usable.
- **Disadvantages** (p. 12): (i) representations "can be biased by infrequent regularities and the presence of outliers or anomalies in the training data"; (ii) the reconstruction objective targets dimension reduction or compression, not anomaly detection, so representations are "a generic summarization of underlying regularities".
- **Challenges targeted** (p. 12): CH2 (high-dimensional and non-independent data, including "multivariate sequence data [91, 97]"); CH1; CH4 only with RPCA-like robustness, since "AEs are generally vulnerable to data noise presented in the training data".

#### 5.1.2 Generative adversarial networks (pp. 12–14)

- **Assumption** (p. 12): normal instances can be better generated than anomalies from the generator's latent space.
- **AnoGAN** (pp. 12–13): standard GAN training,

  $$\min_G \max_D V(D, G) = \mathbb{E}_{\mathbf{x} \sim p_{\mathcal{X}}}\big[\log D(\mathbf{x})\big] + \mathbb{E}_{\mathbf{z} \sim p_{\mathcal{Z}}}\Big[\log\Big(1 - D\big(G(\mathbf{z})\big)\Big)\Big] \tag{7}$$

  then, for each $\mathbf{x}$, a gradient search for $\mathbf{z}$ (GAN fixed) with the residual and feature-matching losses ($\gamma$ is the search step, $h$ an intermediate discriminator layer):

  $$\ell_R(\mathbf{x}, \mathbf{z}_\gamma) = \big\|\mathbf{x} - G(\mathbf{z}_\gamma)\big\|_1 \tag{8}$$

  $$\ell_{fm}(\mathbf{x}, \mathbf{z}_\gamma) = \Big\|h(\mathbf{x}) - h\big(G(\mathbf{z}_\gamma)\big)\Big\|_1 \tag{9}$$

  $$s_{\mathbf{x}} = (1 - \alpha)\,\ell_R(\mathbf{x}, \mathbf{z}_{\gamma^*}) + \alpha\,\ell_{fm}(\mathbf{x}, \mathbf{z}_{\gamma^*}) \tag{10}$$

- **EBGAN** (p. 13), built on BiGAN with an encoder $E$:

  $$\min_{G,E} \max_D \; \mathbb{E}_{\mathbf{x} \sim p_{\mathcal{X}}}\Big[\mathbb{E}_{\mathbf{z} \sim p_E(\cdot|\mathbf{x})} \log\big[D(\mathbf{x}, \mathbf{z})\big]\Big] + \mathbb{E}_{\mathbf{z} \sim p_{\mathcal{Z}}}\Big[\mathbb{E}_{\mathbf{x} \sim p_G(\cdot|\mathbf{z})}\big[\log\big(1 - D(\mathbf{x}, \mathbf{z})\big)\big]\Big] \tag{11}$$

  $$s_{\mathbf{x}} = (1 - \alpha)\,\ell_G(\mathbf{x}) + \alpha\,\ell_D(\mathbf{x}) \tag{12}$$

  with $\ell_G(\mathbf{x}) = \|\mathbf{x} - G(E(\mathbf{x}))\|_1$ and $\ell_D(\mathbf{x}) = \|h(\mathbf{x}, E(\mathbf{x})) - h(G(E(\mathbf{x})), E(\mathbf{x}))\|_1$; no iterative search for $\mathbf{z}$. ALAD extends it with two more discriminators (p. 13).
- **GANomaly** (p. 13): encoder-decoder-encoder generator $\mathbf{x} \xrightarrow{G_E} \mathbf{z} \xrightarrow{G_D} \hat{\mathbf{x}} \xrightarrow{E} \hat{\mathbf{z}}$:

  $$\ell_{fm} = \mathbb{E}_{\mathbf{x} \sim p_{\mathcal{X}}}\big\|h(\mathbf{x}) - h\big(G(\mathbf{x})\big)\big\|_2 \tag{13}$$

  $$\ell_{con} = \mathbb{E}_{\mathbf{x} \sim p_{\mathcal{X}}}\big\|\mathbf{x} - G(\mathbf{x})\big\|_1 \tag{14}$$

  $$\ell_{enc} = \mathbb{E}_{\mathbf{x} \sim p_{\mathcal{X}}}\big\|G_E(\mathbf{x}) - E\big(G(\mathbf{x})\big)\big\|_2 \tag{15}$$

  $$\ell = \alpha\,\ell_{fm} + \beta\,\ell_{con} + \gamma\,\ell_{enc} \tag{16}$$

  $$s_{\mathbf{x}} = \big\|G_E(\mathbf{x}) - E\big(G(\mathbf{x})\big)\big\|_1 \tag{17}$$

- **Advantages** (p. 14): GANs generate realistic instances, especially images; many GAN models and theories can be adapted.
- **Disadvantages** (p. 14): training problems (failure to converge, mode collapse); the generator can produce instances outside the normal manifold, especially with complex distributions or "unexpected outliers" in training data; scores built on a data-synthesis objective can be suboptimal.
- **Challenges targeted** (p. 14): CH2, CH1.

#### 5.1.3 Predictability modeling (pp. 14–15)

- **Idea** (p. 14): learn representations by predicting the current instances from the representations of previous instances in a temporal window; normal instances adhere to temporal/sequential dependencies and are well predicted, anomalies violate them, so "the prediction errors can be used to define the anomaly scores".
- **Assumption** (p. 14): "Normal instances are temporally more predictable than anomalies."
- **Future frame prediction** (p. 14, from [86], video): given frames $\mathbf{x}_1, \dots, \mathbf{x}_t$, predict $\hat{\mathbf{x}}_{t+1}$:

  $$\alpha\,\ell_{pred}\big(\hat{\mathbf{x}}_{t+1}, \mathbf{x}_{t+1}\big) + \beta\,\ell_{adv}\big(\hat{\mathbf{x}}_{t+1}\big) \tag{18}$$

  with $\hat{\mathbf{x}}_{t+1} = \psi\big(\phi(\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_t; \Theta); \mathbf{W}\big)$; $\ell_{pred}$ a mean-squared-error prediction loss (in [86], three losses on intensity, gradient and optical flow), $\ell_{adv}$ an adversarial loss; $\psi$ is a U-Net. The anomaly score is a normalized Peak Signal-to-Noise Ratio of the prediction difference $\|\mathbf{x}_i - \hat{\mathbf{x}}_i\|_2$ (p. 14). [167] adds an autoencoder-based reconstruction network (pp. 14–15).
- **Autoregressive latent density** (p. 15, from [1]): with $\mathbf{z} = \phi(\mathbf{x}; \Theta)$,

  $$p(\mathbf{z}) = \prod_{j=1}^{K} p(z_j \mid z_{1:j-1}) \tag{19}$$

  $$L = \mathbb{E}_{\mathbf{x}}\Big[\big\|\mathbf{x} - \phi_d\big(\phi_e(\mathbf{x}; \Theta_e); \Theta_d\big)\big\|_2 - \lambda \log\big(\psi(\mathbf{z}; \mathbf{W})\big)\Big] \tag{20}$$

  The first term is a reconstruction error "measured by MSE" (printed with an unsquared $\|\cdot\|_2$, as transcribed), the second an autoregressive log-likelihood; at evaluation the two are combined into the anomaly score (p. 15).
- **Advantages** (p. 15): sequence learning techniques can be incorporated; different temporal and spatial dependencies can be learned.
- **Disadvantages** (p. 15): "limited to anomaly detection in sequence data"; sequential predictions "can be computationally expensive"; the objective is sequential prediction, not anomaly detection, so representations may be suboptimal.
- **Challenges targeted** (p. 15): CH1 and CH2 (false positives in high-dimensional and/or temporal data); CH5, "temporal context-based conditional anomalies", since predictions are conditioned on elapsed instances.

#### 5.1.4 Self-supervised classification (pp. 15–17)

- **Assumption** (p. 16): normal instances are more consistent with self-supervised classifiers than anomalies.
- **Formulation** (p. 16, from [48]): train a multi-class classifier to recognize which transformation $T_j$ (flips, translations, rotations) was applied:

  $$L_{cons} = CE\Big(\psi\big(\mathbf{z}_{T_j}; \mathbf{W}\big), \mathbf{y}_{T_j}\Big) \tag{21}$$

  with $\mathbf{z}_{T_j} = \phi(T_j(\mathbf{x}); \Theta)$ and $\mathbf{y}_{T_j}$ the one-hot synthetic class; the anomaly score aggregates classification scores over all $T_j$ (Dirichlet in [48]; "a simple average ... also works well").
- In the unsupervised setting [157], the negative entropy over prediction probabilities generally performed better than the average or maximum prediction probability as anomaly score (p. 16).
- **Advantages** (p. 16): works in unsupervised and semi-supervised settings; scoring grounded in gradient-magnitude properties.
- **Disadvantages** (p. 16): transformations are data dependent and "applicable to image data only"; scores derived from classification scores rather than optimized directly.
- **Challenges targeted** (pp. 16–17): CH1, CH2, CH4.

### 5.2 Anomaly measure-dependent feature learning (pp. 17–21)

General framework (p. 17), $f$ an existing anomaly scoring measure on the representation space, with or without trainable $\mathbf{W}$:

$$\{\Theta^*, \mathbf{W}^*\} = \arg\min_{\Theta, \mathbf{W}} \sum_{\mathbf{x} \in \mathcal{X}} \ell\Big(f\big(\phi(\mathbf{x}; \Theta); \mathbf{W}\big)\Big) \tag{22}$$

$$s_{\mathbf{x}} = f\big(\phi(\mathbf{x}; \Theta^*); \mathbf{W}^*\big) \tag{23}$$

#### 5.2.1 Distance-based measure (pp. 17–18)

- **Assumption** (p. 17): anomalies lie far from their closest neighbors; normal instances lie in dense neighborhoods.
- **REPEN** (p. 17, [112]): hinge loss over pseudo-labeled anomalies $\mathcal{A}$ and normal instances $\mathcal{N}$ (from off-the-shelf detectors), with a random subsample $\mathcal{S}$:

  $$L_{query} = \frac{1}{|\mathcal{X}|} \sum_{\mathbf{x} \in \mathcal{A}, \mathbf{x}' \in \mathcal{N}} \max\big\{0, m + f(\mathbf{x}', \mathcal{S}; \Theta) - f(\mathbf{x}, \mathcal{S}; \Theta)\big\} \tag{24}$$

  $$f(\mathbf{x}, \mathcal{S}; \Theta) = \min_{\mathbf{x}' \in \mathcal{S}} \big\|\phi(\mathbf{x}; \Theta), \phi(\mathbf{x}'; \Theta)\big\|_2 \tag{25}$$

  (Eq. 25 is printed with a comma inside the norm.)
- **RDP** (p. 18, [155]): distance between optimized and randomly projected representations of the same instance, $\phi'$ a fixed random network:

  $$\Theta^* = \arg\min_{\Theta} \sum_{\mathbf{x} \in \mathcal{X}} f\big(\phi(\mathbf{x}; \Theta), \phi'(\mathbf{x})\big) \tag{26}$$

- **Advantages** (p. 18): well-defined, theoretically supported measures; work in low-dimensional spaces where traditional distance measures fail; tailored representations.
- **Disadvantages** (p. 18): extensive computation of most distance measures; limited by the measures' inherent weaknesses.
- **Challenges targeted** (p. 18): CH1, CH2, CH3, CH4.

#### 5.2.2 One-class classification-based measure (pp. 18–20)

- **Assumption** (p. 19): "All normal instances come from a single (abstract) class and can be summarized by a compact model, to which anomalies do not conform."
- **Deep one-class SVM** (p. 19), $\mathbf{z} = \phi(\mathbf{x}; \Theta)$:

  $$\min_{r, \Theta, \mathbf{w}} \frac{1}{2}\|\Theta\|^2 + \frac{1}{\upsilon N} \sum_{i=1}^{N} \max\big\{0, r - \mathbf{w}^\intercal \mathbf{z}_i\big\} - r \tag{27}$$

  $r$ the margin, $\upsilon$ an upper bound on the fraction of anomalies in training data; instances with $r - \mathbf{w}^\intercal \mathbf{z}_i > 0$ are anomalies.
- **SVDD** (p. 19):

  $$\min_{r, \mathbf{c}, \xi} r^2 + \frac{1}{\upsilon N} \sum_{i=1}^{N} \xi_i \tag{28}$$

  $$\text{s.t. } \|\Phi(\mathbf{x}_i) - \mathbf{c}\|^2 \le r^2 + \xi_i, \; \xi_i \ge 0, \; \forall i \tag{29}$$

- **Deep SVDD** (p. 19), unsupervised setting (small contamination assumed):

  $$\min_{r, \Theta} r^2 + \frac{1}{\upsilon N} \sum_{i=1}^{N} \max\{0, \|\phi(\mathbf{x}_i; \Theta) - \mathbf{c}\|^2 - r^2\} + \frac{\lambda}{2}\|\Theta\|^2 \tag{30}$$

  semi-supervised setting (printed without a summation over $i$):

  $$\min_{\Theta} \frac{1}{N}\|\phi(\mathbf{x}_i; \Theta) - \mathbf{c}\|^2 + \frac{\lambda}{2}\|\Theta\|^2 \tag{31}$$

  A trainable $\mathbf{c}$ in Eq. 31 can lead to trivial solutions; $\mathbf{c}$ can be fixed to the mean of the representations from an initial forward pass (p. 20). Deep SAD adds $\sum_{j=1}^{M} \big(\|\phi(\mathbf{x}'_j; \Theta) - \mathbf{c}\|^2\big)^{y_j}$ for labeled instances, $y_j = +1$ normal, $-1$ otherwise (p. 20).
- **Advantages** (p. 20): well-studied foundation; representation and one-class model learned jointly; no manual kernel choice.
- **Disadvantages** (p. 20): may work ineffectively with "complex distributions within the normal class"; performance depends on the one-class measure.
- **Challenges targeted** (p. 20): CH1, CH2, CH3.

#### 5.2.3 Clustering-based measure (pp. 20–21)

- **Assumption** (p. 20): normal instances adhere more strongly to clusters than anomalies.
- **Deep clustering loss** (pp. 20–21):

  $$\alpha\,\ell_{clu}\Big(f\big(\phi(\mathbf{x}; \Theta); \mathbf{W}\big), y_x\Big) + \beta\,\ell_{aux}(\mathcal{X}) \tag{32}$$

  $\ell_{clu}$ a clustering loss (k-means, spectral, agglomerative, GMM), $y_x$ pseudo labels from clustering, $\ell_{aux}$ often an autoencoder reconstruction loss (p. 21). DAGMM-type methods [83, 179] use a GMM loss plus reconstruction loss and concatenate handcrafted reconstruction-error features with the AE features (p. 21).
- **Disadvantages** (p. 21): detection depends heavily on clustering results; clustering may be biased by contaminating anomalies. Without contamination, these methods suit the semi-supervised setting; unsupervised use needs extra constraints (p. 21).
- **Challenges targeted** (p. 21): CH1, CH2, CH4.

### 6. End-to-end anomaly score learning (pp. 21–28)

General framework (p. 22), $\tau(\cdot; \Theta) : \mathcal{X} \mapsto \mathbb{R}$:

$$\Theta^* = \arg\min_{\Theta} \sum_{\mathbf{x} \in \mathcal{X}} \ell\big(\tau(\mathbf{x}; \Theta)\big) \tag{33}$$

$$s_{\mathbf{x}} = \tau(\mathbf{x}; \Theta^*) \tag{34}$$

#### 6.1 Ranking models (pp. 22–24)

- **Assumption** (p. 22): an observable ordinal variable captures some data abnormality.
- **SDOR** (p. 22, [117], unsupervised video): two-class ordinal regression on pseudo labels, $y_{\mathbf{x}} = c_1$ for $\mathcal{A}$, $c_2$ for $\mathcal{N}$, $c_1 > c_2$, MSE/MAE loss:

  $$\arg\min_{\Theta} \sum_{\mathbf{x} \in \mathcal{G}} \ell\big(\tau(\mathbf{x}; \Theta), y_{\mathbf{x}}\big) \tag{35}$$

- **PReNet** (p. 23, [114], weakly supervised): pairwise relation prediction with synthetic ordinal labels $y_{\mathbf{x}_{a_i}\mathbf{x}_{a_j}} > y_{\mathbf{x}_{a_i}\mathbf{x}_{u_i}} > y_{\mathbf{x}_{u_i}\mathbf{x}_{u_j}}$:

  $$\Theta^* = \arg\min_{\Theta} \frac{1}{|\mathcal{P}|} \sum_{\{\mathbf{x}_i, \mathbf{x}_j, y_{ij}\} \in \mathcal{P}} \Big| y_{\mathbf{x}_i \mathbf{x}_j} - \tau\big((\mathbf{x}_i, \mathbf{x}_j); \Theta\big) \Big| \tag{36}$$

- **MIL ranking** (p. 23, [145], video-level labels only), positive bags $\mathcal{B}_p$, negative bags $\mathcal{B}_n$:

  $$\arg\min_{\Theta} \sum_{\mathcal{B}_p, \mathcal{B}_n \in \mathcal{X}} \max\Big\{0, 1 - \max_{\mathbf{x} \in \mathcal{B}_p} \tau(\mathbf{x}; \Theta) + \max_{\mathbf{x} \in \mathcal{B}_n} \tau(\mathbf{x}; \Theta)\Big\} + \lambda_1 \sum_{i=1}^{|\mathcal{B}_p|} \big(\tau(\mathbf{x}_i; \Theta) - \tau(\mathbf{x}_{i+1}; \Theta)\big)^2 + \lambda_2 \sum_{\mathbf{x} \in \mathcal{B}_p} \tau(\mathbf{x}; \Theta) \tag{37}$$

  The second term enforces score smoothness between consecutive segments; the third, anomaly sparsity (p. 23).
- **Disadvantages** (p. 24): need some form of labeled anomalies; may not generalize to unseen anomalies.
- **Challenges targeted** (p. 24): CH1, CH2, CH3, CH4, CH6 (explanation by backpropagating activations or gradients of scores).

#### 6.2 Prior-driven models (pp. 24–25)

- **Assumption** (p. 24): "The imposed prior captures the underlying (ab)normality of the dataset."
- **Bayesian IRL on sequences** (p. 24, [107], PUP): an agent's normal behavior is captured by its latent reward function; a test sequence with low reward is an anomaly:

  $$\max_{\Theta} \mathbb{E}_{\mathbf{s} \sim \mathcal{S}}\big[\log p(\mathbf{s}|\Theta) + \log p(\Theta)\big] \tag{38}$$

  with $p(\mathbf{s}|\Theta) = \frac{1}{Z}\exp\big(\sum_{(o,a) \in \mathbf{s}} \tau_\Theta(o, a)\big)$, Gaussian prior $\Theta \sim \mathcal{N}(0, \sigma^2)$, and

  $$Z = \mathbb{E}_{\mathbf{s} \sim \pi}\Big[\sum_{(o,a) \in \mathbf{s}} \tau_\Theta(o, a)\Big] \tag{39}$$

  The inverse of the reward is the anomaly score (p. 24).
- **Deviation loss** (p. 25, [115], DevNet), Gaussian prior on anomaly scores:

  $$L_{dev} = (1 - y_{\mathbf{x}})\,|dev(\mathbf{x})| + y_{\mathbf{x}} \max\{0, m - dev(\mathbf{x})\} \quad \text{and} \quad dev(\mathbf{x}) = \frac{\tau(\mathbf{x}; \Theta) - \mu_b}{\sigma_b} \tag{40}$$

  $\mu_b, \sigma_b$ estimated from values drawn from $\mathcal{N}(\mu, \sigma)$ per batch; $m$ a Z-score confidence parameter; scores interpretable via $\mu \pm z_p \sigma$ (p. 25).
- **Disadvantages** (p. 25): hard to design a universally effective prior; less effective if the prior does not fit.
- **Challenges targeted** (p. 25): CH1, CH2 ("high-dimensional data and sequential data"), CH3, CH4.

#### 6.3 Softmax likelihood models (pp. 25–26)

- **Assumption** (p. 26): anomalies and normal instances are respectively low- and high-probability events.
- **APE** (p. 26, [30]):

  $$\Theta^* = \arg\max_{\Theta} \sum_{\mathbf{x} \in \mathcal{X}} \log p(\mathbf{x}; \Theta) \tag{41}$$

  $$p(\mathbf{x}; \Theta) = \frac{\exp\big(\tau(\mathbf{x}; \Theta)\big)}{\sum_{\mathbf{x} \in \mathcal{X}} \exp\big(\tau(\mathbf{x}; \Theta)\big)} \tag{42}$$

  $$\tau(\mathbf{x}; \Theta) = \sum_{i,j \in \{1, 2, \dots, K\}} w_{ij} \mathbf{z}_i \mathbf{z}_j \tag{43}$$

  trained with noise contrastive estimation, $k$ noise samples $\mathbf{x}'_{1,\dots,k} \sim Q$:

  $$\log p(d = 1|\mathbf{x}; \Theta) + \log \sum_{j=1}^{k} p(d = 0|\mathbf{x}'_j; \Theta) \tag{44}$$

  with $p(d = 1|\mathbf{x}; \Theta) = \frac{\exp(\tau(\mathbf{x};\Theta))}{\exp(\tau(\mathbf{x};\Theta)) + kQ(\mathbf{x}')}$ and $p(d = 0|\mathbf{x}'; \Theta) = \frac{kQ(\mathbf{x}')}{\exp(\tau(\mathbf{x};\Theta)) + kQ(\mathbf{x}')}$ (p. 26).
- **Disadvantages** (p. 26): $O(D^n)$ time per instance for $n$th-order interactions of $D$ features; heavy dependence on negative-sample generation.
- **Challenges targeted** (p. 26): CH2, CH5, CH1.

#### 6.4 End-to-end one-class classification (pp. 27–28)

- **Assumptions** (p. 27): (i) instances approximating anomalies can be synthesized; (ii) all normal instances can be summarized by a discriminative one-class model.
- **Differences from 5.1.2** (p. 27): the discriminator itself is the scorer ($D$ acts as $\tau$ in Eq. 33), instead of a residual between real and generated instances.
- **ALOCC** (p. 27, [135]), with a denoising AE generator, $\hat{\mathbf{x}} = \mathbf{x} + \mathbf{n}$, $\mathbf{n} \sim \mathcal{N}(0, \sigma^2\mathbf{I})$:

  $$\min_{AE} \max_D V(D, G) = \mathbb{E}_{\mathbf{x} \sim p_{\mathcal{X}}}\big[\log D(\mathbf{x})\big] + \mathbb{E}_{\hat{\mathbf{x}} \sim p_{\hat{\mathcal{X}}}}\Big[\log\Big(1 - D\big(AE(\hat{\mathbf{x}})\big)\Big)\Big] \tag{45}$$

  $$\ell_{ae} = \|\mathbf{x} - AE(\hat{\mathbf{x}})\|^2 \tag{46}$$

- **OCAN** (p. 28, [174]), complement generator (bad GAN):

  $$\min_G -\mathcal{H}(p_{\mathcal{Z}}) + \mathbb{E}_{\hat{\mathbf{z}} \sim p_{\mathcal{Z}}} \log p_{\mathcal{X}}(\hat{\mathbf{z}})\,\mathbb{I}[p_{\mathcal{X}}(\hat{\mathbf{z}}) > \epsilon] + \|\mathbb{E}_{\hat{\mathbf{z}} \sim p_{\mathcal{Z}}} h(\hat{\mathbf{z}}) - \mathbb{E}_{\mathbf{z} \sim p_{\mathcal{X}}} h(\mathbf{z})\|_2 \tag{47}$$

  $$\max_D \mathbb{E}_{\mathbf{x} \sim p_{\mathcal{X}}}\big[\log D(\mathbf{z})\big] + \mathbb{E}_{\hat{\mathbf{z}} \sim p_{\mathcal{Z}}}\big[\log\big(1 - D(\hat{\mathbf{z}})\big)\big] + \mathbb{E}_{\mathbf{x} \sim p_{\mathcal{X}}}\big[D(\mathbf{x}) \log D(\mathbf{x})\big] \tag{48}$$

  (As printed, p. 28: the first expectation is over $\mathbf{x}$ but its argument is $D(\mathbf{z})$.)

- **Fence GAN** (p. 28, [103]), $\alpha \in (0, 1)$, $\boldsymbol{\mu}$ the center of generated instances (encirclement loss + dispersion loss):

  $$\min_G \mathbb{E}_{\mathbf{z} \sim p_{\mathcal{Z}}}\Big[\log\big[\big|\alpha - D\big(G(\mathbf{z})\big)\big|\big]\Big] + \beta \frac{1}{\mathbb{E}_{\mathbf{z} \sim p_{\mathcal{Z}}}\|G(\mathbf{z}) - \boldsymbol{\mu}\|_2} \tag{49}$$

- **Disadvantages** (p. 28): generated reference instances may not resemble unknown anomalies; GAN instability makes performance "fluctuate drastically in different training steps" ([169]); limited to semi-supervised scenarios.
- **Challenges targeted** (p. 28): CH1, CH2.

## Experimental setup

None: the survey runs no experiments of its own. It notes that the methods "are evaluated on diverse datasets", which prevents a universal meta-analysis of their empirical performance (pp. 28–29).

**Our reading:** the survey defines no evaluation metrics (no AUROC, AUPRC, F1 or point-adjust protocol) and gives no threshold-selection procedure; the only score definitions are the per-method anomaly scores above. Metrics and protocols for time-series anomaly detection must come from other papers.

## Results

**Key characteristics of 30 representative algorithms** (Table 2, p. 29). DA, DP, PT = data augmentation, dropout, pre-training; "# layers" counts all layers except the input layer; lReLU = leaky ReLU (p. 29):

| Method | Ref. (Section) | Sup. | Objective | DA | DP | PT | Archit. | Activation | # layers | Loss | Data |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OADA | [65] (4) | Semi | Reconstruction | Yes | No | No | AE | ReLU | 3 | MSE | Video |
| Replicator | [57] (5.1.1) | Unsup. | Reconstruction | No | No | No | AE | Tanh | 2 | MSE | Tabular |
| RandNet | [29] (5.1.1) | Unsup. | Reconstruction | No | Yes | Yes | AE | ReLU | 3 | MSE | Tabular |
| RDA | [175] (5.1.1) | Semi | Reconstruction | No | No | No | AE | Sigmoid | 2 | MSE | Tabular |
| UODA | [91] (5.1.1) | Semi | Reconstruction | No | No | Yes | AE & RNN | Sigmoid | 4 | MSE | Sequence |
| AnoGAN | [138] (5.1.2) | Semi | Generative | No | No | No | Conv. | ReLU | 4 | MAE | Image |
| EBGAN | [170] (5.1.2) | Semi | Generative | No | No | No | Conv. & MLP | ReLU/lReLU | 3-4 | GAN | Image & Tabular |
| FFP | [86] (5.1.3) | Semi | Predictive | Yes | No | Yes | Conv. | ReLU | 10 | MAE/MSE | Video |
| LSA | [1] (5.1.3) | Semi | Predictive | No | No | No | Conv. | lReLU | 4-7 | MSE & KL | video |
| GT | [48] (5.1.4) | Semi | Classification | Yes | Yes | No | Conv. | ReLU | 10-16 | CE | Image |
| E³Outlier | [157] (5.1.4) | Semi | Classification | Yes | Yes | No | Conv. | ReLU | 10 | CE | Image |
| REPEN | [112] (5.2.1) | Unsup. | Distance | No | No | No | MLP | ReLU | 1 | Hinge | Tabular |
| RDP | [155] (5.2.1) | Unsup. | Distance | No | No | No | MLP | lReLU | 1 | MSE | Tabular |
| AE-1SVM | [104] (5.2.2) | Unsup. | One-class | No | No | No | AE & Conv. | Sigmoid | 2-5 | Hinge | Tabular & image |
| DeepOC | [161] (5.2.2) | Semi | One-class | No | No | No | 3D Conv. | ReLU | 5 | Hinge | Video |
| Deep SVDD | [132] (5.2.2) | Semi | One-class | No | No | Yes | Conv. | lReLU | 3-4 | Hinge | Image |
| Deep SAD | [133] (5.2.2) | Semi | One-class | No | No | Yes | Conv. & MLP | lReLU | 3-4 | Hinge | Image & Tabular |
| DEC | [162] (5.2.3) | Unsup. | Clustering | No | Yes | Yes | MLP | ReLU | 4 | KL | Image & Tabular |
| DAGMM | [179] (5.2.3) | Unsup. | Clustering | No | Yes | No | AE & MLP | Tanh | 4-6 | Likelihood | Tabular |
| SDOR | [117] (6.1) | Unsup. | Anomaly scores | No | No | Yes | ResNet & MLP | ReLU | 50 + 2 | MAE | Video |
| PReNet | [114] (6.1) | Weak | Anomaly scores | Yes | No | No | MLP | ReLU | 2-4 | MAE | Tabular |
| MIL | [145] (6.1) | Weak | Anomaly scores | No | Yes | Yes | 3DConv. & MLP | ReLU | 18/34 + 3 | Hinge | Video |
| PUP | [107] (6.2) | Unsup. | Anomaly scores | No | No | No | MLP | ReLU | 3 | Likelihood | Sequence |
| DevNet | [115] (6.2) | Weak | Anomaly scores | No | No | No | MLP | ReLU | 2-4 | Deviation | Tabular |
| APE | [30] (6.3) | Unsup. | Anomaly scores | No | No | No | MLP | Sigmoid | 3 | Softmax | Tabular |
| AEHE | [45] (6.3) | Unsup. | Anomaly scores | No | No | No | AE & MLP | ReLU | 4 | Softmax | Graph |
| ALOCC | [135] (6.4) | Semi | Anomaly scores | Yes | No | No | AE & CNN | lReLU | 5 | GANs | Image |
| OCAN | [174] (6.4) | Semi | Anomaly scores | No | No | Yes | LSTM-AE & MLP | ReLU | 4 | GANs | Sequence |
| Fence GAN | [103] (6.4) | Semi | Anomaly scores | No | Yes | No | Conv. & MLP | lReLU/Sigmoid | 4-5 | GANs | Image & Tabular |
| OCGAN | [120] (6.4) | Semi | Anomaly scores | No | No | No | Conv. | ReLU/Tanh | 3 | GANs | Image |

**Observations on Table 2** (p. 29), as stated:

- most methods operate in an unsupervised or semi-supervised mode;
- data augmentation, dropout and pre-training are under-explored;
- networks are not deep: "a majority of the methods having no more than five network layers";
- (leaky) ReLU is the most popular activation;
- diverse backbones handle different input types.

**21 publicly accessible real-world datasets with real anomalies** (Table 3, p. 30). Datasets converted from classification data "may fail to reflect the performance of the methods in real-world anomaly detection applications" (p. 29); only large-scale and/or high-dimensional complex datasets are included (pp. 29–30):

| Domain | Data | Size | Dimension | Anomaly (%) | Type | Reference |
|---|---|---|---|---|---|---|
| Intrusion detection | KDD Cup 99 [13] | 4,091-567,497 | 41 | 0.30%-7.70% | Tabular | [57, 103, 104, 179] |
| Intrusion detection | UNSW-NB15 [100] | 257,673 | 49 | ≤9.71% | Streaming | [114, 115] |
| Excitement prediction | KDD Cup 14 | 619,326 | 10 | 6.00% | Tabular | [114, 115] |
| Dropout prediction | KDD Cup 15 | 35,091 | 27 | 0.10%-0.40% | Sequence | [91] |
| Malicious URLs detection | URL [93] | 2.4m | 3.2m | 33.04% | Streaming | [112] |
| Spam detection | Webspam [160] | 350,000 | 16.6m | 39.61% | Tabular/text | [112] |
| Fraud detection | Credit-card-fraud [34] | 284,807 | 30 | 0.17% | Streaming | [114, 115, 174] |
| Vandal detection | UMDWikipedia [76] | 34,210 | N/A | 50.00% | Sequence | [174] |
| Mutant activity detection | p53 Mutants [13] | 16,772 | 5,408 | 0.48% | Tabular | [112] |
| Internet ads detection | AD [13] | 3,279 | 1,555 | 14.00% | Tabular | [112] |
| Disease detection | Thyroid [13] | 7,200 | 21 | 7.40% | Tabular | [114, 115, 133, 179] |
| Disease detection | Arrhythmia [13] | 452 | 279 | 14.60% | Tabular | [116, 133, 179] |
| Defect detection | MVTec AD | 5,354 | N/A | 35.26% | Image | [15] |
| Video surveillance | UCSD Ped 1 [81] | 14,000 frames | N/A | 28.6% | Video | [117, 161] |
| Video surveillance | UCSD Ped 2 [81] | 4,560 frames | N/A | 35.9% | Video | [117, 161] |
| Video surveillance | UMN [106] | 7,739 frames | N/A | 15.5%-18.1% | Video | [117] |
| Video surveillance | Avenue [90] | 30,652 frames | N/A | 12.46% | Video | [161] |
| Video surveillance | ShanghaiTech Campus | 317,398 frames | N/A | 5.38% | Video | [86] |
| Video surveillance | UCF-Crime | 1,900 videos (13.8m frames) | N/A | 13 crimes | Video | [145] |
| System log analysis | HDFS Log [164] | 11.2m | N/A | 2.90% | Sequence | [40] |
| System log analysis | OpenStack log | 1.3m | N/A | 7.00% | Sequence | [40] |

**Future opportunities** (Section 8, pp. 30–33):

- **8.1 Anomaly-supervisory signals** (p. 30): generic self-/unsupervised objectives are "not optimized specifically for anomaly detection"; explore "new sources of anomaly-supervisory signals" beyond reconstruction and GANs, with weak assumptions on the anomaly distribution; domain-driven anomaly detection.
- **8.2 Deep weakly supervised detection** (pp. 30–31): use a few labeled anomalies; *unknown anomaly detection* (generalize beyond the labeled anomalies); *data-efficient / few-shot anomaly detection*; deeper architectures; learning from inexact/inaccurate labels.
- **8.3 Large-scale normality learning** (p. 31): pre-train transferable representations on large unlabeled data, then fine-tune in semi-supervised mode; precautions against anomaly contamination, "because most methods in Section 5 implicitly assume that the training data are clean"; robustness needed in both pre-training and fine-tuning; normality learning "may need to be domain/application specific".
- **8.4 Complex anomalies** (pp. 31–32): deep models for conditional/group anomalies "significantly less explored"; multimodal anomaly detection "largely unexplored".
- **8.5 Interpretable and actionable detection** (p. 32): model-agnostic explanation is weaker than inherently explainable deep detectors.
- **8.6 Novel applications and settings** (pp. 32–33): OOD detection (which assumes fine-grained normal class labels); curiosity learning in reinforcement learning; non-IID anomaly detection; adversarial examples, anti-spoofing, early detection of rare catastrophic events.

## Assumptions and limitations

What the survey states itself:

- **Every category rests on an explicit assumption** (listed per category above, pp. 8–28); e.g., reconstruction-based methods assume normal instances reconstruct better (p. 10), predictability methods that normal instances are "temporally more predictable" (p. 14).
- **Clean training data:** "most methods in Section 5 implicitly assume that the training data are clean and do not contain any noise/anomaly instances" (p. 31); AEs can memorize training noise, giving "small reconstruction errors of anomalies" (p. 12).
- **Generic objectives are not detection objectives:** reconstruction (p. 12), GAN synthesis (p. 14), sequential prediction (p. 15) and self-supervised classification (p. 16) all optimize something other than anomaly detection.
- **No performance meta-analysis:** methods are evaluated on diverse datasets (pp. 28–29).
- **Benchmarks converted from classification data** may not reflect real-world performance (p. 29).

**Our reading:**

- The survey is broad but light on time series: the only time-series-specific items are the temporal context of conditional anomalies (p. 4), temporal dependence in CH2 (p. 5), the sequence adaptations of AEs (pp. 11–12), predictability modeling (pp. 14–15, illustrated mostly with video), UODA, PUP and OCAN on sequences (Table 2, p. 29) and four "Sequence" datasets in Table 3 (p. 30). None of the common multivariate time-series benchmarks (e.g., sensor or server-machine datasets) appear in Table 3.
- Forecasting is treated only as a means to score anomalies (prediction error), not as a task in its own right.
- Continual or incremental learning, distribution shift over time and model merging are not discussed; the nearest topics are OOD detection (p. 32) and large-scale pre-training then fine-tuning (p. 31).
- The taxonomy is counted as "11 fine-grained categories" (p. 2, p. 7; "11 different modeling perspectives", p. 3) but Section 8 says "12 diverse modeling perspectives" (p. 30); the figure lists 11 leaf categories plus the feature-extraction category, which may explain the 12.
- Section 8.3 refers to "self-supervised classification-based methods in Section 5.1.3" (p. 31), while self-supervised classification is Section 5.1.4 (p. 15); likely a cross-reference slip.

## Relevance to this thesis

**Our reading:**

- **Vocabulary and settings.** The survey's definitions fix our terms: point, conditional (contextual) and group (collective) anomalies (p. 4); and "semi-supervised" for training on normal data only (p. 5, footnote 1). Our time-series detectors trained on normal windows are semi-supervised in this sense.
- **The two families we are most likely to use** are reconstruction (autoencoders, Eqs. 4–6, pp. 10–11) and predictability modeling (prediction error as score, Eq. 18–20, pp. 14–15). The latter ties anomaly detection and forecasting together: a forecaster's error is an anomaly score, which matters if we merge or jointly train detection and forecasting models.
- **Known weaknesses to test against.** Contamination of training data (p. 12, p. 31) and objectives not aligned with detection (p. 12, p. 15) are failure modes that merging could amplify or dampen; a merged model's reconstruction or prediction error is still the score, so these caveats apply unchanged.
- **CH5 and conditional anomalies** (pp. 5, 15): temporal-context anomalies are exactly what predictability methods target; continual settings where "normal" changes over time make the context itself shift, which the survey does not address.
- **Large-scale normality learning** (p. 31), pre-train then fine-tune per domain, is the setting in which task vectors are defined; the survey's warning that normality learning "may need to be domain/application specific" (p. 31) is a hypothesis our merging experiments can test directly.
- **Metrics and benchmarks** must come from elsewhere: the survey gives no metrics, and its dataset table has no multivariate sensor time series.

## Quotes worth keeping

> "Anomaly detection, a.k.a. outlier detection or novelty detection, is referred to as the process of detecting data instances that significantly deviate from the majority of data instances." (p. 2)

> "Also, it is challenging to detect anomalies from instances that may be dependent on each other such as by temporal, spatial, graph-based and other interdependency relationships" (p. 5)

> "Normal instances can be better restructured from compressed space than anomalies." (p. 10)

> "The objective function of the data reconstruction is designed for dimension reduction or data compression, rather than anomaly detection." (p. 12)

> "AEs are generally vulnerable to data noise presented in the training data as they can be trained to remember those noise, leading to severe overfitting and small reconstruction errors of anomalies." (p. 12)

> "Normal instances are temporally more predictable than anomalies." (p. 14)

> "The prediction here is conditioned on some elapsed temporal instances, so this category of methods is able to detect temporal context-based conditional anomalies (CH5)." (p. 15)

> "This is because most methods in Section 5 implicitly assume that the training data are clean and do not contain any noise/anomaly instances." (p. 31)
