# FinBud Synonym System Documentation

## Overview
The synonym system manages financial term mappings to enable intelligent query expansion and document search.

## Components

### 1. SynonymManager (`backend/synonyms/manager.py`)
Core class for managing synonym database.

**Key Methods:**
- `get_synonyms(term)` - Get all variants for a term
- `get_canonical(term)` - Get standardized term name
- `add_synonym(canonical, synonym)` - Add new synonym
- `remove_synonym(canonical, synonym)` - Remove synonym
- `expand_query(query)` - Expand query with all variants
- `search_terms(query)` - Search for terms
- `get_stats()` - Get database statistics

### 2. QueryExpander (`backend/synonyms/query_expander.py`)
Utility for expanding user queries with synonyms.

**Key Methods:**
- `expand_search_terms(query)` - Extract and expand financial terms
- `normalize_term(term)` - Convert to canonical form
- `suggest_terms(partial)` - Auto-complete suggestions
- `get_all_variants(term)` - Get all synonym variants

### 3. API Helpers (`backend/synonyms/api_helpers.py`)
Ready-to-use functions for API endpoints.

**Functions:**
- `get_synonym_response(term)` - Get synonym info
- `add_synonym_response(canonical, synonym)` - Add synonym
- `list_all_synonyms()` - Get all terms
- `search_synonyms_response(query)` - Search terms
- `update_synonym_response(canonical, synonyms)` - Update term
- `delete_synonym_response(canonical, synonym)` - Delete synonym

## Database

**Location:** `backend/data/synonyms/financial_terms.json`

**Statistics:**
- 126 canonical financial terms
- 441 synonym variants
- 3.5 average synonyms per term
- 550 total mappings

**Sample Terms:**
- revenue → Sales, Gross Sales, Total Revenue, Turnover, Income, Top Line
- sales_tax → VAT, GST, Sales Tax, Consumption Tax, Value Added Tax
- profit → Net Income, Earnings, Bottom Line, Net Profit, Profit After Tax

## Usage Examples

### Basic Synonym Lookup
```python
from backend.synonyms.manager import SynonymManager

manager = SynonymManager()
synonyms = manager.get_synonyms("VAT")
# Returns: ['sales_tax', 'VAT', 'GST', 'Sales Tax', ...]
```

### Query Expansion
```python
from backend.synonyms.query_expander import QueryExpander

expander = QueryExpander()
expanded = expander.expand_search_terms("What is our revenue?")
# Returns: {'revenue': ['revenue', 'Sales', 'Gross Sales', ...]}
```

### Add New Synonym
```python
manager = SynonymManager()
manager.add_synonym("revenue", "Annual Sales")
# Automatically saves to JSON file
```

### Search Terms
```python
manager = SynonymManager()
results = manager.search_terms("tax")
# Returns all terms containing "tax"
```

## Testing

Run tests:
```bash
python tests/test_synonyms.py
python tests/test_synonyms.py "sales tax"
```

## Integration with RAG System

The synonym system integrates with the RAG pipeline to:
1. Expand user queries with all synonym variants
2. Normalize terms in documents to canonical forms
3. Improve search accuracy across different terminology
4. Handle regional variations (VAT vs GST vs Sales Tax)

## Future Enhancements

- Industry-specific term sets
- Multi-language support
- Machine learning for automatic synonym discovery
- Context-aware synonym selection
- Confidence scoring for mappings
