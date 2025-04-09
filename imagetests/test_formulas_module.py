import unittest

from generativepy.color import Color
from generativepy.drawing import make_image

from genpygoodies.formula import make_formulas_png
from image_test_helper import run_image_test

"""
Test the formulas module.
"""

class TestFormulas(unittest.TestCase):

    def test_single_formula(self):

        def creator(file):
            width, height = make_formulas_png(file, [r"x^2"], Color("red"))
            self.assertEquals(width, 174)
            self.assertEquals(height, 174)

        self.assertTrue(run_image_test('test_single_formula.png', creator))

    def test_multiple_formulas(self):

        def creator(file):
            width, height = make_formulas_png(file, [r"c^2 = a^2 + b^2", r"\frac{a+b}{c+d} + 3.141592654", r"\frac{a+b}{c+d} + 3.141592654", r"c^2 = a^2 + b^2"], Color("black"), dpi=300, gap=30, background=Color("cadetblue"))
            self.assertEquals(width, 424)
            self.assertEquals(height, 404)

        self.assertTrue(run_image_test('test_multiple_formulas.png', creator))

