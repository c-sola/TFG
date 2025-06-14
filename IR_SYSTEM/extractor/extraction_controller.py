# extractor/extraction_controller.py
# Este módulo gestiona la extracción de texto desde archivos individuales o comprimidos.
# Si el archivo está comprimido (.zip, .tar, .gz), lo descomprime temporalmente y extrae
# el texto de cada archivo interno, utilizando el extractor adecuado según su tipo.

import os
import zipfile
import tarfile
from factories.extractor_factory import get_extractor_for_file

def is_compressed(file_path: str) -> bool:

    """
    Función auxiliar que determina si el archivo dado está comprimido, basándose en su extensión.

    Args:
        file_path (str): Ruta del archivo.

    Returns:
        bool: True si es un archivo comprimido (.zip, .tar, .gz), False en caso contrario.
    """

    return os.path.splitext(file_path)[1].lower() in [".zip", ".tar", ".gz"]

def extract_files_from_archive(file_path: str) -> list[str]:

    """
    Función auxiliar que descomprime un archivo comprimido y devuelve la lista de archivos extraídos.

    Args:
        file_path (str): Ruta del archivo comprimido (.zip, .tar, .gz).

    Returns:
        list[str]: Lista con las rutas completas de los archivos extraídos.
    """
      
    extracted_files = []

    os.makedirs("extracted_temp", exist_ok=True)

    nombre_base = os.path.splitext(os.path.basename(file_path))[0]
    extract_dir = os.path.join("extracted_temp", nombre_base)
    os.makedirs(extract_dir, exist_ok=True)

    ext = os.path.splitext(file_path)[1].lower()

    # Archivos .zip
    if ext == ".zip":
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            for name in zip_ref.namelist():
                full_path = os.path.join(extract_dir, name)
                if os.path.isfile(full_path):
                    extracted_files.append(full_path)

    # Archivos .tar y .gz
    elif ext in [".tar", ".gz"]:
        with tarfile.open(file_path, 'r') as tar_ref:
            tar_ref.extractall(extract_dir)
            for name in tar_ref.getnames():
                full_path = os.path.join(extract_dir, name)
                if os.path.isfile(full_path):
                    extracted_files.append(full_path)

    return extracted_files