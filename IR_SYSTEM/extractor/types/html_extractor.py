# extractor/types/html_extractor.py
# Clase encargada de extraer texto desde un archivo HTML.

from bs4 import BeautifulSoup
from extractor.text_extractor import TextExtractor

class HTMLTextExtractor(TextExtractor):
    """
    Clase que implementa la extracción de texto desde archivos HTML
    utilizando la biblioteca BeautifulSoup. Hereda de TextExtractor.

    Métodos:
        - extract_text(): Lee el archivo HTML y devuelve el texto plano del documento.
    """

    def extract_text(self) -> str:

        """
        Extrae y devuelve el texto contenido en un archivo HTML.

        Returns:
            str: Texto plano extraído del documento HTML.
        """

        # Abrir el archivo HTML en modo lectura con codificación UTF-8.
        with open(self.file_path, "r", encoding="utf-8") as f:
            html = f.read()
            soup = BeautifulSoup(html, "html.parser")

            # Se obtiene solo el texto.
            return soup.get_text(separator=" ", strip=True) 