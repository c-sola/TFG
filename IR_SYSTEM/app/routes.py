from flask import Blueprint, render_template, flash, request, redirect, url_for, send_file, abort, current_app, Response, jsonify
import shutil
import os
from bson import ObjectId
from collections import defaultdict
from controllers.pipeline_executor import PipelineExecutor
from controllers.searcher import Searcher
from db.pipeline_config_model import PipelineConfigModel
from db.method_definition_model import MethodDefinitionModel
from db.processed_collection_model import ProcessedCollectionModel
from db.document_representation_model import DocumentRepresentationModel
from db.collection_representation_model import CollectionRepresentationModel
from db.representation_type_model import RepresentationTypeModel
from db.collection_model import CollectionModel
from db.document_model import DocumentModel

main = Blueprint('main', __name__)
executor = PipelineExecutor("")

# ------------------- PÁGINA PRINCIPAL -------------------
@main.route('/')
def index():
    """
    Renderiza la página principal mostrando todas las colecciones registradas.
    """
    colecciones = executor.collection_model.get_all_collections()
    return render_template("index.html", colecciones=colecciones)

# ------------------- REGISTRO DE COLECCIONES -------------------
@main.route('/form/registrar_coleccion')
def form_registrar_coleccion():
    """
    Renderiza el formulario para registrar una nueva colección.
    """
    return render_template("form_registrar_coleccion.html")

@main.route('/registrar_coleccion', methods=['POST'])
def registrar_coleccion():
    """
    Registra una nueva colección a partir de los datos del formulario.
    """
    path = request.form['collection_path']
    language = request.form['language']
    nombre = request.form.get('collection_name', '').strip()

    executor.collection_path = path
    collection_id = executor.registrar_coleccion(language, nombre if nombre else None)

    return render_template("resultado_registro.html", collection_id=collection_id)

# ------------------- EXTRACCIÓN DE TEXTOS -------------------
@main.route('/extraer_texto', methods=['POST'])
def extraer_texto():
    """
    Ejecuta la extracción de texto para la colección indicada.
    """
    collection_id = request.form['collection_id']
    executor.extraer_textos(collection_id)  # ← Aquí lo llamas
    flash(f"Textos extraídos correctamente para la colección {collection_id}", "success")
    return redirect(url_for('main.index'))

@main.route('/saltar_extraccion', methods=['POST'])
def saltar_extraccion():
    """
    Permite omitir la extracción de texto para una colección específica.
    Cambia su estado a 'registrada'.
    """
    collection_id = request.form['collection_id']
    executor.collection_model.update_state(collection_id, "registrada")
    flash("Extracción de texto omitida. Puedes procesar directamente si ya tienes los textos.", "info")
    return redirect(url_for('main.index'))

# ------------------- CREACIÓN DE PIPELINE -------------------
@main.route('/form/crear_pipeline')
def form_crear_pipeline():
    """
    Renderiza el formulario para crear un pipeline.
    Muestra los métodos agrupados por tipo y los pipelines existentes con sus pasos detallados.
    """
    method_model = MethodDefinitionModel()
    metodos = list(method_model.collection.find({}))

    agrupados = {}
    for m in metodos:
        tipo = m["Method_Type"]
        agrupados.setdefault(tipo, []).append(m)

    pipeline_model = PipelineConfigModel()
    pipelines = list(pipeline_model.collection.find({}))

    for p in pipelines:
        pasos = pipeline_model.get_ordered_methods(p["_id"])
        pasos_detallados = []
        for paso in pasos:
            metodo = method_model.collection.find_one({"_id": ObjectId(paso["method_def_id"])})
            if metodo:
                pasos_detallados.append({
                    "Order": paso["Order"],
                    "Name": metodo["Name"],
                    "Input_Format": metodo["Input_Format"],
                    "Output_Format": metodo["Output_Format"]
                })
        p["Pasos"] = sorted(pasos_detallados, key=lambda x: x["Order"])

    return render_template(
        "form_crear_pipeline.html",
        metodos_agrupados=agrupados,
        pipelines=pipelines
    )

