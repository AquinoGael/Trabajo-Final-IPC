from car3 import Car
import pygame
import numpy as np
import math

class PlayerCar(Car):
    def __init__(self, driver_name: str, car_number: int, movement_keys: list, spawn_point: list, image):
        super().__init__(driver_name, car_number)
        self.movement_keys = movement_keys
        self.car_image = pygame.image.load(image)  # Load car image for player cars
        self.car_image = pygame.transform.scale(self.car_image, (60, 40))  # Adjust car image size (height > width)
        self.set_position(spawn_point)  # Set initial position to the spawn point

    def get_command(self, pygame_keys, is_inside_track):
        acceleration = 0.0
        steer = 0.0

        if pygame_keys[self.movement_keys[0]]:
            acceleration = self.acceleration_rate
        elif pygame_keys[self.movement_keys[1]]:
            acceleration = -self.acceleration_rate * 3

        if pygame_keys[self.movement_keys[2]]:
            steer = -self.turn_rate
        elif pygame_keys[self.movement_keys[3]]:
            steer = self.turn_rate

        return acceleration, steer

    def draw(self, screen):
        car_position = self.get_position()
        car_direction = self.get_direction()
        if car_position is not None and not np.isnan(car_position).any():
            rotated_image = pygame.transform.rotate(self.car_image, -math.degrees(car_direction))
            rect = rotated_image.get_rect(center=(car_position[0], car_position[1]))
            screen.blit(rotated_image, rect.topleft)
