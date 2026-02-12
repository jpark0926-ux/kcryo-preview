#!/bin/bash
# QMB - Quick Markdown Search
# Fast local search for markdown files

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
CONTEXT=2
PATH_FILTER=""
CASE_FLAG="-i"
WORKSPACE="${HOME}/.openclaw/workspace"

# Help
show_help() {
    echo "QMB - Quick Markdown Search"
    echo ""
    echo "Usage: $0 <query> [options]"
    echo ""
    echo "Options:"
    echo "  --context N        Number of context lines (default: 2)"
    echo "  --path PATH        Search only in PATH (relative to workspace)"
    echo "  --case-sensitive   Case-sensitive search"
    echo "  --ignore-case      Case-insensitive search (default)"
    echo "  --help             Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 'CEG'"
    echo "  $0 'ontology' --context 5"
    echo "  $0 'blocker' --path memory/"
    echo "  $0 'Palantir' --case-sensitive"
}

# Parse arguments
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

QUERY="$1"
shift

while [ $# -gt 0 ]; do
    case "$1" in
        --context)
            CONTEXT="$2"
            shift 2
            ;;
        --path)
            PATH_FILTER="$2"
            shift 2
            ;;
        --case-sensitive)
            CASE_FLAG=""
            shift
            ;;
        --ignore-case)
            CASE_FLAG="-i"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if ripgrep is installed
if ! command -v rg &> /dev/null; then
    echo -e "${RED}Error: ripgrep (rg) is not installed${NC}"
    echo "Install: brew install ripgrep"
    exit 1
fi

# Build search path
SEARCH_PATH="$WORKSPACE"
if [ -n "$PATH_FILTER" ]; then
    SEARCH_PATH="$WORKSPACE/$PATH_FILTER"
fi

# Check if path exists
if [ ! -e "$SEARCH_PATH" ]; then
    echo -e "${RED}Error: Path not found: $SEARCH_PATH${NC}"
    exit 1
fi

# Run search
echo -e "${BLUE}🔍 Searching for: ${YELLOW}\"$QUERY\"${NC}"
echo -e "${BLUE}📁 Path: ${NC}$SEARCH_PATH"
echo ""

# ripgrep search with formatting
rg $CASE_FLAG \
    --type md \
    --context "$CONTEXT" \
    --line-number \
    --heading \
    --color always \
    --max-columns 150 \
    --smart-case \
    "$QUERY" \
    "$SEARCH_PATH" \
    2>/dev/null || {
        echo -e "${YELLOW}No results found${NC}"
        exit 0
    }

echo ""
echo -e "${GREEN}✓ Search complete${NC}"
