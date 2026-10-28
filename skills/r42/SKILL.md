---
name: r42
description: >-
  Find and develop research questions worth pursuing, using the After42 method (after42.org): build a literature pack toward a researcher-written goal, oversample candidate questions, develop them by attempting to solve them, accept revisions only when all model judges agree, audit them with a fresh checker, and rank them with mixed-model judges that learn from the researcher's feedback. One entry point for everything: a full run, a portfolio review, a deep-dive on the user's own question, or recording feedback. State lives in .r42/ of the research repo; long steps run as parallel jobs through the harness's own subagents or background commands, on configurable agents (provider, ordered model list with fallback, thinking level, and a plain-language when) on opencode, Claude Code, Codex or pi. No scripts. Use when the user says "/r42", "r42", "after42", or asks to find, propose, sharpen, develop, rank or review research questions or directions, e.g. "研究の問いを出して", "このリサーチクエスチョンを深掘りして", "問いを磨いて", "what should I research next".
compatibility: Agent CLIs as configured (opencode, claude, codex, pi) for entries that run on a runtime other than the current one.
---

# r42

Questions shape where research effort goes, and novel, difficult questions are easy to produce while interesting ones are rare: before development, experts judged 3% of single-pass AI proposals interesting; after solve-driven development, about a third (F1, F16). This skill runs that development process for the user's own field. The researcher sets the goal and decides what is worth pursuing; the agents explore many more candidates than one person could (F36, F44).

`F<n>` cites `references/findings.md`, which links each finding to its source on after42.org.

## Replying to the user

Every reply, in every step, follows this contract. Its purpose is to keep the user on what they asked and to make complex agent reasoning easy to take in.

- **Answer the actual question or request first, directly, in plain words**, in the user's language. Include what that answer needs, including the reasoning it depends on, and nothing else.
- **No tangents.** No "by the way", side observations, unrequested caveats, tours of possible next steps, or menus of options.
- **Simple means direct and understandable, not merely short.** Keep the reasoning the answer needs; drop everything else.
- **Details go to files, not chat.** Evidence, judge rationales, logs, side findings, caveats and alternatives go to `.r42/`: per-question material in the question file, everything else from a step in `.r42/reports/<date>-<step>.md`. When details exist, name the file in one line (`詳細: .r42/reports/2026-10-28-pack.md`).
- **Ask only what is needed to proceed:** at most one or two questions, no option menus unless the user asks for options. When a request is ambiguous, confirming your understanding is the needed question.
- Report questions, findings and decisions, not job ids or machinery.

## Every time /r42 starts

1. Work from the research repo. `<skill-dir>` is this skill's directory.
2. If `.r42/jobs.md` exists, settle it as in `references/jobs.md` (On every start). **Present every unreported job in your reply to the user** (not only in intermediate output), one line each in plain words (what finished, and its result or what went wrong, read from the log tail for failures). Act on what finished (next step of the loop, report to the user), then mark those jobs `reported`. Never mark a job you have not shown.
3. Read the state: `goal.md`, `pack/`, `questions/*.md` frontmatter (status, round), latest `rankings/`, `feedback.md`, `jobs.md`.
4. Route the user's words (below). With no words, say where things stand in two or three lines and ask one question about what to do next.

## Routing

| The user wants | State needed | Do |
|---|---|---|
| Start, set or change the research goal | none | create `.r42/` if needed (State, below), then `steps/pack.md` §1 |
| Literature pack | goal | `steps/pack.md` §2 |
| New candidate questions | goal, pack | `steps/propose.md` |
| Develop / sharpen the pool ("next round") | developing questions | `steps/develop.md` |
| The whole pipeline | none | Full run (below) |
| Develop **their own** question / one question | the question | `steps/deepdive.md` |
| Rank / "which are best" | questions | `steps/judge.md` |
| Audit / "is this open, well posed" | questions | `steps/check.md` |
| Overall picture / "where are we" / review | `.r42/` | `steps/review.md` |
| Reactions to questions ("q3 is boring", "I like q7") | questions | `steps/feedback.md` |
| Change agents, limits, judges | none | edit `.r42/config.toml` |

Read the step file before doing the step. Prompts and rubrics live in `references/`.

**Clear request → just do it.** **Ambiguous → confirm understanding first**: restate your interpretation in one or two sentences and ask whether that is right ("You want to develop your own question about X, two rounds, rather than generate new ones. Right?"). Do not announce "next I will do X" and proceed; ask. Feedback the user gives in passing (any reaction to a specific question) is always recorded, without asking.

**Expensive runs** (full run, propose with several batches, multi-round deep-dive, anything starting more than ~4 jobs): before starting, confirm which agents each step will use, the parallelism, and the size (batches, questions developed, rounds). Include a rough scale in one line, scaled from one After42 math run: 70 final questions in about a day, ~260 agent-hours, ~2.6 B tokens (F37).

## Agents

`.r42/config.toml` (template in `references/jobs.md`) holds `judges`, `max_parallel`, and **agent entries**. Each entry has:

