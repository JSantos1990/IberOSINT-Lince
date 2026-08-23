from pathlib import Path
from datetime import datetime


class MarkdownExporter:

    OUTPUT_DIR = Path(__file__).parent.parent / "output"

    @classmethod
    def save(cls, report_type, document_path, content):

        cls.OUTPUT_DIR.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        report_name = (
            report_type
            .replace(" ", "")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
        )

        document_name = (
            Path(document_path).stem
            .replace(" ", "_")
            .replace("/", "_")
        )

        filename = f"{timestamp}_{report_name}_{document_name}.md"

        path = cls.OUTPUT_DIR / filename

        path.write_text(
            content,
            encoding="utf-8"
        )

        return path