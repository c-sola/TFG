# extractor/types/pdf_extractor.py
# Clase encargada de extraer texto desde archivos PDF. 

from extractor.text_extractor import TextExtractor
import pdfplumber

class PDFTextExtractor(TextExtractor):
    """
    Clase concreta que implementa la extracción de texto desde archivos PDF utilizando
    la biblioteca pdfplumber. Hereda de la clase abstracta TextExtractor.

    Métodos:
        - extract_text(): Abre el archivo PDF y concatena el texto de todas sus páginas.
    """

    def extract_text(self) -> str:

        """
        Extrae y devuelve el texto contenido en un archivo PDF, página por página.

        Returns:
            str: Texto plano concatenado extraído de todas las páginas del PDF.
        """
         
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text