from pymongo import MongoClient

class MongoDBConnector:
    """
    Clase de utilidad para gestionar la conexión con la base de datos MongoDB 
    y facilitar la obtención de colecciones.
    """

    def __init__(self, uri="mongodb://localhost:27017", db_name="tfg_ir_system"):
        """
        Inicializa el conector estableciendo la conexión con el servidor de MongoDB.

        Parámetros:
        - uri (str): URI de conexión a MongoDB. Por defecto se conecta a localhost.
        - db_name (str): Nombre de la base de datos a utilizar.
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, name):
        """
        Obtiene una colección específica de la base de datos conectada.

        Parámetro:
        - name (str): Nombre de la colección deseada.

        Retorna:
        - Collection: objeto de colección de PyMongo para operaciones CRUD.
        """
        return self.db[name]
