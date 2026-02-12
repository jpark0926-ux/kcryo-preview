#!/bin/bash
# Daily Summary - 매일 아침 자동 요약

ONTOLOGY="/Users/roturnjarvis/.openclaw/workspace/CHRIS-ONTOLOGY.yml"

echo "🌅 **Good Morning Chris!**"
echo ""
echo "📅 $(date '+%Y-%m-%d %A')"
echo ""

echo "**🎯 Today's Focus:**"
grep -A 3 "priority_queue:" "$ONTOLOGY" | tail -3 | sed 's/^/• /'
echo ""

echo "**⚠️ Blockers to Clear:**"
grep "blocker:" "$ONTOLOGY" | sed 's/.*blocker: "//;s/"$//' | sed 's/^/• /'
echo ""

echo "**💰 Portfolio Check:**"
echo "• PLTR: 609주 (high conviction)"
echo "• Watch: CEG, ETN"
echo ""

echo "**💡 Suggestion:**"
echo "오늘 오후 3시 = 에너지 피크"
echo "→ 중요한 결정(사진/방향) 그때 하세요!"
echo ""

echo "Have a productive day! 🦇"
