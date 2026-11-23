# Typst + Fletcher Diagram Guide & Archetypes

Practical reference for synthesizing crisp, zero-error academic vector diagrams with `@preview/fletcher`.

---

## 1. Setup, Version Pinning & Page Sizing

Run `compile_fletcher.py --check-env` first to discover the cached `@preview/fletcher` version (e.g., `0.5.8` or `0.6.0`) and available fonts.

```typst
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import fletcher.shapes: rect, circle, ellipse, pill, diamond, hexagon, cylinder, trapezium, parallelogram
```

### Page sizing presets

1. **Tight auto-sized vector (default when venue width is unspecified):**
   ```typst
   #set page(width: auto, height: auto, margin: 8pt, fill: white)
   #set text(font: "Inter", size: 9pt, fill: rgb("#2B2A27"), hyphenate: false)
   ```
   Ideal for clean standalone vector figures: zero wasted margins, guaranteed compact rectangular bounding box.

2. **Exact venue `\linewidth` (recommended for camera-ready papers so font sizes match exact printed pt):**
   | Venue | Single column | Full width |
   |---|---|---|
   | NeurIPS / ICLR | — | `5.5in` |
   | ICML | `3.25in` | `6.75in` |
   | CVPR / ICCV | `3.25in` | `6.875in` |
   | ACL / EMNLP | `7.7cm` | `16cm` |
   | IEEE (`IEEEtran`) | `3.5in` | `7.16in` |
   | 16:9 Slide slot | — | `12.33in` × `4.9in` |

   ```typst
   #set page(width: 5.5in, height: auto, margin: (x: 4pt, y: 6pt), fill: white)
   #set text(font: "Inter", size: 8.5pt, fill: rgb("#2B2A27"), hyphenate: false)
   #set align(center)
   ```
   Use `height: auto` with fixed `width` so vertical height hugs the diagram cleanly while horizontal width matches `\linewidth` (and `compile_fletcher.py` verifies `page_count == 1`).

---

## 2. Core Fletcher Primitives

### Grid & Coordinates
- Grid coordinates `(col, row)`: `col` increases **rightward**, `row` increases **downward**.
- Fractional coordinates work cleanly for centered titles or branching junctions: `(1.5, -0.65)`, `(2.5, 0.5)`.
- Always name important nodes (`name: <id>`) and connect edges by name (`edge(<a>, <b>, "-|>")`).
- CeTZ anchors on named nodes work directly in edges: `edge(<a.east>, <b.west>, "-|>")`, `edge(<box.south>, (1, 1.5), "-|>")`.

### Nodes
```typst
node(
  (0, 0),
  [*Encoder* \ #text(size: 7.5pt, fill: muted)[Frozen]],
  name: <enc>,
  width: 2.6cm,          // optional: omit for auto-fit with inset
  inset: 7pt,            // MUST be a single length (NOT a dict!)
  fill: rgb("#F0EEE6"),
  stroke: 1pt + rgb("#5E5D59"),
  corner-radius: 5pt,
  shape: rect,           // rect, circle, ellipse, pill, diamond, hexagon, cylinder, trapezium
  extrude: (0, 2.5),     // optional: double border / stacked tensor feel
  layer: 0,              // layer: -1 for background enclose zones
)
```

### Enclosing Zones (Groups) & Zero-Footprint Zone Titles
Put zones on `layer: -1` so they sit cleanly behind nodes and edges. **Always put the zone caption in a separate node above or below the group** — putting content directly inside an `enclose` node places the text in the middle on top of its children!

**Critical anti-inflation pattern (`floating-title`):** A wide caption node placed at an integer column `(col, -0.78)` silently widens that entire grid column in Fletcher, often pushing a `5.5in` or `6.75in` diagram past its page margin! Wrap wide stage or panel titles in a zero-footprint `floating-title` helper so they never distort grid track widths:

```typst
#let floating-title(pos, body, width: 7cm) = node(
  pos,
  box(width: 0pt, align(center, box(width: width, body))),
  inset: 0pt, stroke: none, fill: none,
)

// Pill-shaped zone header; pass the zone's tint/hue (defaults are the warm neutral)
#let stage-pill(pos, label, fill: rgb("#F0EEE6"), stroke: rgb("#CFCCC2"), text-color: rgb("#2B2A27"), width: 7cm) = floating-title(
  pos,
  box(inset: (x: 6pt, y: 2pt), radius: 99pt, fill: fill, stroke: 0.75pt + stroke,
    text(size: 7.5pt, weight: "bold", fill: text-color)[#label]),
  width: width,
)

node(
  enclose: (<n1>, <n2>),
  name: <zone1>,
  inset: 10pt,
  fill: rgb("#FAF9F5"),
  stroke: (paint: rgb("#CFCCC2"), thickness: 0.85pt, dash: "dashed"),
  corner-radius: 8pt,
  layer: -1,
)
stage-pill((0.5, -0.76), [Stage 1: Encoding])
```

