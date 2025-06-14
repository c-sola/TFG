# buscador/meta_buscador.py
# Encargado de realizar una búsqueda en una colección procesada aplicando
# los mismos pasos de preprocesamiento y representación usados en el pipeline.
# Recupera las representaciones documentales y compara contra la consulta
# usando un comparador especificado

import os
import json
from bson import ObjectId
from db.processed_collection_model import ProcessedCollectionModel
from db.pipeline_config_model import PipelineConfigModel
from db.method_definition_model import MethodDefinitionModel
from db.document_representation_model import DocumentRepresentationModel
from buscador.comparadores.comparador_coseno import ComparadorCoseno
from preprocessor.preprocessor import Preprocessor
from buscador.comparadores.comparador_booleano import ComparadorBooleano
from db.document_model import DocumentModel
from db.representation_type_model import RepresentationTypeModel
from factories.preprocessing_step_factory import build_steps_from_methods
from factories.document_representator_factory import get_representator


class Searcher:

    """
    Clase encargada de realizar una búsqueda sobre una colección procesada.
    Aplica los mismos pasos de preprocesamiento y representación que se usaron
    en el pipeline original, y compara la consulta con las representaciones documentales.
    """

    def __init__(self, processed_collection_id: str):
        """
        Inicializa el buscador con el ID de una colección procesada.

        Args:
            processed_collection_id (str): ID de la colección procesada en la BD.
        """

        self.processed_collection_id = processed_collection_id
        self.processed_model = ProcessedCollectionModel()
        self.pipeline_model = PipelineConfigModel()
        self.pipeline_method_model = MethodDefinitionModel()
        self.doc_rep_model = DocumentRepresentationModel()
        self.document_model = DocumentModel()

    def buscar(self, texto_consulta: str, comparador_nombre: str = "coseno") -> list[dict]:
        """
        Ejecuta la búsqueda sobre la colección procesada.

        Args:
            texto_consulta (str): Texto ingresado por el usuario como consulta.
            comparador_nombre (str): Nombre del comparador a usar ('coseno' o 'booleano').

        Returns:
            list[dict]: Lista de documentos con su puntuación y ruta, ordenados por relevancia.
        """
        
        # 1. Obtener pipeline asociado a la colección procesada
        processed = self.processed_model.collection.find_one({"_id": ObjectId(self.processed_collection_id)})
        pipeline_id = processed["Pipeline_ID"]
        pasos = self.pipeline_model.get_ordered_methods(pipeline_id)
        metodos = [self.pipeline_method_model.collection.find_one({"_id": ObjectId(p["method_def_id"])}) for p in pasos]

        # 2. Construir preprocesador
        pre_methods = [m for m in metodos if m["Method_Type"] == "preprocessing"]
        pre_steps = build_steps_from_methods(pre_methods)
        preprocessor = Preprocessor(pre_steps)

        # 3. Preprocesar la consulta
        tokens = preprocessor.preprocess(texto_consulta)

        # 4. Representar la consulta
        rep_method = next((m for m in metodos if m["Method_Type"] == "document_representation"), None)
        generator = get_representator(rep_method["Name"])

        # 5. Cargar estructura del representador desde BD o desde fichero
        try:
            if hasattr(generator, "cargar_desde_bd"):
                generator.cargar_desde_bd(self.processed_collection_id)
        except Exception as e:
            print(f" No se pudo cargar desde la BD: {e}")
            if hasattr(generator, "cargar_estructura"):
                rep_type_model = RepresentationTypeModel()

                #  Si la representación es boolean_vector, necesita estructura del tipo 'inverted_index'
                estructura_necesaria = "inverted_index" if rep_method["Output_Format"] == "boolean_vector" else rep_method["Output_Format"]

                rep_type_doc = rep_type_model.collection.find_one({
                    "Format": estructura_necesaria,
                    "Output_Location_Type": "filesystem",
                    "Temporary": False
                })

                if not rep_type_doc:
                    print(f" No se encontró por Format. Intentando por Name = {estructura_necesaria}")
                    rep_type_doc = rep_type_model.collection.find_one({
                        "Name": estructura_necesaria,
                        "Output_Location_Type": "filesystem",
                        "Temporary": False
                    })

                if rep_type_doc and "Output_Destination" in rep_type_doc:
                    ruta_json = rep_type_doc["Output_Destination"]
                    try:
                        generator.cargar_estructura(ruta_json)
                    except Exception as e2:
                        raise RuntimeError(f"No se pudo cargar la estructura desde archivo: {e2}")
                else:
                    raise RuntimeError(
                        f"No se encontró una ruta válida en RepresentationType para cargar la estructura.\n"
                        f"Intentado con Format/Name = {estructura_necesaria}"
                    )
            else:
                raise RuntimeError("El representador no tiene forma de cargar la estructura (ni BD ni fichero).")

        # 6. Representar la consulta
        consulta_rep = generator.representar(tokens, "consulta")

        # 7. Cargar representaciones de documentos
        nombre_rep = rep_method["Output_Format"].strip()
        doc_reps = list(self.doc_rep_model.collection.find({
            "Processed_Collection_ID": ObjectId(self.processed_collection_id),
            "Representation_Type": nombre_rep
        }))

        # 8. Si no se encontraron en MongoDB, intentamos cargar desde disco consultando RepresentationType
        if not doc_reps:
            rep_type_model = RepresentationTypeModel()
            rep_type_doc = rep_type_model.collection.find_one({
                "Format": nombre_rep,
                "Output_Location_Type": "filesystem",
                "Temporary": False
            })

            if not rep_type_doc:
                rep_type_doc = rep_type_model.collection.find_one({
                    "Name": nombre_rep,
                    "Output_Location_Type": "filesystem",
                    "Temporary": False
                })

            if rep_type_doc and "Output_Destination" in rep_type_doc:
                base_dir = os.path.dirname(rep_type_doc["Output_Destination"])
                doc_reps = []
                for doc in self.document_model.collection.find({"Collection_ID": processed["Collection_ID"]}):
                    doc_id = str(doc["_id"])
                    nombre_archivo = f"{nombre_rep}_{doc_id}.json"
                    ruta_vector = os.path.join(base_dir, nombre_archivo)

                    if os.path.exists(ruta_vector):
                        with open(ruta_vector, "r", encoding="utf-8") as f:
                            content = json.load(f)
                        doc_reps.append({
                            "Document_ID": doc["_id"],
                            "Content": content
                        })
                    else:
                        print(f" Vector no encontrado para el documento {doc_id} en {ruta_vector}")
            else:
                print(" No se encontró representación documental en disco registrada en RepresentationType.")

        # 9. Comparar con cada documento
        comparador = ComparadorCoseno() if comparador_nombre == "coseno" else ComparadorBooleano()

        resultados = []
        for doc in doc_reps:
            doc_id = doc["Document_ID"]
            doc_vector = doc["Content"]

            score = comparador.comparar(consulta_rep, doc_vector)

            doc_info = self.document_model.collection.find_one({"_id": ObjectId(doc_id)})
            doc_path = doc_info.get("Path", "Ruta no disponible")

            resultados.append({
                "doc_id": str(doc_id),
                "score": score,
                "path": doc_path
            })

        # Ordenar los resultados por puntuación de similitud
        resultados.sort(key=lambda x: x["score"], reverse=True)
        return resultados
