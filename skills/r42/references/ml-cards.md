# ML improvement cards

General moves that reliably give a way in or a way forward in empirical ML research, collected from textbooks, playbooks and experienced researchers. They are deliberately not specific to one subfield.

**How to use this deck** (see SKILL.md, Getting unstuck): it is a floor to return to, not a recipe. Think from the problem first and write your own candidate moves. Then scan these for blind spots. Use a card only when you can say in one sentence why it fits this problem, and cite it as `C<n>`. A card that does not fit is not a gap in your reasoning. Better problem-specific ideas beat every card.

Each card: **When** (the situation) · **Move** · **Gives** (what you learn or get) · **Trap** · source.

## Diagnose: what is actually wrong

**C1. Look at the failures yourself.**
When: aggregate metrics stopped telling you anything new. Move: pull 50–100 errors, sort them by hand into categories, count. Gives: which error type is worth fixing and the ceiling of fixing it. Trap: categories invented before looking. — Ng, *Machine Learning Yearning* (error analysis); Karpathy, [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/).

**C2. Split the gap.**
When: performance is below target and you do not know why. Move: compare training error, held-out error from the training distribution, and target-distribution error (and a human or oracle level if one exists). Gives: whether the problem is fitting, generalization, or distribution shift; each has different remedies. Trap: tuning regularization when the model cannot even fit. — Ng, *Machine Learning Yearning* (bias, variance, data mismatch).

**C3. Overfit a tiny set.**
When: a new model or loss "does not learn" or behaves oddly. Move: train on one batch or a handful of examples until loss reaches ~0. Gives: a pipeline check; failure means a bug, not a bad idea. Trap: concluding an idea fails before this passes. — Karpathy, Recipe.

**C4. Oracle substitution (ceiling analysis).**
When: a system has several parts and you do not know which limits it. Move: replace one component's output with ground truth and measure the gain; repeat per component. Gives: the headroom of each part; work on the part with the largest ceiling. Trap: assuming the newest component is the bottleneck. — Goodfellow, Bengio, Courville, *Deep Learning* ch. 11; Ng, *Machine Learning Yearning* (error analysis by parts).

**C5. Find the shortcut.**
When: a model scores well yet fails on cases that need the property you care about. Move: build test cases where the easy cue and the intended cue disagree (counterfactual edits, swapped context, controlled pairs). Gives: whether the model uses the intended information at all. Trap: reading high benchmark scores as evidence of the intended skill. — Geirhos et al., *Shortcut learning in deep neural networks*, Nature MI 2020.

**C6. Remove the information and see if it matters.**
When: you want to know whether a model uses some input (position, context, a modality). Move: ablate, shuffle or mask exactly that information at test time, or train without it. Gives: causal evidence of use, which probes do not give. Trap: an ablation that also breaks something else. — standard practice; contrast with C7.

**C7. A probe shows presence, not use.**
When: probing results are being used to argue what a model "relies on". Move: compare against control tasks or random-representation baselines, and confirm with an intervention (C6). Gives: a fair reading of probe accuracy. Trap: many probe experiments that never change a decision. — Hewitt & Liang, *Designing and Interpreting Probes with Control Tasks*, 2019; Belinkov, *Probing Classifiers*, 2022.

**C8. A controlled synthetic world.**
When: real data confounds the factor you care about. Move: build a small synthetic dataset where that factor is set explicitly and everything else is held fixed (CLEVR-style). Gives: a fast, clean test of a mechanism. Trap: claiming real-world gains from synthetic-only results. — e.g. Johnson et al., CLEVR, 2017.

**C9. Audit the metric and the labels.**
When: gains are small, noisy, or do not match what you see. Move: check that the metric measures the claim, inspect test-label errors, check for train–test overlap and leakage. Gives: whether the "problem" is in the evaluation. Trap: optimizing a metric that rewards the wrong thing. — Northcutt et al., *Pervasive Label Errors in Test Sets*, 2021; Kapoor & Narayanan, *Leakage and the reproducibility crisis in ML-based science*, 2023.

## Experiment craft: make results trustworthy and fast

**C10. A strong, equally tuned baseline first.**
When: before any claim of improvement. Move: reproduce the strongest simple baseline and give it the same tuning budget as your method. Gives: honest headroom; many reported gains vanish under equal tuning. Trap: comparing a tuned method to paper numbers. — Melis et al. 2018 (language models); Lucic et al., *Are GANs Created Equal?*, 2018; Musgrave et al., *A Metric Learning Reality Check*, 2020.

