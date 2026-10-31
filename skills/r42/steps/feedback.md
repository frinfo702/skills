# Record researcher feedback

The researcher's reactions to concrete questions are the most valuable input r42 gets: feedback on earlier questions improved a judge's agreement with an expert; a stated-preferences description did not (F35). Record every reaction, even a one-word one.

Record it on the question's issue as one comment quoting the user, and set the `r42:interesting` or `r42:not-interesting` label (`references/records.md`). The comment:

```markdown
## <date> <id>: <title>
- verdict: interesting | not interesting | unsure
- would pursue / suggest to a student: yes | no | maybe
- rank: <position, if the user ranked a set>
- comment: <the user's words, verbatim where possible>
- question version: round <n>
```

Reply in one line that it is recorded, with the link; do not discuss it unless asked.

Prompt for the expert's own questions, not criteria (F14): "Is this genuinely interesting? Would you pursue it, or suggest it to a student? Why?" Do not paraphrase the user's comment into rubric language; the specific reasons are what carry their taste.

If the user flags prior art or an error, record it here and re-run the check for that question (F42, F45).

Feedback that is not about a specific question (a hunch, a view on a method, a decision, a disagreement with r42) goes to the notebook instead (Beliefs with source "user", Decisions, or Disagreements). If you disagree with the user's reaction, say why once, then record both views under Disagreements; the user's verdict is what goes here.

Before judging, collect these comments from the question issues into `<work>/feedback.md`; they are passed verbatim to every judge prompt (`references/judge-rubric.md`, Personalization).
