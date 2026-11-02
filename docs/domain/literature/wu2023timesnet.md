# wu2023timesnet — TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis

- **Status:** verified (2026-11-02): checked against the paper and its text layer by an independent agent (about 150 claims, every cell of 10 tables correct: 4 misstatements, 3 unsupported details, 2 wrong pages, 3 unreported inconsistencies and 5 protocol gaps, all fixed)
- **Reference:** Wu, Hu, Liu, Zhou, Wang, Long; ICLR 2023; arXiv 2210.02186 ([references.bib](../references.bib))
- **Version read:** arXiv v3 (12 Apr 2023), 23 pages: main text pp. 1–9, acknowledgments and references pp. 10–12, appendix pp. 12–23
- **Read:** all 23 pages: main text in full; appendix A (implementation details, metrics, Tables 6–7, pp. 12–14), B (sensitivity to $k$, pp. 13–15), C (ablations, Tables 8–10, pp. 15–16), D (representation analysis, p. 16), E (multi-periodicity, p. 17), F (showcases, pp. 17–18), G (efficiency, Table 11, pp. 17–19), H (mixed-dataset training, Table 12, p. 20), I (full results, Tables 13–17, pp. 20–23). References (pp. 10–12) only skimmed, for the dataset sources. The showcase plots (Figures 9, 11–13) were looked at but not transcribed
- **Code:** <https://github.com/thuml/TimesNet> (p. 1, abstract)

## In one paragraph

TimesNet is a task-general backbone for time series (p. 1). Its premise is that real series are **multi-periodic**, and that each time point varies both within its period (**intraperiod-variation**, short-term) and across periods at the same phase (**interperiod-variation**, long-term) (p. 2). Each **TimesBlock** finds the $k$ dominant periods with an FFT, reshapes the 1D series into $k$ 2D tensors (columns: within a period; rows: same phase across periods), processes them with a shared, parameter-efficient **inception block** of 2D kernels, reshapes back, and sums the $k$ results weighted by the softmax of their FFT amplitudes (pp. 3–5). The paper reports state-of-the-art results on five tasks: long- and short-term forecasting, imputation, classification and anomaly detection (p. 6; Figure 4, p. 6; Table 11, p. 19). For anomaly detection, all models share the same criterion, the reconstruction error, and TimesNet reaches an average F1 of 85.49% with the inception block and 86.34% with a ResNeXt block (Table 5, p. 9).

## Problem

Modeling **temporal variation**, which the authors call "the common key problem of extensive analysis tasks" (p. 1). A single time point carries little information; what matters is how values vary over time, and real-world variations mix and overlap (p. 1). RNNs struggle with long-term dependencies, 1D convolutions only model adjacent points, and attention "is hard ... to find out reliable dependencies directly from scattered time points" (pp. 1–2).

**Setting:** a length-$T$ series with $C$ recorded variates, $\mathbf{X}_{\text{1D}} \in \mathbb{R}^{T \times C}$ (p. 3); one backbone for five tasks; the input embedding and output projection layers are kept the same across base models (p. 12), and forecasting adds an MLP initialization (p. 12).

## Method

### Period discovery with the FFT

For the input $\mathbf{X}_{\text{1D}} \in \mathbb{R}^{T \times C}$ (Equation 1, p. 3):

$$\mathbf{A} = \operatorname{Avg}\Big(\operatorname{Amp}\big(\operatorname{FFT}(\mathbf{X}_{\text{1D}})\big)\Big), \quad \{f_1, \dots, f_k\} = \underset{f_* \in \{1, \dots, [\frac{T}{2}]\}}{\arg\operatorname{Topk}}(\mathbf{A}), \quad p_i = \left\lceil \frac{T}{f_i} \right\rceil, \; i \in \{1, \dots, k\}$$

- $\mathbf{A} \in \mathbb{R}^T$ is the amplitude of each frequency, averaged over the $C$ variates by $\operatorname{Avg}(\cdot)$; $\mathbf{A}_j$ is the intensity of the frequency-$j$ basis function, whose period length is $\lceil T/j \rceil$ (p. 4).
- Only the top-$k$ amplitudes are kept, "considering the sparsity of frequency domain and to avoid the noises brought by meaningless high frequencies"; $k$ is a hyperparameter (p. 4).
- Only frequencies in $\{1, \dots, [T/2]\}$ are considered, because of the conjugacy of the frequency domain (p. 4).
- Summarized as (Equation 2, p. 4):

$$\mathbf{A}, \{f_1, \dots, f_k\}, \{p_1, \dots, p_k\} = \operatorname{Period}(\mathbf{X}_{\text{1D}})$$

### 1D → 2D reshaping

For each selected frequency (Equation 3, p. 4):

$$\mathbf{X}^i_{\text{2D}} = \operatorname{Reshape}_{p_i, f_i}\big(\operatorname{Padding}(\mathbf{X}_{\text{1D}})\big), \quad i \in \{1, \dots, k\}$$

- $\operatorname{Padding}(\cdot)$ extends the series with zeros along time so it fits the reshape (p. 4).
- $\mathbf{X}^i_{\text{2D}} \in \mathbb{R}^{p_i \times f_i \times C}$: $p_i$ rows and $f_i$ columns; in the paper's words, its "columns and rows represent the intraperiod-variation and interperiod-variation under the corresponding period length $p_i$ respectively" (p. 4).
- The result is a set of $k$ 2D tensors $\{\mathbf{X}^1_{\text{2D}}, \dots, \mathbf{X}^k_{\text{2D}}\}$, one per period (p. 4).
- The reshape gives two kinds of locality, adjacent time points (columns) and adjacent periods (rows), so 2D kernels can process it (p. 4).
- Series without clear periodicity: their variation is "dominated by the intraperiod-variation and is equivalent to the ones with infinite period length" (p. 2); the model then learns the most significant frequency as 1, and the trend is covered by intraperiod modeling (p. 15).

