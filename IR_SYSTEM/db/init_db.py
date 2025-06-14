from db.conexion import MongoDBConnector

def init_method_definitions():
    """
    Inicializa la colección 'method_definitions' en la base de datos MongoDB 
    insertando definiciones estándar de métodos.

    Estas definiciones describen las transformaciones que se pueden aplicar 
    en las diferentes etapas del pipeline de procesamiento:
    - Preprocesamiento de texto (limpieza y normalización).
    - Representación de documentos (e.g., vectores booleanos).
    - Representación global de colecciones (e.g., índice invertido).
    """

    # Obtiene la colección 'method_definitions' mediante el conector MongoDB.
    collection = MongoDBConnector().get_collection("method_definitions")

    # Lista de definiciones de métodos a insertar.
    # Cada método incluye:
    # - Name: identificador único del método.
    # - Description: descripción clara del objetivo del método.
    # - Method_Type: categoría del método ('preprocessing', 'document_representation', 'global_representation').
    # - Input_Format: formato de entrada esperado.
    # - Output_Format: formato de salida generado.
    method_definitions = [

        # Métodos de preprocesamiento de texto
        {
            "Name": "lowercase",
            "Description": "Convierte texto a minúsculas.",
            "Method_Type": "preprocessing",
            "Input_Format": "raw_text",
            "Output_Format": "raw_text"
        },
        {
            "Name": "tokenize",
            "Description": "Tokeniza texto en palabras.",
            "Method_Type": "preprocessing",
            "Input_Format": "raw_text",
            "Output_Format": "tokens"
        },
        {
            "Name": "remove_stopwords",
            "Description": "Elimina palabras vacías del texto.",
            "Method_Type": "preprocessing",
            "Input_Format": "tokens",
            "Output_Format": "tokens"
        },
        {
            "Name": "remove_punctuation",
            "Description": "Elimina signos de puntuación.",
            "Method_Type": "preprocessing",
            "Input_Format": "tokens",
            "Output_Format": "tokens"
        },

        # Métodos de representación de documentos
        {
            "Name": "boolean_vector",
            "Description": "Genera un vector binario sobre el vocabulario.",
            "Method_Type": "document_representation",
            "Input_Format": "tokens",
            "Output_Format": "boolean_vector"
        },

        # Métodos de representación global de colecciones
        {
            "Name": "build_inverted_index",
            "Description": "Construye el índice invertido de la colección.",
            "Method_Type": "global_representation",
            "Input_Format": "tokens",
            "Output_Format": "inverted_index"
        }
    ]

    # Inserta todas las definiciones en la colección.
    collection.insert_many(method_definitions)
    print("Métodos insertados correctamente en 'method_definitions'.")


if __name__ == "__main__":
    # Ejecuta la inicialización si se invoca como script principal.
    init_method_definitions()
    print("Base de datos inicializada.")
