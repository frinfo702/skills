# Records

r42 keeps no state directory. What is worth keeping is recorded in the tools the researcher already uses, short and readable by a person. Everything else is working material in `<work>` and is thrown away.

## Two kinds of material

- **Records**: the goal, the notebook, questions, experiment cards and results, decisions, feedback, rankings in brief, the pack. These go to the researcher's tools (below). They are what a person reads and what the next session starts from.
- **Working material**: worker prompts and logs, attempt write-ups, revision drafts, votes, full judge rationales. These live in `<work>`, a temporary directory: the harness's scratchpad directory if it has one, otherwise `${TMPDIR:-/tmp}/r42/<repo name>/`. It may vanish between sessions; never rely on it. Before a step, rebuild what workers need there from the records (for example, write each question issue's body to `<work>/questions/<id>.md`).

## How records are written

The researcher does not read long logs. Every record is written for a person skimming it:

- Lead with what changed or was decided, in one or two sentences. Then links (run, PR, paper, issue).
- No transcripts, no tool output, no worker write-ups pasted in. Summarize and link; if a few lines of rationale are needed, put them in a collapsed `<details>` block.
- One comment per event (a round, an experiment result, a check, a piece of feedback), not one per job.
- Update the current state in place (an issue body, a document) and use comments for history.

## Finding the researcher's tools

On first use in a repo, look for what is already in use. Never introduce a tool the project does not use.

| Tool | Signs it is in use | How to reach it |
|---|---|---|
| GitHub issues and PRs | a `github.com` git remote; `gh auth status` works | `gh` (or `gh-axi`) |
| Linear | a Linear MCP server or CLI is connected; Linear links in the repo | the Linear tools |
| MLflow | `mlflow` in dependencies, `MLFLOW_TRACKING_URI`, a `mlruns/` directory, `mlflow.` calls in code | the project's own logging code, `mlflow` CLI or Python client |
| DagsHub | a `dagshub.com` remote, `dagshub` in dependencies, `dagshub.init` in code | its MLflow endpoint, as MLflow |
| Weights & Biases | `wandb` in dependencies or code | as for MLflow, with run tags and notes |
| Notion | a Notion MCP server is connected and the researcher keeps notes there | the Notion tools |

Then propose a mapping in a few lines, using the defaults below, and ask the researcher once to confirm it. Write the confirmed mapping as a short "r42 records" section in the repo's `AGENTS.md` (or `CLAUDE.md` if that is what the repo has), in a PR or commit the researcher approves; it is the only thing r42 adds to the repo for itself. Once the mapping is confirmed, write records within it without asking again. Creating anything outside it (a new Linear project, a new repo, a new label set in someone else's repo) needs a new confirmation.

## Default mapping

Use the first destination the researcher has; fall back down the list.

| Record | Destination |
|---|---|
| **Notebook** (goal, constraints, beliefs, open threads, decisions, disagreements) | one pinned GitHub issue titled `r42 notebook` (body = current state, comments = log), or a Linear document in the project, or a Notion page |
| **Question** | one issue per question: GitHub issue labelled `r42:question` plus a status label (`r42:candidate`, `r42:developing`, `r42:final`, `r42:user`; closed when removed), or a Linear issue with equivalent labels. Body = the current question in the schema; comments = round summaries, check notes, feedback |
| **Experiment card** | a comment on the question's issue, posted **before** the run with Decides, Prediction and Decision rule. The run itself in MLflow / DagsHub / W&B, tagged `r42.question=<id>`, `r42.card=<E-number>`, with the prediction in the run description. The result is a reply comment with the key numbers and the run link. Comments keep edit history, which shows the card was not rewritten |
| **Experiment code** | a branch and PR in the research repo, linked from the card |
| **Pack** | a document: Linear document, Notion page, or one markdown file in the repo's docs (via PR). `mechanisms` and `baselines` are sections of it |
| **Ranking, review, round report** | one short comment on the notebook issue: the top questions one line each, single-judge picks, what changed. Rationales in `<details>` at most |
| **Feedback** | a comment on the question's issue quoting the researcher, plus a `r42:interesting` / `r42:not-interesting` label |

If the researcher uses none of these, keep the notebook and questions as GitHub issues if there is a GitHub remote; otherwise ask where they want records, and until then keep them only in the conversation.

## Reading records back

At the start of a session: read the notebook record and what changed since its last `r42` comment (edits by the researcher are the most important input); list open question issues and their labels; list recent runs tagged `r42.*`. That is the state. Anything the records do not say is not known.
