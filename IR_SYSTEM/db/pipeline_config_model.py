from db.conexion import MongoDBConnector
from bson import ObjectId

class PipelineConfigModel:
    """
    Modelo para gestionar la configuración de pipelines de procesamiento.
    Permite insertar, consultar, descomponer y eliminar pipelines,
    cada uno compuesto por una secuencia ordenada de métodos definidos.
    """

    def __init__(self):
        """
        Inicializa la conexión con las colecciones:
        - 'pipeline_configs': almacena las configuraciones de pipelines.
        - 'method_definitions': almacena las definiciones de métodos.
        """
        self.collection = MongoDBConnector().get_collection("pipeline_configs")
        self.methods_collection = MongoDBConnector().get_collection("method_definitions")

    def insert_pipeline(self, name: str, description: str, steps: list[dict]) -> str:
        """
        Inserta una nueva configuración de pipeline.

        Parámetros:
        - name (str): nombre del pipeline.
        - description (str): descripción del propósito del pipeline.
        - steps (list[dict]): lista de pasos, cada uno con 'method_def_id' y 'Order'.

        Ejemplo de steps:
        [
            {"method_def_id": "60f...", "Order": 0},
            {"method_def_id": "60g...", "Order": 1}
        ]

        Retorna:
        - str: ID de la configuración de pipeline insertada.
        """
        pipeline = {
            "Name": name,
            "Description": description,
            "Methods": steps
        }
        result = self.collection.insert_one(pipeline)
        return str(result.inserted_id)
    
    def get_pipeline_by_id(self, pipeline_id: str) -> dict | None:
        """
        Recupera una configuración de pipeline por su ID.

        Parámetro:
        - pipeline_id (str): ID del pipeline.

        Retorna:
        - dict | None: configuración del pipeline o None si no existe.
        """
        return self.collection.find_one({"_id": ObjectId(pipeline_id)})

    def get_ordered_methods(self, pipeline_id: str) -> list[dict]:
        """
        Recupera los métodos de un pipeline ordenados según su posición en la secuencia.

        Parámetro:
        - pipeline_id (str): ID del pipeline.

        Retorna:
        - list[dict]: lista de pasos enriquecidos con información del método y su orden.
        """
        pipeline = self.get_pipeline_by_id(pipeline_id)
        if not pipeline:
            return []

        steps = sorted(pipeline["Methods"], key=lambda m: m["Order"])
        enriched_steps = []

        for step in steps:
            method = self.methods_collection.find_one({"_id": ObjectId(step["method_def_id"])})
            if method:
                enriched_steps.append({
                    "_id": str(method["_id"]),
                    "method_def_id": str(method["_id"]),
                    "Name": method.get("Name", "Sin nombre"),
                    "Method_Type": method.get("Method_Type", "desconocido"),
                    "Order": step.get("Order", -1)
                })
        return enriched_steps

    def descomponer_pipeline(self, pipeline_id: str) -> dict:
        """
        Descompone un pipeline en sus componentes funcionales:
        extracción, preprocesamiento, representación global y representación de documentos.

        Parámetro:
        - pipeline_id (str): ID del pipeline.

        Retorna:
        - dict: estructura con claves:
            - 'extraccion': método de extracción (o None)
            - 'preprocesamiento': lista de métodos de preprocesamiento
            - 'representacion_global': método de representación global (o None)
            - 'representacion_documentos': método de representación de documentos (o None)
        """
        steps = self.get_ordered_methods(pipeline_id)
        componentes = {
            "extraccion": None,
            "preprocesamiento": [],
            "representacion_global": None,
            "representacion_documentos": None
        }

        for step in steps:
            # Corregido: usa la clave 'method_def_id' coherente
            method = self.methods_collection.find_one({"_id": ObjectId(step["method_def_id"])})
            tipo = method.get("Method_Type")
            if tipo == "extraction":
                componentes["extraccion"] = method
            elif tipo == "preprocessing":
                componentes["preprocesamiento"].append(method)
            elif tipo == "global_representation":
                componentes["representacion_global"] = method
            elif tipo == "document_representation":
                componentes["representacion_documentos"] = method

        return componentes

    def delete_pipeline(self, pipeline_id: str):
        """
        Elimina una configuración de pipeline por su ID.

        Parámetro:
        - pipeline_id (str): ID del pipeline a eliminar.

        Retorna:
        - DeleteResult: resultado de la operación de borrado.
        """
        return self.collection.delete_one({"_id": ObjectId(pipeline_id)})
