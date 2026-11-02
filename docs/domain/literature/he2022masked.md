# he2022masked — Masked Autoencoders Are Scalable Vision Learners

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 230 claims, every table cell correct: 5 minor misstatements or over-extensions, fixed)
- **Reference:** He, Chen, Xie, Li, Dollár, Girshick; CVPR 2022; arXiv 2111.06377 ([references.bib](../references.bib))
- **Version read:** arXiv v3 (19 Dec 2021, p. 1 margin), 14 pages: main text pp. 1–9 (Broader impacts on p. 9), references pp. 9–10, appendix pp. 11–14
- **Read:** everything: main text Sections 1–6 and Broader impacts (pp. 1–9), references (pp. 9–10), appendix A.1–A.5, B, C (pp. 11–12), Figures 10–11 (pp. 13–14)
- **Code:** no link in the paper; it says "We will release code along with the specific configurations" (p. 12, A.3), about the COCO detection setup

## In one paragraph

The paper proposes the **masked autoencoder (MAE)** for self-supervised pre-training of Vision Transformers: mask a large random subset of image patches and reconstruct the missing pixels (p. 1). Two designs make it work: an **asymmetric encoder-decoder**, where the encoder sees only the visible patches (no mask tokens) and a lightweight decoder reconstructs the image from the encoded patches plus mask tokens; and a **high masking ratio**, e.g. 75%, which makes the task nontrivial (p. 1). Together they speed up pre-training by 3× or more and improve accuracy (p. 1). A vanilla ViT-Huge pre-trained with MAE on ImageNet-1K only reaches **87.8%** top-1 when fine-tuned at 448 size (p. 1, Table 3, p. 7), and transfer to detection and segmentation beats supervised pre-training, and on classification (iNat, Places) it beats the previous best results, for Places205 only at ViT-H₄₄₈ (Section 5, p. 8).

## Problem

Why masked autoencoding, so successful in NLP (BERT), lags behind in vision, and how to make it work (p. 1). The paper gives three reasons (pp. 1–2):

- **(i) Architectures differed:** convolutional networks don't easily integrate mask tokens or positional embeddings; ViT removed this gap (p. 1).
- **(ii) Information density differs:** language is "highly semantic and information-dense", while images have "heavy spatial redundancy", so a missing patch can be recovered from its neighbors "with little high-level understanding" (pp. 1–2). The answer is masking a *very high* portion of random patches (p. 2).
- **(iii) The decoder's role differs:** in vision it reconstructs pixels, of a lower semantic level than words, so the decoder design "plays a key role in determining the semantic level of the learned latent representations" (p. 2).

**Setting:** self-supervised pre-training on the ImageNet-1K (IN1K) training set, then supervised evaluation by end-to-end fine-tuning or linear probing; top-1 validation accuracy of a single 224×224 crop (p. 4).

## Method

**Patches and masking** (p. 3). Following ViT, the image is divided into regular non-overlapping patches; a subset is sampled and the rest masked (removed). Sampling is random, **without replacement, from a uniform distribution** ("random sampling"). A high masking ratio "largely eliminates redundancy"; the uniform distribution "prevents a potential center bias" (p. 3).

**Encoder** (p. 3). A ViT applied **only to visible, unmasked patches**: linear patch embedding plus positional embeddings, then Transformer blocks. It processes a small subset (e.g. 25%) of the patches; "Masked patches are removed; no mask tokens are used" (p. 3).

**Decoder** (pp. 3–4).

- Input: the full set of tokens, i.e. (i) the encoded visible patches and (ii) **mask tokens**. Each mask token is "a shared, learned vector that indicates the presence of a missing patch to be predicted" (pp. 3–4).
- Positional embeddings are added to all tokens of this full set; without them, mask tokens would not know their location (p. 4).
- Another series of Transformer blocks (p. 4).
- Used **only during pre-training**; after it, the decoder is discarded and the encoder is applied to uncorrupted images (full sets of patches) (p. 1, Figure 1; p. 4).
- Its design is independent of the encoder: narrower and shallower; the default has "<10% computation per token vs. the encoder" (p. 4). Default: **8 blocks, width 512**; "9% FLOPs per token vs. ViT-L (24 blocks, 1024-d)" (p. 5).

