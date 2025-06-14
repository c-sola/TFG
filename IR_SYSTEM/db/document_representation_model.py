from db.conexion import MongoDBConnector
from bson import ObjectId

class DocumentRepresentationModel:
    """
    Modelo para gestionar las representaciones individuales de cada documento.
    Permite insertar, consultar y eliminar representaciones almacenadas en MongoDB.
    """

    def __init__(self):
        """
        Inicializa la conexión con la colección 'document_representations' de la base de datos.
        """
        self.collection = MongoDBConnector().get_collection("document_representations")

    def insert_representation(self, processed_collection_id: str, document_id: str, representation_type: str, content) -> str:
        """
        Inserta una nueva representación para un documento dentro de una colección procesada.

        Parámetros:
        - processed_collection_id (str): ID de la colección procesada a la que pertenece.
        - document_id (str): ID del documento al que se asocia la representación.
        - representation_type (str): tipo de representación (por ejemplo, 'tokens', 'boolean_vector').
        - content (any): contenido de la representación (puede ser lista, dict, etc.).

        Retorna:
        - str: ID del documento insertado.
        """
        representation = {
            "Processed_Collection_ID": ObjectId(processed_collection_id),
            "Document_ID": ObjectId(document_id),
            "Representation_Type": representation_type,
            "Content": content
        }
        result = self.collection.insert_one(representation)
        return str(result.inserted_id)

    def get_by_document(self, document_id: str) -> list[dict]:
        """
        Recupera todas las representaciones asociadas a un documento.

        Parámetro:
        - document_id (str): ID del documento.

        Retorna:
        - list[dict]: lista de representaciones.
        """
        return list(self.collection.find({"Document_ID": ObjectId(document_id)}))

    def get_by_processed_collection(self, processed_collection_id: str) -> list[dict]:
        """
        Recupera todas las representaciones pertenecientes a una colección procesada.

        Parámetro:
        - processed_collection_id (str): ID de la colección procesada.

        Retorna:
        - list[dict]: lista de representaciones.
        """
        return list(self.collection.find({"Processed_Collection_ID": ObjectId(processed_collection_id)}))

    def get_by_type(self, processed_collection_id: str, representation_type: str) -> list[dict]:
        """
        Recupera todas las representaciones de un tipo específico dentro de una colección procesada.

        Parámetros:
        - processed_collection_id (str): ID de la colección procesada.
        - representation_type (str): tipo de representación a buscar.

        Retorna:
        - list[dict]: lista de representaciones.
        """
        return list(self.collection.find({
            "Processed_Collection_ID": ObjectId(processed_collection_id),
            "Representation_Type": representation_type
        }))

    def delete_all_by_processed_ids(self, processed_ids: list[str]):
        """
        Elimina todas las representaciones asociadas a una lista de colecciones procesadas.

        Parámetro:
        - processed_ids (list[str]): lista de IDs de colecciones procesadas.
        """
        object_ids = [ObjectId(pid) for pid in processed_ids]
        self.collection.delete_many({"Processed_Collection_ID": {"$in": object_ids}})
