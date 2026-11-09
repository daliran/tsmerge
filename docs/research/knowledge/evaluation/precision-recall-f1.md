# Precision, recall and F1

**In one sentence:** when a model makes yes-or-no calls, precision says how many of its "yes" were right, recall how many of the real "yes" it found, and F1 combines the two.

- **Builds on:** nothing: a starting point.
- **Used by:**
  - [Anomaly detection](../time-series/tasks/anomaly-detection.md)
  - [Classification](../time-series/tasks/classification.md)
  - [AUROC](auroc.md)
  - [AUPRC](auprc.md)
  - [Comparing results](comparing-results.md)
  - [Point adjustment](../time-series/evaluation/point-adjustment.md)

## Counting hits and misses

Compare each call with the truth, and count four cases ([Precision and recall][precision]):

- **true positives** ($tp$): "yes" calls on real positives;
- **false positives** ($fp$): "yes" calls on real negatives;
- **false negatives** ($fn$): "no" calls on real positives;
- **true negatives** ($tn$): "no" calls on real negatives.

| Measure | Formula | Question it answers |
|---|---|---|
| **Precision** | $\dfrac{tp}{tp + fp}$ | of the cases called positive, how many were real positives? |
| **Recall** | $\dfrac{tp}{tp + fn}$ | of the real positives, how many were called positive? |
| **F1** | $\dfrac{2 \cdot \text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}$ | both at once: their harmonic mean |

In anomaly detection, for example, the positives are the anomalous steps: precision asks how many of the flagged steps were real anomalies, recall how many of the real anomalies were flagged.

## Accuracy

**Accuracy** is the share of all calls, "yes" and "no", that were right ([Precision and recall][precision]):

$$\text{accuracy} = \frac{tp + tn}{tp + tn + fp + fn}$$

It's the only one of these measures that counts true negatives. The TSLib benchmark reports accuracy for [classification](../time-series/tasks/classification.md) and F1 for anomaly detection ([wang2026deep](../../literature/wang2026deep.md), p. 11); its overview figure lists both measures for both tasks (Figure 8, p. 10).

When one answer is rare, as anomalies are, accuracy is misleading: always answering "normal" scores high while finding nothing. Precision and recall look only at the rare class, which is why anomaly detection uses them.

## The threshold

A model usually gives a score, not a call; a **threshold** turns scores into calls. Lowering it raises recall (or leaves it unchanged) and usually lowers precision; raising it does the opposite ([Precision and recall][precision]: "usually precision will decrease as the recall increases").

So these measures describe one threshold, not the model.

Threshold-free alternatives: [AUROC](auroc.md), [AUPRC](auprc.md).

## Key points

- **Precision** $= tp/(tp+fp)$: of the calls made, how many were right.
- **Recall** $= tp/(tp+fn)$: of the real cases, how many were found.
- **F1**: their harmonic mean. **Accuracy** $= (tp+tn)/(tp+tn+fp+fn)$: the share of all calls that were right, misleading when one class is rare.
- All depend on the **threshold** that turns scores into calls.

## Sources

- [Precision and recall (Wikipedia)][precision]: definitions, the accuracy formula, and the precision-recall trade-off. Read on 2026-11-09.
- [wang2026deep](../../literature/wang2026deep.md): the TSLib benchmark's measures, F1 for anomaly detection and accuracy for classification (p. 11).

[precision]: https://en.wikipedia.org/wiki/Precision_and_recall
