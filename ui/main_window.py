import customtkinter as ctk
import threading
import os
from pathlib import Path
from tkinter import messagebox
from services.file_manager import FileManager
from core.merger import PDFMerger
from core.splitter import PDFSplitter
from core.editor import PDFEditorCore
from models.document import PDFDocument
from ui.components import FileListItem, PageThumbnail
from utils.logger import logger
from core.word_converter import WordConverterCore

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AntigravityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Habi PDF Tools")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Core modules
        self.merger = PDFMerger()
        self.splitter = PDFSplitter()
        self.editor = PDFEditorCore()
        self.word_converter = WordConverterCore()
        self.current_doc = None
        
        # UI Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Habi PDF Tools", font=ctk.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.btn_merge_tab = ctk.CTkButton(self.sidebar_frame, text="Merge PDF", command=lambda: self.select_tab("merge"))
        self.btn_merge_tab.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_split_tab = ctk.CTkButton(self.sidebar_frame, text="Split PDF", command=lambda: self.select_tab("split"))
        self.btn_split_tab.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_edit_tab = ctk.CTkButton(self.sidebar_frame, text="Edit Pages", command=lambda: self.select_tab("edit"))
        self.btn_edit_tab.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_word_tab = ctk.CTkButton(self.sidebar_frame, text="Word Editor", command=lambda: self.select_tab("word"))
        self.btn_word_tab.grid(row=4, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("Dark")
        
        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.setup_merge_view()
        self.setup_split_view()
        self.setup_edit_view()
        self.setup_word_view()
        
        self.select_tab("merge")
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def select_tab(self, name):
        self.frame_merge.pack_forget()
        self.frame_split.pack_forget()
        self.frame_edit.pack_forget()
        self.frame_word.pack_forget()
        
        if name == "merge":
            self.frame_merge.pack(fill="both", expand=True)
        elif name == "split":
            self.frame_split.pack(fill="both", expand=True)
        elif name == "edit":
            self.frame_edit.pack(fill="both", expand=True)
        elif name == "word":
            self.frame_word.pack(fill="both", expand=True)

    # --- MERGE VIEW ---
    def setup_merge_view(self):
        self.frame_merge = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        lbl_title = ctk.CTkLabel(self.frame_merge, text="Merge PDF Files", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.pack(pady=(20, 10))
        
        btn_add = ctk.CTkButton(self.frame_merge, text="+ Add PDF Files", command=self.add_merge_files)
        btn_add.pack(pady=10)
        
        self.merge_list_frame = ctk.CTkScrollableFrame(self.frame_merge)
        self.merge_list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.merge_progress = ctk.CTkProgressBar(self.frame_merge)
        self.merge_progress.pack(fill="x", padx=40, pady=5)
        self.merge_progress.set(0)
        
        btn_process = ctk.CTkButton(self.frame_merge, text="Merge to PDF", command=self.process_merge, fg_color="green", hover_color="darkgreen")
        btn_process.pack(pady=(10, 20))
        
    def add_merge_files(self):
        files = FileManager.select_files(multiple=True)
        for f in files:
            self.merger.add_file(f)
        self.refresh_merge_list()
        
    def refresh_merge_list(self):
        for widget in self.merge_list_frame.winfo_children():
            widget.destroy()
            
        for i, file_path in enumerate(self.merger.files_to_merge):
            item = FileListItem(
                self.merge_list_frame,
                filename=Path(file_path).name,
                on_remove=lambda idx=i: self.remove_merge_file(idx),
                on_up=lambda idx=i: self.move_merge_file(idx, idx-1) if idx > 0 else None,
                on_down=lambda idx=i: self.move_merge_file(idx, idx+1) if idx < len(self.merger.files_to_merge)-1 else None
            )
            item.pack(fill="x", pady=2)
            
    def remove_merge_file(self, index):
        self.merger.remove_file(index)
        self.refresh_merge_list()
        
    def move_merge_file(self, old_index, new_index):
        self.merger.move_file(old_index, new_index)
        self.refresh_merge_list()
        
    def process_merge(self):
        if not self.merger.files_to_merge:
            messagebox.showwarning("Warning", "No files selected to merge.")
            return
            
        output_path = FileManager.save_file("merged_output.pdf")
        if not output_path: return
        
        self.merge_progress.set(0)
        
        def run():
            success = self.merger.merge(output_path, lambda p: self.merge_progress.set(p))
            if success:
                messagebox.showinfo("Success", f"Merged successfully to:\n{output_path}")
            else:
                messagebox.showerror("Error", "Failed to merge PDFs. Check logs.")
            self.merge_progress.set(0)
            
        threading.Thread(target=run, daemon=True).start()

    # --- SPLIT VIEW ---
    def setup_split_view(self):
        self.frame_split = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        lbl_title = ctk.CTkLabel(self.frame_split, text="Split PDF", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.pack(pady=(20, 10))
        
        self.split_file_var = ctk.StringVar(value="No file selected")
        lbl_file = ctk.CTkLabel(self.frame_split, textvariable=self.split_file_var, text_color="gray")
        lbl_file.pack(pady=5)
        
        btn_select = ctk.CTkButton(self.frame_split, text="Select PDF", command=self.select_split_file)
        btn_select.pack(pady=10)
        
        # Options
        options_frame = ctk.CTkFrame(self.frame_split)
        options_frame.pack(pady=20, padx=20, fill="x")
        
        self.split_mode = ctk.StringVar(value="all")
        
        rb_all = ctk.CTkRadioButton(options_frame, text="Split all pages into separate files", variable=self.split_mode, value="all")
        rb_all.pack(anchor="w", padx=20, pady=10)
        
        range_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        range_frame.pack(anchor="w", padx=20, pady=10, fill="x")
        
        rb_range = ctk.CTkRadioButton(range_frame, text="Extract specific range:", variable=self.split_mode, value="range")
        rb_range.pack(side="left")
        
        self.entry_start = ctk.CTkEntry(range_frame, width=50, placeholder_text="Start")
        self.entry_start.pack(side="left", padx=10)
        
        ctk.CTkLabel(range_frame, text="-").pack(side="left")
        
        self.entry_end = ctk.CTkEntry(range_frame, width=50, placeholder_text="End")
        self.entry_end.pack(side="left", padx=10)
        
        self.split_progress = ctk.CTkProgressBar(self.frame_split)
        self.split_progress.pack(fill="x", padx=40, pady=10)
        self.split_progress.set(0)
        
        btn_process = ctk.CTkButton(self.frame_split, text="Process Split", command=self.process_split, fg_color="#1E90FF")
        btn_process.pack(pady=(10, 20))
        
        self.split_input_path = None
        
    def select_split_file(self):
        file = FileManager.select_files(multiple=False)
        if file:
            self.split_input_path = file
            self.split_file_var.set(Path(file).name)
            
    def process_split(self):
        if not self.split_input_path:
            messagebox.showwarning("Warning", "Please select a PDF to split.")
            return
            
        mode = self.split_mode.get()
        
        if mode == "all":
            output_dir = ctk.filedialog.askdirectory(title="Select Output Directory")
            if not output_dir: return
            
            self.split_progress.set(0)
            def run_all():
                success = self.splitter.split_all(self.split_input_path, output_dir, lambda p: self.split_progress.set(p))
                if success: messagebox.showinfo("Success", f"Split completed in:\n{output_dir}")
                else: messagebox.showerror("Error", "Split failed.")
                self.split_progress.set(0)
            threading.Thread(target=run_all, daemon=True).start()
            
        elif mode == "range":
            try:
                start = int(self.entry_start.get())
                end = int(self.entry_end.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid range values.")
                return
                
            output_path = FileManager.save_file(f"extracted_{start}_{end}.pdf")
            if not output_path: return
            
            def run_range():
                success = self.splitter.extract_range(self.split_input_path, output_path, start, end)
                if success: messagebox.showinfo("Success", f"Extraction completed:\n{output_path}")
                else: messagebox.showerror("Error", "Extraction failed.")
            threading.Thread(target=run_range, daemon=True).start()

    # --- EDIT VIEW ---
    def setup_edit_view(self):
        self.frame_edit = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        header_frame = ctk.CTkFrame(self.frame_edit, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        lbl_title = ctk.CTkLabel(header_frame, text="Page Editor", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.pack(side="left")
        
        btn_open = ctk.CTkButton(header_frame, text="Open PDF", command=self.open_edit_file)
        btn_open.pack(side="right", padx=5)
        
        btn_save = ctk.CTkButton(header_frame, text="Save Changes", command=self.save_edit_file, fg_color="green", hover_color="darkgreen")
        btn_save.pack(side="right", padx=5)
        
        self.edit_scroll = ctk.CTkScrollableFrame(self.frame_edit, orientation="horizontal")
        self.edit_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.edit_progress = ctk.CTkProgressBar(self.frame_edit)
        self.edit_progress.pack(fill="x", padx=40, pady=5)
        self.edit_progress.set(0)
        
    def open_edit_file(self):
        file = FileManager.select_files(multiple=False)
        if file:
            self.editor.load_document(file)
            self.current_doc = PDFDocument(file)
            self.current_doc.load()
            self.refresh_edit_view()
            
    def refresh_edit_view(self):
        for widget in self.edit_scroll.winfo_children():
            widget.destroy()
            
        def load_thumbnails():
            for i, page_info in enumerate(self.editor.pages):
                # We need to get the original page number from the reader
                orig_page_num = page_info['page_num']
                img = self.current_doc.get_page_preview(orig_page_num)
                
                # Apply rotation to PIL image for preview
                if img and page_info['rotation'] != 0:
                    img = img.rotate(-page_info['rotation'], expand=True)
                    
                # Ensure UI update happens in main thread using after
                self.after(0, self.add_thumbnail_ui, i, img)

        threading.Thread(target=load_thumbnails, daemon=True).start()
        
    def add_thumbnail_ui(self, index, img):
        thumb = PageThumbnail(
            self.edit_scroll, 
            img, 
            index + 1,
            on_delete=lambda idx=index: self.delete_page(idx),
            on_rotate=lambda idx=index: self.rotate_page(idx)
        )
        thumb.pack(side="left", padx=10, pady=10)
        
    def delete_page(self, index):
        self.editor.remove_page(index)
        self.refresh_edit_view()
        
    def rotate_page(self, index):
        self.editor.rotate_page(index, 90)
        self.refresh_edit_view()
        
    def save_edit_file(self):
        if not self.editor.pages:
            messagebox.showwarning("Warning", "No pages to save.")
            return
            
        output_path = FileManager.save_file("edited_output.pdf")
        if not output_path: return
        
        self.edit_progress.set(0)
        def run():
            success = self.editor.save(output_path, lambda p: self.edit_progress.set(p))
            if success: messagebox.showinfo("Success", f"Saved successfully:\n{output_path}")
            else: messagebox.showerror("Error", "Failed to save PDF.")
            self.edit_progress.set(0)
        threading.Thread(target=run, daemon=True).start()

    # --- WORD EDITOR VIEW ---
    def setup_word_view(self):
        self.frame_word = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        lbl_title = ctk.CTkLabel(self.frame_word, text="Word Editor (PDF ↔ DOCX)", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.pack(pady=(20, 10))
        
        self.word_file_var = ctk.StringVar(value="No PDF file selected")
        lbl_file = ctk.CTkLabel(self.frame_word, textvariable=self.word_file_var, text_color="gray")
        lbl_file.pack(pady=5)
        
        btn_select = ctk.CTkButton(self.frame_word, text="1. Select PDF File", command=self.select_word_file)
        btn_select.pack(pady=10)
        
        self.btn_convert_word = ctk.CTkButton(self.frame_word, text="2. Convert to Word & Edit", command=self.process_pdf_to_word, state="disabled")
        self.btn_convert_word.pack(pady=10)
        
        self.btn_convert_pdf = ctk.CTkButton(self.frame_word, text="3. Save & Convert back to PDF", command=self.process_word_to_pdf, state="disabled", fg_color="green", hover_color="darkgreen")
        self.btn_convert_pdf.pack(pady=10)
        
        self.word_progress = ctk.CTkProgressBar(self.frame_word)
        self.word_progress.pack(fill="x", padx=40, pady=20)
        self.word_progress.set(0)
        
        self.word_input_path = None
        self.current_docx_path = None
        
    def select_word_file(self):
        file = FileManager.select_files(multiple=False)
        if file:
            self.word_input_path = file
            self.word_file_var.set(Path(file).name)
            self.btn_convert_word.configure(state="normal")
            
    def process_pdf_to_word(self):
        if not self.word_input_path: return
        
        # Save temp docx next to original or in temp dir
        temp_dir = FileManager.create_temp_dir()
        base_name = Path(self.word_input_path).stem
        self.current_docx_path = os.path.join(temp_dir, f"{base_name}_edit.docx")
        
        self.word_progress.set(0.5)
        self.btn_convert_word.configure(state="disabled")
        
        def run_convert():
            success = self.word_converter.pdf_to_word(self.word_input_path, self.current_docx_path)
            self.word_progress.set(1.0)
            
            if success:
                self.btn_convert_pdf.configure(state="normal")
                # Open the file for the user to edit
                try:
                    os.startfile(self.current_docx_path)
                    messagebox.showinfo("Action Required", "The Word document has been opened in your default editor.\n\nPlease edit the file, save it (Ctrl+S), close Word, and then click 'Save & Convert back to PDF'.")
                except Exception as e:
                    messagebox.showwarning("Warning", f"Could not open Word automatically. File saved at:\n{self.current_docx_path}\n\nPlease edit it manually.")
            else:
                messagebox.showerror("Error", "Failed to convert PDF to Word.")
                self.btn_convert_word.configure(state="normal")
                self.word_progress.set(0)
                
        threading.Thread(target=run_convert, daemon=True).start()
        
    def process_word_to_pdf(self):
        if not self.current_docx_path or not os.path.exists(self.current_docx_path):
            messagebox.showerror("Error", "Word file not found. Please convert first.")
            return
            
        output_path = FileManager.save_file("final_edited.pdf")
        if not output_path: return
        
        self.word_progress.set(0.5)
        self.btn_convert_pdf.configure(state="disabled")
        
        def run_back():
            success = self.word_converter.word_to_pdf(self.current_docx_path, output_path)
            self.word_progress.set(1.0)
            
            if success:
                messagebox.showinfo("Success", f"Successfully converted back to PDF:\n{output_path}")
            else:
                messagebox.showerror("Error", "Failed to convert Word back to PDF.\nEnsure you have closed Microsoft Word before converting.")
                self.btn_convert_pdf.configure(state="normal")
                self.word_progress.set(0)
                
        threading.Thread(target=run_back, daemon=True).start()
