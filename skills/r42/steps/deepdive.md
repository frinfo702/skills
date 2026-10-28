# Deep-dive on one question

The user brings their own research question (or picks one from `.r42/questions/`) and wants it developed. This is the solve-refine-critique loop applied to a single question (F9–F12), without the propose stage.

1. **Capture it.** If it is new, write it to `.r42/questions/<id>.md` in the schema with `status: user`, `hint: user`. Fill Motivation, Intuition and Related work from what the user said; leave unknown sections marked `TODO` rather than inventing content. Restate the question in one plain sentence and confirm it with the user before spending budget.
2. **Goal and pack.** If `.r42/goal.md` is missing, ask the user for the goal this question serves (one or two sentences is enough here). A full pack is optional: for a single question, a focused related-work search inside the first solve job is enough.
3. **Rounds.** Run `steps/develop.md` for this one question. Default 2 rounds, 2 solve attempts per round. Rounds are sequential (round 2 depends on round 1's check).
4. **Report each round** directly: what solving found and how the question changed, or why it was kept (F17), in a few plain sentences; the current question in one sentence and its first step in one sentence. Votes, rationales and the check go in the question file; name it.
5. **The user decides.** If the user disagrees with a judge outcome, their call wins; record it with `steps/feedback.md`.

Multi-round deep-dives are expensive runs: confirm rounds, attempts per round, agents and parallelism before starting.
