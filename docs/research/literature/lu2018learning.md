# lu2018learning — Learning under Concept Drift: A Review

- **Status:** verified (2026-11-08): checked against the paper by an independent agent (about 190 claims, every table cell and equation exact: 2 minor misstatements and 1 unverifiable detail, fixed)
- **Reference:** Lu, Liu, Dong, Gu, Gama, Zhang; IEEE Transactions on Knowledge and Data Engineering 31(12), 2346–2363 (2018 per Crossref and the arXiv journal reference, the online date; volume 31, issue 12 is the December 2019 print issue); not printed in the arXiv PDF; DOI 10.1109/TKDE.2018.2876857; arXiv 2004.05785 ([references.bib](references.bib))
- **Version read:** arXiv v1 (stamped 13 Apr 2020 in the margin of p. 1), 18 pages: main text pp. 1–15 (Sections 1–8), acknowledgments p. 15, references [1]–[140] pp. 15–18, author biographies p. 18
- **Read:** everything: main text (Sections 1–8), Tables 1–4, Figures 1–15, acknowledgments; references and biographies skimmed (only reference titles used below)
- **Code:** none given in the paper

## In one paragraph

A review of over 130 publications (p. 1; 137 research articles after the selection process, p. 2) on learning when the data distribution of a stream changes over time ("concept drift").

It:

- defines concept drift as a change of the joint distribution $P_t(X, y)$ (p. 2);
- splits it into three sources by which factor of $P_t(X)\,P_t(y|X)$ changes (p. 3); and
- names four types by how the change unfolds in time: sudden, gradual, incremental, reoccurring (Fig. 4, p. 3).

Its main contribution is a framework with three components: **drift detection** (whether drift occurs), **drift understanding** (when, how severe, where), and **drift adaptation** (how to react) (pp. 1–2, Fig. 2).

Detection methods are grouped by their test statistic into error rate-based, data distribution-based and multiple hypothesis tests (Section 3, Table 1, p. 8); adaptation methods into simple retraining, ensemble retraining and model adjusting (Section 5, p. 9).

It:

- reviews evaluation (validation procedures, metrics, statistical tests; Section 6.1);
- lists 10 synthetic and 14 real-world datasets (Tables 3–4, pp. 13–14); and
- closes with seven findings and four research directions (pp. 14–15).

## Problem

**The question:** how to organize the research on learning under concept drift, which "has become noticeably systematic" (p. 1), into one framework, and update earlier surveys with methods published since (p. 2).

**Positioning** (pp. 1–2):

- An earlier survey (2014, its ref. [8]) "intentionally left certain sub-problems of concept drift to other publications", such as the details of the data distribution change $P(X)$ (p. 1).
- A 2015 survey ([9]) takes an "active and passive" view (pp. 1–2).
- Four other surveys ([6], [7], [10], [11]) focus on data stream learning only (p. 2).
- Since then, "a new category of drift detection methods has arisen, named multiple hypothesis tests drift detection" (p. 2).

**Stated contributions** (p. 2):

- the three-category framework (detection, understanding, adaptation);
- "concept drift understanding" proposed as a new component, which "creates a connection between drift detection and drift adaptation";
- coverage of new techniques (active learning under drift, fuzzy competence model-based detection);
- a systematic look at synthetic and real-world datasets;
- research directions.

**How references were selected** (p. 2), in four steps:

1. Databases: Science Direct, ACM Digital Library, IEEE Xplore, SpringerLink.
2. Keyword search; kept if they present new theory, algorithm or methodology on concept drift, or report a concept drift application.
3. Split into detection, understanding, adaptation; filtered again by time ("published mainly within the last 10 years") or impact ("published in high quality journals/conferences or having high citations").
4. Dataset selection: popular datasets, their characteristics, providers and use.

Result: 137 research articles, 10 synthetic datasets, 14 real-world datasets (p. 2).

**Setting throughout:** streaming data, a learner that predicts a label $y$ from features $X$, and true labels that (in most methods) arrive after prediction (finding 4, p. 14).

Almost all methods and datasets are classification.

## Definitions

### Concept drift (p. 2)

Concept drift is "a phenomenon in which the statistical properties of a target domain change over time in an arbitrary way" (p. 2).

These changes "might be caused by changes in hidden variables which cannot be measured directly" (p. 2).

The notion "was first proposed by [12] who aimed to point out that noise data may turn to non-noise information at different time" (p. 2).

**Formal definition** (p. 2). Given a time period $[0, t]$ and a set of samples

$$S_{0,t} = \{d_0, \dots, d_t\}, \qquad d_i = (X_i, y_i),$$

where $X_i$ is the feature vector and $y_i$ the label, and $S_{0,t}$ follows a distribution $F_{0,t}(X, y)$, concept drift occurs at timestamp $t+1$ if

$$F_{0,t}(X, y) \neq F_{t+1,\infty}(X, y),$$

denoted as

$$\exists t : P_t(X, y) \neq P_{t+1}(X, y).$$

So concept drift at time $t$ is "the change of joint probability of $X$ and $y$ at time $t$" (p. 3).

**Other names** (pp. 2–3): dataset shift (ref. [15]), concept shift (ref. [1]).

- Ref. [16] treats concept drift (or shift) as one subcategory of dataset shift, which consists of covariate shift, prior probability shift and concept shift.
- The review instead follows the publications that call any change of $P_t(X, y)$ "concept drift", since "concept drift is usually associated with covariate shift and prior probability shift" (p. 3).

### Sources of drift (p. 3, Fig. 3)

Using the decomposition

$$P_t(X, y) = P_t(X) \times P_t(y|X),$$

concept drift can be triggered by three sources (p. 3):

