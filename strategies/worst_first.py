import itertools

# This strategy looks for the largest overlaps (by area) in each step, moves one of the
# overlapping rectangles along the X or Y axis to eliminate the overlap, then repeats
class WorstFirst:
    def __init__(self, rectangles):
        self.rectangles = rectangles

    def step(self):
        overlaps = [(r1, r2, r1.overlap_rect(r2).area) for r1, r2 in
                    itertools.combinations(self.rectangles, 2) if r1.overlap(r2)]

        r1, r2, _ = max(overlaps, key=lambda o: o[2])

        overlapx = r1.overlapx(r2)
        overlapy = r1.overlapy(r2)

        # See which distance is bigger (x or y overlap) and move one of
        # the rectangles so they no longer overlap
        if overlapx > overlapy:
            if abs(r1.bottom - r2.top) < abs(r1.top - r2.bottom):
                r2.top = r1.bottom
            else:
                r1.top = r2.bottom
        else:
            if abs(r1.left - r2.right) < abs(r1.right - r2.left):
                r1.left = r2.right
            else:
                r2.left = r1.right
