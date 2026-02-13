#!/bin/bash
# Dart API Search - Wrapper for Python implementation
# Usage: ./dart-search.sh "company_name" [limit]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/dart-search.py" "$@"
