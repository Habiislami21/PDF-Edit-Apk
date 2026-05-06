import os
import subprocess
from pdf2docx import Converter
from core.layout_fixer import LayoutFixer
from utils.logger import logger

class ConversionPipeline:
    """
    Advanced Edit Mode Pipeline (PDF -> DOCX -> PDF)
    """
    @staticmethod
    def pdf_to_docx(pdf_path, docx_path, progress_callback=None):
        try:
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            LayoutFixer.fix_layout(docx_path)
            
            logger.info("PDF converted to DOCX and layout fixed.")
            return True
        except Exception as e:
            logger.error(f"Failed to convert PDF to DOCX: {e}")
            return False

    @staticmethod
    def docx_to_pdf(docx_path, pdf_path):
        """
        Uses LibreOffice Headless for superior rendering layout and font handling.
        Provides a fallback to docx2pdf if LibreOffice is not installed.
        """
        try:
            outdir = os.path.dirname(pdf_path)
            
            # Try to locate soffice on Windows
            soffice_path = 'soffice'
            if os.name == 'nt':
                possible_paths = [
                    r"C:\Program Files\LibreOffice\program\soffice.exe",
                    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
                ]
                for p in possible_paths:
                    if os.path.exists(p):
                        soffice_path = p
                        break

            # LibreOffice command
            cmd = [soffice_path, '--headless', '--convert-to', 'pdf', '--outdir', outdir, docx_path]
            
            try:
                process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if process.returncode == 0:
                    base_name = os.path.splitext(os.path.basename(docx_path))[0]
                    generated_pdf = os.path.join(outdir, f"{base_name}.pdf")
                    
                    if generated_pdf != pdf_path:
                        if os.path.exists(pdf_path):
                            os.remove(pdf_path)
                        os.rename(generated_pdf, pdf_path)

                    logger.info("DOCX successfully converted to PDF via LibreOffice.")
                    return True
                else:
                    logger.error(f"LibreOffice conversion failed: {process.stderr}")
            except FileNotFoundError:
                logger.warning("LibreOffice not found in PATH or standard directories. Falling back to docx2pdf.")
                
            # Fallback to docx2pdf
            from docx2pdf import convert as convert_docx_to_pdf
            convert_docx_to_pdf(docx_path, pdf_path)
            logger.info("DOCX successfully converted to PDF via docx2pdf (fallback).")
            return True
            
        except Exception as e:
            logger.error(f"Error during DOCX to PDF conversion: {e}")
            return False
