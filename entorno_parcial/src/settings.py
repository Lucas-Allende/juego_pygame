import json
import os

def get_path_actual(nombre_archivo):
    """funcion que devuelve la ruta en la que se encuentra el archivo que vamos a abrir

    Args:
        nombre_archivo (_type_): nombre del archivo a abrir

    Returns:
        _type_: retorna la ruta completa en la que se encuentra el archivo
    """
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

def cargar_json(archivo_json):
    """
    Carga datos desde un archivo JSON.

    Args:
        archivo_json: Nombre o ruta del archivo JSON a cargar.

    Returns: Datos cargados del archivo JSON.

    """
    import json
    try:
        with open(get_path_actual(archivo_json), "r" , encoding="utf-8") as archivo:
            lista = json.load(archivo)

            return lista
    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo_json}")
        return None
    except Exception as e:
        print(f"Error inesperado al cargar el archivo JSON: {e}")
        return None


def cargar_csv(archivo_csv):
    lista = []
    try:
        with open(get_path_actual(archivo_csv), "r" , encoding="utf-8") as archivo:  
            encabezado = archivo.readline().strip("\n").split(",")

            for linea in archivo.readlines():
                scores = {}
                linea = linea.strip("\n").split(",")
                posicion, puntaje = linea
                scores["posicion"] = posicion
                scores["puntaje"] = int(puntaje)
                lista.append(scores)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo_csv}")
    except Exception as e:
        print(f"Error inesperado al cargar el archivo CSV: {e}")
    return lista

archivo = "settings.json"
settings = cargar_json(archivo)

if not isinstance(settings, dict):
    print("Error: Los datos de configuración no se cargaron correctamente.")
    settings = {}


WIDTH = settings.get("WIDTH", 800)  
HEIGHT = settings.get("HEIGHT", 600)
SCREEN_SIZE = settings.get("SCREEN_SIZE", (WIDTH, HEIGHT))
SCREEN_CENTER = settings.get("SCREEN_CENTER", (WIDTH // 2, HEIGHT // 2))
ORIGIN = settings.get("ORIGIN", (0, 0))
SCORE_POS = settings.get("SCORE_POS", (10, 10))
LAST_SCORE_POS = settings.get("LAST_SCORE_POS", (10, 50))
MAX_SCORE_POS = settings.get("MAX_SCORE_POS", (10, 90))
MUTE_POS = settings.get("MUTE_POS", (WIDTH - 50, 10))
PAUSE_POS = settings.get("PAUSE_POS", (WIDTH // 2, HEIGHT // 2))
MESSAGE_START_POS = settings.get("MESSAGE_START_POS", (WIDTH // 2, HEIGHT - 50))
FPS = settings.get("FPS", 60)
INITIALS_BUTTONS_SIZE = settings.get("INITIALS_BUTTONS_SIZE", (100, 50))
START_BUTTON_POS = settings.get("START_BUTTON_POS", (WIDTH // 2, HEIGHT // 2 - 50))
RECORDS_BUTTON_POS = settings.get("RECORDS_BUTTON_POS", (WIDTH // 2, HEIGHT // 2))
QUIT_BUTTON_POS = settings.get("QUIT_BUTTON_POS", (WIDTH // 2, HEIGHT // 2 + 50))
SPEED_PLAYER = settings.get("SPEED_PLAYER", 5)
SPEED_KRAKEN = settings.get("SPEED_KRAKEN", 2)
SPEED_FIRE = settings.get("SPEED_FIRE", 10)
INITIAL_QUANTITY_TREASURES = settings.get("INITIAL_QUANTITY_TREASURES", 5)
INITIAL_QUANTITY_FIRES = settings.get("INITIAL_QUANTITY_FIRES", 10)
BLACK = settings.get("BLACK", (0, 0, 0))
WHITE = settings.get("WHITE", (255, 255, 255))
