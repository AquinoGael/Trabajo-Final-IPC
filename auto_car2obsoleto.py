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
        super().init(driver_name, car_number)
        self.track = None  # Track instance to keep reference to the track
        self.car_image = pygame.image.load("autos/car.png")  # Load car image for auto cars
        self.car_image = pygame.transform.scale(self.car_image, (40, 20))  # Scale car image to appropriate size

    def set_track(self, track: Track):
        """
        Sets the track for the AutoCar to reference for pathfinding

        Args:
            track (Track): The track instance
        """
        self.track = track

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

            # Adjust steering based on direction difference
            if direction_diff > 0:
                steer = min(direction_diff, self.turn_rate)
            else:
                steer = max(direction_diff, -self.turn_rate)

        # If the car is getting close to the boundary or not inside the track, adjust steering
        if not is_inside_track:
            # Reduce acceleration to avoid getting out of control
            acceleration *= 0.5
            # Randomly adjust steering to try to re-enter the track
            steer += self.turn_rate if self.position[0] < 0 else -self.turn_rate

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
