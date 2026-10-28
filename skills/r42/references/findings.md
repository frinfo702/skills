# After42 findings

Everything published on after42.org as of 2026-10-28, organized for use. Each finding has an ID (F1, F2, ...) that the rest of the skill cites. Sources:

- **R**: the research post, [Can AI Propose Interesting Research Questions?](https://after42.org/research/can-ai-propose-interesting-research-questions/) (Nie, Wang, et al., 2026). `R§3.2` means section 3.2.
- **Q:id**: a question card in the [question collection](https://after42.org/questions.html), for example `Q:math-6` = <https://after42.org/questions.html#q=math-6>.
- **I**: the [about page](https://after42.org/index.html). **C**: the [contributor page](https://after42.org/contributor.html).

The specific numbers describe frontier models of September 2026 and will date quickly (F41). Use the mechanisms, not the percentages.

## The core problem

- **F1. Novel and difficult is easy; interesting is rare.** Before development, 90% of single-pass, literature-grounded proposals pass an automatic novelty check and 77% a difficulty check, but experts judge only 3% interesting. Novelty and difficulty are not the target. ([R§1](https://after42.org/research/can-ai-propose-interesting-research-questions/#introduction), Figure 2; I FAQ "Why are there so few questions?")
- **F2. "Interesting" means researchers in the field judge it worth pursuing.** Proxies such as proof length relative to statement, or future citations, capture parts of it, but a system optimized for a proxy drifts away from what researchers value. The final judge is the researcher. ([R§1](https://after42.org/research/can-ai-propose-interesting-research-questions/#introduction))
- **F3. Questions shape where effort goes, and solving is getting cheaper,** so choosing what to ask matters more. Good open problems are being "mined in a non-renewable fashion" (Tao); solving is a "tool and proxy" for understanding (Fields Medalists). ([R§1](https://after42.org/research/can-ai-propose-interesting-research-questions/#introduction))

## The workflow

- **F4. Start from a researcher-written goal.** A subfield goal states the understanding the field is after and which kinds of questions matter. Every proposed question is an intermediate step toward it. Example (phase transitions in random structures): understand how many local random rules produce macroscopic qualitative change; ask why a system switches abruptly, where the threshold lies, what structure appears near it, and which phenomena are universal; aim to discover phenomena, mechanisms, critical behavior and universal laws and explain why they matter for real systems. ([R§2](https://after42.org/research/can-ai-propose-interesting-research-questions/#how-after42-works); workflow figure "Research goal"; C "Set a goal in your subfield")
- **F5. Step 0, research pack.** Before proposing, build a shared reference used by every agent: a literature summary, an index of relevant papers with their main results, and open questions collected from the literature. Researchers can help build it. ([R§2](https://after42.org/research/can-ai-propose-interesting-research-questions/#how-after42-works); C)
- **F6. Step 1, oversample.** Interesting questions are rare and hard to produce in one pass, so generate a much larger pool than you need. The main math run generated and filtered 10 batches of initial proposals to end with 70 final questions. ([R§2](https://after42.org/research/can-ai-propose-interesting-research-questions/#how-after42-works), [App. A](https://after42.org/research/can-ai-propose-interesting-research-questions/#appendix-runtime-and-token-usage))
- **F7. Proposers get the goal, instructions and the pack's literature summary,** consult the rest of the pack as needed, search the literature, and make short solution attempts to check and repair each question. Optional **diversity hints**, different per proposer, push toward diverse proposals. The hint texts themselves are not published. (R§2; workflow figure "Propose")
- **F8. Filter.** A critic removes proposals that (a) stay ill posed after attempted repair, (b) add nothing beyond prior work or another proposal (known, duplicate, previously proposed), or (c) a short solution attempt fully resolves (too easy). (R§2; workflow figure "Filter")
- **F9. Step 2, develop by solving.** Each round, solver agents get an additional budget to try to solve each candidate, building on records of earlier attempts or trying new approaches. Attempts yield partial results, obstacles, or new structure. (R§2; workflow figure "Solve")
- **F10. Refine from the evidence.** A development agent reads the solve findings and the literature record. Several subagents independently explore possible directions; the agent picks the most promising and develops the question along it, or keeps the question unchanged. Keeping it is a valid outcome: a round can deepen understanding of the hardest step without changing the statement. (R§2; workflow figure "Refine"; workflow example "Round 2 · Refine")
- **F11. Unanimous judges gate every revision.** Model judges compare current and revised versions pairwise; the revision is accepted only if every judge prefers it. In the spanning-tree trajectory, two of three judges preferred a round-2 revision, so it was rejected. ([R§2](https://after42.org/research/can-ai-propose-interesting-research-questions/#how-after42-works), [R§3.2](https://after42.org/research/can-ai-propose-interesting-research-questions/#solution-attempts-sharpen-or-redirect-research-questions) trajectory 2)
- **F12. Then a fresh-agent validity check.** A fresh agent (not the developer) checks the selected version for prior answers, formulation defects and unsupported claims, makes minimal repairs that preserve the target, and removes questions that remain ill posed. Released questions were also "checked against the literature, tested by repeated solution attempts, and audited for validity". (R§2; workflow "Critique"; I FAQ "How do I know a question is actually open?")
- **F13. Judges rank the survivors before the next round.** The published trajectories ran two rounds. (R§2, R§3.2)
- **F14. Experts read the complete question, the subfield goal, and related work,** about 35 minutes per question including comments, and answer: is it genuinely interesting, would you pursue it or suggest it to a student? They return a ranking with a written rationale for each question and no criteria. Every reviewed question had at least one professor. ([R§2](https://after42.org/research/can-ai-propose-interesting-research-questions/#how-after42-works), [R§5](https://after42.org/research/can-ai-propose-interesting-research-questions/#sec-research-taste) Figure 6)
- **F15. Published question format.** Each card has a title, a precise problem statement ("Prove or refute that ..."), and sections Background, Intuition, Related work (with links), and Routes (approaches and partial progress), plus provenance (which model and runs produced and developed it), status, and expert comments. Status follows the Erdős-problems convention: open (no progress known), partial (meaningful partial results, linked), solved (with link). ([questions data](https://after42.org/data/questions_data.js); I FAQ "What do the status labels mean?")

## What development does

- **F16. Development multiplies the hit rate.** In the phase-transitions study, the share judged interesting rose from 3% of initial proposals to 33% of final questions from the same run. ([R§3.1](https://after42.org/research/can-ai-propose-interesting-research-questions/#experts-find-some-questions-genuinely-interesting))
- **F17. Solution attempts change the question in four observed ways** ([R§3.2](https://after42.org/research/can-ai-propose-interesting-research-questions/#solution-attempts-sharpen-or-redirect-research-questions)):
  1. *Opens a new direction.* Attempts traced a correction to local detours near the optimal path; the revision asked how the detours combine, and the next round turned that into a structural conjecture (Poisson subset sums). (Q:math-19)
  2. *Finds a sharper comparison.* A one-cycle calculation showed the law of a single tree cannot change with temperature, but two trees sampled with the same costs can differ macroscopically; the question moved to that two-sample difference. (Q:math-22)
  3. *Exposes a missing step.* Proving subsequential convergence showed the real gap: whether cooling selects one curve determined by the noise. The revision asked exactly that. (Q:math-21)
  4. *Corrects the intuition.* Attempts showed the geometric signal sits in excess triangles outside the large components the original question looked at; the revision replaced scattered detection targets with one generative model. (Q:math-1)
- **F18. The key change often happens in round one;** later rounds organize ideas into a clearer conjecture or clarify the hardest step. (R§3.2 expert comments on trajectories 1, 2, 4)

## Where it works

- **F19. Yields by subfield (final questions judged interesting by at least two experts):** phase transitions in random structures (math) 33/70 = 47%; black hole ringdown (physics) 3/8 = 38%; online algorithms (TCS) 4/12 = 33%; prediction-powered inference (statistics) 5/35 = 14%; plasma physics 0/10 = 0%. Overall 45/135. ([R§3.1](https://after42.org/research/can-ai-propose-interesting-research-questions/#experts-find-some-questions-genuinely-interesting) Figure 4)
- **F20. Closer to mathematics works better;** the methodology-driven statistics subfield and plasma physics did worst. ([R§3.3](https://after42.org/research/can-ai-propose-interesting-research-questions/#results-remain-uneven-across-fields))
- **F21. The pilot covered theoretical fields** where solving can rely on reasoning, computation and small experiments. Fields that depend on large-scale experiments (e.g. AI) are not yet covered, and the workflow does not yet gather new evidence from data, simulations or experiments. ([R§2](https://after42.org/research/can-ai-propose-interesting-research-questions/#how-after42-works), [R§6](https://after42.org/research/can-ai-propose-interesting-research-questions/#limitations-and-future-steps))

## Novelty and composition

- **F22. Most questions are composition.** Composition = building directly on known work: combine or transfer (A+B), remove or weaken (A−B), next step on a known object (A+1). 97 of 100 initial math proposals and 61 of 70 final questions are composition (initial: 36% A+B, 10% A−B, 51% A+1; final: 51% A+B, 9% A−B, 27% A+1, 13% other). ([R§3.4](https://after42.org/research/can-ai-propose-interesting-research-questions/#most-questions-build-directly-on-known-work) Figure 5)
- **F23. Composition can be strong, but major advances often go beyond it:** introducing a new object and line of inquiry, like percolation (Broadbent and Hammersley 1957) or the evolution of random graphs (Erdős and Rényi 1960). Such questions are rare in AI output. (R§3.4)

## Why questions fail

- **F24. Three recurring motivation and formulation failures** ([R§4](https://after42.org/research/can-ai-propose-interesting-research-questions/#failure-analysis-when-proposed-questions-fail)):
  - *Unnatural combination.* Components do not interact meaningfully, so together they are not a compelling target. "It ties two hard problems directly together, the combination feels forced, and it does not explain why the question should be posed this way."
  - *Engineered complexity.* Added assumptions, parameters or constructions make it harder without isolating a meaningful phenomenon. "With three layers of randomness combined, the central question no longer stands out."
  - *Unclear contribution beyond prior work.* It does not say what it adds to existing results. "More like a lemma in a rigidity project than a standalone problem."
- **F25. Writing defects appear in strong and weak questions alike:** incorrect terminology and nonstandard phrasing obscure meaning; motivation and essential explanations are compressed or omitted while routine details get too much space. (R§4) Experts said of otherwise good questions: "The background and motivation sections are somewhat unclear. However, the problem statement is clear." (Q:math-1, Q:math-3)

## What experts value

- **F26. Four themes from expert comments** (experts were given no criteria) ([R§5.2](https://after42.org/research/can-ai-propose-interesting-research-questions/#sec-taste-criteria)):
  - *Naturalness:* clear motivation within the field, a single main objective; not a combination of familiar ideas whose connection is unmotivated.
  - *Deeper understanding:* the answer would explain a phenomenon not yet explained, ideally such that **either outcome would be informative**.
  - *Need for new ideas:* extensions that require new ideas; the formulation explains why this particular quantitative target matters.
  - *A tractable starting point:* a **concrete first step that is worth doing on its own**.
- **F27. Highly ranked examples** (R§5.2): optimal matchings differing on a large scale, easy to state, sharp structural change, either answer informative (Q:math-17, 6 of 9 experts top five); removing an inactive constraint moving the optimum far away, counterintuitive and shows local stability does not determine the global optimum (Q:math-20, 7 of 9 top 15); near-optimal paths built from separate detours, with the elementary-local-change description valued as a worthwhile first step even if the full law is hard (Q:math-19, 7 of 9 top 15).
- **F28. Patterns praised on individual cards:**
  - Isolates one simple mechanism (reinfection through one junction, Q:math-6); holds a quantity fixed to isolate one effect (mean-preserving variability, Q:math-15; same vertices and ponds, only cycles differ, Q:math-24).
  - Robustness of generic behavior that tests a conjecture from another literature (weak disorder rounding an absorbing-state jump, Q:math-7).
  - Moving from a known quantity to the full object (optimal cost to the Gibbs measure, Q:math-8); from static structure to dynamics (Q:math-3).
  - A precise prediction from a heuristic or a known structure (Airy profile, Q:math-14; PWIT overlap, Q:math-8; scale from percolation exponents, Q:math-13).
  - "Easy to state", "clean", "canonical", "approachable"; partial results already worthwhile (Q:math-9, Q:math-14 "even establishing the exponent 1/3 alone would already be interesting").
  - A non-standard cost model that exposes a cost-performance tradeoff (Q:tcs-2); a natural local version of a known global constraint (Q:tcs-3); a clean comparison family that decouples two effects (Q:physics-2).
- **F29. Reservations recorded on cards** (useful as a checklist; see `checker-checklist.md`):
  - Unexplained specific choices make the model look artificial: why three arms (Q:math-6), why contacts occurring exactly twice (Q:math-16). The fix is usually one sentence of motivation (three is the smallest new case).
  - An inessential parameter or regime in the statement (Q:math-1, the giant-component window seemed inessential).
  - The answer would mostly confirm a familiar picture through technical work (Q:math-3).
  - Only one outcome is interesting: a bounded overlap "would mean unremarkable behavior"; behavior exactly at the critical point is specialized (Q:math-23).
  - Expected answer is a quantitative refinement, not a new phenomenon; generic motivation; A+B of a dynamics and a perturbation (Q:math-25).
  - The full statement is very hard and needs a more focused first target (Q:math-10, Q:math-11, Q:math-12).
  - Jumps from a broad problem to tuning one estimator before establishing the best achievable rate (Q:statistics-1); unclear new insight from the combination; a concrete application would help.
  - No conjecture stated where a sibling question had one (Q:math-2).
  - The central unresolved step is not yet resolved by the provided diagnostics (Q:statistics-2, Q:statistics-3, Q:physics-3).

## Can models judge?

- **F30. Judge instructions used** ([R§5](https://after42.org/research/can-ai-propose-interesting-research-questions/#sec-research-taste) Figure 6): rank which questions are most interesting and worth pursuing, no scores, a written rationale per question, criteria: *Simplicity* (few essential objects, one core target); *Boldness and naturalness* (challenge the standard framing; no routine A+B); *Depth* (deepen understanding or leave a reusable idea); *Difficulty is not a negative* (do not favor what merely looks tractable).
- **F31. Model shortlists match expert consensus.** At top-20 of 70, single models recall 65–80% of the 20-question expert consensus set (individual experts: 45–80%); averaging ranks across four models gives 80%. ([R§5.1](https://after42.org/research/can-ai-propose-interesting-research-questions/#sec-taste-alignment) Figure 7)
- **F32. But not individual taste.** The ensemble top-20 recalls 35–85% of individual experts' top-20. Models are *mode seekers*: they recover consensus picks but do no better than chance on questions only one expert ranked highly, and such questions sometimes open new directions. (R§5.1, [R§7](https://after42.org/research/can-ai-propose-interesting-research-questions/#discussion))
- **F33. The criteria gap: tractability.** Experts value a concrete first step; the judge instructions said the opposite ("do not favor what looks tractable"), so judges may rank highly questions with no clear starting point. ([R§5.3](https://after42.org/research/can-ai-propose-interesting-research-questions/#sec-taste-disagreements))
- **F34. Same criterion, different reading.** (a) Experts ranked the triangles question top-15 (8 of 9); the model ensemble ranked it 36th because models judged the stated conjecture's mechanism predictable, while experts valued what either a proof or a counterexample would reveal. (b) Models ranked the shuffled-permutation community question top-6 of 32, seeing one linking mechanism; experts saw a routine A+B of Markov-chain mixing and weak recovery: "Why is this particular combination intrinsically worth studying?" (R§5.3)
- **F35. Personalization: stated preferences do not help; feedback on earlier questions does.** Giving a judge the expert's written description of preferences (valued qualities, liked and disliked papers) did not improve agreement, because it overlapped the generic criteria. Giving the expert's feedback on 33 earlier questions raised rank correlation from 0.26 to 0.42 for one expert, less for two others; adding stated preferences on top gave no further clear gain. ([R§5.4](https://after42.org/research/can-ai-propose-interesting-research-questions/#sec-taste-personalization) Figure 8)
- **F36. Model judges are prioritization tools, not substitutes.** Their preferences are reproducible and steerable, but the researcher (and the community) decides. ([R§1](https://after42.org/research/can-ai-propose-interesting-research-questions/#introduction), [R§7](https://after42.org/research/can-ai-propose-interesting-research-questions/#discussion); I "What we find")

## Cost

- **F37. One full math run:** 70 final questions in about a day; 10 proposal batches with filtering took ~11 h, then 12 h of development with up to 16 questions in parallel; ~260 agent-hours (3.7 per final question); ~2.62 B tokens (37.4 M per final question: 211 M uncached input, 2.38 B cached input, 24.9 M output). ([App. A](https://after42.org/research/can-ai-propose-interesting-research-questions/#appendix-runtime-and-token-usage))

## Limits and use

- **F38. Expert interest is an early, imperfect proxy** for the value of pursuing a question; consensus can miss directions that later matter, which is why individual judgment matters alongside it. Whether solving the questions yields insight is not yet established. ([R§6](https://after42.org/research/can-ai-propose-interesting-research-questions/#limitations-and-future-steps))
- **F39. Interestingness has cultural and empirical sides.** After42 draws on culture (literature, researcher goals) but not on new evidence from data, simulations or experiments. (R§6)
- **F40. Evaluation scale is small:** one subfield for the model-vs-expert comparison, three experts for personalization; no reliable automatic evaluator of interestingness exists. (R§6)
- **F41. Results are a September 2026 snapshot** of fast-changing models. (R§6)
- **F42. Openness is "our current knowledge of the literature":** do your own prior-art search before investing serious effort. (I FAQ)
- **F43. Responsible use:** questions are released for researchers to pursue, not as an AI benchmark; credit the source (`\citep[question math-1]{nie2026after42}`), disclose AI assistance, and avoid rushed announcements that raise attribution and plagiarism problems. Questions and expert comments are CC BY 4.0. ([R§7](https://after42.org/research/can-ai-propose-interesting-research-questions/#discussion); I FAQ; C)
- **F44. Asking and solving are intertwined** (Lakatos, Thurston): attempted proofs revise conjectures and concepts, and as AI produces ideas faster than people absorb them, the work of understanding grows. Researchers set goals and choose; AI explores many more candidates than one person could. (R§1, R§7)
- **F45. Ways researchers engage:** set a goal in their subfield (and help build the pack), assess questions and share taste (assessments guide later proposing and development), pursue a question and report progress, prior art or errors (corrections are published with what changed). (C; I FAQ)
