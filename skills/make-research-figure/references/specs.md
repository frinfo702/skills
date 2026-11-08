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

Calm by default: what is not the point is black on white, one color carries the focus, and every other color has a fixed meaning. The hues come from Paul Tol's colour-blind-safe schemes (high-contrast and muted), which are less saturated than Okabe–Ito.

| Role | Hex | Use for |
|---|---|---|
| ink | `#22272E` | text, lines, outlines of neutral boxes (filled white) |
| muted | `#8B929A` | axes, ticks, secondary text, and at most one de-emphasized series |
| faint | `#E3E6EA` | grids |
| focus | `#004488` deep blue | ours, the new component, the change, the key number |
| second | `#DDAA33` ochre | the second series, or a second thing to track (e.g. a shared block) |
| third, fourth | `#44AA99` teal, `#AA4499` purple | further series that must be told apart |
| problem | `#BB5566` rose | only for something bad: failure, overflow, removed, regression |

Fills are the same hue lightened to about 85%. Rules:

- **Neutral is black and white, not gray.** Components that are not the point are white boxes with black outlines and black text. Gray fills and gray boxes look muddy and fade on projectors; gray is for axes, grids and secondary text.
- **Series must stay distinguishable.** Every series the reader has to tell apart gets its own hue and line style, in the order focus, second, muted, third. At most one series is gray; two grays, or a gray line on a gray band, cannot be told apart.
- One focus per figure and slide; color keeps its meaning across the whole paper and talk: blue is always "ours / the new thing", rose is always "bad".
- No red-vs-green pairs and no saturated red as emphasis: next to blue or green it reads as "the wrong one", and red–green fails for color-vision deficiency.

## matplotlib defaults (fallback for dense data; Typst is the default, see draw-typst-figure)

```python
import matplotlib as mpl

CYCLE = ["#004488", "#DDAA33", "#8B929A", "#44AA99"]   # focus, second, muted, third

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
