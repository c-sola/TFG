# preprocessor/steps/remove_stopwords_step.py
# Este módulo implementa un paso de preprocesamiento para eliminar las stop words
# de una lista de tokens. Utiliza nltk

from nltk.corpus import stopwords
from preprocessor.base_step import BaseStep
import nltk

nltk.download('stopwords')

class RemoveStopwordsStep(BaseStep):

    """
    Paso de preprocesamiento que elimina las palabras vacías ('stop words') de una lista de tokens.
    Utiliza las listas predefinidas por NLTK en varios idiomas.

    Atributos:
        - stops (set): conjunto de palabras vacías en el idioma especificado.

    Métodos:
        - apply(tokens): recibe una lista de palabras y devuelve una nueva lista sin las stopwords.
    """

    def __init__(self, language='spanish'):

        """
        Inicializa el paso de eliminación de stopwords en un idioma dado.

        Args:
            language (str): Idioma de las stopwords (por defecto, 'spanish').

        Raises:
            ValueError: Si el idioma no está soportado o no se puede cargar.
        """

        try:
            self.stops = set(stopwords.words(language))
        except OSError:
            raise ValueError(f"Idioma no soportado o no descargado: {language}")

    def apply(self, tokens):
        
        """
        Elimina las palabras vacías de una lista de tokens.

        Args:
            tokens (list[str]): Lista de palabras ya tokenizadas.

        Returns:
            list[str]: Lista sin palabras vacías.

        Raises:
            TypeError: Si la entrada no es una lista de strings.
        """

        if not isinstance(tokens, list) or not all(isinstance(t, str) for t in tokens):
            raise TypeError(
                f"Para quitar las stop words se esperaba una lista de strings, pero recibió {type(tokens).__name__}"
            )
        return [t for t in tokens if t not in self.stops]