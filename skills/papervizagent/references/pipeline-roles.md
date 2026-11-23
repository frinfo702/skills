# PaperVizAgent Pipeline Roles (Fletcher + CeTZ Edition)

This reference adapts Google Research's PaperVizAgent (PaperBanana) multi-agent roles to synthesize **Typst + Fletcher and/or CeTZ vector illustrations** instead of Gemini Nano Banana raster images.

---

## 1. Retriever

**Goal:** Identify 1–3 structural and aesthetic reference examples and pick the right rendering engine (**Fletcher**, **CeTZ**, or **Hybrid**).

**Priority order:**
1. **Workspace continuity (highest priority):** Scan the target paper/slide directory for existing `.typ` figures or a shared `theme.typ`. If present, extract the exact palette, font family, stroke weights, corner radii, and helper conventions so the new figure matches the rest of the paper seamlessly.
2. **Engine & archetype match:** Match visual intent first and domain second:
   - *Pipeline / Architecture / Agent Loop / Macro–Micro* → **Fletcher** (`references/fletcher-guide.md`)
   - *Architecture + embedded 3D tensor stacks, vector Frozen/Trainable badges, or mini heatmaps* → **Hybrid (Fletcher + CeTZ)** (`references/fletcher-guide.md` + `references/cetz-guide.md`)
   - *Atypical / spatial visual (KV-cache / memory layout, token eviction strip, 3D tensor stack, attention matrix, latent-space manifold, timeline, conceptual teaser)* → **CeTZ** (`references/cetz-guide.md`)
3. **User-supplied references:** If the user provides reference diagrams or paper figures, inspect them to capture layout rhythm, grouping style, and visual density (never copying content verbatim).

**Output (`<work>/retrieval.md`):** Selected engine (`fletcher` | `cetz` | `hybrid`), workspace conventions, and chosen archetype(s).

---

## 2. Planner

**Goal:** Translate the Methodology Section and Figure Caption into a complete, unambiguous **Vector Blueprint** (`<work>/blueprint.md`).

**Rules:**
- **Fidelity first:** Represent every critical component, spatial relationship, and interaction implied by the Methodology + Caption. Do not fabricate modules or reverse data flow. Smart simplification of standard boilerplate sub-layers into single clean blocks is encouraged.
- **Caption exclusion:** Never include the figure title or caption text (e.g., `"Figure 1: Overview of..."`) as a node or heading inside the diagram.
- **Conciseness:** Keep labels short noun phrases (ideally 1–5 words; never >15 words unless displaying an explicit input/output data example). Move prose explanations to the paper's caption.
- **Explicit geometry:**
  - *For Fletcher:* specify grid coordinates `(col, row)` (rows grow downward), named node IDs (`<enc>`, `<attn>`, `<loss>`), `enclose` zones with zero-footprint `floating-title` / `stage-pill` headers, and explicit width budget fitting inside venue `\linewidth`.
  - *For CeTZ:* specify canvas `cm` bounds matching venue `\linewidth` (`5.5in ≈ 13.6cm`, `6.75in ≈ 16.7cm`), panel/region coordinates (`y` grows upward), and exact spatial primitives (token strips, matrices, 3D tensor stacks, curves).

**Required Blueprint Structure (`<work>/blueprint.md`):**
```markdown
## Scope & Reading Flow
- Visual intent: <one sentence summarizing what the figure communicates>
- Reading direction: Left-to-Right | Top-to-Bottom | Macro-Left / Micro-Right
- Target medium & size: <e.g., NeurIPS full width 5.5in | ICML single-col 3.25in | auto>

## Nodes
| ID | Grid (col, row) | Label (exact English text / Typst math) | Role / State | Shape |
|---|---|---|---|---|
| `<in>` | `(0, 0)` | `Input $x$` | Data | `rect` (sharp) |
| `<enc>` | `(1, 0)` | `Frozen Encoder` | Frozen module | `rect` (rounded) |
| `<mem>` | `(2, 1)` | `Replay Buffer` | Storage | `cylinder` |

## Zones / Groups (`enclose`)
| Zone Name | Enclosed Nodes | Style Intent | Caption Placement |
|---|---|---|---|
| `Stage 1: Retrieval` | `<in>, <enc>` | Soft pastel / dashed scope | Separate node at `(0.5, -0.65)` |

## Edges
| From | To | Route / Geometry | Line Semantics | Label / Operator |
|---|---|---|---|---|
| `<in>` | `<enc>` | straight | Forward data (solid) | — |
| `<loss>` | `<enc>` | `bend: -35deg` or bottom bus | Gradient update (dashed) | `$nabla_theta$` |
```

---

## 3. Stylist

**Goal:** Enrich `<work>/blueprint.md` with concrete Typst + Fletcher aesthetic tokens (`<work>/styled_spec.md`) without altering semantics, logic, or structure.

**Rules:**
1. **Preserve semantic content:** Do not add, delete, or reorder nodes/edges. You may tighten verbose labels slightly while verifying against the methodology section.
2. **Respect existing style:** If the Retriever found a workspace `theme.typ`, use its palette and font choices. Otherwise apply `references/style-guide.md` (**calm restraint by default**).
3. **Enforce color restraint:** Keep standard/neutral components white with `#22272E` ink outlines and keep grouping zones neutral (`white` or `#F8F9FA` with muted dashed gray borders). Spend the **one primary focus hue (`#004488`)** strictly on the novel/key component, and add at most 1–2 muted secondary hues (`#C28A2E` ochre, `#3A8C80` teal) only when distinct categories genuinely require color encoding (e.g., heatmap roles). Reserve muted rose (`#B84A5B`) strictly for failure/loss/eviction. Never give every module its own color.
4. **Strict typography & math separation:** Sans-serif for module/zone labels; Typst math mode (`$x, theta, cal(L)$`) only for mathematical variables and operators (`$plus.o$`, `$times.o$`, `$dot.o$`, or `$+$` inside a `circle` node). Never use LaTeX backslashes inside Typst math.
5. **Icon discipline:** Use minimal monochrome/muted CeTZ vector badges only when they carry conventional meaning (snowflake = frozen, spark = trainable). Avoid noisy emojis or clip-art.

