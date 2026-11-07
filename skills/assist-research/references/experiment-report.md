# Experiment report

An experiment is only useful if someone else can tell what was done, what came out, and what it means, without those three blurring together. Use this structure whenever an experiment is written up: a PR, a report, a results section, a reply to an experiment card.

## Structure

If the `create-ml-experiment-pr` skill is installed, this report goes in the Linear issue, numbers stay in MLflow, and the PR itself follows that skill's format.

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
