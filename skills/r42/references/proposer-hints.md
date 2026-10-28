# Proposer hints

After42 gives each proposer an optional, different **diversity hint** so the pool is diverse (F7). Its hint texts are not published. The hints below are derived from what the published results show experts valued and from the composition analysis; each cites its source. Give each proposer job **one** hint, rotating through the list so a batch covers several.

Every proposer also gets the instructions under "Always" below.

## Always

- Propose toward the goal in `.r42/goal.md`; each question is an intermediate step toward it (F4).
- Ground every question in the pack: name the closest prior result and say what the question adds (F5, F24).
- Make a **short solution attempt** on each question to check and repair it before submitting; drop questions it settles or that stay ill posed (F7, F8).
- One core target per question. No assumption, parameter or layer that the phenomenon does not need (F24, F30).
- Say what **each outcome** would show (F26).
- Name a **concrete first step** worth doing on its own (F26, F33).
- Novelty and difficulty are not the goal; almost everything passes them (F1).
- Write in the question schema (`question-schema.md`).

## Hints

Composition hints (most AI questions are composition; experts still find some interesting, F22):

1. **Next step on a known object (A+1).** Take a recent result in the pack and ask the natural next question it leaves open, especially one that needs a new idea rather than a sharper estimate (F22, F26 "need for new ideas").
2. **Remove or weaken (A−B).** Drop or weaken one assumption of a known theorem and ask whether the conclusion survives, and if not, what replaces it (F22).
3. **Combine or transfer (A+B), only with a reason.** Bring a tool or phenomenon from one area to another only if you can answer "why is this particular combination intrinsically worth studying?" for specialists of both (F22, F24, F34).
4. **From a quantity to the full object.** A known optimal value, threshold or rate: ask about the structure behind it (the Gibbs measure, the set of near-optimal solutions, the geometry of the solution space) (Q:math-8, Q:math-17, Q:math-19, Q:math-22).
5. **From static to dynamic.** A known static structure (barrier, core, cluster): ask whether it governs dynamics or transport (Q:math-3, Q:math-16, Q:math-24).

Phenomenon hints (patterns praised on question cards, F27, F28):

6. **Isolate one mechanism.** Find the smallest model in which a single mechanism can be tested, and justify why it is the smallest new case (Q:math-6).
7. **Control everything but one effect.** Hold a mean, a vertex set or a marginal fixed so only one feature differs, and ask whether that feature alone changes the outcome (Q:math-15, Q:math-24, Q:physics-2).
8. **Robustness of generic behavior.** Does an arbitrarily weak perturbation (disorder, noise, slow change) change a sharp phenomenon? Prefer cases where a conjecture from another literature predicts the answer (Q:math-7, Q:math-12).
9. **Counterintuitive possibility.** Something that "should" have no effect: can it still change the global picture? (Q:math-20)
10. **Sharp structural change.** Is there a threshold where the structure changes qualitatively, and where is it? Either side of the answer should teach something (Q:math-17, F4 example goal).
11. **A precise prediction to test.** Derive a candidate law, scale or constant from a heuristic or known structure, and ask whether it holds (Q:math-13, Q:math-14, Q:math-8).
12. **Limit before method.** Before improving a particular method, ask what the best achievable performance is and how extra information changes it (Q:statistics-1).
13. **A cost model or local constraint.** Replace a global budget with a local one, or measure a non-standard cost, and ask for the tradeoff (Q:tcs-2, Q:tcs-3).

Beyond composition (rare and valuable, F23):

14. **New object, new line of inquiry.** Propose a new mathematical object or model that captures a phenomenon in the goal, the way percolation modeled flow through a random medium or Erdős–Rényi graphs modeled graph evolution. State the first question about it.

From the pack:

15. **Open question, sharpened.** Take an open question from `pack/open-questions.md` that is too vague or too hard as posed, and extract a precise, natural sub-question with a first step (F5, F26).

## Using hints across batches

Hint diversity is for coverage, not quotas. After a batch, check the composition mix of survivors (A+B / A−B / A+1 / other). If almost everything is A+1 or A+B, give later batches more of hints 6–11 and 14 (F22, F23).
