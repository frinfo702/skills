# Use researcher feedback

The researcher's reactions to concrete questions are the most valuable input the judges get: feedback on earlier questions improved a judge's agreement with an expert; a stated-preferences description did not (F35).

When the user reacts to a question, add an entry to `<work>/feedback.md` (it lasts for the session):

```markdown
## <date> <id>: <title>
- verdict: interesting | not interesting | unsure
- would pursue / suggest to a student: yes | no | maybe
- comment: <the user's words, verbatim where possible>
- question version: round <n>
```

Reply in one line that it will be used; do not discuss it unless asked. If the user named a destination for questions, also post the entry there as a comment on the question (`references/records.md`).

Ask with the expert's own questions, not criteria (F14): "Is this genuinely interesting? Would you pursue it, or suggest it to a student? Why?" Do not paraphrase the comment into rubric language; the specific reasons carry the taste.

If the user flags prior art or an error, re-run the check for that question (F42, F45).

In a later session, feedback exists only where the user keeps it. If they point to it (comments on question issues, a page), collect it into `<work>/feedback.md` before judging; the entries are passed verbatim to every judge prompt (`references/judge-rubric.md`, Personalization).
