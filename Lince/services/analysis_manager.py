from parsers.txt_parser import TXTParser
from parsers.pdf_parser import PDFParser
from ai.prompt_manager import PromptManager
from ai.ai_manager import AIManager
from exporters.markdown_exporter import MarkdownExporter
from datetime import datetime
import time
from parsers.docx_parser import DOCXParser
from parsers.csv_parser import CSVParser
from parsers.xlsx_parser import XLSXParser
from services.logger import AnalysisLogger
from services.ioc_engine import IOCEngine
from exporters.ioc_json_exporter import IOCJsonExporter


class AnalysisManager:

    @staticmethod
    def analyze(
    document_path,
    report_type,
    provider,
    model,
    goal="",
    api_key=None
):

        import os

        # -------------------------------------------------
        # ADMITIR UNA O VARIAS EVIDENCIAS
        # -------------------------------------------------

        if isinstance(document_path, str):
            document_paths = [document_path]
        else:
            document_paths = document_path

        document_path = document_paths[0]
        texto = ""

        for index, document_path in enumerate(document_paths, start=1):

            extension = os.path.splitext(document_path)[1].lower()

            if extension == ".txt":
                contenido = TXTParser.read(document_path)

            elif extension == ".pdf":
                contenido = PDFParser.parse(document_path)

            elif extension == ".docx":
                contenido = DOCXParser.parse(document_path)

            elif extension == ".csv":
                contenido = CSVParser.extract_text(document_path)

            elif extension == ".xlsx":
                contenido = XLSXParser.extract_text(document_path)

            else:
                raise ValueError(
                    f"Formato no soportado: {extension}"
                )

            texto += f"""

        ============================================================
        EVIDENCIA {index}
        Archivo: {os.path.basename(document_path)}
        Formato: {extension.upper().replace('.', '')}
        ============================================================

        {contenido}

        """

        # -------------------------------------------------
        # VALIDACIÓN DEL CONTENIDO
        # -------------------------------------------------

        texto = texto.strip()

        # -------------------------------------------------
        # EXTRACCIÓN AUTOMÁTICA DE IOC
        # -------------------------------------------------

        ioc_result = IOCEngine.extract_all(texto)

        if len(texto) == 0:

            if extension == ".pdf":

                raise ValueError(
                    "Error de validación:\n\n"
                    "No se ha podido extraer texto del documento PDF.\n\n"
                    "Es muy probable que se trate de un PDF escaneado o formado únicamente por imágenes.\n\n"
                    "Realice un proceso OCR y vuelva a intentarlo."
                )

            elif extension == ".docx":

                raise ValueError(
                    "Error de validación:\n\n"
                    "El documento Word no contiene texto."
                )

            elif extension == ".txt":

                raise ValueError(
                    "Error de validación:\n\n"
                    "El archivo de texto está vacío."
                )

            if len(texto) < 50:

                raise ValueError(
                    "Error de validación:\n\n"
                    "El documento contiene muy poco texto para generar un informe fiable.\n\n"
                    "Seleccione un documento con mayor contenido."
                )

        prompt = PromptManager.build(
            report_type,
            texto,
            goal,
            ioc_result
        )

        try:

            inicio = time.time()

            respuesta = AIManager.generate(

                provider,

                model,

                prompt,

                api_key

            )

            fin = time.time()

            tiempo_total = int(fin - inicio)

            minutos = tiempo_total // 60

            segundos = tiempo_total % 60

            tiempo_analisis = f"{minutos} min {segundos} s"

        except Exception as e:

            AnalysisLogger.write(
                document_paths[0],
                model,
                report_type,
                "ERROR"
            )

            mensaje = str(e)

            if provider == "gemini":

                posibles_causas = """Posibles causas:

            • El servicio de Gemini puede estar experimentando una incidencia o una alta demanda temporal.

            • El modelo seleccionado puede estar temporalmente no disponible.

            • Se puede haber alcanzado temporalmente algún límite de cuota o solicitudes de la API.

            • La conexión con el servicio de Gemini puede haber fallado temporalmente.

            Espere unos minutos y vuelva a intentarlo."""

            else:

                posibles_causas = """Posibles causas:

            • Ollama no está iniciado.

            • El modelo seleccionado no está instalado.

            • El documento contiene un formato no válido.

            • Se ha producido un error interno durante la generación.

            Revise el problema e inténtelo nuevamente."""

            return f"""# ❌ Error durante el análisis

            Se ha producido un error mientras Lince procesaba el documento.

            ------------------------------------------------------------

            {mensaje}

            ------------------------------------------------------------

            {posibles_causas}
            """

            

        caracteres = len(texto)

        palabras = len(texto.split())

        ioc_stats = IOCEngine.statistics(ioc_result)

        total_ioc = ioc_stats["total"]

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        # -------------------------------------------------
        # LISTADO DE EVIDENCIAS
        # -------------------------------------------------

        lista_evidencias = ""

        for fichero in document_paths:

            ext = os.path.splitext(fichero)[1].replace(".", "").upper()

            lista_evidencias += (
                f"• {os.path.basename(fichero)} ({ext})\n"
            )

        cabecera = f"""# 🛡 Lince AI

        ## 📂 Evidencias analizadas

        {lista_evidencias}

---

## Información del análisis

**Evidencias analizadas:** {len(document_paths)}

**Documento principal:** {os.path.basename(document_paths[0])}

**Formatos detectados:** {", ".join(sorted(set(
    os.path.splitext(f)[1].replace(".", "").upper()
    for f in document_paths
)))}

**Modelo:** {model}

**Tipo de informe:** {report_type}

**Fecha:** {fecha}

**Tiempo de análisis:** {tiempo_analisis}

**Caracteres analizados:** {caracteres:,}

**Palabras analizadas:** {palabras:,}

**IOC detectados:** {total_ioc}

**IPv4:** {ioc_stats["ipv4"]}

**IPv6:** {ioc_stats["ipv6"]}

**URLs:** {ioc_stats["urls"]}

**Dominios:** {ioc_stats["domains"]}

**Emails:** {ioc_stats["emails"]}

**Hashes MD5:** {ioc_stats["md5"]}

**Hashes SHA1:** {ioc_stats["sha1"]}

**Hashes SHA256:** {ioc_stats["sha256"]}

**CVE:** {ioc_stats["cve"]}

---

"""

        ioc_markdown = IOCEngine.to_markdown(ioc_result)

        contenido_final = cabecera + ioc_markdown + "\n" + respuesta

        markdown_path = MarkdownExporter.save(
            report_type,
            document_paths[0],
            contenido_final
        )

        IOCJsonExporter.save(
            markdown_path,
            ioc_result
        )

        AnalysisLogger.write(
            document_paths[0],
            model,
            report_type,
            "OK"
        )

        return {
            "report": contenido_final,
            "ioc": ioc_result,
            "markdown": markdown_path,
            "stats": ioc_stats,
            "analysis_date": datetime.now()
        }