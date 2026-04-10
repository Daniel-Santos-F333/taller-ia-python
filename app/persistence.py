import json
import os

# Ruta base para los archivos de datos
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

def read_json(filename):
    """Lee un archivo JSON y devuelve su contenido como lista/diccionario."""
    file_path = os.path.join(DATA_PATH, filename)
    try:
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error al leer {filename}: {e}")
        return []

def write_json(filename, data):
    """Escribe datos en un archivo JSON con formato legible."""
    file_path = os.path.join(DATA_PATH, filename)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al escribir en {filename}: {e}")
        return False