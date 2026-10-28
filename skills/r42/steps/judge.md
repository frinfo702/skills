# Judge (ranking)

Ranks a set of questions with every configured judge, then combines them (F13, F30–F32). Step `judge`.

1. `r42.py agents` lists the judges on its last line. Submit one ranking job per judge with `--agent <judge>`, all in parallel, each using the ranking prompt in `references/judge-rubric.md`. Each writes `.r42/rankings/<label>.<agent>.md`. Include the researcher's feedback entries from `.r42/feedback.md` verbatim in each prompt when there are any (F35).
2. When all succeed, combine (you do this inline): average ranks across judges, and write `.r42/rankings/<label>.md` with the averaged order, each judge's rank, short rationales, and the "single-judge picks / largest spread" list described in the rubric (F32).
3. Present the top of the averaged order and the spread list together. Remind the user once that this is a prioritization aid; their own ranking overrides it (F36).

Set of questions by default: all `developing` and `final` questions. For a filter-stage ranking, the survivors of the filter.
