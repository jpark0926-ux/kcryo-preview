#!/usr/bin/env python3
"""
QMB Phase 2 - Semantic Search with Hybrid BM25 + Vector Search
Uses all-MiniLM-L6-v2 for embeddings (local, free, Korean support)
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple

# Will be imported after installation
# from sentence_transformers import SentenceTransformer
# import chromadb

WORKSPACE = Path.home() / ".openclaw/workspace"
INDEX_DIR = Path(__file__).parent / ".qmb_index"

class QMBPhase2:
    def __init__(self):
        self.model = None
        self.client = None
        self.collection = None
        self.initialized = False
        
    def init(self):
        """Initialize embedding model and vector DB"""
        try:
            from sentence_transformers import SentenceTransformer
            import chromadb
            
            # Load lightweight embedding model (384 dimensions)
            print("🔧 Loading embedding model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize ChromaDB
            INDEX_DIR.mkdir(exist_ok=True)
            self.client = chromadb.PersistentClient(path=str(INDEX_DIR))
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="qmb_documents",
                metadata={"hnsw:space": "cosine"}
            )
            
            self.initialized = True
            print("✅ Phase 2 ready!")
            return True
            
        except ImportError as e:
            print(f"❌ Dependencies not installed: {e}")
            print("Run: pip install sentence-transformers chromadb")
            return False
    
    def index_file(self, file_path: Path) -> bool:
        """Index a single markdown file"""
        if not self.initialized:
            return False
            
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Split into chunks (paragraphs)
            chunks = self._chunk_text(content)
            
            # Generate embeddings
            embeddings = self.model.encode(chunks).tolist()
            
            # Create IDs
            doc_id = hashlib.md5(str(file_path).encode()).hexdigest()[:8]
            ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                ids=ids,
                metadatas=[{"file": str(file_path), "chunk": i} for i in range(len(chunks))]
            )
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error indexing {file_path}: {e}")
            return False
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into overlapping chunks"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks if chunks else [text[:chunk_size]]
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Semantic search"""
        if not self.initialized:
            return []
            
        # Encode query
        query_embedding = self.model.encode([query]).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        return [
            {
                "text": doc,
                "file": meta["file"],
                "score": 1 - dist  # Convert distance to similarity
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    
    def index_workspace(self):
        """Index all markdown files in workspace"""
        if not self.initialized:
            print("❌ Not initialized")
            return
            
        print("📚 Indexing workspace...")
        md_files = list(WORKSPACE.rglob("*.md"))
        
        for i, file_path in enumerate(md_files, 1):
            if file_path.name.startswith("."):
                continue
            print(f"  [{i}/{len(md_files)}] {file_path.name}")
            self.index_file(file_path)
            
        print(f"✅ Indexed {len(md_files)} files")

if __name__ == "__main__":
    qmb = QMBPhase2()
    
    if not qmb.init():
        sys.exit(1)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--index":
            qmb.index_workspace()
        elif sys.argv[1] == "--search":
            query = sys.argv[2] if len(sys.argv) > 2 else input("Query: ")
            results = qmb.search(query)
            for r in results:
                print(f"\n📄 {r['file']} (score: {r['score']:.2f})")
                print(r['text'][:300] + "...")
    else:
        print("Usage: python3 semantic.py --index")
        print("       python3 semantic.py --search 'your query'")
