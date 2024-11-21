import pygame
import numpy as np
from car3 import *
from player_car2 import PlayerCar
from auto_car2 import AutoCar
from track import *
import math
from tracks import *
# Inicializar Pygame
pygame.init()

# Obtener tamaño de pantalla del usuario
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w - 100
SCREEN_HEIGHT = screen_info.current_h - 100

import random
background_images = ["grass.png"]
selected_image = random.choice(background_images)
background_image = pygame.image.load(selected_image)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Configurar la pantalla en modo ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulación de Pista")

# Crear la pista
# Crear la pista
# Crear la pista
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()

    # Obtener los comandos para los coches
    insidetrack=player_car.is_inside_track(track)  # Aquí podrías añadir lógica para verificar si está dentro de la pista
    auto_command = auto_car.get_command(keys, insidetrack)
    player_command = player_car.get_command(keys, insidetrack)

    # Enviar comandos a los coches
    auto_car.send_command(*auto_command,track)
    player_car.send_command(*player_command,track)

    # Dibujar fondo y pista
    screen.blit(background_image, (0, 0))  # Dibujar fondo primero
    draw_track(screen, track)  # Dibujar la pista después

    # Dibujar coches al final para que queden encima del fondo y la pista
    auto_car.draw(screen)
    player_car.draw(screen)
    print(player_car.is_inside_track(track))
    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(100)


# Salir de Pygame
pygame.quit()
