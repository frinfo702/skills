# Critic Evaluation Rubric & Fletcher Diagnostic Table

Adapted from PaperVizAgent's 4-dimension referenced evaluation rubric (`prompts/diagram_eval_prompts.py`), paired with concrete Fletcher code fixes so every Critic finding translates directly into a surgical `.typ` edit.

---

## 1. The Four Dimensions & Veto Rules ("Red Lines")

A diagram passes (`"No changes needed."`) **only when it commits zero Veto Rule violations** across all four dimensions and exhibits clean visual balance.

### Dimension 1: Faithfulness *(highest priority)*
Does the diagram faithfully reflect the Methodology Section and adhere strictly to the Figure Caption's scope? Smart simplification of standard boilerplate sub-modules is encouraged; fabrication or logical inversion is forbidden.

**Veto Rules:**
1. **Major Hallucination:** Inventing modules, agents, datasets, or connections not supported by the methodology text.
2. **Logical Contradiction:** Reversing data direction, bypassing an essential stage, or omitting a core connection described in the method.
3. **Scope Violation:** Visualizing content outside the figure scope specified by the caption.
4. **Gibberish / Broken Notation:** Typos, garbled labels, or malformed Typst math (`$...$` syntax artifacts).

### Dimension 2: Conciseness
Does the diagram achieve a high visual signal-to-noise ratio through structural shorthand (blocks, arrows, zones) and concise keywords rather than walls of text?

**Veto Rules:**
1. **Textual Overload:** Boxes containing full sentences, verb-heavy prose, or lengthy descriptions (> 15 words). *(Exception: explicit sample data / input-output example boxes when required by the caption.)*
2. **Literal Copying:** A "box-ified" copy-paste of paragraphs from the methodology section with no visual abstraction.
3. **Math Dump:** Cluttering conceptual blocks with raw multi-line derivations instead of clean symbol annotations ($x, \theta, \mathcal{L}$).

### Dimension 3: Readability
Can a reader trace the architecture and data flow at a glance without visual interference?

**Veto Rules:**
1. **Extraneous Meta-Elements:** Figure title or full caption text (`"Figure 1: ..."`) rendered inside the image, watermarks, or accidental duplicate titles. *(Subfigure tags `(a)`, `(b)` and intentional repeated modules for iterations are allowed.)*
2. **Occlusion & Overlap:** Text labels colliding with arrows, node borders, zone borders, or other text.
3. **Chaotic Routing:** Spaghetti loops, arrows passing straight through unrelated nodes, or excessive ambiguous crossings.
4. **Illegible Font Size:** Text too small to read comfortably at target print/slide width, or wildly inconsistent font sizes across peer nodes.
5. **Low Contrast:** Light text on light pastel fills, or faint strokes that vanish at print scale.
6. **Inefficient Non-Rectangular Layout:** Protruding components creating huge blank corners / dead zones (wastes vertical space in LaTeX papers).
7. **Black Background:** Dark/black page backgrounds unsuitable for academic publications.

### Dimension 4: Aesthetics
Does the diagram meet top-tier conference visual polish (visual hierarchy, harmonious colors, consistent geometry, clean typography)?

**Veto Rules:**
1. **Rendering Artifacts:** Clipped borders, broken/unaligned group boxes, missing font fallbacks, or multi-page overflow.
2. **Over-Coloring / Color Disharmony:** Jarring neon colors, red-vs-green pairs, **or rainbow over-coloring** where neutral boxes and background zones each use competing hues (blue + amber + purple + teal + red in one diagram) instead of calm white/ink neutrals + one focus color (`#004488`) and at most 1–2 muted accents where strictly needed.
3. **Amateurish Styling:** Heavy pure-black outlines on harsh PowerPoint defaults, inconsistent corner radii across identical node types, or gratuitous clip-art.
4. **Inconsistent Typography:** Mixing unrelated font families (e.g., serif module names alongside sans-serif ones) or hyphenated broken words inside boxes.
5. **Black Background:** Unprofessional dark canvas for print venues.

