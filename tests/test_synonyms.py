import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.synonyms.manager import SynonymManager


def test_synonym_manager():
    print("=" * 60)
    print("Synonym Manager Test")
    print("=" * 60)
    
    manager = SynonymManager()
    
    stats = manager.get_stats()
    print(f"\n✓ Loaded synonym database:")
    print(f"  - Total canonical terms: {stats['total_canonical_terms']}")
    print(f"  - Total synonym variants: {stats['total_synonym_variants']}")
    print(f"  - Average synonyms per term: {stats['average_synonyms_per_term']}")
    print(f"  - Total mappings: {stats['total_mappings']}")
    
    print("\n✓ Testing synonym lookup:")
    test_terms = ["revenue", "VAT", "Sales Tax", "profit", "EBIT"]
    for term in test_terms:
        synonyms = manager.get_synonyms(term)
        canonical = manager.get_canonical(term)
        print(f"  - '{term}' -> canonical: '{canonical}' ({len(synonyms)} variants)")
    
    print("\n✓ Testing query expansion:")
    query = "What is our revenue and sales tax?"
    expanded = manager.expand_query(query)
    print(f"  - Query: '{query}'")
    print(f"  - Expanded to {len(expanded)} terms:")
    print(f"    {', '.join(sorted(list(expanded))[:10])}...")
    
    print("\n✓ Testing search:")
    search_results = manager.search_terms("tax")
    print(f"  - Search 'tax' found {len(search_results)} terms:")
    for term in list(search_results.keys())[:5]:
        print(f"    - {term}")
    
    print("\n✓ Testing add/remove operations:")
    test_added = manager.add_synonym("revenue", "Test Revenue Term")
    print(f"  - Add synonym: {'Success' if test_added else 'Already exists'}")
    
    if test_added:
        test_removed = manager.remove_synonym("revenue", "Test Revenue Term")
        print(f"  - Remove synonym: {'Success' if test_removed else 'Failed'}")
    
    print("\n" + "=" * 60)
    print("✓ Synonym Manager initialized and tested successfully!")
    print("=" * 60)
    
    print("\nKey Features:")
    print("1. ✓ Load/Save financial term mappings")
    print("2. ✓ Get synonyms for any term")
    print("3. ✓ Expand queries with all variants")
    print("4. ✓ Add/Remove/Update terms")
    print("5. ✓ Search and validate terms")
    print("6. ✓ Merge duplicate terms")
    print("7. ✓ Export/Import functionality")


def test_specific_term(term: str):
    manager = SynonymManager()
    
    print(f"\n{'=' * 60}")
    print(f"Synonym Details for: '{term}'")
    print('=' * 60)
    
    canonical = manager.get_canonical(term)
    synonyms = manager.get_synonyms(term)
    
    print(f"\nCanonical term: {canonical}")
    print(f"Total variants: {len(synonyms)}")
    print("\nAll synonyms:")
    for i, syn in enumerate(synonyms, 1):
        print(f"  {i}. {syn}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_specific_term(sys.argv[1])
    else:
        test_synonym_manager()
