import pygame
from pygame.locals import *
from random import randint
from settings import *
import sys

def create_player(imagen=None, left=0, top=0, width=50, height=50, color=(255, 255, 255), dir=3, borde=0, radio=-1):
    """
    Crea un jugador con los parámetros especificados.

    Args:
        imagen: Imagen del jugador. Por defecto es None.
        left: Posición izquierda del jugador. Por defecto es 0.
        top: Posición superior del jugador. Por defecto es 0.
        width: Ancho del jugador. Por defecto es 50.
        height: Altura del jugador. Por defecto es 50.
        color: Color del jugador en formato RGB. Por defecto es (255, 255, 255).
        dir: Dirección inicial del jugador. Por defecto es 3.
        borde: Ancho del borde del jugador. Por defecto es 0.
        radio: Radio del jugador. Por defecto es -1.

    Returns:
        dict: Diccionario con los atributos del jugador.
    """
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))

    return {"rect": pygame.Rect(left, top, width, height), "color": color, "dir": dir, "borde": borde, "radio": radio, "img": imagen}

def salir_juego():
    """
    Finaliza el juego cerrando Pygame y el sistema.
    """
    pygame.quit()
    sys.exit()

def mostrar_texto(superficie: pygame.Surface, texto: str, fuente: pygame.font.Font, posicion: tuple[int, int], color: tuple[int, int, int], color_fondo: tuple[int, int, int] = None):
    """
    Muestra un texto en la superficie especificada.

    Args:
        superficie: Superficie donde se mostrará el texto.
        texto: Texto a mostrar.
        fuente: Fuente del texto.
        posicion: Posición del texto en la superficie.
        color: Color del texto en formato RGB.
        color_fondo: Color de fondo del texto en formato RGB. Por defecto es None.
    """
    sup_texto = fuente.render(texto, True, color, color_fondo)
    rect_texto = sup_texto.get_rect(center=posicion)
    superficie.blit(sup_texto, rect_texto)
    pygame.display.flip()

def wait_user(tecla: int):
    """
    Espera hasta que el usuario presione la tecla especificada.

    Args:
        tecla: Código de la tecla que se espera que el usuario presione.
    """
    continuar = True
    while continuar:
        for event in pygame.event.get():
            if event.type == QUIT:
                salir_juego()
            if event.type == KEYDOWN:
                if event.key == tecla:
                    continuar = False

def wait_user_click(button_rect1: pygame.Rect, button_rect2: pygame.Rect, button_rect3: pygame.Rect, best_scores, pantalla, fuente, sonido_tesoro: pygame.mixer_music, sonido_disparo: pygame.mixer_music):
    """
    Espera hasta que el usuario haga clic en uno de los rectángulos especificados.

    Args:
        button_rect1: Primer rectángulo de botón.
        button_rect2: Segundo rectángulo de botón.
    """
    continuar = True
    while continuar:
        for event in pygame.event.get():
            if event.type == QUIT:
                salir_juego()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if punto_en_rectangulo(event.pos, button_rect1):
                        continuar = False
                    if punto_en_rectangulo(event.pos, button_rect2):
                      mostrar_best_scores(best_scores, pantalla, fuente, WHITE, BLACK)
                    if punto_en_rectangulo(event.pos, button_rect3):
                        salir_juego()


