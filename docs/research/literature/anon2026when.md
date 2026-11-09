# anon2026when — When Foundation Models are One-Liners: Limitations and Future Directions for Time Series Anomaly Detection

- **Status:** verified (2026-11-08): checked against the paper by an independent agent (about 190 claims, every table cell correct; every "not in the paper" statement confirmed: 2 misstatements, 1 unmarked inference and 3 clarity points, fixed)
- **Reference:** Anonymous authors; ICLR 2026 submission 10983, **under double-blind review** (not accepted at the time of reading; authors unknown) ([references.bib](references.bib))
- **Version read:** the ICLR 2026 submission PDF, 28 pages: main text pp. 1–10, references pp. 11–13, appendices A–M pp. 14–28. Parts of the text are printed in blue (e.g. p. 2, p. 6, pp. 8–9, appendices I–M); the paper doesn't say why
- **Read:** all 28 pages: main text in full, references, and appendices A–M in full (A declarations, B design choices, C examples, D derivation, E–F complete results, G data contamination, H secondary findings and labeling flaws, I normalization ablation, J statistical analysis, K non-TSFM comparison, L forecasting horizons, M multivariate). Figures were read for their printed numbers and captions; values that exist only as plotted points or curves were not extracted, except where marked **our reading**
- **Code:** not released; "All our scripts to load the time series, detect anomalies, and evaluate the performances will be released upon publication" (p. 14)

## In one paragraph

The paper tests whether time-series foundation models (TSFMs) used **zero-shot** for univariate time-series anomaly detection (TSAD) through their reconstruction or forecasting error actually beat trivial "one-liner" detectors (pp. 1–2).

It evaluates five families — MOMENT (reconstruction), Chronos-Bolt, TimesFM and Time-MoE (forecasting), and TSPulse (both) — at two sizes each (except TSPulse) and context windows of 64, 256 and 512 (p. 2, Table 2, p. 5), on the 350 series of the TSB-AD-U evaluation set, scored with VUS-PR (p. 5).

Against **moving-window variance** (for reconstruction models) and **squared difference** from a local mean (for forecasting models), no TSFM is consistently or significantly better:

- correlations of per-series VUS-PR with the baseline are 0.848–0.995 and Cohen's $d$ ranges from −0.180 to 0.194 (Table 8, p. 24).

The reasons given:

- z-normalization makes MOMENT's score approximately the window variance times a near-constant reconstruction error (Eq. 1, p. 6; Appendix D, p. 17),
- and one-step forecasting lets anomalous inputs in the context make the anomaly itself predictable (p. 7).

The paper also reports 50 series of TSB-AD-U with problematic labels (Table 7, p. 21) and a metric effect where tiny score differences inflate VUS-PR (p. 21).

It proposes three directions:

- ensembling short and long forecasting horizons,
- detecting anomalies in hidden representations,
- and end-to-end fine-tuning with labeled anomalies (Section 6, pp. 8–10).

## Problem

**Research question** (p. 3): "Are current approaches to apply time-series foundation models to time-series anomaly detection effective?"

**Setting:**

- **Univariate** series only (p. 2, footnote 1), because "the majority of TSFMs support only univariate inputs natively".
  - Chronos-2 and Toto 1.0 are named as recent exceptions, with preliminary multivariate results in Appendix M (p. 2).
- **Zero-shot:** the evaluation set is used "to evaluate the models' zero-shot anomaly detection capabilities for univariate TSAD" (p. 5).
  - No fine-tuning of the TSFMs is performed in the paper's own experiments (Sections 4–5).
  - Fine-tuning with labeled anomalies is left as a future direction (p. 10).
- **Motivation:** the only extensive prior evaluation (Liu & Paparrizos, 2024, the TSB-AD benchmark)
  - "heavily relies on aggregate metrics which overlook counterintuitive details",
  - and uses one model size and short context windows per family (p. 2).

**Definitions** (p. 2, p. 3):

- A univariate time series $T = (x_1, \dots, x_n)$, $x_i \in \mathbb{R}$; a subsequence $T_{s,e} = (x_s, x_{s+1}, \dots, x_e)$ with $1 \le s < e \le n$, of length $e - s + 1$ (p. 2).
- **TSAD** (Definition 1, p. 3): predicting anomaly scores $s_i \in \mathbb{R}^+$ for each $x_i \in T$; $x_i$ is more anomalous than $x_j$ if $s_i > s_j$.
  - The task is defined as **scoring**, not as binary labeling.
- **Forecasting-based TSFM** (Definition 2, p. 3): $\mathcal{F}^{(\text{forecast})} : \mathbb{R}^w \mapsto \mathbb{R}$, pre-trained to predict the next value after a context window of length $w$.
- **Reconstruction-based TSFM** (Definition 3, p. 3): $\mathcal{F}^{(\text{reconstruct})} : \mathbb{R}^w \mapsto \mathbb{R}^w$, pre-trained to reconstruct sequences of length $w$.
- **The assumption under test** (p. 3):
  - forecasting-based detection assumes "anomalous observations are inherently more difficult to predict";
  - reconstruction-based detection assumes "anomalous sequences are harder to reconstruct".

## Method

### How a TSFM produces anomaly scores (Figure 1, p. 3)

