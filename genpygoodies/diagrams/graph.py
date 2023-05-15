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
from generativepy.geometry import Circle, Text, Line, Bezier
from generativepy.math import Vector as V


class Vertex:
    """
    Represents a vertex in a graph. This appears as a circle with a text label at the centre.
    """

    def __init__(self, position=(0, 0), label=""):
        self.position = position
        self.label = label

    def draw(self, ctx, fgcolor, bgcolor, radius, lw, font, text_size):
        """Draw the vertex
        Draw the vertex to the drawing context. This will usually be called by the `Graph` object that owns the vertex,
        although it is possible to draw a vertex directly.
        """
        Circle(ctx).of_center_radius(self.position, radius).fill(bgcolor).stroke(fgcolor, lw)
        Text(ctx).of(self.label, self.position).align(CENTER, MIDDLE).font(font).size(text_size).fill(
            fgcolor)


class Edge:
    start: int
    end: int
    directed: bool = False
    weighted: bool = False
    weight: Union[int, float] = 0
    curve: bool = False

    def __init__(self, start, end, directed=False, weighted=False, weight=0, curve=False):
        self.start = start
        self.end = end
        self.directed = directed
        self.weighted = weighted
        self.weight = weight
        self.curve = curve

    def draw(self, ctx, vertices, color, lw):
        if not self.curve:
            Line(ctx).of_start_end(vertices[self.start].position, vertices[self.end].position).stroke(color, lw)
            Line(ctx).of_start_end(vertices[self.start].position, vertices[self.end].position).stroke(color, lw)
        else:
            p0 = V(vertices[self.start].position)
            p1 = V(vertices[self.end].position)
            angle = (p1 - p0).angle
            length = (p1 - p0).length
            bezier_point = (p1+p0)/2 + V.polar(length/5, angle+math.radians(90))
            # Line(ctx).of_start_end(p0, bezier_point).stroke(fgcolor, lw)
            # Line(ctx).of_start_end(p1, bezier_point).stroke(fgcolor, lw)
            Bezier(ctx).of_abcd(p0, bezier_point, bezier_point, p1).stroke(color, lw)


class Graph:

    def __init__(self, vertices=None, edges=None):
        self.vertices = vertices if vertices else []
        self.edges = edges if edges else []
        self.fgcolor = Color(0)
        self.bgcolor = Color(1)
        self.lw = 4
        self.radius = 30
        self.font = "Arial"
        self.text_size = 30

    def add(self, item):
        if isinstance(item, Vertex):
            self.vertices.append(item)
        if isinstance(item, Edge):
            self.edges.append(item)

    def draw(self, ctx: object):
        for edge in self.edges:
            edge.draw(ctx, self.vertices, self.fgcolor, self.lw)
        for vertex in self.vertices:
            vertex.draw(ctx, self.fgcolor, self.bgcolor, self.radius, self.lw, self.font, self.text_size)
