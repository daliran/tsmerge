# Precision, recall and F1

**In one sentence:** when a model makes yes-or-no calls, precision says how many of its "yes" were right, recall how many of the real "yes" it found, and F1 combines the two.

- **Builds on:** nothing: a starting point.
- **Used by:** [Anomaly detection](../time-series/tasks/anomaly-detection.md), [Classification](../time-series/tasks/classification.md), [AUROC](auroc.md), [AUPRC](auprc.md), [Point adjustment](../time-series/evaluation/point-adjustment.md).

## Counting hits and misses

Compare each call with the truth, and count true positives ($tp$), false positives ($fp$) and false negatives ($fn$) ([Precision and recall][precision]):

| Measure | Formula | Question it answers |
|---|---|---|
| **Precision** | $\dfrac{tp}{tp + fp}$ | of the steps flagged, how many were real anomalies? |
| **Recall** | $\dfrac{tp}{tp + fn}$ | of the real anomalies, how many were flagged? |
| **F1** | $\dfrac{2 \cdot \text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}$ | both at once: their harmonic mean |

## Accuracy

**Accuracy** is the share of all calls, "yes" and "no", that were right. It's the standard measure for [classification](../time-series/tasks/classification.md) benchmarks ([wang2026deep](../../literature/wang2026deep.md), p. 11). When one answer is rare, as anomalies are, accuracy is misleading: always answering "normal" scores high while finding nothing. Precision and recall look only at the rare class, which is why anomaly detection uses them.

## The threshold

A model usually gives a score, not a call; a **threshold** turns scores into calls. Lowering it raises recall and lowers precision, and the other way round, so these measures describe one threshold, not the model. Threshold-free alternatives: [AUROC](auroc.md), [AUPRC](auprc.md).

## Key points

- **Precision** $= tp/(tp+fp)$: of the calls made, how many were right.
- **Recall** $= tp/(tp+fn)$: of the real cases, how many were found.
- **F1**: their harmonic mean. **Accuracy**: the share of all calls that were right, misleading when one class is rare.
- All depend on the **threshold** that turns scores into calls.

## Sources

- [Precision and recall (Wikipedia)][precision]: definitions. Read on 2026-11-08.
- [wang2026deep](../../literature/wang2026deep.md): F1 and accuracy as the standard benchmark measures.

[precision]: https://en.wikipedia.org/wiki/Precision_and_recall
