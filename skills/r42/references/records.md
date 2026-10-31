# Writing to external tools

r42 is stateless. It writes outside the reply only when the user names a destination for an output ("put the plan in Linear", "post the card on issue #12", "log it to MLflow"). There is no default destination and no mapping kept anywhere.

## Writing

- Write for a person skimming: the conclusion or decision first in one or two sentences, then links (run, PR, paper, issue). Rationale of more than a few lines goes in a collapsed `<details>` block or stays out.
- No transcripts, tool output or worker write-ups.
- One entry per event (a plan, an experiment card, a result, a review), not one per job.
- Writing to a tool the user named is authorized for that output. Anything else outward (a new issue the user did not ask for, a new label set, a new project) needs a one-line confirmation.

## Shapes that fit common tools

Use these when the user picks the tool; follow the user's own conventions where they have them.

| Output | GitHub | Linear / Notion | MLflow / DagsHub / W&B |
|---|---|---|---|
| Plan or approach review | an issue or a comment on one | an issue, document or page | — |
| Question | one issue per question; body = the question in the schema; comments = rounds, checks, feedback | one issue per question | — |
| Experiment card | a comment posted **before** the run (Decides, Prediction, Readings); the result as a reply with the run link. Comment edit history shows the card was not rewritten | a comment on the issue, same order | the run tagged `r42.card=<name>`, prediction in the run description |
| Experiment code | a branch and PR, linked from the card | linked from the issue | the run's git commit |
| Results summary, ranking | one comment | one comment | — |

## Reading

When the user points to a tool ("my plan is in Linear issue ABC-12", "runs are in MLflow experiment X"), read that and use it as input for this session only.
