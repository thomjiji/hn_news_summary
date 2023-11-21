#!/bin/bash
# source: https://til.simonwillison.net/llms/claude-hacker-news-themes

# Validate that the argument is an integer
if [[ ! $1 =~ ^[0-9]+$ ]]; then
  echo "Please provide a valid integer as the argument."
  exit 1
fi

# Make API call, parse and summarize the discussion
curl -s "https://hn.algolia.com/api/v1/items/$1" | \
  jq -r 'recurse(.children[]) | .text' | \
  llm -m claude-instant 'Summarize the themes of the opinions expressed here, including quotes where appropriate.'
