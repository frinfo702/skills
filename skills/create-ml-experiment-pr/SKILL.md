---
name: create-ml-experiment-pr
description: >-
  Make an ML experiment pull request easy to review: put each fact in the one
  place that owns it (numbers in the experiment tracker, the question and
  interpretation in the issue tracker, the code change in the PR), split mixed diffs into small single-purpose
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

Write for the future reader: someone months later who vaguely remembers that an experiment like this existed but not its details, and who finds the PR by searching. From the title, the first sentence and the diagram alone, they should be able to tell whether this is the PR they are looking for and what it did, without having followed the work.

## Where each fact lives

Facts are split by role, not by product. Use whatever tools the project already uses for each role: find them from the repo (logging calls, config, links in the README or commits) or ask the user. Do not introduce a tool the project does not use without asking.

| Role | Owns | Does not hold |
|---|---|---|
| **Issue tracker** (the task's issue or ticket) | Why: the question, prediction, plan, decisions, interpretation, next steps. Outlives the PR. | Code, full metric tables |
| **Experiment tracker** | What came out: params, metrics, resolved config, git SHA, data version, plots, sample outputs. The source of truth for every number. | Interpretation |
| **PR** | What changed and why, a diagram of the experiment, the headline result as links into the experiment tracker, how to reproduce it. | The research narrative, every metric, how the agent got there, the file list (the diff shows it), the review guide (the issue tracker or the review tool holds it) |
| **Commits** | One logical change each, in the imperative ("Add hard-negative sampler"). | "wip", "fix", "try again" |

Each fact is written once, in its home, and linked from everywhere else. If you are about to paste a 30-row metric table into a PR or write three paragraphs of hypothesis there, it belongs in the experiment tracker or the issue tracker instead.

## One PR, one purpose

Before writing a description, look at `git diff <base>...HEAD`. Review cost grows faster than diff size, and mixed purposes make every line suspect. Split by type:

1. **Refactor**: no behavior change. Evidence: the baseline reproduces within seed noise, linked to its run in the experiment tracker.
2. **Method**: a new component behind a config flag that defaults to off, so the baseline path is untouched.
3. **Experiment**: config files (one experiment config per arm) and little or no code. Often only YAML.
4. **Fix**: a bug fix, with a note on which past runs it invalidates.

If the diff mixes types, propose the split to the user with the list of PRs. Do the split only once they agree, or if they already asked for it.

## Clean the diff before anyone sees it

Read the full diff yourself first, as the reviewer would. Remove:

- Run outputs, checkpoints, the experiment tracker's local directories, data files, notebooks with cell outputs.
- Debug prints, commented-out code, scratch scripts, unused helpers left from abandoned attempts.
- Unrelated formatting or renames (separate PR if wanted).
- Hyperparameters changed "while I was there". Only the variable under study changes (see `assist-research` if installed).

## Make the experiment tracker complete before linking it

Every run the PR cites must carry: the resolved config as a param set or artifact, the git SHA, the dataset version or hash, the seed, and tags or labels naming the issue and the PR (add the PR one after opening). Link **all** runs of the experiment, including failed and discarded ones, through a filtered or comparison view, not hand-picked run links. A reviewer must be able to see that the reported runs are not cherry-picked.

## Write the issue update

The experiment report goes in the issue as a comment or description section: question and one-line answer, setup at architecture level, headline numbers linked to the experiment tracker, interpretation, threats to validity, next step. If `assist-research` is installed, its experiment report (Overview / Method / Results / Discussion structure) is this report. Link the PR. Lead with the conclusion.

## Write the PR description

Use the template in `references/pr-template.md`. The sections, in order:

1. **What & why**: problem first, then the change, in two or three sentences. Link the issue. Name the task, dataset, model and method in full words, so a search for any of them finds the PR. If the change touches the baseline, the eval protocol or the data pipeline, say so in bold here: it changes every past number. (Google: the first line must stand alone. Kernel: describe the problem before the solution.)
2. **Experiment diagram**: a figure of what the experiment does (below), followed by text explaining it.
3. **Fairness check** (method and experiment PRs): the variable under study, and the `diff` between the baseline config and each arm. It should show only that variable.
4. **Result**: the one-line answer and a table of at most three headline metrics, mean ± std with the number of seeds, each linked to its run. "Full results: <link to the filtered view of all runs>." Facts only. Interpretation is in the issue.
   If the experiment involves training, add the loss curve in addition to the experiment diagram: train loss and the loss on the evaluation split monitored during training (validation, not the untouched final test set) overlaid on one plot, x-axis in steps or epochs. Log the plot to the experiment tracker and embed it in the PR. It shows convergence and overfitting at a glance, which the final numbers hide.
5. **Reproduce**: the exact command and commit. One command, no extra CLI overrides.

Do not write the PR type, a list of changed files, or a review guide in the body. The type is a label (`refactor`, `method`, `experiment`, `fix`); create the labels if the repo lacks them. The diff shows which files changed. The review guide lives in the issue tracker or the review tool.

Delete a section that does not apply instead of writing "N/A". Title: `<area>: <imperative summary>`, under about 70 characters, e.g. `contrastive: add hard-negative mining (off by default)`.

### Experiment diagram

The diagram shows what the experiment does, not its results: what goes in, which components it passes through, what is compared and what is measured. The future reader understands from it in a few seconds what this PR was about. If the experiment involves training, it also gets the loss curve in addition to this diagram (see Result).

Almost every experiment gets one. What it shows depends on the experiment, not on a fixed recipe: capture the flow of the experiment and the core of what it does, at the level of detail that core needs. Ask what someone must picture to understand this experiment, and draw that; put the part that is new or varied in the focus color, and leave out what does not help explain it. A sweep of one loss setting may need only the training and evaluation path with the loss highlighted; a new mechanism may need its internals; a study spanning several models or phases may need the whole flow. Only a change that alters no experiment, such as a refactor or fix with no behavior change, goes without one.

Follow the figure rules of `make-research-figure` if it is installed: all text in the image is English; the image holds only names of components, data and arms, never titles, explanations or numbers; a box holds a name only; one focus color for the new or varied part. Draw it with whatever the project or the user uses for figures, export an image, attach it to the PR and log it to the experiment tracker next to the runs.

Below the figure, write two to four sentences in the team's language. First say what kind of figure it is and what it depicts as a whole (e.g. the training and evaluation pipeline). Then say which highlighted part is new or varied, and what each arm does differently. Define every name in the figure that is not common knowledge in the field.

### Writing rules

- Describe the final state, not the journey. "First I tried X, then Y failed…" goes in an issue comment if it is worth keeping, otherwise nowhere.
- Every number links to the run it came from. A number without a run is not reported.
- Every reference to another tool is a clickable link to the exact page, written as `[<name>](<URL>)` (e.g. `[run abc](https://<tracker>/runs/abc)`, `[ENG-123](https://<issue tracker>/ENG-123)`), never "the results are in the tracker" or "see the issue". The future reader must be able to follow it in one click. If you do not have the URL, get it (from the tracker's API or by asking) rather than writing the tool's name alone.
- Say what was not done: runs that failed, seeds not run, evals skipped.
- No filler ("This PR comprehensively…"), no emoji headings, no restating the diff line by line.
- Write in the language the team reviews in.

## Procedure

1. **Gather.** The issue, the diff against base, the experiment's runs in the tracker. If any is missing, ask for it in one question.
2. **Check scope.** Classify the diff. If it mixes types, propose a split and wait.
3. **Clean** the diff (above). Rewrite commits into logical units if the history is noise, unless the user prefers to keep it.
4. **Complete the tracker's** tags and artifacts for every cited run.
5. **Draft** the issue update, the experiment diagram and the PR description, and set the type label. Show both to the user before posting: posting is visible to the team. Post directly only if the user already said to.
6. **Cross-link.** PR → issue and runs. Issue → PR. Runs → PR tag.
7. **Five-minute test.** Re-read the PR as a reviewer who has not seen the work. In five minutes, can they say what changed, why, whether the comparison is fair, and where each number came from? Then re-read the title, the first sentence and the diagram as the future reader who remembers only roughly what this was: would a search with the words they remember find it, and would they recognize it? If not, fix the section that failed.

When reviewing someone else's ML PR, apply the same checks and report which ones fail, quoting the line, with a concrete fix.

## Sources

- Google Engineering Practices, "Writing good CL descriptions" and "Small CLs".
- Linux kernel, "Submitting patches": describe the problem first, one logical change per patch, imperative mood.
- Kubernetes PR template: what this PR does, which issue it fixes, special notes for your reviewer.
- Hugging Face transformers PR template: "What does this PR do?", "Fixes #", "Who can review?".
- ML-specific rules (one variable per comparison, uncherry-picked runs, config diff as fairness evidence) come from common reproducibility practice and the `assist-research` skill in this repo.
