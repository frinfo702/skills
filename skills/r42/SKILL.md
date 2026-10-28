---
name: r42
description: >-
  Find and develop research questions worth pursuing, using the After42 method (after42.org): build a literature pack toward a researcher-written goal, oversample candidate questions, develop them by attempting to solve them, accept revisions only when all model judges agree, audit them with a fresh checker, and rank them with mixed-model judges that learn from the researcher's feedback. One entry point for everything: a full run, a portfolio review, a deep-dive on the user's own question, or recording feedback. State lives in .r42/ of the research repo; long steps run as background jobs on configurable agents (provider, ordered model list with fallback, thinking level, and a plain-language when) on opencode, Claude Code, Codex or pi. Use when the user says "/r42", "r42", "after42", or asks to find, propose, sharpen, develop, rank or review research questions or directions, e.g. "研究の問いを出して", "このリサーチクエスチョンを深掘りして", "問いを磨いて", "what should I research next".
compatibility: Python 3.11+ (stdlib only). Agent CLIs as configured (opencode, claude, codex, pi).
---

# r42

Questions shape where research effort goes, and novel, difficult questions are easy to produce while interesting ones are rare: before development, experts judged 3% of single-pass AI proposals interesting; after solve-driven development, about a third (F1, F16). This skill runs that development process for the user's own field. The researcher sets the goal and decides what is worth pursuing; the agents explore many more candidates than one person could (F36, F44).

`F<n>` cites `references/findings.md`, which links each finding to its source on after42.org.

Talk to the user in their language. Keep the machinery out of the conversation: report questions, findings and decisions, not job ids.

## Every time /r42 starts

1. `S=<this skill's directory>`; the script is `python3 $S/scripts/r42.py`. Run it from the research repo.
2. If `.r42/` exists, run `r42.py events`. **Present every unacknowledged event in your reply to the user** (not only in intermediate output), one line each in plain words (which question or step finished, succeeded / failed / crashed / skipped, where the output is). For failures and crashes, read the log tail and say what went wrong. Act on what finished (next step of the loop, report to the user), then `r42.py ack <highest seq presented>`. Never ack an event you have not shown.
3. Read the state: `goal.md`, `pack/`, `questions/*.md` frontmatter (status, round), latest `rankings/`, `feedback.md`, `r42.py status`.
4. Route the user's words (below). With no words, give a three-line state summary and suggest the next step as a question.

## Routing

| The user wants | State needed | Do |
|---|---|---|
| Start, set or change the research goal | none | `r42.py init` if needed, then `steps/pack.md` §1 |
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

**Expensive runs** (full run, propose with several batches, multi-round deep-dive, anything starting more than ~4 jobs): before starting, confirm which agents each step will use, the parallelism, and the size (batches, questions developed, rounds). Give a rough scale: one After42 math run of 70 final questions took about a day, ~260 agent-hours and ~2.6 B tokens (F37); scale from that.

## Agents

`.r42/config.toml` (created by `r42.py init`) holds `judges`, `max_parallel`, `notify`, and **agent entries**. Each entry has:

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

- **Choosing an entry per job:** `r42.py agents` lists entries with their `when`. For each job, use the entry whose `when` fits the step, else the default; pass it as `submit --agent <name>`. An explicit request in the user's words ("solve on pi this time", "use codex as a third judge") wins for that request; change config only if the user says "always" or "from now on". Add or edit entries when the user describes one in words ("long literature research on pi with max thinking").
- **Judges** (`judges = [...]`, entry names, `default` allowed) should mix model families (F30, F31). If a judge's runtime is missing or keeps failing, tell the user and ask before judging with fewer.
- **On first init,** check the configured runtimes exist (`opencode`, `claude`, `codex`, `pi`). If the default entry's runtime is missing, ask the user which to use (offer the one running you) rather than switching silently.
- Events and job records name the model that actually ran. `unavailable` means every model in the list failed: tell the user which models failed and why (log tail); do not change their model list without asking.

## Jobs