**Output (`<work>/styled_spec.md`):** The finalized blueprint enriched with exact Typst declarations:
- Page size & margins (`width`, `height`, `margin`, `fill: white`)
- Font family (verified via `--check-env`), base size, and header/label hierarchy
- Exact hex color table (`zone-*`, `active-*`, `frozen-*`, `highlight-*`, `ink`, `muted`)
- Node helper definitions (`corner-radius`, `stroke`, `inset`, fixed vs. elastic `width`/`height`)
- Edge stroke weights, arrowhead styles (`-|>`, `--|>`), and `spacing: (col-gap, row-gap)`

---

## 4. Visualizer (Fletcher Vector Synthesizer)

**Goal:** Translate `<work>/styled_spec.md` into clean, modular, compiling Typst + Fletcher code (`round_0.typ`), and in subsequent rounds apply **surgical patches** (`round_<r>.typ` → `round_<r+1>.typ`).

**Round 0 synthesis rules:**
- Pin the verified `@preview/fletcher` version at the top of the file.
- Define clean local helper functions (`#let proc(...)`, `#let data(...)`, `#let zone(...)`, `#let op(...)`) so the `#diagram(...)` block reads cleanly like the diagram's semantic structure.
- Name every node (`name: <id>`) and connect edges by name or explicit bus vertices.
- Put zone captions in dedicated nodes *outside/above* `enclose: (...)` — never inside the `enclose` node's body (which places text in the center over enclosed members).
- Run the Inner Compile & Preflight Gate immediately via `scripts/compile_fletcher.py`. If compilation fails or `page_count > 1`, fix the exact error/overflow immediately before handing off to the Critic.

**Refinement round (`r >= 1`) patching rules:**
- Copy `round_<r>.typ` to `round_<r+1>.typ`.
- Apply **only the targeted patches** requested by the Critic (coordinate shifts, spacing tweaks, intermediate edge vertices, label tightening, color/contrast fixes).
- Preserve all nodes, styles, and edges that the Critic did not flag. Never rewrite from scratch unless the Critic explicitly reports a fundamental layout-topology failure.

---

## 5. Critic

**Goal:** Conduct a rigorous dual-modality audit of `(round_<r>-1.png, round_<r>.typ)` against the original Methodology Section, Figure Caption, and `references/critique-rubric.md`.

**Inspection protocol:**
1. **Visually inspect `round_<r>-1.png`** (open/read the image directly). Look for visual defects that code alone hides: clipped text, unwanted line wraps inside boxes, labels colliding with lines or group borders, edges crossing through nodes, unbalanced empty corners, low contrast, illegible font size.
2. **Use Fletcher's `debug: 2` overlay when layout is unclear:** Run
   ```sh
   python3 <skill-dir>/scripts/compile_fletcher.py <work>/round_<r>.typ --debug 2
   ```
   and inspect `round_<r>_debug-1.png` to read exact grid coordinates `(col, row)`, bounding boxes, and anchor offsets.
3. **Read `round_<r>.typ`** to verify exact spelling, math notation (`$...$`), consistent styling tokens, and clean structure.
4. **Score all 4 dimensions & Veto Rules** (`references/critique-rubric.md`):
   - Faithfulness
   - Conciseness
   - Readability
   - Aesthetics

**Output format (strictly actionable):**
If all 4 dimensions pass with zero Veto violations and clean visual balance:
```json
{
  "verdict": "PASS",
  "critic_suggestions": "No changes needed.",
  "patches": []
}
```
Otherwise, list concrete, code-level patches ordered by severity (Veto violations first):
```json
{
  "verdict": "REVISE",
  "veto_violations": ["Readability: edge label 'Feedback' overlaps dashed zone border"],
  "critic_suggestions": "1. Widen horizontal spacing from 1.2cm to 1.8cm...\n2. Route gradient edge via bottom bus...",
  "patches": [
    {
      "target": "spacing in #diagram(...)",
      "issue": "Edge label overlaps dashed enclose border between <dec> and <eval>",
      "fix": "Change `spacing: (1.2cm, 1.0cm)` to `spacing: (1.8cm, 1.1cm)` and add `label-fill: white` on edge(<dec>, <eval>)"
    }
  ]
}
```

---

## 6. Polish (`polish` mode)

**Goal:** Convert an existing raster diagram, hand sketch, draw.io export, or rough `.typ` figure into a crisp, publication-ready Fletcher vector diagram.

**Procedure:**
1. Inspect the input diagram (image or `.typ`) plus any provided methodology/caption.
2. Run a style-and-rubric audit against `references/style-guide.md` and `references/critique-rubric.md`, listing up to 10 concrete improvements (fixing muddy colors, inconsistent shapes, overlapping arrows, embedded titles, mixed fonts, low-res raster artifacts) while **strictly preserving semantic logic and structure**.
3. Extract the diagram into `<work>/blueprint.md` (Planner format) + `<work>/styled_spec.md` (applying the improvements).
4. Enter Stage 4 (**Fletcher Visualizer ↔ Critic Loop**) and export crisp `.typ`, `.pdf`, and `.svg`.
