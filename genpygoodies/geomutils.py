# Author:  Martin McBride
# Created: 2025-03-23
# Copyright (C) 2025, Martin McBride
# License: MIT
"""
Geometry utility functions.

Some on these functions work best for nominal draw size of about 500 units (passed into the generativepy.drawing.setup function, because
parameters such as line width, dash pattern, angle radius are designed for that approximate size.

It is always possible to create an output image of a different size using the width and height parameters of make_image etc. For example
if a width of 1000 is passed into generativepy.drawing.make_image, the whole image will be scaled up to 1000px so the linewidths etc will
apppear correct
"""
import math

from generativepy.drawing import ROUND
from generativepy.geometry import Line, Marker, StrokeParameters
from generativepy.math import Vector as V

FONT = "DejaVu Sans"    # Default font
DRAW_HEIGHT = 500       # Nominal drawing height

# Some useful defaults that work well with default drawing size

LW = 4                  # Line width
DOT = 6                 # Small dot radius
TICK_LENGTH = 20        # Length of a tick or parallel marker
TICK_GAP = 10           # Gap between multiple tick or parallel markers
ANGLE_RADIUS = 40       # Default angle marker radius
ANGLE_RADIUS_SMALL = 30 # Smaller angle marker radius
ANGLE_GAP = 10          # Gap between multiple angle markers
TEXT_SIZE = 30          # Default text size for label text
TO = 20                 # Nominal text offset from point

def LN(color):
    """
    Stroke params for a solid line of width LW
    Args:
        color: Line colour

    Returns:

    """
    return StrokeParameters(color, LW, cap=ROUND, join=ROUND)

def DASH(color):
    """
    Stroke params for a dashed line of width LW
    Args:
        color: Line colour

    Returns:

    """
    return StrokeParameters(color, LW, cap=ROUND, join=ROUND, dash=[LW * 2, LW*2])

def DOT(color):
    """
    Stroke params for a dotted line of width LW
    Args:
        color: Line colour

    Returns:

    """
    return StrokeParameters(color, LW, cap=ROUND, join=ROUND, dash=[0, LW * 2])


def extended_line(ctx, a, b, ext, stroke_params):
    """
    Draw a dashed line between a and b, extended by a length ext in each direction
    """
    start = a - (b-a).unit*ext
    end = b + (b-a).unit*ext
    Line(ctx).of_start_end(start, end).stroke(stroke_params)


def arrow_line(ctx, a, b, ext, stroke_params, tick_length=TICK_LENGTH):
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
