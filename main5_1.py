import pygame
import sys
import time
import numpy as np
from car3 import *
from player_car2 import PlayerCar
from auto_car2 import AutoCar
from track import *
import math
from tracks import *
import random
num_players=1
# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
largo, alto = 800, 600
blanco = (255, 255, 255)
screen = pygame.display.set_mode((largo, alto))
pygame.display.set_caption("Turbo Track")

# Clock setup
clock = pygame.time.Clock()
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
    fondo = pygame.transform.scale(pygame.image.load("Imagenes y demas descargas/pantalla_inicio.png"), (largo, alto))
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
        renderizar_texto_con_contorno("Press any key to continue", fuente, colores[indice_color], blanco, (largo // 2-20, alto - 100))
        pygame.display.flip()
        clock.tick(60)

def pantalla_eleccion_modo():
    '''pantalla de eleccion del modo de juego'''
    global num_players
    # Cargar la imagen de fondo
    fondo = pygame.image.load("imagenes y demas descargas/pantalla_eleccion.png")
    fondo = pygame.transform.scale(fondo, (largo , alto))
    # Configuración de la fuente
    fuente = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 40)
    # Opciones de texto y posiciones individuales
    opciones = [
        {"texto": "1. 1 player", "posicion": (largo // 2, alto // 2 - 50)},
        {"texto": "2. 2 players", "posicion": ((largo // 2)+24, (alto // 2)+20)},
        {"texto": "3. Instructions", "posicion": (largo // 2, (alto // 2 + 50)+35)},
    ]
    # Colores iniciales
    COLOR_BASE = (92, 225, 230)
    COLOR_ALTERNADO = (255, 255, 255)
    tiempo_cambio = 500  # Tiempo en ms para alternar el color
    ultima_actualizacion = pygame.time.get_ticks()
    mostrar_color_base = True  # Alternar entre los colores

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pantalla_eleccion_personaje(1)
                    num_players=1
                    return
                elif event.key == pygame.K_2:
                    pantalla_eleccion_personaje(2)
                    num_players=2
                    return
                #elif event.key == pygame.K_3:
                    #pantalla_instrucciones()
                 #   return
        # Alternar colores de texto
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - ultima_actualizacion >= tiempo_cambio:
            mostrar_color_base = not mostrar_color_base
            ultima_actualizacion = tiempo_actual

        # Definir el color actual
        color_actual = COLOR_BASE if mostrar_color_base else COLOR_ALTERNADO

        # Dibujar el fondo
        screen.blit(fondo, (0, 0))

        # Dibujar las opciones animadas en sus posiciones individuales
        for opcion in opciones:
            texto_surface = fuente.render(opcion["texto"], True, color_actual)
            texto_rect = texto_surface.get_rect(center=opcion["posicion"])
            screen.blit(texto_surface, texto_rect)

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)

def pantalla_eleccion_personaje(num_players):
    '''pantalla de eleccion de personaje'''
    # Cargar la imagen de fondo
    background_imagez = pygame.image.load('Imagenes y demas descargas/eleccion_personajes.png')
    background_image = pygame.transform.scale(background_imagez, (largo, alto))
    # Fuente de letras
    font = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 25)
    # Ubicación del texto animado
    text_data = [
        {'text': 'Press W', 'pos': (5, 520), 'colors': [(255, 255, 255), (92, 225, 230)]},
        {'text': 'Press M', 'pos': (205, 520), 'colors': [(255, 255, 255), (92, 225, 230)]},
        {'text': 'Press R', 'pos': (405, 520), 'colors': [(255, 255, 255), (92, 225, 230)]},
        {'text': 'Press F', 'pos': (615, 520), 'colors': [(255, 255, 255), (92, 225, 230)]},
    ]
    toggle_index = 0

    players_selected = 0  # Contador de jugadores que han seleccionado personaje

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Si eligen a un personaje, sale su pantalla de carga
                if event.key == pygame.K_w:  
                    pantalla_de_carga_personaje('pantalla_personajes/colapinto.png', (173, 216, 230), (0, 0, 128), 'Williams')
                    players_selected += 1
                elif event.key == pygame.K_r: 
                    pantalla_de_carga_personaje('pantalla_personajes/red bull.png', (255, 0, 0), (0, 0, 128), 'Red Bull')
                    players_selected += 1
                elif event.key == pygame.K_f:  
                    pantalla_de_carga_personaje('pantalla_personajes/ferrari.png', (255, 20, 0), (255, 24, 7), 'Ferrari')
                    players_selected += 1
                elif event.key == pygame.K_m:
                    pantalla_de_carga_personaje('pantalla_personajes/mclaren.png', (254, 80, 0), (255, 200, 0), 'McLaren')
                    players_selected += 1
                
                # Verificar si ya se seleccionaron los personajes necesarios
                if players_selected == num_players:
                    return 

        # Dibujar la imagen de fondo
        screen.blit(background_image, (0, 0))
        # Dibujar el texto
        for data in text_data:
            color = data['colors'][toggle_index % 2]
            text_surface = font.render(data['text'], True, color)
            screen.blit(text_surface, data['pos'])
        
        # Actualizar la pantalla
        pygame.display.flip()
        # Alternar índice de colores
        toggle_index += 1
        pygame.time.delay(500)  # Retraso en la animación

# Función para mostrar la pantalla de cargar
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
def main():
    '''funcion principal del programa'''
    pygame.mixer_music.load('stressed_out.mp3')
    pygame.mixer_music.play(-1)
    pantalla_de_inicio()
    pantalla_eleccion_modo()
    pantalla_eleccion_personaje(1)
    pygame.quit()
if __name__ == "__main__":
    main()

def draw_controls_message(screen):
    """
    Dibuja un mensaje en la parte inferior izquierda de la pantalla indicando cómo reiniciar o salir del juego.
    Args:
        screen (pygame.Surface): La superficie de la pantalla donde se dibuja el mensaje.
    """
    font = pygame.font.Font(None, 36)
    message = "Para reiniciar carrera y mapa apretar R, para cerrar juego apretar Q"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(bottomleft=(10, screen.get_height() - 10))
    screen.blit(text, text_rect)
# Ejemplo de uso
# Crear una instancia de Track
def draw_lap_counter(screen, car, track):
    font = pygame.font.Font(None, 36)
    lap_message = f"Vueltas: {car.lap_count}/5"
    speed_message = f"Velocidad: {car.speed:.2f}"
    # Calcular la distancia al borde de la pista
    distance_to_border = car.calculate_distance_to_border(track)
    if distance_to_border < 0:
        border_message = f"¡Te saliste de la pista! Distancia al borde: {-distance_to_border:.2f} unidades"
    else:
        border_message = f"Distancia al borde: {distance_to_border:.2f} unidades"
    # Crear los textos
    name_text = font.render(car.driver_name, True, (255, 255, 0))  # Nombre del jugador (color amarillo)
    lap_text = font.render(lap_message, True, (255, 255, 255))
    speed_text = font.render(speed_message, True, (255, 255, 255))
    border_text = font.render(border_message, True, (255, 255, 255))
    # Verificar si es PlayerCar 2 y ajustar la posición
    if isinstance(car, PlayerCar) and car.driver_name == "Player2":
        # Imprimir arriba a la derecha
        screen_width = screen.get_width()
        screen.blit(name_text, (screen_width - name_text.get_width() - 10, 10))  # Nombre del jugador
        screen.blit(lap_text, (screen_width - lap_text.get_width() - 10, 50))
        screen.blit(speed_text, (screen_width - speed_text.get_width() - 10, 90))
        screen.blit(border_text, (screen_width - border_text.get_width() - 10, 130))
    else:
        # Imprimir arriba a la izquierda
        screen.blit(name_text, (10, 10))  # Nombre del jugador
        screen.blit(lap_text, (10, 50))
        screen.blit(speed_text, (10, 90))
        screen.blit(border_text, (10, 130))
pygame.init()
# Obtener tamaño de pantalla del usuario
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w - 100
SCREEN_HEIGHT = screen_info.current_h - 100

background_images = ["imagenes_pista/grass.png"]
selected_image = random.choice(background_images)
background_image = pygame.image.load(selected_image)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Configurar la pantalla en modo ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulación de Pista")
# Crear la pista
track = Track()
# Obtener los puntos de la línea de meta
finish_line_start, finish_line_end = track.finish_line
# Calcular el punto medio de la línea de meta usando la función calculate_custom_point
midpoint = calculate_custom_point(finish_line_start, finish_line_end, 0.5)
# Calcular un vector perpendicular hacia la izquierda de la línea de meta
direction_vector = np.array(finish_line_end) - np.array(finish_line_start)
direction_vector = direction_vector / np.linalg.norm(direction_vector)  # Normalizar el vector
# Calcular el vector perpendicular hacia la izquierda
perpendicular_vector = np.array([-direction_vector[1], direction_vector[0]])
# Definir la distancia para colocar el coche a la izquierda del punto medio
spawn_distance = 50  # Por ejemplo, 50 píxeles a la izquierda del punto medio
spawn_point = midpoint - perpendicular_vector * spawn_distance
auto_car = AutoCar("AutoBot", 3)
player_car = PlayerCar("Player1", 1, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], spawn_point.tolist(),"autos/cars.png")
if num_players ==2:
    player_car2 = PlayerCar("Player2", 2, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], spawn_point.tolist(), "autos/Redbull_car.png")
    player_car2.set_direction(math.atan2(direction_vector[1], direction_vector[0])+8)
# Establecer la dirección inicial del coche mirando hacia la línea de meta
player_car.set_direction(math.atan2(direction_vector[1], direction_vector[0])+8)
auto_car.set_start_position(spawn_point.tolist(), math.atan2(direction_vector[1], direction_vector[0]) + 8)
# Asignar pista al AutoCar
auto_car.set_track(track)
def is_inside_track(self, track):
        """
        Verifica si el coche se encuentra dentro del área de la pista.

        Args:
            track (Track): La pista donde se encuentra el coche.

        Returns:
            bool: True si el coche está dentro del área de la pista, False de lo contrario.
        """
        return track.is_point_inside_track(self.get_position())

track_polygon=track.get_track_area_polygon()
# Bucle principal de Pygame
# Bucle principal de Pygame
running = True
clock = pygame.time.Clock()

winner_declared = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()

    # Obtener los comandos para los coches si no hay un ganador declarado
    if not winner_declared:
        
        if num_players == 2:
            insidetrack2=player_car2.is_inside_track(track)
            player2_command=player_car2.get_command(keys,insidetrack2)
            player_car2.send_command(*player2_command,track)
            player2_distance_to_border = player_car2.calculate_distance_to_border(track)
        insidetrack = player_car.is_inside_track(track)
        auto_command = auto_car.get_command(keys, insidetrack)
        player_command = player_car.get_command(keys, insidetrack)

        # Enviar comandos a los coches
        auto_car.send_command(*auto_command, track)
        player_car.send_command(*player_command, track)

        # Calcular la distancia al borde para el PlayerCar
        player_distance_to_border = player_car.calculate_distance_to_border(track)

    # Dibujar fondo y pista
    if num_players==2:
        if player_car.lap_count > 5:
            winner_declared = True
            winner_text = "PlayerCar Gana!"
            player_car.set_speed(0)
            auto_car.set_speed(0)
            player_car2.set_speed(0)
        elif player_car2.lap_count > 5:
            winner_declared = True
            winner_text = "Playercar2 Gana!"
            player_car.set_speed(0)
            auto_car.set_speed(0)
            player_car2.set_speed(0)
        elif auto_car.lap_count > 5:
            winner_declared = True
            winner_text = "AutoCar Gana!"
            player_car.set_speed(0)
            auto_car.set_speed(0)
            player_car2.set_speed(0)
    screen.blit(background_image, (0, 0))  # Dibujar fondo primero
    draw_track(screen, track)  # Dibujar la pista después
    # Dibujar coches al final para que queden encima del fondo y la pista
    auto_car.draw(screen)
    player_car.draw(screen)
    if num_players ==2:
        player_car2.draw(screen)
    # Mostrar el mensaje del ganador si la carrera ha terminado
    if winner_declared:
        font = pygame.font.Font(None, 74)
        text = font.render(winner_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
    # Verificar teclas para reiniciar o salir del juego
    if keys[pygame.K_r]:
        # Reiniciar el juego (volver a crear las instancias)
        track = Track()
        finish_line_start, finish_line_end = track.finish_line
        midpoint = calculate_custom_point(finish_line_start, finish_line_end, 0.5)
        direction_vector = np.array(finish_line_end) - np.array(finish_line_start)
        direction_vector = direction_vector / np.linalg.norm(direction_vector)
        perpendicular_vector = np.array([-direction_vector[1], direction_vector[0]])
        spawn_distance = 50
        spawn_point = midpoint - perpendicular_vector * spawn_distance
        # Crear instancias del coche
        auto_car = AutoCar("AutoBot", 1)
        player_car = PlayerCar("Player1", 2, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], spawn_point.tolist(),"autos/cars.png")
        player_car.set_direction(math.atan2(direction_vector[1], direction_vector[0]) + 8)
        auto_car.set_start_position(spawn_point.tolist(), math.atan2(direction_vector[1], direction_vector[0]) + 8)
        auto_car.set_track(track)
        if num_players ==2:
            player_car2 = PlayerCar("Player2", 2, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], spawn_point.tolist(),"autos/Redbull_car.png")
            player_car2.set_direction(math.atan2(direction_vector[1], direction_vector[0])+8)
        winner_declared = False
        winner_text = ""
    elif keys[pygame.K_q]:
        pygame.quit()
        sys.exit()
    # Dibujar el contador de vueltas, mensaje de controles y la distancia al borde
    if num_players==2:
        draw_lap_counter(screen, player_car, track)
        draw_lap_counter(screen,player_car2,track)
        draw_controls_message(screen)
        pygame.display.flip()
        clock.tick(100)
    else:
        draw_lap_counter(screen, player_car, track)
        draw_controls_message(screen)
        pygame.display.flip()
        clock.tick(100)
pygame.quit()

