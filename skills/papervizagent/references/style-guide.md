# Academic Illustration Style Guide (Calm Warm Palette → Typst / Fletcher / CeTZ)

Adapted from PaperVizAgent's NeurIPS 2025 academic design standards, with a **calm, warm, muted palette inspired by Anthropic's visual identity** (clay, sky, olive, ochre and heather on warm neutrals).

> **Workspace override rule:** If the user's project already has a `theme.typ` or established color semantics across other figures in the paper, follow the workspace theme instead of introducing a second palette.

---

## 1. Visual Philosophy: Calm Color, Not No Color

The target is the middle ground between two failures:
- **Too loud:** saturated or neon hues, or every box in a different color (blue + yellow + purple + teal + red), so nothing stands out.
- **Too bare:** a black-and-white / grayscale wireframe with one lonely accent. It reads as unfinished and gives the reader no grouping cues. **Do not produce monochrome figures.**

**Default rule for every diagram:**
1. **Use color to show structure.** Components that play the same role share one muted hue (e.g., all encoders sky, all memory/data olive, all agents/tools ochre). A typical architecture diagram uses **2–4 palette hues**, each with a stated meaning, plus the warm neutrals.
2. **Neutral is warm, not black-and-white.** Generic or boilerplate parts (inputs, outputs, glue steps) use a soft `sand` fill with an `ink-soft` outline and `ink` text — not white boxes with hard black outlines.
3. **Clay is the emphasis.** The novel / proposed / key component gets `clay` stroke + `clay-fill`, so the eye lands on the contribution first. Keep exactly one clay focus region per figure.
4. **Zones are lightly tinted.** Grouping containers (`enclose` / panels) use `paper` (warm off-white) or the very light tint of their group's hue, with a thin dashed `line-c` border — never a saturated block.
5. **Never neon, never pure black.** All hues are muted, mid-lightness colors; text and lines are warm near-black `ink`, not `#000000`.
6. **Brick red only for bad things** (error, loss, eviction, failure), always paired with a dashed line or cross mark so it is not confused with clay.

### Default Palette: Calm Warm (Anthropic-Inspired)

```typst
// Warm neutrals
#let ink        = rgb("#2B2A27")  // text, main arrows (warm near-black, never pure black)
#let ink-soft   = rgb("#5E5D59")  // subtitles, outlines of neutral boxes, secondary labels
#let muted      = rgb("#8F8D86")  // dashed auxiliary arrows, axis ticks
#let line-c     = rgb("#CFCCC2")  // zone borders, dividers
#let faint      = rgb("#E8E6DC")  // grids, masked matrix cells, freed slots
#let sand       = rgb("#F0EEE6")  // fill of neutral / generic boxes
#let paper      = rgb("#FAF9F5")  // zone background (page itself stays white)

// Emphasis: ours / novel / trainable / key mechanism (one region per figure)
#let clay        = rgb("#C6613F")
#let clay-fill   = rgb("#F6E4DC")

// Role hues: assign one meaning each, consistently across the paper
#let sky         = rgb("#4F7FAE")  // e.g., encoders, perception, input stream
#let sky-fill    = rgb("#E2EBF4")
#let olive       = rgb("#6B7F4E")  // e.g., memory, data, retrieval, frozen backbone
#let olive-fill  = rgb("#E8EDE0")
#let ochre       = rgb("#B98A3E")  // e.g., agents, tools, a second tracked stream
#let ochre-fill  = rgb("#F5ECDA")
#let heather     = rgb("#7D76A8")  // e.g., a fourth role, only if needed
#let heather-fill = rgb("#ECEAF3")

// Negative / failure / loss / eviction ONLY
#let problem      = rgb("#A23E3E") // brick red
#let problem-fill = rgb("#F5E1DF")
```

Fills are the same hue lightened to roughly 85–90%; strokes use the full hue at 0.9–1.25pt. Body text inside a tinted box stays `ink`.

> **Opt-in modes:** Use brighter, more saturated pastels only if the user asks for a colorful style. Use a black-and-white figure only if the user or venue explicitly requires grayscale printing.

---

## 2. Shapes & Containers ("Softened Geometry")

Use **role hue + shape + stroke weight** together to distinguish roles:

