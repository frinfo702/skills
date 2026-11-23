---
name: papervizagent
description: >-
  Generate and iteratively refine publication-ready vector academic illustrations (PDF, SVG, PNG) using Google Research's PaperVizAgent (PaperBanana) multi-agent pipeline with Typst + Fletcher (@preview/fletcher) for diagrams and CeTZ (@preview/cetz) for atypical/bespoke academic visuals (tensor stacks, memory/KV-cache layouts, token strips, attention grids, latent manifolds, conceptual teasers, and hybrid vector badges), replacing Gemini Nano Banana raster image generation. Use whenever turning a paper's methodology section, algorithm, system architecture, memory/token layout, or figure caption into a publication-ready vector figure; when polishing an existing raster/sketch diagram into crisp vector graphics; or when the user mentions PaperVizAgent, PaperBanana, method diagram, architecture figure, teaser figure, Fletcher, or CeTZ — e.g. "PaperVizAgentで図を作って", "手法の概要図をベクターで", "論文のメソッド図を生成して", "CeTZで図を描いて", "この図を論文品質に清書して", "/papervizagent".
compatibility: Requires Typst CLI (`typst`) and Python 3. Uses `@preview/fletcher` and `@preview/cetz` (Typst Universe).
---

# papervizagent

Automated academic illustration generation modeled on Google Research's **PaperVizAgent** (formerly **PaperBanana**), replacing Gemini Nano Banana raster image generation with **Typst + Fletcher** (`@preview/fletcher`) and **CeTZ** (`@preview/cetz`) so every output is crisp, editable, font-embedded **vector graphics** (`.pdf` and `.svg`).

Why this works better than raster generation: instead of regenerating pixels blindly from prose every round, the pipeline separates *what to show* (Planner) from *how it looks* (Stylist) from *deterministic vector synthesis* (Fletcher/CeTZ Visualizer), and overrides PaperVizAgent's original `_run_critic_iterations` loop into a **compile-preflight + dual visual/source critique + surgical `.typ` patch loop**.

## Renderer Selection (Fletcher vs. CeTZ vs. Hybrid)

Pick the simplest engine that faithfully expresses the figure's visual style:

| Visual Style / Figure Type | Engine | Reference to Read |
|---|---|---|
| Box-and-arrow diagrams: method pipelines, system architectures, agent loops, state machines, macro–micro module breakouts | **Fletcher** (`@preview/fletcher`) | `references/fletcher-guide.md` |
| Architecture diagrams needing custom mini-visuals (3D tensor blocks, vector Frozen/Trainable badges, mini attention maps or token strips inside nodes) | **Hybrid** (`@preview/fletcher` + `@preview/cetz`) | `references/fletcher-guide.md` + `references/cetz-guide.md` |
| Atypical / spatial academic visuals: timelines, memory & KV-cache layouts, token eviction strips, 3D feature stacks & camera frustums, attention heatmaps, latent-space manifolds, before/after swimlanes, bespoke Figure 1 teasers | **CeTZ** (`@preview/cetz`) | `references/cetz-guide.md` |
| Statistical data plots (line, scatter, bar, trade-off) | **cetz-plot** (`@preview/cetz-plot`) or vector `matplotlib` PDF (`pdf.fonttype: 42`) | Same loop, data-faithful Critic |

## Modes

| Mode | Pipeline | When to use |
|---|---|---|
| `full` *(default)* | Retriever → Planner → Stylist → **Vector Loop** → Export | New method overview, architecture, atypical teaser, or spatial illustration from text/caption |
| `quick` | Retriever → Planner → **Vector Loop** → Export | Workspace already enforces a strict `theme.typ` or layout is structurally simple |
| `polish` | Existing image/sketch/`.typ` → Style Critique → **Vector Loop** → Export | Upgrading a rough sketch, raster image, draw.io export, or existing `.typ` figure into publication-quality vectors |
| `candidates` | Run 2–3 distinct layout topologies/styles in parallel (via subagents), compare, and export the strongest | Complex Figure 1 / teaser figures where the best visual framing is not obvious upfront |

## Bundled resources

Read only what the current stage needs:

