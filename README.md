# Skills for my ideal engineering

## Install

```bash
npx skills@latest add frinfo702/skills
```

## Paper search

The research skills search papers with [cito](https://cito.fim.ai/). Add its MCP server to each agent:

```bash
claude mcp add --transport http cito https://api.cito.fim.ai/mcp   # Claude Code
codex mcp add cito --url https://api.cito.fim.ai/mcp               # Codex
pi mcp add cito --url https://api.cito.fim.ai/mcp                  # pi
```
