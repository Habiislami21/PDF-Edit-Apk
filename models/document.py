import fitz  # PyMuPDF
from pathlib import Path
from utils.logger import logger

class PDFDocument:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.doc = None
        self.name = self.file_path.name
        self.page_count = 0
        
    def load(self):
        try:
            self.doc = fitz.open(self.file_path)
            self.page_count = len(self.doc)
            logger.info(f"Loaded PDF: {self.name} with {self.page_count} pages")
            return True
        except Exception as e:
            logger.error(f"Failed to load PDF {self.name}: {str(e)}")
            return False
            
    def close(self):
        if self.doc:
            self.doc.close()
            
    def get_page_preview(self, page_num, zoom=0.2):
        """Returns a Pillow Image of the page."""
        try:
            if not self.doc:
                self.load()
            page = self.doc.load_page(page_num)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # Convert PyMuPDF pixmap to PIL Image
            from PIL import Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            return img
        except Exception as e:
            logger.error(f"Failed to get preview for page {page_num}: {str(e)}")
            return None