### Edges & Routing
- Arrow marks: `"-|>"` (solid stealth/filled tip), `"->"` (open tip), `"--|>"` (dashed + filled tip), `"<|-|>"` (bidirectional), `"|->"` (maps-to), `"-"` (plain connector).
- Orthogonal bus routing via intermediate vertices:
  ```typst
  edge(<src>, (1.5, 0), (1.5, 1), <dst1>, "-|>")
  edge((1.5, 0), (1.5, -1), <dst2>, "-|>")
  ```
- Curved feedback / skip arcs:
  ```typst
  edge(<critic>, <vis>, "--|>", bend: -38deg, label: [Revise], label-side: right, label-fill: white)
  ```
- Clean crossing halo:
  ```typst
  edge(<a>, <b>, "-|>", crossing: true, crossing-thickness: 4)
  ```
- Label placement tuning: `label-pos: 0.5` (or `(segment_idx, 0.5)` on multi-segment edges), `label-side: left | right | center`, `label-sep: 3pt`, `label-fill: white`.

### Built-In Visual Debugger
Fletcher supports `debug: 1`, `debug: 2`, or `debug: 3` inside `#diagram(...)` to overlay grid axes, node bounding boxes, and edge anchor points. **Do not leave `debug` in final files** — use `scripts/compile_fletcher.py --debug 2` to render a non-destructive debug overlay PNG during Critic inspection.

---

## 3. Reusable Academic Diagram Archetypes

### Archetype 1: Left-to-Right Pipeline with Stage Zones

```typst
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#set page(width: auto, height: auto, margin: 10pt, fill: white)
#set text(font: "Inter", size: 8.5pt, fill: rgb("#2B2A27"), hyphenate: false)

#let ink = rgb("#2B2A27")
#let ink-soft = rgb("#5E5D59")
#let muted = rgb("#8F8D86")
#let line-c = rgb("#CFCCC2")
#let sand = rgb("#F0EEE6")
#let paper = rgb("#FAF9F5")
#let clay = rgb("#C6613F")
#let clay-fill = rgb("#F6E4DC")
#let sky = rgb("#4F7FAE")
#let sky-fill = rgb("#E2EBF4")
#let olive = rgb("#6B7F4E")
#let olive-fill = rgb("#E8EDE0")
#let ochre = rgb("#B98A3E")
#let ochre-fill = rgb("#F5ECDA")

#let proc(pos, body, name, stroke: ink-soft, fill: sand) = node(
  pos, body, name: name, shape: fletcher.shapes.rect,
  inset: 7pt, corner-radius: 5pt, fill: fill, stroke: 1pt + stroke,
)
#let data-node(pos, body, name) = node(
  pos, body, name: name, shape: fletcher.shapes.rect,
  inset: 6pt, corner-radius: 2pt, fill: olive-fill, stroke: 0.9pt + olive,
)
#let zone(nodes, name: none) = node(
  enclose: nodes, name: name, inset: 11pt, corner-radius: 8pt,
  fill: paper, stroke: (paint: line-c, thickness: 0.85pt, dash: "dashed"), layer: -1,
)

#diagram(
  spacing: (1.2cm, 0.9cm),
  edge-stroke: 1pt + ink-soft,
  data-node((0, 0), [Raw Input $x$], <in>),
  proc((1, 0), [Tokenizer], <tok>, stroke: sky, fill: sky-fill),
  proc((2, 0), [*Proposed Backbone* \ $f_theta$], <enc>, stroke: clay, fill: clay-fill),
  proc((3, 0), [Task Head], <head>, stroke: ochre, fill: ochre-fill),
  data-node((4, 0), [Prediction $hat(y)$], <out>),

  zone((<tok>, <enc>)),
  node((1.5, -0.78), text(size: 7.5pt, weight: "bold", fill: ink)[Feature Extraction]),

  edge(<in>, <tok>, "-|>"),
  edge(<tok>, <enc>, "-|>"),
  edge(<enc>, <head>, "-|>"),
  edge(<head>, <out>, "-|>"),
)
```

