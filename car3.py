# ALUMNOS: CUIDADO SI DESEAN MODIFICAR ESTE ARCHIVO

import math

from track import *

class Car:
    def __init__(self, driver_name: str, car_number: int) -> None:
        self.init(driver_name, car_number)

    def init(self, driver_name: str, car_number: int):
        """
        Initializes the car with the driver name and car number. All the common attributes should be initialized here.
        
        Args:
            driver_name (str): The name of the driver
            car_number (int): The number of the car
        """
        self.original_max_speed=10.0
        self.driver_name = driver_name
        self.car_number = car_number
        self.position = [0.0, 0.0]  # Initial position [x, y]
        self.speed = 0.0            # Initial speed
        self.direction = 0.0        # Initial direction in radians
        self.last_position = [0.0, 0.0]
        self.distances = []         # Distances to obstacles or track boundaries

        # Car specifications
        self.max_speed = self.original_max_speed           # Maximum speed (0.5 units per tick of time)
        self.acceleration_rate = 0.08       # Acceleration per tick of time squared
        self.turn_rate = math.radians(3)      # Turn rate in radians per tick of time (0.5 degrees)

    def get_speed(self) -> float:
        """
        Returns the speed of the car
        
        Returns:
            float: The speed of the car
        """
        return self.speed

    def get_position(self) -> list[float]:
        """
        Returns the position of the car

        Returns:
            list[float]: The position [x, y] of the car
        """
        return self.position

    def get_direction(self) -> float:
        """
        Returns the direction of the car

        Returns:
            float: The direction of the car in radians
        """
        return self.direction

    def set_position(self, position: list[float]):
        """
        Sets the position of the car (and save the last position too)

        Args:
            position (list[float]): The position [x, y] of the car
        """
        self.last_position = self.position.copy()
        self.position = position

    def set_speed(self, speed: float):
        """
        Sets the speed of the car

        Args:
            speed (float): The speed of the car
        """
        self.speed = max(0, min(speed, self.max_speed))  # Limit speed between 0 and max_speed

    def set_direction(self, direction: float):
        """
        Sets the direction of the car

        Args:
            direction (float): The direction of the car in radians
        """
        self.direction = direction % (2 * math.pi)  # Keep direction within 0 to 2*pi

    def set_distances(self, distances: list[float]):
        """
        Sets the distances of the car

        Args:
            distances (list[float]): The distances of the car
        """
        self.distances = distances

    def get_command(self, pygame_keys: dict, is_inside_track: bool) -> tuple[float, float]:
        """
        Returns the command of the car

        Args:
            pygame_keys (dict): The keys pressed by the player (obtained with pygame.key.get_pressed())
            is_inside_track (bool): If the car is inside the track

        Returns:
            tuple[float, float]: The acceleration and steer of the car
        """
        acceleration = 0.0
        steer = 0.0

        if pygame_keys.get('up'):  # Accelerate
            acceleration = self.acceleration_rate
        elif pygame_keys.get('down'):  # Brake
            acceleration = -self.acceleration_rate

        if pygame_keys.get('left'):  # Steer left
            steer = -self.turn_rate
        elif pygame_keys.get('right'):  # Steer right
            steer = self.turn_rate


        return acceleration, steer

    def send_command(self, acceleration: float, steer: float,track:Track):
        """
        Sends the command to the car

        Args:
            acceleration (float): The acceleration of the car (how much to speed up, or slow down in this time step)
            steer (float): The steer of the car (how much to turn in this time step)
        """
        self.speed += acceleration
        self.speed = max(0, min(self.speed, self.max_speed))

        # Reducir la velocidad si el coche está fuera de la pista
        if not self.is_inside_track(track):
            # Reducir la velocidad temporalmente si el coche está fuera de la pista
            self.speed = max(self.speed / 2, self.original_max_speed / 10)
            self.max_speed = self.original_max_speed / 2  # Limitar la velocidad máxima mientras esté fuera
            # Ajustar la dirección para intentar volver a la pista
        else:
            self.max_speed = self.max_speed

        # Actualizar la dirección con el giro
        self.direction += steer
        self.direction %= 2 * math.pi
        # Update the position based on speed and direction
        self.position[0] += self.speed * math.cos(self.direction)
        self.position[1] += self.speed * math.sin(self.direction)
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