#!/bin/bash
# Quick ontology status check (no Python deps needed)

ONTOLOGY="/Users/roturnjarvis/.openclaw/workspace/CHRIS-ONTOLOGY.yml"

echo "=================================================="
echo "📊 Chris Status - $(date '+%Y-%m-%d %H:%M')"
echo "=================================================="
echo ""

echo "🏢 Business Projects:"
grep -A 2 "name: \"" "$ONTOLOGY" | grep -E "(name|status|progress)" | head -6
echo ""

echo "⚠️  Blockers:"
grep "blocker:" "$ONTOLOGY" | sed 's/.*blocker: /  • /'
echo ""

echo "🎯 Priority Queue:"
grep -A 3 "priority_queue:" "$ONTOLOGY" | tail -3
echo ""

echo "💰 Top Holdings:"
grep -A 1 "PLTR:" "$ONTOLOGY" | head -2
grep -A 1 "IREN:" "$ONTOLOGY" | head -2
grep -A 1 "NVDA:" "$ONTOLOGY" | head -2
echo ""

echo "Updated: $(grep "last_updated:" "$ONTOLOGY" | cut -d'"' -f2)"
