# Review an approach before running it

The cheapest point to catch a flaw is before the experiment: ideas that look promising often fail when executed (E1), and most of an experiment's cost is spent after the design is fixed. This action reviews the user's approach or experiment plan and returns concrete problems and fixes. It does not change the plan; the user decides.

## Inputs

The approach in the user's words or a document they point to, the goal and constraints, and the code if it exists. If the plan leaves out something the review needs (the baseline, the data split, what result is expected), ask for it in one question rather than guessing.

## Procedure

Work through these in order. Write your own reading of each before consulting anything else.

1. **The claim.** Restate in one sentence what the approach is meant to show and the sentence it would put in an abstract. If you cannot, that is the first finding.
2. **Diagnosis.** What bottleneck does it target, and is there evidence it is a cause rather than a symptom? If it borrows a mechanism from elsewhere: is the bottleneck really the same, and do the mechanism's assumptions (data scale, label quality, resolution, compute) hold here (E11, E12)?
3. **Prior art.** A short search (`steps/papers.md`, step 5) for the same approach or a known fix for the same problem, including whether scale alone already closes the gap (C20).
4. **The experiment.** Does it isolate the claim? Check: the scientific variable versus nuisance settings (C11); a reproduced, equally tuned baseline (C10); a metric that measures the claim, leakage and label quality (C9); expected effect size against seed variance (C12); a proxy whose ranking agrees with the full setting (C13); interventions rather than only probes for claims about what a model uses (C6, C7).
5. **Readings.** Write the prediction and, for each qualitatively different outcome, what it would mean and what would be done next (C14). If every outcome leads to the same next step, the experiment does not inform the decision; say what would.
6. **Cost.** Compute and time against the constraints, and the cheapest version that would still be informative.
7. **Blind spots.** Only now scan `references/ml-cards.md` and `references/checker-checklist.md` section D for anything you missed; add items that apply, with the card cited.

## Output

Lead with a one-line verdict in plain words (e.g. "Sound idea, but the planned comparison cannot separate A from B"). Then findings, most serious first, each with the fix:

```markdown
1. <problem> — <why it matters> — <concrete fix>
```

Then the experiment card for the recommended first run (`references/question-schema.md`), ready to use. If the user names a destination, write the verdict, findings and card there (`references/records.md`).

For a second opinion from another model family, run the review as a job on a different agent entry and report where the two disagree.
