# Academic Illustration Style Guide (Calm Restraint → Typst / Fletcher / CeTZ)

Adapted from PaperVizAgent's NeurIPS 2025 academic design standards and Paul Tol's colorblind-safe scientific palettes, tuned for **calm visual restraint**.

> **Workspace override rule:** If the user's project already has a `theme.typ` or established color semantics across other figures in the paper, follow the workspace theme instead of introducing a second palette.

---

## 1. Visual Philosophy: Color Restraint First

Color is a scarce attention channel. When every module box and every background zone gets a different hue (blue + amber + purple + teal + crimson in one figure), nothing stands out and the diagram reads like a decorative slideshow rather than a scientific paper.

**Default rule for every diagram:**
1. **Neutral is white + ink (`#22272E`), not colored pastel fills.** Standard components (inputs, outputs, frozen backbones, generic layers, boilerplate steps) are **white boxes with clean `ink` (or muted slate) outlines**.
2. **Zones stay neutral.** Grouping containers (`enclose` / panels) use a **pure white** or **ultra-faint neutral gray (`#F8F9FA`)** fill with a **dashed muted gray border (`#94A3B8`)** and a calm dark/muted header — never competing tinted pastel blocks.
3. **Spend ONE focus color (`#004488` deep academic blue) on the contribution.** Highlight only what is novel, trainable, or central to the paper's claim with `focus` stroke + light `tint(focus)` fill so the reader's eye lands on the key idea in one second.
4. **Add a second muted hue ONLY when semantics genuinely require it** (e.g., distinguishing 3 token roles in a KV-cache heatmap, or separating a second tracked stream). Cap typical architecture diagrams at **1 focus hue** (at most 2); cap multi-category spatial visuals (heatmaps/memory strips) at **3 muted hues max**.
5. **Reserve muted rose (`#B84A5B`) strictly for negative/error/eviction/loss signals** — never as generic emphasis alongside blue or teal.

### Default Palette: Calm Scientific Restraint (Paul Tol-Inspired, Colorblind-Safe)

```typst
// Core neutrals (80%+ of the figure lives here)
#let ink        = rgb("#22272E")  // primary text, outlines of neutral white boxes, forward arrows
#let ink-soft   = rgb("#4B5563")  // subtitles, frozen module outlines, secondary labels
#let muted      = rgb("#8B929A")  // dashed zone borders, auxiliary/skip arrows, axis ticks
#let zone-bg    = rgb("#F8F9FA")  // ultra-subtle neutral zone fill (or use `white`)
#let faint      = rgb("#E5E7EB")  // subtle dividers, masked matrix cells, freed slots

// Primary focus (ONE focus hue per diagram: ours / novel / trainable / key mechanism)
#let focus      = rgb("#004488")  // deep academic blue
#let focus-fill = rgb("#EDF3F9")  // calm 88% tint for focus boxes

// Optional secondary muted accents (use ONLY when distinct categories must be told apart)
#let second      = rgb("#C28A2E") // muted ochre (e.g., attention sink / secondary stream)
#let second-fill = rgb("#FBF5E8")
#let third       = rgb("#3A8C80") // muted teal (e.g., recent window / third distinct role)
#let third-fill  = rgb("#EDF6F4")

// Negative / failure / loss / eviction ONLY
#let problem      = rgb("#B84A5B") // muted rose
#let problem-fill = rgb("#FAEEF0")
```

> **Opt-in multi-pastel mode:** Only use multi-colored pastel zones (blue/cream/mint/lavender backgrounds) if the user explicitly asks for a colorful/pastel style. Otherwise stick strictly to the calm neutral + 1 focus color discipline above.

---

## 2. Shapes & Containers ("Softened Geometry")

Use **shape and stroke weight**, not extra colors, to distinguish roles:

| Semantic Role | Fletcher / CeTZ Styling |
|---|---|
| Standard / neutral process / layer / agent | `shape: rect`, `fill: white`, `stroke: 0.95pt + ink`, `corner-radius: 5pt` |
| Novel / proposed / trainable component | `shape: rect`, `fill: focus-fill`, `stroke: 1.25pt + focus`, `corner-radius: 5pt` |
| Frozen / static / external module | `shape: rect`, `fill: zone-bg`, `stroke: 0.9pt + ink-soft`, `corner-radius: 5pt` (plus small monochrome/muted snowflake badge) |
| Data / tensor / prompt / matrix | Sharp or tight-radius `rect` (`corner-radius: 1.5pt`), `fill: white`, `stroke: 0.9pt + ink` |
| Database / memory / replay buffer / KV store | `shape: fletcher.shapes.cylinder`, `fill: white` (or `zone-bg`), `stroke: 0.9pt + ink-soft` |
| Decision / router / gate | `shape: fletcher.shapes.diamond`, `fill: white`, `stroke: 1pt + ink` (or `focus` if key gate) |
| Math operator ($+$, $\times$) | Small `shape: circle`, `inset: 2pt`, `fill: white`, `stroke: 0.9pt + ink` |
| Logical stage / scope / phase (`enclose`) | `fill: zone-bg` (or `white`), `stroke: (paint: muted, dash: "dashed", thickness: 0.85pt)`, `corner-radius: 8pt`, `layer: -1` |
| Macro–Micro breakout | Neutral outer macro panel + focus-highlighted target block connected via dotted `focus` callout lines to a focus-bordered zoomed micro panel |

