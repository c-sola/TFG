from db.conexion import MongoDBConnector
from bson import ObjectId
from datetime import datetime

class ProcessedCollectionModel:
    """
    Modelo para gestionar las colecciones procesadas.
    Permite registrar qué colección de documentos ha sido procesada, 
    con qué pipeline y en qué fecha, así como consultar y eliminar registros.
    """

    def __init__(self):
        """
        Inicializa la conexión con la colección 'processed_collections' de la base de datos.
        """
        self.collection = MongoDBConnector().get_collection("processed_collections")

    def insert_processed_collection(self, collection_id: str, pipeline_id: str) -> str:
        """
        Inserta un registro de colección procesada.

        Parámetros:
        - collection_id (str): ID de la colección de documentos original.
        - pipeline_id (str): ID del pipeline que se utilizó para procesar la colección.

        Retorna:
        - str: ID del registro de colección procesada insertado.
        """
        document = {
            "Collection_ID": ObjectId(collection_id),
            "Pipeline_ID": ObjectId(pipeline_id),
            "Process_Date": datetime.utcnow()
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def get_by_id(self, processed_id: str) -> dict | None:
        """
        Recupera un registro de colección procesada por su ID.

        Parámetro:
        - processed_id (str): ID de la colección procesada.

        Retorna:
        - dict | None: documento encontrado o None si no existe.
        """
        return self.collection.find_one({"_id": ObjectId(processed_id)})

    def get_by_collection(self, collection_id: str) -> list[dict]:
        """
        Recupera todas las instancias procesadas de una misma colección de documentos.

        Parámetro:
        - collection_id (str): ID de la colección original.

        Retorna:
        - list[dict]: lista de registros de colecciones procesadas.
        """
        return list(self.collection.find({"Collection_ID": ObjectId(collection_id)}))

    def get_by_pipeline(self, pipeline_id: str) -> list[dict]:
        """
        Recupera todas las colecciones procesadas que se han generado usando un mismo pipeline.

        Parámetro:
        - pipeline_id (str): ID del pipeline.

        Retorna:
        - list[dict]: lista de registros de colecciones procesadas.
        """
        return list(self.collection.find({"Pipeline_ID": ObjectId(pipeline_id)}))

    def get_by_collection_id(self, collection_id: str) -> list[dict]:
        """
        (Alias de get_by_collection) Recupera todas las instancias procesadas de una colección.

        Parámetro:
        - collection_id (str): ID de la colección original.

        Retorna:
        - list[dict]: lista de registros de colecciones procesadas.
        """
        return list(self.collection.find({"Collection_ID": ObjectId(collection_id)}))

    def delete_all_by_collection_id(self, collection_id: str):
        """
        Elimina todos los registros de colecciones procesadas asociados a una colección original.

        Parámetro:
        - collection_id (str): ID de la colección original.

        Retorna:
        - DeleteResult: resultado de la operación de borrado.
        """
        return self.collection.delete_many({"Collection_ID": ObjectId(collection_id)})

    def delete_all_by_pipeline_id(self, pipeline_id: str):
        """
        Elimina todos los registros de colecciones procesadas asociados a un pipeline específico.

        Parámetro:
        - pipeline_id (str): ID del pipeline.

        Retorna:
        - DeleteResult: resultado de la operación de borrado.
        """
        return self.collection.delete_many({"Pipeline_ID": ObjectId(pipeline_id)})
