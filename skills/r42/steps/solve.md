# Attempt (solve)

The core idea of the method: a question improves when someone tries to answer it (F9, F44). In empirical ML, trying to answer means diagnosing what must be true, checking what is already known, and getting the smallest piece of evidence that would change a decision. Answering is not the goal; learning what the attempt reveals is.

One job per question per round, step `solve`. For two independent attempts per question, run two jobs with different `<k>`; give one the reasoning-and-literature angle and the other the experiment angle when experiments are allowed.

```text
You are attempting to answer this ML research question. Your budget: <time budget>, and
<compute: "no experiments" | "experiments up to <budget> each, in <code repo>, run as <how to run">>.
The point is to learn what the attempt reveals about the question, not only to finish.
Goal and constraints: <the goal and constraints from <work>/goal.md>
Question: <work>/questions/<id>.md  (read all of it, including its experiment cards and Development log)
Earlier attempts: <list of <work>/solves/<id>/*.md, or "none">. Build on them or try a new approach.
Literature: <work>/pack/ (mechanisms.md and baselines.md especially) and your own search.

1. Diagnose: what would have to be true for the question's intuition to hold? Which of those is
   the weakest link? Is the stated diagnosis a cause or a symptom?
2. Check the literature for an existing answer, a partial answer, or a known fix.
3. Design the smallest experiment whose outcome would change what we do next. Write its
   prediction and readings (what each qualitatively different outcome would mean and
   what we would do; not a numeric cutoff) before running. If every outcome would lead to the same action,
   design a different one. Prefer a reproduced baseline on a fixed small split and a fast proxy.
4. If experiments are allowed and it fits the budget, run it. If the project logs runs to
   MLflow, DagsHub or W&B, log this run there too, tagged r42.question=<id> and
   r42.card=<card name>, with the prediction in the run description. Before trusting a negative result,
   rule out an implementation bug (overfit a tiny set, check the baseline number).
   If not allowed or too expensive, leave it as a card for the researcher.
5. If a result is unexpected, list competing explanations (hypothesis wrong / design wrong /
   implementation bug) and the evidence for each before concluding.

Write <work>/solves/<id>/r<round>-<k>.md with these sections:
## Approach
## Diagnosis             what must be true, the weakest link, cause vs symptom
## Literature            existing answers, partial answers, known fixes, with links
## Experiment cards      one card per experiment, in the format of
                         <skill-dir>/references/question-schema.md (status: ran / for the researcher)
## Partial results       what you established, with enough detail to check
## Obstacles             where it breaks and why
## New structure         anything unexpected: a sharper comparison, a hidden cause,
                         a simpler setting that shows the phenomenon, a wrong intuition in the question
## If answered           the answer and how confident you are
## Suggested changes     how the question could be sharpened, redirected or corrected (do not edit the question file)
```

When the job finishes, the coordinator copies its experiment cards into `<work>/questions/<id>.md`, numbered in order, and shows cards marked "for the researcher" to the user with the prediction and readings. If the user named a destination for questions, a card is posted there before its run, and its result as a reply with the run link (`references/records.md`).

A full answer is a finding too: the question was too easy, or a known trick already fixes it (F8). The develop step decides what to do with it.

When the attempt is stuck (no diagnosis it believes, or an unexplained failure), the attempt may, after writing its own candidate moves, scan `<skill-dir>/references/ml-cards.md` for blind spots, citing any card it uses and why it fits.
