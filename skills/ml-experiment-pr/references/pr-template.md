# PR template for ML experiment work

Copy this, fill it in, then delete every section that does not apply.

~~~~markdown
## What & why
<!-- Problem first, then the change. 2–3 sentences. The first sentence must stand alone. -->

Linear: <ISSUE-ID link>

## Type
<!-- Exactly one: refactor | method | experiment | fix -->

## Changes
<!-- One bullet per logical change, with paths. Bold anything that touches the baseline,
     eval protocol or data pipeline. -->
- `path/to/file.py`: ...

## Fairness check
<!-- Method / experiment PRs only. -->
Variable under study: <X>

```diff
<diff of configs/experiment/baseline.yaml vs configs/experiment/<arm>.yaml>
```

## Result
<!-- Facts only. ≤3 headline metrics. Interpretation lives in Linear. -->
<One-line answer.>

| Arm | Metric A ↑ | Metric B ↓ |
|---|---|---|
| [baseline](<mlflow run/compare link>) | 71.2 ± 0.3 | 1.84 ± 0.02 |
| [<arm>](<mlflow link>) | 73.3 ± 0.4 | 1.79 ± 0.03 |

n = 3 seeds. Not run: <...>. Full results: <MLflow compare link filtered by tag linear=ISSUE-ID>.

## Reproduce
```bash
python train.py +experiment=<arm>   # at <commit SHA>
```

## Review guide
- Start at: `<file>`
- Mechanical, skim: `<files>`
- Needs careful eyes: `<file:line>`, because ...
- Question for reviewer: ...
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

1. `data: split loader into dataset and sampler (no behavior change)`: refactor; baseline reproduces at 71.2 ± 0.3 (link).
2. `eval: fix macro-F1 averaging over empty classes`: fix; **invalidates macro-F1 for runs before <SHA>**; baseline re-run linked.
3. `contrastive: add hard-negative mining (off by default)`: method + experiment config; fairness diff shows only `sampler.hard_negatives: true`; the LR change is proposed in the Linear issue as a separate follow-up experiment.
