import unittest

from generativepy.color import Color
from generativepy.drawing import setup, make_image
from generativepy.geometry import Transform

from genpygoodies.diagrams.graph import Graph, Vertex, Edge
from image_test_helper import run_image_test

"""
Test the diagrams.graph module.
"""


class TestGraphImages(unittest.TestCase):

    def test_default_graph(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            graph = Graph()
            graph.add(Vertex((100, 100), "A"))
            graph.add(Vertex((100, 300), "B"))
            graph.add(Vertex((200, 50), "C"))
            graph.add(Vertex((300, 200), "D"))
            graph.add(Edge(0, 1))
            graph.add(Edge(1, 3))
            graph.add(Edge(2, 0))
            graph.add(Edge(3, 2))
            graph.draw(ctx)

            with Transform(ctx).translate(400, 0):
                graph = Graph()
                graph.add(Vertex((200, 100), "1"))
                graph.add(Vertex((300, 250), "2"))
                graph.add(Vertex((200, 300), "3"))
                graph.add(Vertex((100, 200), "4"))
                graph.add(Edge(0, 1))
                graph.add(Edge(1, 2))
                graph.add(Edge(2, 3))
                graph.add(Edge(3, 0))
                graph.add(Edge(1, 3))
                graph.add(Edge(0, 2))
                graph.draw(ctx)

        def creator(file):
            make_image(file, draw, 800, 400)

        self.assertTrue(run_image_test('test_default_graph.png', creator))

class TestGraphImages(unittest.TestCase):

    def test_default_graph(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # graph = Graph()
            # graph.add(Vertex((100, 100), "A"))
            # graph.add(Vertex((100, 300), "B"))
            # graph.add(Vertex((200, 50), "C"))
            # graph.add(Vertex((300, 200), "D"))
            # graph.add(Edge(0, 1, curve=True))
            # graph.add(Edge(1, 0))
            # graph.add(Edge(2, 3, curve=True))
            # graph.add(Edge(2, 3))
            # graph.draw(ctx)

            with Transform(ctx).translate(400, 0):
                graph = Graph()
                graph.add(Vertex((100, 100), "A"))
                graph.add(Vertex((100, 300), "B"))
                graph.add(Vertex((200, 50), "C"))
                graph.add(Vertex((300, 200), "D"))
                graph.add(Edge(1, 0, curve=True))
                graph.add(Edge(0, 2, curve=True))
                graph.add(Edge(2, 3, curve=True))
                graph.add(Edge(3, 1, curve=True))
                graph.draw(ctx)

        def creator(file):
            make_image(file, draw, 1200, 800)

        self.assertTrue(run_image_test('test_curve_graph.png', creator))

