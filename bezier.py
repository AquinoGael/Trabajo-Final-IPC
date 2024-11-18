# ALUMNOS: NO MODIFICAR ESTE ARCHIVO NI USAR ESTAS FUNCIONES EN SU CODIGO

import numpy as np

class Bezier():
    def TwoPoints(t, P1, P2):

        if not isinstance(P1, np.ndarray) or not isinstance(P2, np.ndarray):
            raise TypeError('Points must be an instance of the numpy.ndarray!')
        if not isinstance(t, (int, float)):
            raise TypeError('Parameter t must be an int or float!')

        Q1 = (1 - t) * P1 + t * P2
        return Q1

    def Points(t, points):
        newpoints = []
        for i1 in range(0, len(points) - 1):


            newpoints += [Bezier.TwoPoints(t, points[i1], points[i1 + 1])]
        return newpoints

    def Point(t, points):
        newpoints = points
        while len(newpoints) > 1:
            newpoints = Bezier.Points(t, newpoints)

        return newpoints[0]

    def Curve(t_values, points):

        if not hasattr(t_values, '__iter__'):
            raise TypeError("`t_values` Must be an iterable of integers or floats, of length greater than 0 .")
        if len(t_values) < 1:
            raise TypeError("`t_values` Must be an iterable of integers or floats, of length greater than 0 .")
        if not isinstance(t_values[0], (int, float)):
            raise TypeError("`t_values` Must be an iterable of integers or floats, of length greater than 0 .")

        curve = np.array([[0.0] * len(points[0])])
        for t in t_values:
            curve = np.append(curve, [Bezier.Point(t, points)], axis=0)

        curve = np.delete(curve, 0, 0)
        return curve