| Field | Meaning |
|---|---|
| `when` | Natural-language condition for the steps or situations it serves ("long literature research", "judging"). The one entry **without** `when` is the default for everything else. |
| `provider` | The runtime: `claude-code`, `opencode`, `codex`, or `pi`. |
| `model` | An **ordered list**. On an availability error (model not found, 401/402/403/404/429/5xx, quota, auth, provider unreachable) the job reruns on the next model. A working model that fails the task does not fall back. Omit for the provider's default. |
| `thinking` | Thinking/effort level, mapped per runtime: claude-code `--effort` (low–max), opencode model variant (`model#high`; deepseek-v4.1-flash: low, high, max), codex `model_reasoning_effort`, pi `--thinking` (off–max). |
| `limit` | Max jobs of this entry at once. |

The shipped config:

```toml
judges = ["default", "codex"]

[agents.deepseek]                       # no when: the default
provider = "opencode"
model = ["opencode-go/deepseek-v4.1-flash", "opencode-go/glm-5.3", "opencode-go/kimi-k3"]
thinking = "high"

[agents.opus]
when = "checking questions for prior answers and validity (a fresh agent from another model family)"
provider = "claude-code"
model = ["claude-opus-5-5", "claude-sonnet-5-5"]
thinking = "high"
```

(plus `codex` for judging and `pi` on request).

- **Choosing an entry per job:** read the entries and their `when` in config. For each job, use the entry whose `when` fits the step, else the default. An explicit request in the user's words ("solve on pi this time", "use codex as a third judge") wins for that request; change config only if the user says "always" or "from now on". Add or edit entries when the user describes one in words ("long literature research on pi with max thinking").
- **Judges** (`judges = [...]`, entry names, `default` allowed) should mix model families (F30, F31). If a judge's runtime is missing or keeps failing, tell the user and ask before judging with fewer.
- **On first init,** check the configured runtimes exist (`opencode`, `claude`, `codex`, `pi`). Also check each runtime has the cito MCP server (`claude mcp list`, `codex mcp list`, `pi mcp list`) and offer to add it where it is missing (`references/paper-search.md`). If the default entry's runtime is missing, ask the user which to use (offer the one running you) rather than switching silently.
- `jobs.md` names the model that actually ran. `unavailable` means every model in the list failed: tell the user which models failed and why (log tail); do not change their model list without asking.

## Jobs

Anything slow or parallel runs as a job. Small inline work (recording feedback, combining rankings, writing a review) you do directly.

Run jobs the way your harness already runs parallel and background work: subagents for entries on your own runtime, the entry's CLI command as a background command for any other runtime, and plain foreground runs where the harness has neither. Do not build a queue of your own on top of it. **Read `references/jobs.md` before starting the first job of a session**: it covers how to run a job, ordering, deciding success, model fallback, the record in `.r42/jobs.md`, and the commands per provider.

Start every worker prompt with:

```text
You are a worker in an r42 research run in <absolute repo path>. There is no human to ask:
make reasonable choices and note them in your output. Work only on the files named below.
<skill-dir> means <absolute path of this skill>.
Search papers with cito first, as in <skill-dir>/references/paper-search.md.
```

## Paper search

Search papers with cito first, in every step: its hits are real papers, which keeps invented citations out, and its date filter tests whether a question was open at a given time (F42). Install, usage and rate limits: `references/paper-search.md`.

## Full run

Confirm first (see Expensive runs). Then, pausing for the user where marked:

1. Goal (`steps/pack.md` §1). **User confirms the goal.**
2. Pack (`steps/pack.md` §2). **Ask if anything central is missing.**
3. Propose in batches, then filter, then rank (`steps/propose.md`).
4. Develop round 1, then round 2 (`steps/develop.md`).
5. Final ranking (`steps/judge.md`); mark the top questions `final`.
6. Review (`steps/review.md`) and **ask for the user's verdict on the top few**; record it (`steps/feedback.md`).

Between steps, start the next step as soon as the previous step's jobs finish; the pauses above are the only stops. Each step's reply and report file follow the step file.

## State

All state is in `.r42/` of the research repo. To create it, make the directories below and write `config.toml` from the template in `references/jobs.md`:

```text
.r42/config.toml         agents and limits
.r42/goal.md             the researcher's goal (F4)
.r42/pack/               summary.md, papers.md, open-questions.md (F5)
.r42/questions/<id>.md   one file per question (references/question-schema.md)
.r42/solves/<id>/        solve records per round
.r42/rankings/           per-judge and averaged rankings
.r42/feedback.md         the researcher's reactions (the most valuable file, F35)
.r42/reports/            per-step reports and portfolio reviews: the details behind each chat reply
.r42/jobs.md             one line per job: status, agent, model, reported (references/jobs.md)
.r42/jobs/               each job's prompt and log
```

## Ground rules

- The researcher decides what is interesting; model rankings are a prioritization aid (F36). Show single-judge picks, not only consensus (F32).
- Report only what was found. Never present a heuristic as proved, an invented citation as real, or a question as open without a prior-art search (F42).
- When questions or results leave `.r42/`, credit After42 for the method and disclose AI assistance (F43).

## Install

- **Claude Code** and other Agent Skills hosts: `npx skills@latest add frinfo702/skills` (or copy `skills/r42` into `~/.claude/skills/`). Invoke with `/r42`.
- **pi**: `pi install git:github.com/frinfo702/skills` (pi discovers the repo's `skills/` directory), or copy `skills/r42` into `~/.pi/agent/skills/`, `~/.agents/skills/`, or a project's `.pi/skills/`. Invoke with `/skill:r42`.
