# Propose and filter

Needs the notebook's Goal and the pack (rebuilt into `<work>/pack/`). Produces candidate question files in `<work>/questions/`; only the ones chosen for development become records.

## Oversample

One proposal is almost never enough; experts found 3% of single-pass proposals interesting (F1). Generate a pool several times the number of questions you want to develop (F6). Default: `batches × per_batch = 4 × 5` per run of this step; the user's budget overrides it.

Run one job per batch, in parallel, step `propose`, each with a **different hint** from `references/proposer-hints.md` (rotate; F7). Reserve ids in advance so batches do not collide (batch 1 writes q001–q005, batch 2 q006–q010, ...).

```text
You are proposing research questions toward this goal:
<the notebook's Goal and Constraints>
Read the literature summary <work>/pack/summary.md and <work>/notebook.md now; consult
<work>/pack/papers.md, mechanisms.md, baselines.md and open-questions.md as needed, and search the literature yourself.
Read <skill-dir>/references/proposer-hints.md ("Always" section) and follow it.
Your diversity hint: <hint number and text>.
Avoid duplicating existing questions: <list of existing ids and titles>.

Propose <per_batch> questions. For each, make a short attempt (a literature check for an
existing answer or known fix, a short argument, a sketch of the decisive first experiment) to
test whether it is well posed, non-trivial, still open and affordable; repair or replace it if not.
Write each to <work>/questions/<id>.md using <skill-dir>/references/question-schema.md,
ids <range>, status: candidate, hint: <n>, and a one-paragraph Round 0 entry in the
Development log saying what the short attempt found.
```

## Filter

After all propose jobs succeed, run one job, step `check`, using `steps/check.md` in **filter mode**. It removes ill-posed, known, duplicate and too-easy candidates (F8).

Then rank the survivors (`steps/judge.md`) and pick the top N for development (default N = 8; the user's budget overrides). After42 developed up to 16 in parallel (F37). Mark them `developing` and create one issue per developing question (`references/records.md`; body = the question in the schema, label `r42:developing`). Candidates not chosen are not filed; list their titles in one collapsed block in the notebook comment below, so they can be revived.

Post one short comment on the notebook: how many proposed, removed by reason, kept, the composition mix (F22), and links to the new question issues. Reply with how many survived and which questions go into development, one line each with links. If a removed or low-ranked candidate struck you as interesting anyway, say so: single-taste picks are worth the user's look (F32).
