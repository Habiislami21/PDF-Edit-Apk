import fitz  # PyMuPDF
from utils.logger import logger

class PDFDirectEditor:
    """
    Direct PDF Edit Mode (Primary).
    Uses PyMuPDF to edit directly on the PDF without changing the layout.
    """
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = None

    def load(self):
        try:
            self.doc = fitz.open(self.pdf_path)
            return True
        except Exception as e:
            logger.error(f"Failed to open PDF for direct editing: {e}")
            return False

    def add_text(self, page_num, point, text, font_size=12, color=(0, 0, 0)):
        if self.doc and not self.doc.is_closed:
            page = self.doc[page_num]
            page.insert_text(point, text, fontsize=font_size, color=color)

    def highlight_text(self, page_num, text_to_highlight):
        if self.doc and not self.doc.is_closed:
            page = self.doc[page_num]
            text_instances = page.search_for(text_to_highlight)
            for inst in text_instances:
                page.add_highlight_annot(inst)

    def redact_text(self, page_num, text_to_redact):
        if self.doc and not self.doc.is_closed:
            page = self.doc[page_num]
            text_instances = page.search_for(text_to_redact)
            for inst in text_instances:
                page.add_redact_annot(inst, text=" ")
            page.apply_redactions()

    def add_watermark(self, text, font_size=50, color=(0.8, 0.8, 0.8)):
        if self.doc and not self.doc.is_closed:
            for page in self.doc:
                rect = page.rect
                p = fitz.Point(rect.width / 2 - 100, rect.height / 2)
                page.insert_text(p, text, fontsize=font_size, color=color, rotate=45)

    def save(self, output_path):
        if getattr(self, 'doc', None) and not self.doc.is_closed:
            self.doc.save(output_path)
            self.doc.close()
            self.doc = None
            return True
        return False