@main.route('/crear_pipeline', methods=['POST'])
def crear_pipeline():
    """
    Crea un nuevo pipeline usando la secuencia de métodos seleccionada.
    """
    name = request.form['name']
    desc = request.form['desc']
    method_ids = request.form.getlist('method_order')
    method_ids = [m for m in method_ids if m.strip()]

    pasos = [
        {"method_def_id": mid, "Order": i}
        for i, mid in enumerate(method_ids)
    ]

    PipelineConfigModel().insert_pipeline(name, desc, pasos)

    flash("✅ Pipeline creado correctamente", "success")
    return redirect(url_for('main.form_crear_pipeline'))


# ------------------- PROCESAMIENTO DE PIPELINE -------------------
@main.route('/form/procesar_pipeline')
def form_procesar_pipeline():
    """
    Renderiza el formulario para aplicar un pipeline a una colección.
    Muestra colecciones, pipelines y procesados previos.
    """
    colecciones = executor.collection_model.get_all_collections()
    pipeline_model = PipelineConfigModel()
    pipelines = list(pipeline_model.collection.find())

    processed_model = ProcessedCollectionModel()
    procesadas = []
    for p in processed_model.collection.find():
        col = executor.collection_model.get_collection_by_id(p["Collection_ID"])
        pipe = pipeline_model.get_pipeline_by_id(p["Pipeline_ID"])
        procesadas.append({
            "_id": p["_id"],
            "Collection_Name": col["Name"] if col else "Desconocido",
            "Pipeline_Name": pipe["Name"] if pipe else "Desconocido"
        })

    pipeline_id = request.args.get("pipeline_id")
    if not pipeline_id and pipelines:
        pipeline_id = str(pipelines[0]['_id'])

    pasos_pipeline = []
    if pipeline_id:
        pasos_pipeline = executor.pipeline_method_model.get_ordered_methods(pipeline_id)

    return render_template(
        "form_procesar_pipeline.html",
        colecciones=colecciones,
        pipelines=pipelines,
        procesadas=procesadas,
        pasos_pipeline=pasos_pipeline,
        pipeline_seleccionado=pipeline_id
    )

@main.route('/procesar_pipeline', methods=['POST'])
def procesar_pipeline():
    """
    Procesa una colección usando el pipeline seleccionado y 
    la configuración de destinos de almacenamiento.
    """
    collection_id = request.form['collection_id']
    pipeline_id = request.form['pipeline_id']

    if not pipeline_id:
        flash("No se seleccionó ningún pipeline. Revisa el formulario.", "error")
        return redirect(url_for('main.form_procesar_pipeline'))
    
    num_steps = int(request.form.get('num_steps', 0))
    destinos = {}
    for i in range(num_steps):
        step_id = request.form.get(f'step_id_{i}')
        destino = request.form.get(f'almacenamiento_{i}')
        if step_id and destino:
            destinos[step_id] = destino

    processed_id = executor.procesar_pipeline(collection_id, pipeline_id, destinos)
    flash(f"Colección procesada correctamente. ID: {processed_id}", "success")
    return redirect(url_for('main.form_procesar_pipeline'))