---

## 2. Fletcher & CeTZ Visual Defect → Exact Code Fix Table

When inspecting `round_<r>-1.png` (and `round_<r>_debug-1.png` when needed), **explicitly scan every edge label against every dashed zone border** and check outer margins for clipping. Map every visual symptom directly to a surgical `.typ` patch:

| Visual Symptom in Render | Likely Cause in `.typ` | Exact Surgical Patch |
|---|---|---|
| Diagram looks too colorful / "rainbow" boxes competing for attention | Decorative hues assigned to neutral modules and zone backgrounds | Reset neutral boxes to `fill: white, stroke: 0.95pt + rgb("#22272E")`, set `enclose` zones to `fill: rgb("#F8F9FA")` + muted dashed stroke, and reserve `rgb("#004488")` (`#EDF3F9` fill) strictly for the novel/key component |
| Edge label touches or crosses a dashed `enclose` zone border | `spacing` or `enclose` `inset` too tight near zone perimeter | Widen `spacing` or `enclose` `inset`, shift label to `label-side: right`/`left` inside/outside the zone, shorten to 1 compact line, or add `label-fill: white` |
| Wide zone/panel title pushes diagram past `5.5in`/`6.75in` page edge | Wide title `node((col, y), [...])` inflates Fletcher column `col` | Replace with zero-footprint `floating-title(...)` / `stage-pill(...)` from `fletcher-guide.md` |
| Text wraps awkwardly onto 2–3 narrow lines inside a box | Fixed `width:` too narrow for bold label | Increase `width:` on that helper/node, omit `width:` (use `inset: 7pt`), or shorten label + add explicit `\ ` line break |
| Word split with a hyphen (`Architec-ture`) | Typst hyphenation enabled by default | Add `#set text(hyphenate: false)` near top of file |
| Group title sits on top of enclosed nodes | Title placed as content inside `node(enclose: ...)` | Remove content from `enclose` node; use `floating-title((mid_x, top_y - 0.78), ...)` |
| Arrow passes directly through an intermediate node | Straight edge connects non-adjacent nodes | Route with explicit intermediate vertices `edge(<a>, (x, y_bus), (x2, y_bus), <b>, "-|>")` or add `bend: 35deg` / `-35deg` |
| Two crossing arrows look merged | Intersecting edges lack visual separation | Add `crossing: true, crossing-thickness: 4` on the foreground edge, or reorder rows to eliminate the crossing |
| Forward pass and gradient/feedback arrows look identical | Same stroke/tip used for both | Make auxiliary/gradient edges dashed (`"--|>"`, `stroke: (paint: muted, dash: "dashed")`) and curve/bus feedback arcs cleanly |
| Diagram spills onto 2 pages (`overflow: true`) or CeTZ clips left/right | Total grid width or CeTZ `x` span exceeds fixed `#set page(width: ...)` | For Fletcher: use `floating-title`, tighten `spacing`, or fold into 2 rows. For CeTZ: shrink `length:` (e.g., `1cm` → `0.9cm`) or tighten `x` coordinates to fit `5.5in ≈ 13.6cm` / `6.75in ≈ 16.7cm` |
| CeTZ text label overlaps nearby shape or curve | Default center anchor placed on top of geometry | Set `anchor: "north"` / `"south"` / `"east"` / `"west"` with a `0.12–0.20` offset from the shape edge |
| Font looks like unexpected serif (`font_warnings` non-empty) | Specified font not installed locally | Switch `font:` to one of `available_preferred_fonts` reported by `compile_fletcher.py --check-env` |
| Clipped outer stroke or curved arc at page edge | `margin` too small or `bend:` arc bulges past bounds | Increase `#set page(margin: 10pt)` (or `12pt`) or reduce `bend` angle |
