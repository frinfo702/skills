---
name: review-diff
description: >-
  Quick surface review of the change one task just produced, run every time a task finishes. Compares the diff against the tests, the surrounding code, and the request, and reports what that comparison shows: missing tests and uncovered branches, poor or unconventional names, weak error handling, wrong choice between null and empty values, and leftovers. Doesn't trace logic and doesn't fix anything. Use when the user says "review this", "review-diff", "check what you just did", or after any task that edited files. For the deep review of everything about to be pushed, use audit-push instead.
---

# Review Diff

This review runs after every task, so it has to be fast. It covers what you can see by comparing things side by side, without working out whether the logic is right:

- the changed code against its tests
- new names against naming practice and against the names around them
- new error handling and absent-value handling against the surrounding code
- the diff against the request

Tracing logic, checking external APIs, and judging the design belong to `audit-push`. If you happen to see a bug while reading, report it, but don't go looking for one.

## Scope

Review the change this task made, and nothing older.

- Uncommitted work: `git diff HEAD` plus untracked files (`git status --short`).
- Already committed: the commits this task made (`git show`).

Read the diff from git, not from your memory of what you wrote. Read it as if someone else had written it.

Report only on lines that the task added or changed. A problem in untouched code is out of scope, even when it sits next to the change.

## Find the conventions first

Several checks below compare the change with how this codebase already does things. Before checking, look that up. Don't assume it.

- Read the project's instructions and config that state conventions: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and linter and formatter settings.
- For each kind of thing the diff adds (a function, a variable, a constant, a file, a test, an error, an optional field), find two or three existing examples nearest to it: first in the same file, then in the same directory, then in the same package.

When the codebase's convention differs from the general practice listed below, the codebase wins. When you report a deviation, cite the existing example that you compared against.

## Checks

### 1. Tests

- **No test at all.** For each function, method, or class that was added or whose behavior changed, search the tests for its name. Report the ones with no test.
- **Branches not covered.** List the branches in the changed code, then match each one to a test case. Report the branches with no case. Branches include:
  - each side of an `if`, `else`, `match`, or ternary
  - early returns and guard clauses
  - each `except` / `catch` and each raised error
  - loops over zero, one, and many items
  - boundary values in comparisons (`<` against `<=`, zero, negative, the maximum)
  - default arguments, and optional arguments passed as absent
- **Behavior changed, test didn't.** If existing behavior changed and no test changed, either the behavior had no test or the test doesn't check it.
- **Tests made weaker.** Tests deleted, skipped, or marked as expected failures; assertions removed or loosened; a test with no assertion; a test that mocks the thing it is testing.
- **Test placement and naming** that differ from the existing tests.

If this area of the project has no tests at all, say so once. Don't list every function.

### 2. Names

Check each name that the diff adds or changes, including files, tests, config keys, and CLI flags.

General practice:

- The name says what the thing holds or does. It doesn't repeat the type (`user_list`, `name_str`) or describe the implementation.
- Functions are verbs or verb phrases. A function named `get_…` or `is_…` doesn't modify anything.
- Booleans read as a yes-or-no statement (`is_`, `has_`, `can_`, `should_`) and are stated positively (`is_enabled`, not `is_not_disabled`).
- Collections are plural. Mappings name both sides (`user_by_id`).
- Quantities carry their unit (`timeout_ms`, `size_bytes`, `lr_per_step`).
- No vague names (`data`, `info`, `tmp`, `result`, `obj`, `handle`, `process`, `manager`, `util`) where a specific one exists.
- No abbreviations except the ones the field already uses. No single letters outside short loops and math.
- The wider the scope, the more descriptive the name.
- One word per concept: the diff doesn't mix `fetch`, `get`, and `load` for the same operation, or use one word for two different things.
- The name still matches after the change. A function whose behavior changed may need a new name.
- Casing follows the language's standard (PEP 8, Effective Go, and so on).

Codebase convention: compare each new name with the neighbors you found. Report it when it uses a different word for the same concept, a different prefix or suffix pattern, a different casing, or a different word order.

### 3. Error handling

