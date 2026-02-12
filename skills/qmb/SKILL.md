# QMB - Quick Markdown Search

Fast local search for markdown files in your workspace using hybrid search approach.

## What It Does

**Quick search** across all markdown files in workspace:
- Memory files (`memory/*.md`)
- Project READMEs
- Documentation
- Notes and logs

**Keyword-based search** using ripgrep (BM25-style):
- Fast full-text search
- Context lines around matches
- Line numbers for precise reference

## When to Use

- "What did I decide about CEG last week?"
- "When did I resolve that blocker?"
- "Find all mentions of Roturn blog"
- "Search investment analysis notes"

**Replace broken memory_search()** with local alternative.

## Usage

### Basic Search
```bash
./search.sh "search term"
```

### Search with More Context
```bash
./search.sh "search term" --context 5
```

### Search Specific Directory
```bash
./search.sh "CEG" --path memory/
```

### Case Insensitive
```bash
./search.sh "palantir" --ignore-case
```

## Examples

```bash
# Find CEG investment analysis
./search.sh "CEG" --path personal/investment/

# Find recent blockers
./search.sh "blocker" --path memory/

# Find ontology mentions
./search.sh "ontology" --context 3

# Search everything
./search.sh "decision"
```

## Output Format

```
File: memory/2026-02-12.md
Line 245: ## CEG Investment Analysis
Line 246: 
Line 247: **Analysis**: CEG (Constellation Energy) shows...
Line 248: - Current: $360
Line 249: - Fair value: $380-420
```

## Installation

Already installed if you see this file!

**Requirements**:
- `ripgrep` (rg) - Install: `brew install ripgrep`

## Future Enhancements

**Phase 2** (vector search):
- Semantic/meaning-based search
- "Find similar concepts to X"
- True hybrid BM25 + vectors
- Relevance scoring

**Phase 3** (indexing):
- Pre-built index for speed
- Auto-update on file changes
- Caching for frequent queries

## Architecture

**Current (Phase 1)**:
```
Query → ripgrep → Results (with context)
```

**Future (Phase 2)**:
```
BM25 (Keywords) + Vectors (Meaning) → Ranked Results
```

## Benefits

**vs memory_search()**:
- ✅ $0 cost (no external API)
- ✅ Works offline
- ✅ Private (all local)
- ✅ Fast
- ✅ No configuration needed

**vs manual grep**:
- ✅ Better output formatting
- ✅ Smart defaults (MD files only)
- ✅ Context handling
- ✅ Easy to use

## Cost

**Free** - all local execution

## Notes

This is Phase 1 (keyword search only). Vector search coming in Phase 2.

---

**Created**: 2026-02-12  
**Author**: Wayne Manor 🦇  
**Status**: Active (Phase 1)
