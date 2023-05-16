# Author:  Martin McBride
# Created: 2023-05-14
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
The graph module provides classes to draw graphs. It contains:

* The `Graph` class to draw the graph.
* The `Vertex` to represent vertices.
* The `Edge` class to represent edges.
"""
import math
from dataclasses import dataclass
from typing import Union

from generativepy.color import Color
from generativepy.drawing import CENTER, MIDDLE
from generativepy.geometry import Circle, Text, Line, Bezier, ParallelMarker
from generativepy.math import Vector as V


class Vertex:
    """
    Represents a vertex in a graph. This appears as a circle with a text label at the centre.
    """

    def __init__(self, position=(0, 0), label="", fgcolor=None, bgcolor=None, lw=None, radius=None,
                 font=None, text_size=None):
        self.position = position
        self.label = label
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.lw = lw
        self.radius = radius
        self.font = font
        self.text_size = text_size

    def draw(self, ctx, fgcolor, bgcolor, radius, lw, font, text_size):
        """Draw the vertex
        Draw the vertex to the drawing context. This will usually be called by the `Graph` object that owns the vertex,
        although it is possible to draw a vertex directly.
        """
        fgcolor = fgcolor if self.fgcolor is None else self.fgcolor
        bgcolor = bgcolor if self.bgcolor is None else self.bgcolor
        lw = lw if self.lw is None else self.lw
        radius = radius if self.radius is None else self.radius
        font = font if self.font is None else self.font
        text_size = text_size if self.text_size is None else self.text_size
        Circle(ctx).of_center_radius(self.position, radius).fill(bgcolor).stroke(fgcolor, lw)
        Text(ctx).of(self.label, self.position).align(CENTER, MIDDLE).font(font).size(text_size).fill(fgcolor)


class Edge:

    def __init__(self, start, end, directed=False, weight=None, offset=None, curve=False, curvature=1,
                 color=None, lw=None, font=None, text_size=None):
        self.start = start
        self.end = end
        self.directed = directed
        self.weight = weight
        self.offset = offset
        self.curve = curve
        self.curvature = curvature
        self.color = color
        self.lw = lw
        self.font = font
        self.text_size = text_size

    def draw(self, ctx, vertices, color, lw, font, text_size):
        color = color if self.color is None else self.color
        lw = lw if self.lw is None else self.lw
        font = font if self.font is None else self.font
        text_size = text_size if self.text_size is None else self.text_size
        p0 = V(vertices[self.start].position)
        p1 = V(vertices[self.end].position)
        direction = p1 - p0
        if not self.curve:
            Line(ctx).of_start_end(vertices[self.start].position, vertices[self.end].position).stroke(color, lw)
            if self.directed:
                ParallelMarker(ctx).of_start_end(vertices[self.start].position, vertices[self.end].position).with_length(lw*4).stroke(color, lw)
            if self.weight is not None:
                if self.offset is not None:
                    print("---", self.offset, self.weight)
                offset = V.polar(text_size, direction.angle - math.radians(90)) if self.offset is None else V(self.offset)
                print("-", offset, self.weight)
                Text(ctx).of(str(self.weight), (p0+p1)/2).align(CENTER, MIDDLE).size(text_size).offset(*offset).font(font).fill(color)
        else:
            apex = self.arc_between_points(ctx, p0, p1, color, lw)
            if self.directed:
                ParallelMarker(ctx).of_start_end(apex - direction, apex + direction).with_length(lw * 4).stroke(color, lw)
            if self.weight is not None:
                if self.offset is not None:
                    print("+++", self.offset, self.weight)
                offset = V.polar(text_size, direction.angle - math.radians(90)) if self.offset is None else V(self.offset)
                print("+", offset, self.weight)
                Text(ctx).of(str(self.weight), apex).align(CENTER, MIDDLE).size(text_size).offset(*offset).font(font).fill(color)

    def arc_between_points(self, ctx, p0, p1, color, lw):
        x, y = p1 - p0
        a = (p1 - p0).angle - math.radians(90)
        l = (p1 - p0).length
        radius = l/(1.2*self.curvature)
        b = math.asin(l/(2*radius))
        h = radius*math.cos(b)
        c = p0 + V(x/2 - h*(y/l), y/2 + h*(x/l))
        Circle(ctx).of_center_radius(c, radius).as_arc(a-b, a+b).stroke(color, lw)
        return c + V.polar(radius, a)



class Graph:

    def __init__(self, vertices=None, edges=None, fgcolor=Color(0), bgcolor=Color(1), lw=4, radius=30, font="Arial", text_size=30):
        self.vertices = vertices if vertices else []
        self.edges = edges if edges else []
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.lw = lw
        self.radius = radius
        self.font = font
        self.text_size = text_size

    def add(self, item):
        if isinstance(item, Vertex):
            self.vertices.append(item)
        if isinstance(item, Edge):
            self.edges.append(item)

    def draw(self, ctx: object):
        for edge in self.edges:
            edge.draw(ctx, self.vertices, self.fgcolor, self.lw, self.font, self.text_size)
        for vertex in self.vertices:
            vertex.draw(ctx, self.fgcolor, self.bgcolor, self.radius, self.lw, self.font, self.text_size)
