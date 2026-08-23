import customtkinter as ctk
import config
from pathlib import Path


class DocumentCard(ctk.CTkFrame):

    def __init__(self, master, filepath, delete_callback):

        super().__init__(
            master,
            fg_color="#2b2b2b",
            corner_radius=8,
            border_width=1,
            border_color="#3d3d3d"
        )

        self.pack(
            fill="x",
            pady=5
        )

        path = Path(filepath)

        # -------------------------------------------------
        # NOMBRE CORTO PARA EVITAR OCULTAR EL BOTÓN ✕
        # -------------------------------------------------

        display_name = path.name

        MAX_FILENAME = 40

        if len(display_name) > MAX_FILENAME:

            stem = path.stem
            suffix = path.suffix

            visible = MAX_FILENAME - len(suffix) - 3

            display_name = f"{stem[:visible]}...{suffix}"

        self.filepath = filepath

        extension = path.suffix.lower()

        icons = {
            ".pdf":  "📕",
            ".docx": "📝",
            ".xlsx": "📊",
            ".csv":  "📈",
            ".txt":  "📄"
        }

        icon = icons.get(extension, "📁")

        size = path.stat().st_size

        if size < 1024:

            size_text = f"{size} B"

        elif size < 1024 * 1024:

            size_text = f"{size/1024:.1f} KB"

        else:

            size_text = f"{size/(1024*1024):.1f} MB"

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=10,
            pady=(8,2)
        )

        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        title = ctk.CTkLabel(
            header,
            text=f"{icon}  {display_name}",
            font=("Segoe UI",13,"bold"),
            anchor="w",
            text_color=config.TEXT
        )

        title.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8)
        )

        delete = ctk.CTkButton(
            header,
            text="✕",
            width=28,
            height=28,
            fg_color="transparent",
            hover_color="#aa3333",
            command=lambda: delete_callback(self.filepath)
        )

        delete.grid(
            row=0,
            column=1,
            sticky="e"
        )

        info = ctk.CTkLabel(
            self,
            text=f"{extension.upper().replace('.','')} • {size_text}",
            anchor="w",
            font=("Segoe UI",11),
            text_color=config.TEXT_SECONDARY
        )

        info.pack(
            fill="x",
            padx=12,
            pady=(0,8)
        )