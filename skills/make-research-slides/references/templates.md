# Templates

## Typst deck

Every content slide is a title (noun phrase), a lead (noun phrase: what the figure is) and the evidence. Figures are compiled separately (draw-typst-figure) at the slot size, 12.33 × 4.9 in, and placed as PDFs. Titles and leads stay here, editable.

```typst
#let ink = rgb("#22272E")
#let muted = rgb("#8B929A")
#let focus = rgb("#004488")    // the one emphasis color; same meaning as in the figures
#let slide-font = ("Inter", "Hiragino Kaku Gothic ProN")   // Latin first, then Japanese; check `typst fonts`

#set page(width: 13.333in, height: 7.5in, margin: (x: 0.5in, top: 0.35in, bottom: 0.45in),
  footer: context align(right, text(size: 14pt, fill: muted, counter(page).display())))
#set text(font: slide-font, size: 24pt, fill: ink, lang: "ja")
#set par(leading: 0.6em)

#let title(body) = block(height: 1.0in, width: 100%, spacing: 0pt,
  align(left + horizon, text(size: 30pt, weight: "bold", body)))
#let lead(body) = block(height: 0.7in, width: 100%, spacing: 0pt,
  align(left + top, text(size: 24pt, body)))

// Title (noun phrase) + lead (noun phrase) + evidence in the 12.33 x 4.9 in slot.
#let slide(head, line, fig: none, body: none) = {
  title(head)
  lead(line)
  if fig != none { align(center, image(fig, width: 12.33in, height: 4.9in, fit: "contain")) }
  if body != none { body }
  pagebreak(weak: true)
}

// Title slide: a noun-phrase title, then speaker · venue · date. No subtitle, tagline or rules.
#let title-slide(title, who) = {
  set align(left + horizon)
  text(size: 40pt, weight: "bold", title)
  v(0.5in)
  text(size: 20pt, fill: muted, who)
  pagebreak(weak: true)
}

#title-slide[Context Language Models][Name · Lab seminar · 2026-11-15]

#slide([<title: noun phrase>],
  [<lead: what the figure is>],
  fig: "fig-bench.pdf")
```

Build and check:

```sh
typst compile deck.typ deck.pdf
typst compile deck.typ 'deck-{p}.png' --ppi 60   # one PNG per slide; more PNGs than slides = overflow
```

A lead that wraps to more than two lines pushes the slide onto an extra page; shorten the sentence rather than shrinking the figure.

## Outline (before building)

```markdown
Talk: <setting>, <length> min, audience: <who>
Takeaway: <one sentence>

1. <title (noun phrase)> | <lead: what the figure is> | <point (said aloud)> | evidence = <figure / table / example>
2. ...
Backup: <expected questions → slide>
```
