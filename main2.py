import pygame
import numpy as np
from car3 import *
from player_car2 import PlayerCar
from auto_car2 import AutoCar
from track import *
import math
from tracks import *
import sys
import random



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

    lap_text = font.render(lap_message, True, (255, 255, 255))
    speed_text = font.render(speed_message, True, (255, 255, 255))
    border_text = font.render(border_message, True, (255, 255, 255))

    screen.blit(lap_text, (10, 10))
    screen.blit(speed_text, (10, 50))
    screen.blit(border_text, (10, 90))

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

# Crear el AutoCar y PlayerCar utilizando el punto de inicio calculado
auto_car = AutoCar("AutoBot", 1)
player_car = PlayerCar("Player1", 2, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], spawn_point.tolist())
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
        insidetrack = player_car.is_inside_track(track)
        auto_command = auto_car.get_command(keys, insidetrack)
        player_command = player_car.get_command(keys, insidetrack)

        # Enviar comandos a los coches
        auto_car.send_command(*auto_command, track)
        player_car.send_command(*player_command, track)

        # Calcular la distancia al borde para el PlayerCar
        player_distance_to_border = player_car.calculate_distance_to_border(track)

    # Dibujar fondo y pista
    if player_car.lap_count > 5:
        winner_declared = True
        winner_text = "PlayerCar Gana!"
        player_car.set_speed(0)
        auto_car.set_speed(0)
    elif auto_car.lap_count > 5:
        winner_declared = True
        winner_text = "AutoCar Gana!"
        player_car.set_speed(0)
        auto_car.set_speed(0)

    screen.blit(background_image, (0, 0))  # Dibujar fondo primero
    draw_track(screen, track)  # Dibujar la pista después

    # Dibujar coches al final para que queden encima del fondo y la pista
    auto_car.draw(screen)
    player_car.draw(screen)

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
        # Recalcular el spawn point
        finish_line_start, finish_line_end = track.finish_line
        midpoint = calculate_custom_point(finish_line_start, finish_line_end, 0.5)
        direction_vector = np.array(finish_line_end) - np.array(finish_line_start)
        direction_vector = direction_vector / np.linalg.norm(direction_vector)
        perpendicular_vector = np.array([-direction_vector[1], direction_vector[0]])
        spawn_distance = 50
        spawn_point = midpoint - perpendicular_vector * spawn_distance

        # Crear instancias del coche
        auto_car = AutoCar("AutoBot", 1)
        player_car = PlayerCar("Player1", 2, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], spawn_point.tolist())
        player_car.set_direction(math.atan2(direction_vector[1], direction_vector[0]) + 8)
        auto_car.set_start_position(spawn_point.tolist(), math.atan2(direction_vector[1], direction_vector[0]) + 8)
        auto_car.set_track(track)

        winner_declared = False
        winner_text = ""
    elif keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

    # Dibujar el contador de vueltas, mensaje de controles y la distancia al borde
    draw_lap_counter(screen, player_car, track)
    draw_controls_message(screen)

    pygame.display.flip()

    clock.tick(100)

# Salir de Pygame
pygame.quit()
