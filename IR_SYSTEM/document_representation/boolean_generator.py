# document_representation/boolean_generator.py
# Implementa un generador de representaciones booleanas a partir de un vocabulario.
# Cada término del vocabulario se representa con 1 (presente) o 0 (ausente) en el documento.

import json
from document_representation.base_generator import RepresentationGenerator
from db.collection_representation_model import CollectionRepresentationModel

class BooleanRepresentationGenerator(RepresentationGenerator):
    """
    Generador de representaciones booleanas para documentos.
    A partir de un vocabulario (previamente cargado), construye un vector binario
    que indica la presencia o ausencia de cada término en el documento.
    """

    def cargar_estructura(self, ruta_estructura: str):
        """
        Carga el vocabulario desde un archivo JSON.

        Args:
            ruta_estructura (str): Ruta al archivo con la estructura de representación.

        Raises:
            IOError: Si ocurre un error al leer el archivo.
            ValueError: Si el JSON no contiene un campo 'vocabulario'.
        """
        try:
            with open(ruta_estructura, "r", encoding="utf-8") as f:
                estructura = json.load(f)
        except Exception as e:
            raise IOError(f"No se pudo cargar la estructura desde archivo: {e}")

        if "vocabulario" in estructura:
            self.vocabulario = set(estructura["vocabulario"])
        else:
            raise ValueError("El archivo JSON no contiene un campo 'vocabulario'.")

    def cargar_desde_bd(self, processed_collection_id: str):
        """
        Carga el vocabulario desde la base de datos MongoDB,
        utilizando el ID de la colección procesada.

        Args:
            processed_collection_id (str): ID de la colección procesada.

        Raises:
            ValueError: Si no se encuentra la estructura o no contiene vocabulario válido.
        """
        modelo = CollectionRepresentationModel()
        estructura = modelo.get_by_type(processed_collection_id, "inverted_index")

        if estructura is None:
            raise ValueError("No se encontró la representación global en la BD.")

        if "Content" in estructura and "vocabulario" in estructura["Content"]:
            self.vocabulario = set(estructura["Content"]["vocabulario"])
        else:
            raise ValueError("La representación no contiene vocabulario válido.")

    def representar(self, data, doc_id: str) -> dict[str, int]:
        """
        Genera un vector booleano para un documento: 1 si el término aparece, 0 si no.

        Args:
            data (list | dict): Lista de tokens o diccionario de términos.
            doc_id (str): Identificador del documento (no se utiliza internamente, pero se respeta la firma).

        Returns:
            dict[str, int]: Diccionario con términos del vocabulario como claves y 0/1 como valores.

        Raises:
            RuntimeError: Si no se ha cargado el vocabulario.
            TypeError: Si se proporciona texto plano o un tipo no compatible.
        """
        if not hasattr(self, "vocabulario"):
            raise RuntimeError("Debes cargar primero el vocabulario con cargar_desde_bd()")

        if isinstance(data, str):
            raise TypeError("BooleanRepresentationGenerator no acepta texto plano. Usa un tokenizer primero.")
        if isinstance(data, list):
            tokens = data
        elif isinstance(data, dict):
            tokens = list(data.keys())
        else:
            raise TypeError(f"Tipo de entrada no compatible: {type(data).__name__}")

        # Devuelve un diccionario con 1 si el término está presente, 0 en caso contrario
        return {term: int(term in tokens) for term in self.vocabulario}
