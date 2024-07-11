import pygame
from settings import *
from pygame.locals import *
from funciones import *
from random import randint
from kraken import *


# Inicializa los módulos
pygame.init()
clock = pygame.time.Clock()

# Configuración
pygame.display.set_caption("Piratas")
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

# Cargo imágenes

background = cargar_imagen("./entorno_parcial/src/assets/mar.jpg", SCREEN_SIZE)
background_inicio = cargar_imagen("./entorno_parcial/src/assets/fondo_inicio.png", SCREEN_SIZE)
imagen_barco = cargar_imagen("./entorno_parcial/src/assets/barco.png")
imagen_kraken = cargar_imagen("./entorno_parcial/src/assets/kraken.png")
imagen_tesoro = cargar_imagen("./entorno_parcial/src/assets/tesoro.png")
imagen_disparo = cargar_imagen("./entorno_parcial/src/assets/disparo.png")
imagen_vidas3 = cargar_imagen("./entorno_parcial/src/assets/vidas3.png")
imagen_vidas2 = cargar_imagen("./entorno_parcial/src/assets/vidas2.png")
imagen_vidas1 = cargar_imagen("./entorno_parcial/src/assets/vidas1.png")
start_button = cargar_imagen("./entorno_parcial/src/assets/start.png", INITIALS_BUTTONS_SIZE)
records_button = cargar_imagen("./entorno_parcial/src/assets/records.png", INITIALS_BUTTONS_SIZE)
quit_button = cargar_imagen("./entorno_parcial/src/assets/quit.png", INITIALS_BUTTONS_SIZE)



rect_start_button = start_button.get_rect(center=START_BUTTON_POS)
rect_records_button = records_button.get_rect(center=RECORDS_BUTTON_POS)
rect_quit_button = quit_button.get_rect(center=QUIT_BUTTON_POS)



