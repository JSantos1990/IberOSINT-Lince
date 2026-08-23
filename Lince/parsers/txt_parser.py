class TXTParser:

    @staticmethod
    def read(path):

        with open(path, "r", encoding="utf-8", errors="ignore") as f:

            return f.read()