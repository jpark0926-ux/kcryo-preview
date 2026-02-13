#!/bin/bash
# Smart Search Router for Chris
# Automatically selects best search tool based on query
# Usage: ./smart-search.sh "query"

QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"search query\""
    exit 1
fi

# Detect query type
KOREAN=$(echo "$QUERY" | grep -E '[가-힣]' | wc -l)
STOCK_KR=$(echo "$QUERY" | grep -Ei "삼성|하이닉스|현대차|카카오|네이버|코스피|코스닥|공시|실적|분기|연간" | wc -l)
SEMANTIC=$(echo "$QUERY" | grep -Ei "similar|like|비슷|관련|cluster|발굴|찾아|유사" | wc -l)
NEWS=$(echo "$QUERY" | grep -Ei "news|뉴스|최근|오늘|어제|발표|속보" | wc -l)

echo "🔍 Smart Search: $QUERY"
echo "---"

# Route decision (priority: semantic > stock_kr > news/general)
if [ "$SEMANTIC" -gt 0 ]; then
    echo "🧠 Route: Exa Neural Search (Semantic similarity)"
    ~/.openclaw/workspace/scripts/exa-search.sh "$QUERY" 10
    
elif [ "$STOCK_KR" -gt 0 ]; then
    echo "📊 Route: Dart API (Korean stock disclosure)"
    echo "Target: Korean stock disclosure search"
    # TODO: Implement Dart search
    echo "Status: Implementation pending"
    
elif [ "$NEWS" -gt 0 ]; then
    echo "🔎 Route: Perplexity (Real-time news)"
    echo "Target: Latest market news and updates"
    echo "Use: web_search tool"
    
else
    echo "🔎 Route: Perplexity (General web search)"
    echo "Target: General information"
    echo "Use: web_search tool with provider=perplexity"
fi
