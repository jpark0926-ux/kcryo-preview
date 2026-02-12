#!/usr/bin/env python3
"""
QMB Hybrid Search - Combines Phase 1 (keyword/BM25) + Phase 2 (semantic/vector)
Best of both worlds: exact matching + meaning matching
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict

WORKSPACE = Path.home() / ".openclaw/workspace"
SKILL_DIR = Path(__file__).parent

def keyword_search(query: str, path: str = "", context: int = 2) -> List[Dict]:
    """Phase 1: Fast keyword search using ripgrep"""
    
    search_path = WORKSPACE / path if path else WORKSPACE
    
    cmd = [
        "rg", "-i", "--type", "md",
        "-C", str(context),
        "-n", "--color", "never",
        query, str(search_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        results = []
        current_file = None
        current_matches = []
        
        for line in result.stdout.split('\n'):
            if line.startswith(search_path.parent.name) or line.startswith('/'):
                # New file
                if current_file and current_matches:
                    results.append({
                        "file": current_file,
                        "matches": current_matches,
                        "type": "keyword"
                    })
                current_file = line.strip()
                current_matches = []
            elif ':' in line:
                current_matches.append(line)
        
        # Add last file
        if current_file and current_matches:
            results.append({
                "file": current_file,
                "matches": current_matches,
                "type": "keyword"
            })
            
        return results
        
    except Exception as e:
        print(f"Keyword search error: {e}")
        return []

def semantic_search(query: str, top_k: int = 5) -> List[Dict]:
    """Phase 2: Semantic/meaning-based search"""
    
    try:
        # Import and run semantic search
        sys.path.insert(0, str(SKILL_DIR))
        from semantic import QMBPhase2
        
        qmb = QMBPhase2()
        if not qmb.init():
            return []
            
        return qmb.search(query, top_k)
        
    except Exception as e:
        print(f"Semantic search not available: {e}")
        return []

def hybrid_search(query: str, path: str = "", top_k: int = 10) -> None:
    """
    Hybrid search: Run both keyword + semantic, merge and rank
    """
    print(f"🔍 Hybrid search: '{query}'\n")
    
    # Phase 1: Keyword search (fast)
    print("Phase 1: Keyword search...")
    keyword_results = keyword_search(query, path)
    print(f"  Found {len(keyword_results)} files via keywords\n")
    
    # Phase 2: Semantic search (if available)
    print("Phase 2: Semantic search...")
    semantic_results = semantic_search(query, top_k)
    print(f"  Found {len(semantic_results)} results via meaning\n")
    
    # Display results
    print("=" * 50)
    print("📊 COMBINED RESULTS")
    print("=" * 50)
    
    # Show keyword results
    if keyword_results:
        print("\n🎯 Exact Matches (Keywords):")
        for r in keyword_results[:3]:
            print(f"\n  📄 {r['file']}")
            for m in r['matches'][:5]:
                print(f"    {m}")
    
    # Show semantic results
    if semantic_results:
        print("\n🧠 Semantic Matches (Meaning):")
        for r in semantic_results[:5]:
            print(f"\n  📄 {r['file']} (relevance: {r['score']:.2f})")
            preview = r['text'][:200].replace('\n', ' ')
            print(f"    {preview}...")
    
    if not keyword_results and not semantic_results:
        print("\n❌ No results found")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="QMB Hybrid Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--path", default="", help="Subdirectory to search")
    parser.add_argument("-n", "--top-k", type=int, default=10, help="Number of semantic results")
    
    args = parser.parse_args()
    
    hybrid_search(args.query, args.path, args.top_k)
