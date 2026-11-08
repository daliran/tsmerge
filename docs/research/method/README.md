# Method

Everything specific to this work: what we ask, what we decided, how we test it, and what we found. The general concepts it relies on are in [knowledge/](../knowledge/README.md); what other people published is in [literature/](../literature/README.md).

**Status:** planned. Each part is created when it's first needed, with its own README holding its template and index.

| Part | What it will hold |
|---|---|
| `questions/` | Research questions, `RQ-NNNN`: what this thesis asks, and what would answer it |
| `decisions/` | Research decisions, `RD-NNNN`: methods, datasets, metrics, settings, each with its options and reasons |
| Protocol | How every experiment is run and judged: data use per dataset, splits, the strategies compared, selection rules, when a difference is real |
| Experiments | One doc per experiment, `e<NNNN>-<slug>` ([ED-0032](../../engineering/decisions/ED-0032-experiment-ids.md)): its question, setup, runs and results |
| Findings | What the experiments support, each claim linked to the runs behind it |

How this area relates to the rest of the research docs: [ED-0036](../../engineering/decisions/ED-0036-research-docs.md).
