import csv


class CSVParser:

    @staticmethod
    def extract_text(filepath):

        lines = []

        with open(filepath, "r", encoding="utf-8", errors="ignore", newline="") as file:

            reader = csv.reader(file)

            for row in reader:

                if row:
                    lines.append(" | ".join(str(cell) for cell in row))

        return "\n".join(lines)