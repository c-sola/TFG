# preprocessor/base_step.py
# Este módulo define la clase base abstracta para todos los pasos de preprocesamiento.
# Cada subclase debe implementar el método apply()

from abc import ABC, abstractmethod

class BaseStep(ABC):
    
    """
    Clase abstracta que define la interfaz común para todos los pasos de preprocesamiento.
    Cada clase que herede de BaseStep debe implementar el método 'apply', el cual realiza
    una transformación sobre los datos de entrada.

    Métodos:
        - apply(data): método abstracto que aplica una transformación sobre los datos.
    """

    @abstractmethod
    def apply(self, data):

        """
        Método abstracto que debe ser implementado por cada subclase.

        Args:
            data: Entrada sobre la que se aplicará el preprocesamiento (puede ser texto o tokens).

        Returns:
            Resultado del paso de preprocesamiento.

        Raises:
            NotImplementedError: Si no se implementa en la subclase.
        """

        pass