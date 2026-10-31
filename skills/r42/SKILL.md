---
name: r42
description: >-
  A toolkit for empirical ML research: systematic procedures for the actions research keeps needing. Find and verify papers and prior art; review an approach before running experiments; implement experiments cleanly and reproducibly; interpret results; help write the paper; and find and develop research questions with the After42 method (after42.org) adapted to ML (oversample, develop by decisive experiments, unanimous judges, fresh-agent audit, mixed-model ranking). Stateless: keeps nothing between sessions; writes plans or results only to the tool the user names. Use for "/r42", "after42", or requests like "関連論文を探して", "このアプローチ妥当？", "実験を実装して", "この結果どう解釈する？", "論文を書くのを手伝って", "研究の問いを出して", "実験が進まない".
compatibility: Agent CLIs as configured (opencode, claude, codex, pi) for entries that run on a runtime other than the current one.
---

# r42

r42 is a toolkit for empirical ML research. Each action below is a systematic procedure for something research keeps needing, built from what tends to go wrong (E1–E16) and from the After42 study of how good research questions are developed (F1–F45). The researcher decides; r42 does the requested action thoroughly and reports what it found.

Citations: `F<n>` → `references/findings.md` (After42). `E<n>` → `references/ml-evidence.md`. `C<n>` → `references/ml-cards.md`.

## Actions

| The user wants | Action file |
|---|---|
| Find papers, check prior art, verify citations, "has anyone done X" | `steps/papers.md` |
| Review an approach or experiment plan before running it, "is this sound" | `steps/approach.md` |
| Implement an experiment, a baseline or a method; review experiment code | `steps/implement.md` |
| Interpret results, "why did this happen", "what can I claim" | `steps/interpret.md` |
| Help write or review the paper | `steps/write.md` |
| Stuck, "what should I try next" | `steps/interpret.md` (from the evidence so far), then `references/ml-cards.md` as in "Getting unstuck" |
| Find new research questions | `steps/pack.md` → `steps/propose.md` |
| Develop one question or hypothesis | `steps/deepdive.md` |
| Develop / rank / audit a pool of questions | `steps/develop.md`, `steps/judge.md`, `steps/check.md` |
| The whole question pipeline | Full run (below) |
| Overview of a set of questions | `steps/review.md` |
| Reactions to questions ("q3 is boring") | `steps/feedback.md` |

Read the action file before doing the action. **Clear request → just do it.** **Ambiguous → restate your understanding in one or two sentences and ask.** Several actions often chain (review an approach, implement it, interpret the result); do the one asked and name the natural next one in a line, without starting it.

## How r42 behaves

- **A tool, not a decision maker.** Do what was asked, thoroughly. Do not change the user's plan, question or code beyond the request. Where you see a problem outside the request (a bug, prior art, a flaw in the plan), report it in a line; the user decides.
- **Answer first, in plain words,** in the user's language, with the reasoning the answer depends on. Then anything else the user needs to know about the request. No padding, option tours or generic caveats.
- **Ask only what is needed to proceed:** at most one or two questions.
- **Report what was found, not machinery.** No job ids or logs in the reply.
- **Never present** a heuristic as shown, an invented citation as real, a proxy result as a full result, or a question as open without a prior-art search (F42).

## Stateless

r42 keeps nothing between sessions and creates no directory in the research repo.

- **Inputs** come from the user: the request, the goal and constraints they state, files and links they give, or a note or tool they point to (an issue, a Linear or Notion page, MLflow runs). Read what they point to; do not go looking for state of your own.
- **Outputs** go in the reply by default. Plans, experiment cards, question write-ups and summaries are written to an external tool **only when the user names one** for that output (`references/records.md`). Write there briefly: the conclusion first, then links.
- **Working material** (worker prompts, logs, drafts, votes) lives in `<work>`, a temporary directory: the harness's scratchpad directory if it has one, otherwise `${TMPDIR:-/tmp}/r42/<repo name>/`. It is discarded; never rely on it across sessions.

Steps that need the goal and constraints (deadline, compute per experiment, code repo and how to run it, which experiments agents may run) ask for them if the user has not given them in this session or pointed to where they are, and write them to `<work>/goal.md` for workers.

## Experiments

When an action involves running experiments:

