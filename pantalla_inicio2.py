import pygame
import sys
import time
import numpy as np
import math
import random
from car3 import *
from player_car2 import PlayerCar
from auto_car2 import AutoCar
from track import *
from tracks import *

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
largo, alto = 800, 600
blanco = (255, 255, 255)

screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w - 100
SCREEN_HEIGHT = screen_info.current_h - 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Turbo Track")

# Clock setup
clock = pygame.time.Clock()

# Funciones para manejar eventos y pantallas

def manejar_eventos(salir=True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if salir and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            return True
    return False

# Función para renderizar texto con contorno
def renderizar_texto_con_contorno(texto, fuente, color_texto, color_contorno, pos):
    text_surf = fuente.render(texto, True, color_contorno)
    rect = text_surf.get_rect(center=pos)
    for dx in (-2, 2):
        for dy in (-2, 2):
            screen.blit(fuente.render(texto, True, color_contorno), (rect.x + dx, rect.y + dy))
    screen.blit(fuente.render(texto, True, color_texto), rect)

def pantalla_de_inicio():
    fondo = pygame.transform.scale(pygame.image.load("Imagenes y demas descargas/pantalla_inicio.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    fuente = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 20)
    colores = [(92, 225, 230), blanco]
    indice_color, tiempo_anterior = 0, pygame.time.get_ticks()

    while True:
        if manejar_eventos():
            return
        if pygame.time.get_ticks() - tiempo_anterior > 500:
            indice_color = 1 - indice_color
            tiempo_anterior = pygame.time.get_ticks()

        screen.blit(fondo, (0, 0))
        renderizar_texto_con_contorno("Press any key to continue", fuente, colores[indice_color], blanco, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100))
        pygame.display.flip()
        clock.tick(60)

def pantalla_eleccion_modo():
    fondo = pygame.image.load("imagenes y demas descargas/pantalla_eleccion.png")
    fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH , SCREEN_HEIGHT))

    fuente = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 40)

    opciones = [
        {"texto": "1. 1 player", "posicion": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)},
        {"texto": "2. 2 players", "posicion": ((SCREEN_WIDTH // 2) + 24, (SCREEN_HEIGHT // 2) + 20)},
        {"texto": "3. Instructions", "posicion": (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2 + 50) + 35)},
    ]

    COLOR_BASE = (92, 225, 230)
    COLOR_ALTERNADO = (255, 255, 255)

    tiempo_cambio = 500
    ultima_actualizacion = pygame.time.get_ticks()
    mostrar_color_base = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pantalla_eleccion_personaje(1)
                    return
                elif event.key == pygame.K_2:
                    pantalla_eleccion_personaje(2)
                    return
                elif event.key == pygame.K_3:
                    pantalla_instrucciones()
                    return

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - ultima_actualizacion >= tiempo_cambio:
            mostrar_color_base = not mostrar_color_base
            ultima_actualizacion = tiempo_actual

        color_actual = COLOR_BASE if mostrar_color_base else COLOR_ALTERNADO

        screen.blit(fondo, (0, 0))

        for opcion in opciones:
            texto_surface = fuente.render(opcion["texto"], True, color_actual)
            texto_rect = texto_surface.get_rect(center=opcion["posicion"])
            screen.blit(texto_surface, texto_rect)

        pygame.display.flip()
        clock.tick(60)

def pantalla_instrucciones():
    instrucciones_img = pygame.image.load("imagenes y demas descargas/instrucciones.png")
    instrucciones_img = pygame.transform.scale(instrucciones_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        screen.blit(instrucciones_img, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def pantalla_eleccion_personaje(num_players):
    #def pantalla_eleccion_personaje(num_players):
    #def pantalla_eleccion_personaje(num_players):
    fondo = pygame.image.load("Imagenes y demas descargas/eleccion_personajes.png")
    fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

    fuente = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 30)

    # Ajusta las posiciones para que coincidan con la ubicación debajo de cada imagen en la pantalla
    opciones = [
        {"texto": "Press W", 'pos': (160, 700), "key": pygame.K_w, 'colors': [(255, 255, 255), (92, 225, 230)], "nombre": "Franco Colapinto", "imagen": "autos/Williams_car.png"},
        {"texto": "Press M", 'pos': (520, 700), "key": pygame.K_m, 'colors': [(255, 255, 255), (255, 140, 0)], "nombre": "Lando Norris", "imagen": "autos/McLaren_car.png"},
        {"texto": "Press R", 'pos': (880, 700), "key": pygame.K_r, 'colors': [(255, 255, 255), (0, 255, 0)], "nombre": "Max Verstappen", "imagen": "autos/RedBull_car.png"},
        {"texto": "Press F", 'pos': (1260, 700), "key": pygame.K_f, 'colors': [(255, 255, 255), (255, 0, 0)], "nombre": "Charles Leclerc", "imagen": "autos/Ferrari_car.png"}
    ]

    index = 0

    while True:
        # Dibujar el fondo
        screen.blit(fondo, (0, 0))

        # Dibujar cada opción en la posición fija, alternando el color
        for data in opciones:
            color = data['colors'][index % 2]  # Alternar entre los colores definidos
            text_surface = fuente.render(data['texto'], True, color)
            text_rect = text_surface.get_rect(center=data['pos'])
            screen.blit(text_surface, text_rect)

        # Incrementar el índice para alternar colores
        index += 1

        # Actualizar la pantalla
        pygame.display.flip()

        # Retraso para controlar la velocidad de cambio de color
        pygame.time.delay(500)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for opcion in opciones:
                    if event.key == opcion["key"]:
                        if event.key == pygame.K_w:  
                            pantalla_de_carga_personaje('pantalla_personajes/colapinto.png', (173, 216, 230), (0, 0, 128), 'Williams')
                            iniciar_juego(num_players, opcion["nombre"], opcion['imagen'])
                        elif event.key == pygame.K_r: 
                            pantalla_de_carga_personaje('pantalla_personajes/red bull.png', (255, 0, 0), (0, 0, 128), 'Red Bull')
                            iniciar_juego(num_players, opcion["nombre"], opcion['imagen'])
                        elif event.key == pygame.K_f:  
                            pantalla_de_carga_personaje('pantalla_personajes/ferrari.png', (255, 20, 0), (255, 24, 7), 'Ferrari')
                            iniciar_juego(num_players, opcion["nombre"], opcion['imagen'])                       
                        elif event.key == pygame.K_m:
                            pantalla_de_carga_personaje('pantalla_personajes/mclaren.png', (254, 80, 0), (255,200,0), 'Mc Laren')
                            iniciar_juego(num_players, opcion["nombre"], opcion['imagen'])
                    iniciar_juego(num_players, opcion["nombre"], opcion["imagen"])
                return 


                       # iniciar_juego(num_players, opcion["nombre"], opcion["imagen"])
                        #return
def pantalla_de_carga_personaje(nombre_archivo, color_principal, color_secundario, nombre):
    '''pantalla de carga dependiendo la eleccion de personaje
    argumentos:
    nombre_archivo(str): nombre del archivo de la imagen
    color_principal(list): indica el color con el que va a ir alternando el titular
    color_barra(list): indica el color de la barra de carga
    nombre(str): nombre de la marca representante'''
    # Colores personalizados segun el personaje elegido
    color_principal = color_principal
    color_barra = color_secundario

    # Fuente
    font_title = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 35)
    font_small = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 30)

    # Cargar la imagen de fondo
    fondo = pygame.image.load(nombre_archivo)
    fondo = pygame.transform.scale(fondo, (largo,alto))

    titular = nombre
    color_titular = [color_principal, blanco]
    color_index = 0  # Para alternar los colores

    # Configuración de la animación de "Cargando..."
    texto_carga = ["Cargando.", "Cargando..", "Cargando..."]
    loading_text_index = 0

    # Barra de carga
    largo_barra_carga = 600
    ancho_barra_carga = 20
    start_time = time.time()

    # Bucle principal
    running = True
    while running:

        # Dibujar la imagen de fondo
        screen.blit(fondo, (0, 0))

        # Alternar colores para "Williams"
        color_index = (color_index + 1) % 2  # Alternar entre 0 y 1
        title_text = font_title.render(titular, True, color_titular[color_index])
        screen.blit(title_text, (30, 50))

        # Dibujar el texto de "Cargando..." animado
        loading_text = font_small.render(texto_carga[loading_text_index], True, blanco)
        screen.blit(loading_text, (largo // 2 - 130, alto - 100))
        loading_text_index = (loading_text_index + 1) % len(texto_carga)

        # Barra de carga
        elapsed_time = time.time() - start_time
        progress = min(1, elapsed_time / 10)  # Progreso de 0 a 1 en 10 segundos
        pygame.draw.rect(screen, color_barra, (
            largo // 2 - largo_barra_carga // 2, alto - 50,
            largo_barra_carga * progress, ancho_barra_carga))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar la pantalla
        pygame.display.flip()
        pygame.time.delay(500)  # Retraso para la animación

        # Salir cuando la barra de carga esté completa
        if progress >= 1:
            running = False

    # Finalizar Pygame
    pygame.quit()



# Función para iniciar el juego con el número de jugadores y autos seleccionados
def iniciar_juego(num_players, player1_name, player1_image):
    # Configuración de la pista y autos
    track = Track()
    finish_line_start, finish_line_end = track.finish_line
    midpoint = calculate_custom_point(finish_line_start, finish_line_end, 0.5)
    direction_vector = np.array(finish_line_end) - np.array(finish_line_start)
    direction_vector = direction_vector / np.linalg.norm(direction_vector)
    perpendicular_vector = np.array([-direction_vector[1], direction_vector[0]])
    spawn_distance = 50
    spawn_point = midpoint - perpendicular_vector * spawn_distance

    auto_car = AutoCar("AutoBot", 3)
    player_car = PlayerCar(player1_name, 1, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], spawn_point.tolist(), player1_image)

    if num_players == 2:
        player_car2 = PlayerCar("Player2", 2, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], spawn_point.tolist(), "autos/RedBull_car.png")
        player_car2.set_direction(math.atan2(direction_vector[1], direction_vector[0]) + 8)

    player_car.set_direction(math.atan2(direction_vector[1], direction_vector[0]) + 8)
    auto_car.set_start_position(spawn_point.tolist(), math.atan2(direction_vector[1], direction_vector[0]) + 8)
    auto_car.set_track(track)

    # Bucle principal del juego
    running = True
    clock = pygame.time.Clock()
    winner_declared = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not winner_declared:
            insidetrack = player_car.is_inside_track(track)
            auto_command = auto_car.get_command(keys, insidetrack)
            player_command = player_car.get_command(keys, insidetrack)

            auto_car.send_command(*auto_command, track)
            player_car.send_command(*player_command, track)

            if num_players == 2:
                insidetrack2 = player_car2.is_inside_track(track)
                player2_command = player_car2.get_command(keys, insidetrack2)
                player_car2.send_command(*player2_command, track)

        # Dibujar elementos en la pantalla
        screen.fill(blanco)
        screen.blit(pygame.image.load("imagenes_pista/grass.png"), (0, 0))
        draw_track(screen, track)
        auto_car.draw(screen)
        player_car.draw(screen)
        if num_players == 2:
            player_car2.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.mixer_music.load('stressed_out.mp3')
    pygame.mixer_music.play(-1)
    pantalla_de_inicio()
    pantalla_eleccion_modo()
    pygame.quit()

if __name__ == "__main__":
    main()
