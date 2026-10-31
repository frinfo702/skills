# Interpret results

Helps the user understand what an experiment shows and what they can claim. The danger runs both ways: a post-hoc story fitted to any result, and a real effect dismissed because of a bug or noise (E8).

## Inputs

The results (numbers, logs, runs in a tracker the user points to, figures, failure cases), the experiment card if there was one, and the code if needed. If there was no card, reconstruct what was expected before reading the numbers, and say so.

## Procedure

1. **Compare to the card.** What was predicted, what happened, and which reading applies. If the outcome falls between readings, say what it does and does not support rather than forcing it into one.
2. **Is the difference real?** Compare the effect with seed variance and the spread across runs (C12). One run per arm is not evidence for a small gain; say what would be.
3. **Is the comparison fair?** Same tuning budget, same evaluation, same data (C10, C11). A gain against an untuned baseline is not yet a gain.
4. **If it is unexpected, attribute before explaining.** List the competing explanations (hypothesis wrong; experiment design wrong; implementation bug) with the evidence for each, and the cheapest check that would separate them (E8). Bugs come first: re-check the baseline number and the tiny-set overfit (C3).
5. **Look at examples.** Aggregate numbers hide where the change acts. Pull failure and success cases, sort them by hand into a few types, and count (C1). Show the user a few concrete cases; their reading of the examples often matters more than yours.
6. **What can be claimed.** State the strongest claim the evidence supports, the scope (data, scale, setting) it is supported for, and what would be needed to claim more.
7. **What next.** The one or two experiments that would most change the picture, as cards with readings. If you are short of ideas, write your own first, then scan `references/ml-cards.md` for blind spots.

## Output

Lead with the plain-words reading ("The gain is real but comes from X, not the relation module"). Then: confidence and why; the competing explanations still open; the supportable claim and its scope; the next experiments as cards. If the user names a destination, write the result as a reply to the experiment card there, conclusion first (`references/records.md`).
