from pypdf import PdfWriter, PdfReader
from utils.logger import logger

class PDFEditorCore:
    def __init__(self):
        self.doc_path = None
        self.pages = []  # List of dicts: {'reader': reader, 'page_num': num, 'rotation': 0}
        
    def load_document(self, file_path):
        try:
            self.doc_path = file_path
            reader = PdfReader(file_path)
            self.pages = [{'reader': reader, 'page_num': i, 'rotation': 0} for i in range(len(reader.pages))]
            logger.info(f"Editor loaded {file_path} with {len(self.pages)} pages")
            return True
        except Exception as e:
            logger.error(f"Editor failed to load {file_path}: {str(e)}")
            return False
            
    def remove_page(self, index):
        if 0 <= index < len(self.pages):
            self.pages.pop(index)
            logger.info(f"Removed page at index {index}")
            
    def rotate_page(self, index, angle=90):
        if 0 <= index < len(self.pages):
            self.pages[index]['rotation'] = (self.pages[index]['rotation'] + angle) % 360
            logger.info(f"Rotated page at index {index} by {angle} degrees")
            
    def reorder_page(self, old_index, new_index):
        if 0 <= old_index < len(self.pages) and 0 <= new_index < len(self.pages):
            page = self.pages.pop(old_index)
            self.pages.insert(new_index, page)
            logger.info(f"Moved page from {old_index} to {new_index}")
            
    def save(self, output_path, progress_callback=None):
        try:
            writer = PdfWriter()
            total_pages = len(self.pages)
            
            for i, page_info in enumerate(self.pages):
                page = page_info['reader'].pages[page_info['page_num']]
                if page_info['rotation'] != 0:
                    page.rotate(page_info['rotation'])
                writer.add_page(page)
                
                if progress_callback:
                    progress_callback((i + 1) / total_pages)
                    
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
                
            logger.info(f"Successfully saved edited PDF to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save edited PDF: {str(e)}")
            return False