**Reconstruction target and loss** (p. 4).

- The decoder predicts the **pixel values** of each masked patch; each output element is a vector of pixel values for one patch; the last decoder layer is a linear projection with as many outputs as pixels in a patch; the output is reshaped into an image (p. 4).
- The loss is the **mean squared error (MSE)** between reconstructed and original images in pixel space, computed **only on masked patches**, similar to BERT (p. 4).
- Why only masked patches: "purely result-driven: computing the loss on all pixels leads to a slight decrease in accuracy (e.g., ∼0.5%)" (p. 4, footnote 1).
- **Normalized-pixel variant:** the target is each masked patch normalized by the mean and standard deviation of all its pixels; it "improves representation quality" (p. 4).

The paper gives no equation. **Our reading**, a formalization of the description above: with $M$ the set of masked patches, $x_i \in \mathbb{R}^{P}$ the $P$ pixel values of patch $i$ and $\hat{x}_i$ its prediction,

$$\mathcal{L} = \frac{1}{|M|\,P} \sum_{i \in M} \lVert \hat{x}_i - \tilde{x}_i \rVert_2^2, \qquad \tilde{x}_i = x_i \ \text{(default)} \quad \text{or} \quad \tilde{x}_i = \frac{x_i - \mu_i}{\sigma_i} \ \text{(normalized)},$$

where $\mu_i, \sigma_i$ are the mean and standard deviation of the pixels of patch $i$. The exact averaging (per patch, per pixel, over the batch) and any epsilon in $\sigma_i$ are not stated in the paper.

**Implementation** (p. 4): no sparse operations needed.

1. Make a token for every patch (linear projection plus positional embedding).
2. **Randomly shuffle** the token list and **remove the last portion**, by the masking ratio; this equals sampling without replacement.
3. Encode the remaining tokens.
4. Append mask tokens to the encoded patches and **unshuffle** the full list to align tokens with their targets.
5. Apply the decoder to the full list (with positional embeddings added).

**Architecture details** (p. 11, A.1):

- Standard ViT: Transformer blocks of multi-head self-attention and MLP, both with LayerNorm; the encoder ends with LN.
- A linear projection after the encoder matches the decoder's width.
- Positional embeddings: the **sine-cosine** version, added to both encoder and decoder inputs; no relative position or layer scaling.
- An auxiliary **dummy token** appended to the encoder input in pre-training, used as the class token for linear probing and fine-tuning; MAE "works similarly well without this token (with average pooling)".

## Experimental setup

**Models:** ViT-B/16, ViT-L/16, ViT-H/14 (Table 3, p. 7); ViT-L/16 is the ablation backbone (p. 4). Params: ViT-B 86 M, ViT-L 304 M, ViT-H 632 M (Table 12, p. 12).

**Pre-training** (Table 8, p. 11):

| Config | Value |
|---|---|
| optimizer | AdamW |
| base learning rate | 1.5e-4 |
| weight decay | 0.05 |
| optimizer momentum | $\beta_1, \beta_2 = 0.9, 0.95$ |
| batch size | 4096 |
| learning rate schedule | cosine decay |
| warmup epochs | 40 |
| augmentation | RandomResizedCrop |

- No color jittering, drop path or gradient clipping; xavier_uniform initialization of all Transformer blocks (p. 11).
- Linear lr scaling: $lr = base\_lr \times \text{batchsize} / 256$ (p. 11).
- Ablation default: decoder depth 8, width 512, unnormalized pixels, random resized cropping, masking ratio 75%, **800 epochs** (Table 1 caption, p. 5). Final models in Table 3: normalized pixels, **1600 epochs** (p. 7).

**End-to-end fine-tuning** (Table 9, p. 11), with layer-wise lr decay:

