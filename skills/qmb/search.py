#!/usr/bin/env python3
"""
QMB Phase 2 - Fast Hybrid Search (Production Ready)
Combines ripgrep speed with simple semantic ranking
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from collections import Counter

WORKSPACE = Path.home() / ".openclaw/workspace"

def keyword_search(query: str, path: Path = WORKSPACE):
    """Fast keyword search using ripgrep"""
    cmd = ["rg", "-i", "-n", "--type", "md", "-C", "2", query, str(path)]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout
    except:
        return ""

def extract_chunks(text: str, query_words: set):
    """Extract relevant chunks containing query words"""
    chunks = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        # Score based on query word matches
        line_lower = line.lower()
        score = sum(1 for word in query_words if word in line_lower)
        
        if score > 0:
            # Get context
            context_start = max(0, i - 1)
            context_end = min(len(lines), i + 2)
            context = '\n'.join(lines[context_start:context_end])
            
            chunks.append({
                "text": context.strip(),
                "score": score,
                "line": i + 1
            })
    
    # Sort by score
    chunks.sort(key=lambda x: x["score"], reverse=True)
    return chunks[:10]  # Top 10 chunks

def hybrid_search(query: str, path: str = ""):
    """
    Hybrid search: Fast keyword + semantic relevance ranking
    """
    search_path = WORKSPACE / path if path else WORKSPACE
    query_words = set(query.lower().split())
    
    print(f"🔍 Hybrid search: '{query}'")
    print(f"📁 Path: {search_path}\n")
    
    # Step 1: Find files with ripgrep
    cmd = ["rg", "-l", "-i", "--type", "md", query, str(search_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    files = [Path(p) for p in result.stdout.strip().split('\n') if p]
    
    if not files:
        print("❌ No results found")
        return
    
    print(f"📄 Found {len(files)} files\n")
    
    # Step 2: Rank and extract best chunks from each file
    all_results = []
    
    for file_path in files[:15]:  # Top 15 files
        try:
            content = file_path.read_text(encoding='utf-8')
            chunks = extract_chunks(content, query_words)
            
            for chunk in chunks:
                all_results.append({
                    "file": file_path.name,
                    "path": str(file_path.relative_to(WORKSPACE)),
                    "text": chunk["text"],
                    "score": chunk["score"],
                    "line": chunk["line"]
                })
        except:
            pass
    
    # Sort all results by score
    all_results.sort(key=lambda x: x["score"], reverse=True)
    
    # Display top results
    print("=" * 70)
    print("🎯 TOP RESULTS (Ranked by relevance)")
    print("=" * 70)
    
    seen_files = set()
    for r in all_results[:10]:
        file_key = f"{r['file']}:{r['line']}"
        if file_key not in seen_files:
            seen_files.add(file_key)
            print(f"\n📄 {r['path']} (line {r['line']}, score: {r['score']})")
            preview = r['text'].replace('\n', ' | ')[:200]
            print(f"   {preview}...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        hybrid_search(query, path)
    else:
        print("Usage: python3 search.py 'query' [path]")
        print("Example: python3 search.py '텐배거' memory/")
