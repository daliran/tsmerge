# wang2026deep — Deep Time Series Models: A Comprehensive Survey and Benchmark

- **Status:** verified (2026-11-02): checked against the paper and its text layer by an independent agent (about 150 claims, all 73 bar labels correct: 2 misstatements, 1 unsupported claim and 3 precision points, fixed)
- **Reference:** Wang, Wu, Dong, Liu, Wang, Long, Wang; IEEE TPAMI 48(10), 2026; DOI 10.1109/TPAMI.2026.3690845; arXiv 2407.13278 ([references.bib](../references.bib))
- **Version read:** arXiv 2407.13278v2 (27 Sep 2025, p. 1 margin), 20 pages: main text pp. 1–16, references pp. 16–20, author biographies p. 20. The PDF header reads "IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. X" (p. 1): it is the preprint, not the typeset TPAMI version
- **Read:** the whole paper, pp. 1–20: Sections 1–7 in full (pp. 1–16), with Tables 1–4 and Figures 1–10; reference list (pp. 16–20) skimmed for the entries cited in this note; author biographies (p. 20). There is no appendix
- **Code:** <https://github.com/thuml/Time-Series-Library> (p. 1, abstract; p. 10)

## In one paragraph

The paper surveys deep models for time-series analysis from a "model-centric" view (p. 3): first the **basic modules** reused across models — stationarization (normalization), decomposition, Fourier analysis (Section 3, pp. 3–5) — then the **architectures**, grouped into MLP-, RNN-, CNN-, GNN- and Transformer-based (Section 4, pp. 5–10). It then presents the **Time Series Library (TSLib)**, a benchmark that implements 30 models, covers 30 datasets and supports five tasks: long- and short-term forecasting, imputation, classification and anomaly detection (p. 1, abstract; pp. 10–13). Thirteen models are compared across the tasks, TiDE on long-term forecasting only (p. 13). The stated findings: Transformer-based models (iTransformer, PatchTST) are best at forecasting; TimesNet (CNN) is the most comprehensive on classification, imputation and anomaly detection; MLP-based models are good at forecasting but weaker elsewhere; RNN-based models do well on anomaly detection but show limited effectiveness overall; MLP-based models and Mamba are the most efficient (p. 13). Section 6 lists future directions, including pre-training and large time-series (foundation) models (pp. 14–16).

## Problem

There is no comprehensive overview covering both tasks and models: earlier reviews focus on one task or one architecture, and earlier benchmarks (BasicTS, TFB) cover forecasting only and don't describe architectures (pp. 1–2, Table 1, p. 2). Benchmarks also lack task and domain coverage, and don't summarize task types, architectures and baselines (p. 10); papers use inconsistent look-back lengths (p. 12). The survey aims at both a review and "a fair benchmark" (p. 1, abstract).

**Setting** (p. 2): a time series is a sequence of $T$ observations

$$\mathbf{X} = \{\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_T\} \in \mathbb{R}^{T \times C}, \qquad \mathbf{x}_t \in \mathbb{R}^C,$$

where $\mathbf{x}_t$ holds the observed values at timestamp $t$ and $C$ is the number of variables. No spatial structure is assumed among the variates (p. 2). The two things a model must capture are **temporal dependency** and **variate correlation** (p. 2).

## Tasks

The paper defines the tasks in words, not with formal input/output equations (pp. 2–3, Figure 1, p. 3):

| Task | Definition in the paper | Example applications (Figure 1, p. 3) |
|---|---|---|
| Forecasting | "aims to predict future values or trends of the input series" by capturing relations between past and future (pp. 2–3) | weather forecasting, energy/traffic planning |
| Imputation | "focuses on reconstructing missing values using the available contextual information" (p. 3) | data mining |
| Anomaly detection | "identifying unusual or abnormal patterns within a time series, which can indicate critical events, system faults, or outliers" (p. 3) | industrial maintenance |
| Classification | "assigns a label or category to a given time series based on its characteristics" (p. 3) | action recognition, heartbeat diagnosis |

