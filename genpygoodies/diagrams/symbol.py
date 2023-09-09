# Author:  Martin McBride
# Created: 2023-07-29
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
Main module for symbols in diagrams module
"""
from abc import ABC, abstractmethod

from generativepy.drawing import SQUARE, MITER
from generativepy.geometry import FillParameters, StrokeParameters
from generativepy.color import Color
from generativepy.math import Vector as V


class Symbol(ABC):
    """
    Abstract base class for all symbols.
    """
    def __init__(self, position, width, height=None):
        """
        Initialise a symbol object.

        **Parameters**

        * `position`: tuple of numbers - Position of top right boundary of symbol.
        * `width`: number - The width of the symbol.
        * `height`: number - The height of the symbol. If `None` the symbol will use the default height for the supplied width.

        **Returns**

        No return value

        """
        super().__init__()
        self.position = V(position)
        self.width = width
        self._fixed_height = height
        self.strokeparams = StrokeParameters()
        self.fillparams = FillParameters()
        self._connectors = ()

    def fillstyle(self, pattern=None, fill_rule=None):
        """
        Sets the fill style for the symbol, using either a `FillParameters` object or a set of fill parameters.

        **Parameters**

        * `pattern`: `FillParameters` or `Pattern` - If this parameter is a `FillParameters` object, then it will be used to determine the fill pattern and the
        remaining parameters will be ignored. If it is a `Pattern` object, then the patter will be used to fill the object and the remaining parameters will be
        used to controlk the style.
        * `fill_rule`: constant - The fill rule to be used.

        **Returns**

        Self

        """
        if isinstance(pattern, FillParameters):
           self.fillparams = pattern
        else:
            self.fillparams = FillParameters(pattern, fill_rule)
        return self

    def strokestyle(self, pattern=Color(0), line_width=1, dash=None, cap=SQUARE, join=MITER, miter_limit=None, style=None):
        if isinstance(pattern, StrokeParameters):
           self.strokeparams = style
        else:
            self.strokeparams = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def get_connector(self, col, row):
        if col < 0 or col >= len(self._connectors):
            raise ValueError("Connector column out of range")
        if row < 0 or row >= len(self._connectors[col]):
            raise ValueError("Connector row out of range")
        print("get_connector", col, row, self._connectors[col][row], self.position)
        return V(self._connectors[col][row]) + self.position

    @abstractmethod
    def label_pos(self):
        ...

    @property
    def height(self):
        return self._fixed_height if self._fixed_height else self.get_default_height()

    @abstractmethod
    def draw(self, ctx):
        ...

    @abstractmethod
    def get_default_height(self):
        ...


