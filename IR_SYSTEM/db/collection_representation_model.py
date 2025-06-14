from db.conexion import MongoDBConnector
from bson import ObjectId

class CollectionRepresentationModel:
    """
    Modelo para gestionar las representaciones globales de una colección procesada,
    como índices invertidos u otras estructuras que resumen el conjunto documental.
    """
    
    def __init__(self):
        """
        Inicializa la conexión con la colección 'collection_representations' de MongoDB.
        """
        self.collection = MongoDBConnector().get_collection("collection_representations")

    def insert_representation(self, processed_collection_id, representation_type, content):
        """
        Inserta una nueva representación global asociada a una colección procesada.

        Parámetros:
        - processed_collection_id (str): ID de la colección procesada.
        - representation_type (str): tipo de representación (e.g. 'inverted_index').
        - content (dict | list | any): estructura que contiene la representación en sí.

        Retorna:
        - str: ID del documento insertado.
        """

        representation = {
            "Processed_Collection_ID": ObjectId(processed_collection_id),
            "Representation_Type": representation_type,
            "Content": content  # Estructura global como dict, lista, etc.
        }
        result = self.collection.insert_one(representation)
        return str(result.inserted_id)

    def get_by_processed_collection(self, processed_collection_id):
        """
        Recupera todas las representaciones asociadas a una colección procesada.

        Parámetro:
        - processed_collection_id (str): ID de la colección procesada.

        Retorna:
        - list[dict]: lista de representaciones.
        """

        return list(self.collection.find({
            "Processed_Collection_ID": ObjectId(processed_collection_id)
        }))

    def get_by_type(self, processed_collection_id, representation_type):
        """
        Recupera una representación específica por tipo asociada a una colección procesada.

        Parámetros:
        - processed_collection_id (str): ID de la colección procesada.
        - representation_type (str): tipo de representación deseada.

        Retorna:
        - dict | None: representación encontrada o None si no existe.
        """

        return self.collection.find_one({
            "Processed_Collection_ID": ObjectId(processed_collection_id),
            "Representation_Type": representation_type
        })

    def delete_by_processed_collection(self, processed_collection_id):
        """
        Elimina todas las representaciones asociadas a una colección procesada.

        Parámetro:
        - processed_collection_id (str): ID de la colección procesada.

        Retorna:
        - DeleteResult: resultado de la operación de borrado.
        """

        return self.collection.delete_many({
            "Processed_Collection_ID": ObjectId(processed_collection_id)
        })

    def delete_all_by_collection_id(self, collection_id: str):
        """
        Elimina todas las representaciones asociadas directamente por Collection_ID.
        Este campo debe estar explícitamente almacenado si se usa.

        Parámetro:
        - collection_id (str): ID de la colección original.
        """

        self.collection.delete_many({"Collection_ID": ObjectId(collection_id)})

    def delete_all_by_processed_ids(self, processed_ids: list[str]):
        """
        Elimina todas las representaciones asociadas a una lista de colecciones procesadas.

        Parámetro:
        - processed_ids (list[str]): lista de IDs de colecciones procesadas.
        """
        
        object_ids = [ObjectId(pid) for pid in processed_ids]
        self.collection.delete_many({"Processed_Collection_ID": {"$in": object_ids}})