Forecasting is split into **long-term** and **short-term** "following the previous convention, where the separation depends on the forecasting horizon" (p. 11); the concrete horizons are in [Benchmark protocol](#benchmark-protocol).

**Our reading:** the formal input/output setup of each task (window shapes, labels) isn't given in this paper; it defers dataset details to TimesNet ("more details can be found in previous papers [3]", p. 11), which is `wu2023timesnet` in our bibliography.

## Method: basic modules

### Stationarization (Section 3.1, p. 3)

- Stationary series have constant mean and variance; classically, differencing or log-transformation; in deep learning, data normalization "takes the role of stationarization", and "helps mitigate the distribution shift between the source and target domains" (p. 3).
- Specialized layers: DAIN (adaptive input normalization), RevIN (reversible instance normalization with learnable affine transforms), Non-Stationary Transformer ("Stationary"), SAN (normalizes non-overlapping equal-size slices and predicts future slice statistics) (p. 3).

**Stationary** (Eq. 1, p. 3), for $\mathbf{X} \in \mathbb{R}^{T \times C}$, as printed:

$$\mu_{\mathbf{x}} = \frac{1}{T}\sum_{i=1}^{T} \mathbf{x}_i, \quad \sigma_{\mathbf{x}}^2 = \sum_{i=1}^{T} \frac{1}{T}(\mathbf{x}_i - \mu_{\mathbf{x}})^2,$$

$$\bar{\mathbf{X}} = \frac{(\mathbf{X} - \mu_{\mathbf{x}})}{\sqrt{\sigma_{\mathbf{x}}^2 + \epsilon}}, \quad \bar{\mathbf{Y}} = \text{Model}(\bar{\mathbf{X}}), \quad \hat{\mathbf{Y}} = \sigma_{\mathbf{x}}^2(\bar{\mathbf{Y}} + \mu_{\mathbf{x}}),$$

with $\epsilon$ small for numerical stability and $\mu_{\mathbf{x}}, \sigma_{\mathbf{x}}^2 \in \mathbb{R}^{1 \times C}$ the per-variate mean and variance; the denormalization restores the input statistics on the model output (p. 3).

**Our reading:** the printed denormalization $\sigma_{\mathbf{x}}^2(\bar{\mathbf{Y}} + \mu_{\mathbf{x}})$ isn't the inverse of the normalization line above it (that would be $\sqrt{\sigma_{\mathbf{x}}^2 + \epsilon}\,\bar{\mathbf{Y}} + \mu_{\mathbf{x}}$); we take it as a typo and should implement the inverse, checking the Non-Stationary Transformer paper or TSLib code.

### Decomposition (Section 3.2, pp. 3–4)

- **Seasonal-trend** (p. 4): trend, seasonal, cyclical and irregular components. Autoformer's *series decomposition block* (Eq. 2, p. 4):

  $$\mathbf{X}_{\mathcal{T}} = \text{AvgPool}(\text{Padding}(\mathbf{X})), \qquad \mathbf{X}_{\mathcal{S}} = \mathbf{X} - \mathbf{X}_{\mathcal{T}}$$

  ($\mathbf{X}_{\mathcal{T}}$ trend, $\mathbf{X}_{\mathcal{S}}$ seasonal part), widely reused afterwards (p. 4).

- **Basis expansion** (p. 4): N-BEATS, block $l$ (Eq. 3, p. 4):

  $$\mathbf{X}_l = \mathbf{X}_{l-1} - \hat{\mathbf{X}}_{l-1}, \qquad \hat{\mathbf{X}}_l, \hat{\mathbf{Y}}_l = \text{Block}_l(\mathbf{X}_l),$$

  with $\hat{\mathbf{X}}_{l-1}$ the backcast, $\hat{\mathbf{Y}}_l$ a partial forecast, and the final forecast $\hat{\mathbf{Y}} = \sum_l \hat{\mathbf{Y}}_l$. Also N-HiTS, DEPTS, DEWP (p. 4).

- **Matrix factorization** (p. 4): $\mathbf{X} \approx \mathbf{F}\hat{\mathbf{X}}$ with $\mathbf{F} \in \mathbb{R}^{k \times C}$, $\hat{\mathbf{X}} \in \mathbb{R}^{T \times k}$, $k$ a hyperparameter (as printed; the paper describes the matrix as variates × time, p. 4); with regularizers (TRMF, NoTMF, BTF, DeepGLO, LSTM-GL-ReMF) (p. 4).

### Fourier analysis (Section 3.3, pp. 4–5)

- **Time-domain modeling** (p. 5): TimesNet uses the FFT to find the dominant periods and reshapes the 1D series into 2D; FiLM, FITS (low-pass filter) keep low frequencies; FEDformer keeps a random fixed number of components, both high and low; Autoformer's Auto-Correlation uses the FFT (via the Wiener–Khinchin theorem).
- **Frequency-domain modeling** (p. 5): ATFN, TFAD, STFNet, StemGNN, EV-FGN, FreTS, FCVAE, TSLANet, FourierDiffusion.

## Method: architectures (Section 4)

Five groups by backbone: MLP, RNN, CNN, GNN, Transformer (p. 5); Figure 2 (p. 6) places representative models on a 2018–2024 timeline and marks those implemented in TSLib.

**Our reading:** foundation models are not a sixth architecture group in this paper's taxonomy; they appear only as a future direction (Section 6.2, pp. 14–15, below).

### MLP (Section 4.1, pp. 5–6)

- Inspired by autoregressive models, where the output depends linearly on past values (pp. 5–6). Figure 3 (p. 6): linear layers map the historical points to the future points.
- N-BEATS (Eq. 3), N-HiTS, N-BEATSx (exogenous variables); DLinear ("a simple linear regression in the raw space"); FITS (complex-valued linear layer in the frequency domain); TSMixer (time-mixing and feature-mixing MLPs); FreTS; TimeMixer (multiscale mixing); TiDE (exogenous variables); Koopa (Koopman theory) (p. 6).

### RNN (Section 4.2, pp. 6–7)

- Focus on vanishing gradients and on correlations among variates (p. 6). Figure 4 (p. 6) contrasts deterministic and generative (autoregressive) outputs.
- LSTNet (recurrent + convolution, recurrent-skip), DA-RNN (dual-stage attention), DeepAR (probabilistic, autoregressive), DTWAtt (p. 7).
- **State space models** (p. 7): DSSM (RNN parametrizes a linear SSM), S4 (low-rank correction of matrix $\mathbf{A}$), **Mamba** ("a simple selection mechanism that parameterizes the SSM parameters based on input", linear complexity in sequence length). Mamba is counted as RNN-based in the benchmark (p. 13).
- Neural ODEs for continuous time and irregular sampling (p. 7).

### CNN (Section 4.3, pp. 7–8)

- 1D CNNs; SCINet (downsample-convolve-interact), WaveNet (dilated causal convolution), TCN, MICN (local-global), ModernTCN (DWConv + ConvFFN) (p. 7). Figure 5 (p. 7): 1D vs 2D representation space.
- **TimesNet** (Eq. 4, p. 8): the 1D series is turned into $k$ 2D tensors, one per estimated period, with inter-period variation in columns and intra-period variation in rows (p. 7):

  $$\mathbf{X}_{\text{2D}}^i = \text{Reshape}(\text{Padding}(\mathbf{X}_{\text{1D}})), \quad \hat{\mathbf{X}}_{\text{2D}}^i = \text{Inception}(\mathbf{X}_{\text{2D}}^i), \quad \hat{\mathbf{X}}_{\text{1D}}^i = \text{Trunc}(\text{Reshape}(\hat{\mathbf{X}}_{\text{2D}}^i)), \quad i \in \{1, \dots, k\}$$

  The 1D results are then aggregated; the paper says this lets TimesNet handle "four distinct tasks" (p. 8).

### GNN (Section 4.4, p. 8)

- Variates as nodes of a spatio-temporal graph (Figure 6, p. 8). Two kinds, predefined graph and learned graph (p. 8). **Our reading** of the per-model assignment, which the paper doesn't state: DCRNN and STGCN predefined; AGCRN, MTGNN, STFGNN, StemGNN learned; Graph WaveNet is discussed with DCRNN and STGCN but "learns an adaptive dependency matrix through node embedding" (p. 8), so it belongs with the learned graphs.

### Transformer (Section 4.5, pp. 8–10)

Grouped by token granularity: point-wise, patch-wise, series-wise (Figure 7, p. 8).

**Point-wise** (pp. 8–9). Data embedding (Eq. 5, p. 9), for $\mathbf{X} \in \mathbb{R}^{T \times C}$ and timestamps $\mathbf{X}^{\text{ts}} \in \mathbb{R}^{T \times D}$ ($D$ the types of timestamps):

$$\mathbf{H}_t = \text{Projection}(\mathbf{X}_t) + \text{PE}(\mathbf{X}_t) + \text{TE}(\mathbf{X}_t^{\text{ts}}),$$

with $\mathbf{H}_t \in \mathbb{R}^{T \times d_{\text{model}}}$, Projection $: \mathbb{R}^C \mapsto \mathbb{R}^{d_{\text{model}}}$ and TE $: \mathbb{R}^D \mapsto \mathbb{R}^{d_{\text{model}}}$ channel-dimension linear layers, PE the absolute position embedding (p. 9). Work either adds pre-processing (RevIN, Stationary, with normalization and de-normalization around the Transformer blocks; Stationary also adds De-stationary Attention against over-stationarization) or modifies attention to cut its quadratic cost (LogSparse, Informer, Pyraformer) (p. 9).

**Patch-wise** (pp. 9–10). Autoformer's Auto-Correlation (sub-series similarity via FFT, p. 9). PatchTST (Eq. 6, p. 9):

$$\{\mathbf{P}_1, \mathbf{P}_2, \dots, \mathbf{P}_N\} = \text{Patchify}(\mathbf{X}), \qquad \mathbf{H}_i = \text{PatchEmbed}(\mathbf{P}_i) + \mathbf{W}_{\text{pos}}^i,$$

with patch length $P$, $N$ patches, PatchEmbed $: \mathbb{R}^P \mapsto \mathbb{R}^{d_{\text{model}}}$ and learnable $\mathbf{W}_{\text{pos}} \in \mathbb{R}^{d_{\text{model}} \times N}$; patches are "overlapped" (p. 9), while p. 14 says PatchTST "segments the time series data into multiple non-overlapping patches": the paper contradicts itself. PatchTST is **channel-independent**: each token holds information from a single series (p. 9). Crossformer's Two-Stage Attention (Eq. 7, p. 10), for $\mathbf{H} \in \mathbb{R}^{N \times C \times d_{\text{model}}}$:

$$\mathbf{Z}^{\text{time}} = \text{Attention}^{\text{time}}(\mathbf{H}, \mathbf{H}, \mathbf{H}), \quad \mathbf{B} = \text{Attention}_1^{\text{dim}}(\mathbf{R}, \mathbf{Z}^{\text{time}}, \mathbf{Z}^{\text{time}}), \quad \overline{\mathbf{Z}}^{\text{dim}} = \text{Attention}_2^{\text{dim}}(\mathbf{Z}^{\text{time}}, \mathbf{B}, \mathbf{B}),$$

with $\mathbf{R} \in \mathbb{R}^{N \times C \times d_{\text{model}}}$ a learnable router (as printed, p. 10).

**Series-wise** (p. 10). iTransformer embeds each whole variate as one token (Eq. 8, p. 10):

$$\mathbf{H}^{(i)} = \text{VariateEmbed}(\mathbf{X}^{(i)}), \qquad \text{VariateEmbed}: \mathbb{R}^T \to \mathbb{R}^{d_{\text{model}}}$$

(a trainable linear projector), then a vanilla Transformer captures correlations among variates. TimeXer: patch-level tokens for endogenous and series-level tokens for exogenous variables, plus an endogenous global token (p. 10).

**Model cards** (Table 2, p. 9), attention formulas as printed:

| Category | Method | Architecture | Embedding | Attention mechanism |
|---|---|---|---|---|
| Vanilla | Transformer | Enc-Dec | Standard | $\text{FullAttention}(\mathbf{Q},\mathbf{K},\mathbf{V}) = \text{Softmax}(\frac{\mathbf{Q}\mathbf{K}^\intercal}{\sqrt{d}})$ |
| Point-wise | LogSparse | Dec-only | Standard | $\widehat{\mathbf{Q}}, \widehat{\mathbf{K}} = \text{CausalCov}(\mathbf{H})$; $\text{FullAttention}(\widehat{\mathbf{Q}},\widehat{\mathbf{K}},\mathbf{V}) = \text{Softmax}(\frac{\widehat{\mathbf{Q}}\widehat{\mathbf{K}}^\intercal}{\sqrt{d}})$ |
| Point-wise | Informer | Enc-Dec | Standard | $\overline{\mathbf{Q}} = \text{Top}_u(\overline{M}(\mathbf{q}_i, \mathbf{K}))$; $\text{ProbSparse-Attention}(\mathbf{Q},\mathbf{K},\mathbf{V}) = \text{Softmax}(\frac{\overline{\mathbf{Q}}\mathbf{K}^\intercal}{\sqrt{d}})\mathbf{V}$ |
| Point-wise | Pyraformer | Enc-Dec | Standard | $\text{Pyramid-Attention}(\mathbf{Q},\mathbf{K},\mathbf{V}) = \text{Masked}(\text{Softmax}(\frac{\mathbf{Q}\mathbf{K}^\intercal}{\sqrt{d}})\mathbf{V})$ |
| Patch-wise | Autoformer | Enc-Dec | Standard | $\text{Auto-Correlation}(\mathbf{Q},\mathbf{K},\mathbf{V}) = \sum_{i=1}^{k} \text{Roll}(\mathbf{V}, \tau_i)\widehat{\mathcal{R}}_{\mathbf{Q},\mathbf{K}}(\tau_i)$ |
| Patch-wise | Crossformer | Enc-Dec | Patch-Wise | FullAttention, as Transformer |
| Patch-wise | PatchTST | Enc-only | Patch-Wise | FullAttention, as Transformer |
| Variate-wise | iTransformer | Enc-only | Variate-Wise | FullAttention, as Transformer |

## Benchmark protocol

**TSLib** (Section 5, pp. 10–12; Figure 8, p. 10):

- Factory pattern with a unified interface between data, model and experiment objects (p. 11). Tasks are unified "as a representation learning task with domain-specific heads": a shared backbone plus task-specific heads (p. 11; Figure 8, p. 10).
- 30 models implemented following the official codes (p. 10); "more than 30 datasets" (p. 11); formats `.csv`, `.npz`, `.txt`, `.ts` (Figure 8, p. 10).
- Built-in data processing: train-val-test splitting, sample splitting, data normalization (Figure 8, p. 10); "the raw data is partitioned into separate windows for training, validation, and testing" (p. 11). Optional processing layers: normalization, time-frequency decomposition, Fourier analysis (p. 11).
- **Fairness:** "different models are trained and tested based on the same training strategies and test sets" (p. 11).

**Our reading:** the paper gives no split ratios, no window stride, and doesn't say which normalization is applied in the benchmark runs; those details live in TSLib's code or in TimesNet.

**Comparison with other libraries** (Table 3, p. 11; stars as of July 2025; * = no deep models):

| Library | Models | Tasks | Stars |
|---|---|---|---|
| tslearn* | 10 | Clustering, Classification, Regression | 3k |
| StatsForecast* | 31 | Forecasting, Anomaly Detection | 4.4k |
| NeuralForecast | 33 | Forecasting | 3.6k |
| GluonTS | 25 | Forecasting, Anomaly Detection | 4.9k |
| TSLib | 30 | Forecasting, Imputation, Classification, Anomaly Detection | 9.4k |

**Metrics** (Section 5.2, p. 11; Figure 8, p. 10, lists "Accuracy, F1-Score" for both classification and anomaly detection, while the text names F1 for anomaly detection and accuracy for classification, p. 11):

| Task | Metrics |
|---|---|
| Long-term forecasting, imputation | MSE and MAE (primary) |
| Short-term forecasting | SMAPE and MASE; Figure 9 reports average OWA (p. 12) |
| Classification | accuracy |
| Anomaly detection | F1 score, "a balanced combination of precision and recall" (p. 11) |

The paper gives no formulas for these metrics, and doesn't define OWA.

**Datasets** (Section 5.3, pp. 11–12):

| Task | Datasets |
|---|---|
| Long-term forecasting | 9 datasets: ETT (4 subsets), Electricity, Weather, Traffic, Exchange, Illness (p. 11) |
| Short-term forecasting | M4, 6 sub-datasets with different sampling frequencies and domains (p. 11) |
| Imputation | ETT (4 subsets), Electricity, Weather, with time steps masked at random (p. 12) |
| Anomaly detection | SMD, MSL, SMAP, SWaT, PSM, "collected from a variety of industrial scenarios" (p. 12) |
| Classification | 10 multivariate datasets from the UEA archive (p. 12) |

**Input and prediction lengths** (Section 5.4, p. 12):

- **Long-term forecasting:** ILI: look-back 36, horizons $\{24, 36, 48, 60\}$; all other datasets: unified look-back 96, horizons $\{96, 192, 336, 720\}$.
- **Short-term forecasting:** horizons $\{6, 8, 18, 13, 14, 48\}$ for yearly, quarterly, monthly, weekly, daily and hourly data (as printed).
- **Imputation:** time points masked at random in ratios $\{12.5\%, 25\%, 37.5\%, 50\%\}$.
- **Anomaly detection:** reconstruction; deep models are the base models for reconstruction and the **reconstruction error is "a shared anomaly criterion across all experiments"** (p. 12).
- **Look-back searching** (pp. 12–13): because results depend strongly on the input length and papers use different ones, a second set of long-term experiments searches the input length in $\{96, 192, 336, 512\}$ together with each model's hyperparameters.

**Our reading:** for anomaly detection the paper doesn't give the window length, the threshold rule (how the reconstruction error becomes a label), or whether point adjustment is used; we need TimesNet or TSLib's code for those.

**Training** (Table 4 and "Implementation Details", p. 12):

| Task | Initial LR | Loss | Batch size | Epochs |
|---|---|---|---|---|
| Long-term forecasting | $10^{-4}$ | MSE | 32 | 10 |
| Short-term forecasting | $10^{-3}$ | SMAPE | 16 | 10 |
| Imputation | $10^{-3}$ | MSE | 16 | 10 |
| Classification | $10^{-3}$ | Cross Entropy | 16 | 100 |
| Anomaly detection | $10^{-4}$ | MSE | 128 | 10 |

- PyTorch, one NVIDIA A100, Adam (p. 12).
- Hyperparameter search per architecture: number of layers $L \in \{2, 3, 4\}$, $d_{\text{model}}$ in $[2^4, 2^9]$ (p. 12).

**Models compared** (p. 13): 13 models.

- Transformer: iTransformer, PatchTST, Autoformer, Non-Stationary Transformer (Stationary), FEDformer; Crossformer also appears in Figure 9 (p. 12).
- CNN: TimesNet, SCINet.
- RNN: Mamba.
- GNN: StemGNN.
- MLP: DLinear, N-BEATS, TiDE. TiDE needs timestamps, so it is tested on long-term forecasting only (p. 13).

**Our reading:** the text lists five Transformer models while Figure 9 shows six (with Crossformer), for 13 in total; "NSFormer" in Figure 9 is the Non-Stationary Transformer.

## Results

All results are **averages over the task's datasets** (Figure 9 caption, p. 12); the paper prints no per-dataset or per-horizon numbers. Values as printed on the bars of Figure 9 (p. 12); medals mark the top three.

**Forecasting and anomaly detection** (Figure 9, p. 12):

| Model | Backbone | Long-term MSE ↓ (unified look-back) | Long-term MSE ↓ (look-back searching) | Short-term OWA ↓ | Anomaly detection F1 (%) ↑ |
|---|---|---|---|---|---|
| iTransformer | Transformer | **0.342** (1st) | 0.317 (3rd) | 1.030 | 81.39 |
| PatchTST | Transformer | 0.373 (3rd) | **0.305** (1st) | **0.871** (1st) | 82.79 |
| Crossformer | Transformer | 0.559 | 0.490 | 1.075 | 83.45 |
| Autoformer | Transformer | 0.436 | 0.436 | 0.992 | 84.26 |
| NSFormer | Transformer | 0.427 | 0.430 | 1.000 | 82.10 |
| FEDformer | Transformer | 0.403 | 0.394 | 0.945 | 84.97 (2nd) |
| TimesNet | CNN | 0.381 | 0.362 | 0.888 (2nd) | **85.24** (1st) |
| SCINet | CNN | 0.589 | 0.369 | 1.309 | 84.74 (3rd) |
| Mamba | RNN | 0.429 | 0.386 | 0.922 | 83.89 |
| DLinear | MLP | 0.414 | 0.332 | 1.130 | 82.46 |
| N-BEATS | MLP | 0.371 (2nd) | 0.313 (2nd) | 0.890 (3rd) | 81.93 |
| TiDE | MLP | 0.459 | 0.352 | — | — |
| StemGNN | GNN | 0.442 | 0.432 | 1.060 | 79.87 |

**Imputation and classification** (Figure 9, p. 12), for completeness:

| Model | Imputation MSE ↓ | Classification accuracy (%) ↑ |
|---|---|---|
| iTransformer | 0.117 | 70.06 |
| PatchTST | 0.065 | 72.50 |
| Crossformer | 0.077 | 73.17 (2nd) |
| Autoformer | 0.062 | 71.07 |
| NSFormer | 0.057 (2nd) | 72.66 (3rd) |
| FEDformer | 0.112 | 70.67 |
| TimesNet | **0.050** (1st) | **73.67** (1st) |
| SCINet | 0.059 (3rd) | 71.71 |
| Mamba | 0.069 | 69.87 |
| DLinear | 0.119 | 70.71 |
| N-BEATS | 0.190 | 68.96 |
| TiDE | 0.118 | — |
| StemGNN | 0.174 | 65.16 |

**Our reading:** the imputation panel shows a TiDE bar (0.118) although the text says TiDE was tested on long-term forecasting only (p. 13); classification shows none.

**By backbone** (Figure 10 left, p. 13): each backbone's score is the best among its models (p. 13). The best values printed on the radar are those of Figure 9: long-term MSE 0.342, long-term MSE (*) 0.305, short-term OWA 0.871, imputation MSE 0.050, classification 73.67, anomaly detection F1 85.24; the GNN values 0.442, 0.432, 1.060, 0.174, 65.16, 79.87 are printed as the inner points. **Our reading:** "(*)" is the look-back searching setting, judging by the value 0.305.

**Efficiency** (Figure 10 middle and right, p. 13): long-term forecasting on Weather, unified hyperparameters (p. 13); bubble size is memory (1.0, 1.5, 2.0 GB reference bubbles). Labels as printed, in the order **our reading** of the axes suggests (inference ms/sample, training ms/iter):

| Model | Inference (ms/sample) | Training (ms/iter) |
|---|---|---|
| iTransformer | 3.2 | 25.1 |
| PatchTST | 3.7 | 31.2 |
| StemGNN | 3.8 | 52.7 |
| N-BEATS | 5.5 | 29.9 |
| Mamba | 8.1 | 25.9 |
| DLinear | 10.6 | 21.8 |
| Crossformer | 16.7 | 67.2 |
| TimesNet | 22.2 | 473.4 |
| Autoformer | 56.1 | 49.6 |
| SCINet | 62.2 | 513.4 |

**Stated conclusions** (pp. 13, 16):

- Transformer-based models (iTransformer, PatchTST) have the best long- and short-term forecasting; tokenization "is the key to unlocking the capacity of Transformer-based models" (p. 13).
- TimesNet "shows a more comprehensive and effective performance covering time series classification, imputation, and anomaly detection tasks" (p. 13).
- MLP-based models perform well on forecasting but "appear to be less effective in other types of tasks, which require the model to learn more informative representations" (p. 13).
- CNN-based models "excel in classification, imputation, and anomaly detection tasks" (p. 13).
- RNN-based models perform well on anomaly detection but show "limited effectiveness" compared to other architectures (p. 13).
- Transformer-based models are "highly competitive" across tasks, a "particularly promising option" (p. 13).
- Efficiency: point-wise tokens (Autoformer) are slower than patch-wise (PatchTST) and series-wise (iTransformer); CNN-based models (SCINet, TimesNet) are much more time-consuming; MLP-based models and Mamba are the most efficient (p. 13).
- Section 7 (p. 16): separating basic modules from full models uncovers "the fundamental design principles"; TSLib enables flexible and comprehensive evaluation.

## Future directions (Section 6, pp. 13–16)

- **Pre-training** (p. 14): contrastive (CPC, TimeCLR, TS-TCC, TS2Vec, LaST, CoST, TF-C) and masked modeling (TST, PatchTST, SimMTM, HiMTM, TimeSiam).
- **Time-series foundation models** (p. 14): pre-trained on massive data; TimeGPT, Lag-Llama, Timer (univariate only); MOIRAI flattens multivariate series into one sequence; multimodal learning as a direction.
- **Adapting LLMs** (pp. 14–15): fine-tuning (LLM4TS, LLMTime, Chronos, GPT4TS, which fine-tunes the positional embeddings and layer-norm parameters of GPT-2) and prompting (PromptCast, UniTime, TimeLLM, AutoTimes); most work is on forecasting. Both need large training sets, limited by privacy in industrial and IoT settings, hence data generation (p. 15).
- **Practical applications** (pp. 15–16): probabilistic forecasting, extremely long series (patch length trades cost against accuracy), exogenous variables, heterogeneous data (sampling rates, irregularity, variable lengths).

## Assumptions and limitations

- **Averages only:** results are averaged over each task's datasets (Figure 9, p. 12); no per-dataset numbers, no standard deviations, no number of runs or seeds.
- **Anomaly detection by reconstruction only:** one shared criterion, the reconstruction error, for all models (p. 12); thresholding and evaluation details aren't given.
- **Fixed training budget:** 10 epochs for every task but classification (Table 4, p. 12), with a hyperparameter search over $L$ and $d_{\text{model}}$ (p. 12).
- **Look-back sensitivity:** the authors state that long-term results depend highly on the input length, and add the look-back searching runs for this reason (p. 12); rankings change between the two settings (Figure 9, p. 12).
- **TiDE** isn't evaluated on tasks without timestamps (p. 13).
- **Our reading:** the benchmark is single-task and static: each model is trained once per dataset; nothing on continual learning, distribution shift over time beyond normalization, multi-task training or model merging. The survey's conclusions about architectures are drawn from average scores without significance tests. The authors are also the TSLib developers.

## Relevance to this thesis

**Our reading:**

- **A standard protocol to adopt:** look-back 96 with horizons {96, 192, 336, 720} and MSE/MAE for long-term forecasting; reconstruction with MSE loss and the reconstruction error as anomaly score, F1 as metric, on SMD, MSL, SMAP, SWaT, PSM for anomaly detection (pp. 11–12). Using it makes our joint-training and merging numbers comparable with Figure 9.
- **Reference numbers:** Figure 9 gives what a single model trained on each dataset reaches (e.g. TimesNet 85.24 average F1; iTransformer 0.342 average long-term MSE). They are averages, so per-dataset baselines must come from our own runs or from `wu2023timesnet`.
- **Backbone choice for merging:** a task vector needs the same architecture and initialization across tasks. TimesNet (best on anomaly detection, comprehensive across tasks) and PatchTST/iTransformer (best on forecasting) are candidates; the efficiency table (p. 13) matters on our budget: TimesNet takes 473.4 ms per training iteration, 15 to 19 times PatchTST (31.2) or iTransformer (25.1), if our reading of the labels is right.
- **Channel independence and series-wise tokens** (pp. 9–10) decide how parameters relate to variates: with a different number of variates per dataset, a shared backbone (needed to merge) is easier with channel-independent or per-variate-token designs.
- **Normalization:** per-window instance normalization (Eq. 1, RevIN) is part of the standard pipeline and may interact with merging (statistics are recomputed per input, not learned); to check when we fix the data pipeline.
- **Open points to resolve elsewhere:** anomaly thresholding, point adjustment, window lengths for anomaly detection, split ratios: from `wu2023timesnet` and TSLib's code.

## Quotes worth keeping

> "TSLib implements 30 prominent models, covers 30 datasets from different domains, and supports five prevalent analysis tasks." (p. 1)

> "different models are trained and tested based on the same training strategies and test sets to avoid potential unaligned configurations and ensure a rigorous comparison among different models." (p. 11)

> "In the anomaly detection task, the reconstruction is a classical task for unsupervised point-wise representation learning, where the reconstruction error is a natural anomaly criterion." (p. 12)

> "Note that in long-term forecasting tasks, the model's performance is highly dependent on the historical length of the input series." (p. 12)

> "Additionally, TimesNet [3] shows a more comprehensive and effective performance covering time series classification, imputation, and anomaly detection tasks, pioneering a milestone in task-general time series models." (p. 13)

> "We surprisingly find that the MLP-based models, which are generally simpler and have lower computational overhead, perform well on time series forecasting. However, these models appear to be less effective in other types of tasks, which require the model to learn more informative representations." (p. 13)
