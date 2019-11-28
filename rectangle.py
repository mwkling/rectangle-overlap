import itertools
import math

class Rectangle:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        # So we can track how far the rectangle moved from original position
        self.original_left = left
        self.original_top = top

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def original_right(self):
        return self.original_left + self.width

    @property
    def original_bottom(self):
        return self.original_top + self.height

    @property
    def midx(self):
        return (self.left + self.right) / 2

    @property
    def midy(self):
        return (self.top + self.bottom) / 2

    @property
    def original_midx(self):
        return (self.original_left + self.original_right) / 2

    @property
    def original_midy(self):
        return (self.original_top + self.original_bottom) / 2

    @property
    def distance_from_original(self):
        return math.sqrt((self.left - self.original_left) ** 2 + (self.top - self.original_top) ** 2)

    def overlap(self, other):
        if(self.left >= other.right or other.left >= self.right): 
            return False
        if(self.top >= other.bottom or other.top >= self.bottom): 
            return False
        return True

    def overlapx(self, other):
        return max(0, min(self.right, other.right) - max(self.left, other.left))

    def overlapy(self, other):
        return max(0, min(self.bottom, other.bottom) - max(self.top, other.top))

    def center_vec(self, other):
        return (self.midx - other.midx, self.midy - other.midy)

    def as_tuple(self):
        return (self.left, self.top, self.width, self.height)

    def __str__(self):
        return "Rect" + str(self.as_tuple())

    @staticmethod
    def has_overlaps(rectangles):
        for (r1, r2) in itertools.combinations(rectangles, 2):
            if r1.overlap(r2):
                return True
        return False

    @staticmethod
    def total_movement(rectangles):
        return sum([r.distance_from_original for r in rectangles])
