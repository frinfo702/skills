# Jobs

A job is one worker prompt run by one agent entry. There is no queue program: you run jobs with whatever your harness already has for parallel and background work, and the harness keeps track of them. Prompts and logs are working material in `<work>/jobs/`; nothing about jobs is recorded beyond the session.

## Running a job

1. Write the prompt to `<work>/jobs/<job>.prompt.md` with your file-writing tool, not a shell heredoc (long nested heredocs tend to hang the shell). `<job>` is a short slug of the job name, e.g. `solve-q007-r1-1`.
2. Start it in one of two ways:
   - **Your own runtime.** If the entry's provider is the runtime you are running in, and your harness can run a fresh subagent with the entry's model (or the entry gives no model), give the prompt to a subagent. A fresh subagent counts as a fresh agent; the checker needs one (F12).
   - **Another runtime**, or a model or thinking level your subagents cannot set: run the entry's command (below) from the research repo root, with stdin from `/dev/null` and stdout and stderr written to `<work>/jobs/<job>.log`. Run it as a background command if your harness has them; otherwise in the foreground.
3. When it ends, decide the result (below), tell the user in one line if it matters, and continue with the step.

**Parallel.** Start independent jobs together, using your harness's own mechanism for that (several subagents or background commands in one turn). Keep to `max_parallel` running jobs in total and to each entry's `limit`. Start more as running jobs finish.

**No parallel or background support.** Run jobs one at a time in the foreground. Results are the same, only slower. Tell the user once, when an expensive run starts.

**Waiting.** Use your harness's completion notice (a subagent returning, a background command exiting). Do not poll in a loop or sleep. While a round runs, give each finished job one line; the step's full reply comes when the round is done.

**Order.** The step files say which jobs need others first (e.g. refine after both solves). Start a job only after the jobs it needs have succeeded. If one of them did not succeed, do not start the jobs that depend on it: mark them `skipped` and say why.

## Result

A job **succeeded** when it exited cleanly *and* wrote the files its prompt names. A clean exit with a missing file is a failure, and so is a nonzero exit. For a failure, read the log tail (or the subagent's answer) and decide:

- **Availability failure:** the model was not found, an auth, quota or credit error, HTTP 401/402/403/404/408/429/5xx, the provider was unreachable, or the command itself was not found. Rerun the same prompt on the entry's next model, and log a line saying which model failed and why.
- **Ordinary failure** of a working model (it ran and got the task wrong, or crashed in its own code): do not try the next model. Mark it `failed`.
- If every model had an availability failure, mark it `unavailable`. Tell the user which models failed and why, and do not change their model list without asking.

A worker's output that merely quotes an error (e.g. a paper that mentions "HTTP 503") is not an availability failure. Judge from where the run stopped.

## Interrupted sessions

If a session ends while jobs run, their results are lost with `<work>`. Nothing is recovered; if the user wants the step again, rerun it.

## Commands per provider

Fill `<model>` and `<thinking>` from the entry. When an entry has no value for a placeholder, drop that argument and the flag right before it. An entry's `cmd = "..."` replaces the template, with the same placeholders plus `<prompt_file>`.

```bash
P="$(cat <work>/jobs/<job>.prompt.md)"

# claude-code   (keep "$P" right after -p: --allowedTools takes several values and would swallow it)
claude -p "$P" --model <model> --effort <thinking> --permission-mode acceptEdits \
  --allowedTools "WebSearch,WebFetch,Read,Grep,Glob,Write,Edit,Bash(python3:*)"

# opencode      (thinking is a model variant: <model>#<thinking>; with no model, drop -m entirely)
opencode run --auto -m <model>#<thinking> "$P"

# codex
codex exec --skip-git-repo-check -s workspace-write -m <model> -c model_reasoning_effort=<thinking> "$P"

# pi
pi -p --no-session --model <model> --thinking <thinking> "$P"
```

Each one runs as `<command> < /dev/null > <work>/jobs/<job>.log 2>&1` from the repo root.

**Watching jobs live in Rex.** If you run inside [Rex](https://www.superlogical.com/rex/docs/automate/cli) and the user wants to watch, run each command in its own unfocused tab named `r42 <job name>` with `rex run`, still writing the log. Load the `rex` skill for the commands (or run `rex skill show`). Close tabs only when the user asks.

## Default agent configuration

These are the defaults. A repo overrides them only with a toml block under an "r42 agents" heading in its `AGENTS.md` or `CLAUDE.md`, written when the user asks for a lasting change ("always solve on pi"). Overrides replace only the keys they set:

```toml
max_parallel = 4
# Judges for revision votes and rankings: entry names ("default" = the entry without when).
# Mix model families.
judges = ["default", "codex"]

# Agent entries. The entry without `when` is the default for every step. Read each `when`
# and use that entry where it applies; an explicit request ("solve on pi") wins.
#   provider  claude-code | opencode | codex | pi
#   model     ordered list; on an availability failure the next model runs. Omit for the
#             provider's default.
#   thinking  claude-code: --effort low|medium|high|xhigh|max
#             opencode: model variant, e.g. deepseek-v4.1-flash low|high|max (needs a model)
#             codex: model_reasoning_effort, e.g. low|medium|high
#             pi: --thinking off|minimal|low|medium|high|xhigh|max
#   limit     max jobs of this entry at once
#   cmd       optional: replaces the provider's command (placeholders as in references/jobs.md)
[agents.deepseek]
provider = "opencode"
model = ["opencode-go/deepseek-v4.1-flash", "opencode-go/glm-5.3", "opencode-go/kimi-k3"]
thinking = "high"
limit = 2

[agents.opus]
when = "checking questions for prior answers and validity (a fresh agent from another model family)"
provider = "claude-code"
model = ["claude-opus-5-5", "claude-sonnet-5-5"]
thinking = "high"
limit = 2

[agents.codex]
when = "judging, and whenever the user asks for codex"
provider = "codex"
limit = 2

[agents.pi]
when = "only when the user asks for pi"
provider = "pi"
limit = 2
```

Exactly one entry has no `when`. If a config has none or several, ask the user which entry is the default. Keys from older configs (`notify`, `rex`, `fallback`) are no longer used; leave them alone.
