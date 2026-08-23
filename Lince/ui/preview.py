import customtkinter as ctk
import config


class Preview(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color=config.PANEL,
            corner_radius=12
        )

        self.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(10,25)
        )

        self.textbox = ctk.CTkTextbox(

            self,

            font=("Consolas",14),

            wrap="word"

        )

        self.textbox.pack(

            fill="both",

            expand=True,

            padx=15,

            pady=15

        )

        self.textbox.insert(

            "1.0",

            "El informe generado aparecerá aquí..."

        )

    def set_text(self, text):

        self.textbox.delete("1.0","end")

        self.textbox.insert("1.0", text)

    def clear(self):

        self.textbox.delete("1.0", "end")

        self.textbox.insert(
            "1.0",
            "El informe generado aparecerá aquí..."
        )