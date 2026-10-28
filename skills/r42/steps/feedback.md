# Record researcher feedback

The researcher's reactions to concrete questions are the most valuable input in `.r42/`: feedback on earlier questions improved a judge's agreement with an expert; a stated-preferences description did not (F35). Record every reaction, even a one-word one.

Append to `.r42/feedback.md` (create it with a `# Researcher feedback` heading) one entry per question:

```markdown
## <date> <id>: <title>
- verdict: interesting | not interesting | unsure
- would pursue / suggest to a student: yes | no | maybe
- rank: <position, if the user ranked a set>
- comment: <the user's words, verbatim where possible>
- question version: round <n>
```

Mirror the entry under the question file's `## Researcher feedback`.

Prompt for the expert's own questions, not criteria (F14): "Is this genuinely interesting? Would you pursue it, or suggest it to a student? Why?" Do not paraphrase the user's comment into rubric language; the specific reasons are what carry their taste.

If the user flags prior art or an error, record it here and in the question's Check notes, and re-run the check for that question (F42, F45).

These entries are passed verbatim to every judge prompt (`references/judge-rubric.md`, Personalization).
