# Author:  Martin McBride
# Created: 2025-03-23
# Copyright (C) 2025, Martin McBride
# License: MIT
"""
Geometry utility functions
"""
import math

from generativepy.geometry import Line, Marker
from generativepy.math import Vector as V


def extended_line(ctx, a, b, ext, stroke_params):
    """
    Draw a dashed line between a and b, extended by a length ext in each direction
    """
    start = a - (b-a).unit*ext
    end = b + (b-a).unit*ext
    Line(ctx).of_start_end(start, end).stroke(stroke_params)

def arrow_line(ctx, a, b, ext, stroke_params, tick_length):
    """
    Draw a dashed line between a and b, extended by a length ext in each direction
    """
    start = a + (b-a).unit*ext
    end = b - (b-a).unit*ext
    Line(ctx).of_start_end(start, end).stroke(stroke_params)
    Marker(ctx).of_points(start, end, 1).as_parallel(tick_length).stroke(stroke_params)


def mid_angle(a, b, c):
    """
    Return a point p such that the angle from b to p bisects the angle from b to a and b to c
    """
    return  b + (a - b).unit + (c - b).unit

def ortho_angle(a, b):
    """
    Return a point p that is on the perpendicular bisector the line ab
    """
    perp = V.polar(10, (b - a).angle + math.radians(90))
    return  (a + b)/2 + perp

def intersection(p1, p2, p3, p4):
    """
    Return the point of intersection between the line defined by p1/p2, and the line defined
    by p3/p4
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    x = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4))/((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    y = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4))/((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    return V(x, y)
