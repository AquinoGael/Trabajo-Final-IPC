from car import Car

class PlayerCar(Car):
    def __init__(self, driver_name: str, car_number: int, movement_keys: list):
        """
        Initializes the player car

        Args:
            driver_name (str): The name of the driver
            car_number (int): The number of the car
            movement_keys (list): The keys for the movement [up, down, left, right]. 
                                  Probably something like [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        """
        super().init(driver_name, car_number)
        self.movement_keys = movement_keys

    def get_command(self, pygame_keys, is_inside_track):
        """
        Returns the command for the car

        Args:
            pygame_keys (dict): The pygame keys
            is_inside_track (bool): Whether the car is inside the track

        Returns:
            list[float]: The command [acceleration, steering]
        """
        pass
