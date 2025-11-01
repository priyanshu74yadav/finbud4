from typing import List, Set, Dict
from .manager import SynonymManager


class QueryExpander:
    
    def __init__(self, synonym_manager: SynonymManager = None):
        self.manager = synonym_manager or SynonymManager()
    
    def expand_search_terms(self, query: str) -> Dict[str, List[str]]:
        words = self._extract_financial_terms(query)
        
        expanded = {}
        for word in words:
            synonyms = self.manager.get_synonyms(word)
            if len(synonyms) > 1:
                expanded[word] = synonyms
        
        return expanded
    
    def _extract_financial_terms(self, query: str) -> List[str]:
        words = query.lower().split()
        financial_terms = []
        
        for word in words:
            word_clean = word.strip('.,!?;:()[]{}"\'-')
            if word_clean and self.manager.validate_term(word_clean):
                financial_terms.append(word_clean)
        
        multi_word_terms = self._extract_multi_word_terms(query)
        financial_terms.extend(multi_word_terms)
        
        return list(set(financial_terms))
    
    def _extract_multi_word_terms(self, query: str) -> List[str]:
        query_lower = query.lower()
        found_terms = []
        
        for canonical, variants in self.manager.get_all_terms().items():
            all_terms = [canonical] + variants
            for term in all_terms:
                if len(term.split()) > 1 and term.lower() in query_lower:
                    found_terms.append(canonical)
                    break
        
        return found_terms
    
    def build_search_query(self, original_query: str) -> str:
        expanded = self.expand_search_terms(original_query)
        
        if not expanded:
            return original_query
        
        query_parts = [original_query]
        
        for term, synonyms in expanded.items():
            alternatives = [s for s in synonyms if s.lower() != term.lower()]
            if alternatives:
                query_parts.append(f"({' OR '.join(alternatives[:5])})")
        
        return " ".join(query_parts)
    
    def get_all_variants(self, term: str) -> Set[str]:
        synonyms = self.manager.get_synonyms(term)
        return set(s.lower() for s in synonyms)
    
    def normalize_term(self, term: str) -> str:
        return self.manager.get_canonical(term)
    
    def suggest_terms(self, partial: str) -> List[str]:
        partial_lower = partial.lower()
        suggestions = []
        
        for canonical, variants in self.manager.get_all_terms().items():
            if canonical.startswith(partial_lower):
                suggestions.append(canonical)
            else:
                for variant in variants:
                    if variant.lower().startswith(partial_lower):
                        suggestions.append(canonical)
                        break
        
        return sorted(list(set(suggestions)))
