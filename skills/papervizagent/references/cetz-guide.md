# Typst + CeTZ Guide for Atypical Academic Visuals

Use `@preview/cetz` whenever a figure goes beyond box-and-arrow diagrams — timelines, memory/KV-cache layouts, token/sequence strips, 3D tensor/feature-map stacks, attention heatmaps, latent-space manifolds, before/after swimlanes, conceptual teasers, or crisp vector badges embedded inside Fletcher nodes.

---

## 1. Setup, Version Pinning & Coordinate Budget

Run `compile_fletcher.py --check-env` first to inspect cached `cetz` and `fletcher` versions.

```typst
#import "@preview/cetz:0.3.4"
```
> **Version rule:** When combining CeTZ with `@preview/fletcher:0.5.8` in the same file, pin the matching `cetz` version (`0.3.4` or whatever `fletcher` depends on). For standalone CeTZ drawings, any cached version (`0.3.4` or newer `0.5.x`) works cleanly.

### Planning Coordinates Against Venue Width
An over-wide `cetz.canvas` is **not** scaled down on a fixed-width page — it is centered and clipped on both sides! Always budget your `x` span in `cm` directly against the venue's `\linewidth`:

| Venue | Width (in) | Safe Canvas Span (`length: 1cm`, 4pt margins) |
|---|---|---|
| ICML / CVPR single-col | `3.25in` | `0 .. 7.9 cm` |
| NeurIPS / ICLR full-width | `5.5in` | `0 .. 13.6 cm` |
| ACL / EMNLP full-width | `16cm` | `0 .. 15.6 cm` |
| ICML / CVPR full-width | `6.75in` | `0 .. 16.7 cm` |
| 16:9 Slide slot | `12.33in` | `0 .. 30.8 cm` |

To verify exact canvas width before locking coordinates, compile once with `width: auto, height: auto` or run `compile_fletcher.py --debug 2` to overlay a 1 cm coordinate grid.

---

## 2. Core CeTZ Drawing Primitives

```typst
#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  // Background zone (draw behind foreground using on-layer(-1, ...))
  on-layer(-1, {
    rect((0, 0), (6, 3), radius: 0.18, fill: rgb("#F8F9FA"),
      stroke: (paint: rgb("#8B929A"), thickness: 0.85pt, dash: "dashed"))
  })

  // Rounded box + anchored label (focus color reserved for the key/novel block)
  rect((0.4, 0.8), (2.8, 2.0), radius: 0.14, fill: rgb("#EDF3F9"), stroke: 1.1pt + rgb("#004488"))
  content((1.6, 1.4), [*Encoder*])

  // Arrow with stealth tip
  line((2.85, 1.4), (4.15, 1.4), stroke: 1pt + rgb("#22272E"),
    mark: (end: "stealth", fill: rgb("#22272E"), scale: 0.55))

  // Smooth curve (for manifolds, distributions, curved arcs)
  bezier((4.2, 0.8), (5.8, 2.2), (4.8, 2.3), (5.2, 0.7),
    stroke: (paint: rgb("#004488"), thickness: 1.1pt, dash: "dashed"),
    mark: (end: "stealth", fill: rgb("#004488"), scale: 0.5))

  // Anchored text (avoid overlapping shapes using north/south/east/west)
  content((3.5, 1.55), anchor: "south", text(size: 7.5pt)[$H_v$])
})
```

> **Coordinate direction:** Unlike Fletcher (where `row` grows downward), CeTZ uses standard mathematical Cartesian coordinates where **`y` grows upward**!

---

## 3. Reusable Atypical Academic Archetypes

### Archetype A: Memory / KV-Cache / Token Eviction Strip (Before → After)

Ideal for systems, long-context LLM, pruning, speculative decoding, and quantization papers.

```typst
#import "@preview/cetz:0.3.4"

#set page(width: 5.5in, height: auto, margin: (x: 5pt, y: 6pt), fill: white)
#set text(font: "Inter", size: 8pt, fill: rgb("#1F2937"), hyphenate: false)

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  let draw-strip(y, tokens, colors, title) = {
    content((0, y + 0.55), anchor: "south-west", text(weight: "bold", size: 8pt)[#title])
    for (i, tok) in tokens.enumerate() {
      let x = i * 1.15
      let (fill-c, stroke-c, dash-s) = colors.at(i)
      rect((x, y - 0.32), (x + 1.05, y + 0.32), radius: 0.08,
        fill: fill-c, stroke: (paint: stroke-c, thickness: 0.9pt, dash: dash-s))
      content((x + 0.525, y), text(size: 7.5pt)[#tok])
    }
  }

  let keep = (rgb("#EDF3F9"), rgb("#004488"), none)
  let sink = (rgb("#FBF5E8"), rgb("#C28A2E"), none)
  let drop = (rgb("#F8F9FA"), rgb("#CBD5E1"), "dashed")

  draw-strip(2.0,
    ([$t_0$], [$t_1$], [$t_2$], [$t_3$], [$t_4$], [$t_5$], [$t_6$], [$t_7$]),
    (sink, drop, keep, drop, drop, keep, keep, keep),
    [Full KV Cache (Eviction Candidates Dashed)])

  draw-strip(0.4,
    ([$t_0$], [$t_2$], [$t_5$], [$t_6$], [$t_7$]),
    (sink, keep, keep, keep, keep),
    [Compressed Cache (Sink + Heavy Hitters + Recent Window)])
})
```