---

## 3. Lines & Arrows (Flow Semantics)

Distinguish flow types by **line style** (solid vs. dashed, straight vs. curved) so every figure stays 100% readable in grayscale print as well as color:

| Flow Type | Edge Style |
|---|---|
| Forward data / main pipeline | Solid `ink` (`stroke: 1pt + ink`, `"-|>"`) |
| Auxiliary flow (gradients, skip connections, retrieval lookup) | Dashed muted (`stroke: (paint: muted, thickness: 0.95pt, dash: "dashed")`, `"--|>"`) |
| Feedback / critique / iterative loop | Dashed `focus` (or `problem` if error-driven) curved or orthogonal return bus (`"--|>"`) |
| Key highlighted output / accepted path | Solid `focus` (`stroke: 1.15pt + focus`, `"-|>"`) |
| Crossing edges | `crossing: true, crossing-thickness: 4` (white halo so paths never look merged) |

---

## 4. Typography & Math Separation

- **Module & zone labels:** Clean **Sans-Serif** (`"Inter"`, `"Helvetica Neue"`, `"Roboto"`, or `"Arial"` — verify installed fonts with `--check-env`).
  - Zone headers: bold dark `ink` or `ink-soft` text (or a subtle neutral pill `#F1F5F9` / `white` with `#CBD5E1` stroke) placed cleanly *above* the zone via `floating-title` / `stage-pill`. Reserve colored pills strictly for the focus breakout panel.
  - Node titles: semibold/bold `ink`; optional short subtitle in smaller `ink-soft`.
- **Mathematical variables:** Always use Typst math mode (`$x$`, `$theta$`, `$cal(L)_"CE"$`, `$Q, K, V$`), which renders in italic math serif. Typst math uses bare identifiers (`theta`, `nabla`, `sigma`, `cal(L)`, `plus.o`, `times.o`, `dot.o`), **not** LaTeX backslashes (`\theta`).
- **Printed legibility:** Paper figures at final `\linewidth`: **7.5–9 pt** (never below 6.5 pt); slides: **≥ 18 pt**. Always set `set text(hyphenate: false)`.
- **Background:** Always pure white (`fill: white`). Never dark/black backgrounds.

---

## 5. Domain-Specific & Atypical Visual Styles

- **Agent / LLM / Multi-Agent Papers:** Clean neutral white boxes for standard agents/tools, dashed gray stage enclosures with calm neutral `stage-pill` headers, deep blue `focus` strictly on the novel module or loop, and subtle monochrome/muted CeTZ vector status badges (snowflake for Frozen, spark for Trainable).
- **Systems / Long-Context / Efficiency Papers (CeTZ):** Use aligned horizontal token/memory strips where evicted/inactive slots are light dashed gray (`faint`/`muted`), retained focus tokens use `focus` (`#004488`), and at most 1–2 muted secondary roles (`second` ochre, `third` teal) separate distinct retention classes (e.g., Sink vs. Heavy Hitter vs. Recent).
- **Computer Vision / 3D / Multimodal Papers (Hybrid / CeTZ):** Neutral frozen backbones (white/`zone-bg` with `ink-soft` border), `focus` deep blue on the proposed fusion/adapter module, 3D tensor stacks in crisp monochrome/focus tints, and single-hue or perceptually uniform heatmaps.
- **Theoretical / Optimization Papers:** Pure monochrome (`ink` on `white`) + single `focus` highlight, orthogonal routing, explicit math on edges.

---

## 6. Common Pitfalls to Avoid

- **Rainbow / over-colored boxes:** Giving every stage and every box its own hue (blue + yellow + purple + teal + red). Strip neutral boxes back to white + `ink` outline!
- **Loud tinted zone backgrounds:** Saturated blue/violet/yellow `enclose` fills competing with foreground content. Keep zones `white` or `#F8F9FA` with muted dashed borders.
- **PowerPoint defaults & heavy borders:** Thick `2pt` pure-black borders on saturated fills.
- **Embedded figure titles/captions:** Putting `"Figure 1: ..."` inside the graphic.
- **Color-only differentiation:** Using solid lines of different colors instead of solid vs. dashed (fails grayscale printing and colorblind readers).
- **Redundant legends:** Big legend boxes repeating labels already written directly on nodes/zones.