Each window is normalized, passed through the TSFM, and de-normalized (Figure 1, p. 3).

- **Forecasting-based:** for the window $T_{i,i+w-1}$, predict $\hat{x}_{i+w}$ and score

  $$s_{i+w} = (\hat{x}_{i+w} - x_{i+w})^2$$

- **Reconstruction-based:** reconstruct $\hat{T}_{i,i+w-1}$ and assign the window's error to its center:

  $$s_{i+\lfloor w/2 \rfloor} = \mathrm{MSE}(T_{i,i+w-1}, \hat{T}_{i,i+w-1})$$

- **Padding** of the positions without a score (Figure 1, p. 3):
  - forecasting: $s_i := s_{w+1}$ for $i \in [1, w]$;
  - reconstruction: $s_i := s_{\lfloor w/2 \rfloor + 1}$ and $s_{n-i+1} := s_{n - \lfloor w/2 \rfloor}$ for $i \in [1, \lfloor w/2 \rfloor]$.

### The one-liner baselines (pp. 4–5)

- **Moving-window variance, Var-$w$** (Definition 4, p. 4), the baseline for reconstruction-based models, chosen "as we found that model performance correlates positively with variance in anomalous regions":

  $$s_{i+\lfloor w/2 \rfloor} = \mathrm{variance}(T_{i,i+w-1})$$

- **Squared difference** (Definition 5, p. 5), the baseline for forecasting-based models, "inspired by the one-liners of Wu & Keogh (2023)", using "the mean of the neighboring observations as forecast" (p. 4):
  - **Last-$w$:** $s_{i+w} = (\mathrm{mean}(T_{i,i+w-1}) - x_{i+w})^2$
  - **Centered-$w$:** $s_{i+\lfloor w/2 \rfloor} = (\mathrm{mean}(T_{i,i+w-1} \setminus x_{i+\lfloor w/2 \rfloor}) - x_{i+\lfloor w/2 \rfloor})^2$
- The baselines used in the comparisons are Var-$w$ with the same $w$ as the TSFM's context (e.g. Var-64 vs MOMENT-base-64, Figure 3, p. 6), Last-1, Last-3 and Centered-5 (Figure 5, p. 7).
  - Last-3 is the reference for the statistical tests on forecasting models (Table 3, p. 8).

### Why MOMENT behaves like variance (p. 5, p. 6, Appendix D p. 17)

With z-normalization of each window, $\mu_i := \mathrm{mean}(T_{i,i+w-1})$, $\sigma_i := \mathrm{std}(T_{i,i+w-1})$, and $T^{\text{norm}}_{i,i+w-1}$ the normalized window (p. 17):

$$
\begin{aligned}
s_{i+\lfloor w/2 \rfloor} &= \mathrm{MSE}\big(T_{i,i+w-1},\ \hat{T}_{i,i+w-1}\big) \\
&= \mathrm{MSE}\big(T^{\text{norm}}_{i,i+w-1} (\sigma_i + \epsilon) + \mu_i,\ \mathcal{F}^{(\text{reconstruct})}(T^{\text{norm}}_{i,i+w-1}) (\sigma_i + \epsilon) + \mu_i\big) \\
&= \mathrm{MSE}\big(T^{\text{norm}}_{i,i+w-1} (\sigma_i + \epsilon),\ \mathcal{F}^{(\text{reconstruct})}(T^{\text{norm}}_{i,i+w-1}) (\sigma_i + \epsilon)\big) \\
&= (\sigma_i + \epsilon)^2 \cdot \mathrm{MSE}\big(T^{\text{norm}}_{i,i+w-1},\ \mathcal{F}^{(\text{reconstruct})}(T^{\text{norm}}_{i,i+w-1})\big) \\
&\approx \sigma_i^2 \cdot \mathrm{MSE}\big(T^{\text{norm}}_{i,i+w-1},\ \mathcal{F}^{(\text{reconstruct})}(T^{\text{norm}}_{i,i+w-1})\big)
\end{aligned}
$$

MOMENT's normalizer adds $\epsilon = 10^{-5}$ to the standard deviation; its influence is called negligible (p. 17).

The last line is Equation 1 (p. 6). If the second factor barely varies, the score is the window variance (p. 6).

### Statistical comparison (Table 3, p. 8; Appendix J, p. 24)

Per configuration, over the 350 series:

- mean VUS-PR of the TSFM and of its baseline,
- the correlation between their per-series scores,
- its p-value,
- and Cohen's $d$ (Table 8, p. 24).

In addition, **non-inferiority tests based on the Wilcoxon signed-rank test** exclude, "with at least 95% confidence level", that the TSFMs beat their baselines by more than a small margin (p. 24).

The paper doesn't state which correlation coefficient is used, nor the sign convention of Cohen's $d$ (**our reading:** the positive values where the TSFM mean is higher suggest TSFM minus baseline).

### One-to-one plots (Figures 3–5, pp. 6–7)

Each point is one series: $x$ = VUS-PR of the TSFM, $y$ = VUS-PR of the baseline.

Legends give the share of series with $y \approx x$, $y > x$ (baseline better) and $y < x$ (TSFM better). The tolerance for "≈" isn't stated in the paper.

The legend percentages are copied as printed; several don't sum to 100 because of rounding (e.g.

