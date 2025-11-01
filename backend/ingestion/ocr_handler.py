from pathlib import Path
from typing import Dict
import fitz


class OCRHandler:
    
    def __init__(self):
        self.tesseract_available = self._check_tesseract()
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
    
    def _check_tesseract(self) -> bool:
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False
    
    def is_image_supported(self, file_path: str) -> bool:
        extension = Path(file_path).suffix.lower()
        return extension in self.supported_image_formats
    
    def process_scanned_pdf(self, file_path: str, dpi: int = 300) -> Dict:
        if not self.tesseract_available:
            return {
                "error": "Tesseract not installed",
                "message": "Install Tesseract OCR to process scanned documents"
            }
        
        import pytesseract
        from PIL import Image
        import io
        
        doc = fitz.open(file_path)
        pages = []
        full_text = []
        
        for page_num, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=dpi)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            text = pytesseract.image_to_string(img)
            
            pages.append({
                "page_number": page_num,
                "text": text,
                "char_count": len(text)
            })
            full_text.append(text)
        
        doc.close()
        
        return {
            "file_name": Path(file_path).name,
            "file_type": "pdf_scanned",
            "total_pages": len(pages),
            "full_text": "\n\n".join(full_text),
            "pages": pages,
            "ocr_method": "tesseract"
        }
    
    def process_image(self, file_path: str) -> Dict:
        if not self.tesseract_available:
            return {
                "error": "Tesseract not installed",
                "message": "Install Tesseract OCR to process images"
            }
        
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if not self.is_image_supported(file_path):
            return {
                "error": f"Unsupported image format: {extension}",
                "supported": list(self.supported_image_formats)
            }
        
        import pytesseract
        from PIL import Image
        
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        
        return {
            "file_name": path.name,
            "file_type": f"image_{extension[1:]}",
            "full_text": text,
            "char_count": len(text),
            "image_format": extension[1:].upper(),
            "ocr_method": "tesseract"
        }