### TimesNet: residual stack of TimesBlocks

The raw input is first embedded, $\mathbf{X}^0_{\text{1D}} = \operatorname{Embed}(\mathbf{X}_{\text{1D}}) \in \mathbb{R}^{T \times d_{\text{model}}}$; layer $l$ then computes (Equation 4, p. 4):

$$\mathbf{X}^l_{\text{1D}} = \operatorname{TimesBlock}\big(\mathbf{X}^{l-1}_{\text{1D}}\big) + \mathbf{X}^{l-1}_{\text{1D}}$$

The embedding layer itself isn't specified further in the paper.

### Inside a TimesBlock: capturing 2D-variations

Periods are re-estimated **from the deep features of each layer**, not only from the raw input (Equation 5, p. 5):

$$
\begin{aligned}
\mathbf{A}^{l-1}, \{f_1, \dots, f_k\}, \{p_1, \dots, p_k\} &= \operatorname{Period}\big(\mathbf{X}^{l-1}_{\text{1D}}\big), \\
\mathbf{X}^{l,i}_{\text{2D}} &= \operatorname{Reshape}_{p_i, f_i}\big(\operatorname{Padding}(\mathbf{X}^{l-1}_{\text{1D}})\big), \quad i \in \{1, \dots, k\} \\
\widehat{\mathbf{X}}^{l,i}_{\text{2D}} &= \operatorname{Inception}\big(\mathbf{X}^{l,i}_{\text{2D}}\big), \quad i \in \{1, \dots, k\} \\
\widehat{\mathbf{X}}^{l,i}_{\text{1D}} &= \operatorname{Trunc}\Big(\operatorname{Reshape}_{1,(p_i \times f_i)}\big(\widehat{\mathbf{X}}^{l,i}_{\text{2D}}\big)\Big), \quad i \in \{1, \dots, k\}
\end{aligned}
$$

- $\mathbf{X}^{l,i}_{\text{2D}} \in \mathbb{R}^{p_i \times f_i \times d_{\text{model}}}$; $\widehat{\mathbf{X}}^{l,i}_{\text{1D}} \in \mathbb{R}^{T \times d_{\text{model}}}$ (p. 5).
- $\operatorname{Inception}(\cdot)$ is a parameter-efficient inception block (Szegedy et al., 2015) with multi-scale 2D kernels (p. 5). Its kernel sizes and number of branches aren't given in the paper.
- $\operatorname{Trunc}(\cdot)$ truncates the padded series of length $p_i \times f_i$ back to $T$ (p. 5).
- **One shared inception block** for all $k$ tensors, "to improve parameter efficiency, which can make the model size invariant to the selection of hyper-parameter $k$" (p. 5).

### Adaptive aggregation

The $k$ 1D outputs are fused with weights from the amplitudes of their frequencies, an idea taken from Auto-Correlation (Wu et al., 2021) (Equation 6, p. 5):

$$
\widehat{\mathbf{A}}^{l-1}_{f_1}, \dots, \widehat{\mathbf{A}}^{l-1}_{f_k} = \operatorname{Softmax}\big(\mathbf{A}^{l-1}_{f_1}, \dots, \mathbf{A}^{l-1}_{f_k}\big), \qquad
\mathbf{X}^l_{\text{1D}} = \sum_{i=1}^{k} \widehat{\mathbf{A}}^{l-1}_{f_i} \times \widehat{\mathbf{X}}^{l,i}_{\text{1D}}
$$

**Our reading:** Equations 4 and 6 both write the output as $\mathbf{X}^l_{\text{1D}}$; Equation 6 gives the TimesBlock output, to which Equation 4 adds the residual input. Figure 3 (p. 5) draws the residual sum after the aggregation.

### Generality in 2D vision backbones

The inception block can be replaced by any 2D vision backbone (ResNet, ResNeXt, ConvNeXt, attention-based models; p. 5, with Swin named on p. 15 and in Table 8); the main experiments use the inception block for its balance of performance and efficiency (p. 5; Figure 4 right, p. 6).

## Experimental setup

### Common implementation (Appendix A, pp. 12–14)

- All experiments repeated three times; PyTorch; a single NVIDIA TITAN RTX 24GB GPU (p. 12).
- Width from the number of variates $C$ (p. 12; Table 7, p. 14): $d_{\text{model}} = \min\{\max\{2^{\lceil \log C \rceil}, d_{\min}\}, d_{\max}\}$. The base of the logarithm isn't stated.
- Optimizer: Adam with $(\beta_1, \beta_2) = (0.9, 0.999)$ (Table 7, p. 14).
- Baselines reproduced from the configurations of their papers or official code; for a fair comparison, the **input embedding and the final projection layer are the same for all base models**, so only the base model differs (p. 12).
- **Forecasting:** "especially for the forecasting task", an MLP on the temporal dimension initializes the predicted future; the next sentence adds the Series Stationarization of the Non-stationary Transformer "to eliminate the affect the distribution shift" (p. 12). **Our reading:** whether Stationarization (and the MLP initialization) also applies to other tasks, anomaly detection included, is ambiguous in the text.

**Hyperparameters** (Table 7, p. 14; LR is the initial learning rate):