| Config | Value |
|---|---|
| optimizer | AdamW |
| base learning rate | 1e-3 |
| weight decay | 0.05 |
| optimizer momentum | $\beta_1, \beta_2 = 0.9, 0.999$ |
| layer-wise lr decay | 0.75 |
| batch size | 1024 |
| learning rate schedule | cosine decay |
| warmup epochs | 5 |
| training epochs | 100 (B), 50 (L/H) |
| augmentation | RandAug (9, 0.5) |
| label smoothing | 0.1 |
| mixup | 0.8 |
| cutmix | 1.0 |
| drop path | 0.1 (B/L) 0.2 (H) |

**Linear probing** (Table 10, p. 11):

| Config | Value |
|---|---|
| optimizer | LARS |
| base learning rate | 0.1 |
| weight decay | 0 |
| optimizer momentum | 0.9 |
| batch size | 16384 |
| learning rate schedule | cosine decay |
| warmup epochs | 10 |
| training epochs | 90 |
| augmentation | RandomResizedCrop |

- No mixup, cutmix, drop path or color jittering; regularization "is in general harmful for linear probing" (p. 11).
- An extra **BatchNorm without affine transformation** before the linear classifier normalizes the features; it can be absorbed into the classifier after training (p. 11). SGD with batch 4096 "works similarly" to LARS (Table 10 caption, p. 11).

**Partial fine-tuning** (p. 11): as Table 9, with fine-tuning epochs in $\{50, 100, 200\}$, the best one per number of tuned blocks.

**Supervised from-scratch baseline** (A.2, pp. 11–12, Table 11): AdamW, base lr 1e-4, weight decay 0.3, $\beta_1, \beta_2 = 0.9, 0.95$, batch 4096, cosine decay, 20 warmup epochs, 300 (B) / 200 (L/H) epochs, RandAug (9, 0.5), label smoothing 0.1, mixup 0.8, cutmix 1.0, drop path 0.1 (B) / 0.2 (L/H), EMA 0.9999. Result: 82.6% ViT-L (81.5% w/o EMA), 83.1% ViT-H (80.9% w/o EMA), 82.3% ViT-B (82.1% w/o EMA) (p. 12).

**Transfer** (pp. 8, 12):

- COCO detection and segmentation: Mask R-CNN, ViT adapted to FPN by splitting its blocks into 4 subsets and resampling to strides 4, 8, 16, 32; hyperparameters (lr, weight decay, drop path, epochs) searched for every entry, competitors included (A.3, p. 12).
- ADE20K: UperNet, 100 epochs, batch size 16, lr searched per entry; relative position bias turned on only during transfer, initialized as zero (A.4, p. 12).
- iNaturalist and Places: Table 9 setting, lr and epochs adjusted per dataset (A.5, p. 12).

## Results

**Baseline ViT-L/16 on IN1K** (p. 4): scratch, original ViT paper 76.5; scratch, our impl. 82.5; baseline MAE (fine-tuned) **84.9**. MAE fine-tuning is 50 epochs vs. 200 from scratch (p. 4).

**Masking ratio** (Figure 5, p. 4). IN1K accuracy (%), ViT-L, values as printed on the plot:

| Masking ratio (%) | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 75 | 80 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|
| Fine-tuning | 83.2 | 83.4 | 83.4 | 84.7 | 84.9 | 85.0 | 84.9 | 84.9 | 84.5 | 83.0 |
| Linear probing | 54.6 | 58.9 | 61.7 | 67.0 | 69.9 | 71.8 | 73.2 | 73.5 | 71.8 | 66.1 |

- 75% "is good for both linear probing and fine-tuning", against BERT's typical 15% and 20%–50% in related vision works (p. 4).
- Linear probing rises steadily to the sweet spot, a gap of up to ∼20% (54.6% vs. 73.5%); fine-tuning is less sensitive, 40–80% works well, and every Figure 5 fine-tuning result beats training from scratch (82.5%) (p. 5).

