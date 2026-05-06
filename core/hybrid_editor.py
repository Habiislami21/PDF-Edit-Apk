from core.pdf_direct_editor import PDFDirectEditor
from core.conversion_pipeline import ConversionPipeline

class HybridEditor:
    """
    Coordinates between Direct Edit Mode and Advanced Edit Mode.
    """
    def __init__(self):
        self.direct_editor = None
        self.current_mode = None

    def load_direct_editor(self, pdf_path):
        self.direct_editor = PDFDirectEditor(pdf_path)
        return self.direct_editor.load()

    def direct_add_text(self, page_num, point, text):
        if self.direct_editor:
            self.direct_editor.add_text(page_num, point, text)

    def direct_highlight(self, page_num, text):
        if self.direct_editor:
            self.direct_editor.highlight_text(page_num, text)

    def direct_redact(self, page_num, text):
        if self.direct_editor:
            self.direct_editor.redact_text(page_num, text)

    def save_direct_edit(self, output_path):
        if self.direct_editor:
            return self.direct_editor.save(output_path)
        return False

    def convert_to_word(self, pdf_path, docx_path, progress_callback=None):
        return ConversionPipeline.pdf_to_docx(pdf_path, docx_path, progress_callback)

    def convert_to_pdf(self, docx_path, pdf_path):
        return ConversionPipeline.docx_to_pdf(docx_path, pdf_path)