### Archetype B: 3D Isometric Tensor / Feature-Map Stack

Ideal for vision, diffusion, 3D geometry, and volumetric feature representations.

```typst
#let tensor-stack(x, y, w: 1.1, h: 1.4, depth: 3, dx: 0.14, dy: 0.14,
                  fill: rgb("#EDF3F9"), stroke: rgb("#004488"), label: none) = {
  import cetz.draw: *
  for k in range(depth).rev() {
    let ox = x + k * dx
    let oy = y + k * dy
    rect((ox, oy), (ox + w, oy + h), radius: 0.05,
      fill: fill.lighten(k * 12%), stroke: 0.85pt + stroke)
  }
  if label != none {
    content((x + w / 2, y - 0.22), anchor: "north", text(size: 7.5pt)[#label])
  }
}
```

### Archetype C: Vector Attention Matrix / Heatmap Grid

Ideal for visualizing sparse attention patterns, block masks, or similarity matrices inside a figure.

```typst
#let attn-grid(x, y, matrix, cell: 0.38, accent: rgb("#004488")) = {
  import cetz.draw: *
  let n = matrix.len()
  for r in range(n) {
    for c in range(matrix.at(r).len()) {
      let v = matrix.at(r).at(c) // 0.0 .. 1.0
      let fill-c = if v <= 0.05 { rgb("#F8F9FA") } else { accent.lighten(int((1 - v) * 85) * 1%) }
      let cy = y + (n - 1 - r) * cell
      rect((x + c * cell, cy), (x + (c + 1) * cell, cy + cell),
        fill: fill-c, stroke: 0.45pt + rgb("#CBD5E1"))
    }
  }
  rect((x, y), (x + n * cell, y + n * cell), fill: none, stroke: 0.9pt + rgb("#22272E"))
}
```

### Archetype D: Hybrid CeTZ Badges & Mini-Visuals Inside Fletcher Nodes

Because Fletcher runs on Typst + CeTZ, you can drop crisp miniature CeTZ drawings directly inside any Fletcher `node(...)` label — zero Unicode emoji font issues, 100% vector!

```typst
#import "@preview/cetz:0.3.4"

// Minimal vector snowflake (Frozen, muted slate) and spark (Trainable, focus blue) badges
#let frozen-badge() = box(baseline: 15%, cetz.canvas(length: 1pt, {
  import cetz.draw: *
  let c = rgb("#64748B")
  for a in (0deg, 60deg, 120deg) {
    line((calc.cos(a) * -3.5, calc.sin(a) * -3.5), (calc.cos(a) * 3.5, calc.sin(a) * 3.5),
      stroke: 0.85pt + c)
  }
}))

#let trainable-badge() = box(baseline: 15%, cetz.canvas(length: 1pt, {
  import cetz.draw: *
  let c = rgb("#004488")
  line((0, 4), (1.4, 1.1), (4, 0), (1.4, -1.1), (0, -4), (-1.4, -1.1), (-4, 0), (-1.4, 1.1),
    close: true, fill: c, stroke: none)
}))

// Subtle status tag ready for any Fletcher node body
#let status-pill(icon, label, fill: rgb("#F1F5F9"), text-color: rgb("#4B5563")) = box(
  inset: (x: 4pt, y: 1.5pt), radius: 99pt, fill: fill,
  text(size: 6.5pt, weight: "semibold", fill: text-color)[#icon #h(1.5pt) #label]
)
```

---

## 4. Composing Multi-Panel Figures (CeTZ + Fletcher Side-by-Side)

For complex papers where Panel (a) is an atypical CeTZ spatial/memory/manifold visual and Panel (b) is a Fletcher architecture diagram, place them cleanly inside a single `#grid(columns: (auto, auto), column-gutter: 10pt, align: horizon, panel-a, panel-b)` on the exact venue page width. Both panels share the same palette variables and font declarations.

---

## 5. CeTZ Gotchas

1. **Name shadowing:** `import cetz.draw: *` shadows Typst's built-in `circle`, `rect`, `line`, `polygon`, and `path`. Inside a `cetz.canvas` block, if you need Typst's inline shape inside `content(...)`, write `std.circle(...)` or `std.rect(...)`.
2. **Y-axis grows UPWARD:** `(0, 0)` is bottom-left; `(0, 2)` is *above* `(0, 0)`. (Opposite of Fletcher's grid where `row` grows downward!)
3. **No auto-scaling on fixed width:** If your CeTZ drawing spans `15cm` on a `5.5in` (`13.97cm`) page, Typst clips left and right edges. Always compute total width in `cm` upfront or adjust `length:` (e.g., `length: 0.92cm`) to fit cleanly with margin.
4. **Rounded corners use `radius:` (not `corner-radius:`):** CeTZ `rect(..., radius: 0.14)` uses `radius` in canvas units (or length like `4pt`); Fletcher `node(..., corner-radius: 5pt)` uses `corner-radius`.
5. **Typst 0.15 math symbols:** Use `$plus.o$`, `$times.o$`, `$dot.o$`, `$theta$`, `$sigma$`, `$cal(L)$` — never LaTeX backslashes (`\theta`, `\sigma`) or deprecated `.circle` modifiers (`plus.circle`, `dot.circle`).
6. **Debug overlay:** Run `scripts/compile_fletcher.py <file>.typ --debug 2` — on standalone `cetz.canvas(` files it automatically overlays a non-destructive 1 cm coordinate grid so the Critic can inspect exact `(x, y)` coordinates and bounds.