**Ablations, ViT-L/16 on IN1K** (Table 1, p. 5). Fine-tuning (ft) and linear probing (lin) accuracy (%); defaults marked *(default)*:

(a) Decoder depth:

| Blocks | ft | lin |
|---|---|---|
| 1 | 84.8 | 65.5 |
| 2 | 84.9 | 70.0 |
| 4 | 84.9 | 71.9 |
| 8 *(default)* | 84.9 | 73.5 |
| 12 | 84.4 | 73.3 |

(b) Decoder width:

| Dim | ft | lin |
|---|---|---|
| 128 | 84.9 | 69.1 |
| 256 | 84.8 | 71.3 |
| 512 *(default)* | 84.9 | 73.5 |
| 768 | 84.4 | 73.1 |
| 1024 | 84.3 | 73.1 |

(c) Mask token:

| Case | ft | lin | FLOPs |
|---|---|---|---|
| encoder w/ [M] | 84.2 | 59.6 | 3.3× |
| encoder w/o [M] *(default)* | 84.9 | 73.5 | 1× |

(d) Reconstruction target:

| Case | ft | lin |
|---|---|---|
| pixel (w/o norm) *(default)* | 84.9 | 73.5 |
| pixel (w/ norm) | 85.4 | 73.9 |
| PCA | 84.6 | 72.3 |
| dVAE token | 85.3 | 71.6 |

(e) Data augmentation:

| Case | ft | lin |
|---|---|---|
| none | 84.0 | 65.7 |
| crop, fixed size | 84.7 | 73.1 |
| crop, rand size *(default)* | 84.9 | 73.5 |
| crop + color jit | 84.3 | 71.9 |

(f) Mask sampling:

| Case | Ratio | ft | lin |
|---|---|---|---|
| random *(default)* | 75 | 84.9 | 73.5 |
| block | 50 | 83.9 | 72.3 |
| block | 75 | 82.8 | 63.9 |
| grid | 75 | 84.0 | 66.0 |

What the authors draw from them:

- **Decoder depth** matters for linear probing (up to 8% improvement) but less for fine-tuning; a single-block decoder still fine-tunes to 84.8% (p. 5).
- **Mask token in the encoder** hurts: linear probing drops by 14% (73.5 vs 59.6, i.e. points), attributed to the gap between pre-training (many mask tokens) and deployment (none) (p. 5); skipping it cuts training FLOPs by 3.3× (p. 5).
- **Target:** normalized pixels improve accuracy (local contrast); PCA (96 largest coefficients) degrades it; "the high-frequency components are useful" (p. 6). dVAE tokens (BEiT's target, cross-entropy loss) give +0.4% fine-tuning over unnormalized pixels but no advantage over normalized pixels and lower linear probing (p. 6).
- **Augmentation:** cropping-only works well; color jitter degrades; with no augmentation MAE still "behaves decently"; random masking does most of the augmentation's job, since masks differ every iteration (p. 6).
- **Sampling:** block-wise masking degrades at 75% (harder, blurrier, higher training loss); grid sampling (keep one in four) is easier and sharper but gives lower representation quality; random sampling works best (p. 6, Figure 6).

**Wall-clock time** (Table 2, p. 5). 800 epochs, 128 TPU-v3 cores, TensorFlow; decoder width 512, mask ratio 75%:

| Encoder | Dec. depth | ft acc | Hours | Speedup |
|---|---|---|---|---|
| ViT-L, w/ [M] | 8 | 84.2 | 42.4 | - |
| ViT-L | 8 | 84.9 | 15.4 | 2.8× |
| ViT-L | 1 | 84.8 | 11.6 | 3.7× |
| ViT-H, w/ [M] | 8 | - | 119.6† | - |
| ViT-H | 8 | 85.8 | 34.5 | 3.5× |
| ViT-H | 1 | 85.9 | 29.3 | 4.1× |

† estimated by training ten epochs (p. 5).

**Training schedule** (Figure 7, p. 6). ViT-L, default setting, values as printed on the plot:

| Epochs | 100 | 200 | 400 | 800 | 1600 |
|---|---|---|---|---|---|
| Fine-tuning | 82.3 | 83.3 | 84.3 | 84.9 | 85.1 |
| Linear probing | 57.3 | 64.4 | 69.7 | 73.5 | 75.1 |

No saturation of linear probing even at 1600 epochs, unlike MoCo v3, which saturates at 300 epochs for ViT-L (p. 6). ViT-L at 1600 epochs takes 31 hours on 128 TPU-v3 cores, vs. 36 hours for 300 epochs of MoCo v3 (p. 7).

**Comparison with self-supervised methods on IN1K** (Table 3, p. 7). End-to-end fine-tuning; 224 size except ViT-H₄₄₈; MAE with normalized pixels, 1600 epochs:

| Method | Pre-train data | ViT-B | ViT-L | ViT-H | ViT-H₄₄₈ |
|---|---|---|---|---|---|
| scratch, our impl. | - | 82.3 | 82.6 | 83.1 | - |
| DINO | IN1K | 82.8 | - | - | - |
| MoCo v3 | IN1K | 83.2 | 84.1 | - | - |
| BEiT | IN1K+DALLE | 83.2 | 85.2 | - | - |
| MAE | IN1K | 83.6 | 85.9 | 86.9 | 87.8 |

- The previous best with IN1K data only was 87.1% (512 size) (p. 7).
- MAE is 3.5× faster per epoch than BEiT (p. 7).
- Figure 8 (p. 7): with MAE pre-training the gain over supervised training from scratch grows with model size, a trend similar to JFT-300M supervised pre-training (p. 7).

**Partial fine-tuning** (Figure 9, p. 7). ViT-L, accuracy (%) vs. number of last blocks fine-tuned (0 = linear probing, 24 = full fine-tuning), values as printed on the plot:

| Blocks tuned | 0 | 1 | 2 | 4 | 6 | 12 | 18 | 24 |
|---|---|---|---|---|---|---|---|---|
| MAE baseline | 73.5 | 81.0 | 83.1 | 84.2 | 84.4 | 84.6 | 84.7 | 84.9 |
| MoCo v3 | 77.6 | 79.9 | 80.8 | 81.6 | 81.9 | 83.2 | 83.8 | 84.1 |

- Tuning only the MLP sub-block of the last block ("half" a block) gives 79.1% (p. 7).
- MoCo v3 has higher linear probing, but all its partial fine-tuning results are worse; the gap is 2.6% with 4 blocks (p. 7). MAE features are "less linearly separable" but "stronger *non-linear* features" (p. 7).
- Linear probing and fine-tuning results are "largely *uncorrelated*" (Table 1; p. 7, repeated in Appendix B, p. 12).

**COCO detection and segmentation** (Table 4, p. 8). Mask R-CNN; AP^box and AP^mask:

| Method | Pre-train data | AP^box ViT-B | AP^box ViT-L | AP^mask ViT-B | AP^mask ViT-L |
|---|---|---|---|---|---|
| supervised | IN1K w/ labels | 47.9 | 49.3 | 42.9 | 43.9 |
| MoCo v3 | IN1K | 47.9 | 49.3 | 42.7 | 44.0 |
| BEiT | IN1K+DALLE | 49.8 | 53.3 | 44.4 | 47.1 |
| MAE | IN1K | 50.3 | 53.3 | 44.9 | 47.2 |

**ADE20K semantic segmentation** (Table 5, p. 8). UperNet, mIoU:

| Method | Pre-train data | ViT-B | ViT-L |
|---|---|---|---|
| supervised | IN1K w/ labels | 47.4 | 49.9 |
| MoCo v3 | IN1K | 47.3 | 49.1 |
| BEiT | IN1K+DALLE | 47.1 | 53.3 |
| MAE | IN1K | 48.1 | 53.6 |

**Classification transfer** (Table 6, p. 8). Accuracy (%), MAE pre-trained on IN1K then fine-tuned:

| Dataset | ViT-B | ViT-L | ViT-H | ViT-H₄₄₈ | Prev best |
|---|---|---|---|---|---|
| iNat 2017 | 70.5 | 75.7 | 79.3 | 83.4 | 75.4 |
| iNat 2018 | 75.4 | 80.1 | 83.0 | 86.8 | 81.2 |
| iNat 2019 | 80.5 | 83.4 | 85.7 | 88.3 | 84.1 |
| Places205 | 63.9 | 65.8 | 65.9 | 66.8 | 66.0† |
| Places365 | 57.9 | 59.4 | 59.8 | 60.3 | 58.0‡ |

† pre-trained on 1 billion images; ‡ on 3.5 billion images (p. 8).

**Pixels vs. tokens** (Table 7, p. 8). △ = dVAE token minus normalized pixel:

| Target | IN1K ViT-B | IN1K ViT-L | IN1K ViT-H | COCO ViT-B | COCO ViT-L | ADE20K ViT-B | ADE20K ViT-L |
|---|---|---|---|---|---|---|---|
| pixel (w/o norm) | 83.3 | 85.1 | 86.2 | 49.5 | 52.8 | 48.0 | 51.8 |
| pixel (w/ norm) | 83.6 | 85.9 | 86.9 | 50.3 | 53.3 | 48.1 | 53.6 |
| dVAE token | 83.6 | 85.7 | 86.9 | 50.3 | 53.2 | 48.1 | 53.4 |
| △ | 0.0 | -0.2 | 0.0 | 0.0 | -0.1 | 0.0 | -0.2 |

"The difference is statistically insignificant" (Table 7 caption, p. 8); tokenization "is not necessary for our MAE" (p. 8).

**Linear probing vs. masked encoding methods** (Table 12, p. 12):

| Method | Model | Params | Acc |
|---|---|---|---|
| iGPT | iGPT-L | 1362 M | 69.0 |
| iGPT | iGPT-XL | 6801 M | 72.0 |
| BEiT | ViT-L | 304 M | 52.1† |
| MAE | ViT-B | 86 M | 68.0 |
| MAE | ViT-L | 304 M | 75.8 |
| MAE | ViT-H | 632 M | 76.6 |

† the authors' implementation. MAE ViT-L (75.8%) still lags MoCo v3 (77.6%) in linear probing (p. 12).

**Robustness** (Table 13, p. 12). Same MAE models as Table 3, inference only, no specialized fine-tuning; top-1 accuracy except IN-Corruption (mean corruption error, lower is better):

| Dataset | ViT-B | ViT-L | ViT-H | ViT-H₄₄₈ | Prev best |
|---|---|---|---|---|---|
| IN-Corruption ↓ | 51.7 | 41.8 | 33.8 | 36.8 | 42.5 |
| IN-Adversarial | 35.9 | 57.1 | 68.2 | 76.7 | 35.8 |
| IN-Rendition | 48.3 | 59.9 | 64.4 | 66.5 | 48.7 |
| IN-Sketch | 34.5 | 45.3 | 49.6 | 50.9 | 36.0 |
| *supervised baselines:* IN-Corruption ↓ | 45.8 | 42.3 | 41.3 | | |
| IN-Adversarial | 27.2 | 29.6 | 33.1 | | |
| IN-Rendition | 49.4 | 50.9 | 50.3 | | |
| IN-Sketch | 35.6 | 37.5 | 38.0 | | |

Larger image size helps on all sets but IN-C; with ViT-H, MAE is 35% better than supervised on IN-A (68.2% vs 33.1%, i.e. 35.1 points; about 106% relative) (p. 12).

**Qualitative** (Figures 2–4, 10–11, pp. 2–3, 13–14): at 80% masking only 39 of 196 patches remain (p. 2); an MAE trained at 75% still gives plausible reconstructions at 85% and 95% (Figure 4, p. 3); the output on visible patches is "qualitatively worse" because no loss is computed there (p. 2).

## Assumptions and limitations

- **Images only:** the argument rests on images having "heavy spatial redundancy", unlike language (pp. 1–2); the authors stress that images and languages "are *signals of a different nature*" and the difference "must be addressed carefully" (p. 8).
- **Linear probing is weak:** MAE features are less linearly separable than contrastive ones (Figure 9, p. 7; Table 12, p. 12); the authors argue linear separability "is not the sole metric" (p. 8).
- **Hyperparameter sensitivity reported only on IN1K with ViT-L** (Table 1, Figure 5). **Our reading:** the optimal masking ratio is an empirical finding for natural images.
- **Masked patches are random, not semantic:** "we remove random patches that most likely do *not* form a semantic segment" (p. 8).
- **Broader impacts** (p. 9): the model reflects biases of its training data and "may generate inexistent content".
- **Our reading:** the loss on masked patches only is called "purely result-driven" (p. 4, footnote 1), and the normalized target and the 75% ratio were chosen from the ablations (Table 1d, Figure 5), all on one dataset; nothing in the paper covers sequential or non-visual signals, continual pre-training, or anomaly detection.

## Relevance to this thesis

**Our reading:**

- **A candidate pre-training recipe for a time-series encoder:** split a series into non-overlapping temporal patches (the analogue of image patches), mask a random subset, encode only the visible patches, and reconstruct the masked values with a small decoder. The encoder's cost scales with the visible fraction (pp. 4–5), which makes long windows affordable.
- **The masking ratio does not transfer directly:** 75% works because images are spatially redundant (pp. 1–2). Time series can be strongly redundant (smooth, periodic signals) or not (noisy, event-driven sensors), so the ratio needs its own sweep, as in Figure 5 (p. 4), on our data.
- **Reconstruction target:** per-patch normalization (p. 4) maps naturally to per-window normalization of a series; it improved accuracy here (Table 1d, p. 5), but for anomaly detection removing a patch's level and scale could hide amplitude anomalies. To be tested, not assumed.
- **Reconstruction error as an anomaly score:** MAE is trained only to reconstruct; the paper never uses its error for detection, so this use is ours to validate.
- **Mask tokens only in the decoder** (Table 1c, p. 5): the pre-training/deployment gap argument applies to any model that is later fine-tuned on unmasked inputs, e.g. a forecasting head.
- **Fine-tuning vs. linear probing:** the two disagree (Table 1; p. 7), so the evaluation protocol after pre-training must be fixed in advance; for task arithmetic, the task vectors would come from fine-tuning (full or partial) a shared MAE-pre-trained encoder, which provides the common initialization merging requires.
- **Partial fine-tuning** (Figure 9, p. 7) gives a natural knob for task vectors restricted to the last blocks.

## Quotes worth keeping

> "we mask random patches of the input image and reconstruct the missing pixels." (p. 1)

> "First, we develop an asymmetric encoder-decoder architecture, with an encoder that operates only on the visible subset of patches (without mask tokens), along with a lightweight decoder that reconstructs the original image from the latent representation and mask tokens." (p. 1)

> "Images, on the contrary, are natural signals with heavy spatial redundancy—e.g., a missing patch can be recovered from neighboring patches with little high-level understanding of parts, objects, and scenes." (pp. 1–2)

> "Our loss function computes the mean squared error (MSE) between the reconstructed and original images in the pixel space. We compute the loss only on masked patches, similar to BERT [14]." (p. 4)

> "Computing the loss only on masked patches differs from traditional denoising autoencoders [58] that compute the loss on all pixels. This choice is purely result-driven: computing the loss on all pixels leads to a slight decrease in accuracy (e.g., ∼0.5%)." (p. 4, footnote 1)

> "By removing the mask token from the encoder, we constrain the encoder to always see *real* patches and thus improve accuracy." (p. 5)

> "These observations suggest that linear separability is not the sole metric for evaluating representation quality." (p. 8)