- MOMENT-large-1024: 77 / 16 / 8, pp. 7, 18;
- TimesFM vs Last-1 without the problematic series: 85 / 3 / 13, p. 22;
- Chronos-t5: 85 / 11 / 5, p. 23;
- Time-MoE with Min-Max: 85 / 5 / 9, p. 23).

### Proposed horizon ensemble (Section 6.1, p. 9)

For a context $T_{t-w:t-1}$ and horizon $h$, the TSFM predicts $\hat{T}_{t:t+h-1}$, and the score of $x_t$ is the MSE between $T_{t:t+h-1}$ and $\hat{T}_{t:t+h-1}$.

Scores from several horizons are combined with a `MAX` operation (p. 9).

## Experimental setup

### Models (Table 1, p. 4; Table 2, p. 5; Appendix B, p. 15)

| | Chronos-Bolt | Time-MoE | TimesFM | MOMENT | TSPulse |
|---|---|---|---|---|---|
| Normalization | Z-scaling | Z-scaling | Z-scaling | Z-scaling | RevIN |
| Tokenization | Patching | Point value | Patching | Patching | Patching |
| Embedding | Residual block | SwiGLU | Residual block | Linear projection | Linear projection |
| Architecture | Encoder-decoder | Decoder-only | Decoder-only | Encoder-only | TSMixer |
| Pre-trained on | Forecasting | Forecasting | Forecasting | Reconstruction | Forec. + Recon. |
| Sizes (ours) | bolt-small, bolt-base | base, large | 1.0 (200M), 2.0 (500M) | base, large | 1M |
| Windows (ours) | 64, 256, 512 | 64, 256, 512 | 64, 256, 512 | 64, 256, 512 (+1024 for large) | 512 |
| Covered by Liu & Paparrizos (2024) | t5-base, window 100 | not covered | 1.0 (200M), window 96 | base, window 64 | not covered |

Sources: Table 1 (p. 4) for the first five rows; Table 2 (p. 5) for the last three, with the footnote that MOMENT-large was also run with window 1024 (p. 5).

- **TSPulse** is "a tiny (1M) non-Transformer model" with three heads:
  - time-domain reconstruction (Head$_\text{time}$),
  - frequency-domain reconstruction (Head$_\text{fft}$),
  - and time-domain forecasting (Head$_\text{future}$),
  - "combined via ensembling and triangulation", "a per-dataset model selection procedure based on the heads' performance on a tuning set" (p. 4).
  - Its numbers are **taken from its own paper** (Ekambaram et al., 2025, Table 1(a)), not rerun (p. 4, p. 8).
- **Pre-training losses** (p. 15):
  - Chronos uses cross-entropy on the next data point;
  - TimesFM MSE on the next patch;
  - Time-MoE forecasting with different horizons;
  - MOMENT is "the only large-scale TSFM, as far as we know, that is pre-trained on the task of sequence reconstruction".
- **Normalization** (p. 15): Time-MoE, MOMENT, Chronos-Bolt and TimesFM z-normalize each context window; Chronos-t5 uses mean scaling.
  - Chronos-t5 is the only family with discrete tokens (uniform binning) (p. 15).
- Naming convention: "model family-model size-context window length", e.g. MOMENT-base-64 (p. 4).

### Dataset (p. 5; Appendix A.2, p. 14; Appendix H, p. 21)

- **TSB-AD-U evaluation set** (Liu & Paparrizos, 2024): **350 univariate time series** curated from **23 univariate datasets** (p. 5)
  - "twelve of the 23 univariate datasets are derived from multivariate datasets" (p. 5, footnote 2).
  - Chosen because "it is the latest curated benchmark emphasizing labeling quality" (p. 5).
- The train-test split is TSB-AD's own (p. 14).
  - Series are referred to by ID, e.g. "TSB-AD-U 811" is `811_Exathlon_id_2_Facility_tr_10766_1st_12590` (p. 5).
- Source datasets visible in the paper's examples: Exathlon, UCR, SMD, OPPORTUNITY, YAHOO, NAB, WSD, SED, SMAP (Figures 2, 9, pp. 6, 16), MSL and SWaT (Table 7, p. 21).
- Datasets **not** used in MOMENT's pre-training: WSD, Stock, LTDB, SED, TAO, NEK, CATSv2, TODS, Power, SWaT, Exathlon (p. 20, footnote 6).
- Exathlon's mean anomaly length is 1577.3, "almost 25 times larger than the context window length" of 64 (p. 5).
- **Multivariate** (Appendix M, p. 28): qualitative examples on TSB-AD-M series (Genesis, SWaT, MSL, Daphnet, LTDB, Exathlon, TAO, SMAP) with Chronos-2-512, Toto-Open-Base-1.0-512 and Last-3.
  - Scores are the mean squared prediction error over all channels (Figure 19, p. 28).
  - No numbers are given.

### Metrics and evaluation protocol (p. 5, p. 21, p. 24)

- **VUS-PR**, following Liu & Paparrizos (2024), the main metric (p. 5).
  - The authors state that all key findings "can be derived by examining intermediate results, such as anomaly scores, or by conducting representative case studies, without relying on any specific metric" (p. 5).
