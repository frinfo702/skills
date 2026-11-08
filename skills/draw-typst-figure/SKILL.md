---
name: draw-typst-figure
description: >-
  Draw research figures in Typst: node-and-arrow diagrams with fletcher, custom drawings (timelines, memory layouts, context strips, teasers) with cetz, and data plots with cetz-plot, then compile them to PDF/PNG for a LaTeX paper or a slide deck. Use whenever a figure, diagram, architecture picture or plot is to be drawn, especially together with make-research-figure, or when the user mentions Typst, fletcher, cetz or cetz-plot. Trigger e.g. "図を描いて", "アーキテクチャ図", "概要図", "パイプラインの図", "Typstで図", "fletcherで", "cetzで", "プロットをTypstで", "/draw-typst-figure".
---

# draw-typst-figure

This skill is the drawing tool. What the figure should say and how it should look comes from `make-research-figure`; read it first when it is available. Two of its rules shape every drawing: all text in the image is English, and the image holds no title, caption, explanatory note or highlighted number, only names, axis labels, legends and data. Slides around the figures are `make-research-slides`. Templates are in `references/templates.md`.

## Pick the package

| Figure | Package |
|---|---|
| Boxes and arrows: architectures, pipelines, data flow, state machines | fletcher (`@preview/fletcher`) |
| Anything placed by coordinates: timelines, memory/buffer layouts, token strips, before/after comparisons, teasers, dumbbell charts | cetz (`@preview/cetz`) |
| Data on axes: scatter, line, trade-off plots | cetz-plot (`@preview/cetz-plot`) |
| Tables | Typst `table` (no package) |
| Thousands of points, images, heatmaps of real data | matplotlib to PDF (see make-research-figure `references/specs.md`), placed with `image()` |

Pin exact versions. Look up the newest before starting, and read the version of cetz that cetz-plot imports:

```sh
curl -s https://packages.typst.org/preview/index.json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(n, max((p['version'] for p in d if p['name']==n), key=lambda v: tuple(map(int, v.split('.'))))) for n in ('cetz','fletcher','cetz-plot')]"
```

## Workflow

1. **One file per figure** (`fig-<name>.typ`), importing a shared `theme.typ` (palette, fonts, page setup). Change the look there, never per figure.
2. **Page = final slot.** The figure's page size is exactly the size it will occupy: `\linewidth` of the paper, or the slide's figure slot below the title and claim line (12.33 × 4.9 in). Then it is placed at 100% and font sizes are what they say.
3. **Compile and look, every iteration:**
   ```sh
   typst compile fig-x.typ 'fig-x-{p}.png' --ppi 100   # {p}: overflow shows up as a second page
   ```
   Open the PNG and check it: clipped text, text wrapped inside boxes, labels on top of lines or borders, edges crossing nodes, content touching the page edge. Most layout bugs only show up in the render.
4. **Export:** `typst compile fig-x.typ fig-x.pdf`. Typst embeds the fonts. LaTeX: `\includegraphics[width=\linewidth]{fig-x.pdf}`. Typst decks: `image("fig-x.pdf")` (make-research-slides). PowerPoint/Keynote: SVG (`--format svg`) or PNG at 200+ ppi.
5. Keep the numbers in the figure source traceable: a comment naming where each number came from (paper table, PR description, run id), or read them with `csv()`/`json()` from the logged results.

## fletcher

