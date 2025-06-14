from indexer.structures.inverted_index_structure import InvertedIndexStructure
from indexer.indexer import Indexer

def get_structure(name, path_salida="None"):
    """
    Devuelve un objeto Indexer configurado con la estructura de indexación global
    correspondiente según el nombre especificado.

    Args:
        name (str): Nombre del método de construcción de estructura global.
        path_salida (str): Ruta donde se podría guardar la estructura

    Returns:
        Indexer: Instancia del indexador con la estructura seleccionada.

    Raises:
        ValueError: Si el nombre no corresponde a una estructura soportada.
    """
    if name == "build_inverted_index":
        estructura = InvertedIndexStructure()           
        return Indexer(estructura, path_salida)         
    else:
        raise ValueError(f"Estructura global no soportada: {name}") 