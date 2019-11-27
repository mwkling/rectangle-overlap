import math

# This strategy finds all overlaps for all rectangles, then computes a vector for each rectangle
# in the opposite direction of all it overlaps, normalizes and translates by that distance
class Separation:
    def __init__(self, rectangles):
        self.rectangles = rectangles

    def translate_vector(self, idx):
        rect = self.rectangles[idx]

        overlap_vectors = [rect.center_vec(r) for i, r in enumerate(self.rectangles)
                if i != idx and rect.overlap(r)]

        if len(overlap_vectors) == 0:
            return (0, 0)
        else:
            # This adds up vectors from each overlap if there were multiple
            return list(map(sum, zip(*overlap_vectors)))

    def normalize(self, pair):
        mag = math.sqrt(pair[0]**2 + pair[1]**2)
        if mag == 0:
            return pair
        else:
            return (pair[0] / mag, pair[1] / mag)

    def step(self):
        vecs = [self.normalize(self.translate_vector(i)) for i in range(len(self.rectangles))]
        for i, r in enumerate(self.rectangles):
            r.left += vecs[i][0]
            r.top += vecs[i][1]
