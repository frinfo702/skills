---
name: make-research-slides
description: >-
  Plan, build and review slide decks for research and development talks: lab seminars, conference talks, paper reading sessions, progress reports, and design or PR walkthroughs. Covers the storyline, a noun-phrase title and a one-line lead per slide, how to write slide text, the evidence on each slide, where numbers and explanations go, text sizes, and assembling the deck in Typst. Use together with make-research-figure (what each figure shows) and draw-typst-figure (drawing it). Trigger even when the skill is not named, e.g. "スライド作って", "発表資料", "ゼミ発表", "輪読の資料", "進捗報告のスライド", "学会発表", "このスライドどう？", "/make-research-slides".
---

# make-research-slides

A talk moves one idea from the speaker to the audience. Each slide names its topic in the title, says in the sentence right under it what the figure is, and shows the evidence; the speaker supplies the rest. Templates are in `references/templates.md`.

## Division of labor

| Where | What goes there |
|---|---|
| **Slide text** (title, lead line) | what each figure is and how its evidence was obtained, definitions, the takeaway. Not a reading of numbers the figure already shows. Written in the talk's language; edited in the deck. |
| **Figure image and tables** | only what is needed to read them: names, axis labels, legends, data, table headers and cells. English. No title, caption, notes or highlighted numbers (make-research-figure). |
| **Speaker** | explanations, caveats, the story between slides. |
| **Backup slides** | details for Q&A: full tables, setups, ablations. |

When a figure needs a sentence to be understood, the sentence goes in the slide text or the speaker's mouth, not into the image.

## Workflow

1. **Frame.** Ask for (or infer) the audience, the length, the setting (seminar, conference, progress report) and the one takeaway sentence. Everything else serves that sentence.
2. **Outline first.** Write the deck as a list of slides, each a title, a lead and the point the slide makes, and check that the points alone tell the whole story. Show this outline before building anything; restructuring a list is cheap, restructuring slides is not. Rough budget: one slide per minute, fewer when slides carry dense figures.
3. **Evidence per slide.** For each claim, pick what proves it: a diagram, a plot, a small table, an example, a demo. A slide without evidence is a speaker note; a slide with two pieces of evidence for two claims is two slides.
4. **Figures.** Make them with make-research-figure and draw-typst-figure, at the slot size of the deck (`references/templates.md`), so they are placed at 100%.
5. **Assemble** in Typst (default) or hand the user the outline, the slide text and the figure files for Keynote, PowerPoint or Google Slides (figures as SVG, or PNG at 200+ ppi).
6. **Check** with the checklist, by rendering every slide to PNG and looking at it.

## Storylines

**Research talk / conference talk.** Title → the whole talk in a few sentences → the problem and why it matters → the key idea, within the first few minutes → how it works → evidence → limitations → the takeaway. Give intuition and examples before definitions; leave details to the paper (Peyton Jones).

**Paper reading (輪読).** What the paper claims and shows, in a few sentences → the setting and the gap → the method in one picture → the evidence that supports the claim and what it does not show → what it means for our work.

**Progress report.** What changed since last time → the result, with numbers → what it means → the decision or help needed → next steps.

**PR / design walkthrough.** The problem in the current system → before vs. after → the evidence (benchmarks, tests) → what is not covered and the follow-ups.

The last slide restates the takeaway; it stays on screen during questions, so it is never only "Thank you" or "Questions?".

## Slide rules

