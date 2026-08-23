import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.header import Header
from ui.preview import Preview
from ui.dashboard import Dashboard
from ui.toolbar import Toolbar

import config


ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(config.APP_NAME)

        self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")

        self.minsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.configure(fg_color=config.BACKGROUND)

        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.create_layout()

    

    def create_layout(self):

        self.left_panel = Sidebar(self)

        self.left_panel.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.right_panel = ctk.CTkFrame(
            self,
            fg_color=config.BACKGROUND,
            corner_radius=0
        )

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        Header(self.right_panel)

        self.toolbar = Toolbar(self.right_panel)

        #
        # Pestañas
        #

        self.tabs = ctk.CTkTabview(self.right_panel)

        self.tabs.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(5,10)
        )

        #
        # Tabs
        #

        self.tabs.add("📄 Informe IA")

        self.tabs.add("📊 Dashboard")

        #
        # Preview
        #

        self.preview = Preview(
            self.tabs.tab("📄 Informe IA")
        )

        self.preview.pack(
            fill="both",
            expand=True
        )

        #
        # Dashboard
        #

        self.dashboard = Dashboard(
            self.tabs.tab("📊 Dashboard")
        )

        self.dashboard.pack(
            fill="both",
            expand=True
        )

        #
        # Tab inicial
        #

        self.tabs.set("📄 Informe IA")

        