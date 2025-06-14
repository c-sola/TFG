# factories/document_representator_factory.py
# Fábrica encargada de devolver instancias de representadores de documentos
# según el nombre del tipo de representación especificado

from document_representation.boolean_generator import BooleanRepresentationGenerator

def get_representator(name):
    """
    Devuelve una instancia del generador de representaciones de documentos
    según el nombre especificado.

    Args:
        name (str): Nombre del tipo de representación deseado. 

    Returns:
        Instancia del generador correspondiente.

    Raises:
        ValueError: Si el nombre no corresponde a un representador soportado.
    """

    if name == "boolean_vector":
        return BooleanRepresentationGenerator()
    else:
        raise ValueError(f"Representador de documentos no soportado: {name}")