- Grid coordinates `(col, row)`, rows grow downward. Fractional coordinates work (`(1, -0.7)` for a group caption).
- Give every node `name: <label>` and connect by name: `edge(<a>, <b>, "-|>")`.
- **Fix node width and height** for a uniform look, but text that does not fit wraps silently (bold text is wider). Size the boxes to the longest name, or leave `width` unset and pad with `inset: 16pt`. `inset` must be a single length; a dictionary like `(x: 18pt)` errors.
- Groups: `node(enclose: (<first>, <last>), stroke: (dash: "dashed"), inset: 12pt)`, with the group's name as a separate node above it. Do not put the name inside the enclose node: it lands in the middle, over the members.
- Orthogonal routing and buses: give the edge intermediate vertices, `edge(<exec>, (2.5, 2), (2.5, 0), <w0>, "-|>")`, then `edge((2.5, 1), <w1>, "-|>")` branches off it.
- Edge labels collide with group borders and boxes on short edges. Lengthen the spacing, or drop the label and say it in the group caption.
- Loops: two `bend:` edges with opposite signs (one above, one below) between the same nodes, with the important one in the focus color and solid, the default one dashed and muted.

## cetz

- `cetz.canvas(length: 1cm, { import cetz.draw: * ... })`. Plan coordinates in cm against the page size: an over-wide canvas is not scaled down, it is centered and clipped on both sides. To measure a canvas, compile it once on `set page(width: auto, height: auto)` and read the page size.
- Write small local functions (`step(i, y, ...)`, `row(...)`, `strip(...)`) for repeated shapes and call them with data. The figure then reads like its content.
- `import cetz.draw: *` shadows Typst's `circle`, `rect`, `line`. Inside the canvas, use `std.circle(...)` for inline content.
- Put text with `content(pos, anchor: "west", ...)`. Anchors (`"west"`, `"south-west"`, `"north"`) are how labels avoid shapes.

## cetz-plot

- Import the same cetz version that cetz-plot imports (cetz-plot 0.1.4 → cetz 0.5.2). A different canvas version breaks or misplaces things.
- `plot.plot` has no `style:` argument and ignores it silently. Style axes with `cetz.draw.set-style(axes: (stroke: ..., tick: ..., grid: ..., x: (mark: (end: none)), y: (mark: (end: none))))` before `plot.plot`.
- `shared-zero` is an axes style key, not a `plot.plot` argument: put `shared-zero: false` in `set-style(axes: (...))`, or the origin shows a single math-font "0" instead of both 0 ticks.
- The axes extend past the data range by default; add `padding: 0, overshoot: 0` to the `axes` style to end them at the data.
- Tick labels can extend past the canvas on the left; leave margin in the page or panel for them.
- Tick labels are math by default (Computer Modern among sans text). Pass `x-format: v => text(size: 15pt)[#v]`, and the same for `y-format`.
- `axis-style: "left"` draws the x-label at the arrow tip. Set `x-label: none, y-label: none`, put the y quantity in the panel subtitle ("Accuracy (%) · BrowseComp-Plus") and the x quantity below the axis with `plot.annotate` and a `content(..., anchor: "north")`.
- Marks drawn inside `plot.annotate` live in data coordinates and get stretched. Do not draw arrowheads there; show before → after as a hollow point → filled point joined by a line, and say so in a legend.
- Direct labels via `plot.annotate({ content((x, y), anchor: ..., text(fill: c)[Name]) })`. `west`/`east` anchors drift horizontally inside annotate; `south`/`north` are reliable. Render and check that labels do not cover their points.

## Typst content gotchas

- `[+ text]`, `[- text]`, `[1. text]` at the start of content are list markup. Write `[\+ text]` or rephrase.
- `#` in text needs escaping: `vllm\#56492`.
- Dictionary keys must be strings; `(1: ...)` is an error.
- `str(62.0)` is `"62"`: a whole float loses its decimals, so a column of values shows uneven digits. Format to a fixed precision: `str(calc.round(v, digits: 1)) + if calc.fract(v) == 0 { ".0" } else { "" }`.
- `context` is a keyword: a color or variable cannot be named `context`.
- Math uses a math font (New Computer Modern Math by default). Keep math to symbols that need it ($c_t$); write words as text.
- A missing font falls back with only a warning. Check `typst fonts` for the theme's font.
- Hyphenation splits words in narrow table cells: `set text(hyphenate: false)`.
