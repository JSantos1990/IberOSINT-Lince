import customtkinter as ctk
import config
import os
import subprocess
from pathlib import Path
from ui.recent_reports import RecentReportsWindow


class Toolbar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.pack(
            fill="x",
            padx=25,
            pady=(10, 0)
        )

        self.output_button = ctk.CTkButton(
            self,
            text="📂 Abrir Output",
            width=150,
            command=self.open_output_folder
)

        self.output_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.recent_button = ctk.CTkButton(
            self,
            text="📄 Recientes",
            width=130,
            command=self.open_recent_reports
        )

        self.recent_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.clean_button = ctk.CTkButton(
            self,
            text="🧹 Limpiar",
            width=120,
            command=self.clear_preview
        )

        self.clean_button.pack(
            side="left"
        )

        self.recent_window = None

    def open_recent_reports(self):

        if (
            self.recent_window is None
            or not self.recent_window.winfo_exists()
        ):

            self.recent_window = RecentReportsWindow(self)

        else:

            self.recent_window.lift()
            self.recent_window.focus_force()

    def open_output_folder(self):

        output_path = Path(config.PROJECT_ROOT) / "output"

        output_path.mkdir(parents=True, exist_ok=True)

        subprocess.Popen(
            ["xdg-open", str(output_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def clear_preview(self):

        self.master.master.preview.clear()