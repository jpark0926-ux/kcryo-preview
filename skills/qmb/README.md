# QMB - Quick Markdown Search

Fast local search for your workspace markdown files.

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/qmb
./search.sh "your query"
```

## Examples

```bash
# Find CEG mentions
./search.sh "CEG"

# Search with more context
./search.sh "ontology" --context 5

# Search only in memory
./search.sh "blocker" --path memory/

# Case-sensitive search
./search.sh "Palantir" --case-sensitive
```

## Installation

**Requires**: ripgrep

```bash
# macOS
brew install ripgrep

# Verify
rg --version
```

## Features

✅ Fast keyword search  
✅ Context lines around matches  
✅ Line numbers for precise reference  
✅ Markdown files only  
✅ Color output  
✅ $0 cost (local)

## Phase 1 ✅

Keyword search using ripgrep (BM25-style)

## Phase 2 ✅ (Complete)

**Hybrid search**: Keywords + Semantic ranking (TF-IDF)

```bash
# New hybrid search (recommended)
python3 search.py "your query"

# Example
python3 search.py "성장주"
python3 search.py "Palantir" memory/
```

### Phase 2 Features
- ✅ Keyword search (ripgrep speed)
- ✅ Semantic relevance ranking (TF-IDF)
- ✅ Top results with context
- ✅ File path and line numbers
- ✅ Relevance scores
- ✅ Python 3.14 compatible

### Files
- `search.sh` - Phase 1 (keyword)
- `search.py` - Phase 2 (hybrid) ⭐ Recommended
- `semantic.py` - Full embedding version (optional)
- `hybrid.py` - Combined interface

---

See `SKILL.md` for full documentation.
