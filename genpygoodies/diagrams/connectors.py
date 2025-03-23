# Author:  Martin McBride
# Created: 2023-10-12
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
Various line connectors for use with other symbols
"""

from generativepy.drawing import SQUARE, MITER
from generativepy.geometry import FillParameters, StrokeParameters, Line, Circle, Polygon
from generativepy.color import Color
from generativepy.math import Vector as V


class Connector():
    """
    A connector is a line joining two points.
    """

    def __init__(self, start, end):
        """
        Initialise a connector with the start and end points

        **Parameters**

        `start`: (number, number) - Start point of connector.
        `end`: (number, number) - End point of connector.
        """
        self.start = start
        self.end = end

    def strokestyle(self, pattern=Color(0), line_width=1, dash=None, cap=SQUARE, join=MITER, miter_limit=None):
        """
        Sets the stroke style of the connector

        **Parameters**

        * `pattern`:  the fill `Pattern` or `Color` to use for the outline, None for default. Alternatively, if a StrokeParameters
        object is supplied as a `pattern`, the style will be taken from the StrokeParameters object and the remaining parameters will be ignored.
        * `line_width`: width of stroke line. None for default
        * dash`: sequence, dash patter of line. None for default
        * cap`: line end style, None for default.
        * join`: line join style, None for default.
        * miter_limit`: mitre limit, number, None for default

        **Returns**

        self
        """
        if isinstance(pattern, StrokeParameters):
            self.strokeparams = pattern
        else:
            self.strokeparams = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def fillstyle(self, pattern=None, fill_rule=None):
        """
        Sets the fill style for the symbol, using either a `FillParameters` object or a set of fill parameters.

        **Parameters**

        * `pattern`: FillParameters` or `Pattern` - If this parameter is a `FillParameters` object, then it will be used to determine the fill pattern and the remaining parameters will be
                     ignored. Otherwise the fill `Pattern` or `Color` to use. None for default.
        * `fill_rule`: the fill rule to use, None for default.

        **Returns**

        self
        """
        if isinstance(pattern, FillParameters):
           self.fillparams = pattern
        else:
            self.fillparams = FillParameters(pattern, fill_rule)
        return self


    def draw(self, ctx):
        """
        Draw the item on the supplied drawing context

        **Parameters**

        `ctx`: PyCairo Context object - The drawing context.
        """
        (Line(ctx)
         .of_start_end(self.start, self.end)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )

        return self



class ElbowConnector(Connector):
    """
    A connector that joins two points with a stepped connector.
    """

    def __init__(self, start, end, position, horizontal=True):
        """
        Initialise a connector with the start and end points

        **Parameters**

        `start`: (number, number) - Start point of connector.
        `end`: (number, number) - End point of connector.
        `position`: number - Position of the step, in range 0 to 1

        **Returns**

        self
        """
        self.start = start
        self.end = end
        
        if horizontal:
            self.p1 = (start[0] + (end[0] - start[0])*position, start[1])
            self.p2 = (start[0] + (end[0] - start[0])*position, end[1])
        else:
            self.p1 = (start[0], start[1] + (end[1] - start[1])*position)
            self.p2 = (end[0], start[1] + (end[1] - start[1])*position)

    def draw(self, ctx):
        (Polygon(ctx)
         .of_points((self.start, self.p1, self.p2, self.end))
         .open()
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )

        return self



class Connection(Connector):
    """
    A connection is a dot at a point.
    """

    def __init__(self, position, radius):
        """
        Initialise a connection with its position

        **Parameters**

        `start`: (number, number) - Start point of connector.
        `end`: (number, number) - End point of connector.

        **Returns**

        self
        """
        self.position = position
        self.radius = radius

    def draw(self, ctx):
        (Circle(ctx)
         .of_center_radius(self.position, self.radius)
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         )

        return self

