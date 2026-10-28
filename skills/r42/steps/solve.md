# Solve

The core idea of the method: a question improves when someone tries to solve it (F9, F44). Solving is not the goal here; learning what the attempt reveals is.

One job per question per round, step `solve` (a good step to route to a long-running agent). For two independent attempts per question, as in the published trajectories ("two attempts wrote out arguments", R§3.2), run two jobs with different `<k>`.

```text
You are attempting to solve this research question. Your budget: <budget, e.g. "about 30 minutes
of work">. The point is to learn what the attempt reveals about the question, not only to finish.
Goal: <.r42/goal.md>
Question: .r42/questions/<id>.md  (read all of it, including the Development log)
Earlier attempts: <list of .r42/solves/<id>/*.md, or "none">. Build on them or try a new approach.
Literature: .r42/pack/ and your own search.

Use reasoning, small computations or small simulations (python3) as useful.
Write .r42/solves/<id>/r<round>-<k>.md with these sections:
## Approach
## Partial results       what you proved or computed, with enough detail to check
## Obstacles             where the argument breaks and why
## New structure         anything unexpected: a sharper comparison, a hidden mechanism,
                         a simpler object that carries the phenomenon, a wrong intuition in the question
## If solved             if you fully solved it, the solution and how confident you are
## Suggested changes     how the question could be sharpened, redirected or corrected (do not edit the question file)
```

A full solution is a finding too: the question was too easy (F8). The develop step decides what to do with it.
