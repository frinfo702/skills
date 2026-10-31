# Implement an experiment

Implements a baseline, a method or an experiment in the user's research repo, or reviews existing experiment code. In ML, code that runs can still be silently wrong, and implementation is where automated research most often fails (E3). The goal is code whose results can be trusted and reproduced, written in the repo's own style.

## Before writing code

1. Read the repo: how training and evaluation are run, configs, data loading, logging (MLflow, DagsHub, W&B or none), tests. Reuse what is there; follow its conventions. Add no framework the repo does not use.
2. Know the experiment card the code serves (`steps/approach.md`); if there is none, write the prediction and readings first.
3. Plan the change as the smallest diff that runs the experiment. Put the new idea behind a config option, so the baseline and the method run from the same code path.

## Writing it

- **Baseline first.** Reproduce the baseline on the fixed small split and compare against its reported number before touching the method (E4, C10).
- **One change at a time** relative to the baseline (C11).
- **Configs, not edits.** Every setting that differs between runs lives in the config and is logged with the run, together with the git commit and seed.
- **Determinism where cheap:** fixed seeds, logged data order; know which operations are non-deterministic.
- **Evaluation is shared:** the method and the baseline use the same evaluation function, split and preprocessing.

## Checking it before real runs

Run these and report each result:

- **Overfit a tiny set** (a batch or a handful of examples) to near-zero loss (C3).
- **Sanity numbers:** loss at initialization matches the expectation for the task; the baseline reproduces.
- **Data checks:** no overlap between train and test; labels and inputs line up after augmentation; the eval loader does not shuffle in a way that breaks per-example matching.
- **Common silent bugs:** train/eval mode (dropout, batch norm), gradient accumulation and loss scaling, wrong reduction (mean vs sum), broadcasting in losses, augmentation applied at test time, metrics computed on a subset, ignored mask or padding indices, mixed-precision overflow, a checkpoint loaded from the wrong run.
- **A small test** for any non-trivial new function (a shape or invariance check runs in seconds).

## Running

Run only what the user allowed. Log runs to the repo's tracker if it has one, tagged `r42.card=<name>`. Work on a branch; open a PR only if the user asks.

## Reviewing existing code

For a review request, go through "Checking it before real runs" against the code and report each problem with file:line, why it changes results, and the fix. Lead with whether results produced by this code can be trusted.

## Output

What was implemented (files, the config option), the check results, how to run the experiment in one command, and anything that looked wrong but was outside the request.
