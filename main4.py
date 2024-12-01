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
    fondo = pygame.image.load("Imagenes y demas descargas/eleccion_personajes.png")
    fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

    fuente = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 30)

    opciones = [
        {"texto": "Press W", 'pos':(5,520), "key": pygame.K_w, 'colors': [(255, 255, 255), (92, 225, 230)], "nombre": "Franco Colapinto", "imagen": "autos/Williams_car.png"},
        {"texto": "Press M", 'pos':(205,520), "key": pygame.K_m, 'colors': [(255, 255, 255), (92, 225, 230)], "nombre": "McLaren", "imagen": "autos/McLaren_car.png"},
        {"texto": "Press R", 'pos':(405,520), "key": pygame.K_r, 'colors': [(255, 255, 255), (92, 225, 230)], "nombre": "Red Bull", "imagen": "autos/RedBull_car.png"},
        {"texto": "Press F", 'pos':(615,520),"key": pygame.K_f, 'colors': [(255, 255, 255), (92, 225, 230)], "nombre": "Ferrari", "imagen": "autos/Ferrari_car.png"}
    ]
    index=0
    while True:
        screen.blit(fondo, (0, 0))

        #for idx, opcion in enumerate(opciones):
         #   texto_surface = fuente.render(opcion["texto"], True, blanco)
          #  texto_rect = texto_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100 + idx * 50))
           # screen.blit(texto_surface, texto_rect)
        screen.blit(fondo, (0,0))
        for data in opciones:
            color = data['colors'][index % 2]
            text_surface = fuente.render(data['texto'], True, color)
            screen.blit(text_surface, data['pos'])
        index+=1
        pygame.display.flip()
        pygame.time.delay(500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for opcion in opciones:
                    if event.key == opcion["key"]:
                        iniciar_juego(num_players, opcion["nombre"], opcion["imagen"])
                        return

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