# ------------------- VISUALIZACIÓN DE REPRESENTACIONES -------------------
@main.route('/representaciones')
def ver_representaciones():
    """
    Muestra las representaciones generadas (documentales y globales) 
    para una colección procesada seleccionada.
    """
    processed_model = ProcessedCollectionModel()
    processed_collections = list(processed_model.collection.find())
    selected_id = request.args.get("id")

    doc_reps = []
    col_rep = None
    rep_type_model = RepresentationTypeModel()

    if selected_id:
        try:
            selected_oid = ObjectId(selected_id)
        except Exception as e:
            print(f"ID inválida: {selected_id} → {e}")
            selected_oid = None

        if selected_oid:
            doc_model = DocumentRepresentationModel()
            col_model = CollectionRepresentationModel()
            doc_reps_db = doc_model.get_by_processed_collection(selected_oid)
            col_reps_db = col_model.get_by_processed_collection(selected_oid)
            col_rep = col_reps_db[0] if col_reps_db else None

            rep_types = rep_type_model.list_all()
            rep_types_for_collection = [
                rep for rep in rep_types if selected_id in rep.get("Output_Destination", "")
            ]

            mongo_doc_rep_keys = {(str(rep["Document_ID"]), rep["Representation_Type"]) for rep in doc_reps_db}
            for rep_type in rep_types_for_collection:
                tipo = rep_type.get("Name")
                destino = rep_type.get("Output_Destination", "")
                is_global = "global" in destino

                if is_global:
                    if not col_rep:
                        col_rep = {
                            "Representation_Type": tipo,
                            "Representation_Type_Info": rep_type,
                            "Content": None
                        }
                else:
                    doc_id_str = destino.split("_")[-1].replace(".json", "")
                    key = (doc_id_str, tipo)
                    if key not in mongo_doc_rep_keys:
                        doc_reps.append({
                            "Document_ID": doc_id_str,
                            "Representation_Type": tipo,
                            "Representation_Type_Info": rep_type,
                            "Content": None
                        })

    doc_reps_grouped = defaultdict(list)
    for rep in doc_reps:
        doc_reps_grouped[rep["Document_ID"]].append(rep)

    return render_template(
        "ver_representaciones.html",
        processed_collections=processed_collections,
        selected_id=selected_id,
        doc_reps_grouped=doc_reps_grouped,
        col_rep=col_rep
    )

# ------------------- BÚSQUEDA -------------------
@main.route("/buscar", methods=["GET", "POST"])
def buscar():
    """
    Realiza una búsqueda en una colección procesada utilizando la consulta del usuario 
    y el comparador seleccionado (por defecto, coseno).

    Renderiza la plantilla con:
    - Todas las colecciones procesadas disponibles.
    - Resultados de la búsqueda (si es POST).
    - Consulta y comparador seleccionados.
    """
    processed_model = ProcessedCollectionModel()
    colecciones = list(processed_model.collection.find())

    resultados = []
    selected_id = None
    consulta = ""
    comparador = "coseno"

    if request.method == "POST":
        selected_id = request.form.get("collection_id")
        consulta = request.form.get("consulta")
        comparador = request.form.get("comparador")

        if selected_id and consulta:
            buscador = Searcher(selected_id)
            resultados = buscador.buscar(consulta, comparador_nombre=comparador)

    return render_template(
        "buscar.html",
        colecciones=colecciones,
        resultados=resultados,
        selected_id=selected_id,
        consulta=consulta,
        comparador=comparador
    )

# ------------------- ELIMINACIÓN DE COLECCIÓN -------------------
@main.route("/eliminar_coleccion/<collection_id>", methods=["POST"])
def eliminar_coleccion(collection_id):
    """
    Elimina completamente una colección:
    - Sus representaciones (en base de datos y opcionalmente en disco).
    - Sus documentos asociados.
    - Los registros de colecciones procesadas.
    - El registro de la colección original.

    Si el formulario incluye 'eliminar_disco' = 'si', también borra los directorios del sistema de ficheros.
    """
    proc_model = ProcessedCollectionModel()
    processed = proc_model.get_by_collection_id(collection_id)
    processed_ids = [str(p["_id"]) for p in processed]

    # Eliminar representaciones del sistema de ficheros si el usuario lo indica
    if request.form.get("eliminar_disco") == "si":
        for proc_id in processed_ids:
            ruta = os.path.join("saved_structures", proc_id)
            if os.path.exists(ruta):
                shutil.rmtree(ruta)

    # Eliminar representaciones en base de datos
    doc_rep_model = DocumentRepresentationModel()
    doc_rep_model.delete_all_by_processed_ids(processed_ids)

    col_rep_model = CollectionRepresentationModel()
    col_rep_model.delete_all_by_collection_id(collection_id)

    # Eliminar documentos y la colección original
    doc_model = DocumentModel()
    documentos = doc_model.get_documents_by_collection(collection_id)
    for doc in documentos:
        doc_model.delete_document(doc["_id"])

    proc_model.delete_all_by_collection_id(collection_id)

    col_model = CollectionModel()
    col_model.delete_collection(collection_id)

    flash("Colección y todos sus datos eliminados correctamente", "success")
    return redirect(url_for('main.index'))


