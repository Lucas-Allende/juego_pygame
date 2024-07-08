import json
import os

archivo = "settings.json"

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
    with open(get_path_actual(archivo_json), "r" , encoding="utf-8") as archivo:
        lista = json.load(archivo)

        return lista

settings = cargar_json(archivo)

WIDTH = settings.get("WIDTH")
HEIGHT = settings.get("HEIGHT")
SCREEN_SIZE = settings.get("SCREEN_SIZE")
SCREEN_CENTER = settings.get("SCREEN_CENTER")
ORIGIN = settings.get("ORIGIN")
SCORE_POS = settings.get("SCORE_POS")
LAST_SCORE_POS = settings.get("LAST_SCORE_POS")
MAX_SCORE_POS = settings.get("MAX_SCORE_POS")
MUTE_POS = settings.get("MUTE_POS")
PAUSE_POS = settings.get("PAUSE_POS")
MESSAGE_START_POS = settings.get("MESSAGE_START_POS")
FPS = settings.get("FPS")
INITIALS_BUTTONS_SIZE = settings.get("INITIALS_BUTTONS_SIZE")
START_BUTTON_POS = settings.get("START_BUTTON_POS")
RECORDS_BUTTON_POS = settings.get("RECORDS_BUTTON_POS")
QUIT_BUTTON_POS = settings.get("QUIT_BUTTON_POS")
SPEED_PLAYER = settings.get("SPEED_PLAYER")
SPEED_KRAKEN = settings.get("SPEED_KRAKEN")
SPEED_FIRE = settings.get("SPEED_FIRE")
INITIAL_QUANTITY_TREASURES = settings.get("INITIAL_QUANTITY_TREASURES")
INITIAL_QUANTITY_FIRES = settings.get("INITIAL_QUANTITY_FIRES")
BLACK = settings.get("BLACK")
WHITE = settings.get("WHITE")
