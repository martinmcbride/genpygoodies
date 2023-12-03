# Author:  Martin McBride
# Created: 2023-07-29
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
Contains symbols for

* Simple logic gates such as AND, OR gates.
* Block components such as flip-flops.
"""
import math

from generativepy.geometry import Polygon, Circle, Line, Transform, Rectangle
from generativepy.math import Vector as V

from genpygoodies.diagrams.symbol import Symbol

class Buffer(Symbol):
    """
    Draws a logic gate, either Buffer or a NOT gate, depending whether the `invert` parameter is set in the constructor.
    """

    def __init__(self, position, width, height=None, invert=False):
        """
        Initialise a buffer object
        
        **Parameters**

        `position`: (number, number) - Position of top right boundary of symbol.
        `width`: number - The width of the symbol.
        `height`: number - The height of the symbol. If `None` the symbol will use the default height for the supplied width.
        `invert`: bool - True if the gate is inverting, in which case a bobble is added to the output.
        
        **Returns**

        self
        """
        super().__init__(position, width, height)
        self.bubble_radius = self.width/10
        self.invert = invert
        output_offset = self.bubble_radius*2 if invert else 0
        self._connectors = ((V(0, self.height/2),), (V(self.width + output_offset, self.height/2),))

    def draw(self, ctx):
        a = V(self.position)
        b = a + V(0, self.height)
        c = a + V(self.width, self.height/2)
        bubble_centre = a + V(self.width + self.bubble_radius, self.height/2)
        (Polygon(ctx)
         .of_points((a, b, c))
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )
        if self.invert:
            (Circle(ctx)
             .of_center_radius(bubble_centre, self.bubble_radius)
             .fill(self.fillparams.pattern, self.fillparams.fill_rule)
             .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                     self.strokeparams.miter_limit)
             )
        return self

    def label_pos(self):
        return self.position + V(self.width/3, self.height/2)

    def get_default_height(self):
        return self.width


class And(Symbol):
    """
    Draws a logic gate, either an AND or a NAND gate, depending whether the `invert` parameter is set in the constructor.
    """

    def __init__(self, position, width, height=None, invert=False):
        """
        Initialise an AND gate

        **Parameters**

        `position`: (number, number) - Position of top right boundary of symbol.
        `width`: number - The width of the symbol.
        `height`: number - The height of the symbol. If `None` the symbol will use the default height for the supplied width.
        `invert`: bool - True if the gate is inverting, in which case a bobble is added to the output.

        **Returns**

        self
        """
        super().__init__(position, width, height)
        self.bubble_radius = self.width/10
        self.invert = invert
        output_offset = self.bubble_radius*2 if invert else 0
        self._connectors = (((0, self.height/4), (0, self.height*3/4)), ((self.width + output_offset, self.height/2),))

    def draw(self, ctx):
        a = V(self.position) +  V(0, self.height)
        b = V(self.position)
        centre = V(self.position) + V(self.height/2, self.height/2)
        bubble_centre = V(self.position) + V(self.width + self.bubble_radius, self.height/2)
        (Line(ctx)
         .of_start_end(a, b)
         .add()
         )
        (Circle(ctx)
         .of_center_radius(centre, self.height/2)
         .as_arc(math.radians(-90), math.radians(90))
         .extend_path(close=True)
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )
        if self.invert:
            (Circle(ctx)
             .of_center_radius(bubble_centre, self.bubble_radius)
             .fill(self.fillparams.pattern, self.fillparams.fill_rule)
             .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                     self.strokeparams.miter_limit)
             )
        return self

    def label_pos(self):
        return self.position + V(2*self.width/5, self.height/2)

    def get_default_height(self):
        return self.width


class Or(Symbol):
    """
    Draws a logic gate, either an OR or a NOR gate, depending whether the `invert` parameter is set in the constructor.
    """

    def __init__(self, position, width, height=None, invert=False):
        """
        Initialise an OR gate

        **Parameters**

        `position`: (number, number) - Position of top right boundary of symbol.
        `width`: number - The width of the symbol.
        `height`: number - The height of the symbol. If `None` the symbol will use the default height for the supplied width.
        `invert`: bool - True if the gate is inverting, in which case a bobble is added to the output.

        **Returns**

        self
        """
        super().__init__(position, width, height)
        self.bubble_radius = self.width/10
        self.invert = invert
        output_offset = self.bubble_radius*2 if invert else 0
        self._connectors = (((0.13333*self.width, self.height/4), (0.13333*self.width, self.height*3/4)), ((self.width + output_offset, self.height/2),))

    def draw(self, ctx):
        a = V(self.position)
        b = a + V(0, self.height)
        c = a + V(self.width, self.height/2)
        ab1 = V(self.position) + V(0.2*self.width, 0.25*self.height)
        ab2 = V(self.position) + V(0.2*self.width, 0.75*self.height)
        bc1 = V(self.position) + V(0.4*self.width, 1*self.height)
        bc2 = V(self.position) + V(0.8*self.width, 0.8*self.height)
        ca1 = V(self.position) + V(0.8*self.width, 0.2*self.height)
        ca2 = V(self.position) + V(0.4*self.width, 0*self.height)
        ab = [*ab1, *ab2, *b]
        bc = [*bc1, *bc2, *c]
        ca = [*ca1, *ca2, *a]
        bubble_centre = V(self.position) + V(self.width + self.bubble_radius, self.height/2)
        (Polygon(ctx)
         .of_points((a, ab, bc, ca))
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )
        if self.invert:
            (Circle(ctx)
             .of_center_radius(bubble_centre, self.bubble_radius)
             .fill(self.fillparams.pattern, self.fillparams.fill_rule)
             .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                     self.strokeparams.miter_limit)
             )
        return self

    def label_pos(self):
        return self.position + V(2*self.width/5, self.height/2)

    def get_default_height(self):
        return self.width


class Xor(Symbol):
    """
    Draws a logic gate, either an XOR or a XNOR gate, depending whether the `invert` parameter is set in the constructor.
    """

    def __init__(self, position, width, height=None, invert=False):
        """
        Initialise an XOR gate

        **Parameters**

        `position`: (number, number) - Position of top right boundary of symbol.
        `width`: number - The width of the symbol.
        `height`: number - The height of the symbol. If `None` the symbol will use the default height for the supplied width.
        `invert`: bool - True if the gate is inverting, in which case a bobble is added to the output.

        **Returns**

        self
        """
        super().__init__(position, width, height)
        self.bubble_radius = self.width/10
        self.invert = invert
        output_offset = self.bubble_radius*2 if invert else 0
        self._connectors = (((0.13333*self.width, self.height/4), (0.13333*self.width, self.height*3/4)), ((self.width + output_offset, self.height/2),))

    def draw(self, ctx):
        a = V(self.position)
        b = a + V(0, self.height)
        c = a + V(self.width, self.height/2)
        ab1 = V(self.position) + V(0.2*self.width, 0.25*self.height)
        ab2 = V(self.position) + V(0.2*self.width, 0.75*self.height)
        bc1 = V(self.position) + V(0.4*self.width, 1*self.height)
        bc2 = V(self.position) + V(0.8*self.width, 0.8*self.height)
        ca1 = V(self.position) + V(0.8*self.width, 0.2*self.height)
        ca2 = V(self.position) + V(0.4*self.width, 0*self.height)
        ab = [*ab1, *ab2, *b]
        bc = [*bc1, *bc2, *c]
        ca = [*ca1, *ca2, *a]
        bubble_centre = V(self.position) + V(self.width + self.bubble_radius, self.height/2)
        (Polygon(ctx)
         .of_points((a, ab, bc, ca))
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )
        with Transform(ctx).translate(-0.2*self.width, 0):
            (Polygon(ctx)
             .of_points((a, ab))
             .open()
             .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                     self.strokeparams.miter_limit)
             )
        if self.invert:
            (Circle(ctx)
             .of_center_radius(bubble_centre, self.bubble_radius)
             .fill(self.fillparams.pattern, self.fillparams.fill_rule)
             .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                     self.strokeparams.miter_limit)
             )
        return self

    def label_pos(self):
        return self.position + V(2*self.width/5, self.height/2)

    def get_default_height(self):
        return self.width

class BoxItem(Symbol):
    """
    Draws a box with inputs and outputs, used for compound items like adders or flip-flops
    """

    def __init__(self, position, width, height=None, left_connections=2, right_connections=1, top_connections=0, bottom_connections=0):
        """
        Initialise the box item.
        Future - decorate output/inputs with bubble, clock
        
        **Parameters**

        `position`: (number, number) - Position of top right boundary of symbol.
        `width`: number - The width of the symbol.
        `height`: number - The height of the symbol. If `None` the symbol will use the default height for the supplied width.
        `left_connections`: int - Number of connection points (usually inputs) on the left side of the box. Connections will be evenly distributed.
        `right_connections`: int - Number of connection points (usually outputs) on the right side of the box. Connections will be evenly distributed.
        `top_connections`: int - Number of connection points (usually inputs) on the top side of the box. Connections will be evenly distributed.
        `bottom_connections`: int - Number of connection points (usually inputs) on the bottom side of the box. Connections will be evenly distributed.
        **Returns**

        self
        """
        super().__init__(position, width, height)
        gap = self.height / left_connections if left_connections else 0
        left = [V(0, gap * (i + 0.5)) for i in range(left_connections)]
        gap = self.height / right_connections if right_connections else 0
        right = [V(self.width, gap * (i + 0.5)) for i in range(right_connections)]
        gap = self.width / top_connections if top_connections else 0
        top = [V(gap * (i + 0.5), 0) for i in range(top_connections)]
        gap = self.width / bottom_connections if bottom_connections else 0
        bottom = [V(gap * (i + 0.5), self.height) for i in range(bottom_connections)]
        self._connectors = (left, right, top, bottom)

    def draw(self, ctx):
        (Rectangle(ctx)
         .of_corner_size(self.position, self.width, self.height)
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )
        return self

    def label_pos(self):
        return self.position + V(self.width/2, self.height/2)

    def get_default_height(self):
        return self.width


