# Check

A **fresh agent** (never the proposer or developer of the question) audits questions against `references/checker-checklist.md`, repairs minimally, or removes (F8, F12). Step `check`.

## Filter mode (after proposing)

```text
You are a critic filtering candidate research questions. You did not write them.
Goal: <.r42/goal.md>
Questions: every .r42/questions/*.md with status: candidate.
Read <skill-dir>/references/checker-checklist.md and apply sections A, B and C to each.
For section A, search the literature for prior answers and make a short solution attempt
to test "too easy". Compare candidates with each other and with .r42/pack/open-questions.md
for duplicates; keep the stronger of two duplicates.
Set status: removed with removed_reason for questions that fail A and cannot be repaired.
Make minimal, target-preserving repairs to the rest. Append Check notes to every file.
Print a table: id, kept/removed, reason.
```

## Round mode (after a development round)

```text
You are checking one research question after a development round. You did not write it.
1. Apply the vote: if .r42/questions/<id>.rev.md exists, read every
   .r42/questions/<id>.vote-*.md. Only if every vote's first line is "PREFER: B", move the
   current Question section into the Development log entry for this round, replace the file
   with the revision (keep the log and notes), and record "accepted (unanimous)". Otherwise
   record "rejected (<who dissented>)" and keep the current version. Missing or malformed
   votes count as dissent. Then delete the .rev.md and .vote-*.md files, copying each vote's
   first line and a one-line rationale into the log.
2. Check the selected version against <skill-dir>/references/checker-checklist.md
   (sections A, B, C). Repair minimally while preserving the target, or set status: removed.
3. Increment round: in the frontmatter. Append Check notes.
Print: id, accepted/rejected, check result.
```

Questions with `status: user` are never removed; failures are flagged in Check notes and reported to the user.
