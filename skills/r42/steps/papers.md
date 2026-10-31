# Find papers

Finds and verifies literature for a specific need: related work for an idea, prior art for a question, the source of a method, a baseline and its numbers, or the citations in a draft. Every paper reported is one you actually found; never one you remember but did not retrieve (F42).

## Procedure

1. **Pin down the need** in one line: what the papers are for (prior-art check, related work, method source, baseline, citation check) and the cutoff date if openness at a date matters.
2. **Search by structure, not only by keyword.** Write the query three ways: the task name; the bottleneck or failure it addresses; the mechanism or method family. Neighbouring tasks with the same bottleneck often hold the closest prior work (E11). Use cito first (`references/paper-search.md`), then arXiv for the last two weeks, OpenReview for reviews, and Papers with Code or the repos for numbers.
3. **Follow the graph.** From the two or three closest hits, read their related-work sections and check who cites them (cito / Semantic Scholar). Stop when new searches return papers you already have.
4. **Read what you report.** For each paper you keep, read at least the abstract and the part that matters for the need (the method section for a mechanism, the results table for a baseline, the limitations for open problems). Say which part you read.
5. **Prior-art checks** look for the exact claim, its special cases, and the obvious reformulations, with a date filter if openness at a date matters. Report one of: done (with the paper), partly done (what remains), not found (with what you searched).
6. **Citation checks** (for a draft): every citation exists, the bibliographic data is right, and the cited paper says what the sentence claims. Report each failure with the fix.

## Output

Lead with the answer to the need (e.g. "Closest prior work is X (2024); it does A but not B"). Then the papers, most relevant first:

```markdown
- Authors (year), [title](link): what it shows, in one or two sentences. Relevance: <why it matters here>. Read: <abstract / method / table N>.
```

Mark anything you could not verify as unverified. If the user names a destination (a Linear page, an issue), write the list there in the same form (`references/records.md`).
