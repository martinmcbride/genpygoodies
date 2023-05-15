import unittest

from generativepy.color import Color
from generativepy.drawing import setup, make_image

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
            graph.add(Vertex((200, 150), "C"))
            graph.add(Edge(0, 1))
            graph.add(Edge(0, 1, curve=True))
            graph.add(Edge(1, 0, curve=True))
            graph.draw(ctx)

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_default_graph.png', creator))

