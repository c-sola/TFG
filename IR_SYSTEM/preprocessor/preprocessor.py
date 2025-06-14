# preprocessor/modular_preprocessor.py
# Encargado de aplicar de forma secuencial
# una lista de pasos de preprocesamiento sobre un texto de entrada.

class Preprocessor:

    """
    Clase que permite aplicar una secuencia de pasos
    definidos por el usuario sobre un texto, siguiendo un orden establecido.

    Cada paso debe implementar el método 'apply', conforme a la interfaz 'BaseStep'.

    Atributos:
        - steps (list): Lista de instancias de pasos de preprocesamiento.

    Métodos:
        - preprocess(data): Aplica todos los pasos sobre el texto dado.
    """

    def __init__(self, steps: list):

        """
        Inicializa el preprocesador con una lista de pasos.

        Args:
            steps (list): Lista de objetos que implementan el método apply().
        """

        self.steps = steps

    def preprocess(self, data: str):

        """
        Aplica secuencialmente todos los pasos de preprocesamiento al texto.

        Args:
            data (str): Texto original (cadena).

        Returns:
            Resultado tras aplicar todos los pasos, que puede ser una lista de tokens
            o un texto transformado, según la secuencia de pasos aplicada.
        """
        
        for step in self.steps:
            data = step.apply(data)
        return data
