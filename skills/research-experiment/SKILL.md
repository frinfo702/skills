---
name: research-experiment
description: Run ML experiments reliably and write them up so results are easy to read. Covers changing only the variable under study, Hydra configs for reproducibility, the experiment PR (Overview, Method, Results, Discussion), architecture-level settings, metric formulas, and keeping results separate from interpretation. Use whenever the user runs, plans, or reports an ML experiment, or writes an experiment PR, report, or results section, even if they just say "実験して", "実験PR書いて", "結果まとめて", "ablationしたい", or "run the experiment".
---

# Research Experiment

An experiment is only useful if someone else can tell what was done, what came out, and what it means, without those three blurring together. This skill covers two things: running the experiment so the numbers can be trusted, and writing it up so they can be read.

## Running the experiment

### Change only the variable under study

An experiment asks "what happens when X changes?" Change X and nothing else. Every other difference between the runs makes the answer unreadable.

This includes changes made with good intentions. If the question is "what happens when we switch to dataset B?", an expected performance drop *is* the answer. Retuning the learning rate, adding augmentation, or adjusting the architecture to soften that drop makes it a different experiment. The user wanted to see the raw effect of the dataset, and a compensated result hides it.

If you think the comparison would be fairer or more interesting with some other change, don't make it. Mention it in Discussion as a possible follow-up.

What stays fixed depends on the experiment type:

| Experiment type | Changes | Stays fixed |
|---|---|---|
| Dataset change | Training and/or eval data | Model, training recipe, hyperparameters, eval protocol |
| Model / architecture change | Model or one component of it | Data, training recipe, hyperparameters (unless the user says to tune each), eval protocol |
| Method addition / ablation | The one added or removed component | Everything else, including the training budget |
| Hyperparameter sweep | The swept parameter(s) only | Data, model, other hyperparameters, seeds |

If the user's request doesn't say which variable is under study, or implies changing two at once, ask before running.

### Make it reproducible with Hydra

Put everything needed to reproduce a run into a single Hydra experiment config, so the PR can point to one file.

- One file per experiment, e.g. `configs/experiment/<experiment_name>.yaml`, with `# @package _global_` so it can override any group.
- It holds the defaults it selects (model, dataset, trainer) and every value that differs from them, including seeds.
- The run command is then `python <entrypoint>.py +experiment=<experiment_name>`, with no extra CLI overrides. If you find yourself adding overrides on the command line, move them into the file instead.
- For a comparison, write one config per arm (e.g. `baseline.yaml`, `dataset_b.yaml`). Diffing the two files should show only the variable under study, which also serves as a check on the rule above.
- In the PR, point to the config file(s) by path.

If the project doesn't use Hydra yet, tell the user and ask before introducing it.

### Report only what was run

- Before running, write down in one sentence what question this experiment answers. If you can't, the experiment isn't ready. That sentence becomes the Overview.
- Put only numbers that came out of an actual run in Results. If a run failed, didn't finish, or wasn't done, say so explicitly. Never fill a table with expected or plausible values.
- Run only the experiments that were asked for. If another experiment looks worth doing, propose it in Discussion instead of running it.

## Experiment PR structure

Use these four sections, in this order:

```markdown
## Overview
<!-- What question this experiment answers, and the one-line answer. 2-3 sentences. -->

## Method
### Setup
<!-- Architecture-level: models, datasets, training paradigm, what is compared with what.
     Link to the Hydra experiment config(s). -->

### Metrics
<!-- Each metric: name, formula, which direction is better. -->

## Results
<!-- Facts only: tables, plots, numbers. -->

## Discussion
<!-- Interpretation: why the results came out this way, limitations, next steps. -->
```

### Overview

The reader decides from this whether to read the rest. State the question and the answer: "Does adding X improve Y on Z? It improves accuracy by 2.1pt but doubles inference time."

### Method → Setup

Write at the level of architecture and design, not hyperparameters. The reader needs to understand *what system was built and what was compared*. Re-running it is what the Hydra config is for.

Write about:
- Models and backbones (e.g., "ViT-B/16, ImageNet-21k pretrained")
- Datasets and splits (e.g., "CIFAR-100, official train/test split")
- Training paradigm (e.g., "full fine-tuning", "LoRA", "contrastive pretraining then linear probe")
- What is being compared: baseline vs. proposed, and the one thing that differs between them

Leave out values like `lr: 0.2`, `batch_size: 64`, `warmup: 500`. They live in the config. A hyperparameter belongs here only when it is itself the variable under study, as in a learning-rate sweep.

"Abstract" doesn't mean vague. "A transformer model on some text data" is too vague. "Llama-3-8B fine-tuned with LoRA on Alpaca, compared against the same model without fine-tuning" is the right level.

### Method → Metrics

Give every metric a formula, even familiar ones. "Accuracy" and "F1" hide choices like macro vs. micro, top-1 vs. top-5, and what counts as positive, and those choices change the number.

For each metric:
- Name
- Formula in LaTeX (`$...$` or `$$...$$`), with every symbol defined
- Which direction is better
- Granularity if it matters (per-sample average vs. corpus-level, macro vs. micro)

Example:

> **Macro-F1** (higher is better)
> $$\text{Macro-F1} = \frac{1}{C}\sum_{c=1}^{C} \frac{2 P_c R_c}{P_c + R_c}$$
> where $C$ is the number of classes and $P_c$, $R_c$ are the precision and recall of class $c$.

### Results

Facts only. The reader should be able to form their own view before reading yours.

- Tables and plots, with units and the better direction (↑/↓) in column headers.
- Mean ± std when there are multiple seeds, and state the number of seeds.
- Bold the best value in each column if that helps, since it is a fact and not interpretation.
- Short descriptive sentences are fine ("B is 2.1pt higher than A on Macro-F1"). Words of cause or judgment are not: "because", "suggests", "effective", "surprisingly", "this shows". Those belong in Discussion.

A quick check: if a sentence would still be true when the reader disagrees with your explanation, it belongs in Results. If it wouldn't, move it to Discussion.

### Discussion

This is where interpretation goes: why the results came out this way, whether the question in Overview is answered, threats to validity (single seed, small eval set, possible leakage), and what to try next. Tie each claim to a specific number in Results.