### Archetype 2: Iterative Agent / Refinement Loop

```typst
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#set page(width: auto, height: auto, margin: 10pt, fill: white)
#set text(font: "Inter", size: 8.5pt, fill: rgb("#2B2A27"), hyphenate: false)

#let ink = rgb("#2B2A27")
#let ink-soft = rgb("#5E5D59")
#let muted = rgb("#8F8D86")
#let line-c = rgb("#CFCCC2")
#let sand = rgb("#F0EEE6")
#let paper = rgb("#FAF9F5")
#let clay = rgb("#C6613F")
#let clay-fill = rgb("#F6E4DC")
#let sky = rgb("#4F7FAE")
#let sky-fill = rgb("#E2EBF4")
#let olive = rgb("#6B7F4E")
#let olive-fill = rgb("#E8EDE0")
#let ochre = rgb("#B98A3E")
#let ochre-fill = rgb("#F5ECDA")
#let box-node(pos, body, name, stroke: ink-soft, fill: sand) = node(
  pos, body, name: name, shape: fletcher.shapes.rect,
  inset: 7pt, corner-radius: 5pt, fill: fill, stroke: 1pt + stroke,
)

#diagram(
  spacing: (1.65cm, 1.0cm),
  edge-stroke: 1pt + ink-soft,
  box-node((0, 0), [Planner], <plan>, stroke: ochre, fill: ochre-fill),
  box-node((1, 0), [Stylist], <style>, stroke: ochre, fill: ochre-fill),
  box-node((2, 0), [*Visualizer* \ (Fletcher)], <vis>, stroke: clay, fill: clay-fill),
  box-node((3, 0), [*Critic* \ (Veto Audit)], <crit>, stroke: clay, fill: clay-fill),
  box-node((4, 0), [Vector \ PDF / SVG], <out>, stroke: olive, fill: olive-fill),

  node(enclose: (<vis>, <crit>), inset: 12pt, corner-radius: 8pt,
    fill: paper, stroke: (paint: line-c, dash: "dashed", thickness: 0.85pt), layer: -1),
  node((2.5, -0.78), text(size: 7.5pt, weight: "bold", fill: clay)[Refinement Loop ($<= 3$ rounds)]),

  edge(<plan>, <style>, "-|>"),
  edge(<style>, <vis>, "-|>"),
  edge(<vis>, <crit>, "-|>", label: [PNG + `.typ`], label-size: 7pt, label-side: left),
  edge(<crit>, <vis>, "--|>", bend: 45deg,
    stroke: (paint: clay, thickness: 1pt, dash: "dashed"),
    label: [Surgical patch], label-size: 7pt, label-side: left, label-fill: white),
  edge(<crit>, <out>, "-|>", label: [Pass], label-size: 7pt, label-side: left),
)
```

### Archetype 3: Parallel Multi-Branch with Math Operators ($+$, $\times$)

```typst
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import fletcher.shapes: circle, rect

#let ink-soft = rgb("#5E5D59")
#let sand = rgb("#F0EEE6")
#let clay = rgb("#C6613F")
#let sky = rgb("#4F7FAE")
#let ochre = rgb("#B98A3E")
#let op(pos, sym, name) = node(
  pos, sym, name: name, shape: circle, inset: 2.5pt,
  fill: white, stroke: 0.9pt + ink-soft,
)

#diagram(
  spacing: (1.2cm, 0.75cm),
  edge-stroke: 1pt + ink-soft,
  node((0, 0.5), [Input $X$], name: <x>, shape: rect, inset: 6pt, fill: sand, stroke: 0.9pt + ink-soft, corner-radius: 2pt),
  node((1, 0), [Vision Branch], name: <v>, shape: rect, inset: 7pt, fill: rgb("#E2EBF4"), stroke: 1pt + sky, corner-radius: 5pt),
  node((1, 1), [Text Branch], name: <t>, shape: rect, inset: 7pt, fill: rgb("#F5ECDA"), stroke: 1pt + ochre, corner-radius: 5pt),
  op((2, 0.5), [$+$], <fuse>),
  node((3, 0.5), [*Fusion Decoder*], name: <dec>, shape: rect, inset: 7pt, fill: rgb("#F6E4DC"), stroke: 1.15pt + clay, corner-radius: 5pt),

  edge(<x>, (0.5, 0.5), (0.5, 0), <v>, "-|>"),
  edge(<x>, (0.5, 0.5), (0.5, 1), <t>, "-|>"),
  edge(<v>, (1.5, 0), (1.5, 0.5), <fuse>, "-|>"),
  edge(<t>, (1.5, 1), (1.5, 0.5), <fuse>, "-|>"),
  edge(<fuse>, <dec>, "-|>"),
)
```

