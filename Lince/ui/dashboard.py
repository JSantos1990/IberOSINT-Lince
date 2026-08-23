import customtkinter as ctk

from ui.components.ioc_dashboard import IOCDashboard


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.ioc_dashboard = IOCDashboard(self)

        self.ioc_dashboard.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

    def update_dashboard(self, ioc):

        self.ioc_dashboard.update_dashboard(ioc)