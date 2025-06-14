from db.conexion import MongoDBConnector
from datetime import datetime
from bson import ObjectId

class CollectionModel:
    """
    Modelo para gestionar las colecciones documentales dentro del sistema.
    Proporciona operaciones CRUD básicas sobre la colección 'collections' de la base de datos MongoDB.
    """

    def __init__(self):
        """
        Inicializa la conexión a la colección 'collections' en la base de datos.
        """

        self.collection = MongoDBConnector().get_collection("collections")

    def insert_collection(self, name, language, path):
        """
        Inserta una nueva colección documental en el sistema.

        Parámetros:
        - name (str): nombre de la colección.
        - language (str): idioma principal de los documentos.
        - path (str): ruta local donde están almacenados los documentos.

        Retorna:
        - str: ID de la colección insertada.
        """

        document = {
            "Name": name,
            "Creation_date": datetime.utcnow(),
            "State": "registrada",
            "Language": language,
            "Path": path
        }

        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def get_collection_by_id(self, collection_id):
        """
        Recupera una colección a partir de su ID.

        Parámetro:
        - collection_id (str): identificador de la colección.

        Retorna:
        - dict: documento correspondiente a la colección.
        """

        return self.collection.find_one({"_id": ObjectId(collection_id)})

    def update_state(self, collection_id, new_state):
        """
        Actualiza el estado de una colección.

        Parámetros:
        - collection_id (str): ID de la colección.
        - new_state (str): nuevo estado que se desea asignar.

        Retorna:
        - UpdateResult: resultado de la operación de actualización.
        """

        return self.collection.update_one(
            {"_id": ObjectId(collection_id)},
            {"$set": {"State": new_state}}
        )

    def get_all_collections(self):
        """
        Recupera todas las colecciones registradas en el sistema.

        Retorna:
        - list[dict]: lista de documentos de colecciones.
        """

        return list(self.collection.find())

    def delete_collection(self, collection_id: str):
        """
        Elimina una colección de la base de datos dado su ID.

        Parámetro:
        - collection_id (str): identificador de la colección a eliminar.
        """
        
        self.collection.delete_one({"_id": ObjectId(collection_id)})
