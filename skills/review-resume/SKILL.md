---
name: review-resume
description: >-
  Review a resume or CV the way a hiring manager at a selective company does:
  concise, relevant, impact-first, and easy to skim. Use whenever the user asks
  for resume or CV feedback, shares a resume and asks "thoughts?" or "is this
  good?", wants bullets rewritten, is applying to a job, or asks for resume
  tips, even if they don't use the word review. Also use when drafting a resume
  from scratch or deciding what to cut.
---

# Review a Resume

A CV is not a description of a person. It is a short argument that this person has relevant experience and can communicate it well, made to earn one thing: a live conversation. The reviewer is skimming a mountain of CVs, so the argument has to land in seconds.

Four rules decide whether it does. They come from Wulfie Bain, who reviewed thousands of CVs while recruiting at BCG and hiring for OpenAI, and they hold across consulting, tech, and other industries.

## The four rules

### 1. Keep it concise

One page is the default. Relevance matters more than an arbitrary limit, so a second page is fine when every line earns its place. What concision really signals is prioritization and written communication: the candidate can decide what matters.

Look for: long summaries, repeated responsibilities, old jobs given equal weight to recent ones, formatting that exists to fill space.

### 2. Cut irrelevant experience

Every line should add signal for *this* role. Make the relevance obvious instead of hoping the reviewer connects the dots. High school achievements, unrelated side jobs, and hobbies usually go once there is real experience. Being proud of something is not the same as it being relevant.

Look for: experience that doesn't support the target role, unexplained career changes, skills lists that just repeat the bullets.

### 3. Show impact, not action

A list of actions says what the person did. Impact says why it mattered. Quantify where possible: time saved, latency reduced, revenue gained, users reached, cost cut, quality improved.

Weak: "Re-architected an agent."
Better: "Re-architected the agent, cutting latency by 2s and raising customer satisfaction."

If the person is in sales, talk revenue. If they are an engineer, talk reliability, speed, or scale. If they are a researcher, talk findings and what changed because of them.

Numbers need to be real. Never invent a metric to make a bullet look stronger; ask the candidate for it or leave a clear placeholder.

### 4. Make it easy to skim

The reviewer will not read every word. Put the strongest evidence first under each experience, bold the few things that should survive a five-second scan, and keep bullets short enough to take in at a glance. A clean structure is itself evidence of clear thinking.

Look for: buried wins, uniform formatting with no emphasis, dense paragraphs, bullets that all start the same way, dates or titles that are hard to find.

## How to review

1. **Get the target.** If the role is obvious from the CV, state it and proceed. If it isn't, ask one question before reviewing.
2. **Do the ten-second test.** Read only the top third. What role does this person appear to want? What is the single strongest piece of evidence? If either answer is unclear, that is the first finding.
3. **Check all four rules.** For each finding, quote the exact line and give a concrete rewrite. "Add more metrics" is not actionable; "this bullet needs a number for time saved" is.
4. **Do not invent facts.** You can restructure, tighten, and suggest what metric to add. You cannot know the candidate's revenue, latency, or team size. Mark unknowns as `[metric?]` and ask.
5. **Prioritize.** Give the three to five changes that most improve the odds of an interview, not an exhaustive line edit. If the CV is strong, say so and keep the review short.

## Output format

Use this structure, and keep the review as skimmable as the CV should be:

```
## Verdict
One or two sentences: would this earn a conversation for the target role, and why?

## What works
- The strongest evidence, quoted.

## Fix first
1. **Rule** — quote the line.
   Why it fails: one sentence.
   Rewrite: the improved line.

## Quick wins
- Smaller edits worth doing.

## Missing
- Facts or sections the candidate needs to supply (metrics, role, dates).
```

If the user asks for tips rather than a review, read `references/checklist.md` and give them the short version in your own words. The checklist is written so a person can use it without an agent.

## Source

Wulfie Bain (@wulfie_bain_), "Tips for people applying to open/upcoming roles on my team at @OpenAI: part 3, CV edition." The four rules are his; the review procedure is an adaptation.