- `references/pipeline-roles.md` — Role specifications for Retriever, Planner, Stylist, Visualizer, Critic, and Polish (covering Fletcher, CeTZ, and Hybrid).
- `references/style-guide.md` — NeurIPS 2025 academic visual aesthetic guide translated into Typst/Fletcher/CeTZ tokens (palettes, shapes, pill headers, vector status badges, strokes, typography, pitfalls).
- `references/fletcher-guide.md` — Verified `@preview/fletcher` syntax, zero-footprint `floating-title` helper, venue widths, 5 diagram archetypes, and Typst 0.15 gotchas.
- `references/cetz-guide.md` — Verified `@preview/cetz` syntax, coordinate budgets in `cm`, 4 atypical visual archetypes (memory/token strip, 3D tensor stack, attention grid, hybrid vector badges), and CeTZ gotchas.
- `references/critique-rubric.md` — PaperVizAgent's 4-dimension Veto-Rule evaluation rubric (Faithfulness, Conciseness, Readability, Aesthetics) + Fletcher/CeTZ visual-defect → code-fix table.
- `scripts/compile_fletcher.py` — Unified Typst compiler, environment checker (`--check-env` for Fletcher + CeTZ + fonts), multi-page overflow preflight checker, non-destructive `--debug 2` grid renderer (for both Fletcher and CeTZ), and PDF/SVG/PNG exporter.

## Inputs & workspace setup

Before starting, collect (or infer from context):
1. **Methodology / source content** — paper method section, algorithm/system spec, or existing figure (for `polish`).
2. **Figure caption / visual intent** — defines the figure's scope. **Never render the figure title or caption text inside the image**; captions live in LaTeX/Typst/slides.
3. **Target medium & width** — paper venue `\linewidth` (e.g., NeurIPS/ICLR `5.5in`, ICML/CVPR `3.25in` single-col or `6.75in` full-width, ACL `16cm`), slide slot (`12.33in × 4.9in`), or `auto` tight bounding box with clean margin.
4. **Output path & formats** — target `.typ` plus vector `.pdf` and/or `.svg` (default: `.typ`, `.pdf`, `.svg`, and `.png` preview).

Keep intermediate scratch files (`blueprint.md`, `styled_spec.md`, `round_0.typ`, `round_0-1.png`, `round_0_debug-1.png`, ...) in `<work>` (e.g., `/tmp/papervizagent/<slug>/`) so the user's repo stays clean. Copy only final deliverables to the user's output path.

Check the local environment once per session:
```sh
python3 <skill-dir>/scripts/compile_fletcher.py --check-env
```
Pin the returned cached/recommended `@preview/fletcher` and `@preview/cetz` versions and confirmed installed fonts so compilation works offline with zero font-fallback warnings.

## Pipeline workflow

Read `references/pipeline-roles.md` for full role prompts and output schemas.

### Stage 1 — Retriever
Find 1–3 structural and aesthetic references before planning:
1. **Workspace first:** check for existing `.typ` figures or a shared `theme.typ` so the new figure matches the paper's palette, font, and stroke hierarchy.
2. **Engine & archetype match:** decide **Fletcher**, **CeTZ**, or **Hybrid** from the table above and pick the closest archetype(s) from `references/fletcher-guide.md` and/or `references/cetz-guide.md`.
3. **User references:** inspect any user-provided reference figures for layout rhythm and visual style.

### Stage 2 — Planner
Translate the methodology and caption into a structured **Vector Blueprint** (`<work>/blueprint.md`):
- **Engine choice & rationale:** Fletcher grid, CeTZ canvas, or Hybrid.
- **Semantic inventory:** every module, data artifact, spatial structure (tokens, tensors, memory blocks, manifolds), state (frozen vs. trainable), and math symbol required by the caption — nothing hallucinated, nothing critical omitted.
- **Conciseness pass:** distill prose into crisp short labels (noun phrases, ≤ ~6 words per box; full sentences only for explicit data examples). English labels by default.
- **Topology & coordinate plan:**
  - *Fletcher:* explicit `(col, row)` grid, named `<id>`s, `enclose` zones, and edge table distinguishing forward solid vs. auxiliary/feedback dashed arrows.
  - *CeTZ:* explicit `cm` bounding-box budget fitting inside the venue `\linewidth`, named panels/layers, and coordinate table (`y` grows upward).

