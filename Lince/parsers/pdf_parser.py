from pypdf import PdfReader


class PDFParser:

    @staticmethod
    @staticmethod
    def parse(filepath):

        reader = PdfReader(filepath)

        print("\n==============================")
        print("      PDF PARSER")
        print("==============================")
        print(f"Archivo: {filepath}")
        print(f"Páginas: {len(reader.pages)}")

        text = ""

        for numero, page in enumerate(reader.pages, start=1):

            contenido = page.extract_text()

            if contenido:

                print(f"Página {numero}: {len(contenido)} caracteres")

                text += contenido + "\n"

            else:

                print(f"Página {numero}: SIN TEXTO")

        print("------------------------------")
        print(f"Total caracteres: {len(text)}")
        print("------------------------------")
        print("Primeros 500 caracteres:\n")

        print(text[:500])

        print("\n==============================\n")

        return text.strip()