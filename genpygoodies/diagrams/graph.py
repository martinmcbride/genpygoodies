# Author:  Martin McBride
# Created: 2023-05-14
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
The graph module provides classes to draw graphs consisting of networks of vertices (or nodes) and edges (or connections). Includes support for directed graphs,
weighted graphs, and loops. It contains:

The `Graph` class is the main class that draws the graph.

The `Vertex` class represents a vertex. A `Vertex` object is created for each vertex in the graph, and added to the
`Graph` object.

The `Edge` class represents an edge. An `Edge` object is created for each edge in the graph, and added to the `Graph`
object.
"""
import math
from dataclasses import dataclass
from typing import Union

from generativepy.color import Color
from generativepy.drawing import CENTER, MIDDLE
from generativepy.geometry import Circle, Text, Line, Bezier, ParallelMarker
from generativepy.math import Vector as V


class Vertex:

    def __init__(self, position=(0, 0), label="", fgcolor=None, bgcolor=None, lw=None, radius=None,
                 font=None, text_size=None):
        """
        Represents a vertex in a graph. This appears as a circle with a text label at the centre.

        **Parameters**

        * position: (number, number) - the position of the centre of the vertex.
        * label: str - the text label.
        * fgcolor: Color - the foreground colour, used for outline and text.
        * bgcolor: Color - the background colour, used to fill the circle.
        * lw: number - the linewidth of the vertext outline.
        * radius: number - the radius of the vertex circle.
        * font: str - the name of the font to use for the text label.
        * text_size: number - the size of the font to use for the text label.

        **Returns**

        The new vertex object

        **Usage**

        Normally it is only necessary to specify the `position` and `label` for the vertex.By default the style of the
        vertex is determined by the parameters of the parent `Graph` object.

        It is only necessary to set the fgcolor, bgcolor, lw, radius, font, and text_size parameters if you wish to
        override the values set for the `Graph` object, for example to male a particular vertex a different colour.
        """
        self.position = position
        self.label = label
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.lw = lw
        self.radius = radius
        self.font = font
        self.text_size = text_size

    def draw(self, ctx, fgcolor, bgcolor, radius, lw, font, text_size):
        """
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
                 color=None, lw=None, font=None, text_size=None, loop_radius=30, loop_angle=0):
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
        self.loop_radius = loop_radius
        self.loop_angle = loop_angle

    def draw(self, ctx, vertices, color, lw, font, text_size, vertex_radius):
        color = color if self.color is None else self.color
        lw = lw if self.lw is None else self.lw
        font = font if self.font is None else self.font
        text_size = text_size if self.text_size is None else self.text_size
        p0 = V(vertices[self.start].position)
        p1 = V(vertices[self.end].position)
        if self.start == self.end: # Loop
            c = p0 + V.polar(vertex_radius + self.loop_radius*0.8, self.loop_angle)
            Circle(ctx).of_center_radius(c, self.loop_radius).stroke(color, lw)
            apex = c + V.polar(self.loop_radius, self.loop_angle)
            direction = V.polar(self.loop_radius, self.loop_angle+math.radians(90))
            if self.directed:
                ParallelMarker(ctx).of_start_end(apex-direction, apex+direction).with_length(lw*4).stroke(color, lw)
            if self.weight is not None:
                offset = V.polar(text_size*0.7, direction.angle - math.radians(90)) if self.offset is None else V(self.offset)
                Text(ctx).of(str(self.weight), apex).align(CENTER, MIDDLE).size(text_size).offset(*offset).font(font).fill(color)
        elif not self.curve: # Straight edge
            direction = p1 - p0
            Line(ctx).of_start_end(vertices[self.start].position, vertices[self.end].position).stroke(color, lw)
            if self.directed:
                ParallelMarker(ctx).of_start_end(vertices[self.start].position, vertices[self.end].position).with_length(lw*4).stroke(color, lw)
            if self.weight is not None:
                offset = V.polar(text_size*0.7, direction.angle - math.radians(90)) if self.offset is None else V(self.offset)
                Text(ctx).of(str(self.weight), (p0+p1)/2).align(CENTER, MIDDLE).size(text_size).offset(*offset).font(font).fill(color)
        else: # Curved edge
            direction = p1 - p0
            apex = self.arc_between_points(ctx, p0, p1, color, lw)
            if self.directed:
                ParallelMarker(ctx).of_start_end(apex - direction, apex + direction).with_length(lw * 4).stroke(color, lw)
            if self.weight is not None:
                offset = V.polar(text_size*0.7, direction.angle - math.radians(90)) if self.offset is None else V(self.offset)
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
            edge.draw(ctx, self.vertices, self.fgcolor, self.lw, self.font, self.text_size, self.radius)
        for vertex in self.vertices:
            vertex.draw(ctx, self.fgcolor, self.bgcolor, self.radius, self.lw, self.font, self.text_size)
