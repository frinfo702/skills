# Judge (ranking)

Ranks a set of questions with every configured judge, then combines them (F13, F30–F32). Step `judge`.

1. The judges are `judges` in the agent configuration (SKILL.md, Agents) (`default` means the entry without `when`). Start one ranking job per judge, on that judge's entry, all in parallel, each using the ranking prompt in `references/judge-rubric.md`. Each writes `<work>/rankings/<label>.<agent>.md`. Include the researcher's feedback (`<work>/feedback.md`, see `steps/feedback.md`) verbatim in each prompt when there are any (F35).
2. When all succeed, combine (you do this inline): average ranks across judges, and write `<work>/rankings/<label>.md` with the averaged order, each judge's rank, short rationales, and the "single-judge picks / largest spread" list described in the rubric (F32).
3. Reply with the top of the averaged order, one line each, and the single-judge picks on one line (F32).

Set of questions by default: all `developing` and `final` questions. For a filter-stage ranking, the survivors of the filter.
