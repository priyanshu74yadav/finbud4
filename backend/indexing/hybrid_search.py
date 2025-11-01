from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class HybridSearchEngine:
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.documents = []
        self.document_vectors = None
        self.embeddings = []
        self.is_fitted = False
    
    def index_documents(self, documents: List[Dict]):
        self.documents = documents
        texts = [doc['text'] for doc in documents]
        
        if texts:
            self.document_vectors = self.tfidf_vectorizer.fit_transform(texts)
            self.is_fitted = True
        
        if 'embedding' in documents[0]:
            self.embeddings = [doc['embedding'] for doc in documents]
    
    def keyword_search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        if not self.is_fitted or not self.documents:
            return []
        
        query_vector = self.tfidf_vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors)[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(int(idx), float(similarities[idx])) for idx in top_indices if similarities[idx] > 0]
        
        return results
    
    def vector_search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[int, float]]:
        if not self.embeddings:
            return []
        
        query_vec = np.array(query_embedding).reshape(1, -1)
        doc_vecs = np.array(self.embeddings)
        
        similarities = cosine_similarity(query_vec, doc_vecs)[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(int(idx), float(similarities[idx])) for idx in top_indices]
        
        return results
    
    def hybrid_search(
        self,
        query: str,
        query_embedding: List[float],
        top_k: int = 5,
        keyword_weight: float = 0.3,
        vector_weight: float = 0.7
    ) -> List[Dict]:
        keyword_results = self.keyword_search(query, top_k * 2)
        vector_results = self.vector_search(query_embedding, top_k * 2)
        
        scores = {}
        for idx, score in keyword_results:
            scores[idx] = scores.get(idx, 0) + score * keyword_weight
        
        for idx, score in vector_results:
            scores[idx] = scores.get(idx, 0) + score * vector_weight
        
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for idx, score in sorted_results:
            result = self.documents[idx].copy()
            result['score'] = float(score)
            result['rank'] = len(results) + 1
            results.append(result)
        
        return results
    
    def get_document_count(self) -> int:
        return len(self.documents)
    
    def clear_index(self):
        self.documents = []
        self.document_vectors = None
        self.embeddings = []
        self.is_fitted = False