- VUS-PR (Paparrizos et al., 2022), "like its parent AUC-PR, only cares about the relative ranking of the scores rather than their actual values" (p. 21).
- **Event-based F1** as a robustness check (Table 9, p. 25; p. 24). Its definition and thresholding aren't given in the paper.
- **Not used or discussed:** point adjustment, PA-F1, point-wise F1, AUROC, affiliation metrics, or any threshold-selection rule.
  - The paper's TSAD definition is score-only (Definition 1, p. 3), and VUS-PR "only cares about the relative ranking of the scores" (p. 21);
  - **our reading:** so it needs no threshold.
- **Forecasting quality:** MASE of each series against the Last-1 baseline, aggregated with the geometric mean.
  - Evaluation starts at the 513th data point "for a fair comparison across different context window lengths" (p. 7, footnote 5).
- **Constant-value windows** are excluded from the MSE histograms "as they are trivially reconstructed" (p. 6, footnote 3).

## Results

### Reconstruction-based: MOMENT vs Var-$w$ (Section 5.1, pp. 5–7; Appendix E, p. 18)

- In Liu & Paparrizos (2024), MOMENT-base-64 reaches VUS-PR 0.81 on Exathlon, among the best detectors there (p. 5).
  - The paper finds MOMENT-base does well where anomalous regions have higher variance than normal ones and fails on low-variance anomalies (p. 5; Figures 2a, 9a).
- MOMENT-base reconstructs all normalized windows "with a consistently high MSE near 1.1", whether or not they contain an anomaly (p. 6, Figure 3).
  - MOMENT-large reconstructs better and with a wider spread, but the MSE distributions of normal and anomalous windows "remain entirely overlapping" (p. 6, Figure 4).
- **Data contamination** isn't the explanation: on 94 series from datasets not in MOMENT's pre-training, the same overlap holds (Figure 14, p. 20).

Share of the 350 series per outcome, as printed in the plot legends (Figures 3–4, pp. 6–7; Figures 10–11, p. 18). $y$ = Var-$w$, $x$ = MOMENT:

| Configuration | $y \approx x$ | $y > x$ (baseline better) | $y < x$ (MOMENT better) |
|---|---|---|---|
| MOMENT-base-64 | 97% | 2% | 1% |
| MOMENT-base-256 | 98% | 1% | 1% |
| MOMENT-base-512 | 97% | 2% | 1% |
| MOMENT-large-64 | 82% | 7% | 11% |
| MOMENT-large-256 | 68% | 15% | 17% |
| MOMENT-large-512 | 70% | 15% | 15% |
| MOMENT-large-1024 | 77% | 16% | 8% |

### Forecasting-based: Chronos-Bolt, Time-MoE, TimesFM vs squared difference (Section 5.2, pp. 6–8; Appendix F, p. 19)

- "No forecasting-based TSFM outperforms the squared-difference baseline on TSAD" (p. 6), "despite the differences in the forecasting performance" (p. 7).
- Pairwise correlation of VUS-PR across all forecasting variants and baselines has a minimum of 0.90 (Figure 13 caption, p. 19; "0.9", p. 7).
- One-to-one, TimesFM-2.0-512 vs Last-3: $y \approx x$ 85%, $y > x$ 6%, $y < x$ 9% (Figure 5b, p. 7).

**Forecasting quality**, aggregate MASE (geometric mean, relative to Last-1), as printed on the bars (Figure 12, p. 19; the six of Figure 5a, p. 7, agree):

| Model | 64 | 256 | 512 |
|---|---|---|---|
| Chronos-Bolt-small | 0.97 | 0.93 | 0.96 |
| Chronos-Bolt-base | 0.92 | 0.89 | 0.89 |
| Time-MoE-base | 0.81 | 0.75 | 0.74 |
| Time-MoE-large | 0.82 | 0.75 | 0.74 |
| TimesFM-1.0 | 0.96 | 0.98 | 1.00 |
| TimesFM-2.0 | 0.84 | 0.82 | 0.83 |

Baselines: Last-1 1.00, Last-3 1.30, Centered-5 0.71 (Figure 12, p. 19).

So Centered-5 has the lowest MASE of all, and Time-MoE the lowest among the TSFMs, yet the VUS-PR boxplots are all similar (Figure 12, p. 19).

**Why:** with a one-step horizon, a sliding context that overlaps a sequence anomaly feeds the model recent anomalous values, so "even anomalous values are usually not 'unexpected'" and are forecast accurately.

Forecasting many steps ahead from the same context avoids this (p. 7; Figure 6, p. 8, TimesFM-1.0-512 with horizon 1 vs 64).

### Statistical analysis, VUS-PR (Table 8, p. 24; excerpt in Table 3, p. 8)

Baseline: Var-$w$ (same $w$) for MOMENT, Last-3 for forecasting models.

