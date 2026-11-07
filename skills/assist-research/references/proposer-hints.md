# Proposer hints

After42 gives each proposer an optional, different **diversity hint** so the pool is diverse (F7). The hints below are adapted to empirical ML from what experts valued (F26–F28), from the composition analysis (F22, F23), and from known weaknesses of model-generated ideas (E1, E2). Give each proposer job **one** hint, rotating through the list so a batch covers several.

Hints are for coverage. They are not the improvement cards (`ml-cards.md`); proposers do not read those.

## Always

- Propose toward the goal in `<work>/goal.md`, within its constraints (deadline, compute); each question is an intermediate step toward the goal (F4).
- Ground every question in the pack: name the closest prior result and say what the question adds (F5, F24).
- Tie the question to a **diagnosis**: what bottleneck it targets and the evidence it is a cause, not a symptom. If there is no evidence yet, say so and make finding it the first experiment.
- Make a **short attempt** on each question (literature check, a short argument, a sketch of the decisive experiment) to check and repair it before submitting; drop questions it settles or that stay ill posed (F7, F8).
- One core target per question. No component, dataset or setting that the phenomenon does not need (F24, F30).
- Say what **each outcome** would show (F26).
- Name a **first experiment** whose result would change a decision, with an estimated cost within the constraints (F26, F33).
- Novelty is not the goal; almost everything passes it, and ideas that sound novel often fail when executed (F1, E1).
- Write in the question schema (`question-schema.md`).

## Hints

Composition (most questions; strong ones still exist, F22, E10):

1. **The failure a recent result leaves (A+1).** Take a recent strong method in the pack and ask about the failure or limitation it leaves, especially one that needs a new idea rather than more tuning.
2. **What is really doing the work (A−B).** Remove or weaken one component or assumption of a strong method and ask whether the gain survives; if not, what replaces it.
3. **Same bottleneck, borrowed mechanism (A+B), only with a reason.** Find another task where the same bottleneck was solved, matched by mechanism, not by task name. Say why the bottleneck is the same and check the mechanism's assumptions hold here (E11, E12).

Diagnosis and phenomenon:

4. **From the score to the failure structure.** Beyond the aggregate metric: which errors, on which cases, and what they have in common.
5. **Isolate one cause.** Find the smallest controlled setting (synthetic or counterfactual data) in which one suspected cause can be tested alone (Q:math-6 in spirit).
6. **Hold everything else fixed.** Fix compute, data or architecture so that only one factor differs, and ask whether that factor alone changes the outcome (Q:math-15).
7. **Robustness of a reported gain.** Does a small shift (another dataset, resolution, seed, tuning budget) remove a published improvement? Prefer cases where the answer would change what the field does.
8. **Counterintuitive possibility.** Something believed irrelevant changes results, or something believed essential does not (Q:math-20).
9. **Limit before method.** Before improving a method, ask what an oracle or upper bound achieves and how much headroom exists (Q:statistics-1).
10. **What scale does.** Does the gap close with more data, compute or model size? A gap that does not close is a stronger target.
11. **A precise prediction.** Derive a specific, testable prediction from a known mechanism and ask whether it holds (Q:math-14).
12. **A different formulation.** Would a different output representation or task formulation fit the structure of the problem better?
13. **Does the training signal ever require it?** Ask whether the property the goal cares about is ever needed to reduce the training loss, and what happens when it is.

Beyond composition (rare and valuable, F23):

14. **New task, benchmark or object.** Propose a new task, evaluation or controlled setting that captures the phenomenon in the goal better than existing ones, and state the first question about it.

From the pack:

15. **Open question, sharpened.** Take an open problem from `pack/open-questions.md` (including limitations sections and reviewer comments) that is too vague as posed, and extract a precise sub-question with a decisive first experiment (F5, F26).

## Using hints across batches

After a batch, check the composition mix of survivors (A+B / A−B / A+1 / other). Model ideas lean toward bridging and integrating methods (E2); if almost everything is A+B or A+1, give later batches more of hints 4–11, 13 and 14 (F22, F23).
