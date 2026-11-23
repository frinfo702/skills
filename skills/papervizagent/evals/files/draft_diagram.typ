#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#set page(width: 5.5in, height: auto, margin: 4pt, fill: white)
#set text(font: "Times New Roman", size: 8pt, fill: black)

#diagram(
  spacing: (0.6cm, 0.7cm),
  edge-stroke: 1.5pt + black,
  node((1.5, -0.9), text(size: 10pt, weight: "bold")[Figure 1: Overview of Our Proposed Multi-Agent Code Repair Pipeline]),

  node((0, 0), [Buggy Repository and Failing Unit Tests Provided by the User], name: <in>,
    width: 1.8cm, fill: yellow, stroke: 2pt + black),
  node((1, 0), [Fault Localizer Agent that searches the codebase and identifies candidate buggy functions], name: <loc>,
    width: 2.0cm, fill: lime, stroke: 2pt + red),
  node((2, 0), [Patch Generator Agent], name: <gen>,
    width: 1.9cm, fill: aqua, stroke: 2pt + blue),
  node((3, 0), [Test Harness Executor], name: <exec>,
    width: 1.8cm, fill: fuchsia, stroke: 2pt + black),

  node(enclose: (<loc>, <gen>), [Iterative Repair Loop],
    stroke: 1.5pt + red, fill: yellow.lighten(50%), layer: -1),

  edge(<in>, <loc>, "->"),
  edge(<loc>, <gen>, "->"),
  edge(<gen>, <exec>, "->"),
  edge(<exec>, <loc>, "->", bend: -25deg, label: [Error trace feedback]),
)