| Task | $k$ (Eq. 1) | Layers | $d_{\min}$ | $d_{\max}$ | LR | Loss | Batch size | Epochs |
|---|---|---|---|---|---|---|---|---|
| Long-term forecasting | 5 | 2 | 32 | 512 | $10^{-4}$ | MSE | 32 | 10 |
| Short-term forecasting | 5 | 2 | 16 | 64 | $10^{-3}$ | SMAPE | 16 | 10 |
| Imputation | 3 | 2 | 64 | 128 | $10^{-3}$ | MSE | 16 | 10 |
| Classification | 3 | 2 | 32 | 64 | $10^{-3}$ | Cross Entropy | 16 | 30 |
| Anomaly detection | 3 | 3 | 32 | 128 | $10^{-4}$ | MSE | 128 | 10 |

The text of Appendix B states $k = 3$ for imputation, classification and anomaly detection and $k = 5$ for short-term forecasting (p. 15); the $k = 5$ for long-term forecasting comes from Table 7 only (p. 14).

**Benchmarks** (Table 1, p. 6):

| Task | Benchmarks | Metrics | Series length |
|---|---|---|---|
| Long-term forecasting | ETT (4 subsets), Electricity, Traffic, Weather, Exchange, ILI | MSE, MAE | 96~720 (ILI: 24~60) |
| Short-term forecasting | M4 (6 subsets) | SMAPE, MASE, OWA | 6~48 |
| Imputation | ETT (4 subsets), Electricity, Weather | MSE, MAE | 96 |
| Classification | UEA (10 subsets) | Accuracy | 29~1751 |
| Anomaly detection | SMD, MSL, SMAP, SWaT, PSM | Precision, Recall, F1-Score | 100 |

**Baselines:** more than 15, including LSTM, LSTNet, LSSL (RNN); TCN (CNN); LightTS, DLinear (MLP); Reformer, Informer, Pyraformer, Autoformer, FEDformer, Non-stationary Transformer, ETSformer (Transformer); plus task-specific ones: N-HiTS and N-BEATS (short-term forecasting), Anomaly Transformer (anomaly detection), Rocket and Flowformer (classification) (p. 6).

### Anomaly detection protocol

- **Task:** unsupervised detection of abnormal time points, because labels are hard to obtain (p. 8).
- **Datasets** (p. 8; Table 6, p. 14), with sizes as (train, validation, test):

  | Dataset | Domain (p. 8) | Information (Table 6) | Dim | Series length | Size (train, val, test) |
  |---|---|---|---|---|---|
  | SMD (Su et al., 2019) | service monitoring | Server Machine | 38 | 100 | (566724, 141681, 708420) |
  | MSL (Hundman et al., 2018) | space & earth exploration | Spacecraft | 55 | 100 | (44653, 11664, 73729) |
  | SMAP (Hundman et al., 2018) | space & earth exploration | Spacecraft | 25 | 100 | (108146, 27037, 427617) |
  | SWaT (Mathur & Tippenhauer, 2016) | water treatment | Infrastructure | 51 | 100 | (396000, 99000, 449919) |
  | PSM (Abdulaal et al., 2021) | service monitoring | Server Machine | 25 | 100 | (105984, 26497, 87841) |

- **Pre-processing:** "Following the pre-processing methods in Anomaly Transformer (2021), we split the dataset into consecutive non-overlapping segments by sliding window" (p. 8); the window (series) length is 100 (Table 1, p. 6; Table 6, p. 14).
- **Criterion:** the models are trained to reconstruct their input, and "the reconstruction error is a natural anomaly criterion"; "we only change the base models for reconstruction and use the classical reconstruction error as the shared anomaly criterion for all experiments" (p. 8). Training loss: MSE (Table 7, p. 14).
- **Anomaly Transformer as a baseline:** its joint criterion (association discrepancy and reconstruction error) is replaced by the reconstruction error alone (Table 5 footnote, p. 9; Table 15 footnote, p. 22).
- **Metrics:** precision, recall and F1-score, in %; F1 is the harmonic mean of precision and recall (p. 13; Table 15 caption, p. 22).
- **Not stated in the paper:** how the reconstruction error is turned into a per-point score (e.g. which norm, averaged over variates or not), how the **threshold** is chosen, and whether **point adjustment** is applied. The paper only points to the pre-processing of Anomaly Transformer (p. 8). Also not stated: what the anomaly-detection validation split (sizes in Table 6, p. 14) is used for (early stopping, threshold); the stride of the "consecutive non-overlapping segments by sliding window" (p. 8) at train and test time, and how per-window errors map back to time points; any normalization for anomaly detection; how the multi-entity SMD, MSL and SMAP are combined.
- **Our reading:** Table 8 shows ConvNeXt as the best 2D backbone (average F1 86.89), but Table 5 headlines ResNeXt (86.34) without explanation; and the mixed-dataset experiment of Table 12 is framed as a test of "large-scale pre-training" capacity (p. 20), which matters when citing it as joint training.
- **Our reading:** the threshold rule and any point adjustment must come from the Anomaly Transformer protocol or the released code; neither can be confirmed from this paper. This matters for comparing against these F1 values, since point adjustment inflates F1 strongly.

### Forecasting protocol

