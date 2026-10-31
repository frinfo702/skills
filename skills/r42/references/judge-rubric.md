# Judge rubric

Judges do two jobs: a **pairwise vote** on each proposed revision, and a **ranking** of the surviving questions. Use the judges listed in config (`judges` in the agent configuration); mix model families. Each judge runs independently and never sees another judge's answer.

## Criteria

Criteria 1, 3, 4 and 5 adapt After42's published judge criteria (F30) and the gap the expert study found (F26, F33). Criterion 2 is for empirical ML, where ideas that sound good often fail when executed (E1).

1. **Simplicity.** Few essential components, one core target. Every dataset, module and setting earns its place.
2. **Grounded in a diagnosis.** It targets a cause of a known failure, with evidence that it is a cause rather than a symptom, or it makes finding that cause its first step. A borrowed mechanism comes with a reason the same bottleneck applies and its assumptions hold (E11, E12).
3. **Depth.** The answer would deepen understanding of the field or leave a reusable idea, not only a number. Prefer questions where **either outcome is informative**.
4. **Boldness and naturalness.** Challenges the standard framing where the evidence supports it. Not a routine A+B. The setting arises naturally in the field, and any specific choice (a dataset, a regime, a scale) is motivated. Ambition of the full question is not a negative.
5. **Decisive, affordable first experiment.** There is a first experiment that fits the constraints in the goal, whose outcome would change what the researcher does next, and that is worth doing on its own. Criteria 4 and 5 do not conflict: the whole question may be ambitious; the entry point must be cheap and clear.

Two checks against known misreadings (F34):

- Before calling a conjecture's mechanism "predictable", state what a proof would reveal and what a counterexample would reveal. If both teach something, that counts toward depth.
- Before calling a combination natural, answer as a specialist in *each* component would: "Why is this particular combination intrinsically worth studying?" A linking mechanism you can describe is not enough if neither field would care.

No numeric scores anywhere (F30). Rationales are prose.

## Pairwise vote (revision gate)

A revision is accepted only if **every** judge prefers it (F11). One dissent keeps the current version. Ties count as dissent.

```text
You are judging two versions of one research question toward this goal:
<goal.md>

Version A (current):
<question A, full file>

Version B (proposed revision):
<question B, full file>
What solving found this round: <solve summary>

Criteria (in order of weight; no numeric scores): Simplicity; Grounded in a diagnosis
(cause, not symptom; a borrowed mechanism's assumptions hold); Depth (either outcome
informative); Boldness and naturalness (ambition is not a negative); Decisive, affordable
first experiment within the goal's constraints.
Evidence from experiments outweighs how promising an idea sounds.
Before calling a mechanism predictable, say what a proof and a counterexample would each reveal.
Before calling a combination natural, say why a specialist in each component would care.
<if the researcher has given feedback (<work>/feedback.md): "How this researcher judged earlier questions:" + those entries verbatim>

Which version is the more interesting research question worth pursuing?
Answer with exactly one first line: "PREFER: A" or "PREFER: B". Then 3-6 sentences of rationale.
```

## Ranking

```text
Rank these research questions toward this goal, most interesting and worth pursuing first:
<goal.md>
<each question file, labeled by id>

Criteria as above. No scores. For every question, give its rank and 2-4 sentences of rationale
naming what makes it interesting or weak (cite the criterion). Output a markdown list:
"1. <id> — <rationale>".
<feedback examples as above>
```

Combine judges by **averaging ranks** (F31). Write the result to `<work>/rankings/<date>-<label>.md` with: the averaged order, each judge's rank per question, and the rationales.

Then flag, separately from the averaged order, the questions with the **largest rank spread** across judges and any question a single judge placed in its top quarter while the average did not. Model judges are mode seekers: they find consensus picks and miss single-taste picks, which are sometimes the ones that open new directions (F32). The researcher should see these, not just the consensus.

## Personalization

Condition judges on the researcher's **feedback on concrete earlier questions** (`<work>/feedback.md`), not on a stated-preferences profile. Feedback raised agreement with one expert's ranking from 0.26 to 0.42; stated preferences gave no gain, alone or on top of feedback (F35). If the user offers a preferences description, record it, but ask them to react to a few questions instead; that is what helps.

## Limits

Model rankings help the researcher prioritize; they do not decide (F36). Agreement with consensus is good (65–80% top-20 recall); agreement with any one person is not reliable (35–85%) (F31, F32).