# ------------------- ELIMINACIÓN DE PIPELINE -------------------
@main.route("/eliminar_pipeline/<pipeline_id>", methods=["POST"])
def eliminar_pipeline(pipeline_id):
    """
    Elimina un pipeline de configuración de la base de datos.
    No afecta a colecciones ni representaciones existentes.
    """
    pipe_model = PipelineConfigModel()
    pipe_model.delete_pipeline(pipeline_id)

    flash("✅ Pipeline eliminado (las colecciones y representaciones se han conservado)", "info")
    return redirect(url_for("main.form_crear_pipeline"))

# ------------------- DESCARGA DE ARCHIVOS DESDE EL SISTEMA DE FICHEROS -------------------
@main.route('/descargar/<path:ruta>')
def descargar_archivo(ruta):
    """
    Permite descargar un archivo de representación almacenado en el sistema de ficheros 
    dentro de la carpeta 'saved_structures'.

    Parámetro:
    - ruta (str): ruta relativa dentro de 'saved_structures'.

    Retorna:
    - Archivo para descarga o error 404 si no existe.
    """
    base_dir = os.path.abspath(os.path.join(current_app.root_path, ".."))
    ruta_absoluta = os.path.join(base_dir, "saved_structures", ruta)
    
    if os.path.exists(ruta_absoluta):
        return send_file(ruta_absoluta, as_attachment=False)
    else:
        abort(404)

# ------------------- DESCARGA DE REPRESENTACIONES DESDE MONGODB -------------------
@main.route('/descargar_mongo/<tipo>/<doc_id>')
def descargar_desde_mongodb(tipo, doc_id):
    """
    Permite descargar en formato JSON la representación almacenada en MongoDB 
    (documento o global) según su ID.

    Parámetros:
    - tipo (str): 'document' o 'global' para indicar el modelo.
    - doc_id (str): ID del documento o colección procesada.

    Retorna:
    - Archivo JSON para descarga o error si no existe.
    """
    try:
        oid = ObjectId(doc_id)
    except:
        return abort(400, "ID no válido")

    if tipo == "document":
        modelo = DocumentRepresentationModel()
        rep = modelo.collection.find_one({"Document_ID": oid})
    else:
        modelo = CollectionRepresentationModel()
        rep = modelo.collection.find_one({"Processed_Collection_ID": oid})

    if rep and "Content" in rep:
        return Response(
            response=jsonify(rep["Content"]).get_data(as_text=True),
            mimetype='application/json',
            headers={
                "Content-Disposition": f"attachment;filename=representacion_{tipo}_{doc_id}.json"
            }
        )
    else:
        return abort(404, "Representación no encontrada")

# ------------------- BORRAR REPRESENTACIONES DE UNA COLECCIÓN -------------------
def eliminar_structures_de_coleccion(processed_id: str):
    """
    Elimina físicamente la carpeta 'saved_structures/<processed_id>' 
    del sistema de ficheros si existe.

    Parámetro:
    - processed_id (str): ID de la colección procesada.
    """
    carpeta = os.path.join("saved_structures", processed_id)
    if os.path.exists(carpeta):
        shutil.rmtree(carpeta)