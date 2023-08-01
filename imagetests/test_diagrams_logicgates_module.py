import math
import unittest

from generativepy.color import Color
from generativepy.drawing import setup, make_image
from generativepy.geometry import Line
from generativepy.math import Vector as V

from genpygoodies.diagrams.logicgates import Not
from image_test_helper import run_image_test

"""
Test the diagrams.logicgates module.
"""

class TestLogicGatesImages(unittest.TestCase):

    def test_not_gate(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            gate = (Not().of_corner_size((200, 200), 50).fillstyle(Color("yellow")).strokestyle(Color("blue"), 3))
            gate.draw(ctx)
            in_pos = V(gate.get_connector(0, 0))
            out_pos = V(gate.get_connector(1, 0))
            print(in_pos, out_pos)
            Line(ctx).of_start_end(in_pos, in_pos + V(-30, 0)).stroke(Color("blue"), 3)
            Line(ctx).of_start_end(out_pos, out_pos + V(50, 0)).stroke(Color("green"), 3)

        def creator(file):
            make_image(file, draw, 800, 400)

        self.assertTrue(run_image_test('test_not_gate.png', creator))
