# Learning

How models learn: from pretraining and fine-tuning, to training on all the data at once, to learning from data that keep arriving (continual learning), including combining models in weight space (model merging).

The generic concepts these build on are one level up, in [knowledge/](../README.md), mostly [models](../models/).

## Reading order

Read top-down the first time; the numbers are a suggested path, not a requirement.

| # | Folder | Docs | Status |
|---|---|---|---|
| 1 | this folder | [self-supervised learning](self-supervised-learning.md), [pretraining and fine-tuning](pretraining-and-fine-tuning.md), [parameter-efficient fine-tuning](parameter-efficient-fine-tuning.md), [joint training](joint-training.md) | placeholders |
| 2 | [continual-learning/](continual-learning/) | [continual learning](continual-learning/continual-learning.md), [forgetting and plasticity](continual-learning/forgetting-and-plasticity.md), [sequential fine-tuning](continual-learning/sequential-fine-tuning.md), [replay](continual-learning/replay.md), [regularization](continual-learning/regularization.md), [parameter isolation](continual-learning/parameter-isolation.md) | placeholders |
| 3 | [continual-learning/model-merging/](continual-learning/model-merging/) | [weight-space geometry](continual-learning/model-merging/weight-space-geometry.md), [loss landscape](continual-learning/model-merging/loss-landscape.md), [Fisher information](continual-learning/model-merging/fisher-information.md), [task arithmetic](continual-learning/model-merging/task-arithmetic.md), [model merging](continual-learning/model-merging/model-merging.md), [interference reduction](continual-learning/model-merging/interference-reduction.md), [continual merging](continual-learning/model-merging/continual-merging.md) | placeholders |
| 4 | [continual-learning/](continual-learning/) | [co-observation](continual-learning/co-observation.md): why combining separately trained models may fall short of joint training | placeholder |

- **Continual learning** sits inside learning, and **model merging** inside continual learning, because each is a special case of the one above it.
- **Co-observation comes last,** because it builds on joint training, replay and model merging.
