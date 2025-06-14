from pymongo import MongoClient

def drop_all_collections(uri="mongodb://localhost:27017", db_name="tfg_ir_system"):
    """
    Elimina todas las colecciones de una base de datos MongoDB específica.

    Parámetros:
    - uri (str): URI de conexión a MongoDB (por defecto apunta al localhost)
    - db_name (str): Nombre de la base de datos sobre la que se ejecutará la operación
    """
    
    client = MongoClient(uri)
    db = client[db_name]

    colecciones = db.list_collection_names()
    for nombre in colecciones:
        db.drop_collection(nombre)
        print(f"Colección eliminada: {nombre}")

    print("Todas las colecciones han sido eliminadas.")

if __name__ == "__main__":
    drop_all_collections()
