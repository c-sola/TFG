# document_representation/base_generator.py
# Define la interfaz abstracta para todos los generadores de representaciones
# de documentos.

from abc import ABC, abstractmethod

class RepresentationGenerator(ABC):
    """
    Clase abstracta que define la interfaz base para los generadores de representaciones
    documentales. Cada clase que herede de esta deberá implementar cómo cargar
    una estructura y cómo representar un documento a partir de sus tokens.
    """

    @abstractmethod
    def cargar_estructura(self, ruta_estructura: str):
        """
        Carga la estructura necesaria para la representación (por ejemplo, un vocabulario)
        desde una ruta determinada (archivo o base de datos).

        Args:
            ruta_estructura (str): Ruta desde la cual se carga la estructura.
        """
        pass

    @abstractmethod
    def representar(self, tokens: list[str], doc_id: str) -> dict:
        """
        Genera la representación del documento a partir de sus tokens.

        Args:
            tokens (list[str]): Lista de términos/token del documento.
            doc_id (str): Identificador del documento que se está representando.

        Returns:
            dict: Representación generada del documento
        """
        pass

    @abstractmethod
    def cargar_desde_bd(self, processed_collection_id: str):
        """
        Carga la estructura necesaria para la representación desde una base de datos,
        utilizando el ID de la colección procesada.

        Args:
            processed_collection_id (str): Identificador de la colección procesada en la base de datos.
        """
        pass