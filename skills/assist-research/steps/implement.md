# Implement an experiment

Implements a baseline, a method or an experiment in the user's research repo, or reviews existing experiment code. In ML, code that runs can still be silently wrong, and implementation is where automated research most often fails (E3). The goal is code whose results can be trusted and reproduced, written in the repo's own style.

## Before writing code

1. Read the repo: how training and evaluation are run, configs, data loading, logging (MLflow, DagsHub, W&B or none), tests. Reuse what is there; follow its conventions. Add no framework the repo does not use.
2. Know the experiment card the code serves (`steps/approach.md`); if there is none, write the prediction and readings first.
3. Plan the change as the smallest diff that runs the experiment. Put the new idea behind a config option, so the baseline and the method run from the same code path.

## Writing it

- **Baseline first.** Reproduce the baseline on the fixed small split and compare against its reported number before touching the method (E4, C10).
- **One change at a time** relative to the baseline (C11); see "Change only the variable under study" below.
- **Configs, not edits.** Every setting that differs between runs lives in the config (Hydra, below) and is logged with the run, together with the git commit and seed.
- **Determinism where cheap:** fixed seeds, logged data order; know which operations are non-deterministic.
- **Evaluation is shared:** the method and the baseline use the same evaluation function, split and preprocessing.

## Change only the variable under study

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

## Make it reproducible with Hydra

Put everything needed to reproduce a run into a single Hydra experiment config, so the PR can point to one file.

- One file per experiment, e.g. `configs/experiment/<experiment_name>.yaml`, with `# @package _global_` so it can override any group.
- It holds the defaults it selects (model, dataset, trainer) and every value that differs from them, including seeds.
- The run command is then `python <entrypoint>.py +experiment=<experiment_name>`, with no extra CLI overrides. If you find yourself adding overrides on the command line, move them into the file instead.
- For a comparison, write one config per arm (e.g. `baseline.yaml`, `dataset_b.yaml`). Diffing the two files should show only the variable under study, which also serves as a check on the rule above.
- In the PR, point to the config file(s) by path.

If the project doesn't use Hydra yet, tell the user and ask before introducing it.

## Report only what was run

- Before running, write down in one sentence what question this experiment answers. If you can't, the experiment isn't ready. That sentence becomes the Overview.
- Put only numbers that came out of an actual run in Results. If a run failed, didn't finish, or wasn't done, say so explicitly. Never fill a table with expected or plausible values.
- Run only the experiments that were asked for. If another experiment looks worth doing, propose it in Discussion (`references/experiment-report.md`) instead of running it.

## Checking it before real runs

Run these and report each result:

- **Overfit a tiny set** (a batch or a handful of examples) to near-zero loss (C3).
- **Sanity numbers:** loss at initialization matches the expectation for the task; the baseline reproduces.
- **Data checks:** no overlap between train and test; labels and inputs line up after augmentation; the eval loader does not shuffle in a way that breaks per-example matching.
- **Common silent bugs:** train/eval mode (dropout, batch norm), gradient accumulation and loss scaling, wrong reduction (mean vs sum), broadcasting in losses, augmentation applied at test time, metrics computed on a subset, ignored mask or padding indices, mixed-precision overflow, a checkpoint loaded from the wrong run.
- **A small test** for any non-trivial new function (a shape or invariance check runs in seconds).

## Running

Run only what the user allowed. Log runs to the repo's tracker if it has one, tagged `assist-research.card=<name>`. Work on a branch; open a PR only if the user asks.

## Reviewing existing code

For a review request, go through "Checking it before real runs" against the code and report each problem with file:line, why it changes results, and the fix. Lead with whether results produced by this code can be trusted.

## Output

When results are written up, use `references/experiment-report.md`. Otherwise: what was implemented (files, the config option), the check results, how to run the experiment in one command, and anything that looked wrong but was outside the request.