| Source | Condition | Other name in the paper | Effect stated |
|---|---|---|---|
| I | $P_t(X) \neq P_{t+1}(X)$ while $P_t(y\|X) = P_{t+1}(y\|X)$ | virtual drift (citing [7]); feature space drift | "does not affect the decision boundary" |
| II | $P_t(y\|X) \neq P_{t+1}(y\|X)$ while $P_t(X) = P_{t+1}(X)$ | actual drift; decision boundary drift | "will cause decision boundary change and lead to learning accuracy decreasing" |
| III | $P_t(X) \neq P_{t+1}(X)$ and $P_t(y\|X) \neq P_{t+1}(y\|X)$ | mixture of I and II | both changes "convey important information about learning environment" |

"In many real-world applications, Source I and Source II occur together, which creates Source III" (p. 3).

**Fig. 3** (p. 3): two-dimensional data $X = \{x_1, x_2\}$ with two class labels $y = \{y_0, y_1\}$, shown at time $t$ and $t+1$.

- (a) Source I: the points move, the separating line stays.
- (b) Source II: the points stay, the separating line rotates.
- (c) Source III: both change.

A drift of $P_t(y)$ as a source appears only in the description of the IV-Jac detector (p. 6), not in this list of sources; p. 13 uses "label-drift" in a different sense (class labels not known in advance).

### Types of drift by how change happens over time (p. 3, Fig. 4)

Four types, following ref. [8] (p. 3). **Fig. 4** plots "data distribution" against time with blue (old) and red (new) blocks; its captions, verbatim:

| Type | Caption in Fig. 4 | Picture |
|---|---|---|
| Sudden drift | "A new concept occurs within a short time." | blue blocks, then only red blocks from one point on |
| Gradual drift | "A new concept gradually replaces an old one over a period of time." | blue and red blocks alternate, red becoming more frequent until only red remains |
| Incremental drift | "An old concept incrementally changes to a new concept over a period of time." | blocks whose level and color shift step by step from the old to the new concept |
| Reoccurring concepts | "An old concept may reoccur after some time." | blue, then red for a while, then blue again |

What research on each type focuses on (p. 3):

- **Types 1–3:** "how to minimize the drop in accuracy and achieve the fastest recovery rate during the concept transformation process".
- **Type 4:** "the use of historical concepts, that is, how to find the best matched historical concepts with the shortest time". "The new concept may suddenly, incrementally, or gradually reoccur."

**Intermediate concepts** (p. 3, citing [8] and [4]):

- Drift "may not only take place at an exact timestamp, but may also last for a long period", so intermediate concepts may appear between the starting and the ending concept.
- An intermediate concept can be "a mixture of the starting concept and the ending concept, like the incremental drift, or one of the starting or ending concept, such as the gradual drift" (p. 3).

## The framework: detection, understanding, adaptation (pp. 1–2, Fig. 2)

"Conventional machine learning has two main components: training/learning and prediction. Research on learning under concept drift presents three new components" (p. 1):

- **Drift detection:** whether or not drift occurs.
- **Drift understanding:** when, how, where it occurs.
- **Drift adaptation:** the reaction to the existence of drift.

**Fig. 2** (p. 2): stream data → training and learning → prediction → concept drift detection.

- If no drift is detected, the loop continues.
- If a drift is detected → concept drift understanding → concept drift adaptation → an "Update" arrow back to training and learning.

The caption notes that "some methods can do concept drift detection and concept drift understanding simultaneously" (p. 2).

Understanding is described as the output of detection and the input of adaptation (p. 7).

## Drift detection (Section 3, pp. 3–8)

### A general four-stage framework (pp. 3–4, Fig. 5)

Drift detection "refers to the techniques and mechanisms that characterize and quantify concept drift via identifying change points or change time intervals" (p. 3).

1. **Data retrieval:** retrieve data chunks from the stream, since "a single data instance cannot carry enough information to infer the overall distribution" (p. 3).
   - Fig. 5 shows a "historical data" window and a "new data" window on the stream (p. 4).
2. **Data modeling (optional):** abstract the retrieved data and extract the key features that most impact a system if they drift.
   - Mainly dimensionality or sample size reduction "to meet storage and online speed requirements" (p. 3).
3. **Test statistics calculation:** a dissimilarity measurement or distance estimation that "quantifies the severity of the drift and forms test statistics for the hypothesis test".
   - "It is considered to be the most challenging aspect of concept drift detection"; how to define "an accurate and robust dissimilarity measurement is still an open question" (p. 3).
4. **Hypothesis test:** evaluates the statistical significance of the change from Stage 3, or the p-value (p. 4).
   - Without it, the test statistics "are meaningless for drift detection", because they cannot say "how likely it is that the change is caused by concept drift and not noise or random sample selection bias" (p. 4).
   - Common tests: estimating the distribution of the test statistics, bootstrapping, the permutation test, and Hoeffding's inequality-based bounds (p. 4).

Without Stage 1, detection can be seen as a **two-sample test** (are two sample sets from the same distribution?), so "any multivariate two-sample test is an option that can be adopted in Stages 2-4" (p. 4).

But "the distribution drift may not be included in the target features", so selecting the target features is "a critical problem in concept drift detection" (p. 4).

**Window schemes** (pp. 4–5):

- **Landmark window** (Fig. 6, p. 4): the starting point is fixed; the end point extends with each new instance.
- **Two windows, new window defined by the user** (Fig. 7, p. 5): the most recent window against the overall window (STEPD).
- **Two sliding windows of fixed size** (Fig. 8, p. 5): the historical window fixed, the new data window moving. The commonly used strategy for distribution-based detectors (p. 5).

### Family 1: error rate-based detection (pp. 4–5)