- **Long-term:** the benchmarks of Autoformer: ETT (ETTm1, ETTm2, ETTh1, ETTh2), Electricity (UCI), Traffic (PeMS), Weather (Wetterstation), Exchange, ILI (CDC) (p. 6). Each dataset is one continuous series, from which samples are taken by a sliding window (p. 6).
- **Input length 96 (ILI: 36); prediction lengths $\{96, 192, 336, 720\}$ (ILI: $\{24, 36, 48, 60\}$)** (Table 2 caption, p. 7; Table 13 caption, p. 21).
- **Short-term:** M4, yearly, quarterly, monthly (p. 6) and other (Table 14, p. 22; six subsets in Table 6, p. 14) univariate marketing series, 100,000 series in total; prediction lengths in $[6, 48]$ (p. 6; Table 3, p. 7).
- **Long-term datasets** (Table 6, p. 14; dimension, size as (train, validation, test), information as printed):

  | Dataset | Dim | Size (train, val, test) | Information (frequency) |
  |---|---|---|---|
  | ETTm1, ETTm2 | 7 | (34465, 11521, 11521) | Electricity (15 mins) |
  | ETTh1, ETTh2 | 7 | (8545, 2881, 2881) | Electricity (15 mins) |
  | Electricity | 321 | (18317, 2633, 5261) | Electricity (Hourly) |
  | Traffic | 862 | (12185, 1757, 3509) | Transportation (Hourly) |
  | Weather | 21 | (36792, 5271, 10540) | Weather (10 mins) |
  | Exchange | 8 | (5120, 665, 1422) | Exchange rate (Daily) |
  | ILI | 7 | (617, 74, 170) | Illness (Weekly) |

  **Our reading:** Table 6 lists ETTh1/ETTh2 as "15 mins", while Appendix H calls them "hourly-collected" (p. 20); the 15-minute label looks like a typo. Table 6 also lists Electricity as "Hourly" in the long-term forecasting block and "15 mins" in the imputation block (p. 14).

- **Metrics** (p. 13): MSE and MAE for long-term forecasting (and imputation). For short-term forecasting, following N-BEATS, with $H$ future points, $m$ the periodicity of the data and $\mathbf{X}, \widehat{\mathbf{X}} \in \mathbb{R}^{H \times C}$ ground truth and prediction:

$$\text{SMAPE} = \frac{200}{H} \sum_{i=1}^{H} \frac{|\mathbf{X}_i - \widehat{\mathbf{X}}_i|}{|\mathbf{X}_i| + |\widehat{\mathbf{X}}_i|}, \qquad \text{MAPE} = \frac{100}{H} \sum_{i=1}^{H} \frac{|\mathbf{X}_i - \widehat{\mathbf{X}}_i|}{|\mathbf{X}_i|}$$

$$\text{MASE} = \frac{1}{H} \sum_{i=1}^{H} \frac{|\mathbf{X}_i - \widehat{\mathbf{X}}_i|}{\frac{1}{H-m} \sum_{j=m+1}^{H} |\mathbf{X}_j - \mathbf{X}_{j-m}|}, \qquad \text{OWA} = \frac{1}{2}\left[\frac{\text{SMAPE}}{\text{SMAPE}_{\text{Naïve2}}} + \frac{\text{MASE}}{\text{MASE}_{\text{Naïve2}}}\right]$$

### Other tasks (briefly)

- **Imputation:** ETT, Electricity, Weather; length-96 series with time points randomly masked at $\{12.5\%, 25\%, 37.5\%, 50\%\}$ (p. 7; Table 4, p. 8).
- **Classification:** 10 multivariate UEA datasets, pre-processed as in Zerveas et al. (2021) (p. 7).

## Results

### Anomaly detection

**Full results** (Table 15, p. 22; Table 5, p. 9, gives the F1 columns). Precision P, recall R and F1, in %; only the F1 and average F1 columns are marked, best in bold red and second underlined (P and R maxima are unmarked). Two inconsistencies as printed: the Stationary model's SMD F1 is 84.72 in Table 5 (p. 9) and 84.62 in Table 15 (p. 22; the table below uses 84.62, which fits its 82.08 average); and Table 15 underlines DLinear's MSL F1 (84.88) though ETSformer's is higher (85.03), which Table 5 underlines correctly:

