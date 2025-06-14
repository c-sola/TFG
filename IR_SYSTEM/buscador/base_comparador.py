# comparadores/base.py
# Define la interfaz abstracta para todos los comparadores de representaciones.
# Cada comparador implementa un método para calcular la similitud entre una
# consulta y un documento representados en forma vectorial (diccionarios).

from abc import ABC, abstractmethod

class QueryComparator(ABC):
    """
    Clase abstracta base para todos los comparadores de representaciones.
    Define la interfaz que debe implementar cualquier función de comparación
    entre la representación de una consulta y la de un documento.
    """

    @abstractmethod
    def comparar(self, query_rep: dict, doc_rep: dict) -> float:
        """
        Compara la representación de la consulta con la del documento.

        Args:
            query_rep (dict): Representación vectorial de la consulta.
            doc_rep (dict): Representación vectorial del documento.

        Returns:
            float: Puntuación de similitud entre la consulta y el documento.
        """
        pass