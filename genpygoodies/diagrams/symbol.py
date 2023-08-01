# Author:  Martin McBride
# Created: 2023-07-29
# Copyright (C) 2023, Martin McBride
# License: MIT

from abc import ABC, abstractmethod

from generativepy.drawing import SQUARE, MITER
from generativepy.geometry import FillParameters, StrokeParameters
from generativepy.color import Color
from generativepy.math import Vector as V


class Symbol(ABC):

    def __init__(self):
        super().__init__()
        self.position = (0, 0)
        self.width = 100
        self._fixed_height = None
        self.strokeparams = StrokeParameters()
        self.fillparams = FillParameters()
        self._connectors = ()

    def of_corner_size(self, position, width, height=None):
        self.position = V(position)
        self.width = width
        self._fixed_height = height
        return self

    def fillstyle(self, pattern=None, fill_rule=None, style=None):
        if style:
           self.fillparams = style
        else:
            self.fillparams = FillParameters(pattern, fill_rule)
        return self

    def strokestyle(self, pattern=Color(0), line_width=1, dash=None, cap=SQUARE, join=MITER, miter_limit=None, style=None):
        if style:
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

    @property
    def height(self):
        return self._fixed_height if self._fixed_height else self.get_default_height()

    @abstractmethod
    def draw(self, ctx):
        ...

    @abstractmethod
    def get_default_height(self):
        ...


