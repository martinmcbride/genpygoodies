# Author:  Martin McBride
# Created: 2025-04-13
# Copyright (C) 2025, Martin McBride
# License: MIT
"""
Graph utility functions.

Styling of graph axes, and special styles for Argand diagrams and blank axes

Some on these functions work best for nominal draw size of about 500 units (passed into the generativepy.drawing.setup function, because
parameters such as line width, dash pattern, angle radius are designed for that approximate size.

It is always possible to create an output image of a different size using the width and height parameters of make_image etc. For example
if a width of 1000 is passed into generativepy.drawing.make_image, the whole image will be scaled up to 1000px so the linewidths etc will
appear correct
"""
from generativepy.graph import Axes


def style_axes(axes, cs):
    """
    Sets a standard style for the axes line width and colours
    Args:
        axes: generativepy.graph.Axes, the axes
        cs: A color space
    """
    (axes.background(cs.WHITE).axis_linestyle(cs.GREY, line_width=2.5)
                              .division_linestyle(cs.GREY.light2, line_width=2.5)
                              .subdivision_linestyle(cs.GREY.light2, line_width=2.5)
                              .text_color(cs.GREY))

def i_formater(value, div):
    """
    Format an axis value  for imaginary numbers. Add i to the number, but use i and -i rather than 1i and -1i
    Args:
        value:
        div:

    Returns:
        The formatted value as a string
    """
    if isinstance(value, int):
        if value == 1:
            return "i"
        if value == -1:
            return "-i"
        return str(value) + "i"
    return str(round(value * 1000) / 1000) + "i"


def style_argand(axes, cs):
    """
    Style axes for an argand diagram. This requires the y axis to be formatted as imaginary.
    Args:
        axes: generativepy.graph.Axes, the axes
        cs: A color space
    """
    style_axes(axes, cs)
    axes.with_division_formatters(y_div_formatter=i_formater)

def blank_formater(value, div):
    """
    Remove numbers from axis.
    Args:
        value:
        div:

    Returns:
        The formatted value as a string
    """
    return ""


def style_blank(axes, cs):
    """
    Style axes for an unscaled graph. Points on the axis are left unnumbered.
    Args:
        axes: generativepy.graph.Axes, the axes
        cs: A color space
    """
    style_axes(axes, cs)
    axes.with_division_formatters(x_div_formatter=blank_formater, y_div_formatter=blank_formater)


def create_axes(ctx, position=(20, 20), width=460, height=460):
    """
    Creates axes with size and location. The default values create axes that are centered within a 500 by 500 drawing space
    Args:
        ctx: Drawing context
        width: number, the width of the graph
        height:  number, the height of the graph
        position: (number, number), the position of the top left of the graph

    Returns:
        The axes
    """
    return Axes(ctx, position, width, height)
