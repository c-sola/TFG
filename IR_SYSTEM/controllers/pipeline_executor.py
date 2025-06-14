# controllers/pipeline_executor.py
# Encargado de orquestar todo el flujo de ejecución de un pipeline sobre una colección:
# extracción de texto, preprocesamiento, representación global y representación documental.

import os
import json
from bson import ObjectId
from db.collection_model import CollectionModel
from db.document_model import DocumentModel
from db.pipeline_config_model import PipelineConfigModel
from db.method_definition_model import MethodDefinitionModel
from db.processed_collection_model import ProcessedCollectionModel
from db.document_representation_model import DocumentRepresentationModel
from db.collection_representation_model import CollectionRepresentationModel
from db.representation_type_model import RepresentationTypeModel
from factories.preprocessing_step_factory import build_steps_from_methods
from factories.representation_structure_factory import get_structure
from factories.document_representator_factory import get_representator
from extractor.extraction_controller import is_compressed, extract_files_from_archive
from factories.extractor_factory import get_extractor_for_file

class PipelineExecutor:
    """
    Clase principal encargada de ejecutar pipelines completos sobre colecciones de documentos:
    desde su registro y extracción de texto, hasta la representación final e indexación.
    """

    def __init__(self, collection_path: str):
        """
        Inicializa el ejecutor con la ruta de la colección y los modelos principales.
        
        Parámetro:
        - collection_path (str): ruta local de la colección de documentos.
        """
        self.collection_path = collection_path
        self.collection_model = CollectionModel()
        self.document_model = DocumentModel()
        self.pipeline_method_model = PipelineConfigModel()
  
    def registrar_coleccion(self, language: str, nombre_personalizado: str = None) -> str:
        """
        Registra una colección de documentos en la base de datos y registra sus documentos.
        Soporta tanto archivos comprimidos como directorios o archivos sueltos.

        Parámetros:
        - language (str): idioma principal de la colección.
        - nombre_personalizado (str, opcional): nombre definido por el usuario.

        Retorna:
        - str: ID de la colección registrada.
        """

        nombre = nombre_personalizado or os.path.basename(self.collection_path)
        collection_id = self.collection_model.insert_collection(nombre, language, self.collection_path)

        if is_compressed(self.collection_path):
            archivos = extract_files_from_archive(self.collection_path)
        elif os.path.isdir(self.collection_path):
            archivos = [os.path.join(self.collection_path, f) for f in os.listdir(self.collection_path)]
        else:
            archivos = [self.collection_path]

        for path in archivos:
            try:
                extractor = get_extractor_for_file(path)
                textos = extractor.extract(path)
                
                for i, doc in enumerate(textos):
                    nombre_doc = doc.get("nombre") or f"{os.path.splitext(os.path.basename(path))[0]}_doc{i}"
                    self.document_model.insert_document(collection_id, nombre_doc, path)

            except Exception as e:
                print(f"No se pudo registrar {path}: {e}")

        return collection_id

    def extraer_textos(self, collection_id: str) -> None:
        """
        Extrae los textos de todos los documentos registrados en una colección
        y los guarda como archivos .txt en una carpeta específica.

        Parámetro:
        - collection_id (str): ID de la colección.
        """

        carpeta_destino = os.path.join("extracted_texts", str(collection_id))
        os.makedirs(carpeta_destino, exist_ok=True)
        documentos = self.document_model.get_documents_by_collection(collection_id)

        for doc in documentos:
            doc_id = str(doc["_id"])
            nombre = doc["Name"]
            ruta = doc["Path"]

            try:
                extractor = get_extractor_for_file(ruta)
                resultados = extractor.extract(ruta)

                for res in resultados:
                    texto = res.get("texto", "")
                    ruta_txt = os.path.join(carpeta_destino, f"{doc_id}.txt")

                    with open(ruta_txt, "w", encoding="utf-8") as f:
                        f.write(texto)

            except Exception as e:
                print(f"Error al extraer texto de {ruta}: {e}")

        self.collection_model.update_state(collection_id, "extraída")

    def crear_pipeline(self, name: str, desc: str, indices: str) -> str:
        """
        Crea y registra un nuevo pipeline con el nombre, descripción y orden de pasos.

        Parámetros:
        - name (str): nombre del pipeline.
        - desc (str): descripción del pipeline.
        - indices (str): cadena separada por comas que define el orden de los pasos.

        Retorna:
        - str: ID del pipeline creado.
        """

        orden = [int(i.strip()) for i in indices.split(",")]
        
        method_model = MethodDefinitionModel()
        pipeline_model = PipelineConfigModel()

        metodos = list(method_model.collection.find({}))
        if not metodos:
            raise ValueError("No hay métodos definidos en la base de datos.")

        metodo_opciones = []
        for m in metodos:
            metodo_opciones.append(m)

        pasos = [
            {"method_def_id": str(metodo_opciones[i]["_id"]), "Order": idx}
            for idx, i in enumerate(orden)
        ]

        pipeline_id = pipeline_model.insert_pipeline(name, desc, pasos)
        return pipeline_id

    
    def procesar_pipeline(self, collection_id: str, pipeline_id: str, destinos: dict = None):
        """
        Ejecuta un pipeline completo: preprocesamiento, representación global y documental.
        """

        global_rep_path = None
        global_rep_destino = None
        global_rep_step_name = None

        documentos = self.document_model.get_documents_by_collection(collection_id)

        processed_model = ProcessedCollectionModel()
        processed_collection_id = processed_model.insert_processed_collection(collection_id, pipeline_id)

        pipeline_step_model = PipelineConfigModel()
        method_model = MethodDefinitionModel()
        steps = pipeline_step_model.get_ordered_methods(pipeline_id)

        # Cargar textos desde archivos extraídos
        reps_actuales = {}
        carpeta_textos = os.path.join("extracted_texts", str(collection_id))

        for doc in documentos:
            doc_id = str(doc["_id"])
            nombre_doc = doc["Name"]
            ruta_txt = os.path.join(carpeta_textos, f"{doc_id}.txt")

            if os.path.exists(ruta_txt):
                with open(ruta_txt, "r", encoding="utf-8") as f:
                    reps_actuales[doc_id] = f.read()
            else:
                print(f"No se encontró el texto extraído para {nombre_doc}")
                reps_actuales[doc_id] = ""

        # PRIMERA PASADA: preprocessing y global_representation
        for step in steps:
            method_id = ObjectId(step["method_def_id"])
            metodo = method_model.collection.find_one({"_id": method_id})

            if not metodo:
                raise ValueError(f"No se encontró el método con ID: {method_id}")

            metodo_categoria = metodo["Method_Type"]
            metodo_nombre = metodo["Name"]
            entrada = metodo["Input_Format"]
            salida = metodo["Output_Format"]
            destino = destinos.get(step["method_def_id"], "memory") if destinos else "memory"

            if metodo_categoria == "preprocessing":
                pasos = build_steps_from_methods([metodo])
                for doc_id in reps_actuales:
                    for paso in pasos:
                        reps_actuales[doc_id] = paso.apply(reps_actuales[doc_id])

                for doc_id, datos in reps_actuales.items():
                    self.decidir_y_guardar_representacion(salida, datos, destino, processed_collection_id, doc_id, step_name=metodo_nombre)

            elif metodo_categoria == "global_representation":
                indexador = get_structure(metodo["Name"])
                indexador.indexar(reps_actuales)
                estructura = indexador.estructura.get_data()

                global_rep_path = self.decidir_y_guardar_representacion(
                    salida, estructura, destino, processed_collection_id, None, step_name=metodo_nombre
                )
                global_rep_destino = destino
                global_rep_step_name = metodo_nombre

        # SEGUNDA PASADA: document_representation (requiere que la global ya esté creada)
        for step in steps:
            method_id = ObjectId(step["method_def_id"])
            metodo = method_model.collection.find_one({"_id": method_id})

            if not metodo or metodo["Method_Type"] != "document_representation":
                continue

            metodo_nombre = metodo["Name"]
            salida = metodo["Output_Format"]
            destino = destinos.get(step["method_def_id"], "memory") if destinos else "memory"

            print(f"\nAplicando método: {metodo_nombre} (tokens → {salida})")

            generator = get_representator(metodo["Name"])
            if destino == "mongodb":
                generator.cargar_desde_bd(processed_collection_id)
            elif destino in ("filesystem", "filesystem_temp"):
                generator.cargar_estructura(global_rep_path)
            else:
                raise ValueError(f"Destino {global_rep_destino} no soportado para carga de representación global.")
            
            for doc_id, datos in reps_actuales.items():
                rep = generator.representar(datos, doc_id)
                reps_actuales[doc_id] = rep
                self.decidir_y_guardar_representacion(salida, rep, destino, processed_collection_id, doc_id, step_name=metodo_nombre)

        self.collection_model.update_state(collection_id, "procesada")
        return processed_collection_id


    def delete_pipeline(self, pipeline_id: str):
        """
        Elimina un pipeline de la base de datos por su ID.
        """

        self.collection.delete_one({"_id": ObjectId(pipeline_id)})

    def decidir_y_guardar_representacion(self, nombre_rep, datos, destino, processed_collection_id=None, doc_id=None, step_name=None):
        """
        Decide dónde almacenar una representación generada (en memoria, disco o MongoDB)
        y registra su metadata en la tabla RepresentationType.

        Parámetros:
        - nombre_rep (str): nombre de la representación.
        - datos (any): datos a guardar.
        - destino (str): destino ('memory', 'filesystem', 'mongodb').
        - processed_collection_id (str, opcional): ID de la colección procesada.
        - doc_id (str, opcional): ID del documento (para representaciones documentales).
        - step_name (str, opcional): nombre del paso/método.

        Retorna:
        - str | any: ruta, nombre o datos en memoria.
        """
        
        rep_type_model = RepresentationTypeModel()

        if destino == "memory":
            rep_type_model.insert_representation_type(
                name=nombre_rep,
                description=f"Temporal en memoria",
                format_="transient",
                location_type="RAM",
                destination="",
                temporary=True
            )
            return datos 

        elif destino == "filesystem":
            carpeta_base = "saved_structures"
            carpeta_proc = os.path.join(carpeta_base, processed_collection_id)
            carpeta_step = os.path.join(carpeta_proc, step_name or "unknown_step")

            os.makedirs(carpeta_step, exist_ok=True)
            filename = f"{nombre_rep}_{doc_id or 'global'}.json"
            path = os.path.join(carpeta_step, filename)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2)

            rep_type_model.insert_representation_type(
                name=nombre_rep,
                description=f"Guardado persistente en disco",
                format_="json",
                location_type="filesystem",
                destination=path,
                temporary=False
            )
            return path

        elif destino == "mongodb":
            if doc_id:
                DocumentRepresentationModel().insert_representation(
                    processed_collection_id, doc_id, nombre_rep, datos
                )
            else:
                CollectionRepresentationModel().insert_representation(
                    processed_collection_id, nombre_rep, datos
                )
            rep_type_model.insert_representation_type(
                name=nombre_rep,
                description=f"Guardado en MongoDB",
                format_="json",
                location_type="MongoDB",
                destination="document_representations" if doc_id else "collection_representations",
                temporary=False
            )
            return "MongoDB"
