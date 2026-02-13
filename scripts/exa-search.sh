#!/bin/bash
# Exa.ai Neural Search Tool for Chris
# Usage: ./exa-search.sh "query" [num_results]

API_KEY="${EXA_API_KEY}"
QUERY="$1"
NUM_RESULTS="${2:-10}"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"search query\" [num_results]"
    exit 1
fi

echo "🔍 Exa Neural Search: $QUERY"
echo "---"

curl -s -X POST https://api.exa.ai/search \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"query\": \"$QUERY\",
        \"numResults\": $NUM_RESULTS,
        \"type\": \"neural\",
        \"contents\": {
            \"text\": true,
            \"highlights\": true
        }
    }" | jq -r '.results[] | "\n📄 \(.title)\n   URL: \(.url)\n   🔑 Highlights: \(.highlights | join(" | "))\n"' 2>/dev/null || echo "Raw results saved to /tmp/exa-result.json"
