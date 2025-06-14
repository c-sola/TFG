# preprocessor/steps/tokenize_step.py
# Este módulo define un paso de preprocesamiento para tokenizar texto en palabras
# utilizando la biblioteca NLTK.

from nltk.tokenize import word_tokenize
from preprocessor.base_step import BaseStep
import nltk

nltk.download('punkt')

class TokenizeStep(BaseStep):

    """
    Paso de preprocesamiento que divide un texto en tokens.
    Utiliza la función 'word_tokenize' de NLTK, que tiene en cuenta aspectos lingüísticos como
    signos y contracciones.

    Métodos:
        - apply(data): recibe una cadena de texto y devuelve una lista de tokens.
    """
     
    def apply(self, data) -> list[str]:

        """
        Aplica la tokenización al texto proporcionado.

        Args:
            data (str): Texto en forma de cadena.

        Returns:
            list[str]: Lista de tokens extraídos del texto.

        Raises:
            TypeError: Si el dato de entrada no es un string.
        """
        
        if not isinstance(data, str):
            raise TypeError(
                f"Para tokenizar se esperaba un string como entrada, pero recibió {type(data).__name__}"
            )
        return word_tokenize(data)