import math
import unittest

from generativepy.color import Color
from generativepy.drawing import setup, make_image, CENTER, MIDDLE, RIGHT, BOTTOM, LEFT, TOP, BUTT, ROUND
from generativepy.geometry import Line, Text, Circle, FillParameters, StrokeParameters, Transform

from generativepy.math import Vector as V

from genpygoodies.diagrams.connectors import Connector, Connection, ElbowConnector
from genpygoodies.diagrams.logicgates import Buffer, And, Or, Xor
from image_test_helper import run_image_test

green_stroke = StrokeParameters(Color("darkgreen"), 4, cap=ROUND)
green_fill = FillParameters(Color("darkgreen"))


"""
Test the diagrams.connector module.
"""

class TestConnectors(unittest.TestCase):

    def test_connector_connection(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            a = (100, 200)
            b = (300, 100)
            Connector(a, b).strokestyle(green_stroke).draw(ctx)
            with Transform(ctx).translate(50, 50):
                Connector(a, b).strokestyle(green_stroke).draw(ctx)
                Connection(a, 4).fillstyle(green_fill).draw(ctx)
                Connection(b, 4).fillstyle(green_fill).draw(ctx)

        def creator(file):
            make_image(file, draw, 400, 300)

        self.assertTrue(run_image_test('test_connector_connection.png', creator))

    def test_elbow_connector(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            a = (100, 100)
            b = (200, 150)
            ElbowConnector(a, b, 0.3).strokestyle(green_stroke).draw(ctx)
            with Transform(ctx).translate(50, 70):
                ElbowConnector(a, b, 0.9, False).strokestyle(green_stroke).draw(ctx)

        def creator(file):
            make_image(file, draw, 400, 300)

        self.assertTrue(run_image_test('test_elbow_connector.png', creator))

