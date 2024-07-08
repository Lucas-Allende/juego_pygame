import pygame
from settings import *
from pygame.locals import *
from funciones import *
from random import choice


# Tamaño del kraken
kraken_w = 100
kraken_h = 100
# Configuración del movimiento del kraken
UR = 9
DR = 3
DL = 1
UL = 7

DIRECCIONES = (UR, DR, DL, UL)

# Verifica si el kraken choca contra los límites de la pantalla y ajusta la dirección
def verificar_direccion_kraken(kraken):
    direccion = kraken["direccion"]
    if kraken["rect"].right >= WIDTH:
        if direccion == DR:
            return DL
        elif direccion == UR:
            return UL
    elif kraken["rect"].left <= 0:
        if direccion == UL:
            return UR
        elif direccion == DL:
            return DR
    elif kraken["rect"].top <= 0:
        if direccion == UL:
            return DL
        elif direccion == UR:
            return DR
    elif kraken["rect"].bottom >= HEIGHT:
        if direccion == DL:
            return UL
        elif direccion == DR:
            return UR
        
    return direccion

# Mueve el kraken de acuerdo a su dirección
def mover_kraken(kraken):
    direccion = kraken["direccion"]
    velocidad = kraken["velocidad"]
    if direccion == DR:
        kraken["rect"].top += velocidad
        kraken["rect"].left += velocidad
    elif direccion == DL:
        kraken["rect"].top += velocidad
        kraken["rect"].left -= velocidad
    elif direccion == UL:
        kraken["rect"].top -= velocidad
        kraken["rect"].left -= velocidad
    elif direccion == UR:
        kraken["rect"].top -= velocidad
        kraken["rect"].left += velocidad

# Crea un kraken con dirección y velocidad aleatoria
def crear_kraken_random(imagen, x, y, width, height, color, borde, radio):
    nuevo_kraken = create_player(imagen, x, y, width, height, color, borde, radio)
    
    nuevo_kraken["direccion"] = choice(DIRECCIONES)
    nuevo_kraken["velocidad"] = SPEED_KRAKEN
    
    return nuevo_kraken

def crear_kraken_random(imagen, x, y, width, height, color, borde, radio, direccion=None, velocidad=None):
    nuevo_kraken = create_player(imagen, x, y, width, height, color, borde, radio)
    
    if direccion is None:
        direccion = choice(DIRECCIONES)
    nuevo_kraken["direccion"] = direccion

    if velocidad is None:
        velocidad = SPEED_KRAKEN
    nuevo_kraken["velocidad"] = velocidad
    
    return nuevo_kraken


