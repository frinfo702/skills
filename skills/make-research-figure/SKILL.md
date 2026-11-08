---
name: make-research-figure
description: >-
  Design, make and review figures for research papers and research talks: result plots (learning curves, ablations, comparisons, trade-offs, sweeps), method overview diagrams, Figure 1 teasers and result tables. Use when plotting experiment results for a paper or a talk, choosing a chart type, colors or sizes, exporting figures for LaTeX or camera-ready, or reviewing an existing figure. Trigger even when the skill is not named, e.g. "図作って", "論文の図", "このプロット綺麗にして", "このグラフどう？", "Figure 1 作りたい", "手法の概要図", "スライド用の図", "camera-ready の図", "/make-research-figure". Drawing itself is done with the draw-typst-figure skill; the deck around the figures with make-research-slides.
---

# make-research-figure

A figure is an argument: one claim, the evidence for it, and nothing that competes with it. Every rule below follows from that. Sizes, widths and plotting defaults are in `references/specs.md`.

**The image holds no title, caption, claim or explanation.** The figure's title, caption, slide title and claim line, takeaway sentence, highlighted numbers ("+11% acc., −21% FLOPs") and explanatory notes ("OpenAI-compatible API" under "HTTP server") belong in the text of the paper or the slide, where they can be edited without redrawing. Inside the image goes only what is needed to read it: names of components and groups, axis labels and ticks, legends, panel labels such as the benchmark name, and data marks. When unsure whether a piece of text belongs in the image, it doesn't.

**All text in figures and tables is English**, whatever the language of the paper, the talk or the conversation: labels, legends, annotations, table headers and cells. Figures get reused across Japanese and English papers, talks and posters, and an English figure never has to be redrawn. Captions and slide text follow the document's language.

**Draw with Typst.** Diagrams with fletcher, custom drawings with cetz, data plots with cetz-plot, using the `draw-typst-figure` skill. Use matplotlib only for data too large or dense for cetz-plot (thousands of points, images, heatmaps of real data) or a plot that already lives in the experiment code.

## Workflow

1. **Claim first.** Write the one sentence the figure must make the reader believe ("Our method matches the baseline at 1/4 of the compute"). It becomes the caption's first sentence in a paper and the claim line on a slide. If the user cannot state it, ask; a figure without a claim is a data dump.
2. **Medium.** Paper and slide are different designs: a paper is read up close at the reader's pace, a slide is seen from far away for a few seconds while someone talks (Rougier et al. 2014, rules 2–3). Never paste a paper figure onto a slide unchanged; re-render it.
3. **Form.** Pick the form from the comparison the claim makes (table below).
4. **Build at final size.** Set the figure size to the exact width it will be printed or projected (`references/specs.md`) and never scale it in LaTeX or PowerPoint. Font sizes are then what they say.
5. **Encode, then strip.** Map the claim to the most salient channel (position > length > color), then remove everything that does not support it.
6. **Check** against the checklist at the end.

## Choosing the form

| The claim compares | Use | Avoid |
|---|---|---|
| Methods on a few metrics, exact numbers matter | Table (booktabs, see below) | A bar chart that hides the numbers |
| Methods on a few metrics, the gap matters | Dot plot with CI, or bars starting at zero | Bars on a truncated axis |
| A quantity over training (steps, tokens, compute, wall clock) | Lines + shaded uncertainty band; say which x | Raw noisy curves only |
| Values across seeds or samples | Points (strip/swarm) + box or mean±CI | Mean-only bars with error bars ("dynamite plots") when n is small |
| A trade-off (accuracy vs. cost, size, latency) | Scatter with the Pareto front, direct labels, log x if it spans orders | Two separate bar charts |
| Ablation | Horizontal dot plot of the change from the full model, sorted | Unsorted grouped bars |
| A 2D sweep | Heatmap with the values written in cells if few | Rainbow colormap |
| Many tasks, aggregate | IQM with stratified bootstrap CI, performance profiles (rliable) | Mean over tasks with no uncertainty |
| A qualitative effect | Small multiples of examples, same layout per row, chosen by a rule you state | Cherry-picked singletons |

Bars encode length, so their axis must start at zero (proportional ink, Wilke ch. 17). If the interesting difference is small, switch to dots or lines rather than truncating bars. Use a log axis when values span orders of magnitude, and label it.

## Encoding

**Color.** Calm and meaningful: black on white for everything that is not the point, one focus color (deep blue) for ours or the new thing, further hues only where series must be told apart (ochre first), and a rose only for something bad. At most one series is gray. The palette and its rules are in `references/specs.md`. No red-vs-green pairs and no saturated red for emphasis; next to blue or green, red reads as "the bad one". One method keeps one color (and marker) across every figure of the paper and the talk. Sequential: viridis, cividis or a Crameri map (batlow). Diverging: a Crameri or RdBu map centered at a meaningful value (0, the baseline). Never jet/rainbow: its uneven lightness invents boundaries and it fails for color-vision deficiency (Crameri et al. 2020). Every heatmap or other color-mapped plot has a colorbar: the gradient with tick values at both ends and evenly spaced ones between, and the quantity with units ("Accuracy (%)"). Keep it minimal: a thin bar, no outline or tick marks, small muted labels, the quantity above the bar. Without it, the colors cannot be read as numbers. With shared color scales across panels, one colorbar serves them all. Never rely on color alone: add marker or line style, and check the figure in grayscale.

