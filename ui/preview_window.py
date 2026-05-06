import customtkinter as ctk
import fitz  # PyMuPDF
from PIL import Image
import threading

class PreviewWindow(ctk.CTkToplevel):
    """
    Preview System: Display PDF preview before confirming to save.
    Flow: Edit -> Preview -> Confirm -> Save
    """
    def __init__(self, master, pdf_path, on_confirm):
        super().__init__(master)
        self.title("Preview Edited PDF")
        self.geometry("800x600")
        
        self.transient(master)
        self.grab_set()

        self.pdf_path = pdf_path
        self.on_confirm = on_confirm
        self.current_page = 0
        self.doc = None
        self.total_pages = 0
        self.is_destroyed = False

        self.setup_ui()
        self.load_pdf()

    def setup_ui(self):
        # Top controls
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_info = ctk.CTkLabel(top_frame, text="Loading preview...", font=ctk.CTkFont(weight="bold"))
        self.lbl_info.pack(side="left", padx=10)

        btn_prev = ctk.CTkButton(top_frame, text="< Prev", command=self.prev_page, width=80)
        btn_prev.pack(side="left", padx=5)

        btn_next = ctk.CTkButton(top_frame, text="Next >", command=self.next_page, width=80)
        btn_next.pack(side="left", padx=5)

        btn_confirm = ctk.CTkButton(top_frame, text="Confirm & Save", fg_color="green", hover_color="darkgreen", command=self.confirm)
        btn_confirm.pack(side="right", padx=10)

        btn_cancel = ctk.CTkButton(top_frame, text="Cancel", fg_color="red", hover_color="darkred", command=self.destroy)
        btn_cancel.pack(side="right", padx=5)

        # Image canvas
        self.canvas_frame = ctk.CTkScrollableFrame(self)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.img_label = ctk.CTkLabel(self.canvas_frame, text="")
        self.img_label.pack(pady=10)

    def load_pdf(self):
        def _load():
            try:
                self.doc = fitz.open(self.pdf_path)
                self.total_pages = len(self.doc)
                self.after(0, self.update_preview)
            except Exception as e:
                self.after(0, lambda: self.lbl_info.configure(text=f"Failed to load preview: {e}"))
        threading.Thread(target=_load, daemon=True).start()

    def update_preview(self):
        if not getattr(self, 'doc', None) or self.is_destroyed or getattr(self.doc, 'is_closed', True):
            return

        self.lbl_info.configure(text=f"Page {self.current_page + 1} of {self.total_pages}")
        
        try:
            page = self.doc[self.current_page]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # higher resolution
            
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(pix.width, pix.height))
            self.img_label.configure(image=ctk_img)
        except Exception as e:
            print(f"Preview update error: {e}")

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_preview()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_preview()

    def confirm(self):
        self.on_confirm()
        self.destroy()

    def destroy(self):
        if self.is_destroyed:
            return
        self.is_destroyed = True
        
        if getattr(self, 'doc', None):
            try:
                if not self.doc.is_closed:
                    self.doc.close()
            except Exception:
                pass
            self.doc = None
            
        super().destroy()
