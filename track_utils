# ALUMNOS: NO MODIFICAR ESTE ARCHIVO NI USAR ESTAS FUNCIONES EN SU CODIGO

import numpy as np
from track.utils.bezier import Bezier

def calculate_custom_point(p1, p2, perc):
    if not (0 <= perc <= 1):
        raise ValueError("Percentage must be between 0 and 1")


    x_custom_point = (1 - perc) * p1[0] + perc * p2[0]
    y_custom_point = (1 - perc) * p1[1] + perc * p2[1]
    custom_point = (x_custom_point, y_custom_point)
    return custom_point

def curve_corners(points, corner_cells):
    inner_point = []
    outer_point = []
    for i in range(len(points)):
        rand_perc = np.random.uniform(0.1, 0.4)
        p1 = calculate_custom_point(points[i], points[(i+1) % len(points)], rand_perc)
        inner_point.append(p1)
        rand_perc = np.random.uniform(0.6, 0.9)
        p2 = calculate_custom_point(points[i], points[(i+1) % len(points)], rand_perc)
        outer_point.append(p2)

    inner_point = np.array(inner_point)
    outer_point = np.array(outer_point)

    all_t_values = np.linspace(0, 1, corner_cells)
    new_curves = []
    i = 0
    for point in points:
        if i == 0:
            last = len(outer_point)
            item = Bezier.Curve(all_t_values, [outer_point[last-1], point, inner_point[i]])
            for coord in item:
                new_curves.append(coord)
        else:
            item = Bezier.Curve(all_t_values, [outer_point[i-1], point, inner_point[i]])
            for coord in item:
                new_curves.append(coord)
        i += 1
    new_curves.append(outer_point[len(outer_point)-1])

    return np.array(new_curves)

def get_mid_points(p1, p2):
    return (((p1[0] + p2[0]) / 2), 
            ((p1[1] + p2[1]) / 2))

def random_midpoint(points, qty_midpoints):
    center = np.mean(points, axis=0)
    
    for point_num in range(qty_midpoints):
        index = np.random.randint(0, len(points)-2)
        point = get_mid_points(points[index], points[(index+1) % len(points)])

        scale_factor = np.random.uniform(1, 0.1)
        displaced = center[0] + scale_factor * (point[0] - center[0]), center[1] + scale_factor * (point[1] - center[1])

        points = np.insert(points, index+1, displaced, 0)

    return points

    