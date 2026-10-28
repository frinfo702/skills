# Paper search with cito

[cito](https://cito.fim.ai/) is a search engine for agents over ~148M papers (Semantic Scholar). Use it first for every literature search, prior-art check and citation lookup, and fall back to web search or arXiv for what it lacks. Every hit is a real paper with a real link, so a pack or check note built from cito hits cannot cite a paper that does not exist (F42).

## Install

The MCP server is streamable HTTP at `https://api.cito.fim.ai/mcp`. Add it to each runtime the agents use:

```bash
claude mcp add --transport http cito https://api.cito.fim.ai/mcp   # Claude Code
codex mcp add cito --url https://api.cito.fim.ai/mcp               # Codex
pi mcp add cito --url https://api.cito.fim.ai/mcp                  # pi
```

No key is needed. A key from https://cito.fim.ai/account/keys raises the limit: Claude Code `--header "Authorization: Bearer sk_..."`, Codex and pi `--bearer-token-env-var CITO_API_KEY`.

## Use

- MCP tools: `search_papers` (query, mode `hybrid` | `semantic` | `keyword`) and `get_paper` (by Semantic Scholar CorpusID).
- Without MCP, call the API: `curl "https://api.cito.fim.ai/search?q=contrastive+learning&limit=5"` and `curl https://api.cito.fim.ai/paper/<corpusid>`.
- `published_before=YYYY-MM-DD` keeps only earlier papers. Use it to check whether a question was already open, or already answered, at some date.
- The corpus is a weekly snapshot (`corpus_release` in each response). Check arXiv directly for papers from the last week or two.
- Link each paper by the hit's `url` (or `doi`).

## Rate limits

Without a key the limit is 15 requests/min per IP, shared by every worker on this machine; with `max_parallel = 4` a literature-heavy step reaches it quickly. On a 429, wait a minute and retry rather than switching to unverified sources. Before a full run or a large pack, suggest the user set up a key (100/min).
