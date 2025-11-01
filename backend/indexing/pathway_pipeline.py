import pathway as pw
from pathlib import Path
from typing import Dict, List, Optional
import json
import time
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.ingestion.document_processor import DocumentProcessor
from backend.indexing.embeddings import EmbeddingGenerator, TextChunker
from backend.indexing.hybrid_search import HybridSearchEngine


class PathwayDocumentPipeline:
    
    def __init__(
        self,
        documents_path: str = "backend/data/documents/",
        index_path: str = "backend/data/index/",
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        self.documents_path = Path(documents_path)
        self.index_path = Path(index_path)
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        self.processor = DocumentProcessor()
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=chunk_overlap)
        self.embedder = EmbeddingGenerator()
        self.search_engine = HybridSearchEngine()
        
        self.indexed_documents = []
        self.last_update = None
    
    def process_document(self, file_path: str) -> Optional[Dict]:
        try:
            result = self.processor.process(file_path)
            
            if "error" in result:
                print(f"Error processing {file_path}: {result['error']}")
                return None
            
            return result
        except Exception as e:
            print(f"Exception processing {file_path}: {str(e)}")
            return None
    
    def chunk_document(self, doc_result: Dict) -> List[Dict]:
        metadata = {
            "file_name": doc_result.get("file_name", "unknown"),
            "file_type": doc_result.get("file_type", "unknown"),
            "file_path": doc_result.get("file_path", ""),
        }
        
        if doc_result["file_type"] == "pdf":
            metadata["total_pages"] = doc_result.get("total_pages", 0)
        
        chunks = self.chunker.chunk_text(doc_result["full_text"], metadata)
        return chunks
    
    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedder.generate_batch(texts)
        
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding
        
        return chunks
    
    def index_document(self, file_path: str) -> Dict:
        start_time = time.time()
        
        doc_result = self.process_document(file_path)
        if not doc_result:
            return {"success": False, "error": "Failed to process document"}
        
        chunks = self.chunk_document(doc_result)
        if not chunks:
            return {"success": False, "error": "No chunks generated"}
        
        chunks = self.embed_chunks(chunks)
        
        doc_id = len(self.indexed_documents)
        doc_entry = {
            "doc_id": doc_id,
            "file_name": doc_result["file_name"],
            "file_path": str(file_path),
            "file_type": doc_result["file_type"],
            "chunks": chunks,
            "chunk_count": len(chunks),
            "indexed_at": datetime.now().isoformat(),
            "processing_time": time.time() - start_time
        }
        
        self.indexed_documents.append(doc_entry)
        self.last_update = datetime.now()
        
        self._rebuild_search_index()
        
        return {
            "success": True,
            "doc_id": doc_id,
            "file_name": doc_result["file_name"],
            "chunks": len(chunks),
            "processing_time": doc_entry["processing_time"]
        }
    
    def _rebuild_search_index(self):
        all_chunks = []
        for doc in self.indexed_documents:
            for chunk in doc["chunks"]:
                chunk_with_doc = chunk.copy()
                chunk_with_doc["doc_id"] = doc["doc_id"]
                chunk_with_doc["file_name"] = doc["file_name"]
                all_chunks.append(chunk_with_doc)
        
        if all_chunks:
            self.search_engine.index_documents(all_chunks)
    
    def index_all_documents(self) -> Dict:
        if not self.documents_path.exists():
            return {"success": False, "error": "Documents path does not exist"}
        
        results = []
        for file_path in self.documents_path.rglob("*"):
            if file_path.is_file() and self.processor.is_supported(str(file_path)):
                result = self.index_document(str(file_path))
                results.append(result)
        
        return {
            "success": True,
            "total_documents": len(results),
            "successful": sum(1 for r in results if r.get("success")),
            "failed": sum(1 for r in results if not r.get("success")),
            "results": results
        }
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        keyword_weight: float = 0.3,
        vector_weight: float = 0.7
    ) -> List[Dict]:
        query_embedding = self.embedder.generate(query)
        
        results = self.search_engine.hybrid_search(
            query=query,
            query_embedding=query_embedding,
            top_k=top_k,
            keyword_weight=keyword_weight,
            vector_weight=vector_weight
        )
        
        return results
    
    def get_stats(self) -> Dict:
        total_chunks = sum(doc["chunk_count"] for doc in self.indexed_documents)
        
        return {
            "total_documents": len(self.indexed_documents),
            "total_chunks": total_chunks,
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "embedding_dimension": self.embedder.get_dimension(),
            "documents": [
                {
                    "doc_id": doc["doc_id"],
                    "file_name": doc["file_name"],
                    "file_type": doc["file_type"],
                    "chunks": doc["chunk_count"],
                    "indexed_at": doc["indexed_at"]
                }
                for doc in self.indexed_documents
            ]
        }
    
    def save_index(self):
        index_file = self.index_path / "index_metadata.json"
        
        metadata = {
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "total_documents": len(self.indexed_documents),
            "documents": [
                {
                    "doc_id": doc["doc_id"],
                    "file_name": doc["file_name"],
                    "file_path": doc["file_path"],
                    "file_type": doc["file_type"],
                    "chunk_count": doc["chunk_count"],
                    "indexed_at": doc["indexed_at"]
                }
                for doc in self.indexed_documents
            ]
        }
        
        with open(index_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def load_index(self) -> bool:
        index_file = self.index_path / "index_metadata.json"
        
        if not index_file.exists():
            return False
        
        try:
            with open(index_file, 'r') as f:
                metadata = json.load(f)
            
            for doc_meta in metadata.get("documents", []):
                if Path(doc_meta["file_path"]).exists():
                    self.index_document(doc_meta["file_path"])
            
            return True
        except Exception as e:
            print(f"Error loading index: {str(e)}")
            return False
    
    def clear_index(self):
        self.indexed_documents = []
        self.search_engine.clear_index()
        self.last_update = None
