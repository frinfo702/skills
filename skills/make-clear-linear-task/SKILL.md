---
name: make-clear-linear-task
description: >-
  Write or rewrite a Linear issue so a teammate understands it in ten seconds,
  using the short, fixed-field templates that well-run OSS projects (uv,
  Ghostty, vLLM) use for bugs, features, and RFCs. Use whenever creating a
  Linear issue, filing a ticket or task, splitting work into issues, or when
  the user says an issue is hard to read, too long, or "AI-written" and wants
  it cleaned up, even if they don't mention templates.
---

# Make a Clear Linear Task

An issue is read far more often than it is written: in triage, in a cycle review, and by whoever picks it up weeks later. Issues written by agents tend to fail the same way. They are long, they mix the problem with an implementation plan, they put a heading on every thought, and they hedge. The reader has to dig for the one sentence that says what is wrong or what is wanted.

Mature OSS projects solved this with templates that have very few fields, each with one job. uv asks for a **Summary** and a reproducible example. Ghostty separates **Expected** from **Actual** behavior and asks for numbered **Reproduction Steps**. vLLM asks for the **motivation** before the proposal and for **alternatives** considered. This skill applies those same fields to Linear.

## Rules

1. **The title says the outcome.** A short imperative or a plain statement of the defect: "Retry failed uploads", "Login redirects to 404 after SSO". No `[Bug]:` prefixes; Linear has labels for that.
2. **The first sentence carries the issue.** Someone who reads only that sentence should know what is wrong or what is wanted, and why it matters.
3. **Use only the template's fields, and drop empty ones.** Never write "N/A" or "None". A missing section is clearer than a filled-in placeholder.
4. **Problem before solution.** Describe what is broken or missing in terms of behavior. Name a solution only if it has already been decided.
5. **Keep the human part short.** Aim for under 150 words above the agent notes. Plain sentences, not nested bullets.
6. **Put agent detail in a collapsed section.** Implementation plans, file lists, logs, and reproduction scripts go at the end in Linear's collapsible block, so they don't crowd the readable part:

   ```
   +++ Agent notes

   Details for agents go here.

   +++
   ```

7. **Don't invent facts.** Versions, error messages, owners, and deadlines come from the user or the codebase. If one is needed and unknown, ask, or leave `[?]` in place.
8. **Write in the language the team uses.** Match the existing issue or the user's prompt.

## Templates

Pick the type first. Most issues are a task; use bug only when something that should work does not.

### Bug (uv, Ghostty)

```markdown
<One sentence: what breaks, where, and for whom.>

## Steps to reproduce
1. ...
2. ...

## Expected
<What should happen.>

## Actual
<What happens instead. Quote the exact error.>

## Environment
<Version, OS, config — only what is relevant to reproduce.>
```

A bug without reproduction steps is a guess. If the user cannot give steps, say so in the summary ("Seen twice in production, not yet reproduced").

### Task or feature (uv, vLLM)

```markdown
<One or two sentences: what should exist or change, and the problem it solves.
If relevant, the current behavior.>

## Example
<How someone will use it, or what the result looks like. A command, a screen,
an API call, or a before/after.>

## Done when
- <Observable condition>
- <Observable condition>

## Alternatives
<Other approaches considered and why not. Omit if none.>
```

"Done when" is not in the OSS templates, but a Linear issue is assigned work, so it needs a finish line. Two or three observable conditions, not a test plan.

### RFC or design question (vLLM)

```markdown
<One sentence: the decision that needs to be made.>

## Motivation
<Why now. What breaks or stays painful without a decision.>

## Proposal
<The proposed change, in a few sentences.>

## Open questions
- ...
```

## Procedure

1. **Read before writing.** When rewriting, fetch the issue and its comments (`get_issue`, `list_comments`). When creating, search for duplicates with `list_issues` first.
2. **Choose the type** and fill only its fields from what the user said, the old issue, and the code. Move everything else into Agent notes or delete it.
3. **Do the ten-second test.** Read only the title and first sentence. If they don't say what is wrong or wanted, rewrite them before anything else.
4. **Show the draft and save after the user agrees**, unless they already asked you to save it. Use `save_issue`; for long descriptions, a full replacement is fine, since the structure usually changes.

## Example

Before (agent-written):

> ## Overview
> This issue aims to comprehensively address the user experience challenges associated with the authentication flow. Currently, there may be several potential issues that could impact users.
> ## Background
> ...
> ## Implementation Plan
> 1. Investigate `auth/redirect.ts`
> 2. ...

After:

> **Title:** Login redirects to 404 after SSO
>
> Users who sign in with Google SSO land on a 404 page instead of the dashboard. Password login is not affected.
>
> ## Steps to reproduce
> 1. Sign out.
> 2. Click "Continue with Google" and finish the Google flow.
>
> ## Expected
> Redirect to `/dashboard`.
>
> ## Actual
> Redirect to `/dashboard/undefined`, which shows the 404 page.
>
> +++ Agent notes
>
> `auth/redirect.ts` builds the path from `session.workspaceId`, which is unset for SSO sessions on first login.
>
> +++

## Sources

- uv: `.github/ISSUE_TEMPLATE/1_bug_report.yaml`, `2_feature_request.yaml` (astral-sh/uv)
- Ghostty: `.github/DISCUSSION_TEMPLATE/issue-triage.yml` (ghostty-org/ghostty)
- vLLM: `.github/ISSUE_TEMPLATE/400-bug-report.yml`, `500-feature-request.yml`, `750-RFC.yml` (vllm-project/vllm)