| Configuration | Mean (TSFM) | Mean (baseline) | Correlation | p-value | Cohen's $d$ |
|---|---|---|---|---|---|
| MOMENT-base-64 | 0.412 | 0.414 | 0.994 | 0 | -0.048 |
| MOMENT-base-256 | 0.386 | 0.386 | 0.995 | 0 | -0.005 |
| MOMENT-base-512 | 0.311 | 0.313 | 0.991 | 7.91E-308 | -0.047 |
| MOMENT-large-64 | 0.427 | 0.414 | 0.926 | 2.90E-149 | 0.091 |
| MOMENT-large-256 | 0.389 | 0.386 | 0.848 | 1.87E-98 | 0.016 |
| MOMENT-large-512 | 0.313 | 0.313 | 0.857 | 1.38E-102 | 0.003 |
| MOMENT-large-1024 | 0.245 | 0.273 | 0.855 | 4.78E-101 | -0.180 |
| Chronos-Bolt-small-64 | 0.303 | 0.284 | 0.925 | 4.83E-149 | 0.152 |
| Chronos-Bolt-small-256 | 0.295 | 0.284 | 0.915 | 1.18E-139 | 0.083 |
| Chronos-Bolt-small-512 | 0.297 | 0.284 | 0.913 | 1.01E-137 | 0.095 |
| Chronos-Bolt-base-64 | 0.298 | 0.284 | 0.937 | 3.85E-161 | 0.123 |
| Chronos-Bolt-base-256 | 0.295 | 0.284 | 0.913 | 1.30E-137 | 0.076 |
| Chronos-Bolt-base-512 | 0.299 | 0.284 | 0.924 | 5.05E-148 | 0.113 |
| Time-MoE-base-64 | 0.301 | 0.284 | 0.917 | 1.36E-141 | 0.123 |
| Time-MoE-base-256 | 0.301 | 0.284 | 0.927 | 5.86E-151 | 0.136 |
| Time-MoE-base-512 | 0.301 | 0.284 | 0.930 | 1.08E-153 | 0.135 |
| Time-MoE-large-64 | 0.304 | 0.284 | 0.899 | 4.04E-127 | 0.135 |
| Time-MoE-large-256 | 0.299 | 0.284 | 0.919 | 8.87E-143 | 0.112 |
| Time-MoE-large-512 | 0.304 | 0.284 | 0.921 | 9.17E-145 | 0.155 |
| Times-FM-1.0-64 | 0.310 | 0.284 | 0.918 | 5.14E-142 | 0.194 |
| Times-FM-1.0-256 | 0.305 | 0.284 | 0.934 | 8.05E-158 | 0.175 |
| Times-FM-1.0-512 | 0.305 | 0.284 | 0.933 | 3.77E-157 | 0.172 |
| Times-FM-2.0-64 | 0.303 | 0.284 | 0.923 | 9.70E-147 | 0.144 |
| Times-FM-2.0-256 | 0.304 | 0.284 | 0.926 | 1.56E-149 | 0.156 |
| Times-FM-2.0-512 | 0.302 | 0.284 | 0.923 | 7.82E-147 | 0.142 |

**Non-inferiority margins** (Wilcoxon signed-rank, at least 95% confidence; p. 24): the TSFMs don't beat their baselines by more than

- 0.016 (MOMENT-large),
- 0.0008 (MOMENT-base),
- 0.008 (all forecasting-based TSFMs) in VUS-PR.

### Statistical analysis, Event-based F1 (Table 9, p. 25)

| Configuration | Mean (TSFM) | Mean (baseline) | Correlation | p-value | Cohen's $d$ |
|---|---|---|---|---|---|
| MOMENT-base-64 | 0.495 | 0.487 | 0.985 | 3.29e-270 | 0.118 |
| MOMENT-base-256 | 0.419 | 0.417 | 0.996 | 0 | 0.065 |
| MOMENT-base-512 | 0.345 | 0.345 | 0.994 | 0 | 0.008 |
| MOMENT-large-64 | 0.509 | 0.487 | 0.864 | 3.76e-106 | 0.106 |
| MOMENT-large-256 | 0.465 | 0.417 | 0.794 | 1.24e-77 | 0.199 |
| MOMENT-large-512 | 0.383 | 0.345 | 0.809 | 1.95e-82 | 0.179 |
| MOMENT-large-1024 | 0.287 | 0.300 | 0.866 | 1.11e-106 | -0.077 |
| Chronos-Bolt-small-64 | 0.633 | 0.619 | 0.840 | 6.50e-95 | 0.062 |
| Chronos-Bolt-small-256 | 0.636 | 0.619 | 0.864 | 4.41e-106 | 0.082 |
| Chronos-Bolt-small-512 | 0.625 | 0.619 | 0.842 | 1.35e-95 | 0.028 |
| Chronos-Bolt-base-64 | 0.623 | 0.619 | 0.900 | 4.33e-128 | 0.022 |
| Chronos-Bolt-base-256 | 0.626 | 0.619 | 0.868 | 2.44e-108 | 0.035 |
| Chronos-Bolt-base-512 | 0.621 | 0.619 | 0.863 | 1.19e-105 | 0.009 |
| Time-MoE-base-64 | 0.626 | 0.619 | 0.884 | 2.32e-117 | 0.040 |
| Time-MoE-base-256 | 0.650 | 0.619 | 0.875 | 9.24e-112 | 0.155 |
| Time-MoE-base-512 | 0.650 | 0.619 | 0.855 | 1.37e-101 | 0.146 |
| Time-MoE-large-64 | 0.635 | 0.619 | 0.887 | 6.05e-119 | 0.085 |
| Time-MoE-large-256 | 0.653 | 0.619 | 0.874 | 1.78e-111 | 0.171 |
| Time-MoE-large-512 | 0.660 | 0.619 | 0.850 | 2.23e-99 | 0.192 |
| Times-FM-1.0-64 | 0.632 | 0.619 | 0.853 | 2.04e-100 | 0.063 |
| Times-FM-1.0-256 | 0.644 | 0.619 | 0.866 | 3.87e-107 | 0.125 |
| Times-FM-1.0-512 | 0.638 | 0.619 | 0.880 | 4.23e-115 | 0.097 |
| Times-FM-2.0-64 | 0.631 | 0.619 | 0.880 | 5.67e-115 | 0.062 |
| Times-FM-2.0-256 | 0.636 | 0.619 | 0.860 | 3.14e-104 | 0.080 |
| Times-FM-2.0-512 | 0.633 | 0.619 | 0.860 | 3.51e-104 | 0.067 |

