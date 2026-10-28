# Question file schema

One file per question: `.r42/questions/<id>.md`. IDs are short and stable (`q001`, `q002`, ...; a revision keeps its id). The sections follow After42's published cards (F15), with the first step made explicit because experts value it (F26). Readers judge from the whole file: the question, the goal, and related work (F14).

```markdown
---
id: q007
title: Can one junction sustain a critical contact process?
status: developing      # candidate | developing | final | removed | user
research_status: open   # open | partial | solved  (Erdős-problems convention, F15)
round: 2                # development rounds completed
hint: 6                 # proposer hint number, or "user"
composition: A+1        # A+B | A-B | A+1 | other  (F22)
origin: proposer job <job id> | user
removed_reason:         # set when status: removed
---

# <title>

## Question
One plain-language sentence saying what this asks ("This asks whether ...").

The precise statement. Define every object. Make quantifiers, regimes and limits explicit.
Say what counts as an answer: "Prove or refute that ...", "Determine ...".

## Motivation
Why the field cares, in plain words, before formalism. Why each specific choice
(model, regime, parameter) is the natural one. What it adds beyond the closest prior work.
What each outcome would show.

## Intuition
The heuristic picture and, when the evidence supports one, the conjectured answer.
Mark heuristics as heuristics.

## Related work
- Author (year), [title](link): what it proves, and how this question goes beyond it.

## Concrete first step
A specific first step that is worth doing on its own even if the full question stays open,
and the main obstacle after it. Known partial progress and possible routes.

## Development log
### Round 1
- What solving found: partial results, obstacles, new structure (link to .r42/solves/q007/r1-*.md).
- How the question changed, or why it was kept.
- Judges: <agent>: PREFER A|B, one line each. Accepted / rejected.

## Check notes
- <date> <checker agent>: items failed and what was done; prior-art links found.

## Researcher feedback
- <date>: the researcher's verdict and comments (mirrored in .r42/feedback.md).
```

Rules:

- The Question section changes only through an accepted revision (unanimous judges, F11) or the checker's minimal, target-preserving repair (F12).
- Keep earlier versions: before applying an accepted revision, copy the old Question section into the Development log entry.
- `status: user` marks a question the researcher brought; it is never removed by the filter, only flagged.
