import unittest
import math
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rectangle import Rectangle

class TestRectangle(unittest.TestCase):
    def test_dimensions(self):
        r = Rectangle(10, 20, 30, 50)
        self.assertEqual(r.right, 10 + 30)
        self.assertEqual(r.bottom, 20 + 50)
        self.assertEqual(r.area, 1500)
        self.assertEqual(r.midx, 25)
        self.assertEqual(r.midy, 45)

    def test_movex(self):
        r = Rectangle(10, 20, 30, 50)
        r.left = 5

        self.assertEqual(r.original_left, 10)
        self.assertEqual(r.left, 5)
        self.assertEqual(r.deltax, 5)
        self.assertEqual(r.distance_from_original, 5)

    def test_movey(self):
        r = Rectangle(10, 20, 30, 50)
        r.top = 5

        self.assertEqual(r.original_top, 20)
        self.assertEqual(r.top, 5)
        self.assertEqual(r.deltay, 15)
        self.assertEqual(r.distance_from_original, 15)

    def test_movexy(self):
        r = Rectangle(10, 20, 30, 50)
        r.top = 16
        r.left = 7

        self.assertEqual(r.deltay, 4)
        self.assertEqual(r.deltax, 3)
        self.assertEqual(r.distance_from_original, 5)

    def test_basic_overlap(self):
        r1 = Rectangle(0, 0, 10, 10)
        r2 = Rectangle(5, 5, 10, 10)

        self.assertTrue(r1.overlap(r2))
        self.assertEqual(r1.overlapx(r2), 5)
        self.assertEqual(r1.overlapy(r2), 5)
        self.assertEqual(r1.overlap_rect(r2).area, 25)

    def test_cross_overlap(self):
        r1 = Rectangle(0, 5, 10, 1)
        r2 = Rectangle(5, 0, 1, 10)

        self.assertTrue(r1.overlap(r2))
        self.assertEqual(r1.overlapx(r2), 1)
        self.assertEqual(r1.overlapy(r2), 1)
        self.assertEqual(r1.overlap_rect(r2).area, 1)

    def test_contained_overlap(self):
        r1 = Rectangle(0, 0, 10, 10)
        r2 = Rectangle(5, 5, 2, 2)

        self.assertTrue(r1.overlap(r2))
        self.assertEqual(r1.overlapx(r2), 2)
        self.assertEqual(r1.overlapy(r2), 2)
        self.assertEqual(r1.overlap_rect(r2).area, 4)

    def test_border_not_overlap(self):
        r1 = Rectangle(0, 0, 10, 10)
        r2 = Rectangle(10, 0, 10, 10)
        self.assertFalse(r1.overlap(r2))

    def test_rotate(self):
        r1 = Rectangle(0, 0, 1, 1)
        r1.left = 5

        self.assertEqual(r1.original_top, 0)
        self.assertEqual(r1.original_left, 0)
        self.assertEqual(r1.deltax, -5)

        r1.rotate(math.pi / 2)

        self.assertAlmostEqual(r1.left, 0)
        self.assertAlmostEqual(r1.top, -5)

if __name__ == '__main__':
    unittest.main()
