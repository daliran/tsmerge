# ilharco2023editing — Editing Models with Task Arithmetic

- **Status:** verified (2026-11-02): checked claim by claim against the paper by an independent agent (about 80 claims: 6 errors, mostly page references, and 6 omissions, all fixed)
- **Reference:** Ilharco, Ribeiro, Wortsman, Gururangan, Schmidt, Hajishirzi, Farhadi; ICLR 2023; arXiv 2212.04089 ([references.bib](../references.bib))
- **Version read:** arXiv v3, 31 pages: main text pp. 1–9, references pp. 10–17, appendix pp. 18–31
- **Read:** main text in full; appendix A (pp. 18–19), B.1–B.2 (p. 19), D–D.5 (pp. 24–27). Not read yet: B.3–B.8, C, D.6–D.7, E (the rest of pp. 19–31)
- **Code:** <https://github.com/mlfoundations/task_vectors> (p. 2, footnote 2)

## In one paragraph

The paper proposes editing a pre-trained model through **task vectors**: the difference between a model's weights after fine-tuning on a task and its pre-trained weights (p. 2). Arithmetic on these vectors steers the model: **negating** a task vector makes the model worse at that task with little change elsewhere (Section 3); **adding** task vectors produces one model that does well on several tasks, sometimes better than fine-tuning on one task (Section 4); and **analogies** ("A is to B as C is to D") improve a task with little or no data for it (Section 5). The experiments use CLIP image classifiers, GPT-2 and T5. Adding the task vectors of 8 image classification tasks gives one model with 91.2% average normalized accuracy, against 100% for 8 separate fine-tuned models (p. 5); adding pairs keeps 98.9% (p. 5).

## Problem

How to change ("edit") the behavior of a pre-trained model after pre-training — improve it on a downstream task, remove an unwanted behavior, add a capability — cheaply, without retraining, and without access to the training data (pp. 1–2).

**Setting:** models that can be fine-tuned without adding parameters ("open-ended" models: open-vocabulary image classifiers, text-to-text models) (p. 3); all task vectors come from the **same architecture** (p. 2, p. 8) and the **same pre-trained initialization** (p. 8).

## Method

**Task vector** (p. 2). For a task $t$ (a dataset and a fine-tuning loss), with pre-trained weights $\theta_{\text{pre}} \in \mathbb{R}^d$ and weights after fine-tuning on $t$, $\theta_{\text{ft}}^t \in \mathbb{R}^d$:

$$\tau_t = \theta_{\text{ft}}^t - \theta_{\text{pre}}$$

**Applying a task vector** (p. 2), element-wise, with a scaling coefficient $\lambda$:

$$\theta_{\text{new}} = \theta + \lambda \tau$$

With $\theta = \theta_{\text{pre}}$ and $\lambda = 1$, this gives back the fine-tuned model (p. 2).

**The three operations** (p. 3), each producing $\tau_{\text{new}}$, applied as $\theta_{\text{new}} = \theta + \lambda \tau_{\text{new}}$:

| Operation | Expression | Effect studied |
|---|---|---|
| Negation | $\tau_{\text{new}} = -\tau$ | worse on the target task, little change on control tasks (Section 3) |
| Addition | $\tau_{\text{new}} = \sum_i \tau_i$ | one multi-task model; sometimes better on a single task (Section 4) |
| Analogy | $\tau_{\text{new}} = \tau_C + (\tau_B - \tau_A)$ | better on task $D$ with little or no data for it (Section 5) |

**Choosing $\lambda$:**

- In general: on held-out validation sets (p. 2, p. 3).
- **Addition:** one single $\lambda$ for the sum of all task vectors, searched in $\{0, 0.05, 0.1, \dots, 1.0\}$. One coefficient per task vector "could improve performance", but exploring all combinations is impractical when the number of tasks isn't small, "due to the curse of dimensionality"; the authors suggest more sophisticated strategies, such as black-box optimization, as future work (p. 24).
- **Negation (image classification):** the largest $\lambda$ in $\{0, 0.05, \dots, 1.0\}$ whose model keeps at least 95% of the pre-trained model's accuracy on the control task (p. 19).
- **Analogies (domain generalization):** two separate coefficients, one for the sentiment task vector and one for both language-modeling task vectors (p. 6).

**Normalized accuracy** (p. 5): a task's accuracy divided by the accuracy of the model fine-tuned on that task; so using one fine-tuned model per task scores 1.0 on average.