"The largest category of algorithms" (p. 4). They track the online error rate of base classifiers; a statistically significant increase or decrease triggers a drift alarm (p. 4).

- **DDM** (p. 4): "one of the most-referenced"; "the first algorithm to define the warning level and drift level".
  - Stage 1 is a landmark window.
  - At the warning level, DDM "starts to build a new learner while using the old learner for predictions"; at the drift level, the old learner is replaced by the new one (p. 4).
- **Variants** (p. 4):
  - LLDD splits detection into decision tree node-level problems (Stages 3–4);
  - EDDM uses the distance between two correct classifications (Stage 3);
  - HDDM uses Hoeffding's inequality (Stage 4);
  - FW-DDM a fuzzy time window for gradual drift (Stage 1);
  - DELM keeps DDM but uses an Extreme Learning Machine as base learner.
- **ECDD** (pp. 4–5): an EWMA chart on the error rate with a dynamic mean $\hat{p}_{0,t}$ (online error rate within $[0, t]$) instead of the static $p_0$, and dynamic variance

  $$\sigma^2_{Z_t} = \hat{p}_{0,t}(1 - \hat{p}_{0,t}) \sqrt{\frac{\lambda}{2-\lambda}\left(1 - (1-\lambda)^{2t}\right)},$$

  with $\lambda = 0.2$ recommended (p. 4).

  Warning if $Z_t > \hat{p}_{0,t} + 0.5 L \sigma_{Z_t}$, drift if $Z_t > \hat{p}_{0,t} + L \sigma_{Z_t}$; $L$ given by the authors "through experimental evaluation" (p. 5).
- **STEPD** (p. 5):
  - compares the most recent window with the overall window;
  - $\theta_{\text{STEPD}} \sim \mathcal{N}(0, 1)$;
  - warning and drift significance levels $\alpha_w = 0.05$, $\alpha_d = 0.003$.
- **ADWIN** (p. 5):
  - needs only the total size $n$ of a "sufficiently large" window $W$;
  - examines all cuts of $W$ into $w_{\text{hist}}$ and $w_{\text{new}}$;
  - test statistic $\theta_{\text{ADWIN}} = |\hat{\mu}_{\text{hist}} - \hat{\mu}_{\text{new}}|$;
  - a cut is found when the difference exceeds a threshold with confidence $\delta$;
  - false positive and false negative rates "are bounded by $\delta$".
  - Many adaptation methods derive from or combine with ADWIN (p. 5).

**Stated limit:** error rate-based detection "cannot directly measure the severity of concept drift, because it mainly focuses on monitoring the performance of the learning system, not the changes in the concept itself" (p. 7).

### Family 2: data distribution-based detection (p. 5)

"The second largest category" (p. 5).

A distance function quantifies the dissimilarity between the historical and the new data distribution; a statistically significant difference triggers model update (p. 5).

**Stated pros** (p. 5):

- they "address concept drift from the root sources, which is the distribution drift";
- they identify the time of drift and "can also provide location information about the drift".

**Stated cons** (p. 5):

- "usually reported as incurring higher computational cost than the algorithms mentioned in Section 3.2.1";
- they "usually require users to predefine the historical time window and new data window".

- **First formal treatment** (ref. [37], p. 5): total variation as the most natural distance,

  $$TV(P_1, P_2) = 2 \sup_{E \in \varepsilon} |P_1(E) - P_2(E)|,$$

  or, with densities, $\text{dist}_{L^1} = \int |f_1(x) - f_2(x)|\,dx$ (notation as printed, p. 5).

  It proposes the Relativized Discrepancy (RD) family, with bounds on missed detections and false alarms via Chernoff bounds and the VC dimension; a suitable Stage 2 data model "is an open question" (p. 5).
- **ITA** (p. 5):
  - kdqTree partitions historical and new data into bins;
  - KL divergence per bin;
  - bootstrapping by merging $W_{\text{hist}}, W_{\text{new}}$ and resampling;
  - drift confirmed when $P(\theta^*_{\text{ITA}} \geq \theta_{\text{ITA}}) < 1 - \alpha$.
- **Others** (p. 5): SCD, CM (competence model), SyncStream, PCA-CD, EDE, LSDD-CDT, LSDD-INC, LDD-DSDA.

### Family 3: multiple hypothesis test detection (pp. 5–7)

They use techniques of the first two families but "multiple hypothesis tests to detect concept drift in different ways" (pp. 5–6). Two groups (p. 6):

**Parallel** (Fig. 9, p. 6): $z$ test statistics and $z$ hypothesis tests on $W_{\text{hist}}$ and $W_{\text{new}}$ at once.

- **JIT** (p. 6), the first of this kind: extends CUSUM (CI-CUSUM) to detect mean changes in features.
  - Four configurations:
    - (1) PCA features (drop eigenvalues whose sum is below a threshold, e.g. 0.001);
    - (2) PCA features plus one generic component of the original features;
    - (3) each feature individually;
    - (4) all combinations of features.
  - Config 2 is preferred; Config 1 "may have a high missing rate", Config 3 "suffers from a high false alarm rate", Config 4 "has exponential computational complexity" (p. 6).
- **LFR** (p. 6): tracks TP, TN, FP, FN rates online, with warning and drift levels.
- **IV-Jac / three-layer** (p. 6): separate layers for label drift $P_t(y)$, feature space drift $P_t(X)$ and decision boundary drift $P_t(y|X)$.
  - Thresholds $\theta_{P_t(y)} = \theta_{P_t(X)} = \theta_{P_t(X|y)} = 0.5$ by default, chosen empirically (subscript as printed).
- **e-Detector** (p. 6) and **DDE**: ensembles of heterogeneous detectors; e-Detector reports a drift as soon as any base detector does ("early-find-early-report").

