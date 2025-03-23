# Author:  Martin McBride
# Created: 2023-05-14
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
The graph module provides classes to draw graphs consisting of networks of vertices (or nodes) and edges (or connections).
Includes support for directed graphs, weighted graphs, and loops.

The `Graph` class is the main class that draws the graph.

The `Vertex` class represents a vertex. A `Vertex` object is created for each vertex in the graph, and added to the
`Graph` object.

The `Edge` class represents an edge. An `Edge` object is created for each edge in the graph, and added to the `Graph`
object. Edges can be drawn as straight or curved, with an optional direction arrow and weight label. A loop can be drawn by
specifying the same vertex as the start and end vertex.
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

        * `position`: (number, number) - the position of the centre of the vertex.
        * `label`: str - the text label.
        * `fgcolor`: Color - overrides the foreground colour, used for outline and text.
        * `bgcolor`: Color - overrides the background colour, used to fill the circle.
        * `lw`: number - overrides the linewidth of the vertext outline.
        * `radius`: number - overrides the radius of the vertex circle.
        * `font`: str - overrides the name of the font to use for the text label.
        * `text_size`: number - overrides the size of the font to use for the text label.

        **Returns**

        The new vertex object

        **Usage**

        Normally it is only necessary to specify the `position` and `label` for the vertex. By default the style of the
        vertex is determined by the parameters of the parent `Graph` object.

        It is only necessary to set the fgcolor, bgcolor, lw, radius, font, and text_size parameters if you wish to
        override the values set for the `Graph` object, for example to make a particular vertex a different colour.
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
        so it is not necessary to use this call directly to draw a graph.

        **Parameters**

        * `ctx`: drawing context - the drawing context where the vertex will be drawn
        * `fgcolor`: Color - the default foreground colour, used for outline and text.
        * `bgcolor`: Color - the default background colour, used to fill the circle.
        * `lw`: number - the default linewidth of the vertext outline.
        * `radius`: number - the default radius of the vertex circle.
        * `font`: str - the default name of the font to use for the text label.
        * `text_size`: number - the default size of the font to use for the text label.

        **Returns**

        None

        **Usage**

        The `draw` function is usually called by the parent `Graph`. It passes in default values for all the colour and
        style parameters fgcolor, bgcolor, lw, radius, font, and text_size.

        If any of these parameters have been overridden in the constructor, the override values will be used instead.
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
        """
        Represents an edge in a graph. This appears as a line between two vertices.

        **Parameters**

        * `start`: int - the index of the start vertex.
        * `end`: int - the index of the end vertex.
        * `directed`: bool - true for a directed edge.
        * `weight`: number - the weight of the edge, leave at None for unweighted.
        * `offset`: (number, number) - controls the offset of the weight text, leave at None for default.
        * `curve`: bool - true for a curved edge.
        * `curvature`: number - adjusts the default curvature of a curved edge.
        * `color`: Color - overrides the colour, used for line and text.
        * `lw`: number - overrides the linewidth of the edge line.
        * `font`: str - overrides the name of the font to use for the edge weight.
        * `text_size`: number - overrides the size of the font to use for the edge weight.
        * `loop-radius`: number - overrides the radius of a loop edge.
        * `loop-angle`: number - sets the angular position of a loop edge.

        **Returns**

        The new vertex object

        **Usage**

        The `start` and `end` parameters should contain the index of the start and end vertices. This is based on the order
        that the vertices were added to the `Graph` object. 0 for the first vertex added, 1 for the second etc.

        To draw a straight edge, only the `start` and `end` values are needed.

        To make the edge directed, set the `directed` flag true. An arrow will be drawn on the edge, pointing towards the
        `end` vertex. To reverse the direction of the arrow, swap the vertices.

        To make the edge weighted, set `weighted` to any number. The text will be added to label the edge. If the text is
        not positioned correctly, use the `offset` to adjust it. This is an (x, y) value that positions the centre of the
        weight label relative to the centre of the edge.

        To make the edge curved, set the `curve` flag true. This is useful if there are several edges between the same two
        vertices. To adjust the curve, the `curvature` value can be set to a value slightly different to 1. To make the
        line curve in the opposite direction, either swap the vertices or set the curvature to -1.

        To draw a loop instead of a normal edge, set `start` and `end` to point to the same vertex. That is usually all that
        is needed. It is possible to change the `loop-radius` to make the loop bigger or smaller, and the `loop-angle` to
        reposition the loop round the edge of the vertex.

        The `directed` and `weighted` parameters can be used with curves or loops.

        It is only necessary to set the color, lw, font, and text_size parameters if you wish to
        override the values set for the `Graph` object, for example to make a particular edge a different colour.
        """
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
        """
        Draw the edge to the drawing context. This will usually be called by the `Graph` object that owns the edge,
        so it is not necessary to use this call directly to draw a graph.

        **Parameters**

        * `ctx`: drawing context - the drawing context where the vertex will be drawn.
        * `vertices`: list[Vertex] - list of vertices in the graph.
        * `color`: Color - the default colour, used for the line and text.
        * `lw`: number - the default linewidth of the edge tline.
        * `font`: str - the default name of the font to use for the text label.
        * `text_size`: number - the default size of the font to use for the text label.
        * `vertex_radius`: number - the default vertex radius for the graph. This is needed to draw loops correctly.

        **Returns**

        None

        **Usage**

        The `draw` function is usually called by the parent `Graph`. It passes in default values for all the colour and
        style parameters color, lw, font, and text_size.

        If any of these parameters have been overridden in the constructor, the override values will be used instead.
        """
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
        """
        Helper method for drawing an arc between two points.
        """
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
        """
        Draws graphs.

        **Parameters**

        * `vertices`: list[Vertex] - list of vertices for the graph.
        * `edges`: list[Edge] - list of edges for the graph.
        * `fgcolor`: Color - sets the default foreground colour, used for outline and text.
        * `bgcolor`: Color - sets the default background colour, used to fill the circle.
        * `lw`: number - sets the default linewidth of the vertex outline.
        * `radius`: number - sets the default radius of the vertex circle.
        * `font`: str - sets the default name of the font to use for the text label.
        * `text_size`: number - sets the default size of the font to use for the text label.

        **Returns**

        The new vertex object

        **Usage**
        A `Graph` holds a list of vertices and a list of edges, plus some styling parameters. It uses these to draw a
        graph diagram.
        
        The list of vertices can either be passed in to this constructor, or set individually by calling `add` and passing
        in `Vertex` objects, or a combination of both.

        The list of edges can either be passed in to this constructor, or set individually by calling `add` and passing
        in `Edge` objects, or a combination of both.

        The fgcolor, bgcolor, lw, radius, font, and text_size parameters set default values that will apply to every
        edge and vertex. It is possible to override any of these parameters for a particular edge or vertex, in the
        `Edge` or `Vertex` constructors. This is useful for highlighting particular edges and vertices
        """
        self.vertices = vertices if vertices else []
        self.edges = edges if edges else []
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.lw = lw
        self.radius = radius
        self.font = font
        self.text_size = text_size

    def add(self, item):
        """
        Add items (`Vertex` or `Edge` objects) to the graph.
        
        **Parameters**

        * `item`: obj - item to add. Can be a `Vertex` or `Edge` object.

        **Returns**

        None
        """
        if isinstance(item, Vertex):
            self.vertices.append(item)
        if isinstance(item, Edge):
            self.edges.append(item)

    def draw(self, ctx):
        """
        Draw the complete graph to the drawing context. Call this method after creating the `Graph` and adding the
        required edges and vertices.

        **Parameters**

        * `ctx`: drawing context - the drawing context where the vertex will be drawn.

        **Returns**

        None
        """
        for edge in self.edges:
            edge.draw(ctx, self.vertices, self.fgcolor, self.lw, self.font, self.text_size, self.radius)
        for vertex in self.vertices:
            vertex.draw(ctx, self.fgcolor, self.bgcolor, self.radius, self.lw, self.font, self.text_size)
