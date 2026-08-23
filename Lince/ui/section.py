import customtkinter as ctk
import config


class Section(ctk.CTkFrame):

    def __init__(self, master, title):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.pack(
            fill="x",
            padx=18,
            pady=(4, 6)
        )

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 17, "bold"),
            text_color=config.GOLD
        )

        title_label.pack(anchor="w")

        divider = ctk.CTkFrame(
            self,
            height=2,
            fg_color=config.GOLD,
            corner_radius=5
        )

        divider.pack(
            fill="x",
            pady=(2,3)
        )

        self.body = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.body.pack(fill="x")