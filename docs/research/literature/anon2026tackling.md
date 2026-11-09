# anon2026tackling — Tackling Time-Series Forecasting Generalization via Mitigating Concept Drift

- **Status:** verified (2026-11-08): checked against the paper by an independent agent (about 170 claims, every table cell correct: 5 misstatements and 1 wrong page, all fixed)
- **Reference:** anonymous authors (double-blind); ICLR 2026 submission, **under review, not accepted**; authors not known ([references.bib](references.bib))
- **Version read:** the ICLR 2026 review version ("Under review as a conference paper at ICLR 2026"), 16 pages: main text pp. 1–9, references pp. 10–12, appendix pp. 12–16
- **Read:** everything: main text (Sections 1–5, pp. 1–9), references (pp. 10–12), appendices A–E (pp. 12–16)
- **Code:** <https://anonymous.4open.science/r/shifts_iclr-ED40> (p. 7, anonymized link given in the paper)

## In one paragraph

The paper splits distribution shift in time-series forecasting into two types:

- **temporal shift**, where marginal distributions change over time and conditional ones stay the same, and
- **concept drift**, where conditional distributions change and marginal ones stay the same (Definitions 2.1–2.2, p. 2).

It argues that existing forecasting work mostly handles temporal shift (through normalization), while concept drift is largely overlooked (p. 1, pp. 2–3).

It proposes:

- **SAM** (soft attention masking), which builds a surrogate exogenous feature $\mathbf{X}^{\text{SUR}}$ from "invariant patterns" in both the lookback and the horizon windows of the exogenous series, and
- **ShifTS**, a model-agnostic framework that first removes temporal shift with RevIN and then applies SAM (pp. 3–6).

On six datasets (ILI, Exchange, ETTh1/ETTh2/ETTm1/ETTm2), with univariate targets and exogenous features:

- ShifTS lowers MSE and MAE on average (IMP.) for all six base forecasting models tested, though not in every cell:
  - e.g. ERM wins for TimeMixer on ILI $H$ = 48 and on ETTh1 $H$ = 96 MAE, and
  - the Table 4 caption calls the results "near-consistent" (Table 1, p. 7; Table 4, p. 16), and
- with Crossformer it is best in 6 of 8 averaged evaluations against concept-drift, temporal-shift and combined baselines (Table 2, p. 8).

## Problem

**Setting** (Section 2.1, p. 2): forecasting a target series $\mathbf{Y}$ with exogenous covariate features $\mathbf{X}$. At time step $t$, predict the horizon window from the lookback window:

$$\mathbf{Y}_t^H = [y_{t+1}, y_{t+2}, \dots, y_{t+H}] \in \mathbf{Y}$$

from historical data $(\mathbf{X}_t^L, \mathbf{Y}_t^L)$, with

$$\mathbf{X}_t^L = [x_{t-L+1}, x_{t-L+2}, \dots, x_t] \in \mathbf{X}, \qquad \mathbf{Y}_t^L = [y_{t-L+1}, y_{t-L+2}, \dots, y_t] \in \mathbf{Y}$$

where $L$ is the length of the **lookback window** and $H$ the number of forecast steps, the **horizon window** (p. 2).

(The paper prints the first element as "$yt + 1$", p. 2.)

$\mathbf{Y}^H = \{\mathbf{Y}_t^H\}$ for $\forall t$ is the collection of horizon series over all time steps, and likewise $\mathbf{Y}^L$, $\mathbf{X}^L$ (p. 2).

- Conventional forecasting learns $f_\theta : (\mathbf{X}^L, \mathbf{Y}^L) \to \mathbf{Y}^H$ by empirical risk minimization (ERM) (p. 2).
- **Scope:** univariate forecasting with exogenous features, $d_{\mathbf{Y}} = 1$ and $d_{\mathbf{X}} \ge 1$ (p. 2).

**The question:** how to mitigate concept drift in *standard* (offline) time-series forecasting, where invariant-learning methods from general machine learning don't fit (pp. 1–3).

**Why existing concept-drift methods don't fit** (p. 1, p. 3):

- Invariant-learning methods need **environment labels**, "typically unavailable in time-series datasets" (p. 1, p. 3).
- They assume **all correlated exogenous features** needed to determine the target are accessible, which often doesn't hold for time series ("lookback window information is not sufficiently determining the horizon target") (p. 3).
- The few concept-drift methods built for time series are designed for **online** settings, which require iterative retraining over time steps (p. 1),
  and are validated only on limited synthetic datasets (p. 3).

## Definitions: the taxonomy of distribution shift

**Two types** (p. 1, citing Granger 2003):

1. The distributions of the series themselves change over time, "including shifts in mean, variance, and autocorrelation structure", referred to as non-stationarity or temporal drift (p. 1).
2. Unforeseen exogenous factors shift the distribution of the target series: concept drift (p. 1).

**Target distribution, as printed** (p. 2): a forecasting model aims to predict

$$\mathrm{P}(\mathbf{Y}^H) = \mathrm{P}(\mathbf{Y}^H \mid \mathbf{Y}^L)\,\mathrm{P}(\mathbf{Y}^L) + \mathrm{P}(\mathbf{Y}^H \mid \mathbf{X}^L)\,\mathrm{P}(\mathbf{X}^L)$$

which "should be generalizable for both training and testing time steps" (p. 2).

**Definition 2.1 (Temporal Shift)** (p. 2, citing Shimodaira 2000 and Du et al. 2021): "Temporal shift (also known as virtual shift (Tsymbal, 2004)) is the marginal probability distributions changing over time, while the conditional distributions are the same."

**Definition 2.2 (Concept Drift)** (p. 2, citing Lu et al. 2018): "Concept drift (also known as real concept drift (Gama et al., 2014)) is the conditional distributions changing over time, while the marginal probability distributions are the same."

- Footnote 1 (p. 2): Gama et al. (2014) define concept drift as *both* virtual shift and real concept drift; the paper's concept drift matches only **real concept drift**.

