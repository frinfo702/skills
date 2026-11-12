---
name: audit-push
description: >-
  Deep review of everything about to be pushed, run once before each `git push`. Understands how the change works, then checks whether it actually solves the original request, traces the logic for bugs and breakage, looks up the real specs of the external services and APIs it touches, and audits security, developer workflow, and feature gates. Verifies every finding, keeps problems outside the push's responsibility in a separate list, and ends with a push or fix-first verdict. Reports only. Use when the user says "audit-push", "audit this", "deep review", "review before I push", "ready to push?", or is about to push. For the quick surface check after a single task, use review-diff instead.
---

# Audit Push

A push is where several tasks' worth of work leaves the machine. `review-diff` already checked each task for what is visible on the surface: tests, names, error handling, leftovers. This audit does what that check skips. It works out how the change behaves and whether that behavior is right.

Be thorough. Trace every path the change touches, and read whatever code you need to settle a question.

## What this push is responsible for

Review the code that this push adds or changes, measured against what the push set out to do.

You will find problems outside that: a bug in code the push didn't touch, a bottleneck that was already there, a design you would have done differently. Follow the same principle as `rule-of-one`. They are not this push's job.

- List them under "Outside this push" in the report, one line each.
- Don't investigate them further, don't rank them, and don't let them affect the verdict.

The line between the two: if the push introduced the problem or made it worse, it is in scope. If the problem would exist without the push, it is outside. Existing code that the push newly depends on is the border case. It is in scope when the new code is wrong because of it.

## Scope

```bash
git log --oneline @{u}..HEAD
git diff @{u}...HEAD
```

If the branch has no upstream, compare against the merge base with the default branch.

If the working tree has uncommitted changes, say so at the top of the report. They are not part of the push, and the user may think they are.

## Steps

### 1. Find the original request

Find what was actually asked for: the issue or ticket, the task description, the conversation, the PR description. Write it down in one or two sentences, in the requester's terms and not in the implementation's terms.

If you can't find it, ask the user. The audit can't judge a solution without knowing the problem.

### 2. Understand the mechanism

Read the full diff, the files it touches, the callers of what changed, and the code that the change calls. Then write a short description of how the change works, from input to output.

Do this before judging anything. If you can't explain how it works, keep reading.

### 3. Run the project's checks

Run the test suite, the type checker, and the linter that the project already has. Report failures with the output. If something can't be run, say which and why.

### 4. Review in passes

Do each pass separately, looking for one kind of problem at a time. If subagents are available, give each pass to a fresh one. Hand it the diff, the request, and your description of the mechanism. Don't hand it your suspicions.

**Does it solve the request?**

- Does the change fix the problem that was asked about, or a nearby one that was easier?
- Does it fix the cause or hide the symptom? Look for special cases, retries, and fallbacks that make the failure stop showing.
- Does it cover every case the request names, and the obvious ones it implies?
- Would it still work on real inputs, at real size, in the environment where it will run?
- Is there a clearly simpler or more direct way to do the same thing? Report this only when the difference is large.
- Is part of the request missing? Is there work that the request doesn't explain?

**Logic**

- Trace each changed path with concrete values, including the empty, zero, one, maximum, and malformed cases.
- Check conditions, boundaries, ordering, and what state is left behind when a step fails midway.
- Check concurrency: shared state, races, retries, and operations that run twice.
- Check changes made in different tasks that interact with each other.
- Check for bottlenecks that the change introduces: work repeated inside a loop, a query per item, quadratic behavior on input that can grow, blocking calls on a hot path.

**Breaking what already works**

A small change in one place often breaks something elsewhere. Trace the side effects.

- For each changed function, type, default value, config key, schema, file format, and serialized format, find everything that depends on it, across modules and packages.
- Check that existing callers, stored data, and saved files still work with the new behavior.

**Consistency with the outside world**

List every external service, API, library, CLI, file format, and protocol that the change uses or changes its use of. For each one, look up the actual specification. Don't work from memory.

- Use the documentation for the version this project uses. Read the version from the lockfile or the config.
- Check endpoints, parameters, types, units, required fields, authentication, pagination, rate limits, error responses, idempotency, and deprecations.
- Where the docs are unclear, read the library's source or make a harmless real call.
- Cite the source in the finding.

Check the inside in the same way: the change agrees with the project's own schemas, configs, other modules, and docs.

**Security**

- Injection, path traversal, unsafe deserialization, missing authentication or authorization checks, secrets written to logs, and untrusted input reaching a shell, a query, or a file path.
- Things that can't be unpushed: secrets, tokens, credentials, personal data, absolute local paths, large binaries, datasets, and generated files that should be ignored.

**Developer workflow**

Changes that stop other developers from building or running the project the way they do now:

- How or where secrets are read
- Environment variables renamed or newly required
- Ports and networking remapped
- A script or manual step that now has to be run for existing functionality to keep working
- Software that has to be installed by hand, outside the package manager

