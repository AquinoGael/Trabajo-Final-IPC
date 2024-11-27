# ALUMNOS: CUIDADO SI DESEAN MODIFICAR ESTE ARCHIVO

import math
from shapely.geometry import Point, LineString

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
        self.lap_count = 0  # Contador de vueltas
        self.last_position = [0.0, 0.0]  # Posición anterior
        self.lap_block_ticks = 0  # Temporizador para bloquear el conteo de vueltas después de cruzar la meta

        self.originalacceleration_rate = 0.08       # Acceleration per tick of time squared
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
        self.acceleration_rate = self.originalacceleration_rate       # Acceleration per tick of time squared
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

    def send_command(self, acceleration: float, steer: float,track,reduce_speed_outside_track: bool = True):
        """
        Envía el comando al coche y actualiza el contador de vueltas si se cruza la línea de meta.

        Args:
            acceleration (float): La aceleración del coche (cuánto acelerar o desacelerar en este paso de tiempo).
            steer (float): El giro del coche (cuánto girar en este paso de tiempo).
            track (Track): La pista para verificar si el coche está dentro del área permitida.
        """
        # Verificar si se ha completado una vuelta
        if track and track.finish_line and track.check_lap(self) and self.lap_block_ticks == 0:
            self.lap_count += 1
            self.lap_block_ticks = 100  # Bloquear el conteo de vueltas por 100 ticks
        """
        Sends the command to the car

        Args:
            acceleration (float): The acceleration of the car (how much to speed up, or slow down in this time step)
            steer (float): The steer of the car (how much to turn in this time step)
        """
        self.speed += acceleration
        self.speed = max(0, min(self.speed, self.max_speed))

        if not self.is_inside_track(track) and reduce_speed_outside_track:
            # Reducir la velocidad máxima mientras esté fuera, pero permitir control del usuario
            self.max_speed = self.original_max_speed *0.1  # Limitar la velocidad máxima a un cuarto de la original
            # La velocidad actual se reduce, pero no debe bajar de un mínimo para que aún se mueva si el usuario no frena
            if acceleration >= 0:
                self.speed = max(0, self.speed * 1)
        else:
            # Restablecer la velocidad máxima si el coche vuelve a la pista
            self.max_speed = self.original_max_speed
            self.acceleration_rate=self.originalacceleration_rate
        # Actualizar la dirección con el giro
        self.direction += steer
        self.direction %= 2 * math.pi
        # Update the position based on speed and direction
        self.position[0] += self.speed * math.cos(self.direction)
        self.position[1] += self.speed * math.sin(self.direction)

        if self.lap_block_ticks > 0:
            self.lap_block_ticks -= 1

        
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
    
    def calculate_distance_to_border(self, track: 'Track') -> float:
        """
        Calcula la distancia desde la posición del coche al borde más cercano de la pista.

        Args:
            track (Track): La pista en la cual el coche se encuentra.

        Returns:
            float: La distancia al borde más cercano. Si el coche está fuera de la pista, la distancia será negativa.
        """
        car_point = Point(self.position)
        track_polygon = track.get_track_area_polygon()

        if track_polygon.contains(car_point):
            # Dentro de la pista, calcular distancia al borde más cercano
            min_distance = min(
                car_point.distance(LineString(track.inner_track)),
                car_point.distance(LineString(track.middle_of_track))
            )
            return min_distance
        else:
            # Fuera de la pista, retornar la distancia en negativo
            min_distance = -min(
                car_point.distance(LineString(track.inner_track)),
                car_point.distance(LineString(track.middle_of_track))
            )
            return min_distance