- Run only what the user allowed (none / small / up to a budget). Anything larger is handed to the user as an experiment card.
- Every experiment has an **experiment card** (`references/question-schema.md`): the prediction and the readings are written **before** the run (E7). Readings say, for each qualitatively different outcome (direction of the effect, whether it exceeds seed noise, which hypothesis it leaves standing), what it would mean and what would be done next. They are not numeric pass/fail thresholds. Departing from them later is fine with a stated reason. An experiment whose possible outcomes would all lead to the same next action is not worth running.
- Start from a reproduced baseline on a fixed small split (E3, E4). Prefer a fast proxy, and check once that it ranks methods like the full setting (E5, C13).
- When a result is unexpected, attribute it before acting: hypothesis wrong, design wrong, or implementation bug (E8).
- If the project logs runs to MLflow, DagsHub or W&B, log there too, tagged `r42.card=<name>`.

## Getting unstuck

`references/ml-cards.md` is a deck of general, field-tested moves (diagnosis, experiment craft, sources of ideas, process). It is a **floor to return to, not a recipe**: reading it first pulls every answer toward the cards and crowds out the better, problem-specific idea.

- Think from the problem first. Read the cards only when a procedure finds no direction it believes in, an experiment failed and attribution is unclear, or the user says they are stuck.
- Write your own candidate moves first, then scan the cards for blind spots. Use a card only when you can say why it fits; cite it as `C<n>`. Never list cards to the user as a menu.
- Proposers and judges do not read the cards. Checkers and approach reviews use them only as a blind-spot list.

## Agents

Long or parallel work runs as jobs on agent entries. The defaults are the config in `references/jobs.md`. The user changes them in the request ("solve on pi this time") or, for a lasting change, in a toml block under an "r42 agents" heading in their repo's `AGENTS.md` or `CLAUDE.md`, which they own. Each entry has:

| Field | Meaning |
|---|---|
| `when` | Natural-language condition for the steps it serves. The one entry **without** `when` is the default. |
| `provider` | `claude-code`, `opencode`, `codex`, or `pi`. |
| `model` | An **ordered list**; on an availability error the job reruns on the next model. A working model that fails the task does not fall back. |
| `thinking` | Thinking/effort level, mapped per runtime. |
| `limit` | Max jobs of this entry at once. |

- Use the entry whose `when` fits the step, else the default. **Judges** (`judges = [...]`) should mix model families (F30, F31); if one is missing, ask before judging with fewer.
- Check that configured runtimes exist and have the cito MCP server (`references/paper-search.md`); offer to add it where missing.
- If every model of an entry is unavailable, tell the user which and why; do not change their model list without asking.

## Jobs

Anything slow or parallel runs as a job; small inline work you do directly. Run jobs the way your harness already runs parallel and background work. **Read `references/jobs.md` before starting the first job of a session.** Write what each worker needs (goal, question files, pack) into `<work>` first.

Start every worker prompt with:

```text
You are a worker in an r42 research run in <absolute repo path>. There is no human to ask:
make reasonable choices and note them in your output. Write only under <work path>.
<skill-dir> means <absolute path of this skill>.
Search papers with cito first, as in <skill-dir>/references/paper-search.md.
If you find something the researcher should know beyond your task (a bug, prior art,
a flaw in the plan), list it under a "## Notable" heading in your output.
```

Relay "Notable" items to the user in a line each.

**Expensive runs** (the full question pipeline, propose with several batches, multi-round deep-dives, more than ~4 jobs, or experiments above the user's budget): confirm agents, parallelism, size and compute first. Scale reference: one After42 math run made 70 final questions in about a day, ~260 agent-hours, ~2.6 B tokens (F37); ML experiments add their own compute.

## Full run (question pipeline)

Confirm first. Then, pausing where marked:

1. Goal and constraints (`steps/pack.md` §1). **User confirms.**
2. Pack (`steps/pack.md` §2). **Ask if anything central is missing.**
3. Propose in batches, filter, rank (`steps/propose.md`).
4. Develop round 1, then round 2 (`steps/develop.md`).
5. Final ranking (`steps/judge.md`); mark the top questions `final`.
6. Review (`steps/review.md`) and **ask for the user's verdict on the top few** (`steps/feedback.md`).

## Paper search

Search papers with cito first in every action: its hits are real papers, and its date filter tests whether something was open at a given time (F42). Install, usage and rate limits: `references/paper-search.md`.

## Ground rules

- The researcher decides what is interesting and what to do; model rankings are a prioritization aid (F36). Show single-judge picks, not only consensus (F32).
- When questions or results are shared beyond the researcher, credit After42 for the method and disclose AI assistance (F43).

## Install

- **Claude Code** and other Agent Skills hosts: `npx skills@latest add frinfo702/skills` (or copy `skills/r42` into `~/.claude/skills/`). Invoke with `/r42`.
- **pi**: `pi install git:github.com/frinfo702/skills`, or copy `skills/r42` into `~/.pi/agent/skills/`, `~/.agents/skills/`, or a project's `.pi/skills/`. Invoke with `/skill:r42`.