- **Swallowed errors.** An empty `catch`, `except: pass`, or logging the error and carrying on when the caller needs to know about the failure.
- **Silent fallbacks.** A default value returned on failure (`except: return []`, `value or default`) so that the failure looks like a normal result.
- **Catching too much.** A bare `except`, `except Exception`, or a catch-all around code where only one specific error is expected.
- **Ignored results.** A returned error that isn't checked, a promise or coroutine that isn't awaited, an exit code that isn't read.
- **No handling where it is needed.** A new call that can fail (file, network, subprocess, parsing, user input) with no handling, where neighboring code handles the same kind of call.
- **Handling where it isn't needed.** A `try` around code that can't fail, or checks for states that can't occur.
- **Messages without context.** The message doesn't say which operation failed or with which input, or the original cause is dropped (`raise … from e`, `%w`).
- **Cleanup.** A resource opened in the diff that isn't released on the error path (`with`, `defer`, `finally`).
- **Style mismatch.** Failure is signalled differently from neighboring code: an exception where neighbors return an error value, or the reverse.

### 4. Absent and empty values

"There is no value" and "the value is empty" mean different things. Check that the diff picks the right one and stays with it.

- **Which one is meant.** An empty string, `0`, or `-1` used to mean "not set" where the language has `null` / `None` / an optional type.
- **Mixed representations.** Some paths return `None` and others return `""` (or `[]`, `{}`, `0`, `NaN`) for the same situation.
- **Truthiness checks that conflate them.** `if not x` or `x or default` where `0`, `""`, or an empty collection is a valid value.
- **Collections.** A function returns `null` for "no items". General practice is to return an empty collection.
- **Mismatch with the declared type or schema.** A type that says optional when the value is never absent, a function that returns `None` without saying so, a database column or API field whose nullability differs from what the code writes.
- **Serialization.** A missing key, an explicit `null`, and `""` are written or read as if they were the same.
- **Consistency with neighbors.** The same kind of field elsewhere in the codebase uses a different representation.

### 5. The request

- A part of the request that the diff doesn't address.
- A change in the diff that the request doesn't need (see `rule-of-one`).

### 6. Leftovers

- Debug prints, commented-out code, and `TODO` or `FIXME` notes added by this task
- Stubs, placeholder implementations, and hardcoded values standing in for real ones
- Code left over from an approach that was abandoned, unused imports and variables, stray files
- Comments, docstrings, and docs that describe the old behavior
- A counterpart that wasn't updated: a new environment variable missing from the example file, a new option missing from the docs, a changed signature with a caller left as it was
- An existing helper that does the same thing as newly written code

## What not to report

- Whether the logic is correct, beyond a bug you happened to see
- Design and architecture
- Formatting that a formatter or linter already enforces
- Anything in code the task didn't change

## Aggregate

Do this last, after all the checks. While checking, you take notes in the code's own terms. The user hasn't read the code, so those notes mean nothing to them. Rewrite every finding so that it can be understood without opening a file.

First, merge findings that have the same cause, and drop any finding that lacks a specific line or a specific thing you compared it against.

Then write each finding in three parts:

1. **Title.** One line in plain words that says what is wrong.
2. **Explanation.** Two to four sentences. Follow the local flow of the program around the problem: what this piece of code receives, what it does with it step by step, and at which step the problem appears. Then say why that is a problem. Stay local. Don't explain the whole feature.
3. **Location.** `path:line`, followed by a short excerpt of the lines in question in a code block. Three to ten lines is usually enough. When the finding compares the change with existing code, add the line you compared it against in the same way.

Rules for the explanation:

- Don't use identifiers from the code. Refer to things by their role: "the function that computes the wait before a retry", not `backoff()`. The identifiers appear in the excerpt, where a reader who wants them can find them. A naming finding is the exception, because there the name is the subject.
- Do use technical terms where they are the precise word (guard clause, truthiness, off-by-one, swallowed exception). Don't replace them with loose paraphrases.
- Write in the language the user is using.

The excerpt is the fallback. The user reads the code only when the explanation wasn't enough, so the explanation has to stand without it.

## Output

Group the findings under the check they belong to, and skip checks with nothing to report.

````
## Tests

### The retry limit has no test
The function that computes the wait before a retry first checks whether the attempt count has passed the limit, and raises an error if it has. The existing tests only call it with attempt counts below the limit, so this guard clause never runs under test. If the comparison were off by one, no test would fail.

`src/retry.py:31`
```python
if attempt > max_attempts:
    raise RetryExhausted(attempt)
```

## Absent and empty values

### "No host configured" is an empty string here and null elsewhere
When no host is configured, the retry code returns an empty string. The config loader returns null for the same situation. A caller that checks for null to detect a missing host treats the empty string as a real host name and tries to connect to it.

`src/retry.py:40`
```python
if host is None:
    return ""
```

Compared with `src/config.py:22`
```python
return None  # no host configured
```
````

If nothing is wrong, write `No findings.` and stop. Don't summarize the change, and don't list what looked fine.

## Fixing

Report only. Don't fix anything, even a one-line problem. The user decides what to fix.
