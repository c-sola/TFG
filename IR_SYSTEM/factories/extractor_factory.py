# factories/extractor_factory.py
# Fábrica encargada de devolver el extractor de texto adecuado para un archivo

import os
from extractor.types.pdf_extractor import PDFTextExtractor
from extractor.types.html_extractor import HTMLTextExtractor

def get_extractor_for_file(file_path: str):
    """
    Devuelve el extractor de texto adecuado según la extensión del archivo.

    Args:
        file_path (str): Ruta del archivo del que se quiere extraer texto.

    Returns:
        Instancia del extractor correspondiente 

    Raises:
        ValueError: Si no hay extractor disponible para la extensión del archivo.
    """

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return PDFTextExtractor()
    elif ext == ".html":
        return HTMLTextExtractor()
    else:
        raise ValueError(f"No extractor disponible para extensión {ext}")
