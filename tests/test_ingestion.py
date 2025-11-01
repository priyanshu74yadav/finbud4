import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ingestion.document_processor import DocumentProcessor


def test_document_processor():
    processor = DocumentProcessor()
    
    print("=" * 60)
    print("Document Ingestion Module Test")
    print("=" * 60)
    
    print("\n✓ Supported document types:")
    for ext in processor.supported_extensions.keys():
        print(f"  - {ext}")
    
    print("\n✓ Supported image types (OCR):")
    for ext in processor.ocr_handler.supported_image_formats:
        print(f"  - {ext}")
    
    print("\n✓ File type validation:")
    print(f"  - .pdf supported: {processor.is_supported('test.pdf')}")
    print(f"  - .docx supported: {processor.is_supported('test.docx')}")
    print(f"  - .txt supported: {processor.is_supported('test.txt')}")
    print(f"  - .png supported: {processor.is_supported('test.png')}")
    print(f"  - .jpg supported: {processor.is_supported('test.jpg')}")
    
    print("\n" + "=" * 60)
    print("✓ Document Ingestion Module initialized successfully!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Place sample financial documents in backend/data/documents/")
    print("2. Run: python tests/test_ingestion.py <file_path>")
    print("3. Verify text extraction works correctly")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        processor = DocumentProcessor()
        
        print(f"\nProcessing: {file_path}")
        result = processor.process(file_path)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✓ File: {result['file_name']}")
            print(f"✓ Type: {result['file_type']}")
            print(f"✓ Full text extracted: {len(result['full_text'])} characters")
            print(f"✓ File size: {result['file_size']} bytes")
            
            if result['file_type'] == 'pdf':
                print(f"✓ Total pages: {result['total_pages']}")
            elif result['file_type'] == 'docx':
                print(f"✓ Total paragraphs: {result['total_paragraphs']}")
                print(f"✓ Total tables: {result['total_tables']}")
            elif result['file_type'] == 'xlsx':
                print(f"✓ Total sheets: {result['total_sheets']}")
            
            print(f"\n--- FULL TEXT EXTRACTED ({len(result['full_text'])} chars) ---")
            print(result['full_text'])
            print("\n--- END OF EXTRACTED TEXT ---")
    else:
        test_document_processor()
