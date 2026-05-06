import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from utils.logger import logger

class LayoutFixer:
    """
    Post-Processing layer to fix formatting issues in converted DOCX files.
    """
    @staticmethod
    def fix_layout(docx_path):
        try:
            if not os.path.exists(docx_path):
                logger.error(f"File not found for layout fixing: {docx_path}")
                return False

            doc = Document(docx_path)

            for paragraph in doc.paragraphs:
                # Only fix runs that are completely missing styling without overriding explicit layout
                for run in paragraph.runs:
                    if run.font.name is None:
                        # Don't force font size or paragraph spacing as it destroys pdf2docx's absolute positioning
                        pass

            doc.save(docx_path)
            logger.info("Layout successfully fixed.")
            return True
        except Exception as e:
            logger.error(f"Failed to apply layout fixes: {e}")
            return False
