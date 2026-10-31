# Help write the paper

Helps draft, restructure or review an ML paper. The user owns the claims and the voice; r42 makes the argument clear and every statement supported. If a dedicated paper-writing skill is installed (for venue templates and LaTeX), use it for those parts.

## Procedure

1. **Claim first.** Write the paper's main claim in one sentence and the evidence that supports it (which table, which figure). If the user cannot agree on that sentence, help settle it before polishing prose; most writing problems are claim problems.
2. **Figure 1 and the abstract** carry the claim: the problem, why existing work falls short (the specific failure, not "limited performance"), the idea, and the main evidence. Draft these before the body (C24).
3. **Structure.** Introduction (problem, gap, idea, contributions as checkable statements), related work organized by the question each line answers, method in the order a reader needs it, experiments that each answer a stated question, limitations.
4. **Every claim supported.** Each statement of a result points to a table or figure; each comparison is fair as in `steps/interpret.md`; each citation is verified (`steps/papers.md`, step 6). Flag overclaims with the wording the evidence supports.
5. **Reviewer pass.** Read as a skeptical reviewer at the target venue: what is the weakest point, which baseline or ablation is missing, what is unclear. Report the top issues with fixes. For an independent pass, run it as a job on another model family.
6. **Language.** Standard terminology, one idea per paragraph, no unexplained notation, motivation in plain words before formalism (F25). Keep the user's voice; do not rewrite text they did not ask to change.

## Output

For drafting: the draft text in the repo's paper files or the reply, as the user asked. For review: a verdict in one line, then the issues, most serious first, each with location, why it matters, and the fix. Disclose AI assistance as the venue requires (F43).
