import fitz
from pathlib import Path
from typing import Dict, List


class PDFParser:
    
    def parse(self, file_path: str) -> Dict:
        doc = fitz.open(file_path)
        
        pages = []
        full_text = []
        
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            pages.append({
                "page_number": page_num,
                "text": text,
                "char_count": len(text)
            })
            full_text.append(text)
        
        metadata = doc.metadata
        doc.close()
        
        return {
            "file_name": Path(file_path).name,
            "file_type": "pdf",
            "total_pages": len(pages),
            "full_text": "\n\n".join(full_text),
            "pages": pages,
            "metadata": {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", "")
            }
        }
    
    def extract_tables(self, file_path: str) -> List[Dict]:
        doc = fitz.open(file_path)
        tables = []
        
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("blocks")
            tables.append({
                "page": page_num,
                "blocks": len(blocks)
            })
        
        doc.close()
        return tables
