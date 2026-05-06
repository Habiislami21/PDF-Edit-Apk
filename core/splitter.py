from pypdf import PdfWriter, PdfReader
from pathlib import Path
from utils.logger import logger

class PDFSplitter:
    def __init__(self):
        pass
        
    def split_all(self, input_path, output_dir, progress_callback=None):
        try:
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)
            base_name = Path(input_path).stem
            
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                output_filename = Path(output_dir) / f"{base_name}_page_{i+1}.pdf"
                with open(output_filename, "wb") as output_file:
                    writer.write(output_file)
                    
                if progress_callback:
                    progress_callback((i + 1) / total_pages)
                    
            logger.info(f"Successfully split {input_path} into {total_pages} files")
            return True
        except Exception as e:
            logger.error(f"Split failed: {str(e)}")
            return False

    def extract_range(self, input_path, output_path, start_page, end_page):
        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            # Convert to 0-indexed
            start = max(0, start_page - 1)
            end = min(len(reader.pages), end_page)
            
            for i in range(start, end):
                writer.add_page(reader.pages[i])
                
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
                
            logger.info(f"Successfully extracted pages {start_page}-{end_page} to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Extract range failed: {str(e)}")
            return False
