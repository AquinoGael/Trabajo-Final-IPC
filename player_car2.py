from car3 import Car
import pygame
import numpy as np
import math

class PlayerCar(Car):
    def __init__(self, driver_name: str, car_number: int, movement_keys: list, spawn_point: list):
        """
        Initializes the player car

        Args:
            driver_name (str): The name of the driver
            car_number (int): The number of the car
            movement_keys (list): The keys for the movement [up, down, left, right]. 
                                  Probably something like [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
            spawn_point (list): The spawn point [x, y] of the car on the track
        """
        super().init(driver_name, car_number)
        self.movement_keys = movement_keys
        self.car_image = pygame.image.load("autos/mclaren_car.png")  # Load car image for player cars
        self.car_image = pygame.transform.scale(self.car_image, (60, 40))  # Adjust car image size (height greater than width)
        self.set_position(spawn_point)  # Set initial position to the spawn point

    def get_command(self, pygame_keys, is_inside_track):
        """
        Returns the command for the car

        Args:
            pygame_keys (dict): The pygame keys
            is_inside_track (bool): Whether the car is inside the track

        Returns:
            tuple[float, float]: The command [acceleration, steering]
        """
        acceleration = 0.0
        steer = 0.0

        if pygame_keys[self.movement_keys[0]]:  # Accelerate (W)
            acceleration = self.acceleration_rate
        elif pygame_keys[self.movement_keys[1]]:  # Brake (S)
            acceleration = -self.acceleration_rate*3

        if pygame_keys[self.movement_keys[2]]:  # Steer left (A)
            steer = -self.turn_rate
        elif pygame_keys[self.movement_keys[3]]:  # Steer right (D)
            steer = self.turn_rate

        # If the car is not inside the track, reduce acceleration and steer to avoid getting out of control


        return acceleration, steer

    def draw(self, screen):
        """
        Draws the car on the given screen

        Args:
            screen (pygame.Surface): The surface to draw the car on
        """
        car_position = self.get_position()
        car_direction = self.get_direction()
        if car_position is not None and not np.isnan(car_position).any():
            rotated_image = pygame.transform.rotate(self.car_image, -math.degrees(car_direction))
            rect = rotated_image.get_rect(center=(car_position[0], car_position[1]))
            screen.blit(rotated_image, rect.topleft)