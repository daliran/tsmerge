# Anomaly detection

**In one sentence:** anomaly detection flags the steps, or stretches, of a series that don't behave as normal.

- **Builds on:** [Tasks](tasks.md), [Patterns](../structure/patterns.md).
- **Used by:** [Windows](../data-preparation/windows.md), [Precision, recall and F1](../../evaluation/precision-recall-f1.md), [AUROC](../../evaluation/auroc.md), [AUPRC](../../evaluation/auprc.md), [Point adjustment](../evaluation/point-adjustment.md), [VUS](../evaluation/vus.md).

## The task

**Purpose:** "identifying unusual or abnormal patterns within a time series, which can indicate critical events, system faults, or outliers" ([wang2026deep](../../../literature/wang2026deep.md), p. 3). In general, anomalies are observations that "deviate significantly from the majority of the data" and "do not conform to a well defined notion of normal behavior" ([Anomaly detection][anomaly]).

**Examples:** industrial maintenance ([wang2026deep](../../../literature/wang2026deep.md)); a water-treatment plant under attack; server failures; fraud.

**Input and output:**

- **given:** a series;
- **produce:** an **anomaly score** for each step, then a decision, normal or anomalous, by comparing the score with a **threshold**.

### Kinds of anomalies

The anomaly-detection survey we read distinguishes three kinds ([pang2021deep](../../../literature/pang2021deep.md)):

| Kind | What it is | Example |
|---|---|---|
| **Point** | a single value far from the rest | a sensor suddenly reading ten times its usual value |
| **Contextual** (conditional) | a value that is normal in general, but not at that moment, e.g. a "sudden temperature drop/increase in a particular temporal context" | heating at full power on a summer afternoon |
| **Collective** (group) | a stretch that is abnormal as a whole, even if each value alone looks normal | a machine's regular rhythm stopping for an hour |

![A point anomaly, a contextual anomaly (a peak-like value where a trough is due) and a collective one (the rhythm stops)](assets/anomaly-types.png)

### Labels: usually there are none

Anomalies are rare, and labeled anomaly data are hard or impossible to collect at scale ([pang2021deep](../../../literature/pang2021deep.md)). So most methods learn **what normal looks like**, then flag what doesn't fit:

| Setting | Training data | How common |
|---|---|---|
| **Unsupervised** | unlabeled data, assumed mostly normal | "by far the most commonly used" ([Anomaly detection][anomaly]) |
| **Semi-supervised** | data known to be normal | common: a model of "normal behavior" is built from it ([Anomaly detection][anomaly]) |
| **Supervised** | data labeled normal and abnormal | "rarely used", because labels are unavailable ([Anomaly detection][anomaly]) |

### How it's judged

By comparing the flagged steps with the true anomalies: **precision, recall and F1** once a threshold is set ([precision, recall and F1](../../evaluation/precision-recall-f1.md)); threshold-free measures such as [AUROC](../../evaluation/auroc.md) and [AUPRC](../../evaluation/auprc.md); and measures adapted to anomalies that last several steps ([point adjustment](../evaluation/point-adjustment.md), [VUS](../evaluation/vus.md)). F1 is the standard benchmark measure, "a balanced combination of precision and recall" ([wang2026deep](../../../literature/wang2026deep.md), p. 11).

**What makes it hard:**

- **The threshold decides everything.** A low threshold catches more anomalies but raises false alarms; a high one does the opposite. How it's chosen changes the results, and papers often don't say ([wu2023timesnet](../../../literature/wu2023timesnet.md), [wang2026deep](../../../literature/wang2026deep.md)).
- **False alarms:** methods "still often incur high false positives on real-world datasets" ([pang2021deep](../../../literature/pang2021deep.md), p. 4).
- **"Normal" can change over time.** If the series drifts, behavior that was abnormal may become normal, and the other way round ([drift in time series](../change-over-time/drift-in-time-series.md)).

## Key points

- **Given** a series, **produce** an anomaly score per step, then normal or abnormal via a **threshold**.
- Anomalies can be **point**, **contextual** or **collective**.
- Labels are usually missing: most methods learn what normal looks like.
- Judged by **precision, recall and F1**, or threshold-free measures.

## Sources

- [wang2026deep](../../../literature/wang2026deep.md): definition, examples, benchmark metric.
- [pang2021deep](../../../literature/pang2021deep.md): kinds of anomalies, labeling settings, false positives.
- [wu2023timesnet](../../../literature/wu2023timesnet.md): the unstated anomaly threshold.
- [Anomaly detection (Wikipedia)][anomaly]: general definition, labeling settings. Read on 2026-11-08.

[anomaly]: https://en.wikipedia.org/wiki/Anomaly_detection