# Cargo sonidos
pygame.mixer.music.load("./entorno_parcial/src/assets/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.1)
game_over_sound = pygame.mixer.Sound("./entorno_parcial/src/assets/game_over.mp3")
tesoro_sound = pygame.mixer.Sound("./entorno_parcial/src/assets/tesoro.mp3")
disparo_sound = pygame.mixer.Sound("./entorno_parcial/src/assets/canon.mp3")



# Cargo fuente
fuente = pygame.font.SysFont(None, 32)


# Eventos personalizados
GAMETIMEOUT = USEREVENT + 1
NEWKRAKEN = USEREVENT + 2
NEWFIRES = USEREVENT + 3

max_score = 0
#tamaño del player
player_w = 50
player_h = 50


archivo_csv = cargar_csv("best_scores.csv")

best_scores = archivo_csv


continuar = True
while continuar:
    SCREEN.blit(background_inicio, ORIGIN)
    SCREEN.blit(start_button, rect_start_button)
    SCREEN.blit(records_button, rect_records_button)
    SCREEN.blit(quit_button, rect_quit_button)
    pygame.display.flip()

    wait_user_click(rect_start_button, rect_records_button, rect_quit_button, best_scores, SCREEN, fuente, tesoro_sound, disparo_sound)

    pygame.time.set_timer(GAMETIMEOUT, 120000)
    pygame.time.set_timer(NEWKRAKEN, 10000)
    pygame.time.set_timer(NEWFIRES, 5000)

    
    # Creo el player
    player = create_player(imagen_barco, 50, 50, player_w, player_h, WHITE, 0, 0, 50)
    
    # Creo el primer kraken
    krakens = [crear_kraken_random(imagen_kraken, randint(0, WIDTH - kraken_w), randint(0, HEIGHT - kraken_h), kraken_w, kraken_h, WHITE, 0, 50)]
    
    # CONFIGURACION TESOROS
    tesoros = []
    load_treasure_list(tesoros, INITIAL_QUANTITY_TREASURES, imagen_tesoro)
    #CONFIGURACION DISPAROS
    disparos = []
    
    pygame.mixer.music.play(-1)
    playing_music = True
    score = 0
    lives = 3


    # Configuro el movimiento del jugador
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    # Inicializa las variables de movimiento
    move_left = move_right = move_up = move_down = False
    #reinicio la velocidad
    SPEED_PLAYER = reiniciar_speed(SPEED_PLAYER)
    

    # Juego principal
    is_running = True
    while is_running:
        clock.tick(FPS)
        
        # Analizar eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                salir_juego()

            if event.type == KEYDOWN:
                # Mutear sonido
                if event.key == K_m:
                    if playing_music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    playing_music = not playing_music
                
                # Movimiento player
                if event.key == K_LEFT:
                    move_left = True
                if event.key == K_RIGHT:
                    move_right = True
                if event.key == K_DOWN:
                    move_down = True
                if event.key == K_UP:
                    move_up = True

                if event.key == K_p:
                    pygame.mixer.music.pause()
                    mostrar_texto(SCREEN, "PAUSA", fuente, PAUSE_POS, WHITE)
                    wait_user(K_p)
                    if playing_music:
                        pygame.mixer.music.unpause()

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_left = False
                if event.key == K_RIGHT:
                    move_right = False
                if event.key == K_DOWN:
                    move_down = False
                if event.key == K_UP:
                    move_up = False

            # Eventos personalizados
            if event.type == GAMETIMEOUT:
                is_running = False
            if event.type == NEWKRAKEN:
                nuevo_kraken = crear_kraken_random(imagen_kraken, randint(0, WIDTH - kraken_w), randint(0, HEIGHT - kraken_h), kraken_w, kraken_h, WHITE, 0, 50)
                krakens.append(nuevo_kraken) 
            if event.type == NEWFIRES:
                disparo_sound.play()
                disparo_sound.set_volume(0.5)
                load_fire_list(disparos, INITIAL_QUANTITY_FIRES, imagen_disparo)
                


        # Muevo el jugador de acuerdo a su dirección
        if move_left:
            player["rect"].left -= SPEED_PLAYER
        if move_right:
            player["rect"].right += SPEED_PLAYER
        if move_up:
            player["rect"].top -= SPEED_PLAYER
        if move_down:
            player["rect"].bottom += SPEED_PLAYER

        # Asegurar que el jugador no se mueva fuera de los límites de la pantalla
        player["rect"].left = max(0, player["rect"].left)
        player["rect"].right = min(WIDTH, player["rect"].right)
        player["rect"].top = max(0, player["rect"].top)
        player["rect"].bottom = min(HEIGHT, player["rect"].bottom)

        # Muevo y dibujo los krakens y tesoros
        for kraken in krakens:
            kraken["direccion"] = verificar_direccion_kraken(kraken)
            mover_kraken(kraken)

        for disparo in disparos:
            disparo["rect"].move_ip(SPEED_FIRE, 0)
            if colision_circulos(player["rect"], disparo["rect"]):
                disparos.remove(disparo)
                lives -= 1
                if lives <= 0:
                    is_running = False
                    
        for tesoro in tesoros.copy():
            if colision_circulos(tesoro["rect"], player["rect"]):
                tesoro_sound.play()
                tesoro_sound.set_volume(0.2)
                tesoros.remove(tesoro)
                score += 1
                SPEED_PLAYER += 0.1
                player["color"] = BLACK
                if not tesoros:
                    load_treasure_list(tesoros, INITIAL_QUANTITY_TREASURES, imagen_tesoro)

        # Configuro que el kraken se coma al barco
        for kraken in krakens:
            if colision_circulos(player["rect"], kraken["rect"]):
                is_running = False


        # Dibujar pantalla
        SCREEN.blit(background, ORIGIN)
        
        # Dibujo el barco solo si el kraken no se lo comió
        if player["img"]:
            SCREEN.blit(player["img"], player["rect"])
        
        # Dibujo los krakens
        for kraken in krakens:
            SCREEN.blit(kraken["img"], kraken["rect"])
        
        #dibujo los disparos
        for disparo in disparos:
            SCREEN.blit(disparo["img"], disparo["rect"])

        # Dibujo los tesoros
        for tesoro in tesoros:
            if tesoro["img"]:
                SCREEN.blit(tesoro["img"], tesoro["rect"])
            else:
                pygame.draw.rect(SCREEN, tesoro["color"], tesoro["rect"], tesoro["borde"], tesoro["radio"])

        #dibujo las vidas:
        if lives == 3:
            SCREEN.blit(imagen_vidas3, (10, 10))
        elif lives == 2:
            SCREEN.blit(imagen_vidas2, (10, 10))
        elif lives == 1:
            SCREEN.blit(imagen_vidas1, (10, 10))

        mostrar_texto(SCREEN, f"score: {score}", fuente, SCORE_POS, BLACK, WHITE)

        if not playing_music:
            mostrar_texto(SCREEN, "MUTE", fuente, MUTE_POS, WHITE)

        # Actualizar pantalla
        pygame.display.flip()

    # Pantalla game over


    if score > max_score:
        max_score = score

    actualizar_top_scores(score, best_scores)

    pygame.mixer.music.stop()
    game_over_sound.play()
    SCREEN.fill(BLACK)
    mostrar_texto(SCREEN, f"last score: {score}", fuente, LAST_SCORE_POS, BLACK, WHITE)
    mostrar_texto(SCREEN, f"max score: {max_score}", fuente, MAX_SCORE_POS, BLACK, WHITE)
    mostrar_texto(SCREEN, "GAME OVER", fuente, SCREEN_CENTER, WHITE)
    mostrar_texto(SCREEN, "Presione space para cerrar", fuente, MESSAGE_START_POS, WHITE)


    wait_user(K_SPACE)

    pygame.display.flip()

    guardar_best_scores(best_scores)




