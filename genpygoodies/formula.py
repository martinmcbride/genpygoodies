# Author:  Martin McBride
# Created: 2023-06-03
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
The formula module provides some utility functions and classes for creating formulas that appear and disappear in
specific locations.

The code converts a formula from Latex to a PNG image that is then rendered as an image. The conversion is relatively
time-consuming (typically it takes a few seconds). When making movies is best to avoid creating formulas per frame, if
possible. It is better to create a formula image just once outside the draw function.
"""
from generativepy.formulas import rasterise_formula
from generativepy.tween import Tween
from generativepy.geometry import Image

_FORMULA_INDEX = 0 # Global index used to create temp filenames for formulas

class formula_zoom_in():

    def __init__(self, formula, position, color, appear_time=0, scale_duration=1, initial_scale=0.7, dpi=600, disappear_time=None, fade_duration=1, packages=[]):
        """

        Parameters
        ----------
        formula
        position
        color
        appear_time
        scale_duration
        initial_scale
        dpi
        disappear_time
        fade_duration
        packages
        """
        global _FORMULA_INDEX
        _FORMULA_INDEX += 1
        name = "formula" + str(_FORMULA_INDEX)
        self.image, self.size = rasterise_formula(name, formula, color, dpi=dpi, packages=packages)
        self.position = position
        self.scale = Tween(initial_scale).wait(appear_time).to_d(1, scale_duration)
        self.alpha = Tween(0).wait(appear_time).set(1)
        if disappear_time is not None:
            self.alpha.wait(disappear_time).to_d(0, fade_duration)

    def at(self, position):
        self.position = position
        return self

    def show(self, ctx, fn):
        if self.alpha[fn]:
            Image(ctx).of_file_position(self.image, (self.position[0] - self.size[0] * self.scale[fn] / 2, self.position[1] - self.size[1] * self.scale[fn] / 2)).scale(self.scale[fn]).paint()

class formula_fade_in():

    def __init__(self, formula, position, color, appear_time=0, appear_duration=1, dpi=600, disappear_time=None, fade_duration=1):
        global _FORMULA_INDEX
        _FORMULA_INDEX += 1
        name = "formula" + str(_FORMULA_INDEX)
        self.image, self.size = rasterise_formula(name, formula, color, dpi=dpi)
        self.position = position
        self.alpha = Tween(0).wait(appear_time).to_d(1, appear_duration)
        if disappear_time is not None:
            self.alpha.wait(disappear_time).to_d(0, fade_duration)

    def at(self, position):
        self.position = position
        return self

    def show(self, ctx, fn):
        # if self.alpha[fn]:
        #     Image(ctx).of_file_position(self.image, self.position)
        Image(ctx).of_file_position(self.image, self.position)