**Hierarchical** (Fig. 10, p. 6): "an emerging drift detection category that has a multiple verification schema": a detection layer, then a validation layer that re-tests a detected drift.

- **HCDTs** (p. 6): the first hierarchical one.
  - The detection layer can be any detector "that has a low drift delay rate and low computational burden".
  - Validation by likelihood-based estimation of the test statistic's distribution, or by an existing test (Kolmogorov-Smirnov, Cramer-Von Mises).
- **HLFR** (p. 6): LFR as detection layer; validation by zero-one loss $E$ over the ordered train-test split, confirmed if above $\eta = 0.01$.
- **TSMSD-EWMA** (p. 6): similar, not claimed as hierarchical by its authors.
- **HHT-CU, HHT-AG** (pp. 6–7): "request and reverify".
  - HHT-AG uses KS tests per feature, then $d$ two-dimensional KS tests on feature-label pairs; it "can handle concept drift with less true labels", useful "when dealing with high verification latency" (p. 7).

### Table 1 and Table 2: detectors by stage and by what they understand

**Table 1** (p. 8) lists each detector's implementation of the four stages; **Table 2** (p. 9) ticks whether it identifies When, How, Where.

Merged here (every detector is ticked under When in Table 2; Table 2 names [52] "EWMA"):

| Category | Algorithm | Stage 1 | Stage 2 | Stage 3 | Stage 4 | How | Where |
|---|---|---|---|---|---|---|---|
| Error rate-based | DDM [20] | Landmark | Learner | Online error rate | Distribution estimation | | |
| | EDDM [26] | Landmark | Learner | Online error rate | Distribution estimation | | |
| | FW-DDM [5] | Landmark | Learner | Online error rate | Distribution estimation | | |
| | DEML [27] | Landmark | Learner | Online error rate | Distribution estimation | | |
| | STEPD [30] | Predefined $w_{\text{hist}}$, $w_{\text{new}}$ | Learner | Error rate difference | Distribution estimation | | |
| | ADWIN [31] | Auto cut $w_{\text{hist}}$, $w_{\text{new}}$ | Learner | Error rate difference | Hoeffding's Bound | | |
| | ECDD [29] | Landmark | Learner | Online error rate | EWMA Chart | | |
| | HDDM [23] | Landmark | Learner | Online error rate | Hoeffding's Bound | | |
| | LLDD [25] | Landmark, or sliding $w_{\text{hist}}$, $w_{\text{new}}$ | Decision trees | Tree node error rate | Hoeffding's Bound | | ✓ |
| Data distribution-based | kdqTree [22] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | kdqTree | KL divergence | Bootstrapping | ✓ | ✓ |
| | CM [2], [3] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | Competence model | Competence distance | Permutation test | ✓ | ✓ |
| | RD [37] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | KS structure | Relativized Discrepancy | VC-Dimension | ✓ | |
| | SCD [38] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | kernel density estimator | log-likelihood | Distribution estimation | ✓ | |
| | EDE [40] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | Nearest neighbor | Density scale | Permutation test | | |
| | SyncStream [36] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | PCA | P-Tree | Wilcoxon test | ✓ | |
| | PCA-CD [39] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | PCA | Change-Score | Page-Hinkley test | ✓ | |
| | LSDD-CDT [21] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | Learner | Relative difference | Distribution estimation | | |
| | LSDD-INC [41] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | Learner | Relative difference | Distribution estimation | | |
| | LDD-DSDA [4] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | k-nearest neighbor | Local drift degree | Distribution estimation | ✓ | ✓ |
| Multiple hypothesis tests | JIT [19] | Landmark | Selected features | 4 configurations | Distribution estimation | | |
| | LFR [46] | Landmark | Learner | TP, TN, FP, FN | Distribution estimation | | |
| | Three-layer [47] | Sliding both $w_{\text{hist}}$, $w_{\text{new}}$ | Learner | $P(y)$, $P(X)$, $P(X\|y)$ | Distribution estimation | | |
| | e-Detector [48] | depends on base detector | depends | depends | depends | | |
| | DDE [49] | depends on base detector | depends | depends | depends | | |
| | TSMSD-EWMA [52] | Landmark | Learner | Online error rate | EWMA Chart | | |
| | HCDTs [50] | Landmark | Depending on layers | Depending on layers | Depending on layer | | |
| | HLFR [51] | Landmark | Learner | TP, TN, FP, FN | Distribution estimation | | |
| | HHT-CU [53] | Landmark | Learner | Classification uncertainty | Layer-I Hoeffding's Bound, Layer-II Permutation Test | | |
| | HHT-AG [53] | Fixed $w_{\text{hist}}$, Sliding $w_{\text{new}}$ | N/A | KS statistic on each attribute | Layer-I KS test, Layer-II 2D KS test | | |

A comparative study of eight popular detectors is in ref. [54] (p. 7).

## Drift understanding (Section 4, pp. 7–9)

Retrieving "When" (the time a drift occurs and how long it lasts), "How" (its severity or degree) and "Where" (its regions) (p. 7).

### When (p. 7)

- The variable $t$ in $\exists t : P_t(X, y) \neq P_{t+1}(X, y)$ is the drift time; "a delay or a false alarm will lead to failure of the learning system to track new concepts" (p. 7).
- Understanding should cover the start time, the change period and the end time (p. 7).
- **Fig. 11** (p. 7): an incremental drift from $t+1$ to $t+5$ and a sudden drift between $t+9$ and $t+10$, with the alarm triggered after the start of the drift.
- The alarm "is delayed compared to the actual drifting timestamp, since most drift detectors require a minimum number of new data to evaluate the status of the drift" (p. 7).
- **Warning levels** (p. 7): DDM, EDDM, STEPD, HDDM use a relaxed threshold, e.g. warning at p-value 95% or $2\sigma$, drift at p-value 99% or $3\sigma$.
  - "the data accumulated between the warning level and the drift level are used as the training set for updating a learning model".

