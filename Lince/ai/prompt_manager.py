from pathlib import Path


class PromptManager:

    TEMPLATE_MAP = {

    "Resumen técnico": {
        "file": "resumen_tecnico.md"
    },

    "Executive Summary": {
        "file": "executive_summary.md"
    },

    "Informe de incidente": {
        "file": "incidente.md"
    },

    "Análisis forense": {
        "file": "forense.md"
    },

    "Informe de vulnerabilidades": {
        "file": "vulnerabilidades.md"
    },

    "Informe de phishing": {
        "file": "phishing.md"
    },

    "Análisis de malware": {
        "file": "malware.md"
    },

    "Informe OSINT": {
        "file": "osint.md"
    },

    "Timeline de eventos": {
        "file": "timeline.md"
    },

    "Indicadores de compromiso (IOC)": {
        "file": "ioc.md"
    }

}

    @classmethod
    def build(
        cls,
        report_type,
        document,
        goal="",
        ioc_result=None
    ):

        filename = cls.TEMPLATE_MAP[report_type]["file"]

        path = Path(__file__).parent.parent / "templates" / filename

        system_path = Path(__file__).parent.parent / "templates" / "system.md"

        system_prompt = system_path.read_text(
            encoding="utf-8"
        )

        template = path.read_text(
            encoding="utf-8"
        )

        ioc_section = ""

        if ioc_result is not None:

            ioc_section = f"""

        ==========================
        INDICADORES DE COMPROMISO (IOC)
        ==========================

        IPv4:
        {chr(10).join(ioc_result.ipv4) or "Ninguna"}

        IPv6:
        {chr(10).join(ioc_result.ipv6) or "Ninguna"}

        URLs:
        {chr(10).join(ioc_result.urls) or "Ninguna"}

        Dominios:
        {chr(10).join(ioc_result.domains) or "Ninguno"}

        Emails:
        {chr(10).join(ioc_result.emails) or "Ninguno"}

        MD5:
        {chr(10).join(ioc_result.md5) or "Ninguno"}

        SHA1:
        {chr(10).join(ioc_result.sha1) or "Ninguno"}

        SHA256:
        {chr(10).join(ioc_result.sha256) or "Ninguno"}

        CVE:
        {chr(10).join(ioc_result.cve) or "Ninguno"}

        """

        if goal.strip():

            document = (
                "OBJETIVO DEL ANALISTA\n"
                "=====================\n\n"
                f"{goal.strip()}\n\n"
                "DOCUMENTO A ANALIZAR\n"
                "====================\n\n"
                + document
            )

        prompt = f"""
        ==========================
        LINCE AI - SYSTEM PROMPT
        ==========================

        {system_prompt}

        ==========================
        TIPO DE INFORME
        ==========================

        {template}

        ==========================
        DOCUMENTO
        ==========================

        {ioc_section}

        {document}
        """

        return prompt.replace(
            "{{DOCUMENT}}",
            document
        )