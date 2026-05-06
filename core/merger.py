from pypdf import PdfWriter, PdfReader
from utils.logger import logger

class PDFMerger:
    def __init__(self):
        self.files_to_merge = []
        
    def add_file(self, file_path):
        if file_path not in self.files_to_merge:
            self.files_to_merge.append(file_path)
            logger.info(f"Added {file_path} to merge list")
            
    def remove_file(self, index):
        if 0 <= index < len(self.files_to_merge):
            removed = self.files_to_merge.pop(index)
            logger.info(f"Removed {removed} from merge list")
            
    def move_file(self, old_index, new_index):
        if 0 <= old_index < len(self.files_to_merge) and 0 <= new_index < len(self.files_to_merge):
            file = self.files_to_merge.pop(old_index)
            self.files_to_merge.insert(new_index, file)
            logger.info(f"Moved file from {old_index} to {new_index}")

    def merge(self, output_path, progress_callback=None):
        try:
            writer = PdfWriter()
            total_files = len(self.files_to_merge)
            
            for i, file_path in enumerate(self.files_to_merge):
                reader = PdfReader(file_path)
                for page in reader.pages:
                    writer.add_page(page)
                
                if progress_callback:
                    progress_callback((i + 1) / total_files)
                    
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
                
            logger.info(f"Successfully merged files into {output_path}")
            return True
        except Exception as e:
            logger.error(f"Merge failed: {str(e)}")
            return False