### Archetype 4: Macro–Micro Breakout
Use a left-hand system overview (`col 0..2`) and a right-hand zoomed-in container (`col 3.5..5`) linked from the highlighted target node via two dashed callout edges (`stroke: (paint: muted, dash: "dotted")`, `"-"`) pointing to the zoomed container's `<micro.north-west>` and `<micro.south-west>` anchors.

### Archetype 5: Hybrid CeTZ Inside a Fletcher Node
When a diagram needs a small tensor stack, attention matrix, or token strip inside a node, embed a compact `box(...)` containing Typst grids/blocks or a mini CeTZ canvas right as the node's content — Fletcher routes arrows cleanly to its outer boundary!

```typst
#let token-strip(labels, fill: rgb("#F6E4DC"), stroke: rgb("#C6613F")) = stack(
  dir: ltr, spacing: 2pt,
  ..labels.map(t => box(inset: (x: 4pt, y: 3pt), radius: 2pt, fill: fill, stroke: 0.7pt + stroke, text(size: 7pt)[#t]))
)
```

---

## 4. Typst & Fletcher Gotchas

1. **`inset` must be a single length:** `node(..., inset: 8pt)` works; `inset: (x: 8pt, y: 5pt)` throws a Fletcher error. If you need asymmetric padding, wrap the content inside `pad(x: 6pt, y: 2pt)[...]` and use `inset: 4pt`.
2. **Never put text inside `enclose`:** `node(enclose: (<a>, <b>), [Title])` draws `[Title]` in the middle over `<a>` and `<b>`. Put the title in its own `node((x, y), [Title])` above the enclosed group.
3. **Silent text wrap with fixed `width`:** Fixed `width` makes rows uniform, but long/bold words wrap onto ugly extra lines silently. Either size `width` generously to the widest label or omit `width` and rely on `inset`.
4. **Content markup collisions:**
   - Leading `+ `, `- `, or `1. ` inside `[...]` is parsed as a list (`[\+ Residual]` to escape).
   - `#` inside text must be escaped (`\#`).
   - `context` is a reserved Typst keyword — never name a variable or node helper `context`.
5. **Arrow tip vs. label ambiguity:** In Fletcher ≥ 0.5, pass edge labels as content (`[label]`) or named `label: [label]`, not bare strings (`"label"`), because strings are parsed as arrow/direction shorthands.
6. **Multi-page overflow:** If a diagram exceeds a fixed page width or height, Typst silently spills onto page 2. Always compile with `scripts/compile_fletcher.py`, which checks `page_count == 1`.
7. **Font fallback warnings:** Typst falls back silently to Libertinus Serif if a named font is missing. Always check `font_warnings` from `compile_fletcher.py` and pick a font listed by `--check-env`.
8. **Typst 0.15 math is NOT LaTeX:** Never write LaTeX backslashes inside `$...$` (`\theta`, `\nabla`, `\mathcal{L}`, `\oplus`, `\otimes` fail to compile!) and avoid removed `.circle` modifiers (`plus.circle`, `dot.circle`). Write Typst 0.15 math symbols directly: `$theta$`, `$nabla_theta$`, `$cal(L)_"CE"$`, `$plus.o$` (or `$+$` inside a `circle` node), `$times.o$`, `$dot.o$`, `$hat(y)$`.
9. **Column inflation from wide title nodes:** Any wide text node placed at an integer column inflates that column's track width. Always wrap stage/panel headers in `floating-title(...)` (above).
10. **Explicit `shape: rect` on compact data boxes:** Always specify `shape: fletcher.shapes.rect` on custom box helpers so square data nodes never collapse into circles.
11. **Fixed-width budget upfront:** On `5.5in` (`13.97cm`) or `6.75in` (`17.15cm`) paper figures, plan column count × node width + `(cols - 1) * spacing.x` ≤ page width minus margins on Round 0 (e.g., 4–5 columns at `5.5in` → keep `spacing.x` around `0.65cm–0.85cm` and body text `7.5pt–8pt`).
