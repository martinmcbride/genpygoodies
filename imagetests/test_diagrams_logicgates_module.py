import math
import unittest

from generativepy.color import Color
from generativepy.drawing import setup, make_image, CENTER, MIDDLE, RIGHT, BOTTOM, LEFT, TOP, BUTT, ROUND
from generativepy.geometry import Line, Text, Circle, FillParameters, StrokeParameters

from generativepy.math import Vector as V

from genpygoodies.diagrams.logicgates import Buffer, And, Or, Xor, BoxItem
from image_test_helper import run_image_test

green_stroke = StrokeParameters(Color("darkgreen"), 4, cap=ROUND)
grey_fill = FillParameters(Color(0.8))

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

            gate = Buffer((100, 200), 50, invert=True).fillstyle(grey_fill).strokestyle(green_stroke)
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

            gate = And((100, 200), 50, invert=True).fillstyle(grey_fill).strokestyle(green_stroke)
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
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("red"), 3, cap=BUTT)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("red"), 3, cap=BUTT)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3, cap=BUTT)

            Text(ctx).of("A", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-15, -5).fill(Color(0))
            Text(ctx).of("B", in_pos2).size(20).align(RIGHT, TOP).offset(-15, 5).fill(Color(0))
            Text(ctx).of("C", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("X", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

            gate = Or((100, 200), 50, invert=True).fillstyle(grey_fill).strokestyle(green_stroke)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("red"), 3, cap=BUTT)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("red"), 3, cap=BUTT)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3, cap=BUTT)

            Text(ctx).of("D", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-15, -5).fill(Color(0))
            Text(ctx).of("E", in_pos2).size(20).align(RIGHT, TOP).offset(-15, 5).fill(Color(0))
            Text(ctx).of("F", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("Y", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

        def creator(file):
            make_image(file, draw, 400, 300)

        self.assertTrue(run_image_test('test_or_gate.png', creator))

    def test_xor_gate(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            gate = Xor((100, 100), 50).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

            Text(ctx).of("A", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-20, -5).fill(Color(0))
            Text(ctx).of("B", in_pos2).size(20).align(RIGHT, TOP).offset(-20, 5).fill(Color(0))
            Text(ctx).of("C", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("X", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

            gate = Xor((100, 200), 50, invert=True).fillstyle(grey_fill).strokestyle(green_stroke)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

            Text(ctx).of("D", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-20, -5).fill(Color(0))
            Text(ctx).of("E", in_pos2).size(20).align(RIGHT, TOP).offset(-20, 5).fill(Color(0))
            Text(ctx).of("F", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("Y", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

        def creator(file):
            make_image(file, draw, 400, 300)

        self.assertTrue(run_image_test('test_xor_gate.png', creator))


    def test_box_item(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            gate = BoxItem((50, 50), 100).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            out_pos = V(gate.get_connector(1, 0))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(30, 0)).stroke(Color("green"), 3)

            Text(ctx).of("A", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-20, -5).fill(Color(0))
            Text(ctx).of("B", in_pos2).size(20).align(RIGHT, BOTTOM).offset(-20, -5).fill(Color(0))
            Text(ctx).of("C", out_pos).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("X", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

            gate = BoxItem((250, 50), 100, height=150, left_connections=3, right_connections=2).fillstyle(Color("white")).strokestyle(Color("black"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            in_pos2 = V(gate.get_connector(0, 1))
            in_pos3 = V(gate.get_connector(0, 2))
            out_pos1 = V(gate.get_connector(1, 0))
            out_pos2 = V(gate.get_connector(1, 1))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("black"), 3)
            Line(ctx).of_start_end(in_pos2, in_pos2 + V(-30, 0)).stroke(Color("black"), 3)
            Line(ctx).of_start_end(in_pos3, in_pos3 + V(-30, 0)).stroke(Color("black"), 3)
            Line(ctx).of_start_end(out_pos1, out_pos1 + V(30, 0)).stroke(Color("black"), 3)
            Line(ctx).of_start_end(out_pos2, out_pos2 + V(30, 0)).stroke(Color("black"), 3)

            Text(ctx).of("A", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-20, -5).fill(Color(0))
            Text(ctx).of("B", in_pos2).size(20).align(RIGHT, BOTTOM).offset(-20, -5).fill(Color(0))
            Text(ctx).of("Ci", in_pos3).size(20).align(RIGHT, BOTTOM).offset(-20, -5).fill(Color(0))
            Text(ctx).of("S", out_pos1).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("Co", out_pos2).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("Adder", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))

            gate = BoxItem((50, 200), 150, left_connections=1, right_connections=2, top_connections=1, bottom_connections=2).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3)
            gate.draw(ctx)
            in_pos1 = V(gate.get_connector(0, 0))
            out_pos1 = V(gate.get_connector(1, 0))
            out_pos2 = V(gate.get_connector(1, 1))
            top_pos1 = V(gate.get_connector(2, 0))
            bottom_pos1 = V(gate.get_connector(3, 0))
            bottom_pos2 = V(gate.get_connector(3, 1))
            Line(ctx).of_start_end(in_pos1, in_pos1 + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos1, out_pos1 + V(30, 0)).stroke(Color("green"), 3)
            Line(ctx).of_start_end(out_pos2, out_pos2 + V(30, 0)).stroke(Color("green"), 3)
            Line(ctx).of_start_end(top_pos1, top_pos1 + V(0, -30)).stroke(Color("black"), 3)
            Line(ctx).of_start_end(bottom_pos1, bottom_pos1 + V(0, 30)).stroke(Color("red"), 3)
            Line(ctx).of_start_end(bottom_pos2, bottom_pos2 + V(0, 30)).stroke(Color("red"), 3)

            Text(ctx).of("Ck", in_pos1).size(20).align(RIGHT, BOTTOM).offset(-20, -5).fill(Color(0))
            Text(ctx).of("Q", out_pos1).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("Q'", out_pos2).size(20).align(LEFT, BOTTOM).offset(10, -5).fill(Color(0))
            Text(ctx).of("A", top_pos1).size(20).align(LEFT, BOTTOM).offset(5, -5).fill(Color(0))
            Text(ctx).of("J", bottom_pos1).size(20).align(LEFT, TOP).offset(5, 5).fill(Color(0))
            Text(ctx).of("K", bottom_pos2).size(20).align(LEFT, TOP).offset(5, 5).fill(Color(0))
            Text(ctx).of("X", gate.label_pos()).size(20).align(CENTER, MIDDLE).fill(Color(0))



        def creator(file):
            make_image(file, draw, 400, 400)

        self.assertTrue(run_image_test('test_box_item.png', creator))
