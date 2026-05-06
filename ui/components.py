import customtkinter as ctk
from PIL import Image

class FileListItem(ctk.CTkFrame):
    def __init__(self, master, filename, on_remove, on_up=None, on_down=None, **kwargs):
        super().__init__(master, fg_color=("gray85", "gray20"), corner_radius=8, **kwargs)
        
        self.filename = filename
        
        self.grid_columnconfigure(1, weight=1)
        
        self.lbl_name = ctk.CTkLabel(self, text=filename, anchor="w")
        self.lbl_name.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        if on_up:
            self.btn_up = ctk.CTkButton(self, text="▲", width=30, command=on_up)
            self.btn_up.grid(row=0, column=2, padx=2)
            
        if on_down:
            self.btn_down = ctk.CTkButton(self, text="▼", width=30, command=on_down)
            self.btn_down.grid(row=0, column=3, padx=2)
            
        self.btn_remove = ctk.CTkButton(self, text="✖", width=30, fg_color="red", hover_color="darkred", command=on_remove)
        self.btn_remove.grid(row=0, column=4, padx=(2, 10))


class PageThumbnail(ctk.CTkFrame):
    def __init__(self, master, image, page_num, on_delete, on_rotate, **kwargs):
        super().__init__(master, fg_color=("gray85", "gray20"), corner_radius=8, **kwargs)
        
        self.image = image
        self.page_num = page_num
        
        if image:
            ctk_img = ctk.CTkImage(light_image=image, dark_image=image, size=(100, 140))
            self.lbl_img = ctk.CTkLabel(self, image=ctk_img, text="")
            self.lbl_img.pack(pady=(10, 5), padx=10)
        else:
            self.lbl_img = ctk.CTkLabel(self, text="No Preview", width=100, height=140)
            self.lbl_img.pack(pady=(10, 5), padx=10)
            
        self.lbl_num = ctk.CTkLabel(self, text=f"Page {page_num}")
        self.lbl_num.pack()
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        self.btn_rotate = ctk.CTkButton(btn_frame, text="⟳", width=30, command=on_rotate)
        self.btn_rotate.pack(side="left", padx=2)
        
        self.btn_delete = ctk.CTkButton(btn_frame, text="✖", width=30, fg_color="red", hover_color="darkred", command=on_delete)
        self.btn_delete.pack(side="left", padx=2)
