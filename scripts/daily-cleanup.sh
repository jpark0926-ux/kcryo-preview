#!/bin/bash
# Daily Mac mini optimization - runs at 03:00
# Kills idle Chrome, clears cache, monitors RAM

LOG_FILE="$HOME/.openclaw/workspace/logs/daily-cleanup.log"
mkdir -p "$(dirname $LOG_FILE)"

echo "=== $(date): Daily cleanup started ===" >> "$LOG_FILE"

# 1. Check Chrome idle time (if running for >12 hours, kill it)
CHROME_HOURS=$(ps aux | grep -i "Google Chrome" | grep -v grep | awk '{print $10}' | head -1 | cut -d: -f1)
if [ -n "$CHROME_HOURS" ] && [ "$CHROME_HOURS" -gt 12 ] 2>/dev/null; then
    echo "Chrome running ${CHROME_HOURS}h - killing" >> "$LOG_FILE"
    killall "Google Chrome" 2>/dev/null
    echo "✅ Chrome terminated" >> "$LOG_FILE"
fi

# 2. Clear user caches (older than 7 days)
find ~/Library/Caches -type f -mtime +7 -delete 2>/dev/null
echo "✅ Cache cleared (7+ days old)" >> "$LOG_FILE"

# 3. Check RAM usage
RAM_USED=$(vm_stat | grep "Pages active" | awk '{print $3}' | sed 's/\.//')
RAM_TOTAL=$(sysctl -n hw.memsize)
RAM_USED_GB=$((RAM_USED * 4096 / 1024 / 1024 / 1024))
RAM_TOTAL_GB=$((RAM_TOTAL / 1024 / 1024 / 1024))
RAM_PERCENT=$((RAM_USED_GB * 100 / RAM_TOTAL_GB))

echo "RAM: ${RAM_USED_GB}GB / ${RAM_TOTAL_GB}GB (${RAM_PERCENT}%)" >> "$LOG_FILE"

# 4. Alert if RAM > 80%
if [ "$RAM_PERCENT" -gt 80 ]; then
    echo "⚠️ WARNING: RAM usage ${RAM_PERCENT}%" >> "$LOG_FILE"
    # Send notification via OpenClaw
    echo "RAM usage high (${RAM_PERCENT}%). Consider closing apps."
fi

# 5. Cleanup Downloads folder (files > 30 days old, keep .pdf, .dmg, .zip)
find ~/Downloads -type f -mtime +30 ! -name "*.pdf" ! -name "*.dmg" ! -name "*.zip" -delete 2>/dev/null
echo "✅ Old downloads cleaned" >> "$LOG_FILE"

echo "=== Cleanup complete: $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
