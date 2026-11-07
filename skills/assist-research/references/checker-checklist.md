# Checker checklist

Used by the filter (after proposing) and by the fresh-agent check (after each development round). The checker must be a **fresh agent**, not the one that wrote or revised the question (F12).

The checker's job: **repair minimally while preserving the target, or remove** (F12). It does not improve the question's taste; that is the developer's and judges' job. It does fix defects that hide a good target.

## A. Validity (remove if not repairable)

From the published filter and check (F8, F12):

- [ ] **Prior answer.** Search the literature (the pack first, then the web) for the exact statement, special cases, and the obvious reformulations. If it is already answered, remove it. If a special case is known, cite it in Related work and make sure the question asks for more.
- [ ] **Known or duplicate.** Not the same as an open question already in the pack, an earlier proposal, or another question in `<work>/questions/`, up to rewording.
- [ ] **Too easy.** A short attempt (literature, a known trick, a quick argument) does not settle it. If one does, remove it (or record it as a lemma inside a parent question).
- [ ] **Ill posed.** The setting is defined (task, data and split, models compared, metric); the regime is explicit (scale, resolution, training budget); the statement says what would count as an answer ("show or refute that ...", "determine which of ... explains ..."). Repair if possible; remove if it stays ill posed.
- [ ] **Unsupported claims.** Every factual claim in Motivation, Intuition and Related work is either cited, derived in the file, or marked as heuristic or conjecture. Delete or soften what cannot be supported. Related-work entries link to real papers that say what the file claims.

## B. Motivation and formulation (repair; flag if not repairable)

The three recurring failures (F24) and the card-level reservations (F29):

- [ ] **Unnatural combination (routine A+B).** Write one sentence answering "why is this particular combination intrinsically worth studying?" If you cannot, flag it. Do not accept "they interact through mechanism X" as the answer unless the interaction itself is the phenomenon of interest (F34).
- [ ] **Engineered complexity.** For each assumption, parameter and layer of randomness: does removing it lose the phenomenon? If not, remove it. "With three layers of randomness combined, the central question no longer stands out."
- [ ] **Unclear contribution beyond prior work.** The file says what the question adds to the closest prior results. Flag it if it reads as a lemma inside someone else's project.
- [ ] **Unexplained specific choices.** Every specific choice (a number of arms, an exponent, a regime, a cost model) has a one-line reason, e.g. "three is the smallest new case" (Q:math-6, Q:math-16).
- [ ] **Inessential parameters or regimes.** If the claim does not depend on a stated condition, generalize or drop it (Q:math-1).
- [ ] **One-sided payoff.** State what each outcome would show. If one outcome would be "unremarkable" or a "quantitative refinement rather than a new phenomenon", flag it (Q:math-23, Q:math-25).
- [ ] **Confirms a familiar picture.** If the expected answer follows from known structure plus technical work, flag it (Q:math-3).
- [ ] **No conjecture.** If the evidence supports a definite expected answer, state it as a conjecture in Intuition (Q:math-2).
- [ ] **Method before limit.** If the question tunes one method before knowing the best achievable rate or the fundamental limit, flag it and suggest asking for the limit first (Q:statistics-1).
- [ ] **No entry point.** The First experiment section names a specific, affordable experiment worth doing on its own. If the full statement is very hard, a more focused first target is named (Q:math-10, F26, F33).

## C. Writing (always repair)

Defects found in strong and weak questions alike (F25):

- [ ] **Terminology.** Standard terms of the field, used correctly. Replace nonstandard phrasing.
- [ ] **Missing motivation.** Motivation explains why the field cares, in plain words, before any formalism. Expand compressed essential explanations.
- [ ] **Routine detail bloat.** Move routine computations out of Motivation and Question into Routes or delete them.
- [ ] **Readable statement.** One plain-language sentence before the formal statement says what the question asks ("This asks whether ...", as in R§3.1).

## D. Empirical soundness (repair; flag if not repairable)

For ML questions and their experiment cards. Use `ml-cards.md` here as a blind-spot list, not as requirements: flag only what applies.

- [ ] **Known fix.** A standard trick or a scale increase already removes the effect (search for it; C20). If so, it is "too easy" under A.
- [ ] **Symptom, not cause.** The Diagnosis names evidence that the target is a cause; if it only describes a failure, flag it and make the first experiment the one that would find the cause.
- [ ] **Decision-relevant experiment.** The first experiment's outcomes lead to different actions, and its prediction and readings are written (C14). Flag readings that are bare numeric thresholds without an interpretation.
- [ ] **Baseline.** The comparison is against a reproduced, equally tuned baseline, not numbers copied from a paper (C10).
- [ ] **Confounds.** Only the scientific variable changes; nuisance settings are re-tuned or held fixed (C11).
- [ ] **Variance.** Expected differences are larger than seed variance, or several seeds are planned (C12).
- [ ] **Proxy validity.** A proxy's ranking agreement with the full setting is checked or planned (C13).
- [ ] **Metric and leakage.** The metric measures the claim; train–test overlap and label errors are considered (C9).
- [ ] **Presence vs use.** Claims about what a model relies on rest on interventions, not only probes (C6, C7).
- [ ] **Within constraints.** The first experiment fits the compute and deadline in `goal.md`.
- [ ] **Card integrity.** No experiment card had its prediction or readings changed after the run (E7).

## Output

For each question checked, append to its file's Check notes: date, checker agent, each item that failed and what was done (repaired / flagged / removed), with links found during the prior-answer search. Set `status:` to `removed` (with reason) when removal is required. Never silently change the target: if a repair changes what is asked, it is a revision and goes through the judges instead.
