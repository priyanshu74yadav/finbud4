from typing import List, Dict, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.indexing.pathway_pipeline import PathwayDocumentPipeline
from backend.synonyms.manager import SynonymManager
from backend.synonyms.query_expander import QueryExpander


class RAGEngine:
    
    def __init__(
        self,
        documents_path: str = "backend/data/documents/",
        index_path: str = "backend/data/index/"
    ):
        self.pipeline = PathwayDocumentPipeline(
            documents_path=documents_path,
            index_path=index_path
        )
        self.synonym_manager = SynonymManager()
        self.query_expander = QueryExpander(self.synonym_manager)
        self.is_indexed = False
    
    def initialize(self) -> Dict:
        result = self.pipeline.index_all_documents()
        self.is_indexed = result.get("success", False)
        return result
    
    def query(
        self,
        question: str,
        top_k: int = 5,
        use_synonyms: bool = True,
        keyword_weight: float = 0.3,
        vector_weight: float = 0.7
    ) -> Dict:
        if not self.is_indexed:
            return {
                "success": False,
                "error": "Index not initialized. Call initialize() first."
            }
        
        expanded_terms = {}
        if use_synonyms:
            expanded_terms = self.query_expander.expand_search_terms(question)
        
        expanded_query = question
        if expanded_terms:
            synonym_additions = []
            for term, variants in expanded_terms.items():
                synonym_additions.extend(variants[:3])
            expanded_query = f"{question} {' '.join(synonym_additions)}"
        
        results = self.pipeline.search(
            query=expanded_query,
            top_k=top_k,
            keyword_weight=keyword_weight,
            vector_weight=vector_weight
        )
        
        return {
            "success": True,
            "question": question,
            "expanded_query": expanded_query if use_synonyms else None,
            "expanded_terms": expanded_terms if use_synonyms else {},
            "results": results,
            "result_count": len(results)
        }
    
    def add_document(self, file_path: str) -> Dict:
        result = self.pipeline.index_document(file_path)
        return result
    
    def get_stats(self) -> Dict:
        pipeline_stats = self.pipeline.get_stats()
        synonym_stats = self.synonym_manager.get_stats()
        
        return {
            "pipeline": pipeline_stats,
            "synonyms": synonym_stats,
            "is_indexed": self.is_indexed
        }
    
    def search_with_context(
        self,
        question: str,
        top_k: int = 5,
        context_window: int = 2
    ) -> Dict:
        query_result = self.query(question, top_k=top_k)
        
        if not query_result.get("success"):
            return query_result
        
        enriched_results = []
        for result in query_result["results"]:
            enriched = result.copy()
            
            doc_id = result.get("doc_id")
            chunk_index = result.get("chunk_index")
            
            if doc_id is not None and chunk_index is not None:
                context_chunks = self._get_surrounding_chunks(
                    doc_id, chunk_index, context_window
                )
                enriched["context_before"] = context_chunks.get("before", [])
                enriched["context_after"] = context_chunks.get("after", [])
            
            enriched_results.append(enriched)
        
        query_result["results"] = enriched_results
        return query_result
    
    def _get_surrounding_chunks(
        self,
        doc_id: int,
        chunk_index: int,
        window: int
    ) -> Dict:
        if doc_id >= len(self.pipeline.indexed_documents):
            return {"before": [], "after": []}
        
        doc = self.pipeline.indexed_documents[doc_id]
        chunks = doc["chunks"]
        
        before = []
        for i in range(max(0, chunk_index - window), chunk_index):
            if i < len(chunks):
                before.append(chunks[i]["text"])
        
        after = []
        for i in range(chunk_index + 1, min(len(chunks), chunk_index + window + 1)):
            after.append(chunks[i]["text"])
        
        return {"before": before, "after": after}
    
    def get_document_summary(self, doc_id: int) -> Optional[Dict]:
        if doc_id >= len(self.pipeline.indexed_documents):
            return None
        
        doc = self.pipeline.indexed_documents[doc_id]
        
        return {
            "doc_id": doc["doc_id"],
            "file_name": doc["file_name"],
            "file_type": doc["file_type"],
            "chunk_count": doc["chunk_count"],
            "indexed_at": doc["indexed_at"],
            "first_chunk": doc["chunks"][0]["text"][:200] if doc["chunks"] else ""
        }
    
    def clear_index(self):
        self.pipeline.clear_index()
        self.is_indexed = False
