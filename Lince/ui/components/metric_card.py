import customtkinter as ctk


class MetricCard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        title,
        value="0",
        icon="📊",
        width=190,
        height=150,
        **kwargs
    ):

        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=16,
            **kwargs
        )

        self.grid_propagate(False)

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI Emoji", 34)
        )

        self.icon_label.grid(row=0, column=0, pady=(12, 0))

        self.value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=("Arial", 34, "bold")
        )

        self.value_label.grid(row=1, column=0)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 14)
        )

        self.title_label.grid(row=2, column=0, pady=(0, 12))

    def set_value(self, value):
        self.value_label.configure(text=str(value))