A new, optional way to run something isn't a finding. Neither is a dependency added through the package manager.

**Feature gates**

If the codebase puts features behind flags or internal-only checks, make sure the change doesn't expose a gated feature. Check every new code path that reaches gated behavior, including defaults, fallbacks, and error paths.

**Tests**

`review-diff` checked that tests exist. Here, check that they test the logic: would each test fail if the code were wrong? Look for tests that assert what the code does instead of what it should do, and mocks that replace the part that matters.

**ML experiments** (when the push contains experiment code)

- Train and test leakage, in splits and in preprocessing fitted on all the data
- Seeds fixed and recorded
- Metric computed the way the write-up says
- Baseline and proposed method run under the same conditions (data, budget, tuning effort)
- Committed configs matching the reported numbers

### 5. Verify each finding

Before reporting a finding, try to disprove it.

- **Finish the research.** Never report "X is a problem unless Y handles it" when you can read Y. Read Y.
- **Reproduce it** where you can: a failing test, a command, a traced example with concrete values.
- **Mark it** as Confirmed (you reproduced it or traced it end to end) or Plausible (you couldn't reproduce it and couldn't rule it out). Drop what you disproved.
- **Rank it honestly.** If findings are marked High when they aren't, the user stops trusting the report. Give a finding a high rank only after you have traced it end to end.
- **Intended breakage.** If the push sets out to remove a feature, a flag, or a safeguard, and the effect is limited to what was intended, don't report it. Do report it when the effect reaches further than the author is likely to realize.

### 6. Check the existing discussion

Do this only after your own audit is finished, so that you review with fresh eyes.

If the branch has a PR or MR, read its discussion with `gh` or `glab`. For findings from other reviewers or bots that you missed, verify them as in step 5 and include the valid ones, marked with who raised them.

### 7. Aggregate

Do this last. During the audit, you and the subagents take notes in the code's own terms. The user hasn't read the code, so those notes mean nothing to them. Rewrite every finding so that it can be understood without opening a file.

First, collect the findings from all passes, merge the ones that have the same cause, and order them by severity.

Then write each finding in three parts:

1. **Title.** One line in plain words that says what goes wrong.
2. **Explanation.** Two to five sentences. Follow the local flow of the program around the problem: what this piece of code receives, what it does with it step by step, at which step it goes wrong, and what happens as a result. Stay local. Don't explain the whole feature. End with whether the finding is Confirmed or Plausible, and how you checked.
3. **Location.** `path:line`, followed by a short excerpt of the lines in question in a code block. Three to ten lines is usually enough. When the problem spans two places (a caller and a callee, the code and the spec it contradicts), show both, and link the spec.

Rules for the explanation:

- Don't use identifiers from the code. Refer to things by their role: "the function that uploads one batch", not `push_batch()`. The identifiers appear in the excerpt, where a reader who wants them can find them.
- Do use technical terms where they are the precise word (race condition, idempotency, N+1 query, off-by-one, pagination cursor). Don't replace them with loose paraphrases.
- Write in the language the user is using.

The excerpt is the fallback. The user reads the code only when the explanation wasn't enough, so the explanation has to stand without it.

Write "How it works" and "Outside this push" by the same rules: roles instead of identifiers. An item under "Outside this push" stays one line with its location, and gets no excerpt.

## Report

````
## Request
<what was asked, in one or two sentences>

## How it works
<short description of the mechanism>

## Checks
<tests / types / lint: passed, failed, or not run>

## Does it solve the request?
<Yes / Partly / No, and why>

## High

### A failed upload is retried without an idempotency key, so records can be stored twice
The uploader sends each batch with a POST request and retries on a timeout. A timeout doesn't tell it whether the server received the batch. The request carries no idempotency key, so when the first attempt did arrive, the retry stores the same records a second time. Confirmed: the API reference says that a POST without the key is not deduplicated (<link>).

`src/upload.py:58`
```python
for attempt in range(MAX_RETRIES):
    try:
        return session.post(url, json=batch, timeout=10)
    except Timeout:
        continue
```

## Medium
## Low

## Outside this push
- `src/export.py:10` — the export reads the whole file into memory before writing it.

## Verdict
Push / Fix first: <the titles of the findings that block>
````

- **High**: the push doesn't solve the request, gives wrong results, loses data, breaks existing functionality, has a security problem, leaks a gated feature, or contains something that can't be unpushed. These block the push.
- **Medium**: a real problem that can follow in a later push.
- **Low**: worth knowing, and no action is needed.

Leave out an empty section. Don't pad the report with praise.

## What this skill doesn't do

It doesn't push, and it doesn't fix. The user decides what to fix. After a fix, re-run the passes that the fix touches.

## Credit

The passes on breaking existing functionality, developer workflow, feature gates, intended breakage, honest ranking, finished research, and the late check of the PR discussion follow the rubric of Cursor's `thermo-nuclear-review` skill ([cursor/plugins](https://github.com/cursor/plugins), `thermos`).
