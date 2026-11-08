# Classification

**In one sentence:** classification gives a whole series one label out of a fixed set.

- **Builds on:** [Tasks](tasks.md).
- **Used by:** [Precision, recall and F1](../../evaluation/precision-recall-f1.md).

## The task

**Purpose:** classification "assigns a label or category to a given time series based on its characteristics" ([wang2026deep](../../../literature/wang2026deep.md), p. 3).

**Examples:** heartbeat diagnosis and action recognition ([wang2026deep](../../../literature/wang2026deep.md)), e.g. telling a normal heartbeat recording from an abnormal one, or recognizing walking or running from a phone's motion sensors.

**Input and output:**

- **given:** a whole series (or a segment);
- **produce:** one label out of a fixed set.

**How it's judged:** by **accuracy**, the share of series labeled correctly ([precision, recall and F1](../../evaluation/precision-recall-f1.md#accuracy); [wang2026deep](../../../literature/wang2026deep.md), p. 11).

**What makes it hard:** the clues can be anywhere in the series, and two classes can differ only in subtle details.

**Not the same as [anomaly detection](anomaly-detection.md):** classification needs examples of every class, and gives one label to a whole series; anomaly detection usually has no anomaly examples, and works step by step.

## Key points

- **Given** a whole series (or a segment), **produce** one label.
- Judged by **accuracy**, the share of series labeled correctly.
- Unlike anomaly detection, it needs examples of every class.

## Sources

- [wang2026deep](../../../literature/wang2026deep.md): definition, examples, benchmark metric.
