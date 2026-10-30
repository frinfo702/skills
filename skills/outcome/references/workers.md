# Worker configuration

Edit this file to change outcome's default routing. These are instructions for the
orchestrator, not a configuration file automatically consumed by any CLI.

## Priority

1. Explicit user instructions for this task or session.
2. Applicable local outcome settings in AGENTS.md, CLAUDE.md, or equivalent.
3. Defaults below.

A harness override replaces harness selection, including the automatic low-usage
fallback. A model override replaces the model, not unrelated settings. If the
specified model cannot run in the selected harness, explain the conflict and ask
for the missing choice. Never silently disregard a user override.

## Harness defaults

| Parent harness | Default worker harness |
| --- | --- |
| Claude Code (`claudecode`) | Claude Code |
| Codex (`codex`) | Codex |
| pi | pi |
| opencode | opencode |

For Claude Code and Codex, check remaining account usage before worker execution.
If remaining usage is **less than 20%**, select an available OSS harness: try pi,
then opencode. This order is a default tie-breaker; user preferences take priority.
Exactly 20% stays on the same harness. Do not switch from one paid harness to the
other as the quota fallback.

Use fresh quota information from a supported status interface. When several
applicable limits exist (for example, short-term and weekly limits), use the lowest
remaining percentage. Ignore limits that do not apply to the selected worker.
Convert used percentage to remaining percentage only when the source clearly
identifies it as used account quota. Context tokens, billing credit, and rate-limit
errors alone are not a remaining subscription-usage percentage.

If usage cannot be read, treat it as unknown, not as zero or plentiful. Briefly
report this and prefer an available OSS fallback. If neither fallback is usable,
finish independent preparation and ask whether to proceed on the paid harness
with unknown usage. Likewise, if usage is below 20% and no OSS fallback is usable,
report that blocker rather than silently consuming the paid quota. A prior user
instruction covering these cases is sufficient; do not ask again.

An OSS fallback is usable only if it is installed, can run workers, and has access
to the configured provider/model and required tools. An OSS harness does not imply
free inference. Do not install software, create accounts, or purchase credits as
part of fallback discovery. If the parent harness is unrecognized, use its native
worker only when an applicable user/local setting supplies the model; otherwise
resolve the missing configuration before launching.

## Model defaults

| Worker harness | Requested model | Reasoning effort |
| --- | --- | --- |
| Claude Code | Opus5.5-medium | medium |
| Codex | GPT-6-Astra-medium | medium |
| pi | opencode-go/deepseek-v4.1-max | Provider default |
| opencode | opencode-go/deepseek-v4.1-max | Provider default |

These names are user-selected targets, not claims that every installation exposes
these exact CLI identifiers. Resolve them against the installed harness's supported
model list or configuration. For the first two rows, `medium` denotes reasoning
effort and may be a separate option. For the OSS rows, preserve the provider/model
pair; do not reinterpret `max` as an effort flag. Do not silently fall back to the
parent model or another provider if a target cannot be resolved.

Apply this table to the **selected worker harness**, including after a quota
fallback. Keep the parent session unchanged. These defaults apply to all worker
roles; task complexity does not automatically change the model.