**Relation to weight averaging and ensembles** (pp. 18–19):

- Adding task vectors is a linear combination of the pre-trained and fine-tuned models (p. 18); with $\lambda = 0.5$, adding two task vectors equals the uniform average of the two fine-tuned models (p. 19, footnote 5):

  $$\theta_{\text{pre}} + 0.5(\tau_1 + \tau_2) = 0.5(\theta_1 + \theta_2)$$

- Linearly combining weights *approximates* ensembling the models' outputs; the approximation holds where the loss is locally well approximated by a linear expansion (the NTK regime), and when it holds exactly, weight averaging and ensembles are exactly equivalent (pp. 18–19, citing prior work).
- Empirically, for two task vectors, the accuracy of the added model closely follows that of the ensemble of the two fine-tuned models, slightly lower on average, with a Pearson correlation of 0.99 (p. 19, Figure 8, p. 18).

## Experimental setup

**Image classification (Sections 3.1, 4.1):**

- Models: CLIP ViT-B/32, ViT-B/16, ViT-L/14 (Table 1, p. 4).
- Tasks: Cars, DTD, EuroSAT, GTSRB, MNIST, RESISC45, SUN397, SVHN (8 tasks) (p. 3); control task for negation: ImageNet (p. 3).
- Fine-tuning (p. 19, B.1): 2000 iterations, batch size 128, learning rate 1e-5, cosine annealing with 200 warm-up steps, AdamW with weight decay 0.1; the classification layer (built from CLIP's text encoder) is **frozen**, so no parameters are added.
- Negation baselines (p. 19, B.2): fine-tuning with gradient ascent (minimizing $-\ell$); and a random vector with the same norm as the task vector, layer by layer: $\tau_{\text{scaled}}^{(L)} = \tau_{\text{rand}}^{(L)} \, \|\tau^{(L)}\| / \|\tau_{\text{rand}}^{(L)}\|$, $\tau_{\text{rand}}^{(L)} \sim \mathcal{N}(0, I)$, the per-layer vectors then concatenated into one vector used like a task vector.
- Multi-task baseline (p. 25, D.2): one model fine-tuned jointly on the 8 tasks, same hyperparameters, frozen heads.

**Text:**

- Toxicity (Section 3.2, pp. 3–4): GPT-2 (small, medium, large); task vectors from fine-tuning on Civil Comments samples with toxicity score above 0.8; the "fine-tuned on non-toxic" baseline uses samples with toxicity below 0.2; toxicity measured with Detoxify on 1000 generations; control: perplexity on WikiText-103.
- Addition for single tasks (Section 4.2, p. 5): T5-base on 4 GLUE tasks; 427 candidate checkpoints from the Hugging Face Hub; best checkpoint and $\lambda$ chosen on held-out validation data.
- Analogies (Section 5, p. 6): T5 small, base, large; sentiment on Yelp and Amazon; $\hat{\tau}_{\text{yelp;sent}} = \tau_{\text{amazon;sent}} + (\tau_{\text{yelp;lm}} - \tau_{\text{amazon;lm}})$, where the "lm" vectors come from (unsupervised) language modeling on each dataset's inputs.

## Results

**Negation, image classification** (Table 1, p. 4). Average accuracy (%) on the 8 target tasks (lower is better) and on ImageNet (control, higher is better):

| Method | ViT-B/32 target | ViT-B/32 control | ViT-B/16 target | ViT-B/16 control | ViT-L/14 target | ViT-L/14 control |
|---|---|---|---|---|---|---|
| Pre-trained | 48.3 | 63.4 | 55.2 | 68.3 | 64.8 | 75.5 |
| Fine-tuned | 90.2 | 48.2 | 92.5 | 58.3 | 94.0 | 72.6 |
| Gradient ascent | 2.73 | 0.25 | 1.93 | 0.68 | 3.93 | 16.3 |
| Random vector | 45.7 | 61.5 | 53.1 | 66.0 | 60.9 | 72.9 |
| Negative task vector | 24.0 | 60.9 | 21.3 | 65.4 | 19.0 | 72.9 |

For ViT-L/14, negation lowers target accuracy by 45.8 points (64.8 → 19.0) with little change on the control task (p. 3, p. 4).

**Negation, toxicity, GPT-2 Large** (Table 2, p. 4):

| Method | % toxic generations ↓ | Avg. toxicity score ↓ | WikiText-103 perplexity ↓ |
|---|---|---|---|
| Pre-trained | 4.8 | 0.06 | 16.4 |
| Fine-tuned | 57 | 0.56 | 16.6 |
| Gradient ascent | 0.0 | 0.45 | > 10¹⁰ |
| Fine-tuned on non-toxic | 1.8 | 0.03 | 17.2 |
| Random vector | 4.8 | 0.06 | 16.4 |
| Negative task vector | 0.8 | 0.01 | 16.9 |

**Addition, image classification** (Section 4.1, p. 5; Figures 2–3):

- Adding **pairs** of task vectors: one model competitive with the two fine-tuned models, **98.9%** normalized accuracy on average (p. 5).
- Adding the task vectors of **all subsets** of the 8 tasks ($2^8$): accuracy averaged over all 8 tasks increases with the number of vectors added; with all 8, the best model reaches **91.2%** (p. 5, Figure 3).
- Averaged only over the tasks whose vectors were added, the gap to separate fine-tuned models **grows with the number of tasks** (p. 26, D.4, Figure 16).
- The best multi-task model is often not the one using all available task vectors (p. 25).
- **Joint multi-task fine-tuning** on the 8 tasks reaches **0.994** normalized accuracy, against **0.912** for the best task-vector model (p. 25, D.2). The authors' counterpoint: multi-task training "is less modular", "requiring a new fine-tuning round every time a new task is added", while task vectors combine "without any additional training and without the need to store or transfer the data used to create them" (p. 25).
- **Choosing which vectors to add:** since adding and evaluating is cheap, practitioners "could try out many subsets of task vectors", or use a greedy algorithm to discard vectors that don't improve accuracy (p. 25); likewise, task vectors that bring no improvement on validation data can simply be discarded (p. 25, D.1).
- **Random seeds:** 5 MNIST and 5 EuroSAT fine-tunings, all 25 pairs added: little impact on the edited models' accuracy (p. 25, D.1, Figure 14).

**Scaling coefficient** (p. 25–26, D.3, Figure 15):

- The optimal $\lambda$ varies across experiments, so it needs tuning case by case (p. 25).
- Values from 0.3 to 0.5 are close to optimal in many cases (p. 26).
- The optimal $\lambda$ tends to decrease as more task vectors are added (Figure 15 left, p. 26; **our reading** of the plot: from about 0.4 for 2 tasks to about 0.3 for 8).
- Accuracy as a function of $\lambda$ drops faster beyond its optimum the more task vectors are added (Figure 15 right, p. 26): with many tasks, a wrong $\lambda$ costs more.

**Adding an ImageNet task vector** (D.5, pp. 26–27; Figure 17, p. 27). An ImageNet task vector, fine-tuned for 4 epochs (about 40 thousand steps), added to each of the 8 task vectors in turn. Accuracy (%), as printed on the bars:

| Other task | ImageNet: task vectors (fine-tuned 85.5, pre-trained 75.5) | Other task: pre-trained / task vectors / fine-tuned |
|---|---|---|
| Cars | 85.0 | 77.8 / 88.6 / 92.8 |
| DTD | 85.0 | 55.4 / 79.9 / 83.7 |
| EuroSAT | 84.8 | 60.3 / 98.7 / 99.2 |
| GTSRB | 85.3 | 50.6 / 98.7 / 99.3 |
| MNIST | 85.3 | 76.4 / 99.7 / 99.8 |
| RESISC45 | 85.1 | 71.0 / 96.2 / 96.9 |
| SUN397 | 84.9 | 68.3 / 78.8 / 82.4 |
| SVHN | 85.1 | 58.6 / 97.6 / 98.0 |

In most experiments, the added model "is competitive with the fine-tuned models on their respective datasets" (p. 26).

**Addition, text** (Table 3, p. 6). Accuracy of fine-tuned T5-base models, with and without an added task vector from the Hugging Face Hub:

| Method | MRPC | RTE | CoLA | SST-2 | Average |
|---|---|---|---|---|---|
| Zero-shot | 74.8 | 52.7 | 8.29 | 92.7 | 57.1 |
| Fine-tuned | 88.5 | 77.3 | 52.3 | 94.5 | 78.1 |
| Fine-tuned + task vectors | 89.3 (+0.8) | 77.5 (+0.2) | 53.0 (+0.7) | 94.7 (+0.2) | 78.6 (+0.5) |

**Analogies, domain generalization** (Table 4, p. 6). Sentiment accuracy, without labeled data from the target:

| Method | Yelp T5-small | Yelp T5-base | Yelp T5-large | Amazon T5-small | Amazon T5-base | Amazon T5-large |
|---|---|---|---|---|---|---|
| Fine-tuned on auxiliary | 88.6 | 92.3 | 95.0 | 87.9 | 90.8 | 94.8 |
| Task analogies | 89.9 | 93.0 | 95.1 | 89.0 | 92.7 | 95.2 |
| Fine-tuned on target | 91.1 | 93.4 | 95.5 | 90.2 | 93.2 | 95.5 |

**Analogies, subpopulations** (p. 7, Figure 4): with no data from the target subpopulation, task vectors improve accuracy by 3.4 points on average over the pre-trained model; the gain is roughly that of collecting about a hundred labeled samples.

**Analyses** (Section 6, pp. 7–8):

- **Task vectors are close to orthogonal:** cosine similarities between the CLIP task vectors of 9 tasks (the 8 above plus KITTI) are mostly 0.01–0.06; the largest is 0.18, between MNIST and SVHN, two digit-recognition tasks (Figure 5, p. 7). The authors *speculate* that this near-orthogonality is what lets vectors be added with little interference (p. 7).
- **Learning rate:** larger learning rates hurt the added model more than they hurt individual fine-tuned models; the authors recommend caution with large learning rates when building task vectors (Figure 6, p. 8).
- **During fine-tuning,** intermediate task vectors quickly align with the final one, and adding intermediate vectors from two tasks reaches high accuracy after a few hundred steps (Figure 7, p. 8).

## Assumptions and limitations

- **Same architecture and same pre-trained initialization** for all task vectors: the operations are element-wise on weights (p. 8, stated by the authors).
- **No new parameters during fine-tuning:** the classification heads are frozen; merging models that add new heads is left to future work (p. 3).
- **One scaling coefficient** for the sum of task vectors; per-vector coefficients aren't explored (p. 24).
- **Interference grows with the number of tasks:** the added model falls further behind separate models, and further behind joint multi-task training (0.912 vs 0.994 on 8 tasks) (p. 25, p. 26).
- **The near-orthogonality explanation is offered as speculation** ("speculate", p. 7).
- $\lambda$ is chosen on held-out validation data (p. 2), while the paper presents task arithmetic as working "all without requiring access to data or additional training" (p. 2).
- **Our reading:** the near-orthogonality explanation isn't tested causally in the paper; choosing $\lambda$ needs validation data from the tasks involved, so the method isn't data-free at selection time; and the domains studied are images and text only (classification, generation, sentiment), with nothing on time series, regression or anomaly detection.

## Relevance to this thesis

**Our reading:**

- **The baseline definition** of task arithmetic for the thesis: task vector $\tau_t = \theta_{\text{ft}}^t - \theta_{\text{pre}}$, merged model $\theta_{\text{pre}} + \lambda \sum_t \tau_t$ with one $\lambda$ chosen on validation data. Our experiments should reproduce this exact form before testing variants.
- **The direct comparison we study already appears here:** on 8 image tasks, joint multi-task training (0.994) beats added task vectors (0.912) (p. 25). Whether the gap holds, grows or shrinks for time-series anomaly detection and forecasting is open.
- **What to measure, following the paper:** normalized accuracy (per-task, relative to its own fine-tuned model), the optimal $\lambda$ as a function of the number of tasks, and the cosine similarity between task vectors (the paper's proposed explanation for low interference).
- **Settings that may not carry over:** the paper's tasks are different datasets from one strong pre-trained model (CLIP); our tasks may be successive periods of the same signal, where task vectors could be far from orthogonal.
- **Learning-rate caution** (p. 8) matters for how we fine-tune before merging.

## Quotes worth keeping

> "A task vector specifies a direction in the weight space of a pre-trained model, such that movement in that direction improves performance on the task." (p. 1)

> "Note that adding a single task vector to a pre-trained model with λ = 1 results in the model fine-tuned on that task." (p. 2)

> "We observe that vectors from different tasks are typically close to orthogonal, and speculate that this enables the combination of task vectors via addition with minimal interference." (p. 7)

> "Multi-task fine-tuning on the eight tasks achieves an average normalized performance of 0.994, compared to the best result obtained with task vectors, 0.912" (p. 25)

> "Task vectors are restricted to models with the same architecture, since they depend on element-wise operations on model weights." (p. 8)
