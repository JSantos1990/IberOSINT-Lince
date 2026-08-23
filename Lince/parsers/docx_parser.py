from docx import Document


class DOCXParser:

    @staticmethod
    def parse(filepath):

        document = Document(filepath)

        text = ""

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                text += paragraph.text + "\n"

        return text.strip()