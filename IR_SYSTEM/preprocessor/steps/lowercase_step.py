# preprocessor/steps/lowercase_step.py
# Este módulo define un paso de preprocesamiento para convertir el texto a minúsculas.

from preprocessor.base_step import BaseStep

class LowercaseStep(BaseStep):

    """
    Paso de preprocesamiento que convierte todo el texto a minúsculas.

    Métodos:
        - apply(data): recibe un string y devuelve el mismo string en minúsculas.
    """

    def apply(self, data):

        """
        Convierte un texto a minúsculas.

        Args:
            data (str): Texto original.

        Returns:
            str: Texto en minúsculas.

        Raises:
            TypeError: Si el dato de entrada no es un string.
        """
        
        if not isinstance(data, str):
            raise TypeError(
                f"Para hacer que el texto sea en minúscula se esperaba un string como entrada, pero recibió {type(data).__name__}"
            )
        return data.lower()