import math
import unittest

from generativepy.color import Color
from generativepy.drawing import make_image, setup
from generativepy.geometry import Polygon, Transform
from generativepy.math import Vector as V
from genpygoodies.geomutils import LN, label_line

from image_test_helper import run_image_test

"""
Test the geomuitils module.
"""

class TestGeomutils(unittest.TestCase):

    def test_label_line(self):

        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))
            with Transform(ctx).translate(350, 250):
                p = [V.polar(200, (i + 0.5)*math.pi/8) for i in range(16)]
                Polygon(ctx).of_points(p).stroke(LN(Color(0)))
                for i, (a, b) in enumerate(zip(p, p[1:] + p[0:1])):
                    label_line(ctx, f"a = {i}", b, a, Color(0))

        def creator(file):
            make_image(file, draw, 700, 500)

        self.assertTrue(run_image_test('test_label_line.png', creator))

