# Author:  Martin McBride
# Created: 2024-01-23
# Copyright (C) 2024, Martin McBride
# License: MIT
"""
Complex number related functionality
"""
import logging

import numpy as np
from generativepy.color import ArtisticColorScheme, Color, make_colormap
from generativepy.drawing import CENTER, FONT_WEIGHT_BOLD
from generativepy.drawing import (setup, MIDDLE, LEFT, )
from generativepy.geometry import (Text, Transform, Line, Circle, )
from generativepy.graph import Axes
from generativepy.math import Vector as V

FONT = "DejaVu Sans"
cs = ArtisticColorScheme()

def draw_overlay(ctx, pixel_width, pixel_height, frame_no, frame_count):
    """
    Drawing function to create an overlay to add "real" and "imaginary" text to a 3D plot.

    This can be used to annotate a plot created with povray to show z against a complex x-y plane.

    Args:
        ctx:
        pixel_width:
        pixel_height:
        frame_no:
        frame_count:

    Returns:

    """
    logging.warning("Update complex.py to allow selection of FONT and cs")
    # Draw the text overlay (marking axes)
    setup(ctx, pixel_width, pixel_height, width=500, background=Color(1))
    a = V(58, 350)
    b = V(250, 457)
    c = V(442, 350)
    angle = 0.55
    mid1 = ((a[0] + b[0]) / 2 - 50, (a[1] + b[1]) / 2 + 30)
    mid2 = ((c[0] + b[0]) / 2 + 50, (c[1] + b[1]) / 2 + 30)
    with Transform(ctx).translate(*mid1).rotate(angle):
        (
            Text(ctx)
            .of("Real", (0, 0))
            .size(20)
            .font(FONT, FONT_WEIGHT_BOLD)
            .align(CENTER, MIDDLE)
            .fill(cs.BLUE)
        )
    with Transform(ctx).translate(*mid2).rotate(-angle):
        (
            Text(ctx)
            .of("Imaginary", (0, 0))
            .size(20)
            .font(FONT, FONT_WEIGHT_BOLD)
            .align(CENTER, MIDDLE)
            .fill(cs.BLUE)
        )


def i_formater(value, div):
    if isinstance(value, int):
        if value == 1:
            return "i"
        if value == -1:
            return "-i"
        return str(value) + "i"
    return str(round(value * 1000) / 1000) + "i"


def style_argand_transparent(axes):
    (
        axes.background(cs.WHITE.with_a(0))
        .axis_linestyle(cs.BLACK, line_width=2.5)
        .division_linestyle(cs.WHITE.with_a(0), line_width=2.5)
        .text_color(cs.BLACK)
    )
    axes.with_division_formatters(y_div_formatter=i_formater)


def draw_complex_plane(
    ctx,
    f,
    low,
    high,
    width,
    height,
    startx=None,
    starty=None,
    elements=200,
    steps=[-2, -1, 0, 1, 2],
    divisions=(1, 1),
    colormap=None,
):
    """
    Plot a real function of a complex variable on and argand diagram, as a colour map. The plot also includes a key.

    Args:
        ctx:
        f:
        low:
        high:
        width:
        height:
        startx:
        starty:
        elements:
        steps:
        divisions:
        colormap:
    """
    if startx is None:
        startx = -width / 2
    if starty is None:
        starty = -height / 2

    if not colormap:
        colormap = make_colormap(
            1000,
            colors=[
                cs.YELLOW,
                cs.ORANGE,
                Color("red"),
                cs.GREY.light2,
                cs.GREEN,
                cs.CYAN,
                cs.BLUE,
            ],
        )
    graph_size = 380
    graph_pos = (8, 8)

    xcoords = np.linspace(startx, startx + width, num=elements)
    ycoords = np.linspace(starty, starty + height, num=elements)

    x = np.tile(xcoords, (elements, 1))
    y = np.tile(np.array([ycoords]).transpose(), (1, elements))

    vfunc = np.vectorize(f)
    out = vfunc(x, y)

    axes = (
        Axes(ctx, graph_pos, graph_size, graph_size)
        .of_start((startx, starty))
        .of_extent((width, height))
        .with_divisions(divisions)
    )

    for i in range(elements):
        x = xcoords[i]
        for j in range(elements):
            y = ycoords[j]
            p = axes.transform_from_graph((x, y))
            v = max(0, min(999, int((out[j, i] - low) * 1000 / (high - low))))
            Circle(ctx).of_center_radius(p, 2).fill(colormap[v])

    style_argand_transparent(axes)
    axes.draw()

    with Transform(ctx).translate(400, 0):
        for i in range(graph_size):
            p1 = (0, graph_size + graph_pos[1] - i)
            p2 = (30, graph_size + graph_pos[1] - i)
            Line(ctx).of_start_end(p1, p2).stroke(
                colormap[i * len(colormap) // graph_size], 2
            )
        for v in steps:
            l = (v - low) / (high - low)
            p = (1 - l) * graph_size + graph_pos[1]
            Line(ctx).of_start_end((30, p), (35, p)).stroke(cs.BLACK, 2)
            Text(ctx).of(str(v), (35, p)).size(15).align(LEFT, MIDDLE).offset(
                5, 0
            ).fill(cs.BLACK)


