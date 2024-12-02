#codigo en el que esta desarrollado la inteligencia de la computadora 
import pygame
import numpy as np
import math
from car3 import Car
from track import Track

class AutoCar(Car):
    def __init__(self, driver_name: str, car_number: int):
        """
        Initializes the auto car

        Args:
            driver_name (str): The name of the driver
            car_number (int): The number of the car
        """
        super().__init__(driver_name, car_number)
        self.track = None  # Track instance to keep reference to the track
        self.car_image = pygame.image.load(car_number)  # Load car image for auto cars
        self.car_image = pygame.transform.scale(self.car_image, (40, 20))  # Scale car image to appropriate size
        self.previous_direction = 0  # Store the previous direction to prevent reversing

    def set_track(self, track: Track):
        """
        Sets the track for the AutoCar to reference for pathfinding

        Args:
            track (Track): The track instance
        """
        self.track = track

    def set_start_position(self, start_position, direction):
        """
        Sets the starting position and direction for the AutoCar

        Args:
            start_position (list): The starting position [x, y]
            direction (float): The initial direction in radians
        """
        self.set_position(start_position)
        self.set_direction(direction)
        self.previous_direction = direction

    def get_distance_to_edge(self, angle_offset):
        """
        Calculates the distance to the edge of the track at a given angle offset.

        Args:
            angle_offset (float): The angle offset relative to the car's current direction.

        Returns:
            float: Distance to the track edge.
        """
        car_position = np.array(self.get_position())
        car_direction = self.get_direction() + angle_offset
        direction_vector = np.array([math.cos(car_direction), math.sin(car_direction)])

        for distance in range(1, 50):  # Check for 100 units forward
            point_to_check = car_position + direction_vector * distance
            if not self.track.is_point_inside_track(point_to_check):
                return distance
        return 50  # Maximum distance

    def get_command(self, pygame_keys: dict, is_inside_track: bool) -> tuple[float, float]:
        """
        Returns the command for the car

        Args:
            pygame_keys (dict): The pygame keys (not used in AutoCar)
            is_inside_track (bool): Whether the car is inside the track

        Returns:
            tuple[float, float]: The command [acceleration, steering]
        """
        if self.track is None:
            raise ValueError("Track not set for AutoCar")

        acceleration = self.acceleration_rate
        steer = 0.0

        # Find the closest point on the middle track line
        car_position = np.array(self.get_position())
        closest_distance = float('inf')
        closest_point = None

        for track_point in self.track.middle_of_track:
            distance = np.linalg.norm(car_position - track_point)
            if distance < closest_distance:
                closest_distance = distance
                closest_point = track_point

        if closest_point is not None:
            # Calculate the desired direction to the closest point
            direction_vector = closest_point - car_position
            desired_direction = math.atan2(direction_vector[1], direction_vector[0])

            # Calculate the difference between current and desired direction
            direction_diff = desired_direction - self.get_direction()
            direction_diff = (direction_diff + math.pi) % (2 * math.pi) - math.pi  # Normalize to [-pi, pi]

            # Prevent reversing by limiting the direction difference
            if abs(direction_diff) > math.pi / 2:
                direction_diff = math.copysign(math.pi / 2, direction_diff)

            # Adjust steering based on direction difference
            if direction_diff > 0:
                steer = min(direction_diff, self.turn_rate)
            else:
                steer = max(direction_diff, -self.turn_rate)

        
        distance_pos_45 = self.get_distance_to_edge(math.radians(45))
        distance_neg_45 = self.get_distance_to_edge(math.radians(-45))

        # Adjust acceleration based on distances to the edge
        if distance_pos_45 < 20 or distance_neg_45 < 20:
            acceleration *= 0.0025  # Reduce speed if getting too close to the edge

        # Adjust steering to stay near the lower edge of the track
        lower_edge_distance = self.get_distance_to_edge(math.radians(90))
        upper_edge_distance = self.get_distance_to_edge(math.radians(-90))

        # Mantenerse cerca del borde inferior
        if lower_edge_distance > upper_edge_distance:
            steer -= 0.05  # Incrementar la tendencia a girar hacia el borde inferior
        else:
            steer += 0.05  # Ajustar ligeramente si se aleja mucho del borde superior

        # Ajuste adicional basado en la diferencia de distancias a los bordes
        direction_correction = (distance_pos_45 - distance_neg_45) * 0.01  # Ajuste para mantener la estabilidad
        steer += direction_correction

        # Si el auto está fuera de la pista, ajustar la dirección
        if not is_inside_track:
            acceleration *= 0.0025  # Reducir la aceleración para evitar descontrolarse
            steer += (self.turn_rate*0.5) if self.position[0] < 0 else (-self.turn_rate*0.5)

        # Update the previous direction to prevent reversing
        self.previous_direction = self.get_direction()

        return acceleration, steer

    def draw(self, screen):
        """
        Draws the car on the given screen

        Args:
            screen (pygame.Surface): The surface to draw the car on
        """
        car_position = self.get_position()
        car_direction = self.get_direction()
        rotated_image = pygame.transform.rotate(self.car_image, -math.degrees(car_direction))
        rect = rotated_image.get_rect(center=(car_position[0], car_position[1]))
        screen.blit(rotated_image, rect.topleft)