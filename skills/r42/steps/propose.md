# Propose and filter

Needs `.r42/goal.md` and `.r42/pack/`. Produces `candidate` question files.

## Oversample

One proposal is almost never enough; experts found 3% of single-pass proposals interesting (F1). Generate a pool several times the number of questions you want to develop (F6). Default: `batches × per_batch = 4 × 5` per run of this step; the user's budget overrides it.

Submit one job per batch, step `propose`, each with a **different hint** from `references/proposer-hints.md` (rotate; F7). Reserve ids in advance so batches do not collide (batch 1 writes q001–q005, batch 2 q006–q010, ...).

```text
You are proposing research questions toward this goal:
<.r42/goal.md>
Read the literature summary .r42/pack/summary.md now; consult .r42/pack/papers.md and
.r42/pack/open-questions.md as needed, and search the literature yourself.
Read <skill-dir>/references/proposer-hints.md ("Always" section) and follow it.
Your diversity hint: <hint number and text>.
Avoid duplicating existing questions: <list of existing ids and titles>.

Propose <per_batch> questions. For each, make a short solution attempt (a few steps of the
argument, a small computation, or a literature check) to test whether it is well posed,
non-trivial and still open; repair or replace it if not.
Write each to .r42/questions/<id>.md using <skill-dir>/references/question-schema.md,
ids <range>, status: candidate, hint: <n>, and a one-paragraph Round 0 entry in the
Development log saying what the short attempt found.
```

## Filter

After all propose jobs succeed, submit one job, step `check`, using `steps/check.md` in **filter mode** with `--after` set to the propose job ids. It removes ill-posed, known, duplicate and too-easy candidates (F8).

Then rank the survivors (`steps/judge.md`) and pick the top N for development (default N = 8; the user's budget overrides). After42 developed up to 16 in parallel (F37). Mark them `developing`; leave the rest as `candidate`.

Report to the user: how many proposed, removed (by reason), kept, and the composition mix (F22).