| Model | SMD P | SMD R | SMD F1 | MSL P | MSL R | MSL F1 | SMAP P | SMAP R | SMAP F1 | SWaT P | SWaT R | SWaT F1 | PSM P | PSM R | PSM F1 | Avg F1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LSTM (1997) | 78.52 | 65.47 | 71.41 | 78.04 | 86.22 | 81.93 | 91.06 | 57.49 | 70.48 | 78.06 | 91.72 | 84.34 | 69.24 | 99.53 | 81.67 | 77.97 |
| Transformer (2017) | 83.58 | 76.13 | 79.56 | 71.57 | 87.37 | 78.68 | 89.37 | 57.12 | 69.70 | 68.84 | 96.53 | 80.37 | 62.75 | 96.56 | 76.07 | 76.88 |
| LogTrans (2019) | 83.46 | 70.13 | 76.21 | 73.05 | 87.37 | 79.57 | 89.15 | 57.59 | 69.97 | 68.67 | 97.32 | 80.52 | 63.06 | 98.00 | 76.74 | 76.60 |
| TCN (2019) | 84.06 | 79.07 | 81.49 | 75.11 | 82.44 | 78.60 | 86.90 | 59.23 | 70.45 | 76.59 | 95.71 | 85.09 | 54.59 | 99.77 | 70.57 | 77.24 |
| Reformer (2020) | 82.58 | 69.24 | 75.32 | 85.51 | 83.31 | 84.40 | 90.91 | 57.44 | 70.40 | 72.50 | 96.53 | 82.80 | 59.93 | 95.38 | 73.61 | 77.31 |
| Informer (2021) | 86.60 | 77.23 | 81.65 | 81.77 | 86.48 | 84.06 | 90.11 | 57.13 | 69.92 | 70.29 | 96.75 | 81.43 | 64.27 | 96.33 | 77.10 | 78.83 |
| Anomaly Transformer* (2021) | 88.91 | 82.23 | 85.49 | 79.61 | 87.37 | 83.31 | 91.85 | 58.11 | 71.18 | 72.51 | 97.32 | 83.10 | 68.35 | 94.72 | 79.40 | 80.50 |
| Pyraformer (2021a) | 85.61 | 80.61 | 83.04 | 83.81 | 85.93 | 84.86 | 92.54 | 57.71 | 71.09 | 87.92 | 96.00 | 91.78 | 71.67 | 96.02 | 82.08 | 82.57 |
| Autoformer (2021) | 88.06 | 82.35 | 85.11 | 77.27 | 80.92 | 79.05 | 90.40 | 58.62 | 71.12 | 89.85 | 95.81 | 92.74 | 99.08 | 88.15 | 93.29 | 84.26 |
| LSSL (2022) | 78.51 | 65.32 | 71.31 | 77.55 | 88.18 | 82.53 | 89.43 | 53.43 | 66.90 | 79.05 | 93.72 | 85.76 | 66.02 | 92.93 | 77.20 | 76.74 |
| Stationary (2022a) | 88.33 | 81.21 | 84.62 | 68.55 | 89.14 | 77.50 | 89.37 | 59.02 | 71.09 | 68.03 | 96.75 | 79.88 | 97.82 | 96.76 | 97.29 | 82.08 |
| DLinear (2023) | 83.62 | 71.52 | 77.10 | 84.34 | 85.42 | 84.88 | 92.32 | 55.41 | 69.26 | 80.91 | 95.30 | 87.52 | 98.28 | 89.26 | 93.55 | 82.46 |
| ETSformer (2022) | 87.44 | 79.23 | 83.13 | 85.13 | 84.93 | 85.03 | 92.25 | 55.75 | 69.50 | 90.02 | 80.36 | 84.91 | 99.31 | 85.28 | 91.76 | 82.87 |
| LightTS (2022) | 87.10 | 78.42 | 82.53 | 82.40 | 75.78 | 78.95 | 92.58 | 55.27 | 69.21 | 91.98 | 94.72 | **93.33** | 98.37 | 95.97 | 97.15 | 84.23 |
| FEDformer (2022) | 87.95 | 82.39 | 85.08 | 77.14 | 80.07 | 78.57 | 90.47 | 58.10 | 70.76 | 90.17 | 96.42 | 93.19 | 97.31 | 97.16 | 97.23 | 84.97 |
| TimesNet (Inception) | 87.76 | 82.63 | 85.12 | 82.97 | 85.42 | 84.18 | 91.50 | 57.80 | 70.85 | 88.31 | 96.24 | 92.10 | 98.22 | 92.21 | 95.21 | 85.49 |
| TimesNet (ResNeXt) | 88.66 | 83.14 | **85.81** | 83.92 | 86.42 | **85.15** | 92.52 | 58.29 | **71.52** | 86.76 | 97.32 | 91.74 | 98.19 | 96.76 | **97.47** | **86.34** |

\* Anomaly Transformer with reconstruction error only (p. 22). "Stationary" is the Non-stationary Transformer (p. 22).

- The canonical Transformer is worse (average F1 76.88%); the authors suggest that vanilla attention "can be distracted by the dominant normal time points", and that periodicity-aware models (TimesNet, FEDformer, Autoformer) do well because periodicity analysis "can highlight variations that violate the periodicity implicitly" (p. 8).
- **Our reading:** the headline TimesNet (Inception) is not best on any single dataset; its first place in Table 5 comes from the ResNeXt variant, and from the average. SMAP F1 stays around 66.9–71.5 for every model, while SWaT and PSM reach the 90s.

**Choice of 2D backbone** (Table 8, p. 15; F1 in %; "Shared" uses the same parameters for the $k$ tensors, "Ind" separate ones):

| Backbone | SMD | MSL | SMAP | SWaT | PSM | Avg F1 |
|---|---|---|---|---|---|---|
| ResNet | 83.82 | 84.70 | 71.10 | 90.97 | 93.45 | 84.81 |
| ResNeXt | 85.81 | 85.15 | 71.52 | 91.74 | 97.47 | 86.34 |
| Swin Transformer | 85.25 | 87.14 | 70.88 | 92.29 | 95.01 | 86.11 |
| ConvNext | 86.25 | 87.12 | 72.16 | 92.31 | 96.62 | 86.89 |
| Inception (Ind) | 84.17 | 87.18 | 70.89 | 92.36 | 93.41 | 85.60 |
| Inception (Shared) | 85.12 | 84.18 | 70.85 | 92.10 | 95.21 | 85.49 |

Efficiency of the same variants on anomaly detection (Figure 4 right, p. 6; parameters, training time per iteration as labeled): Inception (sharing) 0.067MB, 43.2ms; Inception (independent) 0.331MB, 60.2ms; ResNet 0.024MB, 30.5ms; ConvNext 2.196MB, 39.2ms; ResNext 0.103MB, 103.9ms; SwinBlock 0.052MB, 103.6ms.

**Architecture ablations** (Table 9, p. 15, and Table 10, p. 16; F1 in %):

| Variant | SMD | MSL | SMAP | SWaT | PSM | Avg F1 |
|---|---|---|---|---|---|---|
| TimesNet | 85.12 | 84.18 | 70.85 | 92.10 | 95.21 | 85.49 |
| + decomposition (Autoformer's) | 82.72 | 84.95 | 70.54 | 92.54 | 95.69 | 85.29 |
| Transform raw data only | 82.82 | 85.84 | 70.82 | 91.57 | 93.20 | 84.85 |
| Directly-sum ($\sum_i \widehat{\mathbf{X}}^{l,i}_{\text{1D}}$) | 82.81 | 85.62 | 70.64 | 91.43 | 92.35 | 84.57 |
| Removing-Softmax ($\sum_i \mathbf{A}^{l-1}_{f_i} \times \widehat{\mathbf{X}}^{l,i}_{\text{1D}}$) | 83.10 | 85.17 | 71.55 | 91.27 | 95.16 | 85.25 |

- Adding the deep decomposition of Autoformer "cannot bring further promotion" (p. 15).
- Reshaping only the raw input, instead of the deep features at every block, lowers the average F1 from 85.49% to 84.85% (p. 15).
- The softmax-weighted aggregation performs best among the three aggregations (p. 16).

**Sensitivity to $k$** (Figure 8, p. 13): $k \in \{1, \dots, 5\}$; the authors report stable performance across $k$ in all four tasks shown, and note that for low-level tasks such as forecasting and anomaly detection the choice of $k$ "will affect the final performance more" (pp. 13–15). **Our reading** of the anomaly-detection panel: F1 moves by up to about 3 points across $k$ (SMD, dipping at $k = 3$), about 2 for PSM, and under 1 for SWaT and SMAP.

### Long-term forecasting

**Averages over the four prediction lengths** (Table 2, p. 7; MSE / MAE; input 96, ILI 36), TimesNet against the strongest baselines:

| Dataset | TimesNet | ETSformer | LightTS | DLinear | FEDformer | Stationary | Autoformer |
|---|---|---|---|---|---|---|---|
| ETTm1 | 0.400 / 0.406 | 0.429 / 0.425 | 0.435 / 0.437 | 0.403 / 0.407 | 0.448 / 0.452 | 0.481 / 0.456 | 0.588 / 0.517 |
| ETTm2 | 0.291 / 0.333 | 0.293 / 0.342 | 0.409 / 0.436 | 0.350 / 0.401 | 0.305 / 0.349 | 0.306 / 0.347 | 0.327 / 0.371 |
| ETTh1 | 0.458 / 0.450 | 0.542 / 0.510 | 0.491 / 0.479 | 0.456 / 0.452 | 0.440 / 0.460 | 0.570 / 0.537 | 0.496 / 0.487 |
| ETTh2 | 0.414 / 0.427 | 0.439 / 0.452 | 0.602 / 0.543 | 0.559 / 0.515 | 0.437 / 0.449 | 0.526 / 0.516 | 0.450 / 0.459 |
| Electricity | 0.192 / 0.295 | 0.208 / 0.323 | 0.229 / 0.329 | 0.212 / 0.300 | 0.214 / 0.327 | 0.193 / 0.296 | 0.227 / 0.338 |
| Traffic | 0.620 / 0.336 | 0.621 / 0.396 | 0.622 / 0.392 | 0.625 / 0.383 | 0.610 / 0.376 | 0.624 / 0.340 | 0.628 / 0.379 |
| Weather | 0.259 / 0.287 | 0.271 / 0.334 | 0.261 / 0.312 | 0.265 / 0.317 | 0.309 / 0.360 | 0.288 / 0.314 | 0.338 / 0.382 |
| Exchange | 0.416 / 0.443 | 0.410 / 0.427 | 0.385 / 0.447 | 0.354 / 0.414 | 0.519 / 0.500 | 0.461 / 0.454 | 0.613 / 0.539 |
| ILI | 2.139 / 0.931 | 2.497 / 1.004 | 7.382 / 2.003 | 2.616 / 1.090 | 2.847 / 1.144 | 2.077 / 0.914 | 3.006 / 1.161 |

**TimesNet per prediction length** (Table 13, p. 21; MSE / MAE):

| Dataset | 96 | 192 | 336 | 720 |
|---|---|---|---|---|
| ETTm1 | 0.338 / 0.375 | 0.374 / 0.387 | 0.410 / 0.411 | 0.478 / 0.450 |
| ETTm2 | 0.187 / 0.267 | 0.249 / 0.309 | 0.321 / 0.351 | 0.408 / 0.403 |
| ETTh1 | 0.384 / 0.402 | 0.436 / 0.429 | 0.491 / 0.469 | 0.521 / 0.500 |
| ETTh2 | 0.340 / 0.374 | 0.402 / 0.414 | 0.452 / 0.452 | 0.462 / 0.468 |
| Electricity | 0.168 / 0.272 | 0.184 / 0.289 | 0.198 / 0.300 | 0.220 / 0.320 |
| Traffic | 0.593 / 0.321 | 0.617 / 0.336 | 0.629 / 0.336 | 0.640 / 0.350 |
| Weather | 0.172 / 0.220 | 0.219 / 0.261 | 0.280 / 0.306 | 0.365 / 0.359 |
| Exchange | 0.107 / 0.234 | 0.226 / 0.344 | 0.367 / 0.448 | 0.964 / 0.746 |

ILI (prediction lengths 24, 36, 48, 60): 2.317 / 0.934, 1.972 / 0.920, 2.238 / 0.940, 2.027 / 0.928 (Table 13, p. 21).

- Counting first places across Table 13: TimesNet 40, DLinear 14, Non-stationary Transformer 7, FEDformer 6, ETSformer 4, LightTS 1, the rest 0 (Table 13, p. 21). The text says TimesNet is state of the art "in more than 80% of cases" (p. 7).
- LightTS and DLinear are marked as having "some mismatches between our input-output setting and their papers": their official code was run with only the input and output lengths changed (Table 13 footnote, p. 21).

### Short-term forecasting (M4)

Weighted average over the M4 subsets (Table 3, p. 7; Table 14, p. 22):

| Model | SMAPE | MASE | OWA |
|---|---|---|---|
| TimesNet | 11.829 | 1.585 | 0.851 |
| N-HiTS (2022) | 11.927 | 1.613 | 0.861 |
| N-BEATS (2019) | 11.851 | 1.599 | 0.855 |
| FEDformer (2022) | 12.840 | 1.701 | 0.918 |
| DLinear (2023) | 13.639 | 2.095 | 1.051 |

N-BEATS is run without its ensemble (Table 14 footnote, p. 22). TimesNet per subset (SMAPE / MASE / OWA): Yearly 13.387 / 2.996 / 0.786; Quarterly 10.100 / 1.182 / 0.890; Monthly 12.670 / 0.933 / 0.878; Others 4.891 / 3.302 / 1.035 (Table 14, p. 22).

### Other tasks and efficiency (briefly)

- **Imputation:** TimesNet is best on all 6 datasets in Table 4 (averages over the 4 mask ratios, e.g. ETTm1 0.027 / 0.107 MSE / MAE) (p. 8) and takes all 48 first places in Table 16 (p. 23).
- **Classification:** average accuracy 73.6% over 10 UEA datasets, against Flowformer 73.0% and Rocket 72.5% (p. 8; Table 17, p. 23).
- **Efficiency** (Table 11, p. 19, measured on ETTh1 imputation): TimesNet has 0.067 MB of parameters for every series length (384 to 3072), and ranks first in all five tasks (average ranking 1.0) among 13 models.

### Training on mixed datasets (Appendix H)

ETTh1, ETTh2, ETTm1 and ETTm2 are mixed into one training set ("Unified") and compared with training on each subset ("Independent"), for **imputation** (p. 20; Table 12, p. 20). MSE / MAE per mask ratio:

| Model | Training | Ratio | ETTm1 | ETTm2 | ETTh1 | ETTh2 |
|---|---|---|---|---|---|---|
| TimesNet | Unified | 12.5% | 0.019 / 0.091 | 0.018 / 0.075 | 0.035 / 0.126 | 0.032 / 0.112 |
| TimesNet | Unified | 25% | 0.023 / 0.099 | 0.020 / 0.081 | 0.046 / 0.144 | 0.036 / 0.119 |
| TimesNet | Unified | 37.5% | 0.028 / 0.109 | 0.022 / 0.086 | 0.057 / 0.159 | 0.040 / 0.129 |
| TimesNet | Unified | 50% | 0.037 / 0.123 | 0.025 / 0.095 | 0.075 / 0.181 | 0.047 / 0.140 |
| TimesNet | Independent | 12.5% | 0.019 / 0.092 | 0.018 / 0.080 | 0.057 / 0.159 | 0.040 / 0.130 |
| TimesNet | Independent | 25% | 0.023 / 0.101 | 0.020 / 0.085 | 0.069 / 0.178 | 0.046 / 0.141 |
| TimesNet | Independent | 37.5% | 0.029 / 0.111 | 0.023 / 0.091 | 0.084 / 0.196 | 0.052 / 0.151 |
| TimesNet | Independent | 50% | 0.037 / 0.124 | 0.026 / 0.098 | 0.102 / 0.215 | 0.060 / 0.162 |
| Autoformer | Unified | 12.5% | 0.034 / 0.122 | 0.023 / 0.091 | 0.066 / 0.174 | 0.042 / 0.135 |
| Autoformer | Unified | 25% | 0.048 / 0.146 | 0.027 / 0.102 | 0.086 / 0.200 | 0.049 / 0.147 |
| Autoformer | Unified | 37.5% | 0.060 / 0.163 | 0.030 / 0.109 | 0.114 / 0.229 | 0.055 / 0.157 |
| Autoformer | Unified | 50% | 0.078 / 0.185 | 0.034 / 0.117 | 0.133 / 0.247 | 0.065 / 0.171 |
| Autoformer | Independent | 12.5% | 0.034 / 0.124 | 0.023 / 0.092 | 0.074 / 0.182 | 0.044 / 0.138 |
| Autoformer | Independent | 25% | 0.046 / 0.144 | 0.026 / 0.101 | 0.090 / 0.203 | 0.050 / 0.149 |
| Autoformer | Independent | 37.5% | 0.057 / 0.161 | 0.030 / 0.108 | 0.109 / 0.222 | 0.060 / 0.163 |
| Autoformer | Independent | 50% | 0.067 / 0.174 | 0.035 / 0.119 | 0.137 / 0.248 | 0.068 / 0.173 |
| FEDformer | Unified | 12.5% | 0.041 / 0.143 | 0.060 / 0.166 | 0.077 / 0.196 | 0.087 / 0.204 |
| FEDformer | Unified | 25% | 0.057 / 0.169 | 0.089 / 0.205 | 0.101 / 0.228 | 0.125 / 0.246 |
| FEDformer | Unified | 37.5% | 0.073 / 0.192 | 0.125 / 0.244 | 0.130 / 0.258 | 0.161 / 0.283 |
| FEDformer | Unified | 50% | 0.099 / 0.224 | 0.172 / 0.287 | 0.164 / 0.289 | 0.214 / 0.326 |
| FEDformer | Independent | 12.5% | 0.035 / 0.135 | 0.056 / 0.159 | 0.070 / 0.190 | 0.095 / 0.212 |
| FEDformer | Independent | 25% | 0.052 / 0.166 | 0.080 / 0.195 | 0.106 / 0.236 | 0.137 / 0.258 |
| FEDformer | Independent | 37.5% | 0.069 / 0.191 | 0.110 / 0.231 | 0.124 / 0.258 | 0.187 / 0.304 |
| FEDformer | Independent | 50% | 0.089 / 0.218 | 0.156 / 0.276 | 0.165 / 0.299 | 0.232 / 0.341 |

- The authors: TimesNet "can handle this mixed dataset well and generally promote the model performance in four independent subsets", while for the other baselines mixed training "may decrease the model performance in some subsets" (p. 20).
- **Our reading:** for TimesNet the gain is concentrated on the hourly subsets (ETTh1: 0.102 → 0.075 MSE at 50%), with the 15-minute subsets nearly unchanged. The TimesNet "Independent" ETTm1 50% MSE here is 0.037, while Table 16 reports 0.036 for the same setting (p. 23).

## Assumptions and limitations

- **Periodicity is averaged over variates:** $\mathbf{A}$ averages the amplitudes over the $C$ dimensions (p. 4), so all variates share the same $k$ periods. **Our reading:** with heterogeneous variates (as in SMD or SWaT), one set of periods is a compromise; the paper doesn't discuss it.
- **Only the top-$k$ frequencies** in $\{1, \dots, [T/2]\}$ are used (p. 4); with a window of $T = 100$ (anomaly detection), only periods up to 100 points can be found.
- **Non-periodic series** are handled by falling back to frequency 1 (p. 15), argued with the decomposition ablation (Table 9) and the Exchange showcase (Figure 9, p. 16).
- **Anomaly detection uses one criterion, the reconstruction error, for all models** (p. 8); task-specific criteria (Anomaly Transformer's association discrepancy) are switched off (p. 9). The threshold and any point adjustment aren't described (pp. 8, 13, 22).
- **Shared input embedding and projection** for all base models (p. 12): baseline numbers are not those of their original papers. For forecasting, an MLP initialization and Series Stationarization are added (p. 12); whether they apply to all base models or other tasks isn't stated.
- **"All experiments are repeated three times"** (p. 12); standard deviations are reported only for classification ("within 0.1%", Table 17, p. 23).
- **Future work** stated by the authors: large-scale pre-training with TimesNet as backbone (p. 9).
- **Our reading:** the anomaly-detection table compares architectures under one reconstruction pipeline, which is useful for choosing a backbone, but says little about how TimesNet compares with dedicated detectors under their own criteria.

## Relevance to this thesis

**Our reading:**

- **A candidate backbone for both of our tasks:** one architecture, trained with an MSE loss, serves forecasting and reconstruction-based anomaly detection (Table 7, p. 14). Merging needs the same architecture for all task models, which this provides.
- **A concrete anomaly-detection protocol to reproduce:** SMD, MSL, SMAP, SWaT, PSM; windows of 100; reconstruction error as the score; precision, recall and F1 (pp. 6, 8; Table 6, p. 14). The threshold rule and point adjustment must be fixed by us and documented, since the paper doesn't state them.
- **Small model, cheap task vectors:** 0.067 MB of parameters (Table 11, p. 19), independent of $k$ thanks to the shared inception block (p. 5). The width $d_{\text{model}}$ depends on the number of variates $C$ (p. 12): with a base-2 logarithm (the base isn't stated), datasets with $C$ = 38, 55, 25, 51, 25 would get $d_{\text{model}}$ = 64/64/32/64/32, i.e. different shapes (with natural or base-10 logs all would get the minimum, 32), and the embedding and projection layers depend on $C$ anyway. Merging across these datasets would need a common $d_{\text{model}}$ and per-dataset input/output layers.
- **Data-dependent routing inside the model:** the periods (and so the reshape) are recomputed from each input's FFT at every layer (Equation 5, p. 5). Two task models merged in weight space would still pick periods per input; how interference shows up through this routing is an open question.
- **Joint training already appears here:** the mixed-dataset experiment (Table 12, p. 20) is a small instance of joint training versus one model per dataset, for imputation on four ETT subsets; for TimesNet, joint training matches or beats independent training. It is a reference point for our joint-training baseline, not a test of merging.
- **Forecasting protocol to reuse:** input 96, prediction lengths 96/192/336/720, MSE/MAE, with the ETT, Electricity, Traffic, Weather, Exchange benchmarks (Table 2, p. 7; Table 6, p. 14).

## Quotes worth keeping

> "Based on the observation of multi-periodicity in time series, we ravel out the complex temporal variations into the multiple *intraperiod-* and *interperiod-variations*." (p. 1)

> "Note that for the time series without clear periodicity, the variations will be dominated by the intraperiod-variation and is equivalent to the ones with infinite period length." (p. 2)

> "Besides, we adopt a shared inception block for different reshaped 2D tensors $\{\mathbf{X}^{l,1}_{\text{2D}}, \cdots, \mathbf{X}^{l,k}_{\text{2D}}\}$ to improve parameter efficiency, which can make the model size invariant to the selection of hyper-parameter $k$." (p. 5)

> "For a fair comparison, we only change the base models for reconstruction and use the classical reconstruction error as the shared anomaly criterion for all experiments." (p. 8)

> "Following the pre-processing methods in Anomaly Transformer (2021), we split the dataset into consecutive non-overlapping segments by sliding window." (p. 8)

> "For a fair comparison, we keep the input embedding and the final projection layer the same among different base models and only evaluate the capability of base models." (p. 12)
