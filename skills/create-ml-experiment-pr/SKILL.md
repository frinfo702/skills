---
name: create-ml-experiment-pr
description: >-
  Make an ML experiment pull request easy to review: put each fact in the one
  tool that owns it (numbers in MLflow, the question and interpretation in
  Linear, the code change in the PR), split mixed diffs into small single-purpose
  PRs, and write the PR description in a fixed, skimmable format adapted from
  Google, Linux kernel and Kubernetes review practice plus ML-specific checks.
  Use whenever an agent opens, writes, cleans up or reviews a PR for ML research
  or experiment code, when a PR is "too hard to review", or when the user says
  "PRを作って", "PR出して", "PR説明を書いて", "レビューしやすくして", "open a PR",
  or "write the PR description", even if they don't mention reviewability.
---

# ML Experiment PR

An ML experiment PR is hard to review when one page tries to be the lab notebook, the results database and the code change at once. AI-written PRs make this worse: one diff bundles a refactor, a new method and ten config tweaks, and the description narrates the process and pastes every metric. The reviewer cannot tell what changed, whether the comparison is fair, or where the numbers came from.

The fix is to give every fact one home and keep the PR about the code.

## Where each fact lives

| Tool | Owns | Does not hold |
|---|---|---|
| **Linear issue** | Why: the question, prediction, plan, decisions, interpretation, next steps. Outlives the PR. | Code, full metric tables |
| **MLflow** (or the project's tracker) | What came out: params, metrics, resolved config, git SHA, data version, plots, sample outputs. The source of truth for every number. | Interpretation |
| **PR** | What changed in code, how to check it, and the headline result as links into MLflow. | The research narrative, every metric, how the agent got there |
| **Commits** | One logical change each, in the imperative ("Add hard-negative sampler"). | "wip", "fix", "try again" |

Each fact is written once, in its home, and linked from everywhere else. If you are about to paste a 30-row metric table into a PR or write three paragraphs of hypothesis there, it belongs in MLflow or Linear instead.

If the project uses W&B, DagsHub or Notion instead, the same roles apply to whichever tool plays them. If one of these tools is missing entirely, ask before introducing it.

## One PR, one purpose

Before writing a description, look at `git diff <base>...HEAD`. Review cost grows faster than diff size, and mixed purposes make every line suspect. Split by type:

1. **Refactor**: no behavior change. Evidence: the baseline reproduces within seed noise, linked to its MLflow run.
2. **Method**: a new component behind a config flag that defaults to off, so the baseline path is untouched.
3. **Experiment**: config files (one Hydra experiment config per arm) and little or no code. Often only YAML.
4. **Fix**: a bug fix, with a note on which past runs it invalidates.

Aim for under about 400 changed lines of hand-written code. If the diff mixes types, propose the split to the user with the list of PRs. Do the split only once they agree, or if they already asked for it.

## Clean the diff before anyone sees it

Read the full diff yourself first, as the reviewer would. Remove:

- Run outputs, checkpoints, `mlruns/`, `wandb/`, `outputs/`, data files, notebooks with cell outputs.
- Debug prints, commented-out code, scratch scripts, unused helpers left from abandoned attempts.
- Unrelated formatting or renames (separate PR if wanted).
- Hyperparameters changed "while I was there". Only the variable under study changes (see `assist-research` if installed).

## Make MLflow complete before linking it

Every run the PR cites must carry: the resolved config as a param set or artifact, the git SHA, the dataset version or hash, the seed, and tags `linear=<ISSUE-ID>` and `pr=<number>` (add the PR tag after opening). Link **all** runs of the experiment, including failed and discarded ones, through a tag-filtered or compare view, not hand-picked run links. A reviewer must be able to see that the reported runs are not cherry-picked.

## Write the Linear update

The experiment report goes in the Linear issue as a comment or description section: question and one-line answer, setup at architecture level, headline numbers linked to MLflow, interpretation, threats to validity, next step. If `assist-research` is installed, its experiment report (Overview / Method / Results / Discussion structure) is this report. Link the PR. Lead with the conclusion.

## Write the PR description

Use the template in `references/pr-template.md`. The sections, in order:

1. **What & why**: problem first, then the change, in two or three sentences. Link the Linear issue. (Google: the first line must stand alone. Kernel: describe the problem before the solution.)
2. **Type**: refactor / method / experiment / fix. One.
3. **Changes**: one bullet per logical change with file paths. Flag anything that touches the baseline, the eval protocol or the data pipeline in bold. These change every past number.
4. **Fairness check** (method and experiment PRs): the variable under study, and the `diff` between the baseline config and each arm. It should show only that variable.
5. **Result**: the one-line answer and a table of at most three headline metrics, mean ± std with the number of seeds, each linked to MLflow. "Full results: <MLflow compare link>." Facts only. Interpretation is in Linear.
6. **Reproduce**: the exact command and commit. One command, no extra CLI overrides.
7. **Review guide**: where to start reading, what is mechanical and can be skimmed, what needs careful eyes, and specific questions for the reviewer. (Kubernetes: "Special notes for your reviewer".)

Delete a section that does not apply instead of writing "N/A". Title: `<area>: <imperative summary>`, under about 70 characters, e.g. `contrastive: add hard-negative mining (off by default)`.

### Writing rules

- Describe the final state, not the journey. "First I tried X, then Y failed…" goes in a Linear comment if it is worth keeping, otherwise nowhere.
- Every number links to the run it came from. A number without a run is not reported.
- Say what was not done: runs that failed, seeds not run, evals skipped.
- No filler ("This PR comprehensively…"), no emoji headings, no restating the diff line by line.
- Write in the language the team reviews in.

## Procedure

1. **Gather.** The Linear issue, the diff against base, the MLflow experiment. If any is missing, ask for it in one question.
2. **Check scope.** Classify the diff. If it mixes types, propose a split and wait.
3. **Clean** the diff (above). Rewrite commits into logical units if the history is noise, unless the user prefers to keep it.
4. **Complete MLflow** tags and artifacts for every cited run.
5. **Draft** the Linear update and the PR description. Show both to the user before posting: posting is visible to the team. Post directly only if the user already said to.
6. **Cross-link.** PR → Linear and MLflow. Linear → PR. MLflow runs → PR tag.
7. **Five-minute test.** Re-read the PR as a reviewer who has not seen the work. In five minutes, can they say what changed, why, whether the comparison is fair, and where each number came from? If not, fix the section that failed.

When reviewing someone else's ML PR, apply the same checks and report which ones fail, quoting the line, with a concrete fix.

## Sources

- Google Engineering Practices, "Writing good CL descriptions" and "Small CLs".
- Linux kernel, "Submitting patches": describe the problem first, one logical change per patch, imperative mood.
- Kubernetes PR template: what this PR does, which issue it fixes, special notes for your reviewer.
- Hugging Face transformers PR template: "What does this PR do?", "Fixes #", "Who can review?".
- ML-specific rules (one variable per comparison, uncherry-picked runs, config diff as fairness evidence) come from common reproducibility practice and the `assist-research` skill in this repo.
