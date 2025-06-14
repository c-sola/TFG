from db.conexion import MongoDBConnector
from bson import ObjectId

class MethodDefinitionModel:
    """
    Modelo para gestionar las definiciones de métodos utilizados en el pipeline 
    de procesamiento y representación de información.

    Permite insertar nuevas definiciones, consultarlas por ID o tipo, listarlas 
    y eliminarlas de la base de datos.
    """

    def __init__(self):
        """
        Inicializa la conexión con la colección 'method_definitions' de la base de datos.
        """
        self.collection = MongoDBConnector().get_collection("method_definitions")

    def insert_method(self, name: str, description: str, method_type: str, input_format: str, output_format: str) -> str:
        """
        Inserta una nueva definición de método en la colección.

        Parámetros:
        - name (str): nombre identificador del método.
        - description (str): descripción detallada de lo que hace el método.
        - method_type (str): categoría del método ('preprocessing', 'document_representation', 'global_representation').
        - input_format (str): formato de entrada requerido por el método.
        - output_format (str): formato de salida producido por el método.

        Retorna:
        - str: ID de la definición de método insertada.
        """
        method = {
            "Name": name,
            "Description": description,
            "Method_Type": method_type,
            "Input_Format": input_format,
            "Output_Format": output_format
        }
        result = self.collection.insert_one(method)
        return str(result.inserted_id)

    def get_method_by_id(self, method_id: str) -> dict | None:
        """
        Recupera una definición de método por su ID.

        Parámetro:
        - method_id (str): ID de la definición de método.

        Retorna:
        - dict | None: definición encontrada o None si no existe.
        """
        return self.collection.find_one({"_id": ObjectId(method_id)})

    def list_methods(self, method_type: str = None) -> list[dict]:
        """
        Lista todas las definiciones de métodos almacenadas, opcionalmente filtradas por tipo.

        Parámetro:
        - method_type (str, opcional): tipo de método para filtrar resultados.

        Retorna:
        - list[dict]: lista de definiciones de métodos.
        """
        if method_type:
            return list(self.collection.find({"Method_Type": method_type}))
        return list(self.collection.find())

    def delete_method(self, method_id: str):
        """
        Elimina una definición de método por su ID.

        Parámetro:
        - method_id (str): ID de la definición de método a eliminar.

        Retorna:
        - DeleteResult: resultado de la operación de borrado.
        """
        return self.collection.delete_one({"_id": ObjectId(method_id)})
