import math
import unittest

from generativepy.color import Color
from generativepy.drawing import setup, make_image, CENTER, MIDDLE, RIGHT, BOTTOM, LEFT, TOP
from generativepy.geometry import Line, Text, Circle
from generativepy.math import Vector as V

from genpygoodies.diagrams.logicgates import Buffer, And, Or
from image_test_helper import run_image_test

"""
Test the diagrams.logicgates module.
"""

class TestLogicGatesImages(unittest.TestCase):

    def test_buffer_gate(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            gate = Buffer((100, 100), 50).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos = V(gate.get_connector(0, 0))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos, in_pos + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

            Text(ctx).of("A", in_pos).size(20).align(RIGHT, BOTTOM).offset(-10, -5).fill(Color(0))
            Text(ctx).of("B", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("X", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

            gate = Buffer((100, 200), 50, invert=True).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

            Text(ctx).of("C", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-10, -5).fill(Color(0))
            Text(ctx).of("D", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("Y", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

        def creator(file):
            make_image(file, draw, 400, 300)

        self.assertTrue(run_image_test('test_buffer_gate.png', creator))

    def test_and_gate(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            gate = And((100, 100), 50).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

            Text(ctx).of("A", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-10, -5).fill(Color(0))
            Text(ctx).of("B", in_pos2).size(20).align(RIGHT, TOP).offset(-10, 5).fill(Color(0))
            Text(ctx).of("C", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("X", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

            gate = And((100, 200), 50, invert=True).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

            Text(ctx).of("D", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-10, -5).fill(Color(0))
            Text(ctx).of("E", in_pos2).size(20).align(RIGHT, TOP).offset(-10, 5).fill(Color(0))
            Text(ctx).of("F", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("Y", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

        def creator(file):
            make_image(file, draw, 400, 300)

        self.assertTrue(run_image_test('test_and_gate.png', creator))

    def test_or_gate(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            gate = Or((100, 100), 50).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

            Text(ctx).of("A", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-10, -5).fill(Color(0))
            Text(ctx).of("B", in_pos2).size(20).align(RIGHT, TOP).offset(-10, 5).fill(Color(0))
            Text(ctx).of("C", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("X", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

            gate = Or((100, 200), 50, invert=True).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

            Text(ctx).of("D", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-10, -5).fill(Color(0))
            Text(ctx).of("E", in_pos2).size(20).align(RIGHT, TOP).offset(-10, 5).fill(Color(0))
            Text(ctx).of("F", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("Y", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

        def creator(file):
            make_image(file, draw, 400, 300)

        self.assertTrue(run_image_test('test_or_gate.png', creator))
