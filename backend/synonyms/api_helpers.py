from typing import Dict, List
from .manager import SynonymManager


def get_synonym_response(term: str, manager: SynonymManager = None) -> Dict:
    if manager is None:
        manager = SynonymManager()
    
    canonical = manager.get_canonical(term)
    synonyms = manager.get_synonyms(term)
    
    return {
        "query_term": term,
        "canonical_term": canonical,
        "synonyms": synonyms,
        "total_variants": len(synonyms),
        "is_recognized": manager.validate_term(term)
    }


def add_synonym_response(canonical: str, synonym: str, manager: SynonymManager = None) -> Dict:
    if manager is None:
        manager = SynonymManager()
    
    success = manager.add_synonym(canonical, synonym)
    
    return {
        "success": success,
        "canonical_term": canonical,
        "added_synonym": synonym,
        "message": "Synonym added successfully" if success else "Synonym already exists"
    }


def list_all_synonyms(manager: SynonymManager = None) -> Dict:
    if manager is None:
        manager = SynonymManager()
    
    return {
        "synonyms": manager.get_all_terms(),
        "stats": manager.get_stats()
    }


def search_synonyms_response(query: str, manager: SynonymManager = None) -> Dict:
    if manager is None:
        manager = SynonymManager()
    
    results = manager.search_terms(query)
    
    return {
        "search_query": query,
        "results": results,
        "total_matches": len(results)
    }


def update_synonym_response(canonical: str, synonyms: List[str], manager: SynonymManager = None) -> Dict:
    if manager is None:
        manager = SynonymManager()
    
    success = manager.update_term(canonical, synonyms)
    
    return {
        "success": success,
        "canonical_term": canonical,
        "updated_synonyms": synonyms if success else [],
        "message": "Term updated successfully" if success else "Term not found"
    }


def delete_synonym_response(canonical: str, synonym: str = None, manager: SynonymManager = None) -> Dict:
    if manager is None:
        manager = SynonymManager()
    
    if synonym:
        success = manager.remove_synonym(canonical, synonym)
        message = f"Removed synonym '{synonym}'" if success else "Synonym not found"
    else:
        success = manager.remove_term(canonical)
        message = f"Removed term '{canonical}'" if success else "Term not found"
    
    return {
        "success": success,
        "canonical_term": canonical,
        "removed_synonym": synonym,
        "message": message
    }