Non-inferiority margins for Event-based F1 (p. 24): 0.025 (MOMENT-large), 0.0001 (MOMENT-base), 0.02 (all forecasting-based TSFMs).

### TSPulse (Section 5.3, p. 8)

Mean VUS-PR on the TSB-AD-U evaluation set, TSPulse numbers taken from its own paper (Table 4, p. 8). Rows as printed (the first two reconstruction rows both read "Var-96†"):

| Reconstruction-based | VUS-PR | Forecasting-based | VUS-PR | Triangulation | Ensemble |
|---|---|---|---|---|---|
| Var-96† | 0.42 | Last-3 | 0.28 | 0.46 | 0.43 |
| Var-96† | 0.42 | Centered-5 | 0.29 | 0.47 | 0.44 |
| Head$_\text{time}$ | 0.42 | Head$_\text{future}$ | 0.3 | 0.48 | 0.44 |

† Window 96 because TSPulse computes reconstruction MSE "on only the last 96 data points of the 512-point context window" (p. 8).

**Our reading:** the triangulation and ensemble columns appear to combine the two entries of each row (baseline pairs in the first two rows, TSPulse heads in the third).
The paper says only that triangulating or ensembling the two baselines performs similarly to doing so with the heads (p. 8).

### Non-TSFM detectors vs the baselines (Section 5.4, p. 8; Appendix K, p. 26)

VUS-PR scores from Liu & Paparrizos (2024); Var uses the detector's window size, or Var-64 when the detector has none (Table 10, p. 26). Correlation of per-series VUS-PR:

| Detector | with Var | with Last-3 |
|---|---|---|
| Sub-IForest | 0.301 | 0.279 |
| IForest | 0.534 | 0.628 |
| Sub-LOF | -0.088 | 0.140 |
| LOF | 0.395 | 0.654 |
| POLY | 0.795 | 0.436 |
| MatrixProfile | -0.034 | 0.242 |
| KShapeAD | -0.107 | 0.092 |
| SAND | -0.063 | 0.097 |
| Series2Graph | 0.464 | 0.338 |
| SR | 0.556 | 0.805 |
| Sub-PCA | 0.470 | 0.203 |
| Sub-HBOS | 0.285 | 0.250 |
| Sub-OCSVM | 0.104 | 0.213 |
| Sub-MCD | -0.046 | 0.293 |
| Sub-KNN | -0.045 | 0.075 |
| KMeansAD | -0.040 | 0.185 |
| AutoEncoder | 0.378 | 0.361 |
| CNN | 0.660 | 0.704 |
| LSTMAD | 0.518 | 0.587 |
| TranAD | 0.472 | 0.464 |
| AnomalyTransformer | 0.415 | 0.491 |
| OmniAnomaly | 0.494 | 0.435 |
| USAD | 0.615 | 0.277 |
| Donut | 0.580 | 0.527 |
| TimesNet | 0.805 | 0.724 |
| FITS | 0.773 | 0.621 |

"Unlike the TSFMs, the correlation with the baselines is low for the vast majority of non-TSFM anomaly detectors".

The exceptions with high correlation to Var, e.g. TimesNet, "also employ z-normalization" (p. 8).

### Normalization ablation (p. 6, p. 7; Appendix I, Figure 17, p. 23)

Share of series with $y \approx x$ / $y > x$ / $y < x$, as printed in the legends (Figure 17, p. 23):

| Model (baseline) | Window-wise Z-norm | Window-wise Min-Max | Global Z-norm | Window-wise mean scaling |
|---|---|---|---|---|
| MOMENT-base-64 (Var-64) | 97 / 2 / 1 | 86 / 7 / 7 | 66 / 20 / 14 | — |
| Time-MoE-base-64 (Last-3) | 85 / 6 / 9 | 85 / 5 / 9 | 87 / 5 / 8 | — |
| TimesFM-2.0-512 (Last-3) | 85 / 6 / 9 | 85 / 6 / 9 | 85 / 6 / 9 | — |
| Chronos-Bolt-base-64 (Last-3) | 86 / 6 / 8 | — | — | — |
| Chronos-t5-base-64 (Last-3) | — | — | — | 85 / 11 / 5 |

"When employing normalization methods other than window-wise Z-norm, the correlation with baselines diminishes for reconstruction-based models but persists for forecasting-based models" (Figure 17 caption, p. 23).

