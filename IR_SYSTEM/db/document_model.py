from db.conexion import MongoDBConnector
from bson import ObjectId

class DocumentModel:
    """
    Modelo para gestionar los documentos individuales que pertenecen a una colección.
    Permite insertar, consultar y eliminar documentos almacenados en MongoDB.
    """

    def __init__(self):
        """
        Inicializa la conexión con la colección 'documents' de la base de datos.
        """
        self.collection = MongoDBConnector().get_collection("documents")

    def insert_document(self, collection_id: str, name: str, path: str) -> str:
        """
        Inserta un nuevo documento asociado a una colección.

        Parámetros:
        - collection_id (str): ID de la colección a la que pertenece el documento.
        - name (str): nombre del documento.
        - path (str): ruta o ubicación del archivo físico asociado.

        Retorna:
        - str: ID del documento insertado.
        """
        doc = {
            "Collection_ID": ObjectId(collection_id),
            "Name": name,
            "Path": path
        }
        result = self.collection.insert_one(doc)
        return str(result.inserted_id)

    def get_documents_by_collection(self, collection_id: str) -> list[dict]:
        """
        Recupera todos los documentos asociados a una colección.

        Parámetro:
        - collection_id (str): ID de la colección.

        Retorna:
        - list[dict]: lista de documentos.
        """
        return list(self.collection.find({"Collection_ID": ObjectId(collection_id)}))

    def get_document_by_id(self, document_id: str) -> dict | None:
        """
        Recupera un documento por su ID.

        Parámetro:
        - document_id (str): ID del documento.

        Retorna:
        - dict | None: documento encontrado o None si no existe.
        """
        return self.collection.find_one({"_id": ObjectId(document_id)})

    def delete_document(self, document_id: str):
        """
        Elimina un documento por su ID.

        Parámetro:
        - document_id (str): ID del documento a eliminar.

        Retorna:
        - DeleteResult: resultado de la operación de borrado.
        """
        return self.collection.delete_one({"_id": ObjectId(document_id)})
    
    def document_exists(self, collection_id: str, name: str) -> bool:
        """
        Verifica si existe un documento con un nombre específico en una colección.

        Parámetros:
        - collection_id (str): ID de la colección.
        - name (str): nombre del documento a verificar.

        Retorna:
        - bool: True si existe, False en caso contrario.
        """
        return self.collection.find_one({
            "Collection_ID": ObjectId(collection_id),
            "Name": name
        }) is not None

    def get_document_by_name(self, collection_id: str, name: str) -> dict | None:
        """
        Recupera un documento por su nombre dentro de una colección.

        Parámetros:
        - collection_id (str): ID de la colección.
        - name (str): nombre del documento.

        Retorna:
        - dict | None: documento encontrado o None si no existe.
        """
        return self.collection.find_one({
            "Collection_ID": ObjectId(collection_id),
            "Name": name
        })
