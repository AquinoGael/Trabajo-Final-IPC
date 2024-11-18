# ALUMNOS: NO MODIFICAR ESTE ARCHIVO. NO USAR LAS FUNCIONES QUE EMPIEZAN CON GUION BAJO EN SU CODIGO

import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import LineString, Point, MultiPoint
import math

from car.car import Car
from track.utils.track_utils import curve_corners, random_midpoint

class Track:
    def __init__(self, num_points: int=15, corner_cells: int=20, x_max: int=800, y_max: int=600, width: int=20, margin_x: int=50, margin_y: int=50):
        self.width = width
        self.middle_of_track = self._generate_track([margin_x, x_max - margin_x], [margin_y, y_max - margin_y], num_points, corner_cells)
        self.track_polygon = self._create_ring_polygon()
        angle = np.arctan2(
            self.middle_of_track[1][1] - self.middle_of_track[0][1],
            self.middle_of_track[1][0] - self.middle_of_track[0][0]
        )
        angle += np.pi / 2
        self.finish_line = LineString([
            (self.middle_of_track[0][0] + width / 2 * np.cos(angle), self.middle_of_track[0][1] + width / 2 * np.sin(angle)),
            (self.middle_of_track[0][0] - width / 2 * np.cos(angle), self.middle_of_track[0][1] - width / 2* np.sin(angle))
        ])

    def get_starting_position(self) -> list[float]:
        """
        Returns the starting position of the track
        
        Returns:
            list[float]: The starting position [x, y] of the track
        """
        return self.middle_of_track[1] - (self.middle_of_track[1] - self.middle_of_track[0]) * 0.9
    
    def get_starting_direction(self) -> float:
        """
        Returns the starting direction of the track

        Returns:
            float: The starting direction in radians of the track
        """
        return math.atan2(self.middle_of_track[1][1] - self.middle_of_track[0][1],
                          self.middle_of_track[1][0] - self.middle_of_track[0][0])

    def _generate_track(self, x_bounds, y_bounds, num_points, corner_cells):
        x_values = np.random.uniform(x_bounds[0], x_bounds[1], num_points)
        y_values = np.random.uniform(y_bounds[0], y_bounds[1], num_points)
        points = np.column_stack((x_values, y_values))
        
        hull = ConvexHull(points)
        hull_verts = points[hull.vertices]
        
        hull_verts = random_midpoint(hull_verts, num_points // 3)
        curves = curve_corners(hull_verts, corner_cells)
        
        return curves

    def _create_ring_polygon(self):
        outer_line = LineString(self.middle_of_track)
        
        outer_buffer = outer_line.buffer(self.width / 2)
        inner_buffer = outer_line.buffer(-self.width / 2)
        
        track_polygon = outer_buffer.difference(inner_buffer)
        
        return track_polygon

    def is_point_inside_track(self, point: list[float]) -> bool:
        """
        Checks if a point is inside the track

        Args:
            point (list[float]): The point to check [x, y]

        Returns:
            bool: True if the point is inside the track, False otherwise
        """
        return self.track_polygon.contains(Point(point))

    def calculate_distance_to_edge(self, position: list[float], direction: float, angle_offset: float) -> float | None:
        """
        Calculates the distance from a point to the edge of the track in a direction
        
        Args:
            position (list[float]): The position [x, y] of the car
            direction (float): The direction in radians of the car
            angle_offset (float): The angle offset relative to the direction in radians

        Returns:
            float | None: The distance to the edge of the track in the direction, None if there is no intersection
        """
        car_point = Point(position)
        
        new_direction = direction + angle_offset
        ray_length = 1000
        
        ray_end_x = position[0] + ray_length * math.cos(new_direction)
        ray_end_y = position[1] + ray_length * math.sin(new_direction)
        ray_line = LineString([car_point, (ray_end_x, ray_end_y)])
        
        intersections = self.track_polygon.boundary.intersection(ray_line)
        
        if intersections.is_empty:
            return None
        
        if isinstance(intersections, Point):
            return car_point.distance(intersections)
        elif isinstance(intersections, MultiPoint):
            distances = [car_point.distance(point) for point in intersections.geoms]
            return min(distances)
        else:
            return car_point.distance(intersections)
        
    def get_distances_car(self, position: list[float], direction: float) -> list[float]:
        """
        Returns the distances to the edges of the track in the left and right directions

        Args:
            position (list[float]): The position [x, y] of the car
            direction (float): The direction in radians of the car

        Returns:
            list[float]: The distances to the edges of the track in the left and right directions
        """

        left_distance = self.calculate_distance_to_edge(position, direction, math.radians(45))
        right_distance = self.calculate_distance_to_edge(position, direction, math.radians(-45))
        
        return [left_distance, right_distance]

    def check_lap(self, trajectory: list[list[float]]) -> bool:
        """
        Checks if a car has completed a lap

        Args:
            trajectory (list[list[float]]): The trajectory of the car [[last_position_x, last_position_y], [current_position_x, current_position_y]]

        Returns:
            bool: True if the car has completed a lap, False otherwise
        """
        trajectory_line = LineString(trajectory)
        return trajectory_line.intersects(self.finish_line)
    
    def move_car(self, car: Car):
        """
        Moves the car

        Args:
            car (Car): The car to move
        """
        if not self.is_point_inside_track(car.position):
            speed = car.get_speed() / 10
        else:
            speed = car.get_speed()
        position = [car.get_position()[0], car.get_position()[1]]
        position[0] += speed * math.cos(car.get_direction())
        position[1] += speed * math.sin(car.get_direction())
        car.set_position(position)
