# PR template for ML experiment work

Copy this, fill it in, then delete every section that does not apply. Set the type as a label (`refactor` / `method` / `experiment` / `fix`), not in the body.

~~~~markdown
## What & why
<!-- Problem first, then the change. 2–3 sentences. The first sentence must stand alone.
     Name task, dataset, model and method in full words so a search finds this PR.
     Bold any change to the baseline, eval protocol or data pipeline. -->

Issue: [<ISSUE-ID>](<issue URL>)

## Experiment
<!-- What the experiment does, not its results. English labels, names only, no text inside the image.
     Scope matches the experiment; no diagram for a refactor or fix without behavior change. -->
![<what the figure depicts>](<attached PNG>)

<2–4 sentences: what kind of figure this is and what it shows as a whole; which highlighted part is
new or varied; what each arm does differently. Define names that are not common in the field.>

## Fairness check
<!-- Method / experiment PRs only. -->
Variable under study: <X>

```diff
<diff of the baseline config vs the <arm> config>
```

## Result
<!-- Facts only. ≤3 headline metrics. Interpretation lives in the issue. -->
<One-line answer.>

| Arm | Metric A ↑ | Metric B ↓ |
|---|---|---|
| [baseline](<run URL>) | 71.2 ± 0.3 | 1.84 ± 0.02 |
| [<arm>](<run URL>) | 73.3 ± 0.4 | 1.79 ± 0.03 |

n = 3 seeds. Not run: <...>. Full results: [all runs](<URL of the tracker view filtered to this issue>).

<!-- Experiments with training, in addition to the diagram: train and validation loss overlaid on one plot, logged to the experiment tracker. -->
![loss curve: train vs val](<attached PNG>)
Source: [plot in tracker](<URL of the logged plot>)

## Reproduce
```bash
<one command that runs <arm>>   # at <commit SHA>
```
~~~~

## Before / after

**Before** (typical agent-written PR):

> # 🚀 Improve contrastive learning with hard negatives and various enhancements
>
> This PR comprehensively improves our training pipeline. First I tried adding hard negatives but the loss was unstable, so I lowered the learning rate to 1e-4 and added gradient clipping. I also refactored the data loader for clarity and fixed a bug in the eval script. Results are very promising!
>
> | run | acc | f1 | loss | val_loss | top5 | ... (28 columns) |
>
> Files changed: 41, +2,310 −870

Problems: three PR types in one diff, the learning rate changed alongside the method so the comparison is unfair, an eval bug fix silently changes the baseline numbers, results are pasted and not linked, and interpretation ("very promising") sits in place of facts.

**After**: three PRs.

1. `data: split loader into dataset and sampler (no behavior change)`: refactor; baseline reproduces at 71.2 ± 0.3 ([run a1b2](https://tracker.example/runs/a1b2)).
2. `eval: fix macro-F1 averaging over empty classes`: fix; **invalidates macro-F1 for runs before <SHA>**; baseline re-run: [run c3d4](https://tracker.example/runs/c3d4).
3. `contrastive: add hard-negative mining (off by default)`: method + experiment config; fairness diff shows only `sampler.hard_negatives: true`; the LR change is proposed in the issue as a separate follow-up experiment.
