# Methods

**In one sentence:** deep anomaly-detection methods fall into three families, depending on how closely the network that learns the data is tied to the anomaly score.

- **Builds on:** [Anomaly detection](anomaly-detection.md), [Kinds of anomalies](kinds-of-anomalies.md).
- **Used by:** [Anomaly detection in time series](../time-series/tasks/anomaly-detection.md).

## Three families

The survey organizes deep methods into three families, from loosest to tightest link between learning and scoring ([pang2021deep](../../literature/pang2021deep.md), pp. 7–8):

| Family | The idea | Typical techniques |
|---|---|---|
| **Feature extraction** | a network turns the data into features; a separate, classic method scores them | a network used only to produce features |
| **Learning what normal looks like** | the network learns the normal data; an item it fits badly is anomalous | autoencoders, generative adversarial networks, prediction, self-supervised tasks; or distance-, one-class- and clustering-based measures |
| **End-to-end scoring** | the network outputs the anomaly score directly | ranking models, prior-driven models, softmax likelihood, end-to-end one-class classification |

## The middle family, in more detail

Its techniques work on many kinds of data. Two examples:

- **images:** an autoencoder trained on photos of intact products rebuilds them well, but rebuilds a scratch or a dent poorly, so the defect stands out;
- **time series:** the TimesNet benchmark scores anomalies by reconstruction error ([wu2023timesnet](../../literature/wu2023timesnet.md), p. 8), and prediction relies on the order of the data ([pang2021deep](../../literature/pang2021deep.md), p. 14).

The survey splits the family in two ([pang2021deep](../../literature/pang2021deep.md), p. 8):

- **Generic normality learning:** the network is trained on a general task, and its failure becomes the score. Two common examples:
  - **reconstruction:** an autoencoder compresses the input and rebuilds it; normal data rebuild well, anomalies badly, so the reconstruction error is the score;
  - **prediction:** a model predicts the next values from the previous ones; normal data follow the usual order and are predicted well, so a large prediction error is the score.
- **Measure-dependent learning:** the network is trained so that a classic anomaly measure works well in its feature space, e.g. distance to the nearest items (anomalies lie far from their neighbors), or how well an item fits one compact model of all the normal data (one-class).

## Key points

- **Feature extraction:** learn features, score them separately.
- **Learning what normal looks like:** learn the normal data; badly fitted items are anomalous (e.g. high reconstruction or prediction error).
- **End-to-end scoring:** the network outputs the score itself.
- The families differ in how tightly learning and scoring are tied together.

## Sources

- [pang2021deep](../../literature/pang2021deep.md): the taxonomy of deep anomaly-detection methods (Section 3, Figures 1 and 2, pp. 7–8), and the families' descriptions (Sections 4–6).
- [wu2023timesnet](../../literature/wu2023timesnet.md): reconstruction error as the anomaly score.
