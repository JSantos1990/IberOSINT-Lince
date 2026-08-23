from tkinter import filedialog
from ai.ollama_provider import OllamaProvider
from services.analysis_manager import AnalysisManager
import customtkinter as ctk
import config
import subprocess
import threading
import time

from ui.section import Section
from tkinter import StringVar
from ui.document_card import DocumentCard
from utils.settings import (
    get_last_directory,
    set_last_directory
)


class Sidebar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=config.LEFT_PANEL_WIDTH,
            fg_color=config.PANEL,
            corner_radius=0
        )

        self.pack_propagate(False)

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.scroll.pack(
            fill="both",
            expand=True
        )

        # Lista de documentos cargados
        self.documents_loaded = []
        self.analysis_running = False
        self.analysis_cancelled = False

        self.documents = Section(self.scroll, "📂 Documentos")

        # -------------------------------------------------
        # BOTÓN SELECCIONAR DOCUMENTOS
        # -------------------------------------------------

        self.btn_documents = ctk.CTkButton(
            self.documents.body,
            text="📂 Seleccionar documentos",
            height=42,
            font=("Segoe UI", 14, "bold"),
            fg_color=config.GOLD,
            hover_color="#c89b34",
            text_color="black",
            command=self.select_documents
        )

        self.btn_documents.pack(
            fill="x",
            pady=(0,10)
        )

        ctk.CTkButton(
            self.documents.body,
            text="🗑 Limpiar lista",
            height=34,
            fg_color="#444444",
            hover_color="#666666",
            command=self.clear_documents
        ).pack(fill="x", pady=(0,8))

        self.stats_label = ctk.CTkLabel(
            self.documents.body,
            text="0 evidencias",
            text_color=config.TEXT_SECONDARY,
            anchor="w",
            justify="left",
            font=("Segoe UI",12)
        )

        self.stats_label.pack(fill="x", pady=(0,8))

        ctk.CTkFrame(
            self.documents.body,
            height=2,
            fg_color="#3a3a3a"
        ).pack(fill="x", pady=(0,10))

        # -------------------------------------------------
        # CONTENEDOR VARIABLE PARA LOS DOCUMENTOS
        # -------------------------------------------------

        self.documents_frame = ctk.CTkFrame(
            self.documents.body,
            fg_color="transparent"
        )

        self.documents_frame.pack(
            fill="x"
        )

        self.documents_container = ctk.CTkScrollableFrame(
            self.documents_frame,
            fg_color="transparent"
        )

        self.documents_container.pack(
            fill="x",
            expand=False
        )

        self.show_documents()

        self.ai = Section(self.scroll, "🤖 Motor IA")

        # -------------------------------------------------
        # MOTOR IA
        # -------------------------------------------------

        self.ai_provider = StringVar(value="ollama")

        ctk.CTkRadioButton(
            self.ai.body,
            text="Ollama (Local)",
            variable=self.ai_provider,
            value="ollama",
            command=self.change_ai_provider
        ).pack(anchor="w", pady=(4,2))

        ctk.CTkRadioButton(
            self.ai.body,
            text="Gemini API",
            variable=self.ai_provider,
            value="gemini",
            command=self.change_ai_provider
        ).pack(anchor="w", pady=(0,8))

        # -------------------------------------------------
        # API KEY DE GEMINI
        # -------------------------------------------------

        self.gemini_api_frame = ctk.CTkFrame(
            self.ai.body,
            fg_color="transparent"
        )

        self.gemini_api_label = ctk.CTkLabel(
            self.gemini_api_frame,
            text="🔑 API Key de Gemini",
            anchor="w"
        )

        self.gemini_api_label.pack(
            anchor="w",
            pady=(0, 4)
        )

        self.gemini_api_entry = ctk.CTkEntry(
            self.gemini_api_frame,
            placeholder_text="Introduce tu API Key de Gemini",
            show="•"
        )

        self.gemini_api_entry.pack(
            fill="x"
        )

        ctk.CTkFrame(
            self.ai.body,
            height=2,
            fg_color="#3a3a3a"
        ).pack(fill="x", pady=(0,8))

        self.ai_status = ctk.CTkLabel(
            self.ai.body,
            text="🟢 Configurado",
            text_color="#55d66b",
            anchor="w",
            font=("Segoe UI",12)
        )

        self.ai_status.pack(fill="x")

        self.check_ollama()

        self.model = Section(self.scroll, "🧠 Modelo")

        # -------------------------------------------------
        # MODELO
        # -------------------------------------------------

        self.model_combo = ctk.CTkComboBox(

            self.model.body,

            values=["Cargando..."]

        )

        self.model_combo.pack(
            fill="x",
            pady=(6,0)
        )

        self.load_models()

        self.report = Section(self.scroll, "📄 Tipo de informe")

        self.report_combo = ctk.CTkComboBox(

            self.report.body,

            values=[

                "Resumen técnico",

                "Executive Summary",

                "Informe de incidente",

                "Análisis forense",

                "Informe de vulnerabilidades",

                "Informe de phishing",

                "Análisis de malware",

                "Informe OSINT",

                "Timeline de eventos",

                "Indicadores de compromiso (IOC)"

            ],

            width=300

        )

        self.report_combo.pack(

            fill="x",

            padx=10,

            pady=(10,5)

        )

        self.report_combo.set("Resumen técnico")

        self.goal = Section(self.scroll, "🎯 Objetivo")

        self.goal_textbox = ctk.CTkTextbox(
            self.goal.body,
            height=90,
            wrap="word",
            font=("Segoe UI", 12)
        )

        self.goal_textbox.pack(
            fill="x",
            padx=10,
            pady=(10, 5)
        )

        self.goal_textbox.insert(
            "1.0",
            "Opcional: escriba aquí instrucciones adicionales para la IA..."
        )

    def select_documents(self):

        initial_directory = get_last_directory()

        if not initial_directory:
            initial_directory = None

        files = filedialog.askopenfilenames(

            title="Seleccionar documentos",

            initialdir=initial_directory,

            filetypes=[

                (
                    "Documentos compatibles",
                    "*.pdf *.docx *.txt *.csv *.xlsx"
                ),

                ("PDF", "*.pdf"),
                ("Word", "*.docx"),
                ("Texto", "*.txt"),
                ("CSV", "*.csv"),
                ("Excel", "*.xlsx"),
                ("Todos los archivos", "*.*")

            ]

        )

        if files:

            from pathlib import Path

            set_last_directory(
                str(Path(files[0]).parent)
            )

        self.add_documents(files)

    def add_documents(self, files):

        if not files:
            return

        for file in files:

            if file not in self.documents_loaded:
                self.documents_loaded.append(file)

        self.show_documents()

    def show_documents(self):

        for widget in self.documents_container.winfo_children():

            widget.destroy()

        # Ajustar dinámicamente la altura del listado

        cards = len(self.documents_loaded)

        if cards == 0:
            height = 5
        elif cards == 1:
            height = 55
        else:
            height = min(220, cards * 55)

        self.documents_frame.configure(height=height)

        total_size = 0

        for file in self.documents_loaded:

            import os

            total_size += os.path.getsize(file)

        if total_size < 1024:

            size = f"{total_size} B"

        elif total_size < 1024 * 1024:

            size = f"{total_size/1024:.1f} KB"

        else:

            size = f"{total_size/(1024*1024):.1f} MB"

        self.stats_label.configure(

            text=f"{len(self.documents_loaded)} evidencias\n{size}"

        )

        

        if not self.documents_loaded:

            ctk.CTkLabel(
                self.documents_container,
                text="No hay documentos cargados",
                text_color=config.TEXT_SECONDARY
            ).pack(anchor="w")

            return

        for file in self.documents_loaded:

            DocumentCard(
                self.documents_container,
                file,
                self.remove_document
            )

    def remove_document(self, filepath):

        if filepath in self.documents_loaded:

            self.documents_loaded.remove(filepath)

        self.show_documents()

    def clear_documents(self):

        self.documents_loaded.clear()

        self.show_documents()

    def change_ai_provider(self):

        provider = self.ai_provider.get()

        if provider == "ollama":

            # Ocultar el campo de API de Gemini
            self.gemini_api_frame.pack_forget()

            self.set_ai_status(
                "🟢 Ollama disponible",
                "#55d66b"
            )

            models = OllamaProvider.get_models()

            if not models:
                models = ["No disponible"]

        else:

            # Mostrar el campo de API solo con Gemini
            if not self.gemini_api_frame.winfo_ismapped():

                self.gemini_api_frame.pack(
                    fill="x",
                    pady=(0, 8)
                )

            models = [
                "gemini-flash-latest"
            ]

            self.set_ai_status(
                "🟢 Gemini API",
                "#55d66b"
            )

        self.model_combo.configure(values=models)
        self.model_combo.set(models[0])

    def check_ollama(self):

        if OllamaProvider.is_available():

            self.ai_status.configure(
                text="🟢 Ollama disponible",
                text_color="#55d66b"
            )

        else:

            self.ai_status.configure(
                text="🔴 Ollama no disponible",
                text_color="#d65555"
            )

    def load_models(self):

        models = OllamaProvider.get_models()

        if not models:

            models = ["No disponible"]

        self.model_combo.configure(values=models)

        self.model_combo.set(models[0])

        self.change_ai_provider()

        self.btn_analyze = ctk.CTkButton(

            self.model.body,

            text="🛡 Analizar evidencias",

            command=self.test_ai

        )

        self.btn_analyze.pack(

            fill="x",

            pady=(8,0)

        )

        # -------------------------------------------------
        # BOTÓN DETENER ANÁLISIS (OCULTO)
        # -------------------------------------------------

        self.btn_cancel = ctk.CTkButton(

            self.model.body,

            text="⛔ Detener análisis",

            fg_color="#aa3333",

            hover_color="#c63d3d",

            command=self.cancel_analysis

        )

        # Inicialmente permanece oculto

    def test_ai(self):

        # -------------------------------------------------
        # VALIDAR API DE GEMINI
        # -------------------------------------------------

        if self.ai_provider.get() == "gemini":

            api_key = self.gemini_api_entry.get().strip()

            if not api_key:

                self.master.preview.set_text(
                    "⚠️ Debes introducir una API Key de Gemini "
                    "antes de iniciar el análisis."
                )

                self.set_ai_status(
                    "🟠 API Key requerida",
                    "#ff9900"
                )

                return

        if not self.documents_loaded:

            self.master.preview.set_text(
                "No hay documentos seleccionados."
            )

            return

        self.master.preview.set_text(
            "⏳ Analizando evidencias...\n\n"
            "Por favor espere..."
        )

        self.set_ai_status(
            "🟡 Analizando...",
            "#ffcc33"
    )

        self.btn_analyze.configure(

            state="disabled",

            text="⏳ Analizando..."

        )

        self.btn_cancel.pack(

            fill="x",

            pady=(8,0)

        )

        # -------------------------------------------------
        # GUARDAR LOS DATOS DEL ANÁLISIS ANTES DEL HILO
        # -------------------------------------------------

        self.analysis_provider = self.ai_provider.get()
        self.analysis_model = self.model_combo.get()
        self.analysis_report_type = self.report_combo.get()
        self.analysis_goal = self.get_goal()

        if self.analysis_provider == "gemini":
            self.analysis_api_key = self.gemini_api_entry.get().strip()
        else:
            self.analysis_api_key = None

        hilo = threading.Thread(
            target=self.run_analysis,
            daemon=True
        )

        self.analysis_cancelled = False

        hilo.start()

    def run_analysis(self):

        try:

            documentos = self.documents_loaded

            documento_principal = documentos[0]
            numero_evidencias = len(documentos)

            self.analysis_running = True

            model = self.analysis_model

            tipo = self.analysis_report_type

            threading.Thread(
                target=self.update_timer,
                args=(
                    documento_principal.split("/")[-1],
                    model,
                    tipo,
                    self.analysis_provider
                ),
                daemon=True
            ).start()


            # ------------------------------------------
            # MENSAJE SEGÚN EL MOTOR IA SELECCIONADO
            # ------------------------------------------

            if self.analysis_provider == "ollama":
                mensaje_motor = "🦙 Consultando modelo local (Ollama)..."

            elif self.analysis_provider == "gemini":
                mensaje_motor = "☁️ Consultando API de Gemini..."

            else:
                mensaje_motor = "🤖 Consultando motor de IA..."

            self.after(
                0,
                lambda: self.update_preview(
                    f"""🛡 Analizando evidencias

    ────────────────────────

    📄 Evidencia principal:
    {documento_principal.split("/")[-1]}

    📚 Evidencias cargadas:
    {numero_evidencias}

    🤖 Modelo:
    {model}

    📋 Informe:
    {tipo}

    ────────────────────────

    {mensaje_motor}
    """
                )
            )

            api_key = self.analysis_api_key

            resultado = AnalysisManager.analyze(
                documentos,
                tipo,
                self.analysis_provider,
                model,
                self.analysis_goal,
                api_key
            )

            if self.analysis_cancelled:
                self.analysis_running = False
                return

            # -------------------------------------------------
            # COMPROBAR SI EL ANÁLISIS HA DEVUELTO UN ERROR
            # -------------------------------------------------

            if not isinstance(resultado, dict):

                self.analysis_running = False

                mensaje_error = str(resultado)

                self.after(
                    0,
                    lambda error=mensaje_error: (
                        self.update_preview(
                            f"❌ Error durante el análisis con Gemini:\n\n{error}"
                        ),

                        self.set_ai_status(
                            "🔴 Error",
                            "#d65555"
                        ),

                        self.btn_analyze.configure(
                            state="normal",
                            text="🛡 Analizar evidencias"
                        ),

                        self.btn_cancel.pack_forget()
                    )
                )

                return

            # -------------------------------------------------
            # ANÁLISIS COMPLETADO CORRECTAMENTE
            # -------------------------------------------------

            self.analysis_running = False

            self.after(
                0,
                lambda: (
                    self.update_preview(resultado["report"]),

                    self.master.dashboard.update_dashboard(
                        resultado["ioc"]
                    ),

                    self.master.tabs.set("📄 Informe IA"),

                    self.set_ai_status(
                        "🟢 Análisis completado",
                        "#55d66b"
                    ),

                    self.btn_analyze.configure(
                        state="normal",
                        text="🛡 Analizar evidencias"
                    ),

                    self.btn_cancel.pack_forget()
                )
            )

        except Exception as e:

            self.analysis_running = False

            self.after(
                0,
                lambda error=str(e): (
                    self.update_preview(f"❌ {error}"),
                    self.set_ai_status(
                        "🔴 Error",
                        "#d65555"
                    ),
                    self.btn_analyze.configure(
                        state="normal",
                        text="🛡 Analizar evidencias"
                    ),
                    self.btn_cancel.pack_forget(),
                )
            )

    def update_timer(self, documento, modelo, informe, proveedor):

        if proveedor == "ollama":
            estado = "🦙 Consultando modelo local (Ollama)..."
        else:
            estado = "☁️ Consultando API de Gemini..."

        while self.analysis_running:

            texto = f"""🛡 Analizando evidencias

    ────────────────────────

    📄 Documento

    {documento}

    🤖 Modelo

    {modelo}

    📋 Informe

    {informe}

    ────────────────────────

    🟡 Estado

    {estado}

    Este proceso puede tardar varios minutos
    dependiendo del tamaño del documento
    y del modelo seleccionado.

    No cierre la aplicación.
    """

            self.after(
                0,
                lambda t=texto: self.update_preview(t)
            )

            time.sleep(1)
        
    def update_preview(self, texto):

         self.master.preview.set_text(texto)

    def set_ai_status(self, text, color):

        self.ai_status.configure(

            text=text,

            text_color=color

        )

    def get_goal(self):

        texto = self.goal_textbox.get("1.0", "end").strip()

        if texto.startswith("Opcional:"):
            return ""

        return texto

    def cancel_analysis(self):

        self.analysis_cancelled = True
        self.analysis_running = False

        self.update_preview(
            "⛔ Análisis cancelado por el usuario."
        )

        self.set_ai_status(
            "🟠 Análisis cancelado",
            "#ff9933"
        )

        self.btn_cancel.pack_forget()

        self.btn_analyze.configure(
            state="normal",
            text="🛡 Analizar evidencias"
        )