**The formal reading the paper gives** (p. 2; repeated p. 3), stated as examples, not as part of the definitions:

- Temporal shift: unstable marginal distributions, e.g.

  $$\mathrm{P}(\mathbf{Y}^H) \neq \mathrm{P}(\mathbf{Y}^L)$$

- Concept drift: unstable conditional distributions,

  $$\mathrm{P}(\mathbf{Y}_i^H \mid \mathbf{X}_i^L) \neq \mathrm{P}(\mathbf{Y}_j^H \mid \mathbf{X}_j^L) \quad \text{for some } i, j \in t$$

- Concept drift in time series is "the changing correlations between $\mathbf{X}$ and $\mathbf{Y}$ over time" (p. 3);
  "The correlations between $\mathbf{X}$ and $\mathbf{Y}$ can change over time, making the conditional distributions $\mathrm{P}(\mathbf{Y}^H \mid \mathbf{X}^L)$ unstable and less predictable" (p. 3).

**How existing methods handle temporal shift** (pp. 2–3): through normalization, "ensuring $\mathrm{P}(\mathbf{Y}^H) = \mathrm{P}(\mathbf{Y}^L)$ by both normalizing to standard 0-1 distributions" (citing RevIN, Non-stationary Transformers, Dish-TS).

**Appendix B, the distinction in words** (p. 13):

- **Temporal shift:** changes in the statistical properties of a **univariate** series (mean, variance, autocorrelation structure) over time.
  - E.g. mean and variance differing between the lookback and horizon windows.
  - "This issue is inherent in time series forecasting and can occur on any given time series data, regardless of whether the data pertains to the target series or exogenous features" (p. 13).
- **Concept drift:** changes in the **correlations between exogenous features and the target** over time;
  it "involves multiple correlated time series and is not an inherent issue in univariate time series analysis" (p. 13).
- Illustrations (p. 14):
  - Figure 4 shows a target series whose mean and variance vary across periods (temporal shift);
  - Figure 5 shows an exogenous feature whose increases lead to target increases early on and to decreases later (concept drift).
  - In both, N-BEATS+RevIN tracks the ground truth and plain N-BEATS doesn't (Figures 4–5, p. 14; figures adapted from the RevIN repository, footnote 2, p. 13).

**Dataset-level diagnosis** (Figure 6, p. 15):

- ETT: both shifts present: the target's variance is lower earlier and higher later (temporal shift); the $\mathbf{X}$–$\mathbf{Y}$ correlation "is unclear and unstable" (concept drift).
- Traffic: both moderate: the target is near-periodic, and the $\mathbf{X}$–$\mathbf{Y}$ correlation stays stable (both increase or decrease together).

**Our reading:**

- The two definitions are verbal and mirror each other (marginals change and conditionals fixed vs. the reverse).
  - They don't cover the case where both change at once, although the ablation concludes the two "co-exist in time series data" (p. 9) and ETT is said to show both (p. 15).
- "Conditional" is always $\mathbf{Y}^H$ given the **exogenous** $\mathbf{X}$.
  - A change in $\mathrm{P}(\mathbf{Y}^H \mid \mathbf{Y}^L)$ (the target's own dynamics) isn't assigned to either type.
  - So "concept drift" here is narrower than the general machine-learning sense, and by the paper's own account concept drift "is not an inherent issue in univariate time series analysis" (p. 13).
- "Temporal shift" is essentially covariate (virtual) shift applied across time, which is why normalization (RevIN-style) is presented as its remedy.
- The decomposition of $\mathrm{P}(\mathbf{Y}^H)$ on p. 2 is printed as a sum of two products.
  - It isn't a standard identity (the law of total probability would condition on both $\mathbf{X}^L$ and $\mathbf{Y}^L$ jointly).
  - We read it as informal.

## Method

### SAM: soft attention masking (Section 3.1, pp. 3–5)

**Intuition** (p. 3): $\mathbf{X}^L$ alone may lack the information needed to predict $\mathbf{Y}^H$.

- There may be patterns in the **horizon** window of the exogenous features, $\mathbf{X}^H$, jointly with $\mathbf{X}^L$, that influence the target.
- Modeling $P(\mathbf{Y}^H \mid \mathbf{X}^L, \mathbf{X}^H)$ "leads to a more stable conditional distribution" than $P(\mathbf{Y}^H \mid \mathbf{X}^L)$ (p. 3).
- The authors "assume that incorporating causal relationships from the horizon window enables more complete causality modeling", given that the future can't influence the past (e.g. $\mathbf{X}_{t+1}^H \nrightarrow \mathbf{Y}_t^H$) (p. 3).

**Two obstacles** to modeling $P(\mathbf{Y}^H \mid \mathbf{X}^L, \mathbf{X}^H)$ directly (pp. 3–4):

1. $\mathbf{X}^H$ is unknown at test time; predicting it via $P(\mathbf{X}^H \mid \mathbf{X}^L)$ "can be as challenging as predicting $\mathbf{Y}^H$ directly" (p. 4).
2. Not every pattern in $\mathbf{X}^H$ is causally related to the target; modeling all of them adds noisy relationships (p. 4).

**Two-step approach** (p. 4):

1. First identify the patterns in $[\mathbf{X}^L, \mathbf{X}^H]$ that give stable conditional distributions ("invariant patterns"),
2. then model those conditionals.

A pattern is considered stable if its correlation with the target stays consistent over all or most time steps; sporadic or local correlations "are likely spurious" (p. 4).

The invariant patterns are aggregated into a **surrogate feature** $\mathbf{X}^{\text{SUR}}$, and the model learns $P(\mathbf{Y}^H \mid \mathbf{X}^{\text{SUR}})$ (p. 4, Figure 1(b), p. 3).

- Claimed trade-off (p. 4): $P(\mathbf{Y}^H \mid \mathbf{X}^{\text{SUR}})$ is stable, but estimating $\mathbf{X}^{\text{SUR}}$ adds error;
  "practical evaluations demonstrate that the benefits ... outweigh the potential estimation errors", because $\mathbf{X}^{\text{SUR}}$ "contains only partial information, which is easier to predict than the entire $\mathbf{X}^H$" (p. 4).

**Implementation** (p. 4):

1. Concatenate $[\mathbf{X}^L, \mathbf{X}^H]$ into one series of length $L + H$.
2. Slice it with a sliding window of size $H$, giving $L + 1$ slices: local patterns $[\mathbf{X}_{t-L}^H, \dots, \mathbf{X}_t^H]$ at each time step $t$.
3. Model the conditionals of all local patterns $[P(\mathbf{Y}_t^H \mid \mathbf{X}_{t-L}^H), \dots, P(\mathbf{Y}_t^H \mid \mathbf{X}_t^H)]$, weighted by a learnable soft attention matrix $\mathcal{M}$.

**The mask operations** (Equation 1, p. 4), where $i, j$ are the first and second dimensions of $\mathcal{M}$:

$$\text{Softmax:} \quad \mathcal{M}_j = \mathrm{Softmax}(\mathcal{M}_j)$$

$$\text{Sparsity:} \quad \mathcal{M}_{ij} = \mathcal{M}_{ij} \cdot \mathbb{1}_{(\mathcal{M}_{ij} - \mu(\mathcal{M}_j)) \ge 0}$$

$$\text{Normalize:} \quad \mathcal{M}_j = \frac{\mathcal{M}_j}{|\mathcal{M}_j|}$$

- Softmax computes each pattern's weight toward $\mathbf{Y}^H$;
  sparsity keeps only weights at or above the mean $\mu(\mathcal{M}_j)$;
  the high-weight patterns "consistently contribute to the target across all instances at all time steps" and are regarded as invariant (p. 4).
- Invariant patterns, intuitively: $P(\mathbf{Y}_i^H \mid \mathbf{X}_{i-k}^H) \approx P(\mathbf{Y}_j^H \mid \mathbf{X}_{j-k}^H)$ for some $k \in [0, L]$ and $i, j \in t$ (p. 4).

**Surrogate feature** (Equation 2, p. 4):

$$\mathbf{X}^{\text{SUR}} = \texttt{SAM}([\mathbf{X}^L, \mathbf{X}^H]) = \sum_{L+1} \mathcal{M}\big(\mathrm{Slice}([\mathbf{X}^L, \mathbf{X}^H])\big)$$

where $\mathrm{Slice}(\cdot)$ maps $[L + H, d_{\mathbf{X}}] \to [H, L + 1, d_{\mathbf{X}}]$ and $\mathcal{M} \in \mathbb{R}^{L+1 \times d_{\mathbf{X}}}$ (p. 5).

**Surrogate loss** (Equation 3, p. 5): since $\mathbf{X}^{\text{SUR}}$ uses horizon information unavailable at test time, the forecasting model estimates $\hat{\mathbf{X}}^{\text{SUR}}$:

$$\mathcal{L}_{\text{SUR}} = \mathrm{MSE}(\mathbf{X}^{\text{SUR}}, \hat{\mathbf{X}}^{\text{SUR}})$$

### Temporal shift first (Section 3.2, p. 5)

- Claim: mitigating temporal shift "is equally critical and serves as a prerequisite for effectively managing concept drift" (p. 5):
  a stable $P(\mathbf{Y}^H \mid \mathbf{X}^{\text{SUR}})$ is hard to learn if the marginals $P(\mathbf{Y}^H)$ or $P(\mathbf{X}^{\text{SUR}})$ change over time (p. 5).
- Remedy: learn the conditional under standardized marginals with instance normalization: normalize before the model, denormalize after,
  so that $P(\mathbf{X}_{\text{Norm}}^L) \approx P(\mathbf{X}_{\text{Norm}}^H) \sim \mathrm{Dist}(0, 1)$
  and $P(\mathbf{Y}_{\text{Norm}}^L) \approx P(\mathbf{Y}_{\text{Norm}}^H) \sim \mathrm{Dist}(0, 1)$ (p. 5).
- Choice: **RevIN**, for its simplicity and effectiveness;
  SAN and N-S Transformer are left out of the framework because they "often require modifications to forecasting models or additional pre-training strategies" (p. 5).

### ShifTS: the integrated framework (Section 3.3, pp. 5–6; Figure 2, p. 5)

Model-agnostic; four steps (pp. 5–6):

1. Normalize the input series (temporal shift).
2. Forecast the surrogate exogenous features $\hat{\mathbf{X}}^{\text{SUR}}$ determined by SAM (concept drift).
3. An aggregation MLP, $\mathrm{Agg}(\cdot)$, uses $\hat{\mathbf{X}}^{\text{SUR}}$ to forecast the target.
4. Denormalize the output (temporal shift).

**Total loss** (Equation 4, p. 6):

$$\mathcal{L} = \mathcal{L}_{\text{SUR}}(\mathbf{X}^{\text{SUR}}, \hat{\mathbf{X}}^{\text{SUR}}) + \mathcal{L}_{\text{TS}}(\mathbf{Y}^H, \hat{\mathbf{Y}}^H)$$

with $\mathcal{L}_{\text{TS}}$ the conventional MSE forecasting loss; no weight between the two terms (p. 6).

**Algorithm 1** (p. 6), training, for $i$ in range($E$):

$$[\mathbf{X}_{\text{Norm}}^L, \mathbf{Y}_{\text{Norm}}^L] = \mathrm{Norm}([\mathbf{X}^L, \mathbf{Y}^L])$$

$$[\hat{\mathbf{X}}_{\text{Norm}}^{\text{SUR}}, \hat{\mathbf{Y}}_{\text{Norm}}^H] = f_i([\mathbf{X}_{\text{Norm}}^L, \mathbf{Y}_{\text{Norm}}^L])$$

$$\hat{\mathbf{Y}}_{\text{Norm}}^H = \hat{\mathbf{Y}}_{\text{Norm}}^H + \mathrm{Agg}_i(\hat{\mathbf{X}}_{\text{Norm}}^{\text{SUR}})$$

$$[\hat{\mathbf{X}}^{\text{SUR}}, \hat{\mathbf{Y}}^H] = \mathrm{Denorm}([\hat{\mathbf{X}}_{\text{Norm}}^{\text{SUR}}, \hat{\mathbf{Y}}_{\text{Norm}}^H])$$

$$\mathbf{X}^{\text{SUR}} = \texttt{SAM}([\mathbf{X}^L, \mathbf{X}^H])$$

then the loss of Equation 4 and an update of $f$, $\mathcal{M}$, $\mathrm{Agg}$. Testing runs the same steps without SAM and the loss, from $\mathbf{X}^L, \mathbf{Y}^L$ only (p. 6).

**Our reading:**

- The forecasting model $f$ outputs both the target and the surrogate features; the aggregation MLP adds a residual correction to the target. At test time no horizon data is used.
- The mask $\mathcal{M}$ is learned jointly;
  "invariant across time steps" is enforced only through one shared mask over the whole training set, not through any explicit invariance penalty across environments.
- Line 9 of Algorithm 1 is printed as $f_{i+1} \leftarrow f_i$, $\mathcal{M}_{i+1} \leftarrow \mathcal{M}_i$, $\mathrm{Agg}_{i+1} \leftarrow \mathrm{Agg}_i$ (p. 6): the gradient step is implied, not written.

## Experimental setup

**Datasets** (p. 6; C.1, pp. 13–14): six, as used by Liu et al. (2024a, FOIL):

| Dataset | Content (as described) | Variables |
|---|---|---|
| ILI | weekly influenza-like illness patients | 8 |
| Exchange | daily exchange rates | 8 currencies |
| ETTh1, ETTh2 | electricity transformer temperature, hourly, two counties in China | 7 |
| ETTm1, ETTm2 | same, minutely | 7 |

(p. 6 reads "Two-hourly/minutely reported electricity transformer temperature (ETTh1/ETTh2 and ETTm1/ETTm2, respectively)"; **our reading:** "two" most likely counts the two sub-datasets per granularity, consistent with "minutely and hourly" in C.1, p. 13.)

- **Excluded:**
  - Traffic (PeMS) and Weather, for "near-stationary behavior, with only moderate distribution shift issues" (p. 6);
  - Electricity is also excluded, with "strong periodic signals" making shift "less prevalent" (p. 14; Figure 6, p. 15).
- **Preprocessing:** train/validation/test splits and target-variable selection follow prior works (Wu et al. 2022, Nie et al. 2023, Liu et al. 2024b);
  all datasets "preprocessed using the zero-mean normalization method" (p. 14).
  The specific target variable per dataset isn't named.

**Windows** (C.2, pp. 14–15):

| Datasets | Lookback $L$ | Horizons $H$ | Decoder label window |
|---|---|---|---|
| ETT, Exchange | 96 | 96, 192, 336, 720 | 48 |
| ILI | 36 | 24, 36, 48, 60 | 18 |

**Forecasting models** (p. 6): Informer, Pyraformer, Crossformer, PatchTST, TimeMixer, iTransformer (the last two called state of the art); five transformer-based and one MLP-based (p. 7).

- Implementations and suggested hyperparameters from the Time Series Library, "with additional tuning" (p. 15);
- an extra MLP layer at the end of PatchTST to use exogenous features, following Liu et al. 2024a (p. 15).

**Distribution-shift baselines** (pp. 6–7), all with Crossformer as the forecasting model (p. 8):

- Temporal shift: N-S Transformer, RevIN, SAN (Dish-TS and SIN omitted "due to their instability on univariate targets", p. 7).
- Concept drift (general-purpose): GroupDRO, IRM, VREx, EIIL; implementations and tuning from DomainBed (p. 15).
- Combined: IRM+RevIN, EIIL+RevIN, and FOIL (Liu et al. 2024a).
- **Environment labels** for GroupDRO, IRM and VREx: the training set is split into $k$ equal-length time segments (p. 15); the value of $k$ isn't given.
- Temporal-shift baselines use the configurations of their own papers (p. 15).
- Minutely ETT is excluded from this comparison, following Liu et al. 2024a, as it closely resembles hourly ETT (p. 8).

**Metrics** (p. 7): $\mathrm{MSE} = \frac{1}{n}\sum_{i=1}^n (\boldsymbol{y} - \hat{\boldsymbol{y}})^2$ and $\mathrm{MAE} = \frac{1}{n}\sum_{i=1}^n |\boldsymbol{y} - \hat{\boldsymbol{y}}|$.

"IMP." is "the average improvements over all horizons of ShifTS vs ERM" (Table 1 caption, p. 7).

**Hardware:** NVIDIA Tesla V100 32GB (p. 7).

**Not stated:** number of runs or seeds, standard deviations, number of epochs $E$, optimizer and learning rates for ShifTS.

**Mutual information analysis** (C.3, p. 15; Equation 5):

$$\boldsymbol{I}(\mathbf{X}^H; \mathbf{Y}^H) = \sum_{x \in \mathbf{X}^H} \sum_{y \in \mathbf{Y}^H} P(x, y) \log \frac{P(x, y)}{P(x)P(y)}$$

computed per training time step and per exogenous dimension, averaged over time steps, then the maximum over dimensions is taken (p. 15).

## Results

**ShifTS vs ERM, newer models** (Table 1, p. 7). MSE / MAE; ShifTS is bold in every row except where noted; "IMP." as printed:

| Dataset | $H$ | Crossformer ERM | Crossformer ShifTS | PatchTST ERM | PatchTST ShifTS | iTransformer ERM | iTransformer ShifTS |
|---|---|---|---|---|---|---|---|
| ILI | 24 | 3.409 / 1.604 | 0.674 / 0.590 | 0.772 / 0.634 | 0.656 / 0.618 | 0.824 / 0.653 | 0.799 / 0.642 |
| ILI | 36 | 4.001 / 1.772 | 0.687 / 0.617 | 0.763 / 0.649 | 0.694 / 0.602 | 0.917 / 0.738 | 0.690 / 0.640 |
| ILI | 48 | 3.720 / 1.724 | 0.652 / 0.611 | 0.753 / 0.692 | 0.654 / 0.630 | 0.772 / 0.699 | 0.680 / 0.665 |
| ILI | 60 | 3.689 / 1.715 | 0.658 / 0.633 | 0.761 / 0.724 | 0.680 / 0.656 | 0.729 / 0.710 | 0.672 / 0.667 |
| ILI | IMP. | | 81.9% / 64.0% | | 12.0% / 7.1% | | 13.8% / 6.5% |
| Exchange | 96 | 0.338 / 0.475 | 0.102 / 0.237 | 0.130 / 0.265 | 0.102 / 0.236 | 0.135 / 0.272 | 0.115 / 0.255 |
| Exchange | 192 | 0.566 / 0.622 | 0.203 / 0.338 | 0.247 / 0.394 | 0.194 / 0.332 | 0.250 / 0.376 | 0.209 / 0.343 |
| Exchange | 336 | 1.078 / 0.867 | 0.407 / 0.484 | 0.522 / 0.557 | 0.388 / 0.477 | 0.450 / 0.503 | 0.426 / 0.495 |
| Exchange | 720 | 1.292 / 0.963 | 1.165 / 0.813 | 1.171 / 0.824 | 0.995 / 0.747 | 1.501 / 0.941 | 1.138 / 0.827 |
| Exchange | IMP. | | 53.5% / 38.9% | | 20.9% / 12.6% | | 15.2% / 6.9% |
| ETTh1 | 96 | 0.145 / 0.312 | 0.055 / 0.180 | 0.064 / 0.193 | 0.056 / 0.181 | 0.061 / 0.190 | 0.056 / 0.181 |
| ETTh1 | 192 | 0.240 / 0.420 | 0.072 / 0.206 | 0.085 / 0.222 | 0.073 / 0.209 | 0.076 / 0.219 | 0.072 / 0.205 |
| ETTh1 | 336 | 0.240 / 0.424 | 0.084 / 0.228 | 0.096 / 0.244 | 0.089 / 0.235 | 0.086 / 0.227 | 0.083 / 0.225 |
| ETTh1 | 720 | 0.391 / 0.553 | 0.095 / 0.244 | 0.128 / 0.282 | 0.097 / 0.245 | 0.085 / 0.232 | 0.082 / 0.230 |
| ETTh1 | IMP. | | 68.2% / 48.8% | | 14.5% / 7.2% | | 5.1% / 3.3% |
| ETTh2 | 96 | 0.255 / 0.408 | 0.137 / 0.286 | 0.154 / 0.309 | 0.139 / 0.287 | 0.141 / 0.292 | 0.137 / 0.288 |
| ETTh2 | 192 | 1.257 / 1.034 | 0.182 / 0.338 | 0.204 / 0.374 | 0.191 / 0.345 | 0.194 / 0.347 | 0.184 / 0.339 |
| ETTh2 | 336 | 0.783 / 0.771 | 0.234 / 0.388 | 0.252 / 0.406 | 0.222 / 0.381 | 0.229 / 0.383 | 0.225 / 0.381 |
| ETTh2 | 720 | 1.455 / 1.100 | 0.234 / 0.389 | 0.259 / 0.411 | 0.236 / 0.390 | 0.266 / 0.413 | 0.235 / 0.390 |
| ETTh2 | IMP. | | 71.4% / 52.9% | | 9.2% / 6.5% | | 5.4% / 2.5% |
| ETTm1 | 96 | 0.050 / 0.174 | 0.028 / 0.126 | 0.031 / 0.135 | 0.029 / 0.128 | 0.030 / 0.131 | 0.030 / 0.131 |
| ETTm1 | 192 | 0.271 / 0.454 | 0.043 / 0.158 | 0.048 / 0.166 | 0.044 / 0.161 | 0.049 / 0.171 | 0.046 / 0.165 |
| ETTm1 | 336 | 0.731 / 0.805 | 0.057 / 0.184 | 0.058 / 0.190 | 0.058 / 0.186 | 0.066 / 0.199 | 0.059 / 0.188 |
| ETTm1 | 720 | 0.829 / 0.849 | 0.083 / 0.219 | 0.083 / 0.223 | 0.080 / 0.219 | 0.082 / 0.219 | 0.079 / 0.217 |
| ETTm1 | IMP. | | 77.3% / 61.0% | | 4.6% / 3.0% | | 5.1% / 2.5% |
| ETTm2 | 96 | 0.153 / 0.315 | 0.069 / 0.190 | 0.078 / 0.206 | 0.067 / 0.188 | 0.073 / 0.200 | 0.073 / 0.195 |
| ETTm2 | 192 | 0.408 / 0.526 | 0.105 / 0.242 | 0.113 / 0.246 | 0.101 / 0.237 | 0.119 / 0.251 | 0.108 / 0.248 |
| ETTm2 | 336 | 0.428 / 0.504 | 0.146 / 0.289 | 0.176 / 0.320 | 0.134 / 0.278 | 0.157 / 0.302 | 0.144 / 0.291 |
| ETTm2 | 720 | 1.965 / 1.205 | 0.191 / 0.342 | 0.220 / 0.368 | 0.185 / 0.334 | 0.196 / 0.347 | 0.193 / 0.344 |
| ETTm2 | IMP. | | 71.3% / 52.0% | | 15.9% / 8.6% | | 4.8% / 2.1% |

Ties, bold on both sides as printed (p. 7): ETTm1 $H$ = 336 PatchTST MSE (0.058); ETTm1 $H$ = 96 iTransformer MSE and MAE (0.030, 0.131); ETTm2 $H$ = 96 iTransformer MSE (0.073).

- Claims (p. 7): ShifTS reduces errors "of up to 15%" with iTransformer, and helps older models (Informer, Crossformer) even more.

**ShifTS vs ERM, older models** (Table 4, p. 16). MSE / MAE:

| Dataset | $H$ | Informer ERM | Informer ShifTS | Pyraformer ERM | Pyraformer ShifTS | TimeMixer ERM | TimeMixer ShifTS |
|---|---|---|---|---|---|---|---|
| ILI | 24 | 5.032 / 1.935 | 1.030 / 0.812 | 4.692 / 1.898 | 0.979 / 0.749 | 0.853 / 0.733 | 0.789 / 0.702 |
| ILI | 36 | 4.475 / 1.876 | 1.046 / 0.850 | 4.814 / 1.950 | 0.866 / 0.740 | 0.721 / 0.676 | 0.697 / 0.665 |
| ILI | 48 | 4.506 / 1.879 | 0.918 / 0.818 | 4.109 / 1.801 | 0.789 / 0.732 | 0.737 / 0.692 | 0.741 / 0.711 |
| ILI | 60 | 4.313 / 1.850 | 0.957 / 0.839 | 4.483 / 1.850 | 0.723 / 0.698 | 0.788 / 0.723 | 0.670 / 0.659 |
| ILI | IMP. | | 78.4% / 56.0% | | 81.5% / 61.1% | | 6.3% / 3.0% |
| Exchange | 96 | 0.839 / 0.746 | 0.137 / 0.277 | 0.410 / 0.525 | 0.145 / 0.275 | 0.127 / 0.268 | 0.098 / 0.234 |
| Exchange | 192 | 0.862 / 0.773 | 0.210 / 0.346 | 0.529 / 0.610 | 0.300 / 0.404 | 0.229 / 0.355 | 0.214 / 0.352 |
| Exchange | 336 | 1.597 / 1.063 | 0.378 / 0.485 | 0.851 / 0.778 | 0.440 / 0.506 | 0.553 / 0.560 | 0.440 / 0.491 |
| Exchange | 720 | 4.358 / 1.935 | 0.760 / 0.655 | 1.558 / 1.067 | 1.509 / 0.963 | 1.173 / 0.834 | 0.962 / 0.747 |
| Exchange | IMP. | | 79.5% / 59.7% | | 39.8% / 31.5% | | 16.9% / 9.1% |
| ETTh1 | 96 | 0.891 / 0.863 | 0.095 / 0.231 | 0.653 / 0.748 | 0.065 / 0.197 | 0.059 / 0.184 | 0.059 / 0.187 |
| ETTh1 | 192 | 1.027 / 0.958 | 0.096 / 0.237 | 0.853 / 0.828 | 0.075 / 0.210 | 0.099 / 0.247 | 0.077 / 0.211 |
| ETTh1 | 336 | 1.055 / 0.961 | 0.092 / 0.237 | 0.705 / 0.797 | 0.092 / 0.238 | 0.121 / 0.279 | 0.098 / 0.246 |
| ETTh1 | 720 | 1.077 / 0.969 | 0.100 / 0.252 | 0.562 / 0.695 | 0.126 / 0.279 | 0.139 / 0.299 | 0.099 / 0.252 |
| ETTh1 | IMP. | | 90.7% / 74.5% | | 86.4% / 69.6% | | 23.3% / 10.1% |
| ETTh2 | 96 | 3.195 / 1.651 | 0.232 / 0.381 | 1.598 / 1.127 | 0.156 / 0.307 | 0.152 / 0.303 | 0.146 / 0.299 |
| ETTh2 | 192 | 3.569 / 1.778 | 0.334 / 0.464 | 3.314 / 1.599 | 0.217 / 0.367 | 0.195 / 0.349 | 0.185 / 0.343 |
| ETTh2 | 336 | 2.556 / 1.468 | 0.400 / 0.512 | 2.571 / 1.489 | 0.245 / 0.398 | 0.238 / 0.392 | 0.230 / 0.381 |
| ETTh2 | 720 | 2.723 / 1.532 | 0.489 / 0.579 | 2.294 / 1.409 | 0.261 / 0.410 | 0.273 / 0.421 | 0.249 / 0.397 |
| ETTh2 | IMP. | | 82.0% / 69.5% | | 90.6% / 73.5% | | 5.3% / 2.9% |
| ETTm1 | 96 | 0.320 / 0.433 | 0.055 / 0.175 | 0.130 / 0.298 | 0.028 / 0.125 | 0.030 / 0.128 | 0.029 / 0.126 |
| ETTm1 | 192 | 0.459 / 0.582 | 0.079 / 0.211 | 0.240 / 0.4112 | 0.045 / 0.162 | 0.047 / 0.165 | 0.047 / 0.164 |
| ETTm1 | 336 | 0.457 / 0.556 | 0.104 / 0.243 | 0.359 / 0.512 | 0.062 / 0.192 | 0.063 / 0.191 | 0.060 / 0.189 |
| ETTm1 | 720 | 0.735 / 0.760 | 0.148 / 0.294 | 0.657 / 0.750 | 0.091 / 0.231 | 0.083 / 0.223 | 0.081 / 0.220 |
| ETTm1 | IMP. | | 80.7% / 60.3% | | 82.2% / 62.6% | | 2.3% / 1.1% |
| ETTm2 | 96 | 0.191 / 0.345 | 0.154 / 0.298 | 0.275 / 0.422 | 0.075 / 0.200 | 0.079 / 0.205 | 0.075 / 0.201 |
| ETTm2 | 192 | 0.458 / 0.556 | 0.243 / 0.378 | 0.484 / 0.552 | 0.107 / 0.248 | 0.121 / 0.259 | 0.111 / 0.250 |
| ETTm2 | 336 | 0.606 / 0.624 | 0.515 / 0.539 | 1.138 / 0.909 | 0.146 / 0.293 | 0.150 / 0.295 | 0.148 / 0.294 |
| ETTm2 | 720 | 1.175 / 0.879 | 0.564 / 0.592 | 2.920 / 1.537 | 0.196 / 0.347 | 0.246 / 0.387 | 0.198 / 0.346 |
| ETTm2 | IMP. | | 33.4% / 23.0% | | 82.8% / 63.2% | | 8.5% / 4.1% |

ERM is better (bold) than ShifTS for TimeMixer on ILI $H$ = 48 (0.737 / 0.692 vs 0.741 / 0.711) and on ETTh1 $H$ = 96 MAE (0.184 vs 0.187);
ties on TimeMixer ETTh1 $H$ = 96 MSE (0.059) and ETTm1 $H$ = 192 MSE (0.047) (p. 16).

The caption accordingly says "near-consistent" gains (p. 16).

(The Pyraformer ETTm1 $H$ = 192 ERM MAE is printed with four decimals, 0.4112, p. 16.)

**Comparison with distribution-shift methods, Crossformer** (Table 2, p. 8). Averages over the four horizons, MSE / MAE; **bold** = best, *italics* = second best (underlined in the paper):

| Group | Method | ILI | Exchange | ETTh1 | ETTh2 |
|---|---|---|---|---|---|
| Base | ERM | 3.705 / 1.704 | 0.819 / 0.732 | 0.254 / 0.427 | 0.937 / 0.828 |
| Concept drift | GroupDRO | 2.285 / 1.287 | 0.821 / 0.751 | 0.278 / 0.453 | 1.150 / 0.936 |
| Concept drift | IRM | 2.248 / 1.237 | 0.846 / 0.754 | 0.201 / 0.367 | 0.878 / 0.792 |
| Concept drift | VREx | 2.285 / 1.286 | 0.821 / 0.742 | 0.314 / 0.486 | 1.142 / 0.938 |
| Concept drift | EIIL | 2.036 / 1.159 | 0.822 / 0.749 | 0.212 / 0.433 | 1.122 / 0.930 |
| Temporal shift | RevIN | 0.815 / 0.708 | 0.475 / 0.476 | 0.085 / 0.224 | 0.205 / 0.358 |
| Temporal shift | N-S Trans. | 0.781 / 0.688 | 0.484 / 0.481 | 0.086 / 0.226 | 0.203 / 0.355 |
| Temporal shift | SAN | 0.757 / 0.715 | **0.415** / **0.453** | 0.088 / 0.225 | *0.199* / *0.348* |
| Combined | IRM+RevIN | 0.809 / 0.711 | 0.481 / 0.476 | 0.089 / 0.231 | 0.202 / 0.362 |
| Combined | EIIL+RevIN | 0.799 / 0.706 | 0.483 / 0.485 | 0.085 / 0.225 | 0.218 / 0.380 |
| Combined | FOIL | *0.735* / *0.651* | 0.497 / 0.481 | *0.081* / *0.219* | 0.206 / 0.357 |
| Combined | ShifTS (Ours) | **0.668** / **0.613** | *0.470* / *0.468* | **0.076** / **0.214** | **0.194** / **0.348** |

ShifTS is best in 6 and second in 2 of 8 evaluations (p. 8); on ETTh2 MAE, SAN and ShifTS both print 0.348 (SAN underlined, ShifTS bold).

**ShifTS with SAN instead of RevIN, Exchange, Crossformer** (Table 3, p. 9). MSE:

| Horizon | ShifTS | SAN | ShifTS w. SAN |
|---|---|---|---|
| 96 | 0.102 | 0.091 | **0.089** |
| 192 | 0.207 | 0.195 | **0.187** |
| 336 | 0.407 | 0.373 | **0.372** |
| 720 | 1.165 | 1.001 | **0.981** |
| Avg. | 0.470 | 0.415 | **0.407** |

**Ablation, Exchange, $H$ = 96** (Figure 3(b), p. 9). MSE as printed on the bars.

- ShifTS\TS drops temporal-shift handling (RevIN), ShifTS\CD drops SAM (p. 9);
- for PatchTST and iTransformer, which already normalize, ShifTS\TS keeps their standard norm/denorm plus SAM, and ShifTS\CD replaces that norm/denorm with RevIN (p. 15):

| Model | Base | ShifTS\TS | ShifTS\CD | ShifTS |
|---|---|---|---|---|
| Crossformer | 0.338 | 0.242 | 0.107 | 0.102 |
| PatchTST | 0.13 | 0.117 | 0.122 | 0.102 |
| iTransformer | 0.135 | 0.115 | 0.122 | 0.115 |

- The authors' reading (p. 9):
  - handling both shifts gives the lowest error;
  - for models that already normalize (PatchTST, iTransformer), mitigating concept drift helps more than adding RevIN;
  - for Crossformer, which has no temporal-shift mitigation, temporal shift matters more.
  - They conclude "mitigating temporal shift is a necessity in mitigating concept drift" (p. 9).

**When ShifTS helps most** (p. 8; Figure 3(a), p. 9):

- Gains are larger on ILI and Exchange than on ETT;
- across datasets, the gain correlates positively and linearly with $\boldsymbol{I}(\mathbf{X}^H; \mathbf{Y}^H)$, with $p = 0.012 \le 0.05$ (p. 8).
- With iTransformer, the gain is about 15% on ILI and Exchange (p. 8).

**Our reading:**

- **"IMP." is the mean of the per-horizon relative MSE (or MAE) reductions.**
  - Recomputed from the printed cells, this matches e.g. Crossformer ILI (81.9%), PatchTST ILI (12.0%), iTransformer Exchange (15.2%) and ETTh1 (5.1%), but not every cell fits:
    - iTransformer ILI MSE gives 11.9% (printed 13.8%), Crossformer Exchange MSE 51.5% (53.5%), Crossformer ETTm1 MSE 77.6% (77.3%), PatchTST ETTm2 16.1/8.7% (15.9/8.6%) (Table 1, p. 7);
    - Informer ETTh2 MSE 87.4% (82.0%) and TimeMixer ETTh1 MSE 17.5% (23.3%) (Table 4, p. 16).
  - A ratio-of-means definition fits worse; the paper doesn't define IMP.
- **Table 3 vs Table 1:** ShifTS on Exchange $H$ = 192 is 0.207 in Table 3 (p. 9) but 0.203 in Table 1 (p. 7).
  - Table 3's 0.207 averages to 0.470, matching Table 2's Exchange ShifTS MSE (p. 8);
  - Table 1's 0.203 would give 0.469, so the Table 1 cell is probably the misprint.
- **The large gains come with weak baselines:**
  - The Crossformer, Informer and Pyraformer ERM numbers are much worse than RevIN alone (Table 2: Crossformer ILI 3.705 vs 0.815 with RevIN, p. 8).
  - Against RevIN, ShifTS improves Crossformer ILI MSE from 0.815 to 0.668 and ETTh1 from 0.085 to 0.076 (p. 8).
  - With models that already normalize (PatchTST, iTransformer, TimeMixer), gains on ETT are 2–23%, 8 of the 12 ETT MSE values between 2% and 9% (pp. 7, 16).
- In the iTransformer ablation, ShifTS\TS and ShifTS score the same (0.115): adding RevIN brings nothing there (Figure 3(b), p. 9).
- No variance across runs is reported, so small differences (third decimal on ETTm1/ETTm2) can't be judged.
- The concept-drift baselines depend on the arbitrary $k$ time segments used as environments (p. 15), with $k$ unstated.

## Assumptions and limitations

- **Univariate target with exogenous features** ($d_{\mathbf{Y}} = 1$, $d_{\mathbf{X}} \ge 1$, p. 2); concept drift as defined needs exogenous features at all (p. 13).
- **Horizon patterns of exogenous features are assumed causally informative** for the target (p. 3: "We assume that incorporating causal relationships from the horizon window enables more complete causality modeling");
  ShifTS helps less when $\boldsymbol{I}(\mathbf{X}^H; \mathbf{Y}^H)$ is low (p. 8).
- **Invariance is assumed to mean "consistent correlation across most time steps"** (p. 4); patterns with sporadic correlations are treated as spurious.
- **Marginals must be stabilized first:** RevIN is assumed sufficient; more advanced temporal-shift methods are out of scope (p. 5), though Table 3 shows SAN would help (p. 9).
- **Standard offline forecasting** with fixed train/validation/test splits (p. 14); no online or continual setting.
- **Datasets chosen for having shift:** near-stationary datasets are excluded: Traffic and Weather (p. 6), Electricity (p. 14).
- **Stated by the authors** (Appendix E, p. 16): (1) no theoretical guarantee, e.g. no analysis of how much the error bound tightens; (2) SAM and ShifTS "are not the only possible solutions".
- **Our reading:**
  - no seeds or variances;
  - the main comparison with distribution-shift baselines uses only Crossformer, the model with the weakest ERM baseline; and
  - the claim that estimating $\mathbf{X}^{\text{SUR}}$ is easier than $\mathbf{X}^H$ (p. 4) is argued, not measured.

## Relevance to this thesis

**Our reading:**

- **Vocabulary for drift.** The paper gives a clean two-way split for time series:
  - **temporal shift** (marginals change: mean, variance, autocorrelation of a series) and
  - **concept drift** (the relationship between exogenous features and the target changes).
  - When we describe the drift between our tasks (successive periods or datasets), we can say which kind each one is;
    most of what happens between periods of one signal is temporal shift in this vocabulary.
- **Temporal shift has a cheap, standard remedy:** instance normalization (RevIN) before the model and denormalization after.
  - Any comparison of joint training vs task arithmetic on drifting series should fix whether RevIN-style normalization is used,
    because it alone changes errors by large factors (Table 2, p. 8: Crossformer ILI MSE 3.705 → 0.815).
- **Environment labels from time:** splitting the training set into $k$ equal-length time segments as "environments" (p. 15) is close to how we may define tasks (periods of a series);
  it's a precedent for treating time segments as distinct tasks.
- **Dataset selection:** the paper uses ETTh1/ETTh2/ETTm1/ETTm2, Exchange and ILI precisely because they show distribution shift, and excludes Traffic, Electricity and Weather as near-stationary (p. 6, p. 14).
  - That is a useful argument when choosing forecasting datasets where drift matters.
- **Standard forecasting protocol** to align with:
  - lookback 96, horizons {96, 192, 336, 720} for ETT and Exchange;
  - lookback 36, horizons {24, 36, 48, 60} for ILI;
  - MSE and MAE;
  - TSLib implementations (pp. 14–15).
- **Not covered:** anomaly detection, multivariate targets, continual or sequential training, and model merging.
  - The paper's concept drift is about $\mathbf{X} \to \mathbf{Y}$ correlations, which for unsupervised anomaly detection (no target) has no direct counterpart.

## Quotes worth keeping

> "Temporal shift (also known as virtual shift (Tsymbal, 2004)) is the marginal probability distributions changing over time, while the conditional distributions are the same." (Definition 2.1, p. 2)

> "Concept drift (also known as real concept drift (Gama et al., 2014)) is the conditional distributions changing over time, while the marginal probability distributions are the same." (Definition 2.2, p. 2)

> "However, these invariant learning methods typically rely on explicit environment labels as input (e.g., labeled rotation or noisy images in image classification), which are not readily available in time series datasets." (p. 3)

> "While the primary contribution of this work is to mitigate concept drift in time-series forecasting, addressing temporal shifts is equally critical and serves as a prerequisite for effectively managing concept drift." (p. 5)

> "Unlike temporal shift, concept drift involves multiple correlated time series and is not an inherent issue in univariate time series analysis." (p. 13)

> "First, the distribution shift methods in time-series forecasting, including ShifTS, lack a theoretical guarantee." (p. 16)
