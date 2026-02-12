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

## Phase 1 (Current)

Keyword search using ripgrep (BM25-style)

## Phase 2 (Future)

Hybrid search: Keywords + Vector embeddings (semantic meaning)

---

See `SKILL.md` for full documentation.
