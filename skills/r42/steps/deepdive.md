# Deep-dive on one question

The user brings their own research question or hypothesis (or points to one they keep in a tool) and wants it developed. This is the attempt-refine-critique loop applied to a single question (F9–F12), without the propose stage.

1. **Capture it.** Write it to `<work>/questions/<id>.md` in the schema with `status: user`, `hint: user`. Fill Motivation, Diagnosis, Intuition and Related work from what the user said or the record they pointed to; leave unknown sections marked `TODO` rather than inventing content. Restate the question in one plain sentence and confirm it with the user before spending budget.
2. **If the user is stuck,** start from the evidence rather than the question: run `steps/interpret.md` on the experiments so far and say plainly which experiments changed no decision, which assumption everything rests on, and where the evidence is weakest.
3. **Goal and constraints.** If the user has not given them, ask (one or two sentences and the compute budget are enough here) and write them to `<work>/goal.md`. A full pack is optional: for a single question, a focused related-work search inside the first attempt is enough.
4. **Rounds.** Run `steps/develop.md` for this one question. Default 2 rounds, 2 attempts per round. Rounds are sequential (round 2 depends on round 1's check). Between rounds, show the user the experiment results; if they add their reading, pass it to the refine prompt.
5. **Report each round** directly: what the attempts found and how the question changed, or why it was kept (F17), in a few plain sentences; the current question in one sentence and its first experiment in one sentence. Votes and rationales stay in `<work>`; write the question to the user's tool only if they named one.
6. **The user decides.** If the user disagrees with a judge outcome, their call wins.

Multi-round deep-dives are expensive runs: confirm rounds, attempts per round, agents, parallelism and compute before starting.
