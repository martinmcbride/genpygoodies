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
        Circle(ctx).of_center_radius(self.position, radius).fill(bgcolor.with_a(0)).stroke(fgcolor, lw)
        Text(ctx).of(self.label, self.position).align(CENTER, MIDDLE).font(font).size(text_size).fill(
            fgcolor)


class Edge:

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
        else:
            p0 = V(vertices[self.start].position)
            p1 = V(vertices[self.end].position)
            radius = 200
            self.arc_between_points(ctx, p0, p1, radius, color, lw)

    def arc_between_points(self, ctx, p0, p1, radius, color, lw):
        x, y = p1 - p0
        a = (p1 - p0).angle
        l = (p1 - p0).length
        b = math.asin(l/(2*radius))
        h = radius*math.cos(b)
        c = p0 + V(x/2 - h*(y/l), y/2 + h*(x/l))
        Circle(ctx).of_center_radius(c, radius).as_arc(a-b-math.radians(90), a+b-math.radians(90)).stroke(Color("red"), lw)



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