def crear_treasure(imagen=None):
    """
    Crea un tesoro con los parámetros predeterminados.

    Args:
        imagen: Imagen del tesoro. Por defecto es None.

    Returns: Diccionario con los atributos del tesoro.
    """
    width_treasure = 30
    height_treasure = 30
    return create_player(imagen, randint(0, WIDTH - width_treasure), randint(0, HEIGHT - height_treasure),
                         width_treasure, height_treasure, BLACK, 0, 0, height_treasure // 2)

def load_treasure_list(lista, cantidad, imagen=None):
    """
    Carga una lista con la cantidad especificada de tesoros.

    Args:
        lista: Lista donde se agregarán los tesoros.
        cantida: Cantidad de tesoros a agregar.
        imagen: Imagen de los tesoros. Por defecto es None.
    """
    for _ in range(cantidad):
        lista.append(crear_treasure(imagen))

def crear_fire(imagen=None):
    """
    Crea una bola de fuego con los parámetros predeterminados.

    Args:
        imagen: Imagen de la bola de fuego. Por defecto es None.

    Returns: Diccionario con los atributos de la bola de fuego.
    """
    width_fire = 30
    height_fire = 30
    return create_player(imagen, WIDTH, randint(0, HEIGHT - height_fire),
                         width_fire, height_fire, BLACK, 0, 0, height_fire // 2)

def load_fire_list(lista, cantidad, imagen=None):
    """
    Carga una lista con la cantidad especificada de bolas de fuego.

    Args:
        lista (list): Lista donde se agregarán las bolas de fuego.
        cantidad (int): Cantidad de bolas de fuego a agregar.
        imagen: Imagen de las bolas de fuego. Por defecto es None.
    """
    for _ in range(cantidad):
        lista.append(crear_fire(imagen))

# Funciones de colisiones
def punto_en_rectangulo(punto, rect):
    """
    Verifica si un punto está dentro de un rectángulo.

    Args:
        punto: Coordenadas del punto (x, y).
        rect: Rectángulo donde se verificará si el punto está contenido.

    Returns: True si el punto está dentro del rectángulo, False en caso contrario.
    """
    x, y = punto
    return (x >= rect.left and x <= rect.right) and (y >= rect.top and y <= rect.bottom)

def distancia_entre_puntos(pto_1: tuple[int, int], pto_2: tuple[int, int]):
    """
    Calcula la distancia entre dos puntos.

    Args:
        pto_1: Coordenadas del primer punto.
        pto_2: Coordenadas del segundo punto.

    Returns: Distancia entre los dos puntos.
    """
    ca = pto_1[0] - pto_2[0]
    co = pto_1[1] - pto_2[1]
    distancia = (ca ** 2 + co ** 2) ** 0.5
    return distancia

def colision_circulos(rect_1, rect_2):
    """
    Verifica si dos círculos colisionan.

    Args:
        rect_1: Rectángulo que define el primer círculo.
        rect_2: Rectángulo que define el segundo círculo.

    Returns: True si los círculos colisionan, False en caso contrario.
    """
    r1 = rect_1.width // 2
    r2 = rect_2.width // 2
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2

def reiniciar_speed(velocidad: int):
    """si la velocidad del player es mayor a 10 esta funcion la reiniciara

    Args:
        velocidad (int): velocidad de movimiento del jugador

    Returns:
        _type_: retorna la velocidad reiniciada
    """
    if velocidad > 10:
        velocidad = 10

    return velocidad


def actualizar_top_scores(new_score, lista):

    lista_aux = lista[:]
    lista_aux.append({'posicion': 'nuevo', 'puntaje': new_score})

    lista_aux.sort(key=lambda x: x['puntaje'], reverse=True)

    top_10 = lista_aux[:10]

    for i, item in enumerate(top_10):
        item['posicion'] = f'Top{i + 1}'

    lista[:] = top_10

def mostrar_best_scores(best_scores, screen, fuente, color_texto, color_fondo):
    mover_y = 0
    for score in best_scores:
        texto = f"{score['posicion']}: {score['puntaje']}"
        mostrar_texto(screen, texto, fuente, (200, 100 + mover_y), color_texto, color_fondo)
        mover_y += 50

def cargar_imagen(ruta, escala=None):
    try:
        imagen = pygame.image.load(ruta)
        if escala:
            imagen = pygame.transform.scale(imagen, escala)
        print(f"Imagen cargada correctamente: {ruta}")
        return imagen
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {ruta}. Error: {e}")
    except pygame.error as e:
        print(f"Ocurrió un error al cargar la imagen {ruta}: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al cargar la imagen {ruta}: {e}")


def guardar_best_scores(best_scores):
    with open(get_path_actual("best_scores.csv"), "w", encoding="utf-8") as archivo:
        encabezado = ",".join(list(best_scores[0].keys())) + "\n"
        archivo.write(encabezado)
        for score in best_scores:
            values = list(score.values())
            linea = ",".join(str(value) for value in values) + "\n"
            archivo.write(linea)



