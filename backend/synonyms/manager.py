import json
from pathlib import Path
from typing import Dict, List, Set, Optional


class SynonymManager:
    
    def __init__(self, synonyms_file: str = None):
        if synonyms_file is None:
            synonyms_file = Path(__file__).parent.parent / "data" / "synonyms" / "financial_terms.json"
        
        self.synonyms_file = Path(synonyms_file)
        self.synonyms: Dict[str, List[str]] = {}
        self.reverse_map: Dict[str, str] = {}
        self.load()
    
    def load(self):
        if self.synonyms_file.exists():
            with open(self.synonyms_file, 'r', encoding='utf-8') as f:
                self.synonyms = json.load(f)
            self._build_reverse_map()
        else:
            self.synonyms = {}
            self.reverse_map = {}
    
    def save(self):
        self.synonyms_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.synonyms_file, 'w', encoding='utf-8') as f:
            json.dump(self.synonyms, f, indent=2, ensure_ascii=False)
    
    def _build_reverse_map(self):
        self.reverse_map = {}
        for canonical, variants in self.synonyms.items():
            self.reverse_map[canonical.lower()] = canonical
            for variant in variants:
                self.reverse_map[variant.lower()] = canonical
    
    def add_synonym(self, canonical: str, synonym: str) -> bool:
        canonical = canonical.lower().strip()
        synonym = synonym.strip()
        
        if canonical not in self.synonyms:
            self.synonyms[canonical] = []
        
        if synonym not in self.synonyms[canonical]:
            self.synonyms[canonical].append(synonym)
            self.reverse_map[synonym.lower()] = canonical
            self.save()
            return True
        return False
    
    def add_term(self, canonical: str, synonyms: List[str]) -> bool:
        canonical = canonical.lower().strip()
        
        if canonical in self.synonyms:
            return False
        
        self.synonyms[canonical] = synonyms
        self.reverse_map[canonical] = canonical
        for syn in synonyms:
            self.reverse_map[syn.lower()] = canonical
        
        self.save()
        return True
    
    def remove_synonym(self, canonical: str, synonym: str) -> bool:
        canonical = canonical.lower().strip()
        
        if canonical in self.synonyms and synonym in self.synonyms[canonical]:
            self.synonyms[canonical].remove(synonym)
            if synonym.lower() in self.reverse_map:
                del self.reverse_map[synonym.lower()]
            self.save()
            return True
        return False
    
    def remove_term(self, canonical: str) -> bool:
        canonical = canonical.lower().strip()
        
        if canonical in self.synonyms:
            for syn in self.synonyms[canonical]:
                if syn.lower() in self.reverse_map:
                    del self.reverse_map[syn.lower()]
            
            del self.synonyms[canonical]
            if canonical in self.reverse_map:
                del self.reverse_map[canonical]
            
            self.save()
            return True
        return False
    
    def get_synonyms(self, term: str) -> List[str]:
        term_lower = term.lower().strip()
        canonical = self.reverse_map.get(term_lower)
        
        if canonical and canonical in self.synonyms:
            return [canonical] + self.synonyms[canonical]
        
        return [term]
    
    def get_canonical(self, term: str) -> str:
        term_lower = term.lower().strip()
        return self.reverse_map.get(term_lower, term)
    
    def expand_query(self, query: str) -> Set[str]:
        words = query.lower().split()
        expanded = set()
        
        for word in words:
            word_clean = word.strip('.,!?;:()[]{}"\'-')
            if word_clean:
                synonyms = self.get_synonyms(word_clean)
                expanded.update([s.lower() for s in synonyms])
        
        return expanded
    
    def get_all_terms(self) -> Dict[str, List[str]]:
        return self.synonyms.copy()
    
    def search_terms(self, search_query: str) -> Dict[str, List[str]]:
        search_lower = search_query.lower()
        results = {}
        
        for canonical, variants in self.synonyms.items():
            if search_lower in canonical:
                results[canonical] = variants
                continue
            
            for variant in variants:
                if search_lower in variant.lower():
                    results[canonical] = variants
                    break
        
        return results
    
    def update_term(self, canonical: str, new_synonyms: List[str]) -> bool:
        canonical = canonical.lower().strip()
        
        if canonical not in self.synonyms:
            return False
        
        old_synonyms = self.synonyms[canonical]
        for syn in old_synonyms:
            if syn.lower() in self.reverse_map:
                del self.reverse_map[syn.lower()]
        
        self.synonyms[canonical] = new_synonyms
        for syn in new_synonyms:
            self.reverse_map[syn.lower()] = canonical
        
        self.save()
        return True
    
    def get_stats(self) -> Dict:
        total_terms = len(self.synonyms)
        total_synonyms = sum(len(variants) for variants in self.synonyms.values())
        avg_synonyms = total_synonyms / total_terms if total_terms > 0 else 0
        
        return {
            "total_canonical_terms": total_terms,
            "total_synonym_variants": total_synonyms,
            "average_synonyms_per_term": round(avg_synonyms, 2),
            "total_mappings": len(self.reverse_map)
        }
    
    def merge_terms(self, term1: str, term2: str, keep: str = "term1") -> bool:
        term1_lower = term1.lower().strip()
        term2_lower = term2.lower().strip()
        
        if term1_lower not in self.synonyms or term2_lower not in self.synonyms:
            return False
        
        if keep == "term1":
            canonical = term1_lower
            merge_from = term2_lower
        else:
            canonical = term2_lower
            merge_from = term1_lower
        
        self.synonyms[canonical].extend(self.synonyms[merge_from])
        self.synonyms[canonical] = list(set(self.synonyms[canonical]))
        
        for syn in self.synonyms[merge_from]:
            self.reverse_map[syn.lower()] = canonical
        
        del self.synonyms[merge_from]
        if merge_from in self.reverse_map:
            del self.reverse_map[merge_from]
        
        self.save()
        return True
    
    def validate_term(self, term: str) -> bool:
        term_lower = term.lower().strip()
        return term_lower in self.synonyms or term_lower in self.reverse_map
    
    def export_to_dict(self) -> Dict:
        return {
            "synonyms": self.synonyms,
            "stats": self.get_stats()
        }
    
    def import_from_dict(self, data: Dict) -> bool:
        try:
            if "synonyms" in data:
                self.synonyms = data["synonyms"]
                self._build_reverse_map()
                self.save()
                return True
            return False
        except Exception:
            return False
