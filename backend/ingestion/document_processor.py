from pathlib import Path
from typing import Dict
from .pdf_parser import PDFParser
from .word_parser import WordParser
from .excel_parser import ExcelParser
from .txt_parser import TxtParser
from .ocr_handler import OCRHandler


class DocumentProcessor:
    
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.word_parser = WordParser()
        self.excel_parser = ExcelParser()
        self.txt_parser = TxtParser()
        self.ocr_handler = OCRHandler()
        
        self.supported_extensions = {
            '.pdf': self.pdf_parser,
            '.docx': self.word_parser,
            '.xlsx': self.excel_parser,
            '.xls': self.excel_parser,
            '.txt': self.txt_parser
        }
    
    def process(self, file_path: str, use_ocr: bool = False) -> Dict:
        path = Path(file_path)
        
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        extension = path.suffix.lower()
        
        if self.ocr_handler.is_image_supported(file_path):
            result = self.ocr_handler.process_image(str(path))
            if "error" not in result:
                result['file_path'] = str(path)
                result['file_size'] = path.stat().st_size
            return result
        
        if extension not in self.supported_extensions:
            return {
                "error": f"Unsupported file type: {extension}",
                "supported": list(self.supported_extensions.keys()) + list(self.ocr_handler.supported_image_formats)
            }
        
        try:
            parser = self.supported_extensions[extension]
            result = parser.parse(str(path))
            
            if extension == '.pdf' and use_ocr:
                if result.get('full_text', '').strip() == '':
                    result = self.ocr_handler.process_scanned_pdf(str(path))
            
            result['file_path'] = str(path)
            result['file_size'] = path.stat().st_size
            
            return result
            
        except Exception as e:
            return {
                "error": f"Failed to process {path.name}",
                "exception": str(e)
            }
    
    def is_supported(self, file_path: str) -> bool:
        extension = Path(file_path).suffix.lower()
        return extension in self.supported_extensions or self.ocr_handler.is_image_supported(file_path)
