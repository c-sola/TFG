# factories/preprocessing_step_factory.py
# Fábrica encargada de construir los pasos de preprocesamiento a partir de
# definiciones de métodos configuradas por el usuario o cargadas desde la base de datos.

from preprocessor.steps.lowercase_step import LowercaseStep
from preprocessor.steps.remove_stopwords_step import RemoveStopwordsStep
from preprocessor.steps.tokenize_step import TokenizeStep
from preprocessor.steps.remove_punctuation_step import RemovePunctuationStep

def build_steps_from_methods(methods):
    
    """
    Construye una lista de instancias de pasos de preprocesamiento
    a partir de una lista de definiciones de métodos.

    Args:
        methods (list[dict]): Lista de métodos definidos (cada uno como un diccionario)

    Returns:
        list: Lista de instancias de pasos de preprocesamiento en el orden recibido.

    Raises:
        ValueError: Si alguno de los nombres de método no es reconocido.
    """
     
    step_instances = []
    for method in methods:
        nombre = method["Name"]
        if nombre == "lowercase":
            step_instances.append(LowercaseStep())
        elif nombre == "remove_stopwords":
            step_instances.append(RemoveStopwordsStep())
        elif nombre == "tokenize":
            step_instances.append(TokenizeStep())
        elif nombre == "remove_punctuation":
            step_instances.append(RemovePunctuationStep())
        else:
            raise ValueError(f"Método no soportado: {nombre}")
    return step_instances
