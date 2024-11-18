# ALUMNOS: CUIDADO SI DESEAN MODIFICAR ESTE ARCHIVO

import math

from track.track import Track

class Car:
    def __init__(self, driver_name: str, car_number: int) -> None:
        raise NotImplementedError("Car class must be inherited by a child class")

    def init(self, driver_name: str, car_number: int):
        """
        Initializes the car with the driver name and car number. All the common attributes should be initialized here.
        
        Args:
            driver_name (str): The name of the driver
            car_number (int): The number of the car
        """
        pass

    def get_speed(self) -> float:
        """
        Returns the speed of the car
        
        Returns:
            float: The speed of the car
        """
        pass

    def get_position(self) -> list[float]:
        """
        Returns the position of the car

        Returns:
            list[float]: The position [x, y] of the car
        """
        pass

    def get_direction(self) -> float:
        """
        Returns the direction of the car

        Returns:
            float: The direction of the car in radians
        """
        pass

    def set_position(self, position: list[float]):
        """
        Sets the position of the car (and save the last position too)

        Args:
            position (list[float]): The position [x, y] of the car
        """
        pass

    def set_speed(self, speed: float):
        """
        Sets the speed of the car

        Args:
            speed (float): The speed of the car
        """
        pass

    def set_direction(self, direction: float):
        """
        Sets the direction of the car

        Args:
            direction (float): The direction of the car in radians
        """
        pass

    def set_distances(self, distances: list[float]):
        """
        Sets the distances of the car

        Args:
            distances (list[float]): The distances of the car
        """
        pass

    def get_command(self, pygame_keys: dict, is_inside_track: bool) -> tuple[float, float]:
        """
        Returns the command of the car

        Args:
            pygame_keys (dict): The keys pressed by the player (obtained with pygame.key.get_pressed())
            is_inside_track (bool): If the car is inside the track

        Returns:
            tuple[float, float]: The acceleration and steer of the car
        """
        pass

    def send_command(self, acceleration: float, steer: float):
        """
        Sends the command to the car

        Args:
            acceleration (float): The acceleration of the car (how much to speed up, or slow down in this time step)
            steer (float): The steer of the car (how much to turn in this time step)
        """
        pass

