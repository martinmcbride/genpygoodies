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

from generativepy.drawing import ROUND, BOTTOM, TOP, LEFT, RIGHT, CENTER, MIDDLE
from generativepy.geometry import Line, Marker, StrokeParameters, Circle, Text
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
TO = 10                 # Nominal text offset from point

def LN(color):
    """
    Stroke params for a solid line of width LW
    Args:
        color: Line colour

    Returns:

    """
    return StrokeParameters(color, LW, cap=ROUND, join=ROUND)

def DASHED(color):
    """
    Stroke params for a dashed line of width LW
    Args:
        color: Line colour

    Returns:

    """
    return StrokeParameters(color, LW, cap=ROUND, join=ROUND, dash=[LW * 2, LW*2])

def DOTTED(color):
    """
    Stroke params for a dotted line of width LW
    Args:
        color: Line colour

    Returns:

    """
    return StrokeParameters(color, LW, cap=ROUND, join=ROUND, dash=[0, LW * 2])

def dot(ctx, p, color, radius=DOT):
    """
    Draw a dot
    """
    Circle(ctx).of_center_radius(p, radius).fill(color)


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

def text_align_for_angle(angle):
    """
    If text is offset from a point by and angle, the tex must be correctly aligned. For example, if text is displaced at 45 degrees
    clockwise from _ve x axis, the top left of the text should be aligned to the offset point.

    Args:
        angle: float, angle of text offset in radians, clockwise from +ve x axis.

    Returns:
        (halign, valign) the horizontal nd vertical text align, eg (LEFT, TOP) defined in `generativepy.drawing`.

    """
    angle = -math.degrees(angle)

    if angle > 5 and angle < 175:
        valign = BOTTOM
    elif angle < -5 and angle > -175:
        valign = TOP
    else:
        valign = MIDDLE

    if angle > -85 and angle < 85:
        halign = LEFT
    elif angle > 95 or angle < -95:
        halign = RIGHT
    else:
        halign = CENTER

    return halign, valign

def label_line(ctx, text, a, b, color, offset=TO, font=FONT, size=TEXT_SIZE):
    """
    Places a text label near the midpoint of a line.

    Args:
        ctx: The graphics context
        text: str, the text
        a: Vector, the start point of the line
        b:  Vector, the start point of the line
        color: Color, the colour of the text
        offset: float, the offset distance
        font: font, the font to use
        size: float, the text size

    Returns:
        None

    """
    origin = (a + b) / 2
    displacement = ortho_angle(a, b)
    halign, valign = text_align_for_angle((displacement - origin).angle)

    Text(ctx).of(text, origin).offset_towards(displacement, offset).size(size).font(font).align(halign, valign).fill(color)

