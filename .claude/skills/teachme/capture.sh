#!/bin/sh
# Print every other pane in the caller's tab, with secrets masked.
rex session inspect --json |
  jq -r --arg me "$REX_BLOCK" '.windows[] | select(any(..; .block_id? == $me)) | .layers[].blocks[] | select(.block_id != $me) | .block_id' |
  while read -r id; do
    echo "### block $id"
    echo '~~~'
    rex capture --trim -b "$id" | sed -E \
      -e 's/(sk-|ghp_|gho_|ghs_|ghu_|github_pat_|xox[abposr]-|glpat-|AIza)[A-Za-z0-9_-]+/\1****/g' \
      -e 's/AKIA[0-9A-Z]{16}/AKIA****/g' \
      -e 's/([Bb]earer )[A-Za-z0-9._~+\/=-]+/\1****/g' \
      -e 's/([A-Za-z0-9_]*(TOKEN|SECRET|PASSWORD|PASSWD|API_KEY|APIKEY|token|secret|password|api_key)[A-Za-z0-9_]*["'"'"']?[[:space:]]*[=:][[:space:]]*["'"'"']?)[^[:space:]"'"'"']+/\1****/g'
    echo '~~~'
  done
