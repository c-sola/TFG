from abc import ABC, abstractmethod

class BaseStructure(ABC):
    """
    Clase abstracta que define la interfaz que deben implementar todas las estructuras
    globales de representación

    Obliga a implementar los métodos necesarios para construir, cargar y exportar la estructura.
    """

    @abstractmethod
    def build(self, coleccion: dict[str, list[str]]) -> None:
        """
        Construye la estructura global a partir de una colección de documentos ya tokenizados.

        Args:
            coleccion (dict): Diccionario con IDs de documentos como claves y listas de tokens como valores.
        """
        pass

    @abstractmethod
    def load_from_dict(self, estructura: dict) -> None:
        """
        Carga la estructura desde un diccionario

        Args:
            estructura (dict): Estructura ya construida con los datos necesarios para su reconstrucción.
        """
        pass

    @abstractmethod
    def get_data(self) -> dict:
        """
        Devuelve la estructura interna en formato serializable (para guardar o inspeccionar).

        Returns:
            dict: Representación de la estructura.
        """
        pass
