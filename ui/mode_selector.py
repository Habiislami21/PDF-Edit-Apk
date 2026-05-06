import customtkinter as ctk

class ModeSelectorWindow(ctk.CTkToplevel):
    """
    Mode Selection UI: Quick Edit vs Advanced Edit.
    """
    def __init__(self, master, callback):
        super().__init__(master)
        self.title("Select Editing Mode")
        self.geometry("450x300")
        self.resizable(False, False)
        
        # Make modal
        self.transient(master)
        self.grab_set()

        self.callback = callback

        lbl_title = ctk.CTkLabel(self, text="How would you like to edit?", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(pady=(20, 10))

        # Direct Edit
        btn_quick = ctk.CTkButton(
            self, 
            text="Quick Edit (No Layout Change)", 
            font=ctk.CTkFont(size=14),
            height=50,
            command=lambda: self._select("direct")
        )
        btn_quick.pack(pady=10, padx=20, fill="x")
        
        lbl_quick_desc = ctk.CTkLabel(self, text="Stable. Add text/highlights. Recommended for forms.", text_color="gray", font=ctk.CTkFont(size=12))
        lbl_quick_desc.pack(pady=(0, 10))

        # Advanced Edit
        btn_adv = ctk.CTkButton(
            self, 
            text="Advanced Edit (Convert to Word)", 
            font=ctk.CTkFont(size=14),
            height=50,
            fg_color="#A52A2A",
            hover_color="#8B0000",
            command=lambda: self._select("advanced")
        )
        btn_adv.pack(pady=10, padx=20, fill="x")

        lbl_adv_desc = ctk.CTkLabel(self, text="⚠️ Warning: Format might change after conversion.", text_color="#FF6347", font=ctk.CTkFont(size=12))
        lbl_adv_desc.pack(pady=(0, 10))

    def _select(self, mode):
        self.callback(mode)
        self.destroy()