Anything slow or parallel runs as a background job. Small inline work (recording feedback, combining rankings, writing a review) you do directly.

```bash
python3 $S/scripts/r42.py submit --step solve --name "solve q007 r1" [--agent pi] [--after <id>,<id>] --prompt-file /tmp/p.md
```

Write prompt files with your file-writing tool, not shell heredocs (long nested heredocs tend to hang the shell). `submit` prints the job id. The queue starts a job only when its `--after` jobs succeeded (a failed dependency makes it `skipped`), and within `max_parallel` and the agent's `limit`. A wrapper records every exit as a numbered event in `.r42/events.jsonl`: `succeeded`, `failed`, `unavailable` (every model in the agent's list failed for availability), `crashed` (process vanished, found by reconcile), or `skipped`. Queue a whole round at once with `--after` and let it run.

Start every worker prompt with:

```text
You are a worker in an r42 research run in <absolute repo path>. There is no human to ask:
make reasonable choices and note them in your output. Work only on the files named below.
<skill-dir> means <absolute path of this skill>.
```

**Waiting for completions:**

- **Claude Code:** after submitting, start `python3 $S/scripts/r42.py wait` as a background command (Bash `run_in_background`). It blocks until an unacknowledged event exists, then exits, which wakes you. Handle and present the events, ack, and if jobs remain queued or running, start `wait` again. Exit 3 means idle (nothing running, nothing unread); exit 2 means its timeout passed; restart it. Do not poll in a loop yourself.
- **Runtimes that cannot wake you (pi, codex, opencode):** set `notify = true` in config so each completion raises an OS notification, and tell the user to come back with `/r42` (or `/skill:r42` on pi). Unread events are presented on every start, so nothing is lost.

`r42.py status` lists jobs. Logs are in `.r42/jobs/<id>.log`.

## Full run

Confirm first (see Expensive runs). Then, pausing for the user where marked:

1. Goal (`steps/pack.md` §1). **User confirms the goal.**
2. Pack (`steps/pack.md` §2). Show the themes; **ask if anything central is missing.**
3. Propose in batches, then filter, then rank (`steps/propose.md`). Report counts by removal reason and the composition mix.
4. Develop round 1, then round 2 (`steps/develop.md`). Report each question's trajectory after each round.
5. Final ranking (`steps/judge.md`); mark the top questions `final`.
6. Review (`steps/review.md`) and **ask for the user's verdict on the top few**; record it (`steps/feedback.md`).

Between steps, submit the next step as soon as the previous events arrive; the pauses above are the only stops.

## State

All state is in `.r42/` of the research repo:

```text
.r42/config.toml         agents and limits
.r42/goal.md             the researcher's goal (F4)
.r42/pack/               summary.md, papers.md, open-questions.md (F5)
.r42/questions/<id>.md   one file per question (references/question-schema.md)
.r42/solves/<id>/        solve records per round
.r42/rankings/           per-judge and averaged rankings
.r42/feedback.md         the researcher's reactions (the most valuable file, F35)
.r42/review-<date>.md    portfolio reviews
.r42/jobs/, events.jsonl, events.ack   the job queue (managed by r42.py)
```

## Ground rules

- The researcher decides what is interesting; model rankings are a prioritization aid (F36). Show single-judge picks, not only consensus (F32).
- Report only what was found. Never present a heuristic as proved, an invented citation as real, or a question as open without a prior-art search (F42).
- When questions or results leave `.r42/`, credit After42 for the method and disclose AI assistance (F43).

## Install

- **Claude Code** and other Agent Skills hosts: `npx skills@latest add frinfo702/skills` (or copy `skills/r42` into `~/.claude/skills/`). Invoke with `/r42`.
- **pi**: `pi install git:github.com/frinfo702/skills` (pi discovers the repo's `skills/` directory), or copy `skills/r42` into `~/.pi/agent/skills/`, `~/.agents/skills/`, or a project's `.pi/skills/`. Invoke with `/skill:r42`.

Self-check of the job queue: `python3 $S/scripts/test_r42.py`.
