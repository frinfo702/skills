# Portfolio review

The user wants an overall picture: what is in `.r42/`, what is strong, what to do next. Mostly inline work by you; one ranking pass if rankings are stale.

1. **Inventory.** Count questions by status and round; list jobs still queued or running (`r42.py status`); note the last ranking date and whether questions changed since.
2. **Rank if stale.** If no ranking covers the current versions, run `steps/judge.md` (ask first if it would start more than a couple of jobs).
3. **Write `.r42/reports/<date>-review.md`:**
   - Top questions by averaged rank, each with its one-line plain statement and Concrete first step.
   - Single-judge picks and largest-spread questions (F32), as candidates for the user's own judgment.
   - Composition mix of the portfolio (A+B / A−B / A+1 / other) and whether any question goes beyond composition (F22, F23).
   - Recurring weaknesses from Check notes, by checklist item (F24, F25, F29).
   - Questions where development stalled (kept twice with the same obstacle) and questions whose first step is ready to work on now.
   - Suggested next actions, each a concrete /r42 request (e.g. "deep-dive q007, 2 rounds", "propose with hints 6, 9 and 14").
4. **Reply** with the direct answer to what the user asked: where things stand in one or two sentences, the top one to three questions (one line each), and the one next step you recommend. Name the review file. If the review was asked for to decide what to pursue, ask one question: their verdict on the top question (`steps/feedback.md`; this is the input that most improves later rankings, F35).
