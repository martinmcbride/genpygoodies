# Author:  Martin McBride
# Created: 2023-07-29
# Copyright (C) 2023, Martin McBride
# License: MIT

from generativepy.geometry import Polygon, Circle
from generativepy.math import Vector as V

from genpygoodies.diagrams.symbol import Symbol


class Not(Symbol):

    def __init__(self):
        super().__init__()
        self.bubble_radius = self.width/20
        self._connectors = (((0, self.height/2),), ((self.width + self.bubble_radius*2, self.height/2),))

    def draw(self, ctx):
        a = V(self.position)
        print("height", self.height)
        b = a + V(0, self.height)
        c = a + V(self.width, self.height/2)
        bubble_centre = a + V(self.width + self.bubble_radius, self.height/2)
        (Polygon(ctx)
         .of_points((a, b, c))
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )
        (Circle(ctx)
         .of_center_radius(bubble_centre, self.bubble_radius)
         .fill(self.fillparams.pattern, self.fillparams.fill_rule)
         .stroke(self.strokeparams.pattern, self.strokeparams.line_width, self.strokeparams.dash, self.strokeparams.cap, self.strokeparams.join,
                 self.strokeparams.miter_limit)
         )


    def get_default_height(self):
        return self.width


