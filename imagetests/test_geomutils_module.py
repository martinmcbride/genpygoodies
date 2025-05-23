import math
import unittest

from generativepy.color import Color
from generativepy.drawing import make_image, setup
from generativepy.geometry import Polygon, Transform, Circle, Line
from generativepy.math import Vector as V
from genpygoodies.geomutils import LN, label_line, label_point, label_angle, TO

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

    def test_label_point(self):

        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))
            for i in range(16):
                x = 100 + (i%4) * 150
                y = 100 + (i//4) * 100
                a = i*math.pi/8
                p = V(x, y)
                Circle(ctx).of_center_radius(p, 4).fill(Color(0))
                label_point(ctx, f"i = {i}", p, a, Color(0))

        def creator(file):
            make_image(file, draw, 700, 500)

        self.assertTrue(run_image_test('test_label_point.png', creator))

    def test_label_angle(self):

        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))
            for i in range(16):
                x = 200 + (i%4) * 200
                y = 200 + (i//4) * 200
                ang1 = (i-1)*math.pi/8
                ang2 = (i + 1)*math.pi/8
                b = V(x, y)
                a = b + V.polar(100, ang1)
                c = b + V.polar(100, ang2)
                Line(ctx).of_start_end(b, a).stroke(Color(0), 2)
                Line(ctx).of_start_end(b, c).stroke(Color(0), 2)
                label_angle(ctx, f"x", a, b, c, Color(0), offset=5*TO)

        def creator(file):
            make_image(file, draw, 1000, 1000)

        self.assertTrue(run_image_test('test_label_angle.png', creator))

    def test_label_angle_degrees(self):

        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))
            adjust = [
            V(0, 0), V(0, -5), V(5, 0), V(5, 5),
            V(0, 5), V(0, 0), V(0, 0), V(0, 0),
            V(0, 0), V(0, 5), V(0, 0), V(0, 0),
            V(5, 0), V(5, 0), V(5, 0), V(0, 5),
            ]
            for i in range(16):
                x = 200 + (i%4) * 200
                y = 200 + (i//4) * 200
                ang1 = (i-1)*math.pi/8
                ang2 = (i + 1)*math.pi/8
                b = V(x, y)
                a = b + V.polar(100, ang1)
                c = b + V.polar(100, ang2)
                Line(ctx).of_start_end(b, a).stroke(Color(0), 2)
                Line(ctx).of_start_end(b, c).stroke(Color(0), 2)
                label_angle(ctx, f"30°", a, b, c, Color(0), offset=7*TO, adjust=adjust[i])

        def creator(file):
            make_image(file, draw, 1000, 1000)

        self.assertTrue(run_image_test('test_label_angle_degrees.png', creator))