**Text.** Text in a printed figure should be about the size of the caption text (7–9 pt at final size, never below 6 pt), in the paper's font family. Same fonts in all figures. Axis labels are words with units ("Training tokens (B)"), never code names (`val_acc_ema`). Readable horizontal text; rotate tick labels only as a last resort (swap axes instead).

**Labels over legends.** With ≤ ~5 series, label lines directly at their ends. If a legend is needed, order it as the lines appear at the right edge and put it where it covers no data.

**Show only what differs.** In a before/after or method-vs-baseline diagram, leave out the steps both share (say so in the text). A box holds a name only; what the component does goes in the text.

**Strip.** Remove titles and notes inside the image, top/right spines, heavy grids, boxes around legends, 3D effects, and decimal digits beyond what the uncertainty supports.

## Uncertainty (ML specifics)

- Report n (seeds, runs, samples) and what the band or bar is: SD describes spread, SE and CI describe how well the mean is known. State which, in the caption (Cumming et al. 2007). Default: 95% CI over ≥ 3 seeds, 5+ when the gaps are small.
- Do not bold a "best" number whose interval overlaps the runner-up; say they are tied.
- If curves are smoothed, say so (e.g. EMA 0.9) and show the raw curve faintly underneath.
- Across many tasks or environments, use rliable (Agarwal et al. 2021): IQM, stratified bootstrap CIs, performance profiles, probability of improvement.

## Paper figures

**Caption.** First sentence is the claim. Then what is plotted, the x and y meaning if not obvious, n, and what the error bars are. A reader skimming figures and captions only should get the paper's argument.

**Tables.** booktabs rules (`\toprule \midrule \bottomrule`), no vertical rules, numbers right- or decimal-aligned, the same precision in a column, ± with the same precision as the value, best result bold only when it is significantly best, a units/direction marker in the header (Acc. ↑, Loss ↓).

**Method overview / Figure 1.** It must convey the core contribution in about ten seconds through the drawing itself, not through text or big numbers: headline results go in the abstract and the caption. Flow left to right (or top to bottom), one visual vocabulary (same shape and color for the same kind of thing), notation identical to the text, the novel part in the focus color and everything else gray, names only. Must remain readable at its printed width. Draw it with fletcher or cetz (`draw-typst-figure`) and export to PDF.

**Export.** Typst figures compile to PDF with fonts embedded. Plots as vector PDF; photos and dense scatter as raster (PNG ≥ 300 dpi, line art 600 dpi, or `rasterized=True` on the heavy artist inside a PDF). Embed TrueType fonts (`pdf.fonttype: 42`) and check with `pdffonts fig.pdf` that no Type 3 fonts remain; math text can still produce them. Each figure is a script that reads logged results and writes the file, so the figure can be regenerated after one more run; no manual post-editing that a rerun would lose.

## Figures for slides

The deck itself (structure, titles and claim lines, one idea per slide) is the `make-research-slides` skill. For the figure on a slide:

- **Size it to the slot** under the title and claim line (12.33 × 4.9 in on a 13.33 × 7.5 in slide, see make-research-slides) so it is placed at 100%.
- **Readable from the back.** Nothing below 18 pt at displayed size, including tick labels; lines 2–3 pt. Peyton Jones's test: readable when printed and laid on the floor.
- **Re-render, don't paste.** Fewer series, bigger fonts, highlight the one series that matters and gray the rest. For a build-up, export one image per step.
- **Tables.** Never paste a full paper table. Show the few rows that make the claim, with the key cell highlighted.
- High contrast (no light yellow on white; projectors wash out color), same colors per method as in the paper.

## Reviewing a figure

When asked to review, read the figure (render the PDF/PNG and look at it), then reply with:
1. The claim it appears to make, in one sentence. If it is unclear what it claims, that is the first finding.
2. Whether the figure supports that claim.
3. Findings ordered by how much they hurt the claim, each with a concrete fix (what to change and to what).

Do not list rules that already pass.

## Checklist

- [ ] One-sentence claim, stated in the caption or the slide's claim line, not in the image
- [ ] No title, caption, notes or highlighted numbers inside the image
- [ ] Form fits the comparison; bars start at zero
- [ ] Built at final width; text 7–9 pt (paper) or ≥ 18 pt (slide) at displayed size
- [ ] All text in figures and tables in English
- [ ] Axis labels in words with units; no code names
- [ ] Calm palette: black on white + one focus color; series distinguishable (at most one gray); colors keep their meaning; no red–green; readable in grayscale
- [ ] Direct labels or a non-occluding, ordered legend; heatmaps have a colorbar with range and units
- [ ] n and the meaning of error bars/bands stated; smoothing stated
- [ ] Vector export, fonts embedded, no Type 3 (`pdffonts`)
- [ ] Generated by a committed script from logged results
