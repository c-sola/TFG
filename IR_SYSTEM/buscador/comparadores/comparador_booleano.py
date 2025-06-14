# buscador/comparadores/comparador_booleano.py
# Implementa la comparación booleana entre la representación de una consulta
# y la de un documento. Devuelve cuántos términos relevantes coinciden.

import json
from buscador.base_comparador import QueryComparator

class ComparadorBooleano(QueryComparator):
    """
    Implementa un comparador booleano simple que mide el número de términos
    relevantes de la consulta que aparecen en el documento.
    """

    def comparar(self, query_rep: dict, doc_rep: dict | str) -> float:
        """
        Compara la consulta con el documento usando lógica booleana: cuenta cuántos
        términos de la consulta (con valor 1) están presentes también en el documento.

        Args:
            query_rep (dict): Representación booleana de la consulta (término → 0/1).
            doc_rep (dict | str): Representación booleana del documento como diccionario o JSON serializado.

        Returns:
            float: Número de términos en común entre la consulta y el documento (no normalizado).

        Raises:
            ValueError: Si `doc_rep` es una cadena pero no es un JSON válido.
            TypeError: Si `doc_rep` no es ni diccionario ni string JSON.
        """
        # Si es una cadena, intenta interpretarla como JSON
        if isinstance(doc_rep, str):
            try:
                doc_rep = json.loads(doc_rep)
            except json.JSONDecodeError:
                raise ValueError("doc_rep es un string pero no es un JSON válido")

        # Si no es un diccionario, lanza error
        elif not isinstance(doc_rep, dict):
            raise TypeError(f"doc_rep debe ser dict o JSON string, no {type(doc_rep)}")

        # Extrae los términos con valor 1 en la consulta
        query_terms = {k for k, v in query_rep.items() if v == 1}

        # Extrae los términos con valor 1 en el documento
        doc_terms = {k for k, v in doc_rep.items() if v == 1}

        # Calcula la intersección de términos (coincidencias)
        comunes = query_terms & doc_terms

        # Devuelve el número de términos comunes
        return len(comunes)