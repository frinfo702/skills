# Templates

Versions as of 2026-11; check for newer ones (SKILL.md) and keep cetz in step with cetz-plot.

## theme.typ

```typst
// Shared look for every figure in one talk or paper. Change here, not per figure.
// Calm palette with fixed meanings (make-research-figure references/specs.md).
#let ink = rgb("#22272E")       // text, lines
#let muted = rgb("#8B929A")     // secondary text, axes
#let faint = rgb("#E3E6EA")     // grids, inactive borders
#let focus = rgb("#004488")     // ours / the new thing / the change: one per figure
#let second = rgb("#DDAA33")    // the second series / a second thing to track
#let third = rgb("#44AA99")     // further series that must be told apart
// Neutral parts are white boxes with ink outlines; gray (muted) only for axes, grids, secondary text, at most one series.
#let problem = rgb("#BB5566")   // only for something bad: failure, overflow, removed
#let tint(c) = c.lighten(85%)
#let font = "Inter"           // check `typst fonts`; for papers use the paper's family

// Slide figure: the slot under the title and claim line of a 16:9 slide (make-research-slides).
#let slide-fig(body, width: 12.33in, height: 4.9in) = {
  set page(width: width, height: height, margin: 0pt, fill: white)
  set text(font: font, size: 20pt, fill: ink)
  set align(center + horizon)
  body
}

// Paper figure: set width to the venue's \linewidth.
#let paper-fig(body, width: 3.25in, height: 2.0in) = {
  set page(width: width, height: height, margin: 0pt, fill: white)
  set text(font: font, size: 8pt, fill: ink)
  set align(center + horizon)
  body
}
```

## fletcher: architecture with process groups

```typst
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "theme.typ": *
#show: slide-fig

#let box(pos, title, name, color: ink, fill: white) = node(
  pos, title, name: name,
  width: 6.6cm, height: 1.7cm, fill: fill, stroke: 1.4pt + color, corner-radius: 6pt)
#let group(a, b) = node(enclose: (a, b), inset: 12pt,
  stroke: (paint: muted, dash: "dashed", thickness: 1pt), corner-radius: 10pt)

#diagram(
  spacing: (1.6cm, 1.3cm),
  edge-stroke: 1.6pt + ink,
  box((0, 0), [Frontend], <fe>),
  box((0, 1), [Output], <out>),
  box((1, 0), [Scheduler], <sched>, color: focus, fill: tint(focus)),
  box((1, 1), [Executor], <exec>),
  group(<fe>, <out>),
  group(<sched>, <exec>),
  node((0, -0.68), text(fill: muted)[Process A]),
  node((1, -0.68), text(fill: muted)[Process B]),
  edge(<fe>, <sched>, "-|>"),
  edge(<sched>, <exec>, "-|>"),
  edge(<exec>, <out>, "-|>"),
)
```

## cetz: before/after step lanes

```typst
#import "@preview/cetz:0.5.3"
#import "theme.typ": *
#show: slide-fig

#cetz.canvas(length: 1cm, {
  import cetz.draw: *
  let (w, gap) = (6.7, 0.9)
  let step(i, y, title, color: ink, fill: white, dash: none) = {
    let x = i * (w + gap)
    rect((x, y - 0.75), (x + w, y + 0.75), radius: 0.15, fill: fill,
      stroke: (paint: color, thickness: 1.4pt, dash: dash))
    content((x + w / 2, y), title)
    if i > 0 { line((x - gap + 0.06, y), (x - 0.06, y), stroke: 1.5pt + ink,
      mark: (end: "stealth", fill: ink, scale: 0.6)) }
  }
  content((0, 3.0), anchor: "south-west", text(weight: "bold")[Before])
  step(0, 1.9, [Old step], color: muted, dash: "dashed")
  step(1, 1.9, [Shared step])
  content((0, 0.0), anchor: "south-west", text(weight: "bold", fill: focus)[After])
  step(0, -1.1, [New step], color: focus, fill: tint(focus))
  step(1, -1.1, [Shared step])
})
```

Leave out the steps that are the same in both lanes; say so in the slide or caption text.

## cetz-plot: trade-off scatter with before → after

```typst
#import "@preview/cetz:0.5.2"          // same version cetz-plot 0.1.4 imports
#import "@preview/cetz-plot:0.1.4": plot
#import "theme.typ": *
#show: slide-fig

#let fmt = v => text(size: 15pt)[#v]
#let pt(p, c) = plot.add((p,), mark: "o", mark-size: 0.32, style: (stroke: none), mark-style: (fill: c, stroke: white))
#let hollow(p, c) = plot.add((p,), mark: "o", mark-size: 0.3, style: (stroke: none), mark-style: (fill: white, stroke: 2pt + c))

#align(left)[*BrowseComp-Plus*\ #text(size: 15pt, fill: muted)[Accuracy (%)]]   // panel label + y quantity; the claim goes in the slide text
#cetz.canvas(length: 1cm, {
  // plot.plot has no `style:` argument (silently ignored); style axes with set-style before it.
  cetz.draw.set-style(axes: (stroke: 1pt + muted, tick: (stroke: 1pt + muted, length: 0.12), padding: 0, overshoot: 0, shared-zero: false,
    grid: (stroke: 0.5pt + faint), x: (mark: (end: none)), y: (mark: (end: none))))
  plot.plot(size: (7.6, 6.4), axis-style: "left",
    x-label: none, y-label: none, x-format: fmt, y-format: fmt,
    x-min: 0, x-max: 4.5, x-tick-step: 1, y-min: 25, y-max: 45, y-tick-step: 5,
    x-grid: true, y-grid: true, {
    plot.add(((4.01, 34.7), (2.19, 42.1)), style: (stroke: 2pt + second))
    hollow((4.01, 34.7), second)
    pt((2.19, 42.1), second)
    plot.add(((1.52, 28.8), (1.34, 42.5)), style: (stroke: 2.4pt + focus))
    hollow((1.52, 28.8), focus)
    pt((1.34, 42.5), focus)
    plot.annotate({
      import cetz.draw: *
      content((1.15, 43.4), anchor: "south", text(fill: focus, weight: "bold")[Ours])
      content((3.0, 42.6), anchor: "south", text(fill: second.darken(20%))[Baseline])
      content((2.25, 21.4), anchor: "north", text(size: 15pt, fill: muted)[PFLOPs per question])
    })
  })
})
```

The deck that places these figures is in make-research-slides `references/templates.md`.
