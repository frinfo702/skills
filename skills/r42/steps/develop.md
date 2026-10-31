# Develop (one round)

For each `developing` question, one round is: **attempt → refine → judge vote → check**, then rank all survivors (F9–F13). Two rounds is the published default; most of the gain usually comes in round one (F18).

Run the round without stopping. Start each job as soon as the jobs it needs have succeeded, and run the questions side by side (`references/jobs.md`):

```text
for each question q:
  S1, S2 = attempt (step solve)                            # steps/solve.md
  D      = refine (step develop), after S1, S2             # below
  J1..Jn = vote, one per judge (step judge), after D       # judge-rubric.md, pairwise
  C      = check (step check), after J1..Jn                # steps/check.md, round mode
R = ranking per judge, after every C                       # steps/judge.md
```

The C job applies the vote: it reads the judge outputs first (see `steps/check.md`).

While the round runs, hand experiment cards meant for the researcher to the user as soon as they exist.

## Stall rule

If a question has had **two rounds in a row whose experiments changed no decision**, it may not get a third round of probing. The refine job must either turn it into a method or intervention question with a decisive first experiment, or recommend removal. Tell the user which, in one line.

## Refine job

```text
You are developing one ML research question from what the attempts revealed.
Goal and constraints: <the goal and constraints from <work>/goal.md>
Question: <work>/questions/<id>.md (including its experiment cards)
This round's attempt records: <paths>. Literature record: <work>/pack/ and the Related work section.
<if the stall rule applies: "Stall rule: two rounds changed no decision. Choose between a method or
intervention question with a decisive first experiment, and recommending removal.">

1. Read the attempt records. List what they found: diagnosis, results, obstacles, new structure.
2. Explore <k, default 3> directions independently (as separate subagents if you can; otherwise
   write each in isolation before comparing). Typical directions (F17):
   - open the new direction the attempts revealed;
   - replace the target by a sharper comparison that isolates the cause;
   - turn the missing step between the evidence and the claim into the question;
   - correct the diagnosis the question was built on, if the evidence showed it wrong;
   - move from understanding to a fix: a question about an intervention the diagnosis suggests;
   - keep the question, if no direction beats it, and record the hardest step it now faces.
   Only if none of your directions convinces you: write that down, then scan
   <skill-dir>/references/ml-cards.md for blind spots and add a direction only if you can say why it fits.
3. Pick the most promising direction against <skill-dir>/references/judge-rubric.md criteria.
4. If you revise: write the revised full question file to <work>/questions/<id>.rev.md
   (same schema, same id, experiment cards copied unchanged, a new First experiment).
   If you keep: do not create that file.
5. Append to the Development log of <work>/questions/<id>.md a "### Round <r>" entry:
   what the attempts found, the directions considered, and the chosen change or why it was kept.
If the attempts fully answered the question, say so in the log and propose a harder, natural
successor as the revision, or recommend removal.
```

## Vote jobs

Run only if `<work>/questions/<id>.rev.md` exists (the job prompt says: "if the file does not exist, print NO REVISION and stop"). Each judge writes its answer to `<work>/questions/<id>.vote-<agent>.md` using the pairwise prompt in `references/judge-rubric.md`.

## After the round

When the round's jobs have finished, reply with one line per question: what changed and why, in plain words (e.g. "q007: revised; the 2 GPU-h proxy showed the error disappears when relations are required by the labels, both judges agreed"), then any experiment cards waiting for the user and any "Notable" items from workers. If the user named a destination for questions, the per-question record is the check's update (`steps/check.md`, Reporting). Attempt write-ups stay in `<work>`.
