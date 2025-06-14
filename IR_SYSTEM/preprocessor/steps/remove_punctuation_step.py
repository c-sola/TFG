# preprocessor/steps/remove_punctuation_step.py
# Este módulo define un paso de preprocesamiento para eliminar signos de puntuación
# de una lista de tokens.

import string
from preprocessor.base_step import BaseStep

class RemovePunctuationStep(BaseStep):

    """
    Paso de preprocesamiento que elimina los signos de puntuación de una lista de tokens.
    Utiliza el conjunto de caracteres de puntuación definido en el módulo 'string'.

    Métodos:
        - apply(data): recibe una lista de tokens y devuelve una nueva lista sin puntuación.
    """

    def apply(self, data):

        """
        Elimina signos de puntuación de una lista de tokens.

        Args:
            data (list[str]): Lista de tokens (palabras o símbolos).

        Returns:
            list[str]: Lista de tokens sin signos de puntuación.

        Raises:
            TypeError: Si la entrada no es una lista de strings.
        """
        
        if not isinstance(data, list) or not all(isinstance(t, str) for t in data):
            raise TypeError(
                f"Para eliminar los signos de puntuación se esperaba una lista de strings, pero recibió {type(data).__name__}"
            )
        return [token for token in data if token not in string.punctuation]