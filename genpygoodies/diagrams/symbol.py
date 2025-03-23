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
        Initialise a symbol object

        **Parameters**

        `position`: (number, number) - Position of top right boundary of symbol.
        `width`: number - The width of the symbol.
        `height`: number - The height of the symbol. If `None` the symbol will use the default height for the supplied width.

        **Returns**

        self
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

    def strokestyle(self, pattern=Color(0), line_width=1, dash=None, cap=SQUARE, join=MITER, miter_limit=None, style=None):
        """
        Sets the stroke style of the symbol

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

    def get_connector(self, col, row):
        """
        Gets the position of a connector.

        A connector is a point on the symbol where it might be joined to other symbols. The number and types of connections varies depending on the type
        of symbol.

        Connectors are accessed by column and row, but the meaning of these depends on the type of symbol. For example, for the And gate symbol, column 0
        represents inputs, so the two inputs would be col 0 row 0 and col 0 row 1. Column 1 represents outputs so col 1 row 0 is the output.

        **Parameters**

        `col`: int - The column index.
        `row`: int - The row index.

        **Returns**

        A Vector giving the position of the requestd connector. This will be specified relative to the user space that the symbol was created for.
        """
        if col < 0 or col >= len(self._connectors):
            raise ValueError("Connector column out of range")
        if row < 0 or row >= len(self._connectors[col]):
            raise ValueError("Connector row out of range")
        return V(self._connectors[col][row]) + self.position

    @abstractmethod
    def label_pos(self):
        """
        Gets the position for placing a label.

        For symbols that support a label, this will return the position for the label. The label text should be centered on that point.

        **Returns**

        A Vector giving the position for the label. This will be specified relative to the user space that the symbol was created for. If the symbol doesn't
        support labels this will return None.
        """
        ...

    @property
    def height(self):
        """
        Read only property representing the height of the symbol. Symbols have a default height, which will usually be calculated based on the
        width of the symbol.

        Symbol implementations should calculate the height in their `get_default_height` implementation.

        **Returns**

        Return the height if it was set in the constructor, or a default height if it was not set.
        """
        return self._fixed_height if self._fixed_height else self.get_default_height()

    @abstractmethod
    def draw(self, ctx):
        """
        Draw the symbol on the supplied drawing context

        **Parameters**

        `ctx`: PyCairo Context object - The drawing context.
        """
        ...

    @abstractmethod
    def get_default_height(self):
        """
        Ths method should return the default height of the symbol. This will often depend on the s=width of teh symbol, `self.width`.

        **Returns**

        The default height of the symbol, number.
        """
        ...


