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
        Displays a formula with a zoom animation.

        **Parameters**

        * `formula`: str - Latex formula
        * `position`: (number, number) - Tuple giving position of centre of formula
        * `color`: Color - Colour of formula.
        * `appear_time`: number - Time in seconds when formula appears and zoom starts.
        * `scale_duration`: number - Duration for formula to scale to full size. Default 1.
        * `initial_scale`: number - Initial size of formula as fraction of full size. Default 0.7
        * `dpi`: number - Controls formula size. See formula module of generativepy documentation.
        * `disappear_time`: number - Time in seconds when formula starts to fade. Default `None` formula stays visible forever,
        * `fade_duration`: number - Duration for formula to fade out. See usage.
        * `packages`: sequence of str - list of names of Latex packages the `formula` uses.

        **Returns**

        A configured `formula_zoom_in` object.

        **Usage**
        This class displays a formula that zooms in at a certain time. It is best to have an understanding of the generativepy
        formula module before attempting to use this class. It will explain important details such as the `dpi` and `packages`
        parameters.

        Fading is not currently implemented. The formula will behave as if the `fade_duration` is zero.
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
        """
        Changes the position of the formula. This is MUCH faster than creating a new formula object.

        **Parameters**

        * `position`: (number, number) - Tuple giving position of centre of formula

        **Returns**

        self

        **Usage**
        This can be used to change the display position of an existing formula after it has been created.

        This is useful if the formula appears in a movie and you need to move the formula around for each frame. It allows
        you to create the formula once and then move it on each frame.
        """
        self.position = position
        return self

    def show(self, ctx, fn):
        """
        Draws the formula in a frame

        **Parameters**

        * `ctx`: drawing context - Context to draw the formula into.
        * `fn`: int - Current frame number.

        **Returns**

        None

        **Usage**
        Call this in the draw function of every frame where the formula should appear.
        """
        if self.alpha[fn]:
            Image(ctx).of_file_position(self.image, (self.position[0] - self.size[0] * self.scale[fn] / 2, self.position[1] - self.size[1] * self.scale[fn] / 2)).scale(self.scale[fn]).paint()

class formula_fade_in():

    def __init__(self, formula, position, color, appear_time=0, appear_duration=1, dpi=600, disappear_time=None, fade_duration=1):
        """
        Displays a formula with a fade animation. FADE IS NOT YET IMPLEMENTED see usage.

        **Parameters**

        * `formula`: str - Latex formula
        * `position`: (number, number) - Tuple giving position of centre of formula
        * `color`: Color - Colour of formula.
        * `appear_time`: number - Time in seconds when formula appears and zoom starts.
        * `appear_duration`: number - Duration for formula to fade in. See usage.
        * `dpi`: number - Controls formula size. See formula module of generativepy documentation.
        * `disappear_time`: number - Time in seconds when formula starts to fade. Default `None` formula stays visible forever,
        * `fade_duration`: number - Duration for formula to fade out. See usage.
        * `packages`: sequence of str - list of names of Latex packages the `formula` uses.

        **Returns**

        A configured `formula_fade_in` object.

        **Usage**
        Fading is not currently implemented. The formula will always be visible. The description below is for the intended
        behaviour when it is fully implemented.

        This class displays a formula that fades in at a certain time. It is best to have an understanding of the generativepy
        formula module before attempting to use this class. It will explain important details such as the `dpi` and `packages`
        parameters.
        """
        global _FORMULA_INDEX
        _FORMULA_INDEX += 1
        name = "formula" + str(_FORMULA_INDEX)
        self.image, self.size = rasterise_formula(name, formula, color, dpi=dpi)
        self.position = position
        self.alpha = Tween(0).wait(appear_time).to_d(1, appear_duration)
        if disappear_time is not None:
            self.alpha.wait(disappear_time).to_d(0, fade_duration)

    def at(self, position):
        """
        Changes the position of the formula. This is MUCH faster than creating a new formula object.

        **Parameters**

        * `position`: (number, number) - Tuple giving position of centre of formula

        **Returns**

        self

        **Usage**
        This can be used to change the display position of an existing formula after it has been created.

        This is useful if the formula appears in a movie and you need to move the formula around for each frame. It allows
        you to create the formula once and then move it on each frame.
        """
        self.position = position
        return self

    def show(self, ctx, fn):
        """
        Draws the formula in a frame

        **Parameters**

        * `ctx`: drawing context - Context to draw the formula into.
        * `fn`: int - Current frame number.

        **Returns**

        None

        **Usage**
        Call this in the draw function of every frame where the formula should appear.
        """
        # if self.alpha[fn]:
        #     Image(ctx).of_file_position(self.image, self.position)
        Image(ctx).of_file_position(self.image, self.position)