### How: severity (pp. 7–8)

Formally (p. 7):

$$\Delta = \delta\big(P_t(X, y), P_{t+1}(X, y)\big),$$

where $\delta$ measures the discrepancy of two distributions; $\Delta$ is usually non-negative, and larger means more severe (p. 7).

- **From error rate-based detectors** (p. 7), only indirectly:
  - e.g. $\Delta \sim p_i - p_{\min}$ (DDM, DELM);
  - $\Delta \sim \hat{p}_{\text{new}} - \hat{p}_{\text{hist}}$ (STEPD);
  - $\Delta \sim E[\hat{Y}_{i-\text{cut}}] - E[\hat{X}_{\text{cut}}]$ (HDDM).
  - "However, the meaning of these differences is not discussed in existing publications" (p. 7).
- **From distribution-based detectors** (pp. 7–8), directly:
  - a relaxation of total variation $d_{\mathcal{A}}(S_1, S_2)$ ([37]);
  - a competence-based distance $d^{CB}$ ([3]);
  - KL divergence $D(W_1 \| W_2)$ ([22]).
  - "The range of these distances is $[0, 1]$": 1 means a completely different concept, 0 identical (p. 8).
- **Use for adaptation** (p. 8):
  - if severity is low, "adjusting the current learner by incremental learning will be adequate";
  - if high, "discarding the old learner and retraining a new one could be better than incrementally updating the old learner".
  - But this information "is not yet widely utilized in drift adaptation" (p. 8).

### Where: drift regions (pp. 8–9)

Drift regions are "the regions of conflict between a new concept and the previous concept", found where $P_t(X, y)$ and $P_{t+1}(X, y)$ differ significantly (p. 8).

**Fig. 12** (p. 8): data uniform in $[0, 10]^2$; boundary $x_1 + x_2 = 8$ at time $t$ and $x_1 + x_2 = 9$ at $t+1$; points with $8 \leq x_1 + x_2 < 9$ change class and form the drift region.

Methods (p. 9):

- decision tree leaves with drift detectors (LLDD [25]);
- kdq-tree nodes with Kulldorff's spatial scan statistic ([22]);
- top-$p$-competence areas over hyperspheres of a competence model ([2]);
- local drift degree, a change in regional density (LDD-DSDA [4]).

Why it helps adaptation (p. 9):

- some regions of the feature space "will remain stable significantly longer than other regions" (ref. [56]), so old models stay useful there;
- drift regions help separate obsolete data from noise and from novel data (refs. [3], [2]).

**Summary** (p. 9, Table 2): all detectors identify When; most distribution-based ones also How; "only a few algorithms have the ability to locate drift regions (where)".

## Drift adaptation (Section 5, pp. 9–11)

"Three main groups of drift adaptation methods, namely simple retraining, ensemble retraining and model adjusting, that aim to handle different types of drift" (p. 9).

The section headings pair each group with a kind of drift: retraining "for global drift", ensembles "for recurring drift", adjusting "for regional drift" (pp. 9–11).

| Group | Idea | Stated pros | Stated cons or conditions |
|---|---|---|---|
| Training new models for global drift (5.1, pp. 9–10, Fig. 13) | retrain a new model on the latest data to replace the obsolete one | Paired Learners: "simple to understand and easy to implement, and can be applied at any point in the data stream" (p. 9) | "An explicit concept drift detector is required to decide when to retrain […]" (p. 9); window size trade-off (p. 10) |
| Model ensemble for recurring drift (5.2, pp. 10–11, Fig. 14) | keep a set of base classifiers combined by voting; add new ones on drift | "preserving and reusing old models can save significant effort to retrain a new model for recurring concepts" (p. 10) | DWM: adding classifiers "may be triggered too frequently", with performance issues e.g. under gradual drift (p. 10) |
| Adjusting existing models for regional drift (5.3, p. 11, Fig. 15) | partially update the model where the distribution changed | "arguably more efficient than retraining when the drift only occurs in local regions" (p. 11) | mostly decision trees; the Hoeffding bound behind VFDT "may not be appropriate" for node splitting (p. 11) |

### Retraining (pp. 9–10)

- A window strategy keeps the most recent data for retraining and/or old data for the distribution test (p. 9).
- **Paired Learners** (p. 9): a stable and a reactive learner; if the stable one often misclassifies what the reactive one gets right, the reactive one replaces it.
- **Window size trade-off** (p. 10): "A small window can better reflect the latest data distribution, but a large window provides more data for training a new model."
  - ADWIN finds the cut automatically, drops the old window, and trains on the latest (p. 10).
- **Integrated detection and retraining** (p. 10):
  - DELM adds hidden nodes when the error rate increases;
  - FP-ELM adds a forgetting parameter;
  - a parallel ELM;
  - OS-ELM ensembles with ordered aggregation.
- **Lazy learners** (p. 10):
  - JIT with kNN removes instances older than the last $T$ on drift;
  - extensions handle recurrent concepts by comparing with stored concepts;
  - NEFCS with competence-based detection and Stepwise Redundancy Removal.

### Ensembles (pp. 10–11)

- Extensions of classical ensembles (p. 10):
  - online bagging;
  - Leveraging Bagging (with ADWIN: on drift, the worst classifier is replaced by one trained on the latest data);
  - adaptive boosting with a hypothesis test;
  - Adaptive Random Forest (ADWIN decides when to replace a tree).
