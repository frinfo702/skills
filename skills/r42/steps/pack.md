# Goal and research pack

Runs when `.r42/goal.md` or `.r42/pack/` is missing, or when the user wants to change the goal or refresh the pack.

## 1. The goal (with the user, never by a worker)

The goal is written by the researcher; it sets the direction every question serves (F4). Draft it with the user in conversation and save `.r42/goal.md`. It answers:

- What understanding is the subfield after? (One or two sentences.)
- Which kinds of questions matter? (Why X happens, where a threshold lies, what structure appears, what is universal, ...)
- What would count as progress, and why it matters beyond the field.

Use After42's example as the model of size and tone (F4): "The goal of the theory of phase transitions in random structures is to understand how a large number of local random rules produce qualitative change at the macroscopic scale ... The aim is to discover new phenomena, mechanisms, critical behavior, and universal laws, and to explain why they matter for real systems."

If the user gives only a topic word, reply with a draft goal in this shape and one question: is it right? (Ask about scope only if the topic is too broad to draft from.) Do not proceed on a goal the user has not confirmed.

### Field-selection cautions

Mention a caution in the goal reply only when it changes what the user should expect (an experiment-heavy field, or one far from mathematics), in one sentence. Otherwise leave these out of chat:

- The method was validated on **theoretical** subfields where solving can rely on reasoning, computation and small experiments (F21). Yields were highest near mathematics (47% in phase transitions) and lowest in a methodology-driven statistics subfield (14%) and plasma physics (0%) (F19, F20).
- In experiment-heavy fields (e.g. empirical AI), solve attempts cannot run the real experiments, and the workflow does not gather new evidence from data (F21, F39). Expect lower yield; make the Concrete first step a small, cheap experiment or analysis the user can run, and treat proposals as hypotheses to test.
- A narrow, well-developed subfield with a rich open-problem literature gives the pack more to work with. A goal phrased as a method to tune (rather than understanding to gain) invites "method before limit" questions (Q:statistics-1).

## 2. The pack (worker job)

The pack is the shared reference for every later agent (F5). Submit one job, step `pack` (the step most worth giving its own agent entry, e.g. `when = "long literature research"`):

```text
You are building a research pack for this goal:
<.r42/goal.md>
<optional: seed papers or authors the user named>

Search the literature (cito first, then web search and arXiv for surveys and recent papers) and write three files:
1. .r42/pack/summary.md   A literature summary: the main lines of work, the central objects,
   the known results and the main techniques, organized by theme. 1500-3000 words.
2. .r42/pack/papers.md    An index: one entry per relevant paper:
   "- Authors (year), [title](link): main result in one or two sentences." Aim for 40-100 entries.
   Every link must be a real paper you found; never invent one.
3. .r42/pack/open-questions.md  Open questions and conjectures stated in the literature, each with
   its source link and a one-line note on known partial progress.
Do not propose new questions. Finish by printing the three paths.
```

When the job's event arrives, skim the three files and write `.r42/reports/<date>-pack.md`: size, main themes, apparent gaps, links you have not verified. Reply in two or three lines: the pack is ready, what it centres on, and one question: is anything central missing? Name the report file. Researchers can help build the pack (F5, F45); their additions go straight into these files.
