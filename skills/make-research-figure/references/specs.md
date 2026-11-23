# Specs

## Widths

The authoritative number is the template itself: put `\showthe\linewidth` (or `\the\linewidth` in the text) in the paper and use what it prints (pt ÷ 72.27 = in). Typical values:

| Venue / template | Column | Full width |
|---|---|---|
| NeurIPS, ICLR (single column) | — | 5.5 in |
| ICML | 3.25 in | 6.75 in |
| CVPR / ICCV | 3.25 in | 6.875 in |
| ACL / EMNLP (`acl.sty`) | 7.7 cm ≈ 3.03 in | 16 cm ≈ 6.3 in |
| IEEE conference (`IEEEtran`) | 3.5 in | 7.16 in |
| Nature | 89 mm | 183 mm (max height 170 mm) |

Height: width / 1.618 is a sane default; shorter for single-row line plots, taller for small multiples.

## Palette

Calm, warm and muted, inspired by Anthropic's visual identity: warm neutrals, a clay accent for the focus, and a few soft hues that each carry a fixed meaning. Neither loud (saturated, neon, every element a different color) nor monochrome (black-and-white wireframes with a single accent): color should show structure.

| Role | Hex | Use for |
|---|---|---|
| ink | `#2B2A27` warm near-black | text, main lines (never pure `#000`) |
| ink-soft | `#5E5D59` | outlines of neutral boxes, secondary labels |
| muted | `#8F8D86` warm gray | axes, ticks, secondary text, and at most one de-emphasized series |
| faint | `#E8E6DC` | grids, dividers |
| sand | `#F0EEE6` | fill of neutral / generic boxes |
| paper | `#FAF9F5` | background of grouping zones and panels (the page stays white) |
| focus | `#C6613F` clay | ours, the new component, the change, the key number |
| second | `#4F7FAE` sky | the second series, or a second role to track (e.g. encoders, a shared block) |
| third, fourth | `#6B7F4E` olive, `#B98A3E` ochre | further series or roles that must be told apart |
| fifth | `#7D76A8` heather | only if a fifth role is unavoidable |
| problem | `#A23E3E` brick | only for something bad: failure, overflow, removed, regression; pair it with a dashed line or cross so it is not read as clay |

Fills are the same hue lightened to about 85–90%. Rules:

- **Neutral is warm, not black-and-white.** Components that are not the point are `sand` boxes with `ink-soft` outlines and `ink` text; components with a role take that role's light tint and hue outline. Avoid pure-white boxes with hard black outlines: the figure reads as an unfinished wireframe.
- **Color shows structure.** Same role, same hue (all encoders sky, all memory olive); a schematic typically uses 2–4 hues plus the neutrals. Never assign hues with no meaning.
- **Series must stay distinguishable.** Every series the reader has to tell apart gets its own hue and line style, in the order focus, second, third, fourth (muted only for a de-emphasized baseline). At most one series is gray; two grays, or a gray line on a gray band, cannot be told apart.
- One focus per figure and slide; color keeps its meaning across the whole paper and talk: clay is always "ours / the new thing", brick is always "bad".
- No red-vs-green pairs and no saturated red as emphasis: red reads as "the wrong one", and red–green fails for color-vision deficiency. Clay next to sky is the safe main pair.

## matplotlib defaults (fallback for dense data; Typst is the default, see draw-typst-figure)

```python
import matplotlib as mpl

CYCLE = ["#C6613F", "#4F7FAE", "#6B7F4E", "#B98A3E", "#7D76A8"]   # focus, second, third, fourth, fifth

PAPER = {
    "figure.figsize": (3.25, 3.25 / 1.618),   # set to the venue's \linewidth
    "figure.constrained_layout.use": True,     # keeps the exact width (bbox="tight" does not)
    "font.family": "serif",                    # match the paper; "sans-serif" for sans templates
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.prop_cycle": mpl.cycler(color=CYCLE),
    "lines.linewidth": 1.2, "lines.markersize": 4,
    "legend.frameon": False,
    "savefig.dpi": 300,
    "pdf.fonttype": 42, "ps.fonttype": 42,     # no Type 3 fonts
}

SLIDE = {**PAPER,
    "figure.figsize": (12.33, 4.9),            # the slide figure slot
    "font.family": "sans-serif",
    "font.size": 20, "axes.labelsize": 20,
    "xtick.labelsize": 18, "ytick.labelsize": 18, "legend.fontsize": 18,
    "lines.linewidth": 2.5, "lines.markersize": 8,
}

mpl.rcParams.update(PAPER)
```

For Computer Modern text that matches LaTeX exactly, `text.usetex: True` (needs a TeX install) or the `tueplots` package, which ships venue-specific sizes and fonts (`tueplots.bundles.icml2024()`, `neurips2024()`, ...).

Uncertainty band:

```python
m, lo, hi = mean, ci_low, ci_high          # over seeds, per x
ax.plot(x, m, label="Ours")
ax.fill_between(x, lo, hi, alpha=0.2, linewidth=0)
```

Check fonts after export:

```sh
pdffonts fig.pdf   # the "type" column must not contain "Type 3"
```

## Sources

- Rougier, Droettboom, Bourne. Ten Simple Rules for Better Figures. PLOS Comput Biol 2014.
- Wilke. Fundamentals of Data Visualization (clauswilke.com/dataviz), ch. 17 proportional ink.
- Crameri, Shephard, Heron. The misuse of colour in science communication. Nat Commun 2020.
- Weissgerber et al. Beyond bar and line graphs. PLoS Biol 2015.
- Cumming, Fidler, Vaux. Error bars in experimental biology. J Cell Biol 2007.
- Agarwal et al. Deep RL at the Edge of the Statistical Precipice. NeurIPS 2021 (rliable).
- Tol. Colour Schemes, SRON/EPS/TN/09-002 (personal.sron.nl/~pault).
- Okabe & Ito. Color Universal Design (2008); Wong, Points of view: Color blindness, Nat Methods 2011.
- Naegle. Ten simple rules for effective presentation slides. PLOS Comput Biol 2021.
- Alley & Neeley 2005; Garner, Alley et al. 2009 (assertion–evidence slides).
- Peyton Jones, Hughes, Launchbury. How to give a good research talk. 1993.
- Nature research figure guide (research-figure-guide.nature.com).
