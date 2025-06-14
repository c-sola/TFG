# indexer/indexer.py
# Encargado de orquestar la construcción de una estructura de indexación
# a partir de una colección de documentos ya preprocesados.

from indexer.base_structure import BaseStructure
from typing import Any

class Indexer:
    """
    Clase responsable de aplicar una estructura de indexación (por ejemplo, índice invertido)
    sobre una colección de documentos tokenizados.
    """

    def __init__(self, estructura: BaseStructure, ruta_salida: str):
        """
        Inicializa el indexador con una estructura global y una ruta de salida.

        Args:
            estructura (BaseStructure): Objeto que implementa el método de indexación (build y get_data).
            ruta_salida (str): Ruta donde potencialmente se guardaría la estructura construida.
        """
        self.estructura = estructura 
        self.ruta_salida = ruta_salida 

    def indexar(self, coleccion: dict[str, list[str, Any]]) -> dict:
        """
        Construye la estructura de indexación usando los documentos proporcionados.

        Args:
            coleccion (dict): Diccionario donde la clave es el ID del documento
                              y el valor es una lista de tokens (más opcionalmente otros elementos).

        Returns:
            dict: Representación interna de la estructura generada.
        """
        self.estructura.build(coleccion) 
        data = self.estructura.get_data()  
        print("Estructura global construida correctamente")  
        return data  