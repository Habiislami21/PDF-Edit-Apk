import os
import tempfile
from pathlib import Path
from tkinter import filedialog
from utils.logger import logger

class FileManager:
    @staticmethod
    def select_files(multiple=True):
        try:
            if multiple:
                files = filedialog.askopenfilenames(
                    title="Select PDF Files",
                    filetypes=[("PDF Files", "*.pdf")]
                )
                return list(files) if files else []
            else:
                file = filedialog.askopenfilename(
                    title="Select PDF File",
                    filetypes=[("PDF Files", "*.pdf")]
                )
                return file if file else None
        except Exception as e:
            logger.error(f"Error selecting files: {str(e)}")
            return []

    @staticmethod
    def save_file(default_name="output.pdf"):
        try:
            file = filedialog.asksaveasfilename(
                title="Save PDF As",
                defaultextension=".pdf",
                initialfile=default_name,
                filetypes=[("PDF Files", "*.pdf")]
            )
            return file if file else None
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return None
            
    @staticmethod
    def create_temp_dir():
        temp_dir = tempfile.mkdtemp(prefix="pdf_editor_")
        logger.info(f"Created temporary directory: {temp_dir}")
        return temp_dir
