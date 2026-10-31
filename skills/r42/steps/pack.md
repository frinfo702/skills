# Goal and research pack

Runs when the notebook has no Goal or there is no pack record, or when the user wants to change the goal or refresh the pack.

## 1. The goal (with the user, never by a worker)

The goal is written by the researcher; it sets the direction every question serves (F4). Draft it with the user in conversation and save it as the Goal and Constraints sections of the notebook record (creating the notebook if this is the first use; `references/records.md`). It has two parts.

**Goal.** One short paragraph:

- What understanding or capability is the line of work after? Prefer understanding to gain over a method to tune: a goal phrased as a method invites "method before limit" questions (Q:statistics-1).
- Which kinds of questions matter (why a failure happens, what limits performance, what structure a model needs, what transfers across settings).
- What would count as progress, and why it matters beyond the benchmark.

After42's example sets the size and tone (F4): "The goal of the theory of phase transitions in random structures is to understand how a large number of local random rules produce qualitative change at the macroscopic scale ... The aim is to discover new phenomena, mechanisms, critical behavior, and universal laws, and to explain why they matter for real systems."

**Constraints.** A short list:

```markdown
- Target: <venue and deadline, if any>
- Compute: <per experiment> / <total until the deadline>
- Code: <repo path>, how to train and evaluate (one command each), the baseline it implements
- Agents run experiments: none | small (< <budget>) | up to <budget>
- Data available: <datasets and splits>
```

If the user gives only a topic word, reply with a draft in this shape and one question: is it right? Ask about constraints you cannot infer. Do not proceed on a goal the user has not confirmed. Record the goal and constraints as a Decision in the notebook.

Expectations to share when setting the goal, in one sentence, only if they change what the user should expect: After42 was validated on theoretical fields, and yields fall as fields depend more on experiments (F19–F21). r42 compensates by tying every question to cheap, decisive experiments; the yield still depends on how fast experiments run, so a fast proxy is worth setting up early (C13).

## 2. The pack (worker job)

The pack is the shared reference for every later agent (F5). In ML it also records mechanisms and baselines, so later steps can match problems to known solutions by structure rather than by keyword (E11). Run one job, step `pack` (the step most worth giving its own agent entry, e.g. `when = "long literature research"`):

```text
You are building a research pack for this goal:
<the notebook's Goal and Constraints>
<optional: seed papers, authors or repos the user named>

Search the literature (cito first, then web search and arXiv for surveys and recent papers, and
OpenReview for reviews) and write five files under <work>/pack/:
1. <work>/pack/summary.md   A literature summary: the main lines of work, the standard formulations,
   the main methods and what each relies on, the known failure modes, organized by theme.
   1500-3000 words.
2. <work>/pack/papers.md    An index: one entry per relevant paper:
   "- Authors (year), [title](link): main result in one or two sentences." Aim for 40-100 entries.
   Every link must be a real paper you found; never invent one.
3. <work>/pack/mechanisms.md  One entry per important method or idea, in this structure:
   problem type | bottleneck it addresses | mechanism | assumptions it needs (data scale, labels,
   resolution, compute) | known failure modes | metric it improved | source link.
   Include methods from neighbouring tasks that address the same bottlenecks as the goal.
4. <work>/pack/baselines.md  The standard benchmarks and splits, the strongest simple baselines
   with their reported numbers and code links, and known reproducibility issues.
5. <work>/pack/open-questions.md  Open questions stated in the literature, including limitations
   sections and reviewer comments, each with its source link and a note on partial progress.
Do not propose new questions. Finish by printing the five paths.
```

When the job finishes, skim the files and publish them as the pack record (one document with five sections, `references/records.md`). Post one short comment on the notebook: size, main themes, apparent gaps, links not verified. Reply in a few lines: the pack is ready, what it centres on, which baseline it suggests reproducing first, anything in it that surprised you, and one question: is anything central missing? Link the pack. The user's additions go straight into the pack record; rebuild `<work>/pack/` from it before later steps.