The paper doesn't report whether MOMENT's VUS-PR improves with the other normalizations.

### Dataset labeling flaws and metric exaggeration (Appendix H, pp. 21–22)

- **Case TSB-AD-U 534 (SMAP)** (Figure 15, p. 21):
  - every point is −1 except one equal to 1;
  - the ground truth marks an anomaly from 16 steps before the spike to 34 steps after.
  - TimeMoE-large-512 gets VUS-PR 0.51, Last-1 only 0.05 (p. 21).
- **Problematic labeling:** it's unclear why the points around the spike are anomalous, and why more after than before (p. 21).
- **Exaggerating metric:** the gap comes from "tiny bumps at the level of $10^{-5}$" in Time-MoE's scores just after the spike, where Last-1 gives exact zeros.
  - Since VUS-PR only depends on the ranking of scores, these bumps raise its VUS-PR substantially (p. 21).
- **50 problematic series** found in the TSB-AD-U evaluation set (Table 7, p. 21):
  - 47 with "anomalous labels (often arbitrarily) overlapping with normal regions",
  - 3 from UCR with "off-by-one mislabeling".
  - The paper doesn't say whether Table 7's "Index" values are TSB-AD-U IDs.
  - They don't match the IDs used in the figures (e.g. the SMAP case study is series 534, Figure 15, while Table 7 lists SMAP as 245–261), so the flagged series can't yet be located in the benchmark.

| Dataset | Index | Problem |
|---|---|---|
| NAB | 0–22 | Anomalous labeling overlapping with normal regions |
| SMAP | 245–261 | same |
| SWAT | 262 | same |
| MSL | 43, 45, 47, 48 | same |
| SMD | 68, 74 | same |
| UCR | 212, 221, 228 | Off-by-one mislabeling |

- Removing them further narrows the gap between forecasting TSFMs and the squared-difference baseline (p. 22).
- TimesFM-2.0-512 vs each baseline, $y \approx x$ / $y > x$ / $y < x$ (Figure 16, p. 22):

| Baseline | Without problematic series | With problematic series |
|---|---|---|
| Last-1 | 85% / 3% / 13% | 82% / 3% / 15% |
| Last-3 | 88% / 7% / 5% | 85% / 6% / 9% |
| Centered-5 | 89% / 5% / 6% | 86% / 5% / 9% |

### Future directions with evidence (Section 6, pp. 8–10; Appendix L, p. 27)

**1. Combine short and long horizons** (Section 6.1, p. 9). VUS-PR of TimesFM-1.0-512 for increasing horizon $h$ (Table 6, p. 9):

| ID | Anomaly | h=1 | h=2 | h=4 | h=8 | h=16 | h=32 | h=64 | h=128 |
|---|---|---|---|---|---|---|---|---|---|
| 371 | Sequence (length 170) | 0.04 | 0.1 | 0.21 | 0.27 | 0.36 | 0.46 | 0.65 | 0.68 |
| 603 | Point | 1.0 | 0.8 | 0.9 | 0.94 | 0.9 | 0.47 | 0.27 | 0.02 |

- Longer horizons help longer anomalies and hurt shorter ones; "the optimal forecasting horizon correlates with the anomaly length"
  (p. 27; Figures 7, p. 9, and 18, p. 27, for TimesFM-1.0/2.0-512 and Chronos-Bolt-small/base-512, anomaly lengths grouped as 1, 2–64, 65–256, 257-).
- On TSB-AD-U 558 (Yahoo), with one sequence and one point anomaly, $h = 1$ and $h = 64$ each miss one; their `MAX` ensemble finds both (p. 9; Figure 8a, p. 10).
  - No aggregate number for the ensemble is given.

**2. Detect anomalies in hidden representations** (Section 6.2, p. 10). On TSB-AD-U 474 (UCR):

- MOMENT-base-64 with reconstruction error scores VUS-PR 0.003, rank 31st of 32 detectors;
- a KNN on MOMENT's hidden representations scores 0.250, rank 5th in the benchmark of Liu & Paparrizos (2024);
- "other detectors (e.g., KMeansAD) achieve even higher performance" (p. 10, Figure 8b).

One series only.

**3. Fine-tune with labeled anomalies** (Section 6.3, p. 10):

- the pre-training objective "is not aligned with detecting anomalies";
- fine-tuning on the pre-training task "only enhances forecasting or reconstruction performance";
- end-to-end fine-tuning with labeled anomalies is proposed, by analogy with sequence labeling in NLP, and possibly needing only a limited number of anomalous events.

"A comprehensive study of this paradigm is beyond the scope of the present work" (p. 10). No experiment.

### Multivariate (Appendix M, p. 28)

Chronos-2-512 and Toto-Open-Base-1.0-512 give anomaly scores similar to Last-3 on eight TSB-AD-M series (Figure 19, p. 28); qualitative only.

## Assumptions and limitations

Stated or visible in the paper:

- **Univariate, zero-shot only** (p. 2, p. 5); the multivariate evidence is qualitative and called "preliminary" (p. 2, p. 28).
- **One benchmark, one main metric:** TSB-AD-U evaluation set, VUS-PR, with Event-based F1 as a check (p. 5, p. 24).
- **TSPulse is not rerun:** its numbers are copied from its paper (p. 8).
- **The future directions are not evaluated at scale:**
  - the horizon ensemble and the hidden-representation KNN are shown on single series (pp. 9–10; aggregate per-horizon curves exist, but not for the ensemble),
  - and labeled-anomaly fine-tuning is left out of scope (p. 10).
