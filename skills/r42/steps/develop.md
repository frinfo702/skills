# Develop (one round)

For each `developing` question, one round is: **solve → refine → judge vote → check**, then rank all survivors (F9–F13). Two rounds is the published default; most of the gain usually comes in round one (F18).

Run the round without stopping. Start each job as soon as the jobs it needs have succeeded, and run the questions side by side (`references/jobs.md`):

```text
for each question q:
  S1, S2 = solve (step solve)                              # steps/solve.md
  D      = refine (step develop), after S1, S2             # below
  J1..Jn = vote, one per judge (step judge), after D       # judge-rubric.md, pairwise
  C      = check (step check), after J1..Jn                # steps/check.md, round mode
R = ranking per judge, after every C                       # steps/judge.md
```

The C job applies the vote: it reads the judge outputs first (see `steps/check.md`).

## Refine job

```text
You are developing one research question from what solution attempts revealed.
Goal: <.r42/goal.md>
Question: .r42/questions/<id>.md
This round's solve records: <paths>. Literature record: .r42/pack/ and the Related work section.

1. Read the solve records. List what they found: partial results, obstacles, new structure.
2. Explore <k, default 3> directions independently (as separate subagents if you can; otherwise
   write each in isolation before comparing). Typical directions, from observed trajectories (F17):
   - open the new direction the attempts revealed (e.g. how found pieces combine);
   - replace the target by a sharper comparison that shows the phenomenon more clearly;
   - turn the missing step between known results and the goal into the question;
   - correct the intuition the question was built on, if the attempts showed it wrong;
   - keep the question, if no direction beats it, and record the hardest step it now clearly faces.
3. Pick the most promising direction against <skill-dir>/references/judge-rubric.md criteria.
4. If you revise: write the revised full question file to .r42/questions/<id>.rev.md
   (same schema, same id). If you keep: do not create that file.
5. Append to the Development log of .r42/questions/<id>.md a "### Round <r>" entry:
   what solving found, the directions considered, and the chosen change or why it was kept.
If the attempts fully solved the question, say so in the log and propose a harder, natural
successor as the revision, or recommend removal.
```

## Vote jobs

Run only if `.r42/questions/<id>.rev.md` exists (the job prompt says: "if the file does not exist, print NO REVISION and stop"). Each judge writes its answer to `.r42/questions/<id>.vote-<agent>.md` using the pairwise prompt in `references/judge-rubric.md`.

## After the round

When the round's jobs have finished, write `.r42/reports/<date>-round<r>.md`: per question, what solving found, revised or kept, the votes with rationales, the check result. Reply with one line per question: what changed and why, in plain words (e.g. "q007: revised; solving showed the jump comes from the 3-core, both judges agreed"). Then the report path. The full trajectory stays in the question files.
