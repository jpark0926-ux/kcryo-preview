#!/bin/bash
# Dart Monitor Wrapper - For cron jobs
export DART_API_KEY="${DART_API_KEY}"
python3 "$(dirname "$0")/dart-monitor.py" 2>&1
