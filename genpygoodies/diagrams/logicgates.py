# Author:  Martin McBride
# Created: 2023-07-29
# Copyright (C) 2023, Martin McBride
# License: MIT
import math

from generativepy.geometry import Polygon, Circle
from generativepy.math import Vector as V

from genpygoodies.diagrams.symbol import Symbol

class Buffer(Symbol):

    def __init__(self, position, width, height=None, invert=False):
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

    def label_pos(self):
        return self.position + V(self.width/3, self.height/2)

    def get_default_height(self):
        return self.width


class And(Symbol):

    def __init__(self, position, width, height=None, invert=False):
        super().__init__(position, width, height)
        self.bubble_radius = self.width/10
        self.invert = invert
        output_offset = self.bubble_radius*2 if invert else 0
        self._connectors = (((0, self.height/4), (0, self.height*3/4)), ((self.width + output_offset, self.height/2),))

    def draw(self, ctx):
        a = V(self.position) +  V(self.height/2, 0)
        b = V(self.position)
        c = V(self.position) + V(0, self.height)
        d = V(self.position) + V(self.height/2, self.height)
        centre = V(self.position) + V(self.height/2, self.height/2)
        bubble_centre = a + V(self.width + self.bubble_radius, self.height/2)
        (Polygon(ctx)
         .of_points((a, b, c, d))
         .open()
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )
        (Circle(ctx)
         .of_center_radius(centre, self.height/2)
         .as_arc(math.radians(-90), math.radians(90))
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

    def label_pos(self):
        return self.position + V(self.width/3, self.height/2)

    def get_default_height(self):
        return self.width


