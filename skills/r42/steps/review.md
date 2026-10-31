# Overview of a set of questions

The user wants an overall picture of the questions in this session (or the ones they point to in their tool): what is strong and what to do next. Mostly inline work; one ranking pass if rankings are stale.

1. **Inventory.** Count questions by status and round; note whether questions changed since the last ranking; list jobs still running.
2. **Rank if stale.** If no ranking covers the current versions, run `steps/judge.md` (ask first if it would start more than a couple of jobs).
3. **Think through** (in `<work>/review.md`):
   - Top questions by averaged rank, each with its one-line plain statement and First experiment.
   - Experiment cards waiting for the researcher.
   - Single-judge picks and largest-spread questions (F32), as candidates for the user's own judgment.
   - Composition mix (A+B / A−B / A+1 / other) and whether any question goes beyond composition (F22, F23).
   - Recurring weaknesses from Check notes, by checklist item (F24, F25, F29).
   - Questions where development stalled (kept twice with the same obstacle, or under the stall rule) and questions whose first experiment is ready to run now.
   - Time left to the deadline against the compute and steps the top questions need.
   - Suggested next actions, each a concrete /r42 request.
4. **Reply** with the direct answer: where things stand in one or two sentences, the top one to three questions (one line each), and the one next step you recommend. If the review was asked for to decide what to pursue, ask for their verdict on the top question (`steps/feedback.md`; this most improves later rankings, F35). Write the overview to the user's tool only if they named one.
