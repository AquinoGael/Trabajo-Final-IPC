import pygame
import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import LineString, Polygon, MultiLineString, Point
import math
from tracks import curve_corners, random_midpoint

# Inicializar Pygame
pygame.init()

# Obtener tamaño de pantalla del usuario
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w - 100  # Reducir 100 píxeles del ancho para bordes
SCREEN_HEIGHT = screen_info.current_h - 100  # Reducir 100 píxeles del alto para barras

# Configurar la pantalla en modo ventana


# Seleccionar aleatoriamente una imagen de fondo


# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Clase Track usando las herramientas proporcionadas por el profesor
class Track:
    def __init__(self, num_points=15, corner_cells=20, x_max=SCREEN_WIDTH, y_max=SCREEN_HEIGHT, width=20, margin_x=50, margin_y=50, max_width=56):
        """
        Inicializa una instancia de la clase Track.

        Args:
            num_points (int): Número de puntos para generar la pista.
            corner_cells (int): Número de celdas para las esquinas.
            x_max (int): Máxima coordenada X de la pantalla.
            y_max (int): Máxima coordenada Y de la pantalla.
            width (int): Ancho de la pista.
            margin_x (int): Margen en el eje X para evitar los bordes de la pantalla.
            margin_y (int): Margen en el eje Y para evitar los bordes de la pantalla.
            max_width (int): Ancho máximo permitido de la pista.
        """
        self.width = width
        self.max_width = max_width
        self.middle_of_track = None
        self.inner_track = None
        self.outer_track = None
        self.spawn_point = None
        self.finish_line = None
        
        # Generar la pista hasta que se cumpla la condición de ancho máximo sin detener el programa
        while True:
            self.middle_of_track = self._generate_track([margin_x, x_max - margin_x], [margin_y, y_max - margin_y], num_points, corner_cells)
            self.inner_track = self._create_offset_line(50)
            self.outer_track = self._create_offset_line(-50)
            if self._check_track_width():
                self.spawn_point, self.finish_line = self._generate_spawn_and_finish_line(inner=True)
                break

    def _generate_track(self, x_bounds, y_bounds, num_points, corner_cells):
        """
        Genera la pista utilizando puntos aleatorios y curvas.

        Args:
            x_bounds (list): Límites en el eje X para los puntos generados.
            y_bounds (list): Límites en el eje Y para los puntos generados.
            num_points (int): Número de puntos a generar.
            corner_cells (int): Número de celdas para suavizar las esquinas.

        Returns:
            numpy.ndarray: Puntos que representan la pista suavizada.
        """
        min_distance = 10  # Distancia mínima permitida entre puntos
        x_values = np.random.uniform(x_bounds[0], x_bounds[1], num_points * 1)  # Aumentar la cantidad de puntos
        y_values = np.random.uniform(y_bounds[0], y_bounds[1], num_points * 1)  # Aumentar la cantidad de puntos
        points = np.column_stack((x_values, y_values))
        
        # Filtrar puntos para asegurar la distancia mínima
        filtered_points = [points[0]]
        for point in points[1:]:
            if np.linalg.norm(point - filtered_points[-1]) > min_distance:
                filtered_points.append(point)
        points = np.array(filtered_points)
        
        hull = ConvexHull(points)
        hull_verts = points[hull.vertices]
        
        hull_verts = random_midpoint(hull_verts, num_points // 3)
        curves = curve_corners(hull_verts, corner_cells)
        
        return curves

    def _create_offset_line(self, offset):
        """
        Crea una línea desplazada desde la línea media de la pista.

        Args:
            offset (float): Desplazamiento hacia la izquierda de la línea media.

        Returns:
            numpy.ndarray: Coordenadas de la línea desplazada.
        """
        middle_line = LineString(self.middle_of_track)
        try:
            offset_line = middle_line.parallel_offset(offset, 'left', resolution=16, join_style=2, mitre_limit=5.0)
            if isinstance(offset_line, LineString):
                coords = np.array(offset_line.coords)
            elif isinstance(offset_line, MultiLineString):
                coords = max(offset_line, key=lambda line: line.length).coords
            else:
                return None
            return coords
        except ValueError:
            return None

    def _check_track_width(self):
        """
        Verifica que el ancho de la pista no exceda el máximo permitido y que no haya estrechamientos inusuales.

        Returns:
            bool: True si la pista cumple con los requisitos de ancho, False de lo contrario.
        """
        if self.middle_of_track is None or self.outer_track is None or self.inner_track is None:
            return False
        
        middle_line = LineString(self.middle_of_track)
        outer_line = LineString(self.outer_track)
        inner_line = LineString(self.inner_track)
        
        # Iterar sobre cada punto de la línea del medio para medir la distancia al borde exterior e interior
        for i in range(len(self.middle_of_track)):
            middle_point = Point(self.middle_of_track[i])
            # Encontrar el punto más cercano en la línea exterior
            closest_outer_point = outer_line.interpolate(outer_line.project(middle_point))
            distance_to_outer = middle_point.distance(closest_outer_point)
            if distance_to_outer > self.max_width:
                return False
            # Verificar que la distancia entre la línea interior y exterior cumpla con el ancho mínimo
            closest_inner_point = inner_line.interpolate(inner_line.project(middle_point))
            distance_to_inner = middle_point.distance(closest_inner_point)
            if distance_to_inner < (self.width / 4):
                return False
        return True

    def _generate_spawn_and_finish_line(self, inner=False):
        """
        Genera la línea de meta y el punto de inicio en la pista.

        Returns:
            tuple: Punto de inicio y coordenadas de la línea de meta.
        """
        # Buscar un segmento recto de la pista para generar la línea de meta
        best_segment_index = None
        max_length = 0

        for i in range(len(self.middle_of_track) - 1):
            start = self.middle_of_track[i]
            end = self.middle_of_track[i + 1]
            segment_length = np.linalg.norm(end - start)
            
            # Buscar el segmento más largo para garantizar que esté en una parte recta
            if segment_length > max_length:
                max_length = segment_length
                best_segment_index = i

        # Si no se encuentra un buen segmento, usar el primer segmento
        if best_segment_index is None:
            best_segment_index = 0

        best_segment_index = min(best_segment_index, len(self.inner_track) - 2) if inner else min(best_segment_index, len(self.middle_of_track) - 2)
        spawn_point = self.inner_track[best_segment_index] if inner else self.middle_of_track[best_segment_index]
        best_segment_index_next = min(best_segment_index + 1, len(self.inner_track) - 1) if inner else min(best_segment_index + 1, len(self.middle_of_track) - 1)
        next_point = self.inner_track[best_segment_index_next] if inner else self.middle_of_track[best_segment_index_next]
        
        # Calcular el punto medio del segmento seleccionado
        midpoint = (spawn_point + next_point) / 2
        
        # Calcular el vector normal para la dirección de la línea de meta
        direction_vector = next_point - spawn_point
        normal_vector = np.array([-direction_vector[1], direction_vector[0]])
        normal_vector = normal_vector / np.linalg.norm(normal_vector)
        
        # Ajustar la longitud de la línea de meta para que vaya desde la pista interior hasta la pista exterior
        finish_line_start = midpoint  # Desde la pista interior
        finish_line_end = midpoint - normal_vector * 50  # Hasta la pista exterior
        return spawn_point, (finish_line_start, finish_line_end)

    def get_starting_position(self) -> list:
        """
        Retorna la posición inicial de la pista.

        Returns:
            list: La posición inicial [x, y] de la pista.
        """
        return self.middle_of_track[1] - (self.middle_of_track[1] - self.middle_of_track[0]) * 0.9
    
    def get_starting_direction(self) -> float:
        """
        Retorna la dirección inicial de la pista.

        Returns:
            float: La dirección inicial en radianes de la pista.
        """
        return math.atan2(self.middle_of_track[1][1] - self.middle_of_track[0][1],
                          self.middle_of_track[1][0] - self.middle_of_track[0][0])


    def get_track_area_polygon(self):
        """
        Devuelve un polígono que representa el área de la pista entre la línea interior y la línea media.

        Returns:
            Polygon: El polígono que representa el área de la pista.
        """
        if self.inner_track is None or self.middle_of_track is None:
            return None
        
        # Crear un polígono a partir de la combinación de las coordenadas de la línea media y la línea interior
        combined_coords = np.vstack((self.middle_of_track, self.inner_track[::-1]))
        track_polygon = Polygon(combined_coords)
        return track_polygon
    def is_point_inside_track(self, point: list[float]) -> bool:
        """
        Verifica si el coche se encuentra dentro del área de la pista.

        Args:
            point (list[float]): El punto a verificar [x, y].

        Returns:
            bool: True si el coche está dentro del área de la pista, False de lo contrario.
        """
        track_polygon = self.get_track_area_polygon()
        if track_polygon is None:
            return False
        
        car_point = Point(point)
        return track_polygon.contains(car_point)
# Dibujar la pista en Pygame
def draw_track(screen, track):
    """
    Dibuja la pista y sus elementos en la pantalla.

    Args:
        screen (pygame.Surface): La superficie de la pantalla donde se dibuja la pista.
        track (Track): La instancia de la pista a dibujar.
    """
    # Dibujar los pianos en los bordes de la pista (rojo y blanco alternados cada 8 píxeles)
    if track.inner_track is not None:
        inner_coords = np.array(track.inner_track).astype(int)
        is_red = True  # Comenzar con rojo
        pixel_count = 0  # Contador de píxeles
        for i in range(len(inner_coords) - 1):
            start = inner_coords[i]
            end = inner_coords[i + 1]
            segment_vector = end - start
            segment_length = np.linalg.norm(segment_vector)
            direction = segment_vector / segment_length
            current_position = start
            while np.linalg.norm(current_position - start) < segment_length:
                next_position = current_position + 8 * direction
                color = RED if is_red else WHITE  # Alternar entre rojo y blanco cada 8 píxeles
                pygame.draw.line(screen, color, current_position, next_position, 10)
                current_position = next_position
                pixel_count += 8
                if pixel_count >= 8:
                    is_red = not is_red  # Cambiar el color después de 8 píxeles
                    pixel_count = 0

    if track.middle_of_track is not None:
        middle_coords = np.array(track.middle_of_track).astype(int)
        is_red = True  # Comenzar con rojo
        pixel_count = 0  # Contador de píxeles
        for i in range(len(middle_coords) - 1):
            start = middle_coords[i]
            end = middle_coords[i + 1]
            segment_vector = end - start
            segment_length = np.linalg.norm(segment_vector)
            direction = segment_vector / segment_length
            current_position = start
            while np.linalg.norm(current_position - start) < segment_length:
                next_position = current_position + 8 * direction
                color = RED if is_red else WHITE  # Alternar entre rojo y blanco cada 8 píxeles
                pygame.draw.line(screen, color, current_position, next_position, 10)
                current_position = next_position
                pixel_count += 8
                if pixel_count >= 8:
                    is_red = not is_red  # Cambiar el color después de 8 píxeles
                    pixel_count = 0

    # Dibujar el área entre la línea central y la línea interior
    if track.inner_track is not None:
        middle_coords = np.array(track.middle_of_track).astype(int)
        combined_coords = np.vstack((middle_coords, inner_coords[::-1]))
        pygame.draw.polygon(screen, (128, 128, 128), combined_coords)
    # Dibujar el área entre la línea central y la línea interior
    if track.inner_track is not None:
        inner_coords = np.array(track.inner_track).astype(int)
        middle_coords = np.array(track.middle_of_track).astype(int)
        combined_coords = np.vstack((middle_coords, inner_coords[::-1]))
        track_texture = pygame.image.load("asphalt.png")
        track_texture = pygame.transform.scale(track_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))
        track_mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(track_mask, (255, 255, 255), combined_coords)
        track_texture.blit(track_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(track_texture, (0, 0))
    # Dibujar la línea central de la pista
    pygame.draw.lines(screen, BLACK, False, np.array(track.middle_of_track).astype(int), 2)
    # Dibujar la línea interior a 50 píxeles
    if track.inner_track is not None:
        pygame.draw.lines(screen, BLACK, False, track.inner_track.astype(int), 2)
    
    # Dibujar la línea de meta
    finish_line_start, finish_line_end = track.finish_line
    finish_line_image = pygame.image.load("finish_line.png")
    finish_line_rect = finish_line_image.get_rect()
    finish_line_length = np.linalg.norm(np.array(finish_line_end) - np.array(finish_line_start))
    scale_factor = finish_line_length / finish_line_rect.width
    new_height = int(finish_line_rect.height * 0.2)  # Reducir la altura a la mitad
    finish_line_image = pygame.transform.scale(finish_line_image, (int(finish_line_length), new_height))
    finish_line_angle = math.degrees(math.atan2(finish_line_end[1] - finish_line_start[1], finish_line_end[0] - finish_line_start[0]))
    finish_line_image = pygame.transform.rotate(finish_line_image, -finish_line_angle)
    finish_line_rect = finish_line_image.get_rect(center=((finish_line_start[0] + finish_line_end[0]) // 2, (finish_line_start[1] + finish_line_end[1]) // 2))
    screen.blit(finish_line_image, finish_line_rect.topleft)


