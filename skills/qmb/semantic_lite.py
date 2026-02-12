#!/usr/bin/env python3
"""
QMB Phase 2 Lite - ONNX-based Semantic Search
No torch required, uses onnxruntime for embeddings
"""

import os
import sys
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import List, Dict

WORKSPACE = Path.home() / ".openclaw/workspace"
INDEX_DIR = Path(__file__).parent / ".qmb_index"

class QMBPhase2Lite:
    """Lightweight semantic search with sklearn TF-IDF"""
    
    def __init__(self):
        self.vectorizer = None
        self.initialized = False
        self.embedding_dim = 384
        
    def init(self):
        """Initialize TF-IDF vectorizer"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            
            print("🔧 Loading TF-IDF vectorizer...")
            
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                min_df=1,
                stop_words=None
            )
            
            self.initialized = True
            print("✅ Phase 2 (sklearn) ready!")
            return True
                
        except ImportError:
            print("⚠️ scikit-learn not installed")
            return False
    
    def fit_transform(self, texts: List[str]):
        """Fit vectorizer and transform texts"""
        if not self.initialized:
            return None
        return self.vectorizer.fit_transform(texts)
    
    def transform(self, text: str):
        """Transform single text"""
        if not self.initialized:
            return None
        return self.vectorizer.transform([text])
    
    def simple_embed(self, text: str) -> np.ndarray:
        """Simple hash-based embedding fallback"""
        words = text.lower().split()
        vec = np.zeros(self.embedding_dim)
        for i, word in enumerate(words[:self.embedding_dim]):
            vec[i % self.embedding_dim] = hash(word) % 1000 / 1000.0
        return vec / (np.linalg.norm(vec) + 1e-8)
    
    def search_tfidf(self, query: str, texts: List[str], top_k: int = 5) -> List[Dict]:
        """Semantic search using TF-IDF + cosine similarity"""
        
        if not self.initialized or not texts:
            return []
        
        # Fit on all texts
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            query_vec = self.vectorizer.transform([query])
            
            # Calculate cosine similarities
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0:  # Only include relevant results
                    results.append({
                        "index": int(idx),
                        "text": texts[idx][:300],
                        "score": float(similarities[idx])
                    })
            
            return results
            
        except Exception as e:
            print(f"TF-IDF error: {e}, using fallback")
            return self.search_fallback(query, texts, top_k)
    
    def search_fallback(self, query: str, texts: List[str], top_k: int = 5) -> List[Dict]:
        """Fallback hash-based search"""
        query_vec = self.simple_embed(query)
        
        results = []
        for i, text in enumerate(texts):
            text_vec = self.simple_embed(text)
            similarity = np.dot(query_vec, text_vec)
            results.append({
                "index": i,
                "text": text[:300],
                "score": float(similarity)
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

def hybrid_search_files(query: str, workspace: Path = WORKSPACE):
    """
    Hybrid search: ripgrep for files + simple semantic ranking
    """
    import subprocess
    
    print(f"🔍 Hybrid search: '{query}'\n")
    
    # Step 1: Find candidate files with ripgrep
    cmd = ["rg", "-l", "-i", "--type", "md", query, str(workspace)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    files = [Path(p) for p in result.stdout.strip().split('\n') if p]
    
    if not files:
        print("❌ No files found")
        return []
    
    print(f"📁 Found {len(files)} candidate files\n")
    
    # Step 2: Semantic ranking
    qmb = QMBPhase2Lite()
    qmb.init()
    
    all_chunks = []
    file_map = []
    
    for file_path in files[:20]:  # Limit to top 20 files
        try:
            content = file_path.read_text(encoding='utf-8')
            chunks = content.split('\n\n')
            for chunk in chunks:
                if len(chunk) > 50:  # Meaningful chunks only
                    all_chunks.append(chunk)
                    file_map.append(file_path)
        except:
            pass
    
    # Rank chunks
    results = qmb.search_tfidf(query, all_chunks, top_k=10)
    
    # Display
    print("=" * 60)
    print("🎯 TOP RESULTS (Semantic + Keyword)")
    print("=" * 60)
    
    seen_files = set()
    for r in results:
        file_path = file_map[r["index"]]
        if file_path not in seen_files:
            seen_files.add(file_path)
            print(f"\n📄 {file_path.name}")
            print(f"   Relevance: {r['score']:.2f}")
            preview = r['text'].replace('\n', ' ')[:150]
            print(f"   {preview}...")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        hybrid_search_files(query)
    else:
        print("Usage: python3 semantic_lite.py 'your search query'")