### Stage 3 — Stylist *(skip in `quick` mode)*
Read `references/style-guide.md` and enrich `<work>/blueprint.md` into `<work>/styled_spec.md`:
- Preserve semantics, topology, and notation verbatim; refine visual encoding only.
- Apply the workspace `theme.typ` if present; otherwise apply the **calm warm palette** (Anthropic-inspired): one muted role hue per component role (`sky`, `olive`, `ochre`, `heather`; typically 2–4 per figure), warm `sand` fill for generic parts, `paper` zones with thin dashed borders, and `clay` reserved for the novel/key component. Avoid both rainbow boxes with no meaning and black-and-white wireframes.
- Lock exact Typst tokens: `rgb("#...")` hex palette, shape vocabulary, tinted pill headers / subtle CeTZ vector status badges, stroke weights (solid forward vs. dashed auxiliary/feedback), sans-serif label font vs. Typst math (`$x, theta, cal(L), plus.o, times.o, dot.o$`), and exact page width.

### Stage 4 — Overridden Vector Visualizer ↔ Critic Loop

Replaces PaperVizAgent's original `VisualizerAgent` (Nano Banana) + `_run_critic_iterations` prose-only retry loop with a **code-and-vision consolidated vector loop** (default `max_rounds = 3`, configurable):

```text
Round 0: Visualizer writes round_0.typ from styled_spec.md (or blueprint.md in quick mode)
         └─► Inner Gate: compile_fletcher.py --export png
             ├─ Compile error or page_count > 1 ─► Fast Compile-Repair (up to 3 attempts)
             └─ Pass (exit 0, 1 page) ─► best_round = 0

For round r = 0 .. max_rounds - 1:
  1. Critic inspects:
       • Rendered PNG preview (round_<r>-1.png)  [visually open & read image]
       • Typst source (round_<r>.typ)
       • Original methodology + caption
       • Debug overlay when layout/clearance is tight:
         run `compile_fletcher.py round_<r>.typ --debug 2` and inspect round_<r>_debug-1.png
         (injects Fletcher `debug: 2` OR a CeTZ 1cm coordinate grid non-destructively!).
     Critic checks all 4 PaperVizAgent dimensions & Veto Rules (`references/critique-rubric.md`),
     including edge-label-vs-zone-border clearance and fixed-width margin fit.
  2. Stopping check:
       • Zero Veto violations and crisp visual balance ─► Critic outputs "No changes needed." ─► BREAK.
       • Otherwise ─► Critic emits prioritized, code-actionable patches.
  3. Visualizer patches surgically:
       • Copy round_<r>.typ ─► round_<r+1>.typ and apply targeted edits (do NOT rewrite
         working regions from scratch).
       • Run Inner Gate (`compile_fletcher.py round_<r+1>.typ --export png`).
       • If Inner Gate still fails after fast compile-repair, roll back to `best_round` and BREAK.
       • Otherwise update `best_round = r + 1`.
```

**Subagent guidance:** Run roles inline for fast single-figure runs, or spawn a **fresh Critic subagent** per round on high-stakes figures (Figure 1 / camera-ready) to eliminate author confirmation bias. In `candidates` mode, run 2–3 parallel subagents with distinct layout topologies or styles (e.g., Fletcher pipeline vs. CeTZ spatial visual) and compare renders side by side.

### Stage 5 — Final Vector Export & Delivery
Compile `round_<best>.typ` to final vector formats:
```sh
python3 <skill-dir>/scripts/compile_fletcher.py <work>/round_<best>.typ \
  --out-dir <target-dir> --prefix <figure-name> --export pdf,svg,png --ppi 300
```
Copy `round_<best>.typ` to `<target-dir>/<figure-name>.typ` and verify `"ok": true`, `"page_count": 1`, `"font_warnings": []`. Deliver clickable links to the `.typ`, `.pdf`, `.svg`, `.png`, a concise summary of rounds/patches applied, and the LaTeX/Typst inclusion snippet.
