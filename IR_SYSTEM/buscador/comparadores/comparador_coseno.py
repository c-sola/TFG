# buscador/comparadores/comparador_coseno.py
# Implementa la comparación basada en similitud del coseno entre
# representaciones vectoriales de documentos y consultas.

import math
from buscador.base_comparador import QueryComparator

class ComparadorCoseno(QueryComparator):
    """
    Implementa la similitud del coseno entre la representación de una consulta
    y la de un documento.
    """

    def comparar(self, query_rep: dict, doc_rep: dict) -> float:
        """
        Calcula la similitud del coseno entre la consulta y el documento.

        Args:
            query_rep (dict): Representación de la consulta como vector (diccionario término: peso).
            doc_rep (dict): Representación del documento como vector (diccionario término: peso).

        Returns:
            float: Valor entre 0 y 1 que indica la similitud entre los vectores. 
                   1 significa máxima similitud, 0 significa sin coincidencia.
        """
        # Producto punto entre los vectores (numerador de la fórmula del coseno)
        numerador = sum(query_rep.get(k, 0) * doc_rep.get(k, 0) for k in query_rep)

        # Magnitud (norma L2) de la consulta
        magnitud_q = math.sqrt(sum(v ** 2 for v in query_rep.values()))

        # Magnitud (norma L2) del documento
        magnitud_d = math.sqrt(sum(v ** 2 for v in doc_rep.values()))

        # Si alguna de las magnitudes es cero, no se puede calcular la similitud
        if magnitud_q == 0 or magnitud_d == 0:
            return 0.0

        # Devuelve la similitud del coseno
        return numerador / (magnitud_q * magnitud_d)