- **DWM** (p. 10): weights by individual and global performance; new classifier when the ensemble errs; weight reduced by a factor when a classifier errs; removed below a threshold.
- **Learn++.NSE** (pp. 10–11): weights by error on the latest batch; a new classifier when the youngest one's error exceeds 50%.
  - Stated benefits:
    - works with almost any base classifier;
    - "does not store history data, only the latest batch of data, which it only uses once […]";
    - handles sudden, gradual and recurrent drift "because underperforming classifiers can be reactivated or deactivated as needed by adjusting their weights" (p. 11).
- Other voting strategies (p. 11): hierarchical ensembles, short and long term memory, dynamic ensemble sizes.
- For specific drift types (p. 11):
  - AUE2 (sudden and gradual equally well: re-weighting reacts to sudden drift, incremental training of all members follows gradual drift);
  - OWA;
  - class evolution ([75]);
  - recurring concepts by reactivating stored obsolete models ([76], [77]) or refining a concept pool ([78]).

### Adjusting models (p. 11)

- **VFDT** (p. 11): Hoeffding bound limits the instances needed to split; advantages:
  - each instance processed once and not stored;
  - the tree stays small unless there is new information;
  - low maintenance cost.
- **CVFDT** (p. 11): an alternative subtree trained on a sliding window replaces the original if it performs better.
- **VFDTc** and extensions (p. 11):
  - node-level drift detection (error rate, or distribution difference between a node and its sub-nodes);
  - on drift the node becomes a leaf and its subtree is removed;
  - adaptive leaves.
- **Critique** (p. 11): "recent studies [84], [85] have shown that its foundation, the Hoeffding bound, may not be appropriate for the node splitting calculation because the variables it computes, the information gain, are not independent".
  - Alternatives in [86], [87].

## Evaluation, datasets and benchmarks (Section 6, pp. 11–13)

### Evaluation systems (pp. 11–12)

Three aspects: validation methodology, evaluation metrics, statistical significance (p. 11).

**Validation methodology** (pp. 11–12):

| Procedure | How it works | Stated pros and cons |
|---|---|---|
| Holdout | at time $t$, test on a holdout set that "represents exactly the same concept at that time $t$" | "only applied on synthetic datasets with predefined concept drift times" (p. 12) |
| Prequential | each instance first tests, then trains the model; prequential error $S = \sum_{t=1}^{n} f(\hat{y}_t, y_t)$ | "no need to know the drift time of concepts, and it makes maximum use of the available data" (p. 12) |
| Controlled permutation | several test sets with data order permuted so that instances close in time stay close | "reduces the risk that their prequential evaluation may produce biased results for the fixed order of data in a sequence" (p. 12) |

Three prequential error estimates: a landmark window (interleaved-test-then-train), a sliding window, a forgetting mechanism (p. 12).

**Evaluation metrics** (p. 12). Traditional ones (precision/recall in retrieval, mean absolute scaled error in regression, root mean square error in recommender systems), plus:

1. RAM-hours, for computation cost.
2. Kappa statistic, for class imbalance: $\kappa = \dfrac{p - p_{\text{ran}}}{1 - p_{\text{ran}}}$, with $p$ the classifier's accuracy and $p_{\text{ran}}$ that of a random classifier.
3. Kappa-temporal statistic, for streams with temporal dependence: $\kappa_{per} = \dfrac{p - p_{\text{per}}}{1 - p_{\text{per}}}$, with $p_{\text{per}}$ the accuracy of the persistent classifier ("a classifier that predicts the same label as previously observed").
4. Combined kappa: $\kappa^{+} = \sqrt{\max(0, \kappa)\,\max(0, \kappa_{per})}$.
5. Prequential AUC.
6. Averaged Normalized Area Under the Curve (NAUC) for Precision-Range and Recall-Range curves.

**Accuracy of a drift detector** (p. 12): true detection rate, false detection rate, miss detection rate, delay of detection.

**Statistical significance** (p. 12). The three tests most used to compare two learners:

- **McNemar:** with $a$ instances misclassified by the first and correctly classified by the second, $b$ the opposite, $M = \text{sign}(a - b) \times (a - b)^2 / (a + b)$, following a $\chi^2$ distribution.
- **Sign test:** with $B$ instances misclassified by the first and correct for the second, $T$ ties, one-sided $p = \sum_{k=B}^{N-T} \binom{N-T}{k} 0.5^k \times 0.5^{N-T-k}$.
  - If $p$ is below the significance level, the second classifier is better.
- **Wilcoxon signed-rank:** two classifiers on $N$ datasets, measurements $x_{i,1}, x_{i,2}$, $T$ ties, $N_r = N - T$, $W = \sum_{i=1}^{N_r} \big(\text{sign}(x_{i,1} - x_{i,2}) \times R_i\big)$ with $R_i$ the rank by $|x_{i,1} - x_{i,2}|$.
  - Equality rejected if $|W| > W_{\text{critical}, N_r}$ (two-sided).

"All three tests are non-parametric" (p. 12).

For more than two algorithms over multiple datasets, the **Nemenyi test** on average ranks: two differ if their average ranks differ by at least

$$CD = q_\alpha \sqrt{k(k+1)/6N},$$

with $k$ learners, $N$ datasets, $q_\alpha$ from the Studentized range statistic divided by $\sqrt{2}$ (p. 12).

### Synthetic datasets (Table 3, p. 13)

Generated by predefined rules, so "a good option for evaluating the performance of learning algorithms in different concept drift scenarios" (p. 12).

"Custom" as printed (set by the generator).

The "used by references" column is left out.

| # | Dataset | #Insts. | #Attrs. | #Cls. | Types | Sources |
|---|---|---|---|---|---|---|
| 1 | STAGGER [1] | Custom | 3 | 2 | Sudden | II |
| 2 | SEA [100] | Custom | 3 | 2 | Sudden | II |
| 3 | Rotating hyperplane [80], [103] | Custom | 10 | 2 | Gradual; Incremental | II |
| 4 | Random RBF [104] | Custom | Custom | Custom | Sudden; Gradual; Incremental | III |
| 5 | Random Tree [79], [104] | Custom | Custom | Custom | Sudden; Reoccurring | II |
| 6 | LED [106] | Custom | 24 | 10 | Sudden | II |
| 7 | Waveform [106] | Custom | 40 | 3 | Sudden | II |
| 8 | Sine [20] | Custom | 2 | 2 | Sudden | II |
| 9 | Circle [20] | Custom | 2 | 2 | Gradual | III |
| 10 | Rotating chessboard [67] | Custom | 2 | 2 | Gradual | II |

### Real-world datasets (Table 4, p. 14)

Publicly available, "including real-world datasets with synthetic drifts" (p. 12). The "used by references" column is left out.

| # | Dataset | #Insts. | #Attrs. | #Cls. |
|---|---|---|---|---|
| 1 | Airlines [104] | 539384 | 7 | 2 |
| 2 | Covertype [106] | 581012 | 54 | 7 |
| 3 | Electricity [109] | 45312 | 8 | 2 |
| 4 | Poker-Hand [106] | 1025010 | 10 | 10 |
| 5 | NOAA weather [67] | 18159 | 8 | 2 |
| 6 | Sensor [108] | 2219803 | 5 | 54 |
| 7 | KDDCup'99 [106] | 494021 | 41 | 23 |
| 8 | Usenet1 [112] | 1500 | 99 | 2 |
| 9 | Usenet2 [112] | 1500 | 99 | 2 |
| 10 | Email_data [110] | 1500 | 913 | 2 |
| 11 | Spam_data [110] | 9324 | 499 | 2 |
| 12 | Spam assassin corpus [111] | 9324 | 39916 | 2 |
| 13 | ECUE drift dataset 1 [113] | 10983 | 287034 | 2 |
| 14 | ECUE drift dataset 2 [113] | 11905 | 166047 | 2 |

**Kinds of drift in them** (p. 12):

