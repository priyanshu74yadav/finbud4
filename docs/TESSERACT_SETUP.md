# Tesseract OCR Setup Guide

## Overview
Tesseract OCR is used to extract text from scanned documents and images (PNG, JPG, etc.).

## Installation

### Windows
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (default location: `C:\Program Files\Tesseract-OCR\`)
3. The system will auto-detect Tesseract at common paths

### Linux
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### macOS
```bash
brew install tesseract
```

## Auto-Detection

The OCR handler automatically checks these paths:
- `C:\Program Files\Tesseract-OCR\tesseract.exe` (Windows)
- `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe` (Windows)
- `C:\Tesseract-OCR\tesseract.exe` (Windows)
- `/usr/bin/tesseract` (Linux)
- `/usr/local/bin/tesseract` (macOS)

## Verification

Test if Tesseract is working:

```python
from backend.ingestion.ocr_handler import OCRHandler

handler = OCRHandler()
if handler.tesseract_available:
    print("✓ Tesseract is available!")
else:
    print("❌ Tesseract not found")
```

## Supported Image Formats

- .jpg / .jpeg
- .png
- .bmp
- .tiff / .tif
- .gif

## Usage

### Process Image
```python
from backend.ingestion.document_processor import DocumentProcessor

processor = DocumentProcessor()
result = processor.process("path/to/image.png")

print(result['full_text'])  # Extracted text
```

### Process Scanned PDF
```python
result = processor.process("path/to/scanned.pdf", use_ocr=True)
```

## Performance

- PNG image (145KB): ~5.4 seconds
- Quality depends on image resolution and clarity
- Higher DPI = better accuracy but slower processing

## Troubleshooting

### "Tesseract not installed" error
1. Verify Tesseract is installed
2. Check installation path matches one of the auto-detected paths
3. Restart your terminal/IDE after installation

### Poor OCR accuracy
1. Increase image resolution
2. Improve image contrast
3. Remove noise from image
4. Use higher quality scans

### Slow processing
1. Reduce image resolution
2. Process smaller images
3. Use batch processing for multiple images

## Current Status

✅ Tesseract 5.5.0 detected and configured
✅ All image formats supported
✅ Auto-detection working
✅ OCR processing functional
