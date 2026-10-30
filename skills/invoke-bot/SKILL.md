---
name: invoke-bot
description: >-
  Complete multi-step tasks through subagents and return finished deliverables with
  a concise outcome summary. Use when the user invokes invoke-bot, asks to delegate
  an end-to-end job, or wants a Grok Bot-style workflow that coordinates work across
  files, tools, or apps and brings back the result. Route workers by harness,
  remaining usage, and configured models; prepare consequential actions for human review. Do not trigger
  for simple questions or single-step edits unless explicitly requested.
---

# Invoke Bot

Own the result. Delegate concrete work to subagents, verify what comes back, and
give the user the finished artifacts with a short explanation of what was achieved.
Use the user's language. Keep orchestration details out of the final reply unless
they explain a limitation or the user asks for them.

## 1. Define the outcome

Extract the desired result, deliverables, completion criteria, constraints, and
existing authorizations from the conversation. Inspect relevant local instructions
and connected sources before asking for information they may already contain.
Ask only for missing information that materially affects correctness or scope;
continue independent work while waiting. State reasonable assumptions briefly.

Discover the current harness's delegation, tools, and app connections. Read
[Worker configuration](references/workers.md) before launching workers; it is the
single source of truth for harness selection, usage thresholds, and model defaults.
An installed CLI is not proof that its configured provider and model are usable.
Do not install tools or buy access just to obtain a configured worker.

## 2. Select the worker harness and model

Apply explicit user overrides first, then applicable local invoke-bot configuration,
then the defaults in [Worker configuration](references/workers.md). Overrides
replace only the fields they specify. Do not substitute task-based model routing
for the configured per-harness model.

Before launching each worker or concurrent batch, check the relevant paid
harness's remaining usage using its supported status interface or available
account-usage tool. Follow the configuration's rules for multiple limits, unknown
usage, and the strict 20% boundary. Do not infer account quota from context-window
space or invent a usage command or reading.

Resolve the selected model through the harness's supported model/configuration
interface. Preserve the configured provider and reasoning effort; a display label
may need translation into a model ID and a separate effort parameter. Verify that
mapping rather than passing a guessed CLI flag. If the requested combination is
unavailable, report the precise limitation instead of silently choosing another
model. Continue independent preparation while resolving a blocked worker launch.

Use native delegation for the selected harness when it can honor these settings.
Otherwise use that harness's supported worker/CLI interface. Carry the same task
scope, permissions, output destinations, and approval boundaries across harnesses.
Record the selected harness, model, effort, and usage evidence internally so the
routing can be checked without cluttering the final reply.

## 3. Delegate the work

Create at least one subagent for substantive execution. The parent coordinates,
integrates, verifies, and handles user communication and approvals. For a small job,
one worker is enough. Parallelize independent tasks within available capacity;
sequence dependent tasks and writes to shared files or external records. Use
separate output paths or explicit ownership to avoid conflicting edits.

Give each worker a compact brief containing:

- The concrete task and definition of done.
- Required context, inputs, relevant skills, and source locations.
- Output format and destination, including artifact paths or URLs to return.
- Scope, constraints, file ownership, and allowed external actions.
- Verification to perform and the evidence to return.
- A requirement to return blockers and proposed consequential actions to the parent.

Require a handoff with the result, artifact locations, checks performed, unresolved
issues, and any pending action. Do not accept a plan as a completed deliverable.
Reuse a worker for focused corrections. Avoid unbounded delegation and repeated
retries without new evidence.

If delegation is unavailable, say so plainly. Complete useful authorized work
directly where possible, but do not pretend subagents ran or describe this as a
successful test of the delegated workflow.

## 4. Finish preparation before requesting approval

Prepare and verify the exact draft, diff, recipient list, publication preview, or
record changes before asking the user to approve a consequential action. Examples
include sending messages, publishing content, spending money, deleting data, and
changing sensitive records. Workers inherit the same authorization boundary;
delegation does not grant additional permission.

Honor explicit approval requirements and existing authorization. Do not repeatedly
ask for permission already granted for the same scope. If an action is not yet
authorized, present the concrete artifact, destination, and effect, and ask one
specific question. Explain why approval is needed. Pause only the dependent action
and continue useful independent work. A generic request to handle a job does not
resolve an unspecified recipient, audience, price, or destructive choice.

Accept a clear affirmative response in context; do not require the literal word
"Done". Silence or elapsed time is not approval. If several actions are pending,
make clear which ones the response covers. If the payload or scope changes
materially, resolve authorization for the changed action before execution.

After approval, execute the approved action and verify its result. Before retrying
a timed-out external write, check whether it already succeeded to avoid duplicate
sends or updates. Distinguish prepared, approved, executed, and verified states.

## 5. Verify and deliver

Inspect the workers' actual outputs. Check that files exist and open, links point
to the intended artifacts, requested content is present, and relevant tests or
source checks support the result. Resolve missing or contradictory work before
claiming completion. Apply domain-specific skills where useful.

Attach finished files when the host supports attachments. Otherwise provide real,
accessible file links or app/PR URLs. Do not fabricate attachments, cloud URLs,
chat cards, or background execution. Keep outputs somewhere durable for the user;
do not delete deliverables during cleanup. A skill coordinates available tools;
it does not itself provision a cloud computer or scheduler.

Lead the final reply with the outcome, then provide the deliverable links. Usually
one to three short sentences or a few bullets suffice. Include material validation
or limitations, and a pending decision only when one remains. Avoid worker logs,
model-selection narratives, and lengthy process recaps. Never label a prepared
draft as sent or a partially completed task as done.

Example completed reply:

> 比較レポートを作成しました。3案の費用と導入条件を確認しています。
> [レポート](actual-artifact-path)

Example approval handoff:

> [送信文面と宛先一覧](actual-artifact-path)を用意しました。
> 外部送信の承認がまだないため、送信前に確認が必要です。この内容で記載の3名に送信してよいですか？

Replace example paths with verified artifact locations.
