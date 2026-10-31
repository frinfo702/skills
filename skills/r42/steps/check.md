# Check

A **fresh agent** (never the proposer or developer of the question) audits questions against `references/checker-checklist.md`, repairs minimally, or removes (F8, F12). Step `check`.

## Filter mode (after proposing)

```text
You are a critic filtering candidate research questions. You did not write them.
Goal: <the notebook's Goal and Constraints>
Questions: every <work>/questions/*.md with status: candidate.
Read <skill-dir>/references/checker-checklist.md and apply sections A, B, C and D to each.
For section A, search the literature for prior answers and known fixes, and make a short attempt
to test "too easy". Compare candidates with each other and with <work>/pack/open-questions.md
for duplicates; keep the stronger of two duplicates.
Set status: removed with removed_reason for questions that fail A and cannot be repaired.
Make minimal, target-preserving repairs to the rest. Append Check notes to every file.
Print a table: id, kept/removed, reason.
```

## Round mode (after a development round)

```text
You are checking one research question after a development round. You did not write it.
1. Apply the vote: if <work>/questions/<id>.rev.md exists, read every
   <work>/questions/<id>.vote-*.md. Only if every vote's first line is "PREFER: B", move the
   current Question section into the Development log entry for this round, replace the file
   with the revision (keep the log and notes), and record "accepted (unanimous)". Otherwise
   record "rejected (<who dissented>)" and keep the current version. Missing or malformed
   votes count as dissent. Then delete the .rev.md and .vote-*.md files, copying each vote's
   first line and a one-line rationale into the log.
2. Check the selected version against <skill-dir>/references/checker-checklist.md
   (sections A, B, C, D), including its experiment cards. Repair minimally while preserving the target, or set status: removed.
3. Increment round: in the frontmatter. Append Check notes.
Print: id, accepted/rejected, check result.
```

## Recording

After each check job, write back to the records (`references/records.md`): update the question issue's body to the selected version; post one comment with the outcome ("revision accepted (unanimous)" or "rejected (codex preferred A)", what the check repaired or flagged, prior-art links); close the issue with the reason when a question is removed. Keep it to a few lines.

Questions with `status: user` are never removed; failures are flagged in Check notes and reported to the user.
