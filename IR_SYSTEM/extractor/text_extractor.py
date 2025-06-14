# extractor/text_extractor.py
# Clase abstracta base para todos los extractores de texto. Implementa el patrón Template Method.

from abc import ABC, abstractmethod
import os

class TextExtractor(ABC):

    """
    Clase abstracta que define el flujo general de un extractor de texto.
    Utiliza el patrón de diseño Template Method para estandarizar la secuencia de pasos.

    Métodos:
        - extract(file_path): método plantilla que define el flujo de extracción.
        - open_file(file_path): inicializa el atributo del archivo a procesar.
        - extract_text(): método abstracto que deben implementar las subclases.
        - postprocess(): hook opcional para tareas de postprocesamiento.
    """

    def extract(self, file_path: str) -> list[dict]:

        """
        Método plantilla que define el flujo estándar de extracción de texto.

        Args:
            file_path (str): Ruta del archivo a procesar.

        Returns:
            list[dict]: Lista con un único diccionario que contiene el nombre del archivo
                        y el texto extraído.
        """

        self.open_file(file_path)
        nombre = os.path.basename(self.file_path)
        texto = self.extract_text()
        self.postprocess()
        return [{"nombre": nombre, "texto": texto}]

    def open_file(self, file_path: str):

        """
        Guarda la ruta del archivo como atributo interno.
        
        Args:
            file_path (str): Ruta del archivo a abrir.
        """

        self.file_path = file_path

    def postprocess(self):

        """
        Hook opcional. Puede ser sobrescrito por subclases para realizar limpieza
        adicional del texto extraído.
        """

        pass

    @abstractmethod
    def extract_text(self) -> str:
        
        """
        Método abstracto que debe ser implementado por cada extractor específico.
        
        Returns:
            str: Texto plano extraído del documento.
        """

        pass
