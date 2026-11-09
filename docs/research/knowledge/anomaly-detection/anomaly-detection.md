# Anomaly detection

**In one sentence:** anomaly detection finds the data that don't behave like the rest, usually by learning what normal looks like and scoring how far each new item is from it.

- **Builds on:** nothing: a starting point.
- **Used by:** [Kinds of anomalies](kinds-of-anomalies.md), [Methods](methods.md), [Anomaly detection in time series](../time-series/tasks/anomaly-detection.md).

## What it is

Anomaly detection, "a.k.a. outlier detection or novelty detection", is "the process of detecting data instances that significantly deviate from the majority of data instances" ([pang2021deep](../../literature/pang2021deep.md), p. 2).

It "finds application in many domains including cybersecurity, medicine, machine vision, statistics, neuroscience, law enforcement and financial fraud" ([Anomaly detection][anomaly]).

What an anomaly means depends on the domain: it "may represent a measurement or recording error, a change in the process that generated the data, an unusual but valid observation, or an event of interest such as fraud, equipment failure, or a security intrusion" ([Anomaly detection][anomaly]). For example:

- **payments:** a fraudulent transaction;
- **images:** a defect on a product photographed on a production line;
- **computer networks:** an intrusion;
- **medicine:** a sign of disease in a scan or a recording;
- **machines:** a sensor reading that announces a failure.

The data can be tables, images, video, text, graphs or time series ([kinds of anomalies](kinds-of-anomalies.md#examples-across-domains)).

## How it works, in general

Most methods do two things:

1. **Score:** give each item an **anomaly score**; the higher the score, the more anomalous the item ([pang2021deep](../../literature/pang2021deep.md), p. 7).
2. **Decide:** compare the score with a **threshold**: above it, the item is flagged as an anomaly.

The score is where methods differ ([methods](methods.md)). The threshold trades missed anomalies against false alarms ([precision, recall and F1](../evaluation/precision-recall-f1.md#the-threshold)).

## Why it's hard

The survey lists several difficulties shared by all methods ([pang2021deep](../../literature/pang2021deep.md), pp. 3–4):

- **Anomalies are unknown** until they actually happen.
- **They vary:** one kind of anomaly can look completely different from another ([kinds of anomalies](kinds-of-anomalies.md)).
- **They are rare,** so labeled examples are hard or impossible to collect in large numbers.
- **Missing one usually costs more** than raising a false alarm.

## Learning settings: labels are usually missing

Because labeled anomalies are rare, most methods learn **what normal looks like**, then flag what doesn't fit.

The usual settings, as Wikipedia describes them ([Anomaly detection][anomaly]):

| Setting | Training data | How often it's used |
|---|---|---|
| **Unsupervised** | unlabeled data | "by far the most commonly used" |
| **Semi-supervised** | some labeled data; more often than not, data known to be normal, from which a model of "normal behavior" is built | not stated |
| **Supervised** | data labeled normal and abnormal | "rarely used", because labels are unavailable |

The survey adds a fourth, **weakly supervised**: some anomaly labels, but partial, inexact or inaccurate ([pang2021deep](../../literature/pang2021deep.md), p. 5).

**The names clash.** Training on normal data only is called "semi-supervised" in the survey, which notes that it is sometimes called unsupervised elsewhere ([pang2021deep](../../literature/pang2021deep.md), p. 5, footnote 1). When reading a paper, check which data it trained on, not only the name it uses.

## Key points

- Anomaly detection finds items that **deviate from the majority**; it is also called outlier or novelty detection.
- Most methods give each item an **anomaly score**, then flag it with a **threshold**.
- Anomalies are **unknown in advance, varied and rare**, so labels are usually missing.
- Most methods learn **what normal looks like**; the names of the learning settings differ between communities.

## Sources

- [pang2021deep](../../literature/pang2021deep.md): definition, scores, difficulties, weakly supervised setting, the naming clash.
- [Anomaly detection (Wikipedia)][anomaly]: application domains, what an anomaly can mean, the learning settings and how often each is used. Read on 2026-11-09.

[anomaly]: https://en.wikipedia.org/wiki/Anomaly_detection