**C11. One change at a time; know which knobs are which.**
When: designing a comparison. Move: name the scientific variable, the nuisance hyperparameters to re-tune for each setting, and the fixed ones. Gives: comparisons that mean what they say. Trap: changing architecture and schedule together. — [Google Deep Learning Tuning Playbook](https://github.com/google-research/tuning_playbook).

**C12. Seeds and variance.**
When: differences are within a point or two. Move: run several seeds, report spread or intervals, and know the variance from data order and initialization. Gives: whether a difference is real. Trap: picking the best seed. — Henderson et al., *Deep RL that Matters*, 2018; Bouthillier et al., *Accounting for Variance in ML Benchmarks*, 2021.

**C13. A fast proxy, checked once.**
When: one run takes too long to iterate. Move: shrink data, resolution, schedule or model until a run takes minutes; then check once that the proxy ranks a few known methods like the full setting. Gives: many more iterations. Trap: trusting a proxy whose ranking was never checked.

**C14. Predict before you run.**
When: before every experiment. Move: write the expected result and how you would read each qualitatively different outcome (which hypothesis it supports or rules out, what you would do next). If every outcome leads to the same action, skip the run. Gives: experiments that move the project; surprises and changes of interpretation become visible. Trap: post-hoc stories for any result; or the opposite, a numeric cutoff applied mechanically (29.9% vs 30%). — Platt, *Strong Inference*, Science 1964 (crucial experiments between alternative hypotheses); Howard, *Information Value Theory*, 1966 (information is worth gathering only if it can change a decision); Nosek et al., *The preregistration revolution*, PNAS 2018 (predictions fixed before seeing data).

**C15. Learning rate and schedule before anything clever.**
When: a new setup underperforms. Move: sweep learning rate (log scale) and warmup first. Gives: removes the most common cause of a "bad idea". Trap: ablations at a badly tuned learning rate. — Bengio, *Practical Recommendations for Gradient-Based Training*, 2012; Tuning Playbook.

## Sources of ideas: from a diagnosed problem to a candidate fix

**C16. Put the missing structure where it can act.**
When: the model lacks a structural property the task needs (relations, geometry, symmetry, order). Move: consider the three places structure can enter: the architecture (inductive bias, equivariance), the data (augmentation, synthesis), and the objective (a loss term or target that requires it). Gives: a small set of distinct fixes to compare. Trap: only ever adding architecture. — Battaglia et al., *Relational inductive biases, deep learning, and graph networks*, 2018.

**C17. Make the training signal require the property.**
When: the model never needs the property to reduce its loss. Move: check whether any training example is wrong unless the property is used; if not, add such examples (counterfactual pairs, hard negatives) or an auxiliary target. Gives: often the root cause of a "capability gap". Trap: changing the model when the data never asks for the skill. — Kaushik, Hovy, Lipton, *Counterfactually-Augmented Data*, 2020.

**C18. Change the output representation or the task formulation.**
When: incremental changes to a standard formulation keep giving small gains. Move: ask whether a different formulation of the same task fits the structure better (per-pixel to mask classification; dense prediction to set prediction). Gives: occasionally a large step from a simple change. Trap: reformulating without a reason tied to the diagnosis. — Cheng et al., *Per-Pixel Classification is Not All You Need* (MaskFormer), 2021; Carion et al., DETR, 2020.

**C19. Borrow a mechanism from a problem with the same bottleneck.**
When: you have a clear diagnosis. Move: search for other tasks where the same bottleneck was solved, by mechanism, not by task name; list the assumptions the mechanism needs and check them in your setting. Gives: a transfer with a reason. Trap: surface analogies; importing assumptions that do not hold (E10–E12). — Hope et al. 2017.

**C20. Ask what scale alone does.**
When: proposing a method to close a gap. Move: check how the gap changes with more data, longer training or a larger model. Gives: whether the problem is one of capacity or of method; a gap that does not close with scale is a stronger target. Trap: a method that only wins at small scale. — Sutton, *The Bitter Lesson*, 2019.

**C21. Remove pieces from a strong method.**
When: a complicated state of the art exists. Move: remove components one at a time and see what does the work. Gives: often a simpler method, or the real mechanism, which is itself a contribution. Trap: removing components without re-tuning (C11).

**C22. Limit before method.**
When: about to optimize a method. Move: estimate the best achievable result first (oracle, upper bound, human level). Gives: whether the target is worth the effort, and sometimes the more interesting question. Trap: polishing a method in a saturated regime. — After42 Q:statistics-1 (F29).

**C23. Decompose and solve the sub-problem.**
When: the full task is hard to move. Move: split into stages or an easier special case (fewer objects, one relation type, a fixed viewpoint) and solve that cleanly first. Gives: a first step worth doing on its own. Trap: a special case that removes the phenomenon. — Pólya, *How to Solve It* (specialize, auxiliary problem).

## Process: when the project itself is stuck

**C24. Write the claim and Figure 1 first.**
When: experiments are piling up without direction. Move: write the abstract's main sentence and the first figure as if it worked; list the experiments that sentence needs. Gives: a test of which experiments matter. Trap: not revising the claim when evidence says otherwise. — Huang, [steady progress](https://github.com/jbhuang0604/awesome-tips/blob/main/steady-progress.md); Schulman (goal-driven).

**C25. Timebox and kill criteria.**
When: an idea has had "one more try" several times. Move: before continuing, set a date and say what kind of evidence would end it (not a numeric cutoff). Gives: freed time; dropped ideas recorded with why. Trap: switching too often; give an idea a fair test first (E13).

**C26. Explain it to someone.**
When: you cannot say in two sentences why the current direction should work. Move: explain the problem and the bet to a colleague (or the user, or r42) and collect their first objection. Gives: the hidden assumption. Trap: explaining the method instead of the reason.

**C27. Read the limitations sections and reviews.**
When: looking for problems worth solving near a known line of work. Move: read the limitations sections, rebuttals and OpenReview comments of the closest papers. Gives: problems the authors and reviewers already know are open. Trap: picking a limitation nobody cares about.
