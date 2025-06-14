#Índice invertido implementado siguiendo la implementación de https://github.com/JaishreeJanu/information-retrieval-system

from indexer.base_structure import BaseStructure

class InvertedIndexStructure(BaseStructure):
    """
    Implementación de una estructura de índice invertido que asocia términos a los documentos
    en los que aparecen, junto con la frecuencia y las posiciones dentro del texto.
    """

    def __init__(self):
        self.index = {}

    def build(self, coleccion: dict[str, list[str]]):
        """
        Construye el índice invertido a partir de una colección de documentos.

        Args:
            coleccion (dict): Diccionario con IDs de documento como claves y listas de tokens como valores.
        """
        
        if not isinstance(coleccion, dict):
            raise ValueError("La colección debe ser un diccionario.")

        for doc_id, contenido in coleccion.items():
            if not isinstance(contenido, list) or not all(isinstance(t, str) for t in contenido):
                raise TypeError(
                    f"InvertedIndexStructure espera listas de tokens por documento, "
                    f"pero '{doc_id}' tiene {type(contenido).__name__}"
                )

        self.index = {}

        for docID, terms in coleccion.items():
            self._update_inverted_index(terms, docID)

        self.vocabulario = list(self.index.keys())

    def _update_inverted_index(self, terms, docID):
        """
        Actualiza el índice invertido con los términos de un documento.

        Args:
            terms (list[str]): Lista de términos del documento.
            docID (str): Identificador del documento.
        """
    
        term_positions = {}
        for position, term in enumerate(terms):
            term_positions.setdefault(term, []).append(position)

        for term, positions in term_positions.items():
            if term in self.index:   
                doc_ids = [posting[0] for posting in self.index[term]]
                if docID in doc_ids:
                    for posting in self.index[term]:
                        if posting[0] == docID:
                            posting[1] += len(positions)          # Aumenta la frecuencia
                            posting[2].extend(positions)          # Añade las nuevas posiciones
                            break
                else:
                    # Si el documento no está, lo añadimos al listado de postings
                    self.index[term].append([docID, len(positions), positions])
            else:
                # Si el término no existe en el índice, se crea su entrada
                self.index[term] = [[docID, len(positions), positions]]

    def get_data(self) -> dict:
        """
        Devuelve la estructura del índice invertido.

        Returns:
            dict: Diccionario con el tipo de estructura, vocabulario e índice invertido.
        """
        return {
            "tipo": "inverted_index",
            "vocabulario": self.vocabulario,
            "index": self.index
        }

    def load_from_dict(self, estructura: dict) -> None:
        """
        Carga una estructura de índice invertido previamente guardada en un diccionario.

        Args:
            estructura (dict): Diccionario que contiene las claves 'index' y 'vocabulario'.
        """
        self.index = estructura.get("index", {})
        self.vocabulario = estructura.get("vocabulario", [])
