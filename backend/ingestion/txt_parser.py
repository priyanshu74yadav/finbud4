from pathlib import Path
from typing import Dict


class TxtParser:
    
    def parse(self, file_path: str) -> Dict:
        path = Path(file_path)
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        lines = text.split('\n')
        
        return {
            "file_name": path.name,
            "file_type": "txt",
            "total_lines": len(lines),
            "full_text": text,
            "char_count": len(text),
            "metadata": {
                "encoding": "utf-8"
            }
        }
