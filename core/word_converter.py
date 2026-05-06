import os
from pathlib import Path
from pdf2docx import Converter
from docx2pdf import convert as convert_docx_to_pdf
from utils.logger import logger

class WordConverterCore:
    def __init__(self):
        pass
        
    def pdf_to_word(self, pdf_path, docx_path, progress_callback=None):
        try:
            # pdf2docx Converter
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
            logger.info(f"Successfully converted PDF to DOCX: {docx_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to convert PDF to Word: {str(e)}")
            return False
            
    def word_to_pdf(self, docx_path, pdf_path):
        try:
            # docx2pdf uses MS Word via COM on Windows
            convert_docx_to_pdf(docx_path, pdf_path)
            logger.info(f"Successfully converted DOCX to PDF: {pdf_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to convert Word to PDF: {str(e)}")
            return False
