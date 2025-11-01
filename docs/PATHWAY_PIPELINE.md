# FinBud Pathway Streaming Pipeline Documentation

## Overview
The Pathway streaming pipeline provides real-time document indexing with hybrid search capabilities (vector + keyword search) and automatic synonym expansion.

## Architecture

### Components

1. **Document Processor** - Parses multiple file formats
2. **Text Chunker** - Splits documents into searchable chunks
3. **Embedding Generator** - Creates vector representations using sentence-transformers
4. **Hybrid Search Engine** - Combines keyword (TF-IDF) and vector (cosine similarity) search
5. **RAG Engine** - Orchestrates the entire pipeline with synonym integration

## Key Features

### Real-Time Indexing
- Automatic document processing on upload
- Chunk-based indexing for efficient retrieval
- Vector embeddings for semantic search
- TF-IDF for keyword matching

### Hybrid Search
- **Vector Search (70% weight)**: Semantic similarity using embeddings
- **Keyword Search (30% weight)**: Exact term matching using TF-IDF
- Configurable weights for different use cases

### Synonym Integration
- Automatic query expansion with financial term synonyms
- 126 canonical terms with 441 variants
- Context-aware term normalization

### Performance
- **Indexing**: ~0.5s per document
- **Search**: <20ms per query
- **Embedding dimension**: 384 (all-MiniLM-L6-v2)
- **Chunk size**: 500 words with 50-word overlap

## File Structure

```
backend/indexing/
├── embeddings.py           # Embedding generation and text chunking
├── hybrid_search.py        # Hybrid search engine
├── pathway_pipeline.py     # Main pipeline orchestration
└── rag_engine.py          # RAG engine with synonym integration
```

## Usage Examples

### Initialize Pipeline

```python
from backend.indexing.pathway_pipeline import PathwayDocumentPipeline

pipeline = PathwayDocumentPipeline(
    documents_path="backend/data/documents/",
    index_path="backend/data/index/",
    chunk_size=500,
    chunk_overlap=50
)

# Index all documents
result = pipeline.index_all_documents()
```

### Search Documents

```python
# Basic search
results = pipeline.search(
    query="What is our Q3 revenue?",
    top_k=5,
    keyword_weight=0.3,
    vector_weight=0.7
)

for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"File: {result['file_name']}")
    print(f"Text: {result['text'][:100]}...")
```

### RAG Engine with Synonyms

```python
from backend.indexing.rag_engine import RAGEngine

engine = RAGEngine()
engine.initialize()

# Query with automatic synonym expansion
result = engine.query(
    question="What is the VAT amount?",
    top_k=5,
    use_synonyms=True
)

# VAT automatically expands to: Sales Tax, GST, Consumption Tax, etc.
print(f"Expanded terms: {result['expanded_terms']}")
print(f"Results: {result['result_count']}")
```

### Context-Aware Search

```python
# Get results with surrounding context
result = engine.search_with_context(
    question="revenue growth",
    top_k=3,
    context_window=2  # 2 chunks before and after
)

for res in result['results']:
    print(f"Context before: {res['context_before']}")
    print(f"Main chunk: {res['text']}")
    print(f"Context after: {res['context_after']}")
```

### Add New Document

```python
# Add document to existing index
result = engine.add_document("path/to/new/document.pdf")

if result['success']:
    print(f"Indexed: {result['file_name']}")
    print(f"Chunks: {result['chunks']}")
    print(f"Time: {result['processing_time']:.2f}s")
```

## Configuration

### Chunk Settings

```python
# Smaller chunks for precise retrieval
pipeline = PathwayDocumentPipeline(
    chunk_size=300,
    chunk_overlap=30
)

# Larger chunks for more context
pipeline = PathwayDocumentPipeline(
    chunk_size=800,
    chunk_overlap=100
)
```

### Search Weights

```python
# Favor keyword matching (exact terms)
results = pipeline.search(
    query="revenue",
    keyword_weight=0.7,
    vector_weight=0.3
)

# Favor semantic search (meaning)
results = pipeline.search(
    query="revenue",
    keyword_weight=0.2,
    vector_weight=0.8
)
```

### Embedding Models

```python
from backend.indexing.embeddings import EmbeddingGenerator

# Default: all-MiniLM-L6-v2 (384 dimensions, fast)
embedder = EmbeddingGenerator()

# Alternative: all-mpnet-base-v2 (768 dimensions, more accurate)
embedder = EmbeddingGenerator(model_name="all-mpnet-base-v2")
```

## Performance Optimization

### Indexing Performance
- **Batch processing**: Process multiple documents in parallel
- **Incremental updates**: Only re-index changed documents
- **Chunk caching**: Cache embeddings for unchanged chunks

### Search Performance
- **Top-K limiting**: Retrieve only needed results
- **Early termination**: Stop search when confidence threshold met
- **Index pruning**: Remove low-quality chunks

### Memory Management
- **Lazy loading**: Load embeddings on demand
- **Compression**: Use quantized embeddings (future)
- **Disk caching**: Store embeddings on disk for large datasets

## Testing

### Run Pipeline Tests
```bash
python tests/test_pathway_pipeline.py
```

### Run RAG Engine Tests
```bash
python tests/test_rag_engine.py
```

### Test Specific Query
```python
from backend.indexing.rag_engine import RAGEngine

engine = RAGEngine()
engine.initialize()

result = engine.query("your question here", top_k=5)
print(result)
```

## Integration with LLM

The RAG engine provides context for LLM queries:

```python
# 1. Get relevant context
result = engine.query("What is our Q3 revenue?", top_k=3)

# 2. Build LLM prompt
context = "\n\n".join([r['text'] for r in result['results']])
prompt = f"""Based on the following documents:

{context}

Answer this question: {result['question']}
"""

# 3. Send to LLM (next phase)
# response = llm.generate(prompt)
```

## Statistics

Current system stats:
- **Documents indexed**: 4
- **Total chunks**: 69
- **Embedding dimension**: 384
- **Synonym terms**: 126 canonical, 441 variants
- **Average search time**: 15-20ms
- **Average indexing time**: 0.5s per document

## Future Enhancements

1. **True Streaming**: Real-time file system monitoring
2. **Incremental Updates**: Update only changed chunks
3. **Multi-modal**: Support images, tables, charts
4. **Distributed**: Scale across multiple machines
5. **GPU Acceleration**: Faster embedding generation
6. **Query Caching**: Cache frequent queries
7. **Relevance Feedback**: Learn from user interactions

## Troubleshooting

### Slow Indexing
- Reduce chunk size
- Use smaller embedding model
- Process documents in batches

### Poor Search Results
- Adjust keyword/vector weights
- Increase top_k value
- Enable synonym expansion
- Check document quality

### Memory Issues
- Reduce chunk size
- Process fewer documents at once
- Use disk-based index storage

## References

- Sentence Transformers: https://www.sbert.net/
- Pathway Documentation: https://pathway.com/developers/
- Hybrid Search: https://www.pinecone.io/learn/hybrid-search/