- **Title, lead, evidence.** The title is a noun phrase naming what the slide is about. Directly under it, one line, the lead, says what the figure is. The body is visual evidence, not bullets.
- **The lead says what the figure is.** It first names the kind of figure (a training or inference pipeline, a data flow, an experimental comparison, an example) and then what it depicts. For a result: what was run, on what, compared with what, and which quantity is shown. For a diagram: the system as a whole, then which highlighted part is new or changed. A lead that states only the change leaves the audience unsure what the picture as a whole is; a lead that reads values off the figure repeats what they can already see. How to read the result, and which number matters, is said by the speaker; the opening and closing slides state the takeaway in words.
- **One idea per slide** (Naegle 2021). Split complex ideas across slides and build them up step by step.
- **Distracted-viewer test.** Someone who looks up for three seconds knows what the figure is from the title and the lead, and sees the point in the highlighted part of the figure.
- **Numbers stay where they are.** Data values live in the figure or table; no annotations or highlighted numbers are added to the image, and slide text does not read them back.
- **Text.** Title about 30 pt, lead line 24 pt, nothing below 18 pt. A slide with a figure has no text besides the title and the lead line, or at most three short bullets instead of a figure.
- **Calm color.** Black text and white, black-outlined boxes for everything that is not the point (not gray fills), one focus color (deep blue) for ours or the new thing, and the same meanings in figures, tables and text (palette in make-research-figure `references/specs.md`). No red for emphasis: next to blue or green it reads as "the bad one"; red means something bad.
- **Practical.** 16:9, slide numbers, high contrast, the deck's font covers the talk's language (Latin font first, then a Japanese font).

## Writing slide text

Slide text follows the same density rules as prose (mitigate-prose-density), compressed for slides.

- **The title slide is a name.** The talk title is a noun phrase: the paper's title, or the system or topic the talk is about, not a sentence. Under it only the speaker, the venue and the date. No subtitle, tagline or catchphrase and no decorative rules; the claim belongs on the next slide.
- **Open with the conclusion.** Right after the title slide, one slide states the whole talk in a few sentences: the problem, what was done, what it shows. The audience gets the shape of the talk there, and every later slide is evidence for it. No agenda slide listing section names.
- **Titles are specific noun phrases.** A title names what the slide is about, specifically enough to tell slides apart: the object (which method, system or component) and the aspect shown (which measurement, which comparison, which mechanism). Not a sentence (the lead does that), and not a bare section label (background, method, results, numbered results, summary). No label prefixes before a colon and no slides that carry only a name, such as section dividers or a "Backup" page.
- **One register.** Titles and leads are noun phrases; other slide sentences are in plain form (だ・である), as full sentences. Do not mix です・ます and だ・である in one deck.
- **The lead is a noun phrase, not a sentence.** It ends on the kind of figure it names, without a copula (no だ, である, です). What is new follows as a second short fragment, also without a copula, rather than a clause joined on with "で". Side remarks and caveats are said aloud. It does not repeat what the figure's own labels say (axes, legend). A slide without a figure, such as the opening summary or the closing takeaway, has no lead; its text is the content itself, never a description of that text.
- **Few bullets.** Bullets only for truly parallel items, at most three, each a sentence, never "**ラベル**：…".
- **No parenthetical asides.** "+11.4%（相対）" becomes "相対で 11.4% 高い". Needed information goes into the sentence; the rest is dropped or said aloud.
- **Name concepts, not chunks.** Name what the field names (prefix caching, SCR) and define it once in a sentence. Do not invent names for parts of the talk ("3 つの方法", "結果 2").

## Reviewing a deck

Render the slides and read them. Report:
1. The story the deck tells, in two or three sentences. If it does not hold together, that is the first finding.
2. Per slide, only where something is wrong, by impact: a title that is a bare label or a sentence, a missing or vague lead, a lead that names only the change or reads values off the figure instead of saying what the figure is, a slide with two ideas or no evidence, explanatory text or numbers inside figures, Japanese inside figures or tables, label-prefixed bullets or parenthetical asides, unreadable sizes, colors that break their meaning. Each with a concrete fix.

## Checklist

- [ ] Title slide: a noun-phrase title plus speaker, venue, date; no subtitle or decoration
- [ ] One takeaway sentence; the slide after the title and the last slide state it
- [ ] Every slide: a specific noun-phrase title; no bare labels, dividers or agenda slides
- [ ] Every slide with a figure: a noun-phrase lead saying what the figure is, without repeating the figure's labels; slides without a figure have no lead
- [ ] One idea and one piece of evidence per slide
- [ ] No numbers read back from the figure; explanations in slide text or speech, without label prefixes or parenthetical asides; figures and tables are English and hold no titles, captions or notes
- [ ] Calm palette: black on white plus one focus color with fixed meanings; no gray fills; no red emphasis
- [ ] Figures placed at 100% of the slot; nothing below 18 pt
- [ ] Every slide rendered and checked; nothing overflows onto an extra page
- [ ] Backup slides for expected questions
