import customtkinter as ctk
from pathlib import Path
import config
from datetime import datetime
import subprocess


class RecentReportsWindow(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        self.title("Informes recientes")

        self.geometry("700x500")

        self.minsize(700, 500)

        self.transient(master)

        self.grab_set()

        self.build_ui()

        self.load_reports()

    def load_reports(self):

        output_path = Path(config.PROJECT_ROOT) / "output"

        if not output_path.exists():

            return

        valid_extensions = {
            ".md",
            ".pdf",
            ".docx"
        }

        files = sorted(
            [
                f for f in output_path.iterdir()
                if (
                    f.is_file()
                    and f.suffix.lower() in valid_extensions
                )
            ],
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )

        self.subtitle.configure(
            text=f"Mostrando {len(files)} informe(s)"
        )

        if not files:

            label = ctk.CTkLabel(
                self.list_frame,
                text="Todavía no hay informes generados."
            )

            label.pack(
                pady=20
            )

            return

        for file in files:

            row = ctk.CTkFrame(
                self.list_frame,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=10,
                pady=4
            )

            row.grid_columnconfigure(0, weight=1)
            row.grid_columnconfigure(1, weight=0)
            row.grid_columnconfigure(2, weight=0)

            display_name = file.name

            if len(display_name) > 55:

                display_name = display_name[:52] + "..."

            name = ctk.CTkLabel(
                row,
                text=f"📄 {display_name}",
                anchor="w",
                width=360
            )

            name.grid(
                row=0,
                column=0,
                sticky="w",
                padx=(5, 10)
            )

            modified = datetime.fromtimestamp(
                file.stat().st_mtime
            ).strftime("%d/%m/%Y %H:%M")

            date = ctk.CTkLabel(
                row,
                text=modified,
                width=130
            )

            date.grid(
                row=0,
                column=1,
                padx=(10, 20)
            )

            open_button = ctk.CTkButton(
                row,
                text="Abrir",
                width=85,
                command=lambda f=file: self.open_report(f)
            )

            open_button.pack_propagate(False)

            open_button.grid(
                row=0,
                column=2,
                sticky="e"
            )

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="📄 Informes recientes",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(
            pady=(20, 10)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 13)
        )

        subtitle.pack(
            pady=(0, 20)
        )

        self.subtitle = subtitle

        self.list_frame = ctk.CTkScrollableFrame(
            self
        )

        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    def open_report(self, file_path):

        subprocess.Popen(
            ["xdg-open", str(file_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )