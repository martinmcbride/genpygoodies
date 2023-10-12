# Author:  Martin McBride
# Created: 2023-10-12
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
Various line connectors
"""

from generativepy.drawing import SQUARE, MITER
from generativepy.geometry import FillParameters, StrokeParameters, Line, Circle
from generativepy.color import Color
from generativepy.math import Vector as V


class Connector():
    """
    A connector is a line joining two points.
    """

    def __init__(self, start, end):
        """
        Initialise a connector with the start and end points
        Args:
            start: Start point of connector, sequence of 2 numbers.
            end: End point of connector, sequence of 2 numbers.
        """
        self.start = start
        self.end = end

    def strokestyle(self, pattern=Color(0), line_width=1, dash=None, cap=SQUARE, join=MITER, miter_limit=None):
        """
        Sets the stroke style of the connector
        Args:
            pattern: Pattern to fill the line, normally a `Color` object. Alternatively, if a StrokeParameters object is supplied as a `pattern`, the style
            will be taken from the StrokeParameters object and the remaining parameters will be ignored.
            line_width: Width of connection line in userspace units, Number.
            dash: Dash sequence as defined in generativepy.drawing module. Sequnce of numbers.
            cap: Line cap as defined in generativepy.drawing module. Integer.
            join:  Line join as defined in generativepy.drawing module. Integer.
            miter_limit: Smallest angle that mitre join style can apply to. If mitre style is selected but the angle is too snale, bevel style wil be used instead.

        Returns:
            self
        """
        if isinstance(pattern, StrokeParameters):
            self.strokeparams = pattern
        else:
            self.strokeparams = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def draw(self, ctx):
        """
        Draw the item on the supplied drawing context

        Args:
            ctx: The drawing context, a PyCairo Context object.

        Returns:
            None
        """
        (Line(ctx)
         .of_start_end(self.start, self.end)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )


class Connection():
    """
    A connection is a dot at a point.
    """

    def __init__(self, position, radius):
        """
        Initialise a connection with its position
        Args:
            position: Position of connector, sequence of 2 numbers.
            radius: Radius of the dot, number.
        """
        self.position = position
        self.radius = radius

    def fillstyle(self, pattern=None, fill_rule=None):
        """
        Sets the fill style for the symbol, using either a `FillParameters` object or a set of fill parameters.

        Args:
            pattern: If this parameter is a `FillParameters` object, then it will be used to determine the fill pattern and the remaining parameters will be
                     ignored. If it is a `Pattern` object, then the patter will be used to fill the object and the remaining parameters will be used to control
                    the style. `FillParameters` or `Pattern`
            fill_rule: The fill rule to be used. Only used if `pattern` is a `Pattern` object. EVEN_ODD or WINDING

        Returns:
            Self

        """
        if isinstance(pattern, FillParameters):
           self.fillparams = pattern
        else:
            self.fillparams = FillParameters(pattern, fill_rule)
        return self

    def draw(self, ctx):
        """
        Draw the item on the supplied drawing context

        Args:
            ctx: The drawing context, a PyCairo Context object.

        Returns:
            None
        """
        (Circle(ctx)
         .of_center_radius(self.position, self.radius)
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         )