- Temporal drift over different periods, e.g. daily (Sensor), seasonally (Electricity) or yearly (Airlines, NOAA weather); geographical (Covertype); categorical (Poker-Hand).
- Some, mainly text, target a specific type: sudden (Email_data), gradual (Spam assassin corpus), recurrent (Usenet), novel class (KDDCup'99, ECUE drift dataset 2).

**Two stated limitations of real-world datasets** (pp. 12–13): "1) the groud truth of precise start and end time of drifts is unknown; 2) some real datasets may include mixed drift types".

These "make it difficult to evaluate methods for understanding the drift, and could introduce bias when comparing different machine learning models" (pp. 12–13).

## Concept drift in other research areas (Section 7, pp. 13–14)

- **Class imbalance** (p. 13):
  - Learn++.CDS (Learn++.NSE with SMOTE);
  - Learn++.NIE (bagging instead of SMOTE);
  - ESOS-ELM with a drift detector that retrains on drift;
  - OOB and UOB (resampling and time-decayed metrics).
- **Big data mining** (p. 13): velocity, volume and scalability; OMR-DDM (map-reduce error rate), MC-NN (micro-clusters).
- **Active and semi-supervised learning** (pp. 13–14):
  - active learning under a labeling budget with DDM-based adaptation;
  - Gaussian mixture on labeled and unlabeled data for gradual drift;
  - cluster-based semi-supervised ensembles;
  - SAND;
  - studies "that focus on adapting to concept drift in circumstances where true label data is completely unavailable" (p. 14).
- **Decision rules** (p. 14): VFDR and Adaptive VFDR, PRISM-based rules, fuzzy rules with pruning and recall of rules for recurring concepts.
- **Others** (p. 14): among them, ref. [139] "considered the concept drift problem in time series and developed an online explicit drift detection method by monitoring time series features".

## Findings and research directions (Section 8, pp. 14–15)

**Seven findings** (p. 14):

1. Error rate-based and distribution-based detection still dominate; multiple hypothesis tests emerge.
2. All detectors answer "When", "very few methods have the ability to answer 'How' and 'Where'".
3. Adaptive models and ensembles play an increasingly important role; "research of retraining models with explicit drift detection has slowed".
4. Most methods "assume the ground true label is available after classification/prediction, or extreme verification latency"; little research on unsupervised or semi-supervised detection and adaptation.
5. Computational intelligence techniques (fuzzy logic, competence model) have been applied.
6. "There is no comprehensive analysis on real-world data streams from the concept drift aspect", such as drift time, severity and regions.
7. More research areas recognize drift, especially big data.

**Four research directions** (pp. 14–15):

1. Detection should also provide drift severity and regions, "for better concept drift adaptation" (p. 14).
2. True labels can be expensive, so "unsupervised or semi-supervised drift detection and adaptation could still be promising in the future" (pp. 14–15).
3. "A framework for selecting real-world data streams should be established for evaluating learning algorithms handling concept drift" (p. 15).
4. "Research on effectively integrating concept drift handling techniques with machine learning methodologies for data-driven applications is highly desired" (p. 15).

## Assumptions and limitations

- **Supervised streams:** the definitions use labeled pairs $(X_i, y_i)$ (p. 2), and most reviewed methods assume true labels arrive after prediction (finding 4, p. 14).
- **Classification focus:** the reviewed detectors and adapters are classifiers (error rate, decision trees, voting ensembles), and all datasets in Tables 3–4 have a number of classes (pp. 13–14).
  - In the main text, regression appears only as a metric example, mean absolute scaled error (p. 12).
- **No experiments:** the review compares methods by their design (Tables 1–2), not by measured performance; it points to ref. [54] for a comparative study of eight detectors (p. 7).
- **Real-world datasets** lack ground-truth drift times and may mix drift types (pp. 12–13); the authors call for a framework to select real-world streams (p. 15).
- **Severity and regions** are rarely used by adaptation methods (p. 8, p. 14).
- **Minor inconsistencies in the text:**
  - the abstract says "over 130" publications, Section 1 says 137 research articles (p. 1, p. 2);
  - "ECCD" on p. 7 refers to ECDD;
  - Table 2 calls ref. [52] "EWMA" and Table 1 "TSMSD-EWMA" (pp. 8–9);
  - the three-layer detector's Layer III is $P_t(y|X)$ in the text, but its threshold $\theta_{P_t(X|y)}$ (p. 6) and Table 1's Stage 3 $P(X|y)$ (p. 8) use $X|y$;
  - the method is spelled "DELM" in the text and "DEML" in Tables 1–2 and once on p. 4.
- **Our reading:**
  - the review predates deep learning-based streaming methods in its coverage:
    - nothing on neural networks beyond Extreme Learning Machines,
    - nothing on pre-trained models, fine-tuning or weight-space methods, and
    - nothing on forecasting or anomaly detection as tasks.
  - Its "virtual drift" (Source I) is treated as harmless to the decision boundary, which is a classification view: for density-based or reconstruction-based anomaly detection, a change in $P(X)$ is exactly what the model learns.

## Relevance to this thesis

**Our reading:**

- **Vocabulary for describing drift in our datasets:** the joint-distribution definition (p. 2), the three sources (p. 3) and the four types (Fig. 4, p. 3) give a standard way to characterize each time-series dataset or split:
  - which factor changes, and
  - whether the change is sudden, gradual, incremental or reoccurring.
- **Mapping to our tasks:**
  - For forecasting, $X$ is the input window and $y$ the future values, so Source I is a change of the input regime and Source II a change of the dynamics.
  - For unsupervised anomaly detection there is no $y$ during training, so only $P(X)$ is observed: in the paper's terms, the drift we can see is "virtual", even though it is what matters for a model of normal behavior.
- **The adaptation families frame our comparison:**
  - *Simple retraining* corresponds to retraining or fine-tuning on the latest window only.
  - *Joint training* on all data seen so far is not one of the paper's three groups; it is closest to retraining with a growing (landmark) window.
  - *Ensembles for recurring drift* store one model per concept.
    - Task arithmetic keeps one task vector per period and merges them into one model, which reads as a compressed ensemble without the inference cost of voting.
  - *Model adjusting for regional drift* is the closest analogue of updating only part of a model.
- **Reoccurring concepts** (p. 3, p. 10) are the case where keeping old knowledge pays off, and the case where forgetting is most costly: a test for merging versus sequential fine-tuning.
- **Severity as a guide** (p. 8): low severity favors incremental updates, high severity favors retraining.
  - This is a hypothesis we could test with a measured distance between periods (e.g. a two-sample statistic) against which strategy wins.
- **Evaluation protocol:**
  - Holdout per concept fits synthetic or known-boundary splits (p. 12), which is our setting when tasks are defined periods; prequential evaluation fits a single stream.
  - The statistical tests (Wilcoxon, Nemenyi critical difference, p. 12) are candidates for a rule on when a difference between methods is real.
  - The kappa-temporal idea, comparing against a persistence baseline (p. 12), parallels naive forecasting baselines in time series.
- **Datasets:** Electricity, NOAA weather and Sensor carry temporal drift (p. 12) but are labeled classification streams (Table 4, p. 14), so they don't fit our tasks directly.
  - They are useful as reference points on what kinds of drift are documented.
  - The real-world limitation (unknown drift times, mixed types, pp. 12–13) applies to our time-series benchmarks too, which favors also using controlled, synthetic drift.
- **Ref. [139]** (drift detection by monitoring time series features, p. 14) is the only time-series-specific pointer in the review; worth a look if drift detection becomes part of the thesis.

## Quotes worth keeping

> "Concept drift means that the statistical properties of the target variable, which the model is trying to predict, change over time in unforeseen ways [1]." (p. 1)

> "Research on learning under concept drift presents three new components: drift detection (whether or not drift occurs), drift understanding (when, how, where it occurs) and drift adaptation (reaction to the existence of drift) as shown in Fig. 2." (p. 1)

> "Concept drift occurs at timestamp $t+1$, if $F_{0,t}(X, y) \neq F_{t+1,\infty}(X, y)$, denoted as $\exists t : P_t(X, y) \neq P_{t+1}(X, y)$" (p. 2)

> "Since $P_t(X)$ drift does not affect the decision boundary, it has also been considered as virtual drift [7]" (p. 3)

> "In many real-world applications, Source I and Source II occur together, which creates Source III." (p. 3)

> "In contrast, the study of Type 4 drift emphasizes the use of historical concepts, that is, how to find the best matched historical concepts with the shortest time." (p. 3)

> "In contrast, if the severity of the concept drift is high, the decision boundary could change significantly, therefore discarding the old learner and retraining a new one could be better than incrementally updating the old learner." (p. 8)

> "In the case of recurring concept drift, preserving and reusing old models can save significant effort to retrain a new model for recurring concepts." (p. 10)

> "A small window can better reflect the latest data distribution, but a large window provides more data for training a new model." (p. 10)

> "There are, however, two limitations of real world data sets: 1) the groud truth of precise start and end time of drifts is unknown; 2) some real datasets may include mixed drift types." (p. 12)