- **The benchmark's labels are flawed** in at least 50 of 350 series (p. 21), yet the main tables use all 350 (Table 8, p. 24).
  - The cleaned comparison is shown only for TimesFM-2.0-512 (Figure 16, p. 22).
- **Code and raw scores** were not released with the submission (p. 14).

**Our reading:**

- The main TSFM result is "not significantly better", not "worse":
  - all 18 forecasting configurations have a slightly higher mean VUS-PR than Last-3 (0.295–0.310 vs 0.284, Table 8, p. 24),
  - and the non-inferiority tests bound the advantage at small margins (p. 24) rather than showing equivalence.
- Very small p-values here test correlation, not a difference in performance.
  - The difference is described by Cohen's $d$ and the non-inferiority margins (p. 24).
- The paper reports no point-adjusted F1, AUROC or affiliation metrics, and no thresholding protocol, so it says nothing directly about the known inflation of point-adjusted F1.
  - Its metric warning is a different one: rank-based metrics (VUS-PR, AUC-PR) can be moved by score differences of order $10^{-5}$ (p. 21).
- The variance explanation is shown for window-wise z-normalized reconstruction (MOMENT).
  - The TimesNet correlation with Var (0.805, p. 26) suggests the same mechanism can affect any z-normalizing reconstruction or forecasting model, but the paper only states the shared z-normalization (p. 8).
- The paper is under review; numbers or conclusions may change in a later version.

## Relevance to this thesis

**Our reading:**

- **Baselines to always include.**
  - Any anomaly-detection result in the thesis (joint training, task arithmetic, continual strategies) should be compared with Var-$w$ and Last-$w$ / Centered-$w$ (Definitions 4–5, pp. 4–5):
    they cost nothing and, on TSB-AD-U, match four TSFM families (Table 8, p. 24) and TSPulse (Table 4, p. 8).
  - A merging method that only matches a one-liner hasn't shown it detects anything.
- **Check for the variance shortcut.**
  - If our models use per-window z-normalization (as reversible instance normalization does), Eq. 1 (p. 6) predicts a reconstruction score close to window variance times a near-constant error.
  - Reporting the per-series correlation with Var-$w$ (as in Tables 8 and 10) is a cheap diagnostic of whether a model has learned anything beyond variance.
- **Compare per series, not only on averages.**
  - The paper's protocol — one-to-one plots, correlation, Cohen's $d$, Wilcoxon non-inferiority with a stated margin (pp. 6–7, p. 24) — is a ready rule for "when a difference is real" between joint training and merged models.
- **Metric choice.**
  - VUS-PR is threshold-free and is the paper's main metric (p. 5), but it is rank-based and sensitive to tiny score differences (p. 21).
  - Our evaluation should state the metric, its threshold rule if any, and whether point adjustment is used.
  - This paper gives no guidance on point adjustment.
- **Dataset caveats.**
  - Of the datasets this project may use, SMAP, MSL, SMD, SWaT and NAB all have series flagged for problematic labels in TSB-AD-U (Table 7, p. 21).
  - Results on them should be checked with and without the flagged series.
- **Forecasting horizon** matters for forecasting-based detection: one-step error favors point anomalies, longer horizons favor sequence anomalies (Table 6, p. 9).
  - If the thesis uses forecasting error as an anomaly score, the horizon is a design choice to record and possibly to ensemble.
- **Fine-tuning direction.**
  - The paper argues that pre-training-task fine-tuning doesn't align a model with detection (p. 10).
  - Our fine-tuned task vectors are trained on the same proxy objectives, so whether merging them yields detection ability beyond the one-liners is an open question to test, not to assume.

## Quotes worth keeping

> "We find that for each model family using varying model sizes and context window lengths, anomaly detection performance does not significantly differ to simple one-liner baselines: moving-window variance and squared-difference." (p. 1)

> "anomalies are not consistently harder to reconstruct or forecast." (p. 1)

> "As a result, the anomaly scores can be decomposed as the product of the variance of the window ($\sigma_i^2$) and the reconstruction MSEs of the normalized window ($T^{\text{norm}}_{i,i+w-1}$)." (p. 5)

> "As a result, even anomalous values are usually not “unexpected” with regards to the context window, allowing the TSFM to forecast them accurately (see Figure 6)." (p. 7)

> "Because VUS-PR (Paparrizos et al., 2022), like its parent AUC-PR, only cares about the relative ranking of the scores rather than their actual values, these tiny bumps result in a significantly higher VUS-PR for TimeMoE." (p. 21)

> "Our inspection identified 50 time series with problematic labeling in the TSB-AD-U evaluation set." (p. 21)

> "Further fine-tuning on the pre-training task does not address this misalignment, as it only enhances forecasting or reconstruction performance rather than the models' anomaly detection capabilities." (p. 10)

> "We also emphasized the importance of visually analyzing both data and algorithm outputs, because aggregated evaluation metrics often hide the true strengths and weaknesses of an algorithm." (p. 10)