| Semantic Role | Fletcher / CeTZ Styling |
|---|---|
| Standard / generic process / layer | `shape: rect`, `fill: sand`, `stroke: 0.9pt + ink-soft`, `corner-radius: 5pt` |
| Component with a role (encoder, agent, tool, ...) | `shape: rect`, `fill: <role>-fill`, `stroke: 0.95pt + <role>`, `corner-radius: 5pt` (same role → same hue) |
| Novel / proposed / trainable component | `shape: rect`, `fill: clay-fill`, `stroke: 1.25pt + clay`, `corner-radius: 5pt` |
| Frozen / static / external module | Its role hue (or `sand`) with a thinner `0.8pt` stroke, plus a small snowflake badge in that hue |
| Data / tensor / prompt / matrix | Tight-radius `rect` (`corner-radius: 1.5pt`), `fill: olive-fill` (or `sand`), `stroke: 0.9pt + olive` |
| Database / memory / replay buffer / KV store | `shape: fletcher.shapes.cylinder`, `fill: olive-fill`, `stroke: 0.9pt + olive` |
| Decision / router / gate | `shape: fletcher.shapes.diamond`, `fill: ochre-fill`, `stroke: 1pt + ochre` (or `clay` if it is the key gate) |
| Math operator ($+$, $\times$) | Small `shape: circle`, `inset: 2pt`, `fill: white`, `stroke: 0.9pt + ink-soft` |
| Logical stage / scope / phase (`enclose`) | `fill: paper` (or the group's light tint), `stroke: (paint: line-c, dash: "dashed", thickness: 0.85pt)`, `corner-radius: 8pt`, `layer: -1` |
| Macro–Micro breakout | Outer macro panel in role hues + clay-highlighted target block connected via dotted `clay` callout lines to a clay-bordered zoomed micro panel |

---

## 3. Lines & Arrows (Flow Semantics)

Distinguish flow types by **line style** (solid vs. dashed, straight vs. curved) so every figure stays 100% readable in grayscale print as well as color:

| Flow Type | Edge Style |
|---|---|
| Forward data / main pipeline | Solid `ink-soft` or `ink` (`stroke: 1pt + ink-soft`, `"-|>"`) |
| Auxiliary flow (gradients, skip connections, retrieval lookup) | Dashed muted (`stroke: (paint: muted, thickness: 0.95pt, dash: "dashed")`, `"--|>"`) |
| Feedback / critique / iterative loop | Dashed `clay` (or `problem` if error-driven) curved or orthogonal return bus (`"--|>"`) |
| Key highlighted output / accepted path | Solid `clay` (`stroke: 1.15pt + clay`, `"-|>"`) |
| Stream belonging to one role | Solid stroke in that role's hue (still distinguished by line style where streams cross) |
| Crossing edges | `crossing: true, crossing-thickness: 4` (white halo so paths never look merged) |

---

## 4. Typography & Math Separation

- **Module & zone labels:** Clean **Sans-Serif** (`"Inter"`, `"Helvetica Neue"`, `"Roboto"`, or `"Arial"` — verify installed fonts with `--check-env`).
  - Zone headers: bold `ink` text, or a pill in the zone's light tint with its role-hue stroke (`sand` + `line-c` for neutral zones), placed cleanly *above* the zone via `floating-title` / `stage-pill`.
  - Node titles: semibold/bold `ink`; optional short subtitle in smaller `ink-soft`.
- **Mathematical variables:** Always use Typst math mode (`$x$`, `$theta$`, `$cal(L)_"CE"$`, `$Q, K, V$`), which renders in italic math serif. Typst math uses bare identifiers (`theta`, `nabla`, `sigma`, `cal(L)`, `plus.o`, `times.o`, `dot.o`), **not** LaTeX backslashes (`\theta`).
- **Printed legibility:** Paper figures at final `\linewidth`: **7.5–9 pt** (never below 6.5 pt); slides: **≥ 18 pt**. Always set `set text(hyphenate: false)`.
- **Background:** Page is white (`fill: white`); warmth comes from `paper` zones and tinted boxes. Never dark/black backgrounds.

---

## 5. Domain-Specific & Atypical Visual Styles

- **Agent / LLM / Multi-Agent Papers:** Agents/LLMs in `ochre`, tools/environment in `sky`, memory/context in `olive`, the novel module or loop in `clay`; `paper` stage enclosures with tinted `stage-pill` headers; small CeTZ vector status badges (snowflake for Frozen, spark for Trainable) in the hue of their box.
- **Systems / Long-Context / Efficiency Papers (CeTZ):** Aligned horizontal token/memory strips; evicted/inactive slots in `faint` with dashed `muted` border, retained key tokens in `clay`, and other retention classes in `ochre` / `sky` / `olive` (e.g., Sink vs. Heavy Hitter vs. Recent).
- **Computer Vision / 3D / Multimodal Papers (Hybrid / CeTZ):** One hue per modality (e.g., vision `sky`, text `ochre`), frozen backbones in their modality hue with thin strokes, `clay` on the proposed fusion/adapter module, 3D tensor stacks in tints of their hue, and single-hue or perceptually uniform heatmaps.
- **Theoretical / Optimization Papers:** `sand` boxes and `ink` math with `sky` / `olive` for the objects being related and `clay` on the key step; orthogonal routing, explicit math on edges.

---

## 6. Common Pitfalls to Avoid

- **Rainbow / over-colored boxes:** Giving every box its own hue with no meaning behind it. Colors follow roles: same role, same hue; generic parts `sand`.
- **Monochrome wireframes:** Everything white with black outlines and one accent. Give roles their hues and neutral boxes the warm `sand` fill.
- **Loud tinted zone backgrounds:** Saturated `enclose` fills competing with foreground content. Keep zones `paper` or a very light tint with a thin dashed `line-c` border.
- **Cold or harsh tones:** Pure black `#000`, neon, or cold blue-grays. Stay within the warm palette.
- **PowerPoint defaults & heavy borders:** Thick `2pt` pure-black borders on saturated fills.
- **Embedded figure titles/captions:** Putting `"Figure 1: ..."` inside the graphic.
- **Color-only differentiation:** Using solid lines of different colors instead of solid vs. dashed (fails grayscale printing and colorblind readers).
- **Redundant legends:** Big legend boxes repeating labels already written directly on nodes/zones.
