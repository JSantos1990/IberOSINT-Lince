from pathlib import Path
from datetime import datetime


class AnalysisLogger:

    LOG_FILE = Path(__file__).parent.parent / "output" / "analysis.log"

    @classmethod
    def write(cls, document, model, report_type, status):

        cls.LOG_FILE.parent.mkdir(exist_ok=True)

        with open(cls.LOG_FILE, "a", encoding="utf-8") as log:

            log.write(
                f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
                f"{Path(document).name} | "
                f"{model} | "
                f"{report_type} | "
                f"{status}\n"
            )