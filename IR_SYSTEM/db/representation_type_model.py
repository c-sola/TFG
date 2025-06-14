from db.conexion import MongoDBConnector
from bson import ObjectId

class RepresentationTypeModel:
    """
    Modelo para gestionar los tipos de representaciones generadas durante el pipeline.
    Permite registrar metadatos sobre el formato, destino de almacenamiento 
    y la temporalidad de cada representación.
    """

    def __init__(self):
        """
        Inicializa la conexión con la colección 'representation_types' de la base de datos.
        """
        self.collection = MongoDBConnector().get_collection("representation_types")

    def insert_representation_type(self, name: str, description: str, format_: str, location_type: str, destination: str, temporary: bool) -> str:
        """
        Inserta un nuevo tipo de representación en la base de datos.

        Parámetros:
        - name (str): nombre identificador de la representación.
        - description (str): descripción del tipo de representación.
        - format_ (str): formato de la representación (por ejemplo, 'boolean_vector', 'inverted_index').
        - location_type (str): tipo de ubicación de salida ('memory', 'filesystem', 'mongodb').
        - destination (str): ruta o referencia del destino donde se almacena.
        - temporary (bool): indica si es una representación temporal (True) o persistente (False).

        Retorna:
        - str: ID del tipo de representación insertado.
        """
        representation = {
            "Name": name,
            "Description": description,
            "Format": format_,
            "Output_Location_Type": location_type,
            "Output_Destination": destination,
            "Temporary": temporary
        }
        result = self.collection.insert_one(representation)
        return str(result.inserted_id)

    def get_by_id(self, representation_id: str) -> dict | None:
        """
        Recupera un tipo de representación por su ID.

        Parámetro:
        - representation_id (str): ID del tipo de representación.

        Retorna:
        - dict | None: documento encontrado o None si no existe.
        """
        return self.collection.find_one({"_id": ObjectId(representation_id)})

    def list_all(self) -> list[dict]:
        """
        Lista todos los tipos de representaciones registrados.

        Retorna:
        - list[dict]: lista de tipos de representaciones.
        """
        return list(self.collection.find())

    def list_persistent(self) -> list[dict]:
        """
        Lista todos los tipos de representaciones persistentes (Temporary=False).

        Retorna:
        - list[dict]: lista de representaciones persistentes.
        """
        return list(self.collection.find({"Temporary": False}))

    def list_temporary(self) -> list[dict]:
        """
        Lista todos los tipos de representaciones temporales (Temporary=True).

        Retorna:
        - list[dict]: lista de representaciones temporales.
        """
        return list(self.collection.find({"Temporary": True}))

    def get_by_name(self, name: str) -> dict | None:
        """
        Recupera un tipo de representación por su nombre.

        Parámetro:
        - name (str): nombre de la representación.

        Retorna:
        - dict | None: documento encontrado o None si no existe.
        """
        return self.collection.find_one({"Name": name})
