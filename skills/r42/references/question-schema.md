# Question file schema

One file per question during a session: `<work>/questions/<id>.md`. If the user keeps questions in a tool (`references/records.md`), the body there holds the sections from Question to First experiment, and experiment cards, the development log, check notes and feedback are comments; the coordinator rebuilds the file from them when the user points to it. IDs are short and stable (`q001`, `q002`, ...; a revision keeps its id). The sections follow After42's published cards (F15), adapted to empirical ML: a question is tied to a diagnosis and to the experiment that would decide it. Readers judge from the whole file: the question, the goal, and related work (F14).

```markdown
---
id: q007
title: Is the relation error caused by supervision that never requires relations?
status: developing      # candidate | developing | final | removed | user
research_status: open   # open | partial | solved  (F15)
round: 2                # development rounds completed
hint: 13                # proposer hint number, or "user"
composition: A+1        # A+B | A-B | A+1 | other  (F22)
origin: proposer job <job id> | user
first_cost: 4 GPU-h     # estimated cost of the first experiment
removed_reason:
---

# <title>

## Question
One plain-language sentence saying what this asks ("This asks whether ...").

The precise statement: the setting (task, data, models compared), the quantity measured, and
what counts as an answer ("Show or refute that ...", "Determine which of ... explains ...").

## Claim if it works
The sentence this would put in an abstract, and the figure that would show it.

## Diagnosis
The bottleneck this question targets, the evidence that it is a cause rather than a symptom,
and how confident we are. Questions without a diagnosis say so and make finding it the first step.

## Motivation
Why the field cares, in plain words. What it adds beyond the closest prior work.
What each outcome would show.

## Intuition
The expected answer (stated as a conjecture when the evidence supports one) and why.
Mark heuristics as heuristics.

## Related work
- Author (year), [title](link): what it shows, and how this question goes beyond it.
- If a mechanism is borrowed: the source, why the same bottleneck applies, and which of its
  assumptions (data scale, labels, resolution, compute) hold here.

## First experiment
The smallest experiment whose result would change what we do next: setup, proxy, budget,
prediction, readings ("if the gain vanishes when X is removed, then ...; if it persists, then ..."), and what evidence would make us drop the question.

## Experiment cards
### E1 <date> <short name>
- Decides: <which decision this experiment informs>
- Prediction: <written before running>
- Readings: <for each qualitatively different outcome (direction, size relative to seed noise,
  which hypothesis survives): what it would mean and what we do next. Not a numeric cutoff.>
- Setup: data/split, model, baseline (reproduced? numbers), seeds, budget, proxy or full
- Ran by: r42 job <id> | user
- Result: <filled after the run, with links to logs and figures>
- If unexpected: hypothesis | design | implementation, and the evidence for that attribution
- Decision taken: <what changed>

## Development log
### Round 1
- What the attempt found: diagnosis, literature, experiment results (link to <work>/solves/q007/r1-*.md).
- How the question changed, or why it was kept.
- Judges: <agent>: PREFER A|B, one line each. Accepted / rejected.

## Check notes
- <date> <checker agent>: items failed and what was done; prior-art links found.

## Researcher feedback
- <date>: the researcher's verdict and comments.
```

Rules:

- The Question section changes only through an accepted revision (unanimous judges, F11) or the checker's minimal, target-preserving repair (F12).
- Keep earlier versions: before applying an accepted revision, copy the old Question section into the Development log entry.
- In an experiment card, Decides, Prediction and Readings are never edited after the run (E7). A mistaken card is corrected by a new card that cites it. Acting differently from the Readings is allowed; the result comment says why.
- `status: user` marks a question the researcher brought; it is never removed by the filter, only